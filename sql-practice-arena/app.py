import streamlit as st
import pandas as pd
from database import execute_query, get_schema, get_connection
from mock_data import generate_ga_data, generate_retail_data, generate_finance_data, generate_streaming_data
from problems import THEME_PROBLEMS
from schema_desc import SCHEMA_DESCRIPTIONS
import user_db
import os
import random
import sqlglot
import datetime

# --- Page Configuration ---
st.set_page_config(page_title="SQL Practice", page_icon="💾", layout="wide")

# --- Initialize Application ---
def init_db(theme):
    if theme == "구글 애널리틱스 (이커머스)":
        generate_ga_data()
    elif theme == "일반 쇼핑몰 (이커머스)":
        generate_retail_data()
    elif theme == "금융/은행 (Finance)":
        generate_finance_data()
    elif theme == "스트리밍 / 콘텐츠 플랫폼":
        generate_streaming_data()

if 'current_theme' not in st.session_state:
    st.session_state.current_theme = "구글 애널리틱스 (이커머스)"
    init_db(st.session_state.current_theme)

DEFAULT_QUERY_TEMPLATE = "SELECT \n    \nFROM \n    \nWHERE \n    "

if 'query_input' not in st.session_state:
    st.session_state.query_input = DEFAULT_QUERY_TEMPLATE

if 'current_problem' not in st.session_state:
    st.session_state.current_problem = None

if 'seen_problems' not in st.session_state:
    st.session_state.seen_problems = []

# --- Callbacks ---
def clear_query_callback():
    st.session_state.query_input = DEFAULT_QUERY_TEMPLATE

def load_daily_problem_callback(dp):
    st.session_state.current_theme = dp['theme']
    st.session_state.current_problem = dp
    st.session_state.query_input = DEFAULT_QUERY_TEMPLATE
    init_db(dp['theme'])

def load_history_query_callback(theme, query):
    st.session_state.current_theme = theme
    st.session_state.query_input = query
    init_db(theme)

def delete_favorite_callback(fav_id):
    user_db.remove_favorite(fav_id)

# --- Utility Functions ---
def get_table_data(table_name, limit=5):
    """Fetch sample data for a given table."""
    return execute_query(f"SELECT * FROM {table_name} LIMIT {limit};")

def handle_file_upload(uploaded_file):
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload CSV or Excel.")
            return False
            
        df.columns = [c.strip().replace(' ', '_').lower() for c in df.columns]
        table_name = os.path.splitext(uploaded_file.name)[0].replace(' ', '_').lower()
        
        conn = get_connection()
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()
        
        st.success(f"Successfully uploaded data as new table: `{table_name}`")
        return True
    except Exception as e:
        st.error(f"Error processing file: {e}")
        return False


# --- UI Layout ---
st.title("💾 SQL Practice Arena")
st.markdown("다양한 테마의 데이터셋으로 SQL을 연습하고, 나만의 쿼리를 저장해 보세요!")

# Split into Sidebar and Main content
sidebar, main = st.columns([1, 3])

# -- Sidebar: Schema Viewer and File Uploader --
with sidebar:
    st.header("🎨 데이터셋 테마")
    theme_options = list(THEME_PROBLEMS.keys())
    selected_theme = st.selectbox("연습할 주제를 선택하세요:", theme_options, index=theme_options.index(st.session_state.current_theme))
    
    if selected_theme != st.session_state.current_theme:
        st.session_state.current_theme = selected_theme
        st.session_state.current_problem = None
        st.session_state.query_input = DEFAULT_QUERY_TEMPLATE
        with st.spinner("데이터셋 생성 중..."):
            init_db(selected_theme)
        st.rerun()

    st.markdown("---")
    st.header("🗂️ Database Schema")
    
    schema = get_schema()
    if not schema:
        st.warning("No tables found in the database.")
    
    for table_name, columns in schema.items():
        with st.expander(f"📋 {table_name}"):
            st.markdown("**Columns:**")
            for col in columns:
                desc = SCHEMA_DESCRIPTIONS.get(table_name, {}).get(col, "")
                if desc:
                    st.markdown(f"- `{col}`: {desc}")
                else:
                    st.markdown(f"- `{col}`")
            
            if st.button("Preview Data", key=f"preview_{table_name}"):
                st.session_state.query_input = f"SELECT * FROM {table_name} LIMIT 10;"

    st.markdown("---")
    st.header("📤 Upload Custom Data")
    uploaded_file = st.file_uploader("Upload CSV or Excel file", type=['csv', 'xlsx', 'xls'])
    if uploaded_file is not None:
        if st.button("Upload to Database"):
            if handle_file_upload(uploaded_file):
                st.rerun()

