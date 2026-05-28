import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
import json
from datetime import datetime
import html
from groq import Groq

load_dotenv("GROQ_API_KEY.env")

def init_session_state():
    # ── 핵심 1: 앱이 처음 실행될 때 .env에서 키를 가져와 세션에 저장 ──
    if "saved_api_key" not in st.session_state:
        # .env 파일에 GROQ_API_KEY가 있으면 그 값을, 없으면 빈 칸("")을 기본값으로 저장
        st.session_state.saved_api_key = os.getenv("GROQ_API_KEY", "") 

    if "saved_model" not in st.session_state:
        st.session_state.saved_model = "llama-3.3-70b-versatile"




def init_state():
    defaults = {
        "generated_prompt": "",
        "groq_response": "",
        "example_count": 1,
        "examples": [{"input": "", "output": ""}, {"input": "", "output": ""}],
        "history": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v