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

load_dotenv("GPT_API_KEY.env")
init_session_state()

@st.cache_data(show_spinner=False)
def get_recommendation(api_key, model, prompt):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "당신은 Tableau 대시보드 전문 BI 컨설턴트이자 및 UI/UX 디자이너입니다. 항상 유효한 JSON만 출력합니다."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=3000,
        # max_completion_tokens=2500,
        top_p=0.9
    )
    return response.choices[0].message.content

import requests

@st.cache_data(show_spinner=False)
def get_img_recommendation(api_key, prompt):
    client = OpenAI(api_key=api_key)
    response = client.images.generate(
        model="gpt-image-1.5",
        prompt=prompt,
        size="1536x1024",
        quality="high",
        n=1
    )
    
    data = response.data[0]
    if getattr(data, "url", None):
        image_bytes = requests.get(data.url).content
    elif getattr(data, "b64_json", None):
        image_bytes = base64.b64decode(data.b64_json)
    else:
        raise ValueError("이미지 데이터를 반환받지 못했습니다.")
        
    img = Image.open(BytesIO(image_bytes))
    
    target_height = 900  # 원하는 높이(px)
    img_w, img_h = img.size
    ratio = target_height / img_h
    new_w = int(img_w * ratio)
    img = img.resize((new_w, target_height), Image.LANCZOS)
        
    return img