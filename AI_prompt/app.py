import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
import json
from datetime import datetime
import html
from groq import Groq

from assets import styles
from utils.constants import TASK_OPTIONS, TONE_OPTIONS, OUTPUT_FORMAT_OPTIONS, GROQ_MODEL_PRIORITY, GROQ_FALLBACK_MODELS
from utils.state import init_session_state, init_state
from core.prompt_builder import build_final_prompt
from core.groq_api import call_groq, fetch_groq_models
from components.sidebar import render_sidebar
from components.sidebar_components import components_data
from components.main_view import render_tabs



load_dotenv("GROQ_API_KEY.env")

# ============================================================================
# 페이지 설정
# ============================================================================

st.set_page_config(
    page_title="AI 프롬프트 생성기",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# 커스텀 CSS
# ============================================================================
init_session_state()

st.markdown(f"""{styles.apply_custom_css()}""", unsafe_allow_html=True)

# ============================================================================
# Session State 초기화
# ============================================================================

init_state()

# ============================================================================
# 사이드바 — 입력 영역
# ============================================================================

with st.sidebar:
    st.markdown("## ⚡AI 프롬프트 생성기")
    st.markdown("<p style='color:#adc6ff;font-size:13px;margin-top:-8px'>Powered by Groq API</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # API 및 모델 설정 (상단 배치) 
    sidebar_mode = st.radio(
        "메뉴 선택",
        options=["🔑 API Configuration", "🧠 AI Models"], # 이모지가 아이콘 역할을 합니다
        index=1, # API Configuration 탭을 기본으로 켬
        label_visibility="collapsed"
    )
    
    
    # ── 핵심 2: 텍스트 입력창은 세션에 저장된 값을 띄워줌 ──
    if sidebar_mode == "🔑 API Configuration":
        new_key, deploy_btn = render_sidebar(sidebar_mode)
        
        st.session_state.saved_api_key = new_key 

    elif sidebar_mode == "🧠 AI Models":
        current_key, new_model = render_sidebar(sidebar_mode)

        st.session_state.saved_model = new_model


    # ── 👇 투명한 여백을 추가 👇 ──
    st.markdown('<hr style="border:none;border-top:1px solid #c4c6cf;margin:0 0 16px 0;"/>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    st.markdown("#### 💡AI 프롬프트 입력항목")

    # 폼 영역 (내부적으로 expander를 포함하도록 수정됨)
    role_input, expertise_input, task_choice, task_detail_input, target_input, constraints_input, reference_input, format_choice, tone_choice, language_choice, examples_data = components_data()

    st.markdown("<br>", unsafe_allow_html=True)
    
    # 액션 버튼
    generate_btn = st.button("✨ 프롬프트 생성", use_container_width=True, type="secondary")
    run_groq_btn = st.button("⚡ Groq으로 바로 실행", use_container_width=True, type="primary")


# ============================================================================
# 메인 영역 — 출력
# ============================================================================

st.markdown("""
    <div class="main-title-container">
        <div class="main-title"><span>⚡</span> AI 프롬프트 생성기</div>
        <p class="main-subtitle">사이드바에서 조건을 입력하면 AI에 바로 사용할 수 있는 최적화 프롬프트가 생성됩니다</p>
    </div>
""", unsafe_allow_html=True)

# 버튼 로직
if generate_btn or run_groq_btn:
    if not role_input.strip():
        st.warning("⚠️ 역할(Role)을 입력해주세요.")
        st.stop()

    # 프롬프트 즉시 생성 (규칙 기반, API 호출 없음)
    prompt = build_final_prompt(
        role=role_input,
        expertise=expertise_input,
        task=task_choice,
        task_detail=task_detail_input,
        target=target_input,
        constraints=constraints_input,
        reference=reference_input,
        output_format=format_choice,
        tone=tone_choice,
        examples=examples_data,
        language=language_choice,
    )
    st.session_state.generated_prompt = prompt

    # Groq 실행
    if run_groq_btn:
        # api_key_input -> st.session_state.saved_api_key 로 변경
        if not st.session_state.saved_api_key.strip():
            st.error("❌ Groq API 키를 입력해주세요.")
            st.stop()
            
        with st.spinner("⚡ Groq API가 응답 중입니다..."):
            # model_choice -> st.session_state.saved_model 로 변경
            st.session_state.groq_response = call_groq(
                prompt, 
                st.session_state.saved_model, 
                st.session_state.saved_api_key.strip()
            )

    # 히스토리 저장
    st.session_state.history.append({
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "role": role_input,
        "task": task_choice.split("(")[0].strip(),      
        "model": st.session_state.saved_model,        
        "prompt": st.session_state.generated_prompt,
        "response": st.session_state.groq_response,
    })

# ── 탭 구성 ───────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📝 생성된 프롬프트", "⚡ Groq AI 응답", "📜 히스토리"])

render_tabs(tab1, tab2, tab3, role_input, task_choice, format_choice, tone_choice, examples_data)