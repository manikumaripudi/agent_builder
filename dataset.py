
# from dotenv import load_dotenv
# import streamlit as st
# import os
# import PyPDF2  # Library to handle PDFs
# import google.generativeai as genai

# load_dotenv()  
# genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


# def get_gemini_response(file_content, input, prompt):
#     generation_config = {
#         "temperature": 1,
#         "top_p": 0.95,
#         "top_k": 64,
#         "max_output_tokens": 8192,
#     }
#     model =genai.GenerativeModel(
#         'gemini-1.5-pro',
#         system_instruction=["""Your task is to generate diatance,cost,weather report and local news  for the user provided file based on given location"""]
#     )

#     if input != "":
#         response = model.generate_content([file_content,input,prompt], generation_config=generation_config,stream=True)
#     else:
#         response = model.generate_content(file_content, generation_config=generation_config,stream=True)
    
#     result = ""
#     for message in response["candidates"]:
#         result += message["content"]
#     return result


# # Function to process the uploaded file (specifically for PDFs)
# def process_uploaded_file(uploaded_file):
#     file_content = None

#     if "pdf" in uploaded_file.type:
#         try:
#             # Read the PDF content using PyPDF2
#             pdf_reader = PyPDF2.PdfReader(uploaded_file)
#             pdf_text = ""
#             for page_num in range(len(pdf_reader.pages)):
#                 page = pdf_reader.pages[page_num]
#                 pdf_text += page.extract_text()
#             st.text_area("Uploaded PDF Content", pdf_text[:500])  # Display first 500 characters of the PDF
#             file_content = pdf_text
#         except Exception as e:
#             st.error(f"Error reading the PDF file: {str(e)}")
    
#     return file_content


# # Process user input
# def process_input(file_content, input, prompt):
#     """Process the user input."""
#     try:
#         response = get_gemini_response(file_content, input, prompt)
#         return response
#     except Exception as e:
#         st.error(f"Error processing the input: {str(e)}")
#         return None


# # Example output format
# Example_Output = """[{"Location: New York, NY, USA","Distance (km)": 3000,"Cost ($)": 1500,"Weather Report" : "Sunny","Local News":"New York Times: City Council approves new budget"}]"""
# prompt = f"""You are an AI assistant designed to help users explore and analyze user input.\n{Example_Output}\nFind the local news and a small description about this."""

# st.subheader(":green[Gemini] Agent Builder", divider="violet")

# # Sidebar for additional settings
# st.sidebar.header("Local News", divider="green")

# # Upload file using Streamlit's file uploader
# uploaded_file = st.sidebar.file_uploader("**Choose a file**", type=["pdf"])

# file_content = None
# if uploaded_file is not None:
#     file_content = process_uploaded_file(uploaded_file)

# # Initialize chat history
# if 'chat_history' not in st.session_state:
#     st.session_state.chat_history = []

# input = st.chat_input("Enter your prompt")

# # Handle user input
# if input:
#     if not file_content:
#         st.error("Please upload a file before entering the prompt.")
#     else:
#         # Add user input (question) to chat history
#         st.session_state.chat_history.append({"role": "user", "content": input})

#         # Process input and display a spinner
#         with st.spinner("Processing..."):
#             response = process_input(file_content, input, prompt)

#         # Add Gemini's response to chat history
#         if response:
#             st.session_state.chat_history.append({"role": "assistant", "content": response})

# # Function to display chat history
# def display_chat_history(chat_history):
#     for message in chat_history:
#         role = message["role"]
#         content = message["content"]
#         with st.chat_message(role):
#             st.markdown(f"**{role.capitalize()}**: {content}")

# # Display chat history
# if st.session_state.chat_history:
#     display_chat_history(st.session_state.chat_history)







# import streamlit as st
# import pandas as pd
# import json

# # Load local dataset using the new caching method
# @st.cache_data
# def load_data(file_path):
#     return pd.read_csv(file_path)

# # Define a function to fetch weather, distance, cost, and news based on supplier input
# def get_supplier_info(supplier_name, data):
#     # Print the column names to verify correct column name usage
#     st.write("Columns in the dataset:", data.columns.tolist())

