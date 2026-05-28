
import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
import json
from datetime import datetime
import html
from groq import Groq


def apply_custom_css():
    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');

        /* 전체 배경 & 스크롤바 */
        .stApp {{
            background: #131C2E; /* bg-background */
            color: #adc6ff;
            font-family: 'Noto Sans KR', sans-serif;
        }}
        ::-webkit-scrollbar {{ width: 6px; }}
        ::-webkit-scrollbar-track {{ background: #191b23; }}
        ::-webkit-scrollbar-thumb {{ background: #424754; border-radius: 10px; }}

        /* 사이드바 */
        [data-testid="stSidebar"] {{
            background: #131C2E; /* surface-container-low */
            border-right: 1px solid #424754;
        }}
        [data-testid="stSidebar"] * {{
            color: #e1e2ec !important;
        }}
        
        /* 사이드바 헤더 및 제목 강제 스타일 제거 대비 */
        .sidebar-header {{
            padding-bottom: 16px;
            border-bottom: 1px solid #424754;
            margin-bottom: 16px;
        }}
        .sidebar-title {{
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #adc6ff !important;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .sidebar-title span {{ color: #4edea3 !important; font-size: 18px; }}

        /* 입력 폼 라벨 (HTML의 section-header 및 label 스타일) */
        .stTextInput label p, .stTextArea label p, .stSelectbox label p {{
            color: #8c909f !important;
            font-size: 11px !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            margin-bottom: 4px;
        }}

        /* 입력 필드 */
        .stTextInput input, .stTextArea textarea, div[data-baseweb="select"] > div {{
            background: #414552 !important; /* surface-container-highest */
            border: 1px solid #8c909f !important; /* outline-variant */
            border-radius: 6px !important;
            /*color: #e1e2ec !important;
            font-size: 14px !important;
        }}
        .stTextInput input:focus, .stTextArea textarea:focus, div[data-baseweb="select"] > div:focus-within {{
            border-color: #adc6ff !important; /* primary */
            box-shadow: 0 0 0 1px #adc6ff !important;
        }}
        .stTextInput input::placeholder, .stTextArea textarea::placeholder {{
            color: #8c909f !important; /* outline */
        }}

        /* 사이드바 Accordion(Expander) 스타일링 */
        [data-testid="stSidebar"] [data-testid="stExpander"] {{
            background: #414552 !important; /* surface-container */
            border: 1px solid #424754 !important;
            border-radius: 8px !important;
            margin-bottom: 12px;
        }}
        [data-testid="stSidebar"] [data-testid="stExpander"] summary {{
            padding: 16px !important;
            background: transparent !important;
        }}
        [data-testid="stSidebar"] [data-testid="stExpander"] summary:hover {{
            background: #272a31 !important; /* surface-container-high */
        }}
        [data-testid="stSidebar"] [data-testid="stExpander"] summary p {{
            font-size: 14px !important;
            font-weight: 700 !important;
            color: #e1e2ec !important;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        [data-testid="stSidebar"] .streamlit-expanderContent {{
            padding: 16px !important;
            border-top: 1px solid rgba(66, 71, 84, 0.3) !important;
        }}

        /* ── 버튼 커스텀 ── */

        /* 1. 사이드바 - ✨ 프롬프트 생성 (Secondary 타입 활용) */
        [data-testid="stSidebar"] button[kind="secondary"] {{
            background: #4d8eff !important; /* 배경색: 기존 테마의 파란색 */
            border: 1px solid #4d8eff !important;
            padding: 14px !important;
            border-radius: 8px !important;
            box-shadow: 0 10px 15px -3px rgba(77, 142, 255, 0.1) !important;
            transition: all 0.2s;
        }}

        /* 버튼 내부의 텍스트 영역까지 확실하게 색상 고정 */
        [data-testid="stSidebar"] button[kind="secondary"] div,
        [data-testid="stSidebar"] button[kind="secondary"] p {{
            color: #00285d !important; /* 글씨색: 진한 남색 (배경색과 대비되도록) */
            font-weight: 700 !important;
            font-size: 14px !important;
        }}

        [data-testid="stSidebar"] button[kind="secondary"]:hover {{
            filter: brightness(1.1);
        }}

        /* 2. 사이드바 - ⚡ Groq으로 바로 실행 (Primary 타입 활용) */
        [data-testid="stSidebar"] button[kind="primary"] {{
            background: #00a572 !important; /* 배경색: 기존 테마의 초록색 */
            border: 1px solid #00a572 !important; /* 파란 버튼과 동일한 1px 테두리를 줘서 높이 완벽 일치 */
            padding: 14px !important;
            border-radius: 8px !important;
            box-shadow: 0 10px 15px -3px rgba(0, 165, 114, 0.1) !important;
            transition: all 0.2s;
        }}

        /* 버튼 내부의 텍스트 영역까지 확실하게 색상 고정 */
        [data-testid="stSidebar"] button[kind="primary"] div,
        [data-testid="stSidebar"] button[kind="primary"] p {{
            color: #00311f !important; /* 글씨색: 진한 초록색 (배경색과 대비되도록) */
            font-weight: 700 !important;
            font-size: 14px !important;
        }}

        [data-testid="stSidebar"] button[kind="primary"]:hover {{
            filter: brightness(1.1);
        }}

        /* 3. 메인 영역 - 다운로드 버튼 전용 스타일 (.txt / .json 저장 버튼) */
        [data-testid="stMain"] [data-testid="stDownloadButton"] button {{
            background: #9E9B9B !important; /* 작성해주신 회색 배경 */
            color: #e1e2ec !important; /* 밝은 글씨 */
            font-weight: 700 !important;
            font-size: 14px !important;
            border: 1px solid #424754 !important;
            padding: 12px 24px !important;
            border-radius: 9999px !important;
            transition: all 0.2s;
        }}
        [data-testid="stMain"] [data-testid="stDownloadButton"] button:hover {{
            background: rgba(158, 155, 155, 0.9) !important; /* 호버 시 약간 투명하게 */
        }}

        /* 메인 타이틀 영역 */
        .main-title-container {{
            padding-top: 1rem;
            padding-bottom: 1rem;
        }}
        .main-title {{
            font-size: 24px;
            font-weight: 700;
            color: #adc6ff;
            display: flex;
            align-items: center;
            gap: 12px;
            letter-spacing: -0.025em;
            margin-bottom: 8px;
        }}
        .main-title span {{ 
            color: #4edea3; 
        }}
        .main-subtitle {{
            color: #ffffff;
            font-size: 14px;
            line-height: 1.6;
        }}

        /* 탭 스타일링 */
        .stTabs [data-baseweb="tab-list"] {{
            background: transparent !important;
            border-bottom: 1px solid rgba(66, 71, 84, 0.5) !important;
            gap: 32px !important;
            padding: 0 !important;
        }}
        .stTabs [data-baseweb="tab"] {{
            color: #c2c6d6 !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            padding: 0 4px 16px 4px !important;
            border: none !important;
            background: transparent !important;
        }}
        .stTabs [aria-selected="true"] {{
            color: #adc6ff !important;
            font-weight: 700 !important;
            border-bottom: 2px solid #adc6ff !important;
        }}

        /* 메트릭 카드 */
        .metric-card {{
            background-color: #272a31; /* surface-container-high */
            border: 1px solid #424754; /* outline-variant */
            border-radius: 12px;
            padding: 24px;
            text-align: center;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        }}
        .metric-value {{
            font-size: 24px;
            font-weight: 700;
            color: #adc6ff; /* primary */
        }}
        .metric-label {{
            font-size: 14px;
            font-weight: 500;
            color: #c2c6d6; /* on-surface-variant */
            margin-top: 4px;
        }}

        /* 태그 배지 */
        .tag-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 16px;
            margin-bottom: 4px;    /* ← 24px → 4px */
        }}
        .tag-badge {{
            background: #32353c; /* surface-container-highest */
            border: 1px solid #424754; /* outline-variant */
            border-radius: 6px;
            padding: 4px 10px;
            font-size: 11px;
            font-weight: 500;
            color: #c2c6d6;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }}

        /* 프롬프트 출력 박스 */
        /* ── 프롬프트 출력창 내부 마크다운 디자인 (버그 해결 및 1번 이미지 스타일 적용) ── */
        
        /* 1. 박스 전체 디자인 (기존 .prompt-box 역할) */
        div[data-testid="stVerticalBlock"]:has(.prompt-box-marker) {{
            background: #1d2027 !important; 
            border: 1px solid rgba(66, 71, 84, 0.5) !important;
            border-radius: 12px !important;
            padding: 16px 32px 32px 32px !important;  /* ← top만 32→8로 줄임 */
            margin-bottom: 24px !important;
            min-height: 400px !important;
        }}

        /* 마커 div 자체 높이 제거 — 추가 */
        .prompt-box-marker {{
            display: block;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            line-height: 0 !important;
        }}
        
        /* 프롬프트 박스 바깥 부모 블록 테두리 강제 제거 */
        div[data-testid="stVerticalBlock"]:has(.prompt-box-marker) 
        div[data-testid="stVerticalBlock"]:not(:has(.prompt-box-marker)) {{
            background: transparent !important;
            border: none !important;
            border-radius: 0 !important;
            padding: 0 !important;
        }}
        
        /* 2. 본문 텍스트 설정 */
        div[data-testid="stVerticalBlock"]:has(.prompt-box-marker) p,
        div[data-testid="stVerticalBlock"]:has(.prompt-box-marker) li {{
            color: #ffffff !important;
            font-size: 16px !important;
            line-height: 1.8 !important;
        }}

        /* 3. 제목(##) 파란색 세로선 스타일 */
        div[data-testid="stVerticalBlock"]:has(.prompt-box-marker) h2 {{
            border-left: 4px solid #adc6ff !important; 
            padding-left: 12px !important;
            margin-top: 32px !important;
            margin-bottom: 16px !important;
            font-size: 18px !important;
            font-weight: 700 !important;
            color: #ffffff !important;
        }}
        
        div[data-testid="stVerticalBlock"]:has(.prompt-box-marker) h3:first-of-type {{
            margin-top: 0 !important; 
        }}

        /* 4. 소제목(###) 스타일 */
        div[data-testid="stVerticalBlock"]:has(.prompt-box-marker) h3 {{
            font-size: 15px !important;
            color: #c2c6d6 !important;
            margin-top: 16px !important;
            margin-bottom: 8px !important;
        }}
        /* 기존 p, li 스타일 있는 곳 근처에 추가 */
        div[data-testid="stVerticalBlock"]:has(.prompt-box-marker) strong {{
            color: #4edea3 !important;  
            font-weight: 700 !important;
        }}
        /* 성공 알림 배너 */
        .success-banner {{
            background: #00311f;
            border: 1px solid rgba(0, 165, 114, 0.3);
            border-radius: 8px;
            padding: 10px 16px;
            color: #4edea3;
            font-size: 13px;
            display: flex;
            align-items: center;
            gap: 8px;
            margin-top: 24px;
        }}
                
        /* ── 아예 배경 없이 텍스트만 보이게 할 경우 ── */
        pre, code {{
            background-color: transparent !important;
            border: none !important;
            color: #e1e2ec !important;
            padding: 0 !important;
        }}
        
        /* 메인 영역 히스토리 탭(Expander) 다크 테마 적용 */
        [data-testid="stMain"] [data-testid="stExpander"] {{
            background: #1d2027 !important;
            border: 1px solid #424754 !important;
            border-radius: 8px !important;
        }}
        [data-testid="stMain"] [data-testid="stExpander"] summary {{
            background: #272a31 !important;
        }}
        [data-testid="stMain"] [data-testid="stExpander"] summary p {{
            color: #adc6ff !important; /* 글씨를 잘 보이는 밝은 파란색으로 */
            font-weight: 600 !important;
        }}
        [data-testid="stMain"] [data-testid="stExpander"] summary:hover {{
            background: #32353c !important;
        }}
        /* ── 상세 지시사항 회색 박스 (Blockquote 디자인 하이재킹) ── */
        div[data-testid="stVerticalBlock"]:has(.prompt-box-marker) blockquote {{
            background-color: #272a31 !important; /* 이미지와 같은 밝은 다크그레이 */
            border-left: none !important; /* 기본 인용구의 왼쪽 선 제거 */
            border-radius: 8px !important;
            padding: 16px 20px !important;
            margin: 16px 0 !important;
        }}
        
        /* 박스 안의 텍스트 간격 조절 */
        div[data-testid="stVerticalBlock"]:has(.prompt-box-marker) blockquote p,
        div[data-testid="stVerticalBlock"]:has(.prompt-box-marker) blockquote li {{
            color: #e1e2ec !important;
            margin-bottom: 6px !important;
            font-size: 15px !important;
        }}

        /* ── 맥락 및 제약 하위 리스트 디자인 ── */
        /* 리스트 항목들이 조금 더 여유롭게 떨어져 보이도록 설정 */
        div[data-testid="stVerticalBlock"]:has(.prompt-box-marker) ul {{
            margin-top: 12px !important;
            margin-bottom: 20px !important;
        }}
        div[data-testid="stVerticalBlock"]:has(.prompt-box-marker) li {{
            margin-bottom: 8px !important;
        }}
                
        /* ── 맥락 및 제약 가로 2단 박스 디자인 ── */
        .context-grid {{
            display: flex;
            gap: 12px;           /* 박스 사이 간격 */
            margin: 16px 0;      /* 위아래 여백 */
        }}

        .context-item {{
            flex: 1;             /* 반반씩 너비 차지 */
            padding: 14px 18px;
            background: rgba(255, 255, 255, 0.03) !important; /* 은은한 배경색 */
            border: 1px solid rgba(66, 71, 84, 0.5) !important;
            border-radius: 10px !important;
        }}

        /* 상단 라벨 (대상 독자 / 제약 사항 글씨) */
        .context-item b {{
            display: inline;       /* block → inline 으로 변경 */
            font-size: 14px !important;
            color: #8c909f !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        /* 박스 내부 본문 글씨 */
        .context-item {{
            color: #ffffff !important;
            font-size: 14px !important;
            line-height: 1.5;
        }}
        /* components iframe 버튼 배경 투명 처리 */
        iframe {{
            background: transparent !important;
            border: none !important;
        }}
        /* 맥락 및 제약 카드 그리드 */
        .context-grid2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;  /* ← 2컬럼으로 나누기 */
            gap: 12px;
            margin: 12px 0;
        }}
        .context-item2 {{
            background: #272a31;
            border: 1px solid #424754;
            border-radius: 8px;
            padding: 14px 16px;
        }}
    </style>
    """

