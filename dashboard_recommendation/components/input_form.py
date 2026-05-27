import streamlit as st
import pandas as pd
from utils.state import init_session_state

def render_input_section():
    init_session_state()

    st.markdown('<div class="main-content-wrap">', unsafe_allow_html=True)

    st.markdown("""
    <div class="page-header" style="margin-bottom:28px;">
        <h1>대시보드 정보 입력</h1>
        <p>AI가 최적의 시각화 구성을 제안할 수 있도록 대시보드와 데이터의 상세 정보를 입력해주세요.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    .topic-card-header {
        background: #ffffff;
        border: 1px solid #c4c6cf;
        border-bottom: none;
        border-radius: 12px 12px 0 0;
        padding: 24px 24px 8px 24px;  
        margin-bottom: -1rem;
    }
    .topic-card-title {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 16px;
        font-weight: 600;
        color: #002045;
    }
    .topic-card-title .material-symbols-outlined {
        color: #0351d3;
        font-size: 20px;
    }
    div[data-testid="stTextInput"]:has(input[aria-label="dashboard_topic_label"]) {
        background: #ffffff;
        border: 1px solid #c4c6cf;
        border-top: none;
        border-radius: 0 0 12px 12px;
        padding: 0 24px 24px 24px;
        box-shadow: 0 2px 4px rgba(45,102,231,0.04);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="topic-card-header">
        <div class="topic-card-title">
            <span class="material-symbols-outlined">dashboard</span>
            대시보드 주제
        </div>
    </div>
    """, unsafe_allow_html=True)

    dashboard_topic = st.text_input(
        "dashboard_topic_label", 
        label_visibility="collapsed",
        placeholder="예: 2024년 4분기 글로벌 매출 현황 및 분석",
        key="dashboard_topic"
    )

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    st.markdown("""
    <style>
    div[data-testid="stHorizontalBlock"]:has(.data-header-marker) {
        background: #ffffff;
        border: 1px solid #c4c6cf;
        border-radius: 12px !important;
        padding: 16px 24px;
        height: 130px !important;
        align-items: center;
        position: relative;
        z-index: 6;
    }
    .data-header-marker {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 16px;
        font-weight: 600;
        color: #002045;
    }
    .data-header-marker .material-symbols-outlined {
        color: #0351d3;
        font-size: 20px;
    }
    div[data-testid="stHorizontalBlock"]:has(.data-header-marker) button {
        background-color: #2A477A !important;
        border: 1px solid #c4c6cf !important;
        color: #ffffff !important; 
        padding: 0px 16px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        align-items: center;
        border-radius: 6px !important;
        float: right;
    }
    div[data-testid="stHorizontalBlock"]:has(.data-header-marker) button:hover {
        background-color: #CAD7ED !important;
        border-color: #CAD7ED !important;
    }
    div[data-testid="stDataEditor"] {
        border: 1px solid #c4c6cf !important;
        border-radius: 12px !important;
        margin-top: 20px !important;
        overflow: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

    col_title, col_add, col_del = st.columns([8, 1, 1])

    with col_title:
        st.markdown("""
        <div class="data-header-marker">
            <span class="material-symbols-outlined">database</span>
            데이터 설명
        </div>
        """, unsafe_allow_html=True)

    with col_add:
        add_clicked = st.button("➕ 필드 추가", use_container_width=True, type="primary")

    with col_del:
        del_clicked = st.button("🗑️ 선택 삭제", use_container_width=True, type="secondary")

    edited_df = st.data_editor(
        st.session_state.fields_df,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config={
            "선택": st.column_config.CheckboxColumn("선택", default=False, width="small"),
            "Type": st.column_config.SelectboxColumn("Type", options=["Date", "Number", "String"], required=True)
        },
        key="data_editor_fields",
    )

    if add_clicked:
        new_row = pd.DataFrame([{"선택": False, "Field Name": "", "Type": "Dimension", "Usage / Description": ""}])
        st.session_state.fields_df = pd.concat([st.session_state.fields_df, new_row], ignore_index=True)
        st.rerun()

    if del_clicked:
        filtered_df = edited_df[edited_df["선택"] == False].reset_index(drop=True)
        if filtered_df.empty:
            filtered_df = pd.DataFrame(columns=["선택", "Field Name", "Type", "Usage / Description"])
        st.session_state.fields_df = filtered_df
        st.rerun()

    data_description = edited_df.drop(columns=["선택"]).to_string(index=False)
    st.markdown("<div style='height:3px'></div>", unsafe_allow_html=True)

    col_goal, col_complex = st.columns(2, gap="medium")

    with col_goal:
        st.markdown("""
        <style>
        div[data-testid="stVerticalBlock"]:has(.goal-marker-target) {
            background-color: #ffffff;
            border: 1px solid #c4c6cf;
            border-radius: 12px;
            padding: 20px 24px;
            box-shadow: 0 2px 4px rgba(45,102,231,0.04);
        }
        .goal-marker-target {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 16px;
            font-weight: 600;
            color: #002045;
            margin-bottom: 12px;
        }
        .goal-marker-target .material-symbols-outlined {
            color: #0351d3;
            font-size: 20px;
        }
        div[data-testid="stPills"] [data-selected="true"] {
            background-color: #0351d3 !important;
            color: white !important;
            border-color: #0351d3 !important;
        }
        div[data-testid="stPills"] [data-selected="false"] {
            background-color: #f4f3f7 !important;
            color: #43474e !important;
            border-color: #c4c6cf !important;
            transition: all 0.2s;
        }
        div[data-testid="stPills"] [data-selected="false"]:hover {
            border-color: #0351d3 !important;
            color: #0351d3 !important;
        }
        div[data-testid="stPills"] [data-testid="stMarkdownContainer"] p {
            font-size: 13px !important;
            font-weight: 500 !important;
        }
        </style>

        <div class="goal-marker-target">
            <span class="material-symbols-outlined">ads_click</span>
            분석 목표 (Goal Tags)
        </div>
        """, unsafe_allow_html=True)

        GOAL_TAGS = ["Monitoring", "KPI Tracking", "Trend Analysis", "Data Mining", "Forecasting", "+ Add Custom"]

        selected_goals = st.pills(
            "분석 목표 선택",
            options=GOAL_TAGS,
            default=["Monitoring", "Trend Analysis"],
            selection_mode="multi",
            label_visibility="collapsed"
        )

        if "+ Add Custom" in (selected_goals or []):
            custom_goal = st.text_input(
                "커스텀 목표 입력",
                placeholder="예: Cohort Analysis, Funnel Tracking ...",
                label_visibility="collapsed",
                key="custom_goal_input"
            )
            if custom_goal:
                selected_goals = [g for g in selected_goals if g != "+ Add Custom"] + [custom_goal]
        else:
            custom_goal = ""

    with col_complex:
        st.markdown("""
        <div class="section-card" style="margin-bottom: 28px;">
            <div class="section-card-title" style="display: flex; align-items: center;">
                <span class="material-symbols-outlined" style="margin-right: 8px;">speed</span>
                분석 복잡도 (Complexity)
                <span class="material-symbols-outlined" 
                      style="font-size: 16px; color: #74777f; cursor: help; margin-left: 6px;" 
                      title="[복잡도 단계 안내]&#10;1: 간단 (뷰 1~2개)&#10;2: 간단-보통&#10;3: 보통 (뷰 3~5개)&#10;4: 보통-복잡&#10;5: 복잡 (뷰 6개+)">
                    info
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        complexity_val = st.slider(
            "complexity_label", label_visibility="collapsed",
            min_value=1, max_value=5, value=3, step=1,
            key="complexity_slider"
        )
        
        st.markdown("""
        <div class="complexity-labels">
            <span>Simple</span><span>Standard</span><span>Advanced</span>
        </div>
        """, unsafe_allow_html=True)
        complexity_map = {1:"간단 (뷰 1~2개)", 2:"간단-보통", 3:"보통 (뷰 3~5개)", 4:"보통-복잡", 5:"복잡 (뷰 6개+)"}
        complexity = complexity_map[complexity_val]

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    with st.expander("추가 요구사항 입력 (선택)"):
        col_aud, col_pur = st.columns(2)
        with col_aud:
            target_audience = st.selectbox(
                "주요 대상 (보고 받는 사람)",
                ["경영진 / C-Level", "팀장 / 중간관리자", "실무 담당자", "고객 / 외부"],
                index=2
            )
        with col_pur:
            METRIC_OPTIONS = [
                "총 매출 및 성장률 (Revenue & Growth)",
                "영업이익 및 이익률 (Profit & Margin)",
                "고객 확보 비용 (CAC) 및 생애가치 (LTV)",
                "사용자 유지율 및 이탈률 (Retention & Churn)",
                "재고 회전율 (Inventory Turnover)",
                "웹/앱 트래픽 및 전환율 (Traffic & CVR)",
                "기타 (AI가 데이터에 맞게 자동 추천)"
            ]
            selected_metrics = st.multiselect(
                "📊 주요 확인 지표 (Key Metrics)", 
                options=METRIC_OPTIONS,
                placeholder="대시보드에서 반드시 확인해야 할 핵심 지표를 선택하세요 (선택)"
            )

        additional_requirements = st.text_area(
            "추가 요구사항 / 참고사항",
            placeholder="예: 모바일 호환 필요, 실시간 갱신, 특정 KPI 강조, 색약 고려 등",
            height=80
        )

    st.markdown("""
    <style>
    div[data-testid="stColumns"]:has(#reset-anchor) button {
        background: transparent !important;
        border: 1px solid #0351d3 !important;
        color: #0351d3 !important;
        border-radius: 8px !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        padding: 10px 28px !important;
    }
    div[data-testid="stColumns"]:has(#reset-anchor) button:hover {
        background: rgba(3,81,211,0.05) !important;
    }

    div[data-testid="stColumns"]:has(#submit-anchor) button {
        background: #0351d3 !important;
        border: none !important;
        color: white !important;
        border-radius: 8px !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        padding: 10px 28px !important;
        box-shadow: 0 4px 12px rgba(3,81,211,0.3) !important;
    }
    div[data-testid="stColumns"]:has(#submit-anchor) button:hover {
        opacity: 0.9 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    col_spacer, col_reset, col_submit = st.columns([8, 1, 1.5])
    with col_reset:
        st.markdown('<span id="reset-anchor"></span>', unsafe_allow_html=True)
        reset_btn = st.button("초기화", key="reset_btn", use_container_width=True)

    with col_submit:
        st.markdown('<span id="submit-anchor"></span>', unsafe_allow_html=True)
        submit_btn = st.button("✦ 추천 대시보드 생성하기", key="submit_btn", use_container_width=True)

    return {
        "dashboard_topic": dashboard_topic,
        "edited_df": edited_df,
        "data_description": data_description,
        "selected_goals": selected_goals,
        "custom_goal": custom_goal, 
        "complexity_val": complexity_val,
        "complexity": complexity,
        "target_audience": target_audience,
        "selected_metrics": selected_metrics,
        "additional_requirements": additional_requirements,
        "reset_btn": reset_btn,
        "submit_btn": submit_btn
    }