#     # Filter the dataset based on supplier_name
#     if 'Supplier Name' in data.columns:
#         supplier_data = data[data['Supplier Name'] == supplier_name]

#         if supplier_data.empty:
#             return None

#         # Extract the required data
#         distance = supplier_data['Distance (km)'].values[0]
#         cost = supplier_data['Cost ($)'].values[0]
#         weather_report = json.loads(supplier_data['Weather Report'].values[0])
#         local_news = json.loads(supplier_data['Local News'].values[0])

#         # Return all data as a dictionary (JSON format)
#         return {
#             "supplier_name": supplier_name,
#             "distance": f"{distance} km",
#             "cost": f"${cost}",
#             "weather_report": weather_report,
#             "local_news": local_news
#         }
#     else:
#         st.error("The column 'Supplier Name' does not exist in the dataset.")
#         return None

# # Function to generate a summary (mocked)
# def get_summary(data):
#     summary = (
#         f"Supplier {data['supplier_name']} is located at a distance of {data['distance']}. "
#         f"The cost is {data['cost']}. Current weather conditions report "
#         f"{data['weather_report']['condition']} with a temperature of {data['weather_report']['temperature']}°C. "
#         f"In local news: {data['local_news'][0]['title']} - {data['local_news'][0]['description']}."
#     )
#     return summary

# # Streamlit UI
# def main():
#     st.title("Supplier Information Fetcher")

#     # Hardcoded file path
#     file_path = "C:/Users/mpudi/Downloads/weather_report_sample_data.csv"

#     # Load the dataset
#     data = load_data(file_path)
#     st.write("Dataset loaded successfully!")

#     # Print dataset columns to help with debugging
#     st.write("Columns:", data.columns.tolist())

#     # Input field for supplier name
#     supplier_name = st.text_input("Enter Supplier Name")

#     if st.button("Get Information"):
#         if supplier_name:
#             # Fetch supplier information
#             info = get_supplier_info(supplier_name, data)

#             if info:
#                 # Display fetched information
#                 st.json(info)

#                 # Get and display summary
#                 summary = get_summary(info)
#                 st.write("Summary:")
#                 st.write(summary)
#             else:
#                 st.error("Supplier not found or incorrect column name.")
#         else:
#             st.error("Please enter a supplier name.")

# if __name__ == "__main__":
#     main()







#using static approach#



# import streamlit as st
# import pdfplumber
# import pandas as pd

# # Function to extract tabular data from PDF
# def extract_data_from_pdf(file_path):
#     with pdfplumber.open(file_path) as pdf:
#         # Assuming data is in the first page; adjust as needed
#         page = pdf.pages[0]
#         table = page.extract_table()

#     # Convert extracted table into a DataFrame
#     if table:
#         df = pd.DataFrame(table[1:], columns=table[0])  # Assume first row is header
#         return df
#     else:
#         st.error("No table found in the PDF.")
#         return pd.DataFrame()  # Return an empty DataFrame

# # Define a function to fetch weather, distance, cost, and news based on supplier input
# def get_supplier_info(supplier_name, data):
#     # Remove any leading/trailing spaces from the column names
#     data.columns = data.columns.str.strip()

#     # Ensure the column name matches 'Supplier Name'
#     if 'Supplier Name' in data.columns:
#         supplier_data = data[data['Supplier Name'].str.strip() == supplier_name]

#         if supplier_data.empty:
#             return None

#         # Extract the required data
#         distance = supplier_data['Distance (km)'].values[0]
#         cost = supplier_data['Cost ($)'].values[0]
#         weather_report = supplier_data['Weather Report'].values[0]
#         local_news = supplier_data['Local News'].values[0]

#         # Return all data as a dictionary (JSON format)
#         return {
#             "supplier_name": supplier_name,
#             "distance": f"{distance} km",
#             "cost": f"${cost}",
#             "weather_report": weather_report,
#             "local_news": local_news
#         }
#     else:
#         st.error("The column 'Supplier Name' does not exist in the dataset.")
#         return None

# # Function to generate a summary (mocked)
# def get_summary(data):
#     summary = (
#         f"Supplier {data['supplier_name']} is located at a distance of {data['distance']}. "
#         f"The cost is {data['cost']}. Current weather conditions report "
#         f"{data['weather_report']}. "
#         f"In local news: {data['local_news']}."
#     )
#     return summary

