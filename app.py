
# ============== STEP 1: LOAD MODULES ==============

import requests
from urllib.parse import quote
import streamlit as st
import requests
from urllib.parse import quote
from tavily import TavilyClient
from langchain_google_genai import ChatGoogleGenerativeAI


# ============== STEP 2: API KEYS ==============

st.set_page_config(page_title="PPT Maker", page_icon="📊", layout="wide")

st.title("AI Presentation and News Generator")
st.write("Generate images, search for news and create presentations.")

st.sidebar.title("Give API Keys")

GOOGLE_API_KEY = st.sidebar.text_input("GOOGLE_API_KEY", type="password")

TAVILY_API_KEY = st.sidebar.text_input("TAVILY_API_KEY", type="password")

if not GOOGLE_API_KEY:
  st.sidebar.info("Enter your Google API key to generate presentations.")

if not TAVILY_API_KEY:
  st.sidebar.info("Enter your Tavily API key to search for news.")


# ============== STEP 3: BACKEND FUNCTIONS ==============

def generate_image(prompt):
  """Generate an image from the user's prompt."""
  
  if not prompt.strip():
    raise ValueError("Please enter an image description.")
    
    url = "https://image.pollinations.ai/prompt/" + quote(prompt, safe="")

    response = requests.get(url, timeout=120)
    response.raise_for_status()

    if not response.headers.get("Content-Type", "").startswith("image/"):
      raise ValueError("The image service did not return an image.")
      
      
      return response.content


def search_latest_info(query):
  """Search for recent news using Tavily."""
  
  
  if not TAVILY_API_KEY:
    raise ValueError("Please enter your Tavily API key.")

  if not query.strip():
    raise ValueError("Please enter a topic to search.")
    
    client = TavilyClient(api_key=TAVILY_API_KEY)
    
    
    return client.search(query=query,topic="news",max_results=5)

def generate_ppt(prompt):
  """Generate an HTML presentation using Gemini."""
  
  
  if not GOOGLE_API_KEY:
    raise ValueError("Please enter your Google API key.")

  if not prompt.strip():
    raise ValueError("Please enter a presentation topic.")

    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash",google_api_key=GOOGLE_API_KEY)
    
    
    
    instructions = """
    Create a complete HTML presentation based on the user's topic.

    Include:
    - A professional design with a consistent colour theme.
    - Clear headings and short bullet points.
    - Well-organised slides with useful information.
    - Previous and next buttons to move between slides.
    - Slide numbers and keyboard navigation.
    - Sources for factual claims when available.

    Return the complete HTML document only.
    Do not use Markdown code fences.
    Do not invent statistics or sources.
    """

    response = model.invoke(instructions + "\n\nPresentation topic:\n" + prompt)
    
    
    
    code = response.content

    if isinstance(code, list):
      code = "\n".join(
        item.get("text", "")
        for item in code
        if isinstance(item, dict) and item.get("type") == "text")
      
      
      if not isinstance(code, str) or "<html" not in code.lower():
        raise ValueError("Could not generate a complete HTML presentation.")
        
        
      return code


# ============== STEP 4: APPLICATION TABS ==============

tab1, tab2, tab3 = st.tabs([
    "Generate Image",
    "Fetch News",
    "Generate PPT"])


# ============== TAB 1: GENERATE IMAGE ==============


def generate_image(prompt):
    """Generate an image from the user's prompt."""

    if not prompt.strip():
        raise ValueError("Please enter an image description.")

    url = "https://image.pollinations.ai/prompt/" + quote(prompt, safe="")

    response = requests.get(url, timeout=120)
    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "")

    if not content_type.startswith("image/"):
        raise ValueError(
            "The image service did not return an image. "
            "Please try again later.")

    return response.content



# ============== TAB 2: FETCH NEWS ==============

with tab2:
  st.subheader("Latest News")
  
  
  news_query = st.text_input("Enter a topic",
                             value="Latest AWS, Microsoft Azure and Google Cloud news")
  
  if st.button("Fetch Latest News", key="news_button"):
    try:
      with st.spinner("Searching for news..."):
        response = search_latest_info(news_query)
        articles = response.get("results", [])
        
        
        
        if not articles:
          st.info("No articles found. Try another topic.")
          
          for article in articles:
            title = article.get("title", "Untitled article")
            summary = article.get("content", "No summary available.")
            link = article.get("url", "")
            date = article.get("published_date") or "Date unavailable"
            
            
            with st.container(border=True):
              st.subheader(title)
              st.caption(f"Published: {date}")
              st.write(summary)
              
              
              if link.startswith(("https://", "http://")):
                st.link_button("Read Article", link)
    
    except Exception as err:
      st.error(f"Could not fetch news: {err}")


# ============== TAB 3: GENERATE PPT ==============

with tab3:
  st.subheader("Generate Presentation")
  
  user_input = st.text_area(
    "Write your presentation topic and requirements",
    key="ppt_prompt")
  
  
  if st.button("Generate PPT", key="ppt_button"):
    try:
      with st.spinner("Creating your presentation..."):
        code = generate_ppt(user_input)
        
        
        st.session_state["ppt_code"] = code
    
    except Exception as err:
      st.error(f"Could not generate presentation: {err}")

    if st.session_state.get("ppt_code"):
      code = st.session_state["ppt_code"]
      
      
      st.success("Presentation generated successfully.")
      
      
      st.download_button(
        "Download Presentation",
        data=code,
        file_name="presentation.html",
        mime="text/html")
      
      
      st.components.v1.html(
        code,
        height=700,
        scrolling=True)

  
























