import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
import json
from datetime import datetime
import html
from groq import Groq

def render_tabs(tab1, tab2, tab3, role_input, task_choice, format_choice, tone_choice, examples_data):
    
    # ── Tab 1: 생성된 프롬프트 ────────────────────────────────────────────────────
    with tab1:
        if st.session_state.generated_prompt:
            prompt_text = st.session_state.generated_prompt
            
            with st.container(border=False):
                # 메트릭 카드 HTML 렌더링
                shot_type = "Few-Shot" if any(e.get("input", "").strip() for e in examples_data) else "Zero-Shot"
                col1, col2, col3, col4 = st.columns(4)
                with col1: 
                    st.markdown(f'<div class="metric-card"><div class="metric-value">{len(prompt_text.split())}</div><div class="metric-label">단어 수</div></div>', unsafe_allow_html=True)
                with col2: 
                    st.markdown(f'<div class="metric-card"><div class="metric-value">{len(prompt_text)}</div><div class="metric-label">문자 수</div></div>', unsafe_allow_html=True)
                with col3: 
                    st.markdown(f'<div class="metric-card"><div class="metric-value">{len(prompt_text.splitlines())}</div><div class="metric-label">라인 수</div></div>', unsafe_allow_html=True)
                with col4: 
                    st.markdown(f'<div class="metric-card"><div class="metric-value" style="font-size: 24px">{shot_type}</div><div class="metric-label">프롬프트 타입</div></div>', unsafe_allow_html=True)

                # # 태그 배지 오른쪽에 복사 버튼을 배치
                col_tag, col_copy  = st.columns([9, 1])

                with col_tag:
                    # 태그 배지 렌더링
                    tags_html = f"""
                    <div class="tag-container">
                        <span class="tag-badge"><span style="color:#adc6ff">👤</span> {role_input}</span>
                        <span class="tag-badge"><span style="color:#ffb786">📋</span> {task_choice.split('(')[0].strip()}</span>
                        <span class="tag-badge"><span style="color:#4edea3">🎨</span> {format_choice.split('(')[0].strip()}</span>
                        <span class="tag-badge"><span style="color:#ffb4ab">🗣</span> {tone_choice.split('(')[0].strip()}</span>
                        <span class="tag-badge"><span style="color:#adc6ff">🤖</span> {st.session_state.saved_model}</span>
                    </div>
                    """
                    st.markdown(tags_html, unsafe_allow_html=True)

                with col_copy:
                    import json

                    prompt_for_js = json.dumps(prompt_text, ensure_ascii=False)

                    st.components.v1.html(f"""
                    <style>
                        * {{ 
                            margin: 0; 
                            padding: 0; 
                            box-sizing: border-box; 
                        }}
                        html, body {{ 
                            margin: 0 !important; 
                            padding: 0 !important; 
                            background: transparent !important; 
                            overflow: hidden; 
                        }}
                        button {{
                            background: #32353c;
                            color: #e1e2ec;
                            border: 1px solid #424754;
                            border-radius: 8px;
                            padding: 8px 16px;
                            font-size: 13px;
                            font-weight: 600;
                            cursor: pointer;
                            width: 100%;
                            height: 38px;
                            transition: all 0.2s;
                            font-family: sans-serif;
                            margin-top: 16px;
                        }}
                        button:hover {{ background: #424754; }}
                    </style>

                    <button id="copyBtn">📋 프롬프트 복사</button>

                    <script>
                        const text = {prompt_for_js};
                        document.getElementById('copyBtn').addEventListener('click', function() {{
                            navigator.clipboard.writeText(text)
                            .then(() => {{
                                this.textContent = '✅ 복사 완료!';
                                this.style.background = '#00311f';
                                this.style.color = '#4edea3';
                                this.style.borderColor = '#4edea3';
                                setTimeout(() => {{
                                    this.textContent = '📋 프롬프트 복사';
                                    this.style.background = '#32353c';
                                    this.style.color = '#e1e2ec';
                                    this.style.borderColor = '#424754';
                                }}, 2000);
                            }})
                            .catch(() => alert('복사 실패'));
                        }});
                    </script>
                    """, height=58)
                
    
            # # 기존 프롬프트 박스 (그대로 유지)
            st.markdown('<div class="prompt-box-marker"></div>', unsafe_allow_html=True)
            st.markdown(prompt_text, unsafe_allow_html=True)          


            # 다운로드 버튼 영역
            col_a, col_b = st.columns(2)
            with col_a:
                st.download_button("💾 .txt 저장", data=prompt_text, file_name=f"prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", mime="text/plain", use_container_width=True)
            with col_b:
                json_data = json.dumps({
                    "timestamp": datetime.now().isoformat(), "role": role_input, "task": task_choice, "prompt": prompt_text
                }, ensure_ascii=False, indent=2)
                st.download_button("📦 .json 저장", data=json_data, file_name=f"prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", mime="application/json", use_container_width=True)

            # 성공 배너 렌더링
            st.markdown("""
            <div class="success-banner">
                <svg style="width: 1rem; height: 1rem;" fill="currentColor" viewBox="0 0 20 20">
                    <path clip-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" fill-rule="evenodd"></path>
                </svg>
                <span>프롬프트가 생성되었습니다. 위 텍스트를 ChatGPT, Claude, Gemini 등 AI에 바로 복사 붙여넣기 하세요.</span>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown("""
            <div style="text-align:center; padding: 100px 20px;">
                <div style="font-size:64px; margin-bottom:16px;">✨</div>
                <h3 style="font-size:18px; font-weight:700; color:#e1e2ec; margin-bottom:8px;">저장된 기록이 없습니다</h3>
                <p style="font-size:14px; color:#c2c6d6; line-height:1.6;">
                    왼쪽 사이드바에서 조건을 입력하고<br>
                    ✨ 프롬프트 생성 버튼을 눌러주세요.
                </p>
            </div>
            """, unsafe_allow_html=True)

    # ── Tab 2: Groq 응답 ──────────────────────────────────────────────────────────
    with tab2:
        if st.session_state.groq_response:
            st.markdown(f"**모델:** `{st.session_state.saved_model}`")
            st.markdown("---")
            # 폰트 색상을 은은한 오프화이트(#E1E2EC)로 변경하고 줄 간격(line-height)을 늘려 가독성 확보
            st.markdown(f'<div style="color:#E1E2EC; line-height:1.7; font-size:15px;">{st.session_state.groq_response}</div>', 
                        unsafe_allow_html=True)
            st.markdown("---")

            col_a, col_b = st.columns(2)
            with col_a:
                st.download_button(
                    "💾 응답 저장 (.txt)",
                    data=st.session_state.groq_response,
                    file_name=f"response_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            with col_b:
                combined = f"=== 프롬프트 ===\n{st.session_state.generated_prompt}\n\n=== 응답 ===\n{st.session_state.groq_response}"
                st.download_button(
                    "📦 프롬프트+응답 저장",
                    data=combined,
                    file_name=f"prompt_response_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        else:
            st.markdown("""
            <div style="text-align:center; padding: 80px 20px; color: #4a5568;">
                <div style="font-size:64px; margin-bottom:16px">⚡</div>
                <div style="font-size:20px; font-weight:700; color:#718096; margin-bottom:8px">
                    Groq 응답 없음
                </div>
                <div style="font-size:14px; color:#4a5568;">
                    사이드바에서 <strong style="color:#63b3ed">⚡ Groq으로 바로 실행</strong> 버튼을 누르면<br>
                    생성된 프롬프트를 Groq API로 즉시 실행합니다
                </div>
            </div>
            """, unsafe_allow_html=True)


    # ── Tab 3: 히스토리 ───────────────────────────────────────────────────────────
    with tab3:
        # 1. 히스토리 탭 전용 CSS + 클릭 시 펼쳐지는 애니메이션 로직
        st.markdown("""
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap');
                
                /* ✨ 검색창에 입력하는 텍스트 색상을 완전 흰색으로 변경 */
                .stTextInput input {
                    color: #ffffff !important;
                }
                .history-card {
                    display: flex; align-items: center; background: #1d2027;
                    border: 1px solid #424754; border-radius: 10px; padding: 16px 20px;
                    transition: background 0.2s; cursor: pointer; margin-bottom: 0;
                }
                .history-card:hover { background: #272a31; }
                .history-time { 
                    font-family: monospace; 
                    font-size: 15px; 
                    width: 80px; flex-shrink: 0; 
                }
                .history-content {
                    flex-grow: 1; display: flex; align-items: center; gap: 12px;
                    color: #e1e2ec; 
                    font-size: 17px; 
                    font-weight: 500;
                }
                .history-tags { display: flex; gap: 8px; flex-shrink: 0; }
                /* 3) 오른쪽 모델명 및 작업 태그 배지 크기 */
                .h-tag {
                    background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
                    border-radius: 6px; padding: 4px 10px; 
                    font-size: 12px; 
                    font-weight: 600;
                }
                .material-symbols-outlined { font-family: 'Material Symbols Outlined' !important; }
                
                /* ✨ HTML5 details/summary 기능 (클릭 시 열림) CSS 추가 ✨ */
                details.history-details { margin-bottom: 12px; }
                details.history-details summary { list-style: none; outline: none; }
                details.history-details summary::-webkit-details-marker { display: none; }
                
                /* 카드가 열렸을 때 아래쪽 둥근 모서리 제거 */
                details[open] .history-card { border-radius: 10px 10px 0 0; border-bottom: none; }
                
                /* 펼쳐진 내용 영역 스타일 */
                .history-expanded-content {
                    background: #131c2e; border: 1px solid #424754; border-top: 1px dashed #424754;
                    border-radius: 0 0 10px 10px; padding: 20px; color: #e1e2ec; font-size: 15px;
                }
                .history-expanded-content pre {
                    background: #0d121f !important; border-radius: 6px; padding: 16px;
                    white-space: pre-wrap; font-family: inherit; margin-top: 8px; border: 1px solid #2a303f;
                }
            </style>
        """, unsafe_allow_html=True)

        if st.session_state.history:
            # 2. 상단 타이틀 영역
            st.markdown(f"""
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                    <span class="material-symbols-outlined" style="font-size:28px; color:#adc6ff;">history</span>
                    <h1 style="margin:0; font-size:24px; color:#e1e2ec; font-weight:700;">Prompt History</h1>
                </div>
                <p style="color:#8c909f; font-size:13px; margin-bottom:16px;">총 {len(st.session_state.history)}개의 프롬프트 생성 기록이 있습니다.</p>
            """, unsafe_allow_html=True)

            # 3. ✨ 검색 바 (진짜 Streamlit 위젯 사용) ✨
            search_query = st.text_input("검색", placeholder="🔍 역할, 작업 유형, 또는 프롬프트 내용을 검색하세요...", label_visibility="collapsed")
            st.markdown("<br>", unsafe_allow_html=True)
            
            # 검색 필터링 로직
            history_list = list(reversed(st.session_state.history))
            if search_query:
                history_list = [
                    item for item in history_list 
                    if search_query.lower() in item['role'].lower() 
                    or search_query.lower() in item['task'].lower()
                    or search_query.lower() in item.get('prompt', '').lower()
                ]

            if not history_list:
                st.error("검색 조건과 일치하는 기록이 없습니다.")
            
            # 4. ✨ HTML5 <details>를 활용한 클릭 가능 리스트 렌더링 ✨
            for i, item in enumerate(history_list):
                
                if "요약" in item['task']:
                    border_color = "#4edea3"
                    icon_name = "summarize"
                elif "기획" in item['task'] or "제안" in item['task']:
                    border_color = "#4b6bb8"
                    icon_name = "description"
                else:
                    border_color = "#e7823a"
                    icon_name = "chat_bubble"
                
                is_open = 'open' if i == 0 and not search_query else ''
                
            
                safe_prompt = html.escape(item['prompt']).replace('\n', '<br>')
                safe_response = html.escape(item.get('response', '응답 내용이 없습니다.')).replace('\n', '<br>')
                
                
                card_html = f"""
                <details class="history-details" {is_open}>
                    <summary class="history-card" style="border-left: 4px solid {border_color};">
                        <div class="history-time" style="color:{border_color};">{item['timestamp']}</div>
                        <div class="history-content">
                            <span class="material-symbols-outlined" style="color:{border_color};">{icon_name}</span>
                            {html.escape(item['role'])} · {html.escape(item['task'])}
                        </div>
                        <div class="history-tags">
                            <span class="h-tag" style="color:{border_color};">{html.escape(item['task'])}</span>
                            <span class="h-tag" style="color:#adc6ff;">{html.escape(item['model'])}</span>
                        </div>
                    </summary>
                    <div class="history-expanded-content">
                        <strong style="color:{border_color};">📝 생성된 프롬프트:</strong>
                        <div style="background:#0d121f; border-radius:6px; padding:16px; margin-top:8px; border:1px solid #2a303f; font-family:inherit; white-space:pre-wrap; color:#e1e2ec;">{safe_prompt}</div>
                        <strong style="color:#adc6ff; display:inline-block; margin-top:16px;">🤖 Groq 응답:</strong>
                        <div style="background:#0d121f; border-radius:6px; padding:16px; margin-top:8px; border:1px solid #2a303f; font-family:inherit; white-space:pre-wrap; color:#ffffff;">{safe_response}</div>
                    </div>
                </details>
                """
                st.markdown(card_html, unsafe_allow_html=True)