# # Streamlit UI
# def main():
#     st.title("Supplier Information Fetcher")

#     # Use local file path
#     file_path = 'C:/Users/mpudi/Downloads/weather_report_sample_data.pdf'

#     # Extract data from PDF
#     data = extract_data_from_pdf(file_path)

#     if not data.empty:
#         st.write("Data extracted successfully!")
#         st.write("Columns in the dataset:", data.columns.tolist())

#         # Input field for supplier name
#         supplier_name = st.text_input("Enter Supplier Name")

#         if st.button("Get Information"):
#             if supplier_name:
#                 # Fetch supplier information
#                 info = get_supplier_info(supplier_name, data)

#                 if info:
#                     # Display fetched information in JSON format
#                     st.json(info)

#                     # Get and display summary
#                     summary = get_summary(info)
#                     st.write("Summary:")
#                     st.write(summary)
#                 else:
#                     st.error("Supplier not found or incorrect column name.")
#             else:
#                 st.error("Please enter a supplier name.")
#     else:
#         st.error("Failed to extract data from the PDF.")

# if __name__ == "__main__":
#     main()






# import os
# import streamlit as st
# import pdfplumber
# import pandas as pd
# import google.generativeai as genai

# # Configure the Gemini API key
# genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# # Create the Gemini model instance
# generation_config = {
#     "temperature": 1,
#     "top_p": 0.95,
#     "top_k": 64,
#     "max_output_tokens": 8192,
    
# }

# model = genai.GenerativeModel(
#     model_name="gemini-1.5-pro",
#     generation_config=generation_config,
# )

# # Function to extract tabular data from PDF
# def extract_data_from_pdf(file_path):
#     with pdfplumber.open(file_path) as pdf:
#         # Assuming data is in the first page; adjust as needed
#         page = pdf.pages[0]
#         table = page.extract_table()

#     # Convert extracted table into a DataFrame
#     if table:
#         df = pd.DataFrame(table[1:], columns=table[0])  # Assume first row is header
#         return df
#     else:
#         st.error("No table found in the PDF.")
#         return pd.DataFrame()  # Return an empty DataFrame

# # Function to fetch weather, distance, cost, and news based on supplier input
# def get_supplier_info(supplier_name, data):
#     # Remove any leading/trailing spaces from the column names
#     data.columns = data.columns.str.strip()

#     # Ensure the column name matches 'Supplier Name'
#     if 'Supplier Name' in data.columns:
#         supplier_data = data[data['Supplier Name'].str.strip() == supplier_name]

#         if supplier_data.empty:
#             return None

#         # Extract the required data
#         distance = supplier_data['Distance (km)'].values[0]
#         cost = supplier_data['Cost ($)'].values[0]
#         weather_report = supplier_data['Weather Report'].values[0]
#         local_news = supplier_data['Local News'].values[0]

#         # Return all data as a dictionary (JSON format)
#         return {
#             "supplier_name": supplier_name,
#             "distance": f"{distance} km",
#             "cost": f"${cost}",
#             "weather_report": weather_report,
#             "local_news": local_news
#         }
#     else:
#         st.error("The column 'Supplier Name' does not exist in the dataset.")
#         return None

# # Function to generate a summary using Gemini Pro 1.5
# def generate_summary(data):
#     prompt = (
#         f"Create a summary based on the following information:\n\n"
#         f"Supplier Name: {data['supplier_name']}\n"
#         f"Distance: {data['distance']}\n"
#         f"Cost: {data['cost']}\n"
#         f"Weather Report: {data['weather_report']}\n"
#         f"Local News: {data['local_news']}\n"
#     )

#     chat_session = model.start_chat(
#         history=[
#             {
#                 "role": "user",
#                 "parts": [prompt]
#             }
#         ]
#     )

#     response = chat_session.send_message(prompt)
#     return response.text

# # Streamlit UI
# def main():
#     st.title("Supplier Information Fetcher")

#     # Use local file path
#     file_path = 'C:/Users/mpudi/Downloads/weather_report_sample_data.pdf'

#     # Extract data from PDF
#     data = extract_data_from_pdf(file_path)

