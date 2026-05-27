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

def build_prompt(topic, data_desc, audience, goals, metrics, requirements, complexity_level):
    # 태그와 지표를 각각 쉼표로 연결합니다.
    goal_str = ", ".join(goals) if goals else "일반 분석"
    metrics_str = ", ".join(metrics) if metrics else "AI 자동 추천"

    return f"""
    당신은 Tableau 대시보드 설계를 돕는 수석 BI 컨설턴트 및 UI/UX 디자이너입니다. 사용자가 입력한 정보를 바탕으로 최적의 Tableau 대시보드 구성을 한국어로 추천해주세요.
    이미지는 총 세 개의 이미지를 제공하며 대시보드 관련 이미지의 경우 하단에 제공한 템플릿과 UI 요소, 그리고 사용자가 입력한 대시보드 설계 정보 프롬프트를 바탕으로 비즈니스 KPI 대시보드 프리뷰 화면으로 구성합니다. 
    대시보드 프리뷰 화면 이미지 속 언어는 영문으로 번역합니다. 이미지 속 색상은 하단에 색상 팔레트 추천 항목에서 언급된 색상을 사용합니다.
    
    추천뷰 구성의 경우 영문이 아닌 한글로 답변을 출력합니다.
    
    레이아웃 구성과 색상 팔레트 추천 항목 두 개에 각각 하단에 제공한 html 코드를 기반으로 개별 생성합니다. 
    다음 제약 조건을 엄격히 지켜서 HTML/CSS 코드를 생성하세요.
        > 하단에 제공된 HTML 템플릿의 기본 구조와 디자인 스타일은 절대 변경하지 마세요.
        > 사용자 입력 데이터에 따라 내부의 '텍스트 내용'과 '뷰(View)의 배치'만 동적으로 수정하여 적용하세요.
    추천할 색상은 하단에 제공한 색상 팔레트와 동일한 색상일 필요는 없으며 전체 추천 내용에 알맞는 색상 팔레트를 동일한 개수와 구성에 맞추어서 제공합니다.
    레이아웃 구성은 상단 대시보드 프리뷰 이미지와 동일한 구성, 배치를 보여주세요.

    전문가 팁을 제공할 때 내용은 최대한 상세하게, 대신 출력 내용은 간결하면서도 이해하기 쉽게 설명을 하도록 해주세요.
    
    신뢰도 점수는 AI기반 점수이나 전체 내용과 맥락을 바탕으로 BI 컨설턴트가 제시할 수 있는 AI 스스로 계산한 점수입니다.

    ## 입력 정보
    - 대시보드 주제: {topic}
    - 데이터 설명: {data_desc}
    - 주요 대상: {audience}
    - 분석 목표 (Goal): {goal_str}
    - 필수 포함 지표 (Metrics): {metrics_str}
    - 복잡도: {complexity_level}
    - 추가 요구사항: {requirements if requirements else "없음"}

    ## 출력할 대시보드 이미지 (UI 요소)
    대시보드 UI/UX 템플릿 프롬프트는 아래와 같습니다.

    [전체 스타일 & 테마 (Overall Style)]
        - Theme: Modern Executive Dashboard, Clean, Minimalist, Data-Driven, Professional, B2B SaaS style.
        - UI Type: Card-based UI (각 차트가 개별 박스/카드 안에 담긴 형태).
        - Color Palette: 연한 회색(또는 어두운 네이비) 전체 배경 위에, 대비되는 흰색(또는 진한 회색) 카드 컨테이너 배치. 포인트 컬러는 1~2개(파란색, 빨간색 등)로 제한하여 최소한의 색상으로 강조.
        - Typography: 깔끔한 산세리프(고딕) 폰트, 강한 시각적 위계 (숫자는 크고 진하게, 축/설명은 작고 연한 회색으로).

    [UI 디테일 가이드 (UI Details)]
        Padding & Margin: 카드 내부 콘텐츠가 테두리에 닿지 않도록 넉넉한 내부 여백(Inner Padding) 확보.
        Clean Data Ink: 불필요한 테두리선, 눈금선(Grid lines) 제거. 데이터 잉크 비율 최적화.
        Navigation: (필요시) 좌측 좁은 사이드바에 아이콘 형태의 메뉴 네비게이션 배치.
        사용자가 입력한 내용 기반으로 대시보드 이미지 생성할 것. (배치나 구성 전부 사용자 입력 내용 혹은 프롬프트 기반으로 할 것)
        차트 구성 시 무조건 개수나 여백을 채울 필요는 없음. 만약 채울 내용이 없으면 차트 크기 조절할 것.
    
    # 레이아웃 구성과 색상 팔레트 추천 항목 (샘플 UI 요소-동적 코딩 필요)
    ```
    # ── 레이아웃 구성 + 색상 팔레트 (img2 스타일, 2컬럼) ──
    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
    col_lay, col_clr = st.columns(2, gap="large")

    layout = result.get("layout", {{}})
    color  = result.get("color_scheme", {{}})

    # 레이아웃 구성 항목
    with col_lay:
        st.markdown('<h2 class="section-title">레이아웃 구성</h2>', unsafe_allow_html=True)
        st.markdown('''
        <div class="wireframe-wrap">
            <div class="wf-block wf-header">Header / Filter Bar</div>
            <div class="wf-block wf-main">Primary Visualization</div>
            <div class="wf-block">Side Widget</div>
            <div class="wf-block">Action Card</div>
        </div>
        ''', unsafe_allow_html=True)
        st.markdown(f'''
        <p style="font-size:14px;color:#43474e;line-height:1.6;margin-top:12px;">
            {{layout.get('description','')}} {{layout.get('arrangement','')}}
        </p>
        ''', unsafe_allow_html=True)

    # 색상 팔레트 추천 항목
    with col_clr:
        st.markdown('<h2 class="section-title">색상 팔레트 추천</h2>', unsafe_allow_html=True)
        primary_theme  = color[0].get("primary_theme", "Trustworthy Blue")
        colors_list    = color[0].get("colors", ["#002045","#0351D3","#356CED","#1A365D"])
        accent_list    = color[0].get("accent_colors", ["#FFDDBA","#BA1A1A","#C4C6CF","#E3E2E6"])
        text_colors_p  = ["white","white","white","#86a0cd"]
        text_colors_a  = ["#321b00","white","#43474e","#43474e"]

        primary_swatches = "".join([
            f'<div class="palette-swatch" style="background:{{c}};color:{{tc}};font-size:11px;font-weight:600;">{{c.upper()}}</div>'
            for c, tc in zip(colors_list, text_colors_p)
        ])
        accent_swatches = "".join([
            f'<div class="palette-swatch" style="background:{{c}};color:{{tc}};font-size:11px;font-weight:600;">{{c.upper()}}</div>'
            for c, tc in zip(accent_list, text_colors_a)
        ])

        st.markdown(f'''
        <div class="section-card" style="padding:20px;">
            <p style="font-size:15px;color:#43474e;margin:0 0 6px 0;">Primary Theme: {{primary_theme}}</p>
            <div class="palette-bar">{{primary_swatches}}</div>
            <p style="font-size:15px;color:#43474e;margin:12px 0 6px 0;">Accent & Semantic Colors</p>
            <div class="palette-bar">{{accent_swatches}}</div>
            <div style="margin-top:12px;">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
                    <div style="width:8px;height:8px;border-radius:50%;background:#0351d3;"></div>
                    <span style="font-size:15px;color:#43474e;">
                        핵심 데이터 시각화에는 <strong>Secondary Blue</strong>를 사용하여 신뢰감을 부여합니다.
                    </span>
                </div>
                <div style="display:flex;align-items:center;gap:8px;">
                    <div style="width:8px;height:8px;border-radius:50%;background:#ffddba;"></div>
                    <span style="font-size:15px;color:#43474e;">
                        AI 추천 및 강조 포인트에는 <strong>Warm Amber</strong>를 사용하여 주목도를 높입니다.
                    </span>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True) 
    ```

    ## 출력 형식 (반드시 아래 JSON 형식으로만 응답)
    ```json
    {{
        "summary": "대시보드 전체 개요 (2~3문장)",
        "confidence_score": "신뢰도 점수 (예: 98.4%)",
        "data_source": "데이터 소스 (예: SQL, CSV)",
        "update_cycle": "업데이트 주기",
        "user_group": "사용자 그룹",
        "image_prompt": "실제 Tableau 대시보드 UI 이미지를 생성하기 위한 '매우 상세한 영문 프롬프트'. B2B SaaS 스타일, Modern Executive Dashboard, 지정된 핵심 지표와 차트(Bar, Line, Map 등)가 화면에 어떻게 배치되어 있는지 구체적으로 묘사하세요. 텍스트 지시가 아닌 시각적 묘사여야 합니다.",
        "views": [
            {{
                "name": "뷰/시트 이름 (영문, 예: Global Sales Trend)",
                "chart_type": "차트 타입 (예: Line Chart, Bar Chart, Heatmap, Pie Chart)",
                "purpose": "이 뷰의 목적 및 활용 방안 즉, 이 뷰가 왜 필요한지, 어떤 인사이트를 제공하는지, 누가 어떻게 활용하는지를 정리하여 반드시 3문장으로 작성. 예: '지역별 매출을 시계열로 분석하여 성장 트get_recommendation(api_key, model, prompt):렌드를 파악합니다. 전년 대비 성장률(YoY)을 오버레이하여 계절성 변동을 직관적으로 확인할 수 있습니다. 영업 담당자와 경영진이 지역별 전략 수립 시 활용합니다.'",
                "fields": ["필드명1", "필드명2"],
                "tableau_tip": "Tableau 구현 팁",
                "icon": "material symbols 아이콘명 (예: trending_up, bar_chart, pie_chart, map, group, confirmation_number)"
            }}
        ],
        "filters": ["추천 필터1", "추천 필터2"],
        "parameters": ["추천 파라미터1"],
        "implementation_steps": [
            {{"title": "Data Preparation", "desc": "단계 설명", "icon": "database"}},
            {{"title": "Model Building", "desc": "단계 설명", "icon": "query_stats"}},
            {{"title": "Dashboard Design", "desc": "단계 설명", "icon": "dashboard_customize"}}
        ],
        "pro_tips": [
            {{"type": "performance", "title": "팁 제목", "content": "상세 내용", "label": "PERFORMANCE"}},
            {{"type": "kpi", "title": "KPI 시각화 전략", "content": "내용"}},
            {{"type": "filter", "title": "효율적인 필터링", "content": "내용"}},
            {{"type": "dynamic", "title": "동적 매개변수 활용", "content": "내용"}}
        ], 
        "layout": [{{
            "description": "전체 레이아웃 설명",
            "arrangement": "뷰 배치 방식 설명",
            "wireframe_html": "대시보드 레이아웃을 시각적으로 보여주는 HTML코드. ★필수★ 레이아웃과 구성, 배치는 상단 대시보드 프리뷰 이미지와 동일하게 구성해서 보여줄 것. 글씨는 가운데 정렬하고 각 카드 간의 간격 혹은 높이/너비를 균형 있게(예: min-height: 100px) 설정하여 최상위 컨테이너는 반드시 class='wireframe-wrap'을 사용할 것 (border, padding, border-radius가 이미 CSS에 정의되어 있음). 내부 개별 카드는 class='wf-block'을 기본으로 사용하고, 주요 시각화 영역은 class='wf-block wf-main'을 사용할 것. 헤더/필터 영역은 class='wf-block wf-header'를 사용할 것. 배경(#f4f3f7)과 테두리(1px solid #c4c6cf), border-radius(8px)를 적용  ★주의★ JSON 파싱 에러를 막기 위해 HTML 속성 작성 시 반드시 작은따옴표(')만 사용. grid 배치 조정이 필요한 경우 style='grid-column:1/-1' 등 인라인 스타일 추가 가능. 카드 텍스트는 실제 views의 name과 chart_type을 반영할 것. 예시: <div class='wireframe-wrap'><div class='wf-block wf-header'>Filter: Region · Date</div><div class='wf-block wf-main'>Global Sales Trend · Line Chart</div><div class='wf-block'>Revenue KPI</div><div class='wf-block'>CS Overview · Pie Chart</div></div>"
        }}],        
        "color_scheme": [{{
            "primary_theme": "테마 이름",
            "colors": ["#HEX1", "#HEX2", "#HEX3", "#HEX4"],
            "accent_colors": ["#HEX1", "#HEX2", "#HEX3", "#HEX4"],
            "rationale": "이 색상들을 추천하는 구체적인 이유",
        }}]
    }}```
    JSON 외에 마크다운 기호(```json 등)나 다른 텍스트는 절대 출력하지 마세요.
    """