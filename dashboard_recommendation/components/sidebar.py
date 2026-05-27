import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI
from PIL import Image
import base64
from io import BytesIO
import json
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime

from utils.state import init_session_state

def render_sidebar(sidebar_mode):

    init_session_state()

    generate_btn = False

    # ── 탭 분기 시작 ──
    if sidebar_mode == "🔑 API Configuration":
        # 키 입력
        # ... (이하 API Configuration 화면 표시 코드 동일) ...
        st.markdown('<p style="font-size:11px;font-weight:600;color:#74777f;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;">API KEY</p>', unsafe_allow_html=True)
        # 키 입력 후 즉시 저장
        new_key = st.text_input(
            "api_key_label", 
            label_visibility="collapsed",
            value=st.session_state.saved_api_key,
            type="password",
            placeholder="sk-..."
        )
        
        generate_btn = st.button("Deploy Model", use_container_width=True)

        return new_key, generate_btn

    # [탭 B] AI 모델 선택 화면
    elif sidebar_mode == "🧠 AI Models":
        # (기존 모델 가져오기 로직 유지)
        CHAT_MODEL_PREFIXES = ("gpt-4", "gpt-3.5", "o1", "o3", "o4")
        MODEL_PRIORITY = ["gpt-4o", "gpt-4o-mini", "o4-mini", "o3", "o1", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"]
        FALLBACK_MODELS = ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"]

        @st.cache_data(ttl=180, show_spinner=False)
        def fetch_gpt_models(key: str):
            try:
                client = OpenAI(api_key=key)
                all_models = client.models.list()
                chat_models = [m.id for m in all_models.data if m.id.startswith(CHAT_MODEL_PREFIXES) and "instruct" not in m.id and "vision" not in m.id]
                if not chat_models: return FALLBACK_MODELS, "fallback"
                chat_models.sort(key=lambda mid: (0, MODEL_PRIORITY.index(mid)) if mid in MODEL_PRIORITY else (1, mid))
                return chat_models, "live"
            except Exception as e:
                return FALLBACK_MODELS, f"error:{e}"

        current_key = st.session_state.saved_api_key
        if current_key and current_key.startswith("sk-"):
            model_list, _ = fetch_gpt_models(current_key)
        else:
            model_list = FALLBACK_MODELS

        st.markdown('<p style="font-size:11px;font-weight:600;color:#74777f;text-transform:uppercase;letter-spacing:0.5px;margin:0 0 6px 0;">MODEL SELECT</p>', unsafe_allow_html=True)
        default_idx = model_list.index(st.session_state.saved_model) if st.session_state.saved_model in model_list else 0
        
        new_model = st.selectbox(
            "model_label", 
            label_visibility="collapsed",
            options=model_list, 
            index=default_idx
        )

    
        if current_key and current_key.startswith("sk-"):
            if st.button("🔄 모델 새로고침", use_container_width=True):
                st.cache_data.clear()
                st.rerun()
       

    return  current_key, new_model