# -- Main: SQL Editor and Results --
with main:
    tab_practice, tab_daily, tab_history, tab_favorites = st.tabs(["💻 실전 연습", "📅 오늘의 문제", "📜 나의 히스토리", "⭐️ 즐겨찾기"])
    
    with tab_practice:
        st.header("🎯 실전 연습 문제")
        
        col_dialect, col_diff = st.columns(2)
        
        with col_dialect:
            selected_dialect = st.selectbox(
                "사용할 SQL 문법(Dialect)을 선택하세요:",
                options=["sqlite", "mysql", "postgres", "oracle", "bigquery", "tsql"],
                index=0,
                help="선택한 DB의 문법으로 작성하시면, 내부적으로 변환하여 실행합니다. 정답 쿼리도 해당 문법으로 표시됩니다."
            )
        with col_diff:
            selected_difficulty = st.selectbox("문제 난이도 선택", ["모든 난이도", "초급", "중급", "고급"])
            
        st.write("")
        if st.button("🔄 랜덤 문제 뽑기"):
            theme_problems = THEME_PROBLEMS[st.session_state.current_theme]
            if selected_difficulty == "모든 난이도":
                pool = theme_problems
            else:
                pool = [p for p in theme_problems if p.get('difficulty') == selected_difficulty]
                
            unseen_pool = [p for p in pool if p['title'] not in st.session_state.seen_problems]
            
            if not unseen_pool and pool:
                st.toast("✅ 해당 난이도의 모든 문제를 풀었습니다! 중복 방지 목록을 초기화합니다.")
                # Reset seen problems only for the current pool's titles
                pool_titles = [p['title'] for p in pool]
                st.session_state.seen_problems = [t for t in st.session_state.seen_problems if t not in pool_titles]
                unseen_pool = pool
                
            if unseen_pool:
                chosen = random.choice(unseen_pool)
                st.session_state.current_problem = chosen
                st.session_state.seen_problems.append(chosen['title'])
                st.session_state.query_input = DEFAULT_QUERY_TEMPLATE
            else:
                st.warning("해당 조건의 문제가 없습니다.")
            
        if st.session_state.current_problem:
            diff_label = st.session_state.current_problem.get('difficulty', '일반')
            st.info(f"**[{diff_label}] {st.session_state.current_problem['title']}**\n\n{st.session_state.current_problem['question']}")
            
            with st.expander("💡 힌트 보기"):
                st.write(st.session_state.current_problem.get('hint', '이 문제에는 힌트가 제공되지 않습니다.'))
                
            with st.expander("✅ 정답 쿼리 보기"):
                answer_query = st.session_state.current_problem['answer']
                if selected_dialect != "sqlite":
                    try:
                        answer_query = sqlglot.transpile(answer_query, read="sqlite", write=selected_dialect)[0]
                    except Exception:
                        pass
                st.code(answer_query, language="sql")
                
        st.markdown("---")
        st.header("✍️ SQL Editor")
            
        # text_area의 key를 지정하고 세션 상태와 연동
        query = st.text_area(
            "Type your SQL query here:",
            key="query_input",
            height=150,
            help="선택한 Dialect 문법에 맞게 작성하세요."
        )
        
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            run_button = st.button("▶️ Run Query", type="primary")
        with col2:
            st.button("🧹 Clear", on_click=clear_query_callback)
        with col3:
            if st.button("⭐️ 현재 쿼리 즐겨찾기 저장"):
                if query.strip() and query.strip() != DEFAULT_QUERY_TEMPLATE.strip():
                    p_title = st.session_state.current_problem['title'] if st.session_state.current_problem else "Custom Query"
                    user_db.add_favorite(st.session_state.current_theme, p_title, query)
                    st.success("즐겨찾기에 성공적으로 저장되었습니다!")
                else:
                    st.warning("저장할 쿼리가 없습니다.")
                
        st.markdown("---")
        st.header("📊 Results")
        
        if run_button:
            if query.strip() == "" or query.strip() == DEFAULT_QUERY_TEMPLATE.strip():
                st.warning("Please enter a SQL query.")
            else:
                with st.spinner("Executing query..."):
                    final_query = query
                    translation_error = False
                    
                    if selected_dialect != "sqlite":
                        try:
                            final_query = sqlglot.transpile(query, read=selected_dialect, write="sqlite")[0]
                            with st.expander("🔄 내부적으로 실행된 변환된 쿼리 보기"):
                                st.code(final_query, language="sql")
                        except Exception as e:
                            st.error(f"SQL 문법 번역 에러: {e}\n\n지원하지 않는 문법이거나 오타일 수 있습니다.")
                            translation_error = True
                            
                    if not translation_error:
                        result = execute_query(final_query)
                        status_str = "Error"
                    
                        if isinstance(result, str):
                            st.error(f"SQL Error: {result}")
                            status_str = "Error"
                        elif isinstance(result, pd.DataFrame):
                            status_str = "Executed"
                            st.success(f"Query returned {len(result)} rows.")
                            
                            # Check if answer is correct
                            if st.session_state.current_problem:
                                ans_result = execute_query(st.session_state.current_problem['answer'])
                                if isinstance(ans_result, pd.DataFrame):
                                    try:
                                        res_df = result.copy()
                                        ans_df = ans_result.copy()
                                        
                                        if len(res_df.columns) != len(ans_df.columns):
                                            raise AssertionError("컬럼 수가 다릅니다.")
                                        
                                        res_df.columns = ans_df.columns
                                        res_df = res_df.sort_values(by=res_df.columns.tolist()).reset_index(drop=True)
                                        ans_df = ans_df.sort_values(by=ans_df.columns.tolist()).reset_index(drop=True)
        
                                        pd.testing.assert_frame_equal(res_df, ans_df, check_dtype=False, check_exact=False)
                                        st.balloons()
                                        st.success("🎉 정답입니다! 결과가 완벽하게 일치합니다.")
                                        status_str = "Correct"
                                    except AssertionError as e:
                                        st.error(f"❌ 결과 데이터가 정답과 다릅니다. (행 개수, 컬럼 개수, 또는 데이터 값이 다를 수 있습니다.)")
                                        status_str = "Incorrect"
                                        
                            st.dataframe(result, use_container_width=True)
                        else:
                            st.write(result)
                            
                        # Save History
                        p_title = st.session_state.current_problem['title'] if st.session_state.current_problem else "Custom Query"
                        user_db.add_history(st.session_state.current_theme, p_title, query, status_str)

    with tab_daily:
        st.header("📅 오늘의 모의고사 (5문제)")
        today_str = datetime.date.today().isoformat()
        st.markdown(f"**{today_str}** 오늘의 문제 세트입니다. 매일 자정에 새로운 랜덤 5문제가 출제됩니다! (정답 쿼리는 제공되지만 결과 확인은 실전 연습 탭을 이용해주세요.)")
        
        all_problems = []
        for theme_name, p_list in THEME_PROBLEMS.items():
            for p in p_list:
                p_copy = p.copy()
                p_copy['theme'] = theme_name
                all_problems.append(p_copy)
                
        # 고정 시드를 사용하여 하루 동안 같은 문제 유지
        random.seed(today_str)
        daily_problems = random.sample(all_problems, 5)
        random.seed() # reset seed
        
        for idx, dp in enumerate(daily_problems):
            st.markdown(f"### Q{idx+1}. [{dp['theme']}] {dp['title']} ({dp['difficulty']})")
            st.info(dp['question'])
            
            col_d1, col_d2 = st.columns([1, 1])
            with col_d1:
                with st.expander("💡 힌트 보기"):
                    st.write(dp.get('hint', ''))
            with col_d2:
                with st.expander("✅ 정답 쿼리 보기"):
                    st.code(dp['answer'], language="sql")
                    
            if st.button(f"👉 이 문제 메인 에디터에서 풀기", key=f"go_main_{idx}", on_click=load_daily_problem_callback, args=(dp,)):
                st.success("실전 연습 탭으로 이동하여 문제를 풀어보세요! (현재 탭에서 위쪽의 '실전 연습' 탭을 클릭하세요)")
            st.markdown("---")

    with tab_history:
        st.header("📜 나의 쿼리 히스토리")
        st.markdown("최근 실행한 쿼리들의 내역입니다. (최신순)")
        hist_df = user_db.get_history()
        if not hist_df.empty:
            for _, row in hist_df.iterrows():
                with st.expander(f"[{row['timestamp']}] {row['theme']} - {row['question_title']} ({row['status']})"):
                    st.code(row['query'], language="sql")
                    st.button("이 쿼리 다시 불러오기", key=f"hist_{row['id']}", on_click=load_history_query_callback, args=(row['theme'], row['query']))
        else:
            st.info("아직 실행한 쿼리 기록이 없습니다.")

    with tab_favorites:
        st.header("⭐️ 즐겨찾기 한 쿼리")
        st.markdown("저장해둔 중요한 쿼리나 복습할 문제들입니다.")
        fav_df = user_db.get_favorites()
        if not fav_df.empty:
            for _, row in fav_df.iterrows():
                with st.expander(f"[{row['timestamp']}] {row['theme']} - {row['question_title']}"):
                    st.code(row['query'], language="sql")
                    col_load, col_del = st.columns([1, 5])
                    with col_load:
                        st.button("쿼리 불러오기", key=f"fav_load_{row['id']}", on_click=load_history_query_callback, args=(row['theme'], row['query']))
                    with col_del:
                        st.button("삭제", key=f"fav_del_{row['id']}", on_click=delete_favorite_callback, args=(row['id'],))
        else:
            st.info("아직 즐겨찾기에 추가된 쿼리가 없습니다. 실전 연습 탭에서 별(⭐️) 버튼을 눌러보세요!")
