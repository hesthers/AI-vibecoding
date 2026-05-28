TASK_OPTIONS = {
    "요약 (Summary)": "주어진 내용을 핵심만 간추려 요약",
    "초안 작성 (Draft Writing)": "주제에 맞는 글의 초안을 작성",
    "코드 리뷰 (Code Review)": "코드의 품질, 성능, 가독성을 검토",
    "번역 (Translation)": "텍스트를 다른 언어로 자연스럽게 번역",
    "브레인스토밍 (Brainstorming)": "아이디어를 자유롭게 발산하고 제안",
    "기획/제안 (Planning/Suggestion)": "비즈니스 문제를 정의 및 전략적 로직과 구체적인 실행 방안을 설계",
    "편집 및 개선 (Editing)": "기존 글을 더 명확하고 완성도 있게 개선",
    "분석 (Analysis)": "데이터, 텍스트, 상황을 체계적으로 분석",
    "설명 (Explanation)": "복잡한 개념이나 내용을 이해하기 쉽게 설명",
}

TONE_OPTIONS = {
    "전문적 (Professional)": "격식 있고 전문성 있는 톤",
    "친절한 (Friendly)": "따뜻하고 친근한 톤",
    "중립적 (Neutral)": "감정 없이 객관적인 톤",
    "비판적 (Critical)": "날카롭고 비판적인 시각",
    "유머러스한 (Humorous)": "가볍고 재치 있는 톤",
    "학문적 (Academic)": "논문처럼 엄밀하고 체계적인 톤",
    "일상적 (Casual)": "편안하고 구어체적인 톤",
    "격식적 (Formal)": "공식 문서 수준의 엄격한 톤",
    "트렌디한 (Trendy)": "최신 트렌드를 반영한 감각적인 톤"
}

OUTPUT_FORMAT_OPTIONS = {
    "마크다운 (Markdown)": "## 헤더, **굵기**, - 리스트 형식",
    "JSON": '{"key": "value"} 구조화된 데이터 형식',
    "일반 텍스트 (Plain Text)": "서식 없이 순수 텍스트",
    "번호 목록 (Numbered List)": "1. 첫째 2. 둘째 순서 있는 목록",
    "글머리 목록 (Bullet List)": "• 항목1 • 항목2 글머리 목록",
    "표 (Table)": "| 열1 | 열2 | 표 형식",
    "이메일 (Email)": "수신자/제목/본문/서명 이메일 형식",
    "HTML": "<tag> 웹 마크업 형식",
}

GROQ_MODEL_PRIORITY = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "deepseek-r1-distill-llama-70b",
    "gemma2-9b-it",
]

GROQ_FALLBACK_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "gemma2-9b-it",
]