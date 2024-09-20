# from fastapi import FastAPI, HTTPException, Query
# from typing import List, Dict
# import requests
# import uvicorn

# app = FastAPI()

# API_URL = "https://api.goperigon.com/v1/all"
# API_KEY = "f8328a49-93b2-4fa4-886d-6147812f904c"

# HEADERS = {
#     'x-rapidapi-host': 'weather-by-api-ninjas.p.rapidapi.com',
#     'x-rapidapi-key': '742999ab9fmshfb9b47c8eab2089p13bd91jsnafea1a017942'
# }

# def summarize_text(text: str, keywords: List[str]):
#     # Split the text into sentences
#     sentences = text.split(". ")
#     # Filter sentences that contain any of the specified keywords
#     relevant_sentences = [sentence for sentence in sentences if any(keyword in sentence.lower() for keyword in keywords)]
    
#     # If no relevant sentences are found, use the first 2-3 sentences as fallback
#     if not relevant_sentences:
#         relevant_sentences = sentences[:3]
    
#     # Return the summarized text by joining the relevant sentences
#     return ". ".join(relevant_sentences[:3])  # Limit to the first 3 relevant sentences

# def deduplicate_summaries(news_list: List[Dict]) -> List[Dict]:
#     """
#     Removes duplicate news entries based on their summaries.
#     """
#     seen_summaries = set()
#     unique_news = []
#     for news in news_list:
#         # Consider summaries with significant text length only
#         summary = news["summary"].strip()
#         if summary and summary not in seen_summaries:
#             seen_summaries.add(summary)
#             unique_news.append(news)
#     return unique_news

# @app.get("/local-news/")
# async def get_local_news(
#     location: str = Query(..., description="Location for news (e.g., 'Dallas, Texas, USA')"),
#     topics: List[str] = Query(
#         default=["flood", "rain", "roadblock", "tsunami"],
#         description="List of topics to filter the news, e.g., ['flood', 'rain', 'roadblock']"
#     )
# ):
#     try:
#         # Join topics into a single string separated by commas for the query parameter
#         topics_query = ",".join(topics)
        
#         # Construct the URL with query parameters for location and topics
#         url = f"{API_URL}?apiKey={API_KEY}&title={location}&q={topics_query}"
        
#         # Send the GET request
#         response = requests.get(url, headers=HEADERS)

#         # Raise an HTTPException for non-200 responses
#         response.raise_for_status()

#         # Extract relevant data
#         news_data = response.json().get("articles", [])
#         filtered_news = []

#         # Filter news by specific keywords in the title or summary
#         for article in news_data:
#             title = article.get("title", "").lower()
#             summary = article.get("summary", "").lower()

#             # Check if any of the keywords appear in the title or summary
#             if any(keyword.lower() in title or keyword.lower() in summary for keyword in topics):
#                 # Use the 'summary' field or fallback to 'content' if available
#                 summary_text = article.get("summary", "") or article.get("content", "")
                
#                 # Ensure the text to be summarized is not empty
#                 if summary_text:
#                     # Summarize the article summary to focus on relevant sentences
#                     summarized_text = summarize_text(summary_text, topics)
#                 else:
#                     summarized_text = "No summary available."

#                 filtered_news.append({
#                     "url": article.get("url"),
#                     "summary": summarized_text
#                 })

#         # Deduplicate the news list to remove repetitive summaries
#         unique_filtered_news = deduplicate_summaries(filtered_news)

#         # Return the filtered news list
#         return {"filtered_news": unique_filtered_news}

#     except requests.exceptions.HTTPError as http_err:
#         raise HTTPException(status_code=response.status_code, detail=f"HTTP error: {str(http_err)}")
#     except Exception as err:
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(err)}")

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)







import streamlit as st
import requests
from typing import List, Dict

API_URL = "https://api.goperigon.com/v1/all"
API_KEY = "f8328a49-93b2-4fa4-886d-6147812f904c"

HEADERS = {
    'x-rapidapi-host': 'weather-by-api-ninjas.p.rapidapi.com',
    'x-rapidapi-key': '742999ab9fmshfb9b47c8eab2089p13bd91jsnafea1a017942'
}

def summarize_text(text: str, keywords: List[str]):
    # Split the text into sentences
    sentences = text.split(". ")
    # Filter sentences that contain any of the specified keywords
    relevant_sentences = [sentence for sentence in sentences if any(keyword in sentence.lower() for keyword in keywords)]
    
    # If no relevant sentences are found, use the first 2-3 sentences as fallback
    if not relevant_sentences:
        relevant_sentences = sentences[:3]
    
    # Return the summarized text by joining the relevant sentences
    return ". ".join(relevant_sentences[:3])  # Limit to the first 3 relevant sentences

def deduplicate_summaries(news_list: List[Dict]) -> List[Dict]:
    """
    Removes duplicate news entries based on their summaries.
    """
    seen_summaries = set()
    unique_news = []
    for news in news_list:
        # Consider summaries with significant text length only
        summary = news["summary"].strip()
        if summary and summary not in seen_summaries:
            seen_summaries.add(summary)
            unique_news.append(news)
    return unique_news

def fetch_local_news(location: str, topics: List[str]):
    try:
        # Join topics into a single string separated by commas for the query parameter
        topics_query = ",".join(topics)
        
        # Construct the URL with query parameters for location and topics
        url = f"{API_URL}?apiKey={API_KEY}&title={location}&q={topics_query}"
        
        # Send the GET request
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()

        # Extract relevant data
        news_data = response.json().get("articles", [])
        filtered_news = []

        # Filter news by specific keywords in the title or summary
        for article in news_data:
            title = article.get("title", "").lower()
            summary = article.get("summary", "").lower()

            # Check if any of the keywords appear in the title or summary
            if any(keyword.lower() in title or keyword.lower() in summary for keyword in topics):
                # Use the 'summary' field or fallback to 'content' if available
                summary_text = article.get("summary", "") or article.get("content", "")
                
                if summary_text:
                    # Summarize the article summary to focus on relevant sentences
                    summarized_text = summarize_text(summary_text, topics)
                else:
                    summarized_text = "No summary available."

                filtered_news.append({
                    "url": article.get("url"),
                    "summary": summarized_text
                })

        # Deduplicate the news list to remove repetitive summaries
        return deduplicate_summaries(filtered_news)

    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error: {str(http_err)}")
    except Exception as err:
        st.error(f"An error occurred: {str(err)}")
    return []

# Streamlit app
st.title("Local News Fetcher")

# Input for location
location = st.text_input("Enter Location (e.g., 'Dallas, Texas, USA')", "")

# Input for topics
topics = st.multiselect(
    "Select Topics",
    ["flood", "rain", "roadblock", "tsunami", "earthquake", "storm"],
    default=["flood", "rain", "roadblock"]
)

# Fetch and display news when the button is clicked
if st.button("Fetch News"):
    if location and topics:
        news = fetch_local_news(location, topics)
        if news:
            for article in news:
                st.write(f"**URL**: {article['url']}")
                st.write(f"**Summary**: {article['summary']}")
                st.write("---")
        else:
            st.write("No relevant news found.")
    else:
        st.error("Please provide both a location and topics.")
