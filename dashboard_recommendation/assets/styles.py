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

def apply_custom_colors():
    # ── 공통 색상 토큰 (HTML과 동일) ─────────────────────────────────
    COLORS = {
        "primary":        "#002045",
        "secondary":      "#0351d3",
        "sec_container":  "#356ced",
        "bg":             "#f4f3f7",
        "surface":        "#ffffff",
        "surface_low":    "#f4f3f7",
        "outline":        "#74777f",
        "outline_var":    "#c4c6cf",
        "on_surface":     "#1a1c1e",
        "on_surface_var": "#43474e",
        "tertiary_fixed": "#ffddba",
        "error":          "#ba1a1a",
        "inverse_surface":"#2f3033",
    }
    return COLORS

COLORS = apply_custom_colors()

def apply_custom_css(COLORS):
    # ── 전체 CSS ─────────────────────────────────────────────────────
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        background-color: {COLORS['bg']};
        color: {COLORS['on_surface']};
    }}

    /* ── Streamlit 기본 요소 ── */
    /* ── 최상단 고정 헤더 ── */
    .top-navbar {{
        position: fixed;
        top: 0; left: 0; right: 0;
        height: 64px;
        background: {COLORS['surface']};
        border-bottom: 1px solid {COLORS['outline_var']};
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 24px;
        z-index: 999;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }}
    .top-navbar .brand {{
        font-size: 20px;
        font-weight: 700;
        color: {COLORS['primary']};
        letter-spacing: -0.3px;
    }}
    .top-navbar nav a {{
        font-size: 12px;
        font-weight: 500;
        color: {COLORS['on_surface_var']};
        text-decoration: none;
        margin-left: 40px;
        padding-bottom: 4px;
        transition: color 0.2s;
    }}
    .top-navbar nav a.active {{
        color: {COLORS['secondary']};
        border-bottom: 2px solid {COLORS['secondary']};
    }}
    .top-navbar .icons {{
        display: flex;
        align-items: center;
        gap: 16px;
    }}
    .top-navbar .icons .material-symbols-outlined {{
        color: {COLORS['primary']};
        cursor: pointer;
        font-size: 22px;
    }}
    .top-navbar .avatar {{
        width: 32px; height: 32px;
        border-radius: 50%;
        background: {COLORS['outline_var']};
        display: flex; align-items: center; justify-content: center;
        color: {COLORS['primary']};
        font-weight: 700;
        font-size: 13px;
    }}

    /* ── 사이드바 ── */
    [data-testid="stSidebar"] {{
        background-color: {COLORS['surface_low']};
        border-right: 1px solid {COLORS['outline_var']};
        padding-top: 80px;
        width: 260px !important; 
    }}
    [data-testid="stSidebar"] > div:first-child {{
        padding-top: 0;
    }}

    /* 사이드바 내부 텍스트 */
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] p {{
        color: {COLORS['on_surface_var']} !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    /* 사이드바 입력 */
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] select,
    [data-testid="stSidebar"] [data-baseweb="select"] {{
        background: {COLORS['surface']} !important;
        border: 1px solid {COLORS['outline_var']} !important;
        border-radius: 8px !important;
        color: {COLORS['on_surface']} !important;
        font-size: 14px !important;
    }}
    [data-testid="stSidebar"] input::placeholder {{
        color: {COLORS['outline']} !important;
        opacity: 1 !important;
    }}

    /* 사이드바 버튼 (API Configuration 탭과 완벽 동일하게 맞춤) */
    [data-testid="stSidebar"] button[kind="secondary"] {{
        background: #356ced !important; /* API Config 배경색 */
        border: none !important;
        border-radius: 8px !important;
        width: 100% !important;
        padding: 10px 14px !important;
        margin-top: 12px !important;
        transition: opacity 0.2s !important;
    }}

    /* 상단의 범용 p 태그 속성으로 인해 버튼 글씨가 회색/대문자로 깨지는 것을 방어 */
    [data-testid="stSidebar"] button[kind="secondary"] p,
    [data-testid="stSidebar"] button[kind="secondary"] div {{
        color: #ffffff !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        text-transform: none !important; /* 강제 대문자 변환 방지 */
        letter-spacing: 0 !important;
    }}

    [data-testid="stSidebar"] button[kind="secondary"]:hover {{
        opacity: 0.88 !important;
    }}

    /* ── 메인 영역 상단 여백 (고정 헤더 높이) ── */
    .main-content-wrap {{
        margin-top: 8px;
        padding: 8px 20px 30px 20px;
    }}

    /* ── 페이지 헤더 ── */
    .page-header h1 {{
        font-size: 32px;
        font-weight: 600;
        color: {COLORS['primary']};
        margin: 0 0 6px 0;
        line-height: 1.3;
    }}
    .page-header p {{
        font-size: 16px;
        color: {COLORS['on_surface_var']};
        margin: 0;
        line-height: 1.6;
    }}

    /* ── 섹션 카드 ── */
    .section-card {{
        background: {COLORS['surface']};
        border: 1px solid {COLORS['outline_var']};
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 16px;
        box-shadow: 0 2px 4px rgba(45,102,231,0.04);
    }}
    .section-card-title {{
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 16px;
        font-weight: 600;
        color: {COLORS['primary']};
        margin-bottom: 16px;
    }}
    .section-card-title .material-symbols-outlined {{
        color: {COLORS['secondary']};
        font-size: 20px;
    }}

    /* ── 데이터 테이블 ── */
    .data-table {{
        width: 100%;
        border-collapse: collapse;
    }}
    .data-table th {{
        padding: 8px 12px;
        text-align: left;
        font-size: 11px;
        font-weight: 600;
        color: {COLORS['on_surface_var']};
        background: {COLORS['surface_low']};
        border-bottom: 1px solid {COLORS['outline_var']};
    }}
    .data-table td {{
        padding: 14px 12px;
        font-size: 14px;
        color: {COLORS['on_surface']};
        border-bottom: 1px solid {COLORS['outline_var']};
    }}
    .data-table tr:last-child td {{ border-bottom: none; }}
    .type-badge {{
        font-size: 13px;
        font-weight: 500;
        color: {COLORS['secondary']};
    }}
    .type-badge.measure {{ color: {COLORS['secondary']}; }}
    .type-badge.dimension {{ color: {COLORS['secondary']}; }}
    .type-badge.date {{ color: {COLORS['secondary']}; }}

    /* ── Goal Tag 버튼 ── */
    .goal-tags-wrap {{
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 4px;
    }}
    .goal-tag {{
        display: inline-block;
        padding: 6px 16px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 500;
        cursor: pointer;
        border: 1px solid {COLORS['outline_var']};
        background: {COLORS['surface_low']};
        color: {COLORS['on_surface_var']};
        transition: all 0.15s;
    }}
    .goal-tag.active {{
        background: {COLORS['secondary']};
        color: white;
        border-color: {COLORS['secondary']};
    }}

    /* ── 복잡도 슬라이더 라벨 ── */
    .complexity-labels {{
        display: flex;
        justify-content: space-between;
        margin-top: 6px;
        font-size: 11px;
        color: {COLORS['on_surface_var']};
        font-weight: 600;
    }}

    /* ── 액션 버튼 영역 ── */
    .action-buttons {{
        display: flex;
        justify-content: flex-end;
        gap: 12px;
        padding-top: 16px;
    }}
    .btn-outline {{
        padding: 12px 28px;
        border: 1px solid {COLORS['secondary']};
        color: {COLORS['secondary']};
        background: transparent;
        border-radius: 8px;
        font-size: 15px;
        font-weight: 600;
        cursor: pointer;
        transition: background 0.2s;
        font-family: 'Inter', sans-serif;
    }}
    .btn-outline:hover {{ 
        background: rgba(3,81,211,0.05); 
    }}
    .btn-primary {{
        padding: 12px 28px;
        background: {COLORS['secondary']};
        color: white;
        border: none;
        border-radius: 8px;
        font-size: 15px;
        font-weight: 600;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: opacity 0.2s;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 4px 12px rgba(3,81,211,0.3);
    }}
    .btn-primary:hover {{ opacity: 0.9; }}

    /* ── 결과 영역 헤더 카드 ── */
    .result-overview-card {{
        background: {COLORS['surface']};
        border: 1px solid {COLORS['outline_var']};
        border-left: 4px solid {COLORS['secondary']};
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 2px 6px rgba(45,102,231,0.06);
    }}
    .ai-badge {{
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background: {COLORS['tertiary_fixed']};
        color: #321b00;
        padding: 3px 12px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 10px;
    }}
    .overview-meta-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-top: 16px;
        padding-top: 16px;
        border-top: 1px solid {COLORS['outline_var']};
    }}
    .meta-item-label {{
        font-size: 13px;
        font-weight: 600;
        color: {COLORS['outline']};
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 4px;
    }}
    .meta-item-value {{
        font-size: 21px;
        font-weight: 600;
        color: {COLORS['primary']};
        line-height: 1.4;
        word-break: keep-all;
        overflow-wrap: break-word;
    }}

    /* ── 뷰 카드 (추천 뷰 구성) ── */
    .view-card {{
        background: {COLORS['surface']};
        border: 1px solid {COLORS['outline_var']};
        border-radius: 12px;
        padding: 20px;
        height: 300px;
        display: flex;
        flex-direction: column;
        box-shadow: 0 2px 4px rgba(45,102,231,0.04);
        transition: border-color 0.2s;
    }}
    .view-card:hover {{ 
        border-color: {COLORS['secondary']}; 
    }}
    .view-icon-wrap {{
        width: 48px; height: 48px;
        border-radius: 10px;
        background: rgba(53,108,237,0.12);
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 16px;
    }}
    .view-icon-wrap .material-symbols-outlined {{
        color: {COLORS['secondary']};
        font-size: 24px;
    }}
    .view-card h3 {{
        font-size: 15px;
        font-weight: 600;
        color: {COLORS['primary']};
        margin: 0 0 8px 0;
    }}
    .view-card p {{
        font-size: 13px;
        color: {COLORS['on_surface_var']};
        line-height: 1.6;
        flex: 1;
        margin: 0;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 5;
        -webkit-box-orient: vertical;
    }}
    .view-card-footer {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-top: 12px;
        border-top: 1px solid {COLORS['outline_var']};
        margin-top: 12px;
    }}
    .chart-type-badge {{
        font-size: 11px;
        font-weight: 600;
        color: {COLORS['secondary']};
        background: rgba(53,108,237,0.1);
        padding: 2px 8px;
        border-radius: 4px;
    }}
    .view-card-footer .material-symbols-outlined {{
        color: {COLORS['outline']};
        font-size: 18px;
        cursor: pointer;
    }}
    .view-card-footer .material-symbols-outlined:hover {{
        color: {COLORS['secondary']};
    }}

    /* ── 구현 단계 카드 ── */
    .step-card {{
        position: relative;
        background: {COLORS['surface']};
        border: 1px solid {COLORS['outline_var']};
        border-radius: 12px;
        padding: 24px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(45,102,231,0.04);
        transition: border-color 0.2s;
    }}
    .step-card:hover {{ 
        border-color: {COLORS['secondary']}; 
    }}
    .step-number-bg {{
        position: absolute;
        right: -16px; top: -16px;
        width: 80px; height: 80px;
        background: rgba(3,81,211,0.04);
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 40px;
        font-weight: 700;
        color: rgba(0,32,69,0.08);
    }}
    .step-card .material-symbols-outlined {{
        color: {COLORS['secondary']};
        font-size: 32px;
        margin-bottom: 12px;
        display: block;
    }}
    .step-card h3 {{
        font-size: 15px;
        font-weight: 600;
        color: {COLORS['primary']};
        margin: 0 0 8px 0;
    }}
    .step-card p {{
        font-size: 13px;
        color: {COLORS['on_surface_var']};
        line-height: 1.6;
        margin: 0;
    }}

    /* ── 전문가 팁 카드 ── */
    .tip-main-card {{
        background: linear-gradient(135deg, #1a365d 0%, #002045 100%);
        border-radius: 12px;
        padding: 32px;
        position: relative;
        overflow: hidden;
    }}
    .tip-main-card h3 {{
        font-size: 22px;
        font-weight: 600;
        color: white;
        margin: 16px 0 12px 0;
    }}
    .tip-main-card p {{
        font-size: 15px;
        color: rgba(255,255,255,0.8);
        line-height: 1.7;
        max-width: 100%;
        margin: 0 0 24px 0;
        white-space: normal;
    }}
    .perf-badge {{
        display: inline-block;
        background: rgba(53,108,237,0.2);
        color: rgba(255,255,255,0.9);
        padding: 3px 12px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.05em;
    }}
    .tip-side-card {{
        background: {COLORS['surface_low']};
        border: 1px solid {COLORS['outline_var']};
        border-radius: 12px;
        padding: 20px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
    }}
    .tip-side-card h3 {{
        font-size: 15px;
        font-weight: 600;
        color: {COLORS['primary']};
        margin: 8px 0;
    }}
    .tip-side-card p {{
        font-size: 13px;
        color: {COLORS['on_surface_var']};
        line-height: 1.6;
        margin: 0;
    }}
    .tip-filter-card {{
        background: {COLORS['surface']};
        border: 1px solid {COLORS['outline_var']};
        border-left: 4px solid {COLORS['secondary']};
        border-radius: 12px;
        padding: 20px;
        min-height: 140px;   
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}
    .tip-filter-card h3 {{
        font-size: 15px;
        font-weight: 600;
        color: {COLORS['primary']};
        margin: 8px 0;
    }}
    .tip-filter-card p {{
        font-size: 13px;
        color: {COLORS['on_surface_var']};
        line-height: 1.6;
        margin: 0;
    }}
    .tip-amber-card {{
        background: #4f2e00;
        border-radius: 12px;
        padding: 20px;
        display: flex;
        align-items: center;
        gap: 20px;
        min-height: 150px;   /* ← 동일한 값으로 맞추기 */
    }}
    .tip-amber-card .icon-wrap {{
        background: rgba(242,188,130,0.15);
        border-radius: 50%;
        width: 60px; height: 60px;
        display: flex; align-items: center; justify-content: center;
        flex-shrink: 0;
    }}
    .tip-amber-card .icon-wrap .material-symbols-outlined {{
        color: {COLORS['tertiary_fixed']};
        font-size: 32px;
    }}
    .tip-amber-card h3 {{
        font-size: 15px;
        font-weight: 600;
        color: white;
        margin: 0 0 6px 0;
    }}
    .tip-amber-card p {{
        font-size: 13px;
        color: rgba(255,255,255,0.8);
        line-height: 1.6;
        margin: 0;
    }}



    /* ── 색상 팔레트 ── */
    .palette-bar {{
        display: flex;
        height: 56px;
        border-radius: 8px;
        overflow: hidden;
        margin: 8px 0 12px 0;
    }}
    .palette-swatch {{
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        font-weight: 600;
    }}

    /* ── 레이아웃 와이어프레임 ── */
    .wireframe-wrap {{
        background: {COLORS['surface']};
        border: 1px solid {COLORS['outline_var']};
        border-radius: 12px;
        padding: 16px;
        aspect-ratio: 16/9;
        display: grid;
        grid-template-columns: 2fr 1fr;
        grid-template-rows: 1fr 2fr 1fr;
        gap: 6px;
    }}
    .wf-block {{
        background: {COLORS['surface_low']};
        border: 1px solid {COLORS['outline_var']};
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 13px;
        color: {COLORS['outline']};
        font-weight: 600;
    }}
    .wf-header {{
        grid-column: 1 / -1;
    }}
    .wf-main {{
        grid-row: 2 / 4;
        background: rgba(53,108,237,0.06);
        border: 1px solid rgba(53,108,237,0.2);
        color: {COLORS['secondary']};
    }}

    /* ── 섹션 제목 ── */
    .section-title {{
        font-size: 22px;
        font-weight: 600;
        color: {COLORS['primary']};
        margin: 0 0 16px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    .section-title .material-symbols-outlined {{
        color: {COLORS['secondary']};
        font-size: 22px;
    }}

    /* ── 푸터 ── */
    .footer {{
        background: {COLORS['surface']};
        border-top: 1px solid {COLORS['outline_var']};
        padding: 20px 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 40px;
    }}
    .footer p {{
        font-size: 13px;
        color: {COLORS['on_surface_var']};
        margin: 0;
    }}
    .footer a {{
        font-size: 11px;
        color: {COLORS['on_surface_var']};
        text-decoration: none;
        margin-left: 32px;
    }}
    .footer a:hover {{ color: {COLORS['secondary']}; }}

    /* ── Streamlit 버튼 숨기고 HTML 버튼 쓸 때 사용 ── */
    :not([data-testid="stSidebar"]) .stButton > button {{
        background: {COLORS['secondary']} !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        padding: 10px 24px !important;
        transition: opacity 0.2s !important;
        font-family: 'Inter', sans-serif !important;
    }}
    :not([data-testid="stSidebar"]) .stButton > button:hover {{
        opacity: 0.9 !important;
    }}
    .stButton > button:hover {{
        opacity: 0.9 !important;
    }}
    .material-symbols-outlined {{
        font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
    }}

    /* ── 결과 Export 버튼 라인 ── */
    .result-action-bar {{
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        margin-bottom: 24px;
    }}
    .export-btns {{ display: flex; gap: 10px; }}
    .btn-sm-outline {{
        padding: 8px 16px;
        border: 1px solid {COLORS['secondary']};
        color: {COLORS['secondary']};
        background: transparent;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 600;
        cursor: pointer;
        font-family: 'Inter', sans-serif;
    }}
    .btn-sm-primary {{
        padding: 8px 16px;
        background: {COLORS['secondary']};
        color: white;
        border: none;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 600;
        cursor: pointer;
        display: flex; align-items: center; gap: 6px;
        font-family: 'Inter', sans-serif;
    }}

    /* 입력 필드 */
    .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] {{
        border: 1px solid {COLORS['outline_var']} !important;
        border-radius: 8px !important;
        background: {COLORS['surface']} !important;
        color: {COLORS['on_surface']} !important;
        font-size: 14px !important;
    }}
    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {{
        color: {COLORS['outline']} !important;
        opacity: 1 !important;
    }}
    .stTextInput input:focus,
    .stTextArea textarea:focus {{
        border-color: {COLORS['secondary']} !important;
    }}

    /* data_editor */
    [data-testid="stDataEditor"] {{
        border: 1px solid {COLORS['outline_var']} !important;
        border-radius: 8px !important;
        overflow: hidden;
    }}

    /* ── 사이드바 커스텀 탭 (st.radio를 예쁜 HTML 버튼처럼 변장) ── */
    /* 1. 기본 라디오 버튼 동그라미 숨기기 */
    [data-testid="stSidebar"] [role="radiogroup"] label > div:first-child {{
        display: none !important;
    }}

    /* 2. 버튼들을 묶는 그룹 디자인 */
    [data-testid="stSidebar"] [role="radiogroup"] {{
        gap: 4px !important;
        margin-bottom: 20px !important;
    }}

    /* 3. 개별 탭(기본 상태) 디자인 - 사용자가 짠 HTML과 동일하게 적용 */
    [data-testid="stSidebar"] [role="radiogroup"] label {{
        display: flex !important;
        align-items: center !important;
        padding: 10px 14px !important;
        border-radius: 8px !important;
        color: #43474e !important;
        background-color: transparent !important;
        cursor: pointer !important;
        margin: 0 !important;
        width: 100% !important;
        transition: all 0.2s !important;
    }}
    [data-testid="stSidebar"] [role="radiogroup"] label:hover {{
        background: rgba(53, 108, 237, 0.08) !important;
    }}

    /* 4. 선택된 탭(Active) 디자인 (파란색 바탕) */
    [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {{
        background: #356ced !important;
        transform: translateX(2px) !important;
    }}

    /* 5. 텍스트 디자인 설정 */
    [data-testid="stSidebar"] [role="radiogroup"] label p {{
        font-size: 13px !important;
        font-weight: 500 !important;
        margin: 0 !important;
        color: inherit !important;
    }}

    /* 6. 선택된 탭의 글씨 색상을 흰색으로 */
    [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p {{
        color: #ffffff !important;
    }}

    .wireframe-wrap-dynamic {{
        background: #ffffff;
        border: 1px solid #c4c6cf;
        border-radius: 12px;
        padding: 16px;
        min-height: 320px;
    }}

    .dynamic-block {{
        background: #f4f3f7;
        border: 1px solid #c4c6cf;
        border-radius: 8px;
        padding: 12px;
        font-size: 12px;
        color: #43474e;
        font-weight: 600;
    }}
    </style>
    """
    return css 