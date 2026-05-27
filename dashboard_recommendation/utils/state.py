import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

def init_session_state():
    """
    Streamlit 앱 전체에서 사용되는 전역 상태(session_state)를 초기화합니다.
    앱이 처음 로드될 때 한 번만 세팅됩니다.
    """
    load_dotenv("GPT_API_KEY.env")
    
    # 1. 결과 및 UI 렌더링 관련 상태
    if "result" not in st.session_state:
        st.session_state.result = None
    if "dashboard_img" not in st.session_state:
        st.session_state.dashboard_img = None
    if "dashboard_topic_saved" not in st.session_state:
        st.session_state.dashboard_topic_saved = None
    
    # 2. 사용자 입력 폼 기본값 상태
    if "goal_tags" not in st.session_state:
        st.session_state.goal_tags = ["Monitoring", "Trend Analysis"]
    if "complexity" not in st.session_state:
        st.session_state.complexity = 3

    # 3. 데이터프레임 에디터 초기 데이터 (선택 컬럼 포함)
    if "fields_df" not in st.session_state:
        default_df = pd.DataFrame([
                    {"선택": False, "Field Name": "Order_Date",      "Type": "Date",     "Usage / Description": "주문이 발생한 날짜 (시계열 분석용)"},
                    {"선택": False, "Field Name": "Sales_Amount",    "Type": "Number",   "Usage / Description": "통화 단위의 총 매출액 합계"},
                    {"선택": False, "Field Name": "Region",          "Type": "String",   "Usage / Description": "판매 지역 구분 (APAC, EMEA 등)"},
                    {"선택": False, "Field Name": "Category",        "Type": "String",   "Usage / Description": "제품군 대분류"},
                    {"선택": False, "Field Name": "Customer_ID",     "Type": "String",   "Usage / Description": "고객 고유 식별자"},
                    {"선택": False, "Field Name": "Sales_Amount",    "Type": "Number",   "Usage / Description": "총 매출액"},
                    {"선택": True,  "Field Name": "Profit_Margin",   "Type": "Number",   "Usage / Description": "이익률 (%)"},
                    {"선택": True,  "Field Name": "Ticket_Status",   "Type": "String",   "Usage / Description": "CS 문의 처리 상태 (Open, Resolved 등)"},
                    {"선택": False, "Field Name": "Issue_Type",      "Type": "String",   "Usage / Description": "CS 문의 유형 (배송 지연, 환불, 결함 등)"},
                    {"선택": True,  "Field Name": "Resolution_Days", "Type": "Number",   "Usage / Description": "CS 티켓 해결까지 걸린 소요 일수"},
                    {"선택": False, "Field Name": "Resolution_Days", "Type": "Number",   "Usage / Description": "고객 만족도 점수 (1~5점 척도)"},
                ])
        st.session_state.fields_df = default_df

    # 4. API 및 모델 설정 상태
    if "saved_api_key" not in st.session_state:
        st.session_state.saved_api_key = os.getenv("OPENAI_API_KEY", "")
    if "saved_model" not in st.session_state:
        st.session_state.saved_model = "gpt-4o"