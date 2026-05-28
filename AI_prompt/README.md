# AI Prompt Generator ⚡

사용자가 원하는 역할(Role), 작업 유형(Task), 출력 형식(Format) 등의 조건을 입력하면, AI에게 바로 전달할 수 있는 **최적화된 고품질 프롬프트를 자동으로 조립 및 생성해 주는 웹 애플리케이션**입니다. Streamlit과 Groq API를 활용하여 만들어진 프롬프트를 즉시 테스트해 보고, 과거의 프롬프트 기록(History)까지 관리할 수 있습니다.

## 🎯 개발 목적 (Why I Built This)
기존에는 AI에게 원하는 완벽한 답변을 얻기 위해 프롬프트의 내용 구성을 기획하고 텍스트를 다듬는 데 많은 시간과 노력이 투자되어야 했습니다. 본 애플리케이션은 **사용자가 입력한 최소한의 조건을 바탕으로 AI가 시스템 프롬프트 수준의 고품질 텍스트를 즉각적으로 조립해 줌으로써, 프롬프트 엔지니어링에 투자되는 시간을 획기적으로 줄이고 업무 효율성을 극대화하기 위해** 개발되었습니다.

## ✨ 주요 기능

*   **맞춤형 프롬프트 조립**: 역할, 성격, 상세 지시사항, 제약 조건, 출력 톤 앤 매너 등을 세밀하게 설정하여 구조화된 프롬프트를 자동으로 생성합니다.
*   **Zero/Few-Shot 예시 지원**: 사용자가 원하는 입력과 출력 예시를 폼에 입력하면 프롬프트 내에 자동으로 예시 템플릿이 삽입됩니다.
*   **Groq API 실시간 테스트**: 생성된 프롬프트를 복사할 필요 없이, 앱 내에서 바로 Groq API (Llama 등) 모델을 호출하여 AI의 답변 품질을 즉시 테스트할 수 있습니다.
*   **히스토리 관리 및 검색**: 이전에 생성했던 프롬프트와 AI 응답 내역이 자동으로 저장되며, 키워드 검색을 통해 지난 프롬프트 기록을 쉽게 찾아볼 수 있습니다.
*   **다양한 포맷 다운로드**: 생성된 프롬프트와 AI 응답 결과를 `.txt` 또는 `.json` 파일로 손쉽게 저장할 수 있습니다.

## 📁 디렉토리 구조 (Component-based Architecture)

이 프로젝트는 단일 파일로 구성되었던 기존 코드를 유지보수와 확장성을 고려하여 화면 UI, 비즈니스 로직, 데이터 모듈로 명확히 분리한 구조를 채택하고 있습니다.

```text
📦 ai_prompt_generator
 ┣ 📜 app.py                 # 메인 실행 파일 (컨트롤 타워)
 ┣ 📜 README.md              # 프로젝트 설명 문서
 ┣ 📂 core                   # 핵심 로직 & API
 ┃ ┣ 📜 groq_api.py          # Groq API 통신 및 사용 가능한 모델 조회 로직
 ┃ ┗ 📜 prompt_builder.py    # 사용자 입력값을 바탕으로 프롬프트 텍스트를 조립하는 로직
 ┣ 📂 components             # 화면 UI 모듈
 ┃ ┣ 📜 sidebar.py           # API 설정 및 모델 선택 UI
 ┃ ┣ 📜 sidebar_components.py # 역할, 작업, 형식 등 상세 조건 입력 폼 UI
 ┃ ┗ 📜 main_view.py         # 3개의 탭 (프롬프트 결과, AI 응답, 히스토리) 렌더링
 ┣ 📂 utils                  # 유틸리티 및 데이터
 ┃ ┣ 📜 state.py             # Streamlit session_state (상태 관리) 초기화
 ┃ ┗ 📜 constants.py         # 드롭다운 옵션 및 모델 리스트 등 정적 데이터
 ┗ 📂 assets                 # 정적 리소스
   ┗ 📜 styles.py            # 전역 CSS 스타일 및 컬러 토큰
```

## 🚀 시작하기 (Getting Started)

### 1. 필수 조건 (Prerequisites)
*   Python 3.8 이상
*   Groq API Key (무료 발급 가능)

### 2. 설치 (Installation)

1. 저장소를 클론(Clone)하거나 다운로드합니다.
2. 터미널을 열고 필요한 Python 패키지를 설치합니다.
```bash
pip install streamlit groq python-dotenv
```

### 3. 환경 변수 설정 (Environment Setup)

프로젝트 루트 디렉토리에 `GROQ_API_KEY.env` 파일을 생성하고 아래와 같이 입력합니다. (앱 실행 후 화면 왼쪽의 사이드바 메뉴를 통해서도 직접 키를 입력할 수 있습니다.)

```env
GROQ_API_KEY=gsk_... (여기에 실제 발급받은 API 키를 입력하세요)
```

### 4. 앱 실행 (Run Application)

아래 명령어를 터미널에 입력하여 Streamlit 앱을 실행합니다.

```bash
streamlit run app.py
```

## 💡 기대 효과 및 인사이트 (Expected Insights)
사용자는 이 애플리케이션을 통해 단순한 텍스트 생성을 넘어 AI와 더 잘 소통하는 방법을 얻을 수 있습니다:
* **신속한 프롬프트 작성**: 역할, 톤, 출력 형식 등의 체계적인 입력 폼을 통해 몇 번의 클릭만으로 전문적인 프롬프트를 완성하여 기획 시간을 단축합니다.
* **엔지니어링 인사이트 학습**: 앱이 자동으로 조립한 프롬프트의 구조(마크다운 방식, Few-shot 예시 배치 등)를 보며 좋은 프롬프트 작성법에 대한 인사이트를 얻을 수 있습니다.
* **빠른 가설 검증**: 생성된 프롬프트를 Groq API로 즉시 테스트해 보며 어떤 조건이 답변의 퀄리티를 높이는지 실시간으로 비교하고 검증할 수 있습니다.

## 🤝 크레딧 (Acknowledgments)
*   **Main Logic & Code Generation**: 이 프로젝트의 핵심 로직과 초기 코드는 **Claude**를 활용하여 생성되었습니다.
*   **Code Refactoring & Architecture**: 생성된 코드를 바탕으로 직접 컴포넌트 기반(Component-based) 아키텍처로 리팩토링 및 고도화 작업을 진행했습니다.
*   **UI/UX Design & Layout**: 전체적인 사용자 인터페이스(UI)와 화면 레이아웃 구성은 **Stitch**의 도움을 받아 설계되었습니다.

## 📝 라이선스
Copyright (c) 2026 Hesthers. All rights reserved. This project is for portfolio purposes only. Unauthorized copying, modification, or commercial use is strictly prohibited. (이 프로젝트는 포트폴리오용입니다. 무단 복사, 수정 및 상업적 이용을 엄격히 금지합니다.)
