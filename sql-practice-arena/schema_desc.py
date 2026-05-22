# schema_desc.py

SCHEMA_DESCRIPTIONS = {
    "ga_sessions": {
        "session_id": "세션 고유 ID",
        "user_id": "사용자 고유 ID",
        "session_date": "세션 발생 날짜",
        "session_datetime": "세션 발생 일시",
        "browser": "사용 브라우저 (Chrome 등)",
        "device_category": "사용 기기 종류 (desktop, mobile 등)",
        "operating_system": "운영체제 (Windows, iOS 등)",
        "source": "유입 출처 (google, facebook 등)",
        "medium": "유입 매체 (organic, cpc 등)",
        "pageviews": "페이지 뷰 수"
    },
    "ga_events": {
        "event_id": "이벤트 고유 ID",
        "session_id": "해당 이벤트가 발생한 세션 ID",
        "event_name": "이벤트 종류 (page_view, purchase 등)",
        "event_timestamp": "이벤트 발생 일시"
    },
    "transactions": {
        "transaction_id": "결제(주문) 고유 ID",
        "session_id": "결제가 발생한 세션 ID",
        "user_id": "결제한 사용자 ID",
        "transaction_date": "결제 일자",
        "revenue": "총 결제 금액 (달러)",
        "product_name": "구매 상품명",
        "quantity": "구매 수량"
    },
    "customers": {
        "customer_id": "고객 고유 식별자",
        "customer_name": "고객 이름",
        "grade": "회원 등급 (VIP, Gold 등)",
        "join_date": "회원 가입 일자",
        "credit_score": "신용 점수 (금융 전용)"
    },
    "products": {
        "product_id": "상품 고유 식별자",
        "product_name": "상품명",
        "price": "상품 단가 (원)",
        "category": "상품 카테고리 분류"
    },
    "orders": {
        "order_id": "주문 고유 번호",
        "customer_id": "주문한 고객 ID",
        "order_date": "주문 일자"
    },
    "order_items": {
        "item_id": "주문 상세 내역 고유 번호",
        "order_id": "포함된 주문 번호",
        "product_id": "주문한 상품 ID",
        "quantity": "주문 수량",
        "price": "주문 당시 적용 단가"
    },
    "accounts": {
        "account_id": "계좌 고유 번호",
        "customer_id": "계좌 소유주 ID",
        "account_type": "계좌 종류 (SAVINGS 등)",
        "balance": "현재 잔액"
    },
    "loans": {
        "loan_id": "대출 고유 번호",
        "customer_id": "대출자 ID",
        "loan_amount": "대출 잔액",
        "interest_rate": "적용 이자율 (%)"
    },
    "users": {
        "user_id": "사용자의 고유 식별자 (예: U_0001)",
        "email": "사용자의 이메일 주소",
        "username": "사용자 이름",
        "country": "사용자의 국가 코드 (예: US, KR)",
        "joined_at": "플랫폼 가입일",
        "plan_type": "현재 이용 중인 요금제 (free, basic, premium)"
    },
    "content": {
        "content_id": "콘텐츠의 고유 식별자 (예: C_0001)",
        "title": "콘텐츠 제목",
        "genre": "콘텐츠 장르 (Action, Comedy, Drama 등)",
        "type": "콘텐츠 종류 (movie, series)",
        "release_year": "콘텐츠 발매/개봉 연도",
        "duration_min": "총 재생 시간(분 단위)",
        "rating": "전문가/플랫폼 내 전체 평균 평점"
    },
    "subscriptions": {
        "sub_id": "구독 결제 이력 고유 식별자",
        "user_id": "구독을 결제한 사용자 아이디 (users 테이블 참조)",
        "plan": "결제한 요금제 등급",
        "start_date": "구독 시작일",
        "end_date": "구독 종료 예정일",
        "status": "현재 구독 상태 (active: 활성, cancelled: 취소, expired: 만료)"
    },
    "watch_history": {
        "watch_id": "시청 기록 고유 식별자",
        "user_id": "시청한 사용자 아이디 (users 테이블 참조)",
        "content_id": "시청한 콘텐츠 아이디 (content 테이블 참조)",
        "watched_at": "시청을 시작한 날짜 및 시간",
        "watched_sec": "실제 시청한 시간(초 단위)",
        "completed": "끝까지 완주했는지 여부 (1: 완주, 0: 중간 이탈)"
    },
    "reviews": {
        "review_id": "리뷰 고유 식별자",
        "user_id": "리뷰를 작성한 사용자 아이디",
        "content_id": "리뷰 대상 콘텐츠 아이디",
        "score": "사용자가 부여한 평점 (1~5점)",
        "comment": "리뷰 내용 (텍스트)",
        "created_at": "리뷰 작성 일시"
    }
}
