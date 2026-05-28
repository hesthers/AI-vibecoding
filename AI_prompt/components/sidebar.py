
import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
import json
from datetime import datetime
import html
from groq import Groq


from utils.constants import TASK_OPTIONS, TONE_OPTIONS, OUTPUT_FORMAT_OPTIONS, GROQ_MODEL_PRIORITY, GROQ_FALLBACK_MODELS
from core.groq_api import fetch_groq_models


def render_sidebar(sidebar_mode):
    
    deploy_btn = False
      
    # ── 핵심 2: 텍스트 입력창은 세션에 저장된 값을 띄워줌 ──
    if sidebar_mode == "🔑 API Configuration":
        st.markdown('<p style="font-size:11px;font-weight:600;color:#74777f;text-transform:uppercase;margin-bottom:6px;">GROQ API KEY</p>', unsafe_allow_html=True)
 
        new_key = st.text_input(
            "api_key_label",
            label_visibility="collapsed",
            value=st.session_state.saved_api_key, # <--- 여기가 포인트!
            type="password",
            placeholder="gsk_..."
        )
              
        deploy_btn = st.button("Deploy Model", use_container_width=True)

        return new_key, deploy_btn

    else:
        current_key = st.session_state.saved_api_key

        if current_key and current_key.startswith("gsk_"):   # ← Groq 키 검증
            model_list, fetch_status = fetch_groq_models(current_key)

            # 상태 표시
            status_map = {
                "live":     "🟢 실시간 모델 목록 (Groq API 조회)",
                "fallback": "🟡 기본 모델 목록 (조회 결과 없음)",
            }
            label = status_map.get(fetch_status, "🔴 기본 모델 목록 (API 오류 — 키 확인 필요)")

        else:
            model_list = GROQ_FALLBACK_MODELS
            label = "⚪ 기본 모델 목록 (API 키 입력 후 자동 갱신)"

        st.markdown(
            f'<p style="font-size:11px;color:#74777f;margin-bottom:6px;">{label}</p>',
            unsafe_allow_html=True
        )
        st.markdown('<p style="...">MODEL SELECT</p>', unsafe_allow_html=True)

        default_idx = (
            model_list.index(st.session_state.saved_model)
            if st.session_state.saved_model in model_list else 0
        )
        new_model = st.selectbox(
            "model_label",
            label_visibility="collapsed",
            options=model_list,
            index=default_idx
        )

        if current_key and current_key.startswith("gsk_"):
            if st.button("🔄 모델 새로고침", use_container_width=True):
                st.cache_data.clear()
                st.rerun()
 
    return current_key, new_model