#     if not data.empty:
#         st.write("Data extracted successfully!")
#         st.write("Columns in the dataset:", data.columns.tolist())

#         # Input field for supplier name
#         supplier_name = st.text_input("Enter Supplier Name")

#         if st.button("Get Information"):
#             if supplier_name:
#                 # Fetch supplier information
#                 info = get_supplier_info(supplier_name, data)

#                 if info:
#                     # Display fetched information in JSON format
#                     st.json(info)

#                     # Generate and display summary using Gemini Pro 1.5
#                     summary = generate_summary(info)
#                     st.write("Summary:")
#                     st.write(summary)
#                 else:
#                     st.error("Supplier not found or incorrect column name.")
#             else:
#                 st.error("Please enter a supplier name.")
#     else:
#         st.error("Failed to extract data from the PDF.")

# if __name__ == "__main__":
#     main()










# #different companies


# import os
# import streamlit as st
# import pdfplumber
# import pandas as pd
# import google.generativeai as genai

# # Configure the Gemini API key
# genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# # Create the Gemini model instance
# generation_config = {
#     "temperature": 1,
#     "top_p": 0.95,
#     "top_k": 64,
#     "max_output_tokens": 8192,
# }

# model = genai.GenerativeModel(
#     model_name="gemini-1.5-pro",
#     generation_config=generation_config,
# )

# # Function to extract tabular data from PDF
# def extract_data_from_pdf(file_path):
#     with pdfplumber.open(file_path) as pdf:
#         page = pdf.pages[0]
#         table = page.extract_table()

#     if table:
#         df = pd.DataFrame(table[1:], columns=table[0])  # Assume first row is header
#         return df
#     else:
#         st.error("No table found in the PDF.")
#         return pd.DataFrame()  # Return an empty DataFrame

# # Function to fetch weather, distance, cost, and news based on supplier input
# def get_supplier_info(supplier_name, data):
#     data.columns = data.columns.str.strip()

#     if 'Supplier Name' in data.columns:
#         supplier_data = data[data['Supplier Name'].str.strip() == supplier_name]

#         if supplier_data.empty:
#             return None

#         distance = supplier_data['Distance (km)'].values[0]
#         cost = supplier_data['Cost ($)'].values[0]
#         weather_report = supplier_data['Weather Report'].values[0]
#         local_news = supplier_data['Local News'].values[0]

#         return {
#             "supplier_name": supplier_name,
#             "distance": f"{distance} km",
#             "cost": f"${cost}",
#             "weather_report": weather_report,
#             "local_news": local_news
#         }
#     else:
#         st.error("The column 'Supplier Name' does not exist in the dataset.")
#         return None

# # Function to generate a summary using Gemini Pro 1.5
# def generate_summary(data):
#     prompt = (
#         f"Create a summary based on the following information:\n\n"
#         f"Supplier Name: {data['supplier_name']}\n"
#         f"Distance: {data['distance']}\n"
#         f"Cost: {data['cost']}\n"
#         f"Weather Report: {data['weather_report']}\n"
#         f"Local News: {data['local_news']}\n"
#     )

#     chat_session = model.start_chat(
#         history=[{"role": "user", "parts": [prompt]}]
#     )

#     response = chat_session.send_message(prompt)
#     return response.text
# import pandas as pd

# # Function to assign company to supplier
# def assign_company_to_supplier(supplier_name):
#     # Define a mapping for suppliers to companies
#     company_mapping = {
#         "Globex Corporation": "Globex Corporation",
#         "Umbrella Corp": "Umbrella Corp",
#         "Stark Industries": "Stark Industries",
#         "Initech": "Initech",
#         "Acme Corporation": "Acme Corporation",
#         "Wayne Enterprises":"Wayne Enterprises"
#     }
    
    

#     # Normalize supplier name for comparison
#     supplier_name_normalized = supplier_name.lower()

#     # Iterate through the mapping and check if the supplier name matches
#     for company, company_name in company_mapping.items():
#         if company.lower() in supplier_name_normalized:
#             return company_name
    

    
    

# # Function to get the best supplier based on distance and cost
# def get_best_supplier(data):
#     data.columns = data.columns.str.strip()

