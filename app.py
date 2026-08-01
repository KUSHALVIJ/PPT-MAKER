# ============== STEP 1 LOAD MODULES=========
import os
import time
import langchain
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
import pytesseract as pyt
from tavily import TavilyClient
import numpy as np
import streamlit as st

# ============== STEP 2 LOAD ENV and API KEYS=========

st.title("Agentic PPT Generator")
st.header("""User can generate, PPT,Images, and fetch latest news""")

st.sidebar.title("Give API Keys")

GOOGLE_API_KEY = st.sidebar.text_input("GOOGLE_API_KEY",type="password")
TAVILY_API_KEY = st.sidebar.text_input("TAVILY_API_KEY",type="password")

ALL_API























