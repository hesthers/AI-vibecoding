# Tableau AI Dashboard Recommender 📊

사용자의 비즈니스 목표와 데이터 특성을 입력받아, 최적의 **Tableau 대시보드 구성과 레이아웃을 AI가 추천**해주는 지능형 웹 애플리케이션입니다. Streamlit과 OpenAI API(GPT, gpt-image-1.5)를 활용하여 텍스트 기반의 구조 추천뿐만 아니라 AI가 생성한 가상의 대시보드 프리뷰(Mockup) 이미지까지 원스톱으로 제공합니다.

## 🎯 개발 목적 (Why I Built This)
기존에는 대시보드를 기획할 때 데이터 구조를 고민하고 화면을 구성하는 데 많은 시간과 노력이 투자되어야 했습니다. 본 애플리케이션은 **AI가 최적의 대시보드 구조와 시각화 형태를 즉각적으로 추천해 줌으로써 기획 단계의 업무 효율성을 극대화하고 투자되는 시간을 획기적으로 줄이기 위해** 개발되었습니다.

## ✨ 주요 기능

*   **맞춤형 대시보드 구조 추천**: 대시보드 주제, 데이터 설명, 대상 타겟, 분석 목표 등을 입력하면 AI가 최적의 뷰(차트) 구성과 배치를 제안합니다.
*   **AI 대시보드 프리뷰 생성**: 제안된 대시보드 구조를 바탕으로 gpt-image-1.5 (또는 호환 이미지 모델)를 이용해 시각적인 대시보드 Mockup 이미지를 실시간으로 생성합니다.
*   **전문가 팁 및 컬러 팔레트 제안**: 퍼포먼스 최적화, KPI 설정 팁, 그리고 대시보드의 가독성을 높일 수 있는 컬러 팔레트 테마를 함께 추천합니다.
*   **다양한 포맷의 리포트 다운로드**:
    *   `JSON`: AI 추천 원본 데이터 구조 다운로드
    *   `PNG`: AI가 생성한 대시보드 시안 이미지 다운로드
    *   `PDF`: 추천 내용 전체(개요, 레이아웃, 이미지, 팁)를 포함한 자동화된 PDF 보고서 다운로드 (`fpdf2` 활용)

## 📁 디렉토리 구조 (Component-based Architecture)

이 프로젝트는 유지보수와 확장성을 고려하여 화면 UI, 비즈니스 로직, API 통신 모듈을 명확히 분리한 구조를 채택하고 있습니다.

```text
📦 tableau_recommendation
 ┣ 📜 app.py                 # 메인 실행 파일 (컨트롤 타워)
 ┣ 📜 README.md              # 프로젝트 설명 문서
 ┣ 📂 core                   # 핵심 로직 & API
 ┃ ┣ 📜 openai_api.py        # OpenAI API 통신 (텍스트/이미지 생성)
 ┃ ┗ 📜 prompt_builder.py    # AI에 전달할 프롬프트 조립 로직
 ┣ 📂 components             # 화면 UI 모듈
 ┃ ┣ 📜 sidebar.py           # 사이드바 (API 설정 및 모델 선택)
 ┃ ┣ 📜 input_form.py        # 메인 입력 폼 (주제, 데이터, 목표 등)
 ┃ ┗ 📜 result_view.py       # 결과 화면 렌더링 (리포트, 이미지, 다운로드 버튼)
 ┣ 📂 utils                  # 유틸리티 및 데이터
 ┃ ┣ 📜 state.py             # Streamlit session_state 초기화 및 관리
 ┃ ┗ 📜 pdf_generator.py     # 결과물 PDF 보고서 생성 모듈
 ┗ 📂 assets                 # 정적 리소스
   ┣ 📜 styles.py            # 전역 CSS 스타일 및 컬러 토큰
   ┗ 📂 fonts                # PDF 생성을 위한 커스텀 폰트 (NanumGothic 등)
```

## 🚀 시작하기 (Getting Started)

### 1. 필수 조건 (Prerequisites)
*   Python 3.8 이상
*   OpenAI API Key (또는 호환되는 API Key)

### 2. 설치 (Installation)

1. 저장소를 클론(Clone)하거나 다운로드합니다.
2. 필요한 Python 패키지를 설치합니다.
```bash
pip install streamlit openai pandas pillow fpdf2 python-dotenv requests
```
*(참고: PDF 보고서 다운로드 기능을 정상적으로 사용하려면 `fpdf2` 라이브러리가 반드시 필요합니다.)*

### 3. 환경 변수 설정 (Environment Setup)

보안을 위해 API 키는 별도의 환경 변수 파일에 보관하는 것을 권장합니다.
프로젝트 루트 디렉토리에 `GPT_API_KEY.env` 파일을 생성하고 아래와 같이 입력합니다. (앱 내 사이드바 UI를 통해서도 직접 입력 가능합니다.)

```env
GROQ_API_KEY=sk-... (여기에 실제 발급받은 API 키를 입력하세요)
```

### 4. 앱 실행 (Run Application)

아래 명령어를 터미널에 입력하여 Streamlit 앱을 실행합니다.

```bash
streamlit run app.py
```

## 🎨 UI & 디자인 가이드
*   **커스텀 테마**: `assets/styles.py`에서 전체 앱의 색상(Primary, Secondary, Background 등)과 마크다운 CSS 규칙을 전역으로 관리하고 있습니다.
*   **컴포넌트 분리**: 화면 레이아웃과 디자인은 순수하게 `components/` 디렉토리 하위 파일들에서 관리되므로, 비즈니스 로직에 영향을 주지 않고 자유롭게 UI를 수정할 수 있습니다.

## 💡 기대 효과 및 인사이트 (Expected Insights)
사용자는 이 애플리케이션을 통해 단순한 데이터 시각화를 넘어 비즈니스 의사결정에 직결되는 실질적인 인사이트를 얻을 수 있습니다:
* **신속한 기획**: 비즈니스 목표에 딱 맞는 차트 종류와 레이아웃 구성을 빠르게 파악하여 기획 시간을 단축합니다.
* **전문가 수준의 설계**: AI가 제안하는 전문가 팁과 KPI 설정 가이드를 통해 완성도 높은 대시보드를 설계할 수 있습니다.
* **시각적 아이디어 도출**: 생성된 Mockup 이미지를 통해 최종 결과물의 모습을 미리 확인하고 디자인 아이디어를 얻을 수 있습니다.

## 🤝 크레딧 (Acknowledgments)
*   **Main Logic & Code Generation**: 이 프로젝트의 핵심 로직과 초기 코드는 **Claude**를 활용하여 생성되었습니다.
*   **Code Refactoring & Architecture**: 생성된 코드를 바탕으로 직접 컴포넌트 기반(Component-based) 아키텍처로 리팩토링 및 고도화 작업을 진행했습니다.
*   **UI/UX Design & Layout**: 전체적인 사용자 인터페이스(UI)와 화면 레이아웃 구성은 **Stitch**의 도움을 받아 설계되었습니다.

## 📝 라이선스
Copyright (c) 2026 Hesthers. All rights reserved. This project is for portfolio purposes only. Unauthorized copying, modification, or commercial use is strictly prohibited. (이 프로젝트는 포트폴리오용입니다. 무단 복사, 수정 및 상업적 이용을 엄격히 금지합니다.)
