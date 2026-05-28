import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
import json
from datetime import datetime
import html
from groq import Groq


from utils.constants import GROQ_MODEL_PRIORITY, GROQ_FALLBACK_MODELS

load_dotenv("GROQ_API_KEY.env")

# ============================================================================
# Groq API 호출 (선택적 실행)
# ============================================================================

def call_groq(prompt: str, model: str, api_key: str) -> str:
    """생성된 프롬프트를 Groq API로 실행"""
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2048,
        )
        return response.choices[0].message.content
    
    except Exception as e:
        return f"❌ API 오류: {str(e)}"


# ============================================================================
# groq API 호출 - 모델 자동 업데이트
# ============================================================================

@st.cache_data(ttl=180, show_spinner=False)
def fetch_groq_models(key: str):
    """
    Groq /models 엔드포인트에서 사용 가능한 모델 목록을 가져옵니다.
    """
    try:
        client = Groq(api_key=key)
        all_models = client.models.list()   # ← OpenAI와 동일한 방식

        model_ids = [m.id for m in all_models.data]

        if not model_ids:
            return GROQ_FALLBACK_MODELS, "fallback"

        # 우선순위 기준 정렬
        def sort_key(mid):
            if mid in GROQ_MODEL_PRIORITY:
                return (0, GROQ_MODEL_PRIORITY.index(mid))
            return (1, mid)  # 우선순위 외 모델은 알파벳 순

        model_ids.sort(key=sort_key)
        return model_ids, "live"

    except Exception as e:
        return GROQ_FALLBACK_MODELS, f"error:{e}"