#     if 'Supplier Name' in data.columns and 'Distance (km)' in data.columns and 'Cost ($)' in data.columns:
#         # Convert columns to numeric for comparison
#         data['Distance (km)'] = pd.to_numeric(data['Distance (km)'], errors='coerce')
#         data['Cost ($)'] = pd.to_numeric(data['Cost ($)'], errors='coerce')

#         # Filter rows where both distance and cost are valid
#         valid_data = data.dropna(subset=['Distance (km)', 'Cost ($)'])

#         # Find the supplier with the minimum cost and distance
#         best_supplier = valid_data.loc[
#             (valid_data['Cost ($)'] == valid_data['Cost ($)'].min()) &
#             (valid_data['Distance (km)'] == valid_data['Distance (km)'].min())
#         ]

#         if not best_supplier.empty:
#             best_supplier_name = best_supplier['Supplier Name'].values[0]
#             best_supplier_company = assign_company_to_supplier(best_supplier_name)  # Assign company to supplier
#             return best_supplier_name, best_supplier_company
#         else:
#             return None, None
#     else:
#         st.error("Required columns for comparison are missing in the dataset.")
#         return None, None


# # Streamlit UI
# def main():
#     st.title("Supplier Information Fetcher")

#     # Use local file path
#     file_path = 'C:/Users/mpudi/Downloads/weather_report_sample_data.pdf'

#     # Extract data from PDF
#     data = extract_data_from_pdf(file_path)

#     if not data.empty:
#         st.write("Data extracted successfully!")
#         st.write("Columns in the dataset:", data.columns.tolist())

#         # Input field for supplier name
#         supplier_name = st.text_input("Enter Supplier Name")

#         if st.button("Get Information"):
#             if supplier_name:
#                 # Fetch supplier information
#                 info = get_supplier_info(supplier_name, data)

#                 if info:
#                     # Display fetched information in JSON format
#                     st.json(info)

#                     # Generate and display summary using Gemini Pro 1.5
#                     summary = generate_summary(info)
#                     st.write("Summary:")
#                     st.write(summary)
#                 else:
#                     st.error("Supplier not found or incorrect column name.")
#             else:
#                 st.error("Please enter a supplier name.")

#         # Button to get the best supplier based on distance and cost
#         if st.button("Get Best Supplier"):
#             best_supplier_name, best_supplier_company = get_best_supplier(data)

#             if best_supplier_name:
#                 st.write(f"The best supplier based on lowest cost and distance is {best_supplier_name} from Acme Corporation.")
#             else:
#                 st.error("Could not determine the best supplier.")
#     else:
#         st.error("Failed to extract data from the PDF.")

# if __name__ == "__main__":
#     main()






## worked one....



# import os
# import streamlit as st
# import pdfplumber
# import pandas as pd
# import google.generativeai as genai

# # Configure the Gemini API key
# genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# # Create the Gemini model instance
# generation_config = {
#     "temperature": 1,
#     "top_p": 0.95,
#     "top_k": 64,
#     "max_output_tokens": 8192,
# }

# model = genai.GenerativeModel(
#     model_name="gemini-1.5-pro",
#     generation_config=generation_config,
# )

# # Function to extract tabular data from PDF
# def extract_data_from_pdf(file_path):
#     with pdfplumber.open(file_path) as pdf:
#         # Assuming data is in the first page; adjust as needed
#         page = pdf.pages[0]
#         table = page.extract_table()

#     # Convert extracted table into a DataFrame
#     if table:
#         df = pd.DataFrame(table[1:], columns=table[0])  # Assume first row is header
#         return df
#     else:
#         st.error("No table found in the PDF.")
#         return pd.DataFrame()  # Return an empty DataFrame

# # Function to fetch weather, distance, cost, and news based on supplier input
# def get_supplier_info(supplier_name, data):
#     # Remove any leading/trailing spaces from the column names
#     data.columns = data.columns.str.strip()

#     # Ensure the column name matches 'Supplier Name'
#     if 'Supplier Name' in data.columns:
#         supplier_data = data[data['Supplier Name'].str.strip() == supplier_name]

#         if supplier_data.empty:
#             return None

