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
from assets.styles import apply_custom_colors

COLORS = apply_custom_colors()

def render_results(result_json, dashboard_img):
        init_session_state()

        st.markdown("<hr style='border:none;border-top:1px solid #c4c6cf;margin:32px 0;'/>", unsafe_allow_html=True)
    
        # ── 대시보드 개요 카드 (img2 스타일) ──
        summary       = result_json.get("summary", "")
        confidence    = result_json.get("confidence_score", "—")
        data_src      = result_json.get("data_source", "—")
        update_cycle  = result_json.get("update_cycle", "—")
        user_group    = result_json.get("user_group", "—")
    
        # 개요 카드 (이미지 없이 텍스트만)
        st.markdown(f"""
        <div class="result-overview-card">
            <div style="display:flex;gap:32px;align-items:flex-start;">
                <div style="flex:1;">
                    <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
                        <span class="ai-badge">✦ AI Generated</span>
                        <h2 style="font-size:22px;font-weight:600;color:#002045;margin:0;">대시보드 개요</h2>
                    </div>
                    <p style="font-size:15px;color:#43474e;line-height:1.7;margin:0 0 16px 0;">{summary}</p>
                    <div class="overview-meta-grid">
                        <div>
                            <div class="meta-item-label" style="display:flex;align-items:center;gap:4px;">
                                신뢰도 점수
                                <span class="material-symbols-outlined"
                                    style="font-size:16px;color:#74777f;cursor:help;"
                                    title="AI 스스로가 자신이 제안한 대시보드 구성(차트, 레이아웃, KPI 등)이 비즈니스 의사결정에 얼마나 효과적일지 스스로 평가한 확신(Certainty)의 정도">
                                    info
                                </span>
                            </div>
                            <div class="meta-item-value">{confidence}</div>
                        </div>
                        <div>
                            <div class="meta-item-label">데이터 소스</div>
                            <div class="meta-item-value">{data_src}</div>
                        </div>
                        <div>
                            <div class="meta-item-label">업데이트 주기</div>
                            <div class="meta-item-value">{update_cycle}</div>
                        </div>
                        <div>
                            <div class="meta-item-label">사용자 그룹</div>
                            <div class="meta-item-value">{user_group}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # AI 생성 이미지 → 예상 프리뷰 영역에서 st.image()로 렌더링 (base64 분리)
        if dashboard_img is not None:
            _buf = BytesIO()
            dashboard_img.save(_buf, format="PNG")
            _dashboard_img_bytes = _buf.getvalue()
        else:
            _dashboard_img_bytes = None
    
        # ━━━ [1번 영역] 대시보드 예상 프리뷰 (개요 카드 아래 ~ 추천 뷰 구성 위) ━━━
        preview_html = result_json.get("preview_sections", "")
        st.markdown("""
        <div style="margin:28px 0 8px 0;display:flex;align-items:center;gap:10px;">
            <h2 class="section-title" style="margin:0;">대시보드 예상 프리뷰</h2>
            <span style="background:#fff3e0;color:#e65100;font-size:11px;font-weight:600;
                        padding:3px 8px;border-radius:20px;border:1px solid #ffcc02;">
                AI Mockup
            </span>
        </div>
        <p style="font-size:13px;color:#74777f;margin:0 0 12px 0;">
            추천된 뷰 구성을 종합하여 최종 대시보드의 예상 레이아웃을 미리 보여줍니다.
        </p>
        """, unsafe_allow_html=True)
    
        # AI 생성 이미지가 있으면 프리뷰 영역에 표시
        if _dashboard_img_bytes is not None:

            st.image(
                Image.open(BytesIO(_dashboard_img_bytes)),
                caption="AI Generated Dashboard Preview",
                # use_container_width=True
                width=1250
            )
        elif preview_html:
            # AI가 생성한 HTML 와이어프레임 렌더링
            line_count_p = preview_html.count('<div') * 10 + 90
            st.components.v1.html(f"""
            <style>
                * {{ margin:0; padding:0; box-sizing:border-box; }}
                html, body {{ background:transparent !important; overflow:hidden;
                            font-family:'Inter','Noto Sans KR',sans-serif; }}
            </style>
            {preview_html}
            """, height=max(line_count_p, 280))
        else:
            st.markdown("""
            <div style="background:#f8f9fd;border:1.5px dashed #c4c6cf;border-radius:10px;
                        padding:48px;text-align:center;color:#74777f;">
                <span style="font-size:32px;">🖼️</span>
                <p style="margin:8px 0 0 0;font-size:13px;">이미지 생성 옵션을 활성화하면 실제 대시보드 이미지가 표시됩니다.</p>
            </div>
            """, unsafe_allow_html=True)
    
        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    
        # ── 추천 뷰 구성 (img2 스타일 카드) ──
        views = result_json.get("views", [])
        view_icons = ["trending_up", "confirmation_number", "group", "bar_chart", "pie_chart", "map"]
        icon_colors = ["#356ced", "#4f2e00", "#356ced", "#356ced", "#356ced", "#356ced"]
        icon_bg    = ["rgba(53,108,237,0.12)", "rgba(79,46,0,0.15)", "rgba(53,108,237,0.12)",
                    "rgba(53,108,237,0.12)", "rgba(53,108,237,0.12)", "rgba(53,108,237,0.12)"]
    
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;margin:32px 0 16px 0;">
            <h2 class="section-title">추천 뷰 구성</h2>
            <span style="font-size:12px;color:#43474e;">{len(views)}개의 시각화 컴포넌트 제안됨</span>
        </div>
        """, unsafe_allow_html=True)
    
        if views:
            cols = st.columns(min(len(views), 4))
            for i, view in enumerate(views[:min(len(views), 4)]):
                icon   = view.get("icon", view_icons[i % len(view_icons)])
                i_col  = icon_colors[i % len(icon_colors)]
                i_bg   = icon_bg[i % len(icon_bg)]
                with cols[i]:
                    st.markdown(f"""
                    <div class="view-card">
                        <div class="view-icon-wrap" style="background:{i_bg};">
                            <span class="material-symbols-outlined" style="color:{i_col};">{icon}</span>
                        </div>
                        <h3>{view.get('name','')}</h3>
                        <p>{view.get('purpose','')}</p>
                        <div class="view-card-footer">
                            <span class="chart-type-badge">{view.get('chart_type','')}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
        # ── 레이아웃 구성 + 색상 팔레트 (img2 스타일, 2컬럼) ──
        st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
        col_lay, col_clr = st.columns(2, gap="large")
    
        layout = result_json.get("layout", {})
        color  = result_json.get("color_scheme", {})
    
        # ━━━ [2번 영역] 레이아웃 구성 → AI 생성 wireframe_html ━━━
        with col_lay:
            st.markdown('<h2 class="section-title">레이아웃 구성</h2>', unsafe_allow_html=True)
            wireframe_html = layout[0].get("wireframe_html", "")
            
            # 💡 수정됨: 변수 앞뒤의 줄바꿈을 완전히 제거하여 여백이 짝짝이가 되는 현상 방지
            html_content = (
                f"""
                    <div style="background: #ffffff; border: 1px solid #c4c6cf; border-radius: 12px; padding: 24px; box-sizing: border-box;">
                        {wireframe_html}
                    </div>
                    <p style="font-size:13px;color:#43474e;line-height:1.6;margin-top:12px;">
                        {layout[0].get("description", "")} {layout[0].get("arrangement", "")}
                    </p>
                """
            )
            st.markdown(html_content, unsafe_allow_html=True)
    
        # ━━━ [3번 영역] 색상 팔레트 → AI 생성 색상 코드로 카드 직접 그리기 ━━━
        with col_clr:
            st.markdown('<h2 class="section-title">색상 팔레트 추천</h2>', unsafe_allow_html=True)
            primary_theme  = color[0].get("primary_theme", "Trustworthy Blue")
            colors_list    = color[0].get("colors", ["#0351D3","#002045","#356CED","#1A365D"])
            accent_list    = color[0].get("accent_colors", ["#FFDDBA","#BA1A1A","#C4C6CF","#E3E2E6"])
    
            # 밝기에 따라 텍스트 색상(흰/검)을 결정하는 함수
            def is_dark(hex_color):
                h = hex_color.lstrip("#")
                if len(h) != 6: return True
                r,g,b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
                return (r*0.299 + g*0.587 + b*0.114) < 140
    
            # 색상 박스(Swatch) 생성 함수
            def build_swatches(hex_list):
                html = ""
                for c in hex_list:
                    text_color = "white" if is_dark(c) else "#43474e"
                    html += f'<div style="flex:1; display:flex; align-items:center; justify-content:center; background:{c}; color:{text_color}; font-size:11px; font-weight:600;">{c.upper()}</div>'
                return html
            
            primary_swatches = build_swatches(colors_list)
            accent_swatches = build_swatches(accent_list)
    
            # 주의: Streamlit 버그 방지를 위해 내부 HTML 사이의 '빈 줄'을 모두 제거했습니다.
            st.markdown(f"""
            <div style="background:#ffffff; border:1px solid #c4c6cf; border-radius:12px; padding:24px;">
                <p style="font-size:13px; color:#74777f; margin:0 0 8px 0;">Primary Theme: <strong style="color:#002045;">{primary_theme.split('&', 1)[0].strip() if '&' in primary_theme else ''}</strong></p>
                <div style="display:flex; height:48px; border-radius:8px; overflow:hidden; margin-bottom:20px; border:1px solid #e3e2e6;">
                    {primary_swatches}
                </div>
                <p style="font-size:13px; color:#74777f; margin:0 0 8px 0;">Accent & Semantic Colors: <strong style="color:#002045;">{primary_theme.split('&', 1)[1].strip() if '&' in primary_theme else ''}</strong></p></p>
                <div style="display:flex; height:48px; border-radius:8px; overflow:hidden; margin-bottom:20px; border:1px solid #e3e2e6;">
                    {accent_swatches}
                </div>
                <div style="font-size:13px; color:#43474e; line-height:1.7;">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <div style="font-size:13px;width:6px; height:6px; border-radius:50%; background:#0351d3;"></div>
                        <span>핵심 데이터 시각화에는 <strong> {primary_theme.split('&', 1)[0].strip() if '&' in primary_theme else ''} </strong>를 사용하여 신뢰감을 부여합니다.</span>
                    </div>
                    <div style="display:flex; align-items:center; gap:8px;">
                        <div style="font-size:13px; width:6px; height:6px; border-radius:50%; background:#ffddba;"></div>
                        <span>AI 추천 및 강조 포인트에는 <strong> {primary_theme.split('&', 1)[1].strip() if '&' in primary_theme else ''} </strong>를 사용하여 주목도를 높입니다.</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
        # ━━━ img3 영역: Implementation & Tips ━━━━━━━━━━━━━━━━━━━━━━━
        st.markdown("<hr style='border:none;border-top:1px solid #c4c6cf;margin:40px 0;'/>", unsafe_allow_html=True)
        st.markdown("""
            <div class="page-header" style="margin-bottom:28px;">
                <h1>구현단계 &amp; 팁</h1>
                <p style="font-size:15px; color:#43474e; margin:0;">
                성공적인 대시보드 구축을 위한 단계별 가이드와 전문가의 최적화 팁을 제공합니다.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
        # ── Tableau 구현 단계 (3단 카드) ──
        st.markdown('<h2 class="section-title"><span class="material-symbols-outlined">layers</span>Tableau 구현 단계</h2>', unsafe_allow_html=True)
    
        steps = result_json.get("implementation_steps", [])
        step_icons = ["database", "query_stats", "dashboard_customize"]
        if steps:
            scols = st.columns(min(len(steps), 3))
            for i, step in enumerate(steps[:3]):
                title = step.get("title", f"단계 {i+1}") if isinstance(step, dict) else f"단계 {i+1}"
                desc  = step.get("desc", str(step)) if isinstance(step, dict) else str(step)
                icon  = step.get("icon", step_icons[i % 3]) if isinstance(step, dict) else step_icons[i % 3]
                with scols[i]:
                    st.markdown(f"""
                    <div class="step-card">
                        <div class="step-number-bg">{i+1}</div>
                        <span class="material-symbols-outlined">{icon}</span>
                        <h3>{title}</h3>
                        <p>{desc}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
        st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

        # ── 전문가 팁 (img3 비대칭 카드 레이아웃) ──
        st.markdown('<h2 class="section-title"><span class="material-symbols-outlined">auto_awesome</span>전문가 팁</h2>', unsafe_allow_html=True)

        pro_tips = result_json.get("pro_tips", [])

        perf_tip    = next((t for t in pro_tips if isinstance(t,dict) and t.get("type")=="performance"), None)
        kpi_tip     = next((t for t in pro_tips if isinstance(t,dict) and t.get("type")=="kpi"), None)
        filter_tip  = next((t for t in pro_tips if isinstance(t,dict) and t.get("type")=="filter"), None)
        dynamic_tip = next((t for t in pro_tips if isinstance(t,dict) and t.get("type")=="dynamic"), None)

        if not perf_tip and pro_tips:
            perf_tip = {"title": pro_tips[0] if isinstance(pro_tips[0],str) else pro_tips[0].get("title",""),
                        "content": "" if isinstance(pro_tips[0],str).strip('\n') else pro_tips[0].get("content","").strip('\n'),
                        "label": "PERFORMANCE"}

        # 행 1: 메인 팁(8) + KPI 팁(4)
        row1_l, row1_r = st.columns([2, 1], gap="medium")
        with row1_l:
            if perf_tip:
                st.markdown(f"""
                <div class="tip-main-card">
                    <span class="perf-badge">{perf_tip.get('label','PERFORMANCE')}</span>
                    <h3>{perf_tip.get('title','')}</h3>
                    <p>{perf_tip.get('content','').replace(chr(10), ' ').replace(chr(13), ' ').strip('\n')}</p>
                </div>
                """, unsafe_allow_html=True)

        with row1_r:
            if kpi_tip:
                st.markdown(f"""
                <div class="tip-side-card">
                    <div>
                        <span class="material-symbols-outlined" style="color:#0351d3;font-size:22px;">insights</span>
                        <h3>{kpi_tip.get('title','')}</h3>
                        <p>{kpi_tip.get('content','').replace(chr(10), ' ').replace(chr(13), ' ')}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        # 행 2: 필터 팁(4) + 동적 매개변수 팁(8)
        row2_l, row2_r = st.columns([1, 2], gap="medium")
        with row2_l:
            if filter_tip:
                st.markdown(f"""
                <div class="tip-filter-card">
                    <span class="material-symbols-outlined" style="color:#0351d3;font-size:22px;">filter_alt</span>
                    <h3>{filter_tip.get('title','')}</h3>
                    <p>{filter_tip.get('content','').replace(chr(10), ' ').replace(chr(13), ' ')}</p>
                </div>
                """, unsafe_allow_html=True)

        with row2_r:
            if dynamic_tip:
                st.markdown(f"""
                <div class="tip-amber-card">
                    <div class="icon-wrap">
                        <span class="material-symbols-outlined">bolt</span>
                    </div>
                    <div>
                        <h3>{dynamic_tip.get('title','')}</h3>
                        <p>{dynamic_tip.get('content','').replace(chr(10), ' ').replace(chr(13), ' ')}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

        # ── 원본 JSON 결과 (img3 코드 블록) ──
        json_str = json.dumps(result_json, ensure_ascii=False, indent=2)
        json_for_js = json.dumps(json_str, ensure_ascii=False)  # JS 문자열로 안전하게 이스케이프

        line_count = json_str.count('\n') + 1
        total_height = min(line_count * 20, 500)


        st.components.v1.html(f"""
            <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet"/>
            <style>
                * {{ margin:0; padding:0; box-sizing:border-box; }}
                html, body {{ background:transparent !important; overflow:hidden; font-family:'Inter',sans-serif; }}

                .header {{
                    display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;
                }}
                .section-title {{
                    display:flex; align-items:center; gap:6px;
                    font-size:18px; font-weight:700; color:#002045;
                }}
                .copy-btn {{
                    display:flex; align-items:center; gap:6px;
                    padding:8px 16px; background:#e9e7eb;
                    border:1px solid #c4c6cf; border-radius:8px;
                    font-size:12px; font-weight:600; color:#43474e;
                    cursor:pointer; font-family:Inter,sans-serif;
                    transition:all 0.2s;
                }}
                .copy-btn:hover {{ background:#d8d6da; }}
                .copy-btn.copied {{
                    background:#00311f; color:#4edea3; border-color:#4edea3;
                }}
                /* ── JSON 코드 블록 ── */
                .json-block-wrap {{
                    background: {COLORS['inverse_surface']};
                    border-radius: 12px;
                    overflow: hidden;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
                }}
                .json-block-header {{
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    padding: 10px 20px;
                    background: rgba(0,0,0,0.2);
                    border-bottom: 1px solid rgba(255,255,255,0.05);
                }}
                .json-dots {{ 
                    display: flex; gap: 6px; 
                }}
                .json-dot {{
                    width: 12px; height: 12px;
                    border-radius: 50%;
                }}
                .json-filename {{
                    font-size: 11px;
                    color: rgba(255,255,255,0.4);
                    font-family: monospace;
                    margin-left: 12px;
                }}
                .json-content {{
                    padding:20px; 
                    font-family:'Courier New',monospace;
                    font-size:15px; 
                    line-height:1.6; 
                    color:#c8ccd8;
                    white-space:pre-wrap; 
                    word-break:break-all;
                    max-height:500px; 
                    overflow-y:auto;
                }}
            </style>

            <div class="header">
                <div class="section-title">
                    <span class="material-symbols-outlined" style="color:#43474e;font-size:20px;">code</span>
                    원본 JSON 결과
                </div>
                <button class="copy-btn" id="copyBtn">
                    <span class="material-symbols-outlined" style="font-size:14px;">content_copy</span>
                    Copy JSON
                </button>
            </div>

            <div class="json-block-wrap">
                <div class="json-block-header">
                    <div class="json-dots">
                        <div class="json-dot" style="background:rgba(186,26,26,0.5);"></div>
                        <div class="json-dot" style="background:rgba(242,188,130,0.5);"></div>
                        <div class="json-dot" style="background:rgba(53,108,237,0.5);"></div>
                    </div>
                    <span class="json-filename">recommendation_response_v2.json</span>
                </div>
                <div class="json-content" id="jsonContent">{json_str}</div>
            </div>

            <script>
                const jsonText = {json_for_js};
                const btn = document.getElementById('copyBtn');
                btn.addEventListener('click', function() {{
                    navigator.clipboard.writeText(jsonText)
                    .then(() => {{
                        btn.classList.add('copied');
                        btn.innerHTML = '<span class="material-symbols-outlined" style="font-size:14px;">check</span> Copied!';
                        setTimeout(() => {{
                            btn.classList.remove('copied');
                            btn.innerHTML = '<span class="material-symbols-outlined" style="font-size:14px;">content_copy</span> Copy JSON';
                        }}, 2000);
                    }})
                    .catch(() => alert('복사 실패'));
                }});
            </script>
            """, height=total_height)

            # ── 다운로드 버튼 ──
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        dl_col1, dl_col2, dl_col3 = st.columns(3)

        with dl_col1:
            st.download_button(
                "⬇️ JSON 다운로드",
                data=json.dumps(result_json, ensure_ascii=False, indent=2),
                file_name=f"dashboard_recommendation_{datetime.now().strftime('%Y-%m-%d %H%M')}.json",
                mime="application/json",
                use_container_width=True
            )

        with dl_col2:
            if dashboard_img is not None:
                buf = BytesIO()
                dashboard_img.save(buf, format="PNG")
                st.download_button(
                    "⬇️ 대시보드 이미지 다운로드",
                    data=buf.getvalue(),
                    file_name=f"dashboard_sample_{datetime.now().strftime('%Y-%m-%d %H%M')}.png",
                    mime="image/png",
                    use_container_width=True
                )
        
        with dl_col3:
            try:
                from utils.pdf_generator import generate_pdf_report
                pdf_bytes = generate_pdf_report(result_json, dashboard_img)
                st.download_button(
                    "⬇️ PDF 보고서 다운로드",
                    data=pdf_bytes,
                    file_name=f"dashboard_report_{datetime.now().strftime('%Y-%m-%d %H%M')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.warning("⚠️ PDF 보고서 생성 옵션 활성화를 위해서는 'fpdf2' 라이브러리가 필요합니다.")