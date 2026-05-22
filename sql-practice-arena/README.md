# 🚀 SQL Practice Arena (SQL 실전 연습 플랫폼)

**SQL Practice Arena**는 실무에서 마주치는 다양한 비즈니스 상황을 4가지 핵심 도메인(구글 애널리틱스, 이커머스 쇼핑몰, 금융/은행, 스트리밍 플랫폼)으로 분류하고, 현업과 유사한 가상 데이터셋 및 120개의 실전형 쿼리 문제를 제공하는 반응형 SQL 학습 플랫폼입니다.

---

## 💡 기획 의도 (Project Intent)
단순 문법 위주의 SQL 학습에서 벗어나, **"실제 현업 데이터 구조(Schema)를 보며 비즈니스 문제를 해결하는 감각"**을 키우기 위해 기획되었습니다. 
사용자는 복잡한 DB 설치 과정 없이 웹(Streamlit)에서 즉시 쿼리를 작성하고 실행 결과를 확인할 수 있습니다. 또한 `sqlglot` 라이브러리를 통해 자신이 선택한 MySQL, PostgreSQL 등 다양한 방언(Dialect)으로 정답 쿼리를 변환하며 맞춤형으로 학습할 수 있습니다. 매일 랜덤하게 5문제가 출제되는 '오늘의 문제' 기능을 통해 꾸준한 학습 루틴을 형성할 수 있도록 설계했습니다.

## 🧠 도메인 지식 및 바이브 코딩 (Vibe-Coding) 활용
본 프로젝트는 **AI 프로그래밍(Vibe Coding)**을 적극적으로 활용하여 개발되었습니다. 단순한 코드 생성을 넘어, 기획자의 비즈니스 도메인 지식과 데이터 분석 노하우를 AI 프롬프트에 정교하게 녹여내어 프로젝트의 질적 퀄리티를 극대화했습니다.

- **비즈니스 로직 설계**: 구글 애널리틱스 세션 로그, 이커머스 장바구니 전환율, 금융권 이상 징후 탐지, 넷플릭스 형태의 콘텐츠 시청 완주율(Completion Rate) 등 현업에서 실제로 쓰이는 핵심 지표(KPI) 분석 로직을 직접 설계하여 AI에게 명확한 맥락을 부여했습니다.
- **고급 SQL 훈련 세팅**: 단순 조회(`SELECT`)를 넘어, 실무 데이터 추출에서 필수적인 윈도우 함수(`LAG`, `LEAD`, `ROW_NUMBER`)와 CTE(공통 테이블 식)를 능숙하게 다룰 수 있도록 120개의 실전 문제 출제 프롬프트를 세밀하게 제어했습니다.
- **사용자 경험(UX) 고도화**: 상태 관리(Session State)를 통한 UI 꼬임 현상 해결, 2단 분할 레이아웃 최적화, 정답 쿼리 실시간 번역 로직 등 AI와의 지속적인 상호작용 및 피드백 루프를 통해 완성도 높은 서비스를 구축했습니다.

## ⚙️ 아키텍처 구조 (Architecture)
본 프로젝트는 확장성과 가독성을 고려하여 프론트엔드 UI 요소와 백엔드 데이터 처리 로직을 명확히 분리하여 모듈화했습니다.

- **UI / Frontend (`app.py`)**: `Streamlit`을 활용하여 직관적인 2단 레이아웃과 탭(Tab) 구조를 구현했습니다. 버튼 클릭 시 콜백(`on_click`) 함수를 적극 활용하여 Session State의 불필요한 재렌더링과 에러를 방지합니다.
- **데이터베이스 & 모의 데이터 (`database.py`, `mock_data.py`)**: `SQLite3` 인메모리(또는 로컬) DB를 사용하여 빠르고 가벼운 환경을 구축했습니다. Pandas DataFrame을 이용해 4개 도메인의 방대한 가상 데이터를 동적으로 생성하고 주입합니다.
- **문제 은행 & 번역 모듈 (`problems.py`)**: 120개의 문제를 딕셔너리로 체계적으로 관리하며, 유저가 선택한 문법(Dialect)에 맞춰 내부적으로 `sqlglot` 모듈이 정답 쿼리의 방언을 실시간으로 변환하여 제공합니다.

---

## 🛠️ 기술 스택 (Tech Stack)
- **Language**: Python 3.9+
- **Frontend**: Streamlit
- **Database**: SQLite3, MySQL, Oracle, Bigquery, PostgreSQL..
- **Libraries**: Pandas, sqlglot, ..

## 🚀 실행 방법 (How to Run)
```bash
# 1. 필요 패키지 설치
pip install streamlit pandas sqlglot

# 2. 애플리케이션 실행
streamlit run app.py
```

---

Copyright (c) 2026 Hesthers. All rights reserved.
This project is for portfolio purposes only. Unauthorized copying, modification, or commercial use is strictly prohibited. (이 프로젝트는 포트폴리오용입니다. 무단 복사, 수정 및 상업적 이용을 엄격히 금지합니다.)