#         # Extract the required data
#         distance = supplier_data['Distance (km)'].values[0]
#         cost = supplier_data['Cost ($)'].values[0]
#         weather_report = supplier_data['Weather Report'].values[0]
#         local_news = supplier_data['Local News'].values[0]

#         # Return all data as a dictionary (JSON format)
#         return {
#             "supplier_name": supplier_name,
#             "distance": f"{distance} km",
#             "cost": f"${cost}",
#             "weather_report": weather_report,
#             "local_news": local_news
#         }
#     else:
#         st.error("The column 'Supplier Name' does not exist in the dataset.")
#         return None

# # Function to generate a summary using Gemini Pro 1.5
# def generate_summary(data):
#     prompt = (
#         f"Create a summary based on the following information:\n\n"
#         f"Supplier Name: {data['supplier_name']}\n"
#         f"Distance: {data['distance']}\n"
#         f"Cost: {data['cost']}\n"
#         f"Weather Report: {data['weather_report']}\n"
#         f"Local News: {data['local_news']}\n"
#     )

#     chat_session = model.start_chat(
#         history=[
#             {
#                 "role": "user",
#                 "parts": [prompt]
#             }
#         ]
#     )

#     response = chat_session.send_message(prompt)
#     return response.text

# # Function to find the best supplier based on cost and distance
# def find_best_supplier(data):
#     # Remove any leading/trailing spaces from the column names
#     data.columns = data.columns.str.strip()

#     # Ensure the column names are correct
#     if all(col in data.columns for col in ['Supplier Name', 'Distance (km)', 'Cost ($)']):
#         # Convert distance and cost to numeric
#         data['Distance (km)'] = pd.to_numeric(data['Distance (km)'], errors='coerce')
#         data['Cost ($)'] = pd.to_numeric(data['Cost ($)'], errors='coerce')

#         # Drop rows with NaN values in distance or cost
#         data = data.dropna(subset=['Distance (km)', 'Cost ($)'])

#         # Find the supplier with the minimum cost and distance
#         best_supplier = data.loc[data[['Cost ($)', 'Distance (km)']].sum(axis=1).idxmin()]

#         # Format the result
#         return f"The best supplier based on lowest cost and distance is {best_supplier['Supplier Name']} from {best_supplier['Location']}."
#     else:
#         st.error("Required columns are missing in the dataset.")
#         return None

# # Streamlit UI
# def main():
#     st.title("Supplier Information Fetcher")

#     # Use local file path
#     file_path = 'C:/Users/mpudi/Downloads/weather_report_sample_data.pdf'

#     # Extract data from PDF
#     data = extract_data_from_pdf(file_path)

#     if not data.empty:
#         st.write("Data extracted successfully!")
#         st.write("Columns in the dataset:", data.columns.tolist())

#         # Input field for supplier name
#         supplier_name = st.text_input("Enter Supplier Name")

#         if st.button("Get Information"):
#             if supplier_name:
#                 # Fetch supplier information
#                 info = get_supplier_info(supplier_name, data)

#                 if info:
#                     # Display fetched information in JSON format
#                     st.json(info)

#                     # Generate and display summary using Gemini Pro 1.5
#                     summary = generate_summary(info)
#                     st.write("Summary:")
#                     st.write(summary)
#                 else:
#                     st.error("Supplier not found or incorrect column name.")
#             else:
#                 st.error("Please enter a supplier name.")

#         # Find and display the best supplier based on cost and distance
#         best_supplier = find_best_supplier(data)
#         if best_supplier:
#             st.write("Best Supplier Based on Cost and Distance:")
#             st.write(best_supplier)
#     else:
#         st.error("Failed to extract data from the PDF.")

# if __name__ == "__main__":
#     main()










import os
import time
import streamlit as st
import pdfplumber
import pandas as pd
import google.generativeai as genai

# Configure the Gemini API key
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Create the Gemini model instance
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

# Function to extract tabular data from PDF
def extract_data_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        # Assuming data is in the first page; adjust as needed
        page = pdf.pages[0]
        table = page.extract_table()

    # Convert extracted table into a DataFrame
    if table:
        df = pd.DataFrame(table[1:], columns=table[0])  # Assume first row is header
        return df
    else:
        st.error("No table found in the PDF.")
        return pd.DataFrame()  # Return an empty DataFrame

