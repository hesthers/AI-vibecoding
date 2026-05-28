import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
import json
from datetime import datetime
import html
from groq import Groq

from utils.constants import TASK_OPTIONS, TONE_OPTIONS, OUTPUT_FORMAT_OPTIONS

def components_data():
    # ── 1. 역할 정의 ──────────────────────────────────────────────────────────
    with st.expander("👤 1. 역할 및 성격", expanded=False):
        role_input = st.text_input("역할 (Role)", placeholder="예: 시니어 백엔드 개발자")
        expertise_input = st.text_input("전문성 및 성격 (Persona)", placeholder="예: 10년 경력, 냉철하고 논리적")

    # ── 2. 작업 지시 & 맥락 ───────────────────────────────────────────────────
    with st.expander("📋 2. 작업 및 배경", expanded=False):
        task_choice = st.selectbox("작업 유형 (Task)", options=list(TASK_OPTIONS.keys()))
        task_detail_input = st.text_area("상세 지시사항", placeholder="예:\n- 서론/본론/결론 구조로 나누어 작성할 것\n- 반드시 3가지 이상의 대안을 제시할 것\n- 전문 용어는 초보자도 이해하기 쉽게 풀어서 설명할 것", height=80)
        target_input = st.text_input("대상 (Target)", placeholder="예: 초등학생, 시니어 개발자")
        constraints_input = st.text_input("제약 사항 (Constraints)", placeholder="예: 500자 이내로 답변 작성")
        reference_input = st.text_area("참조 데이터 (Reference)", placeholder="데이터에 대한 설명 입력 (데이터 구조, 컬럼명 등)", height=80)

    # ── 3. 출력 형식 & 톤 ────────────────────────────────────────────────────
    with st.expander("🎨 3. 출력 형식 & 톤", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            format_choice = st.selectbox("출력 형식", list(OUTPUT_FORMAT_OPTIONS.keys()))
        with c2:
            tone_choice = st.selectbox("톤 (Tone)", list(TONE_OPTIONS.keys()))
        language_choice = st.selectbox("응답 언어", ["한국어", "영어 (English)", "한국어 + 영어"])

    # ── 4. Few-Shot 예시 ───────────────────────────────────────────────────────
    with st.expander("🎯 4. Zero/Few-Shot 예시", expanded=False):
        example_count = st.radio("예시 개수", [0, 1, 2], horizontal=True)
        examples_data = []
        for i in range(example_count):
            ei = st.text_input(f"요청 예시 (Request) {i+1}", key=f"ex_in_{i}", placeholder="주제, 요청사항 (예: 신제품 출시 홍보 이메일 초안 작성해 줘)")
            eo = st.text_area(f"원하는 출력 형태 (Desired Format) {i+1}", key=f"ex_out_{i}", placeholder="사용자가 원하는 형식 출력 (예:\n 1. 총 매출: OOO원\n2. 전년 대비 증감률: OO%\n(반드시 글머리 기호 사용))", height=60)
            examples_data.append({"input": ei, "output": eo})

    return role_input, expertise_input, task_choice, task_detail_input, target_input, constraints_input, reference_input, format_choice, tone_choice, language_choice, examples_data