# Function to fetch weather, distance, cost, and news based on supplier input
def get_supplier_info(supplier_name, data):
    # Remove any leading/trailing spaces from the column names
    data.columns = data.columns.str.strip()

    # Ensure the column name matches 'Supplier Name'
    if 'Supplier Name' in data.columns:
        supplier_data = data[data['Supplier Name'].str.strip() == supplier_name]

        if supplier_data.empty:
            return None

        # Extract the required data
        distance = supplier_data['Distance (km)'].values[0]
        cost = supplier_data['Cost ($)'].values[0]
        weather_report = supplier_data['Weather Report'].values[0]
        local_news = supplier_data['Local News'].values[0]

        # Return all data as a dictionary (JSON format)
        return {
            "supplier_name": supplier_name,
            "distance": f"{distance} km",
            "cost": f"${cost}",
            "weather_report": weather_report,
            "local_news": local_news
        }
    else:
        st.error("The column 'Supplier Name' does not exist in the dataset.")
        return None

# Function to generate a summary using Gemini Pro 1.5 with retry logic
def generate_summary(data):
    prompt = (
        f"Create a summary based on the following information:\n\n"
        f"Supplier Name: {data['supplier_name']}\n"
        f"Distance: {data['distance']}\n"
        f"Cost: {data['cost']}\n"
        f"Weather Report: {data['weather_report']}\n"
        f"Local News: {data['local_news']}\n"
    )

    max_retries = 3
    for attempt in range(max_retries):
        try:
            chat_session = model.start_chat(
                history=[
                    {
                        "role": "user",
                        "parts": [prompt]
                    }
                ]
            )
            response = chat_session.send_message(prompt)
            return response.text
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(5)  # Wait before retrying
                continue
            else:
                st.error(f"An error occurred while generating the summary: {e}")
                return None

# Function to find the best supplier based on cost and distance
def find_best_supplier(data):
    # Remove any leading/trailing spaces from the column names
    data.columns = data.columns.str.strip()

    # Ensure the column names are correct
    if all(col in data.columns for col in ['Supplier Name', 'Distance (km)', 'Cost ($)', 'Company Name']):
        # Convert distance and cost to numeric
        data['Distance (km)'] = pd.to_numeric(data['Distance (km)'], errors='coerce')
        data['Cost ($)'] = pd.to_numeric(data['Cost ($)'], errors='coerce')

        # Drop rows with NaN values in distance or cost
        data = data.dropna(subset=['Distance (km)', 'Cost ($)'])

        # Find the supplier with the minimum cost and distance
        best_supplier = data.loc[data[['Cost ($)', 'Distance (km)']].sum(axis=1).idxmin()]

        # Format the result
        return f"The best supplier based on lowest cost and distance is {best_supplier['Supplier Name']} from {best_supplier['Company Name']}."
    else:
        st.error("Required columns are missing in the dataset.")
        return None

# Streamlit UI
def main():
    st.title("Supplier Information Fetcher")

    # Use local file path
    file_path = 'C:/Users/mpudi/Downloads/weather_report_sample_data.pdf'

    # Extract data from PDF
    data = extract_data_from_pdf(file_path)

    if not data.empty:
        st.write("Data extracted successfully!")
        st.write("Columns in the dataset:", data.columns.tolist())

        # Input field for supplier name
        supplier_name = st.text_input("Enter Supplier Name")

        if st.button("Get Information"):
            if supplier_name:
                # Fetch supplier information
                info = get_supplier_info(supplier_name, data)

                if info:
                    # Display fetched information in JSON format
                    st.json(info)

                    # Generate and display summary using Gemini Pro 1.5
                    summary = generate_summary(info)
                    st.write("Summary:")
                    st.write(summary)
                else:
                    st.error("Supplier not found or incorrect column name.")
            else:
                st.error("Please enter a supplier name.")

        # Button to get the best supplier based on cost and distance
        if st.button("Find Best Supplier"):
            best_supplier = find_best_supplier(data)
            if best_supplier:
                st.write(best_supplier)
    else:
        st.error("Failed to extract data from the PDF.")

if __name__ == "__main__":
    main()
