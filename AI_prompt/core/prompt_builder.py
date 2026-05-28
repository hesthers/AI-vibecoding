import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
import json
from datetime import datetime
import html
from groq import Groq

from utils.constants import TASK_OPTIONS, TONE_OPTIONS, OUTPUT_FORMAT_OPTIONS

def build_final_prompt(
        role: str,
        expertise: str,
        task: str,
        task_detail: str,
        target: str,
        constraints: str,
        reference: str,
        output_format: str,
        tone: str,
        examples: list,
        language: str,
    ) -> str:
    """
    사용자 입력을 바탕으로 AI에 바로 사용 가능한 최적화 프롬프트를 생성합니다.
    중간 API 호출 없이 규칙 기반으로 즉시 생성됩니다.
    """

    lines = []

    # ── 1. 역할 정의 ──────────────────────────────────────────────────────────
    # lines.append("") # ✨ [추가] HTML 박스와 분리하여 마크다운 버그를 방지하는 빈 줄
    lines.append("## 역할 및 페르소나 (Persona Definition)")
    # lines.append("") # ✨ [추가] 제목과 본문("당신은...") 사이에 확실한 줄바꿈을 보장하는 빈 줄
    role_str = role.strip() if role.strip() else "전문가"
    expertise_str = expertise.strip()

    if expertise_str:
        lines.append(f"당신은 {expertise_str}을(를) 보유한 **{role_str}**로 ")
    else:
        lines.append(f"당신은 **{role_str}**로")

    # 톤 지시
    tone_key = tone.split("(")[0].strip()
    tone_value = TONE_OPTIONS.get(tone).strip()
    lines.append(f"답변은 항상 **{tone_key}** 톤({tone_value})을 유지.")
    lines.append("")
    lines.append("---")

    # ── 2. 작업 지시 ──────────────────────────────────────────────────────────
    task_name = task.split("(")[0].strip()
    task_value = TASK_OPTIONS.get(task).strip()
    lines.append("## 작업 지시 (Task)") 
    lines.append(f"다음 작업을 수행하세요: **{task_name}**\n")
    

    if task_detail.strip():
        lines.append("")
        # ✨ 상세 지시사항 전체에 인용구(>) 기호를 붙여 박스로 만듭니다.
        lines.append("> ⚙️ **상세 지시사항:**")
        lines.append(f"> - {task_value}")
        for step in task_detail.strip().split("\n"):
            if step.strip():
                lines.append(f"> - {step.strip()}")

    lines.append("")
    lines.append("---")

    # ── 3. 대상 및 맥락 ───────────────────────────────────────────────────────
    has_context = any([target.strip(), constraints.strip(), reference.strip()])
    if has_context:
        lines.append("## 맥락 및 제약 (Context & Constraints)")

        if target.strip():
            lines.append(f"- **대상 독자/사용자:** {target.strip()}")

        if constraints.strip():
            lines.append(f"- **제약 사항:** {constraints.strip()}")

        if reference.strip():
            lines.append("")
            lines.append("> ⚙️ **참조 자료:**")
            lines.append(f"> - {reference.strip()}")
    lines.append("")
    lines.append("---")

    # ── 4. Few-Shot 예시 ───────────────────────────────────────────────────────
    valid_examples = [(e["input"], e["output"]) for e in examples
                      if e["input"].strip() and e["output"].strip()]
    if valid_examples:
        lines.append("## 참고 예시 (Zero/Few-Shot Examples)") # ✨ 제목 변경
        for i, (inp, out) in enumerate(valid_examples, 1):
            lines.append(f"\n**예시 {i}**")
            lines.append(f"- 입력: {inp.strip()}")
            lines.append(f"- 출력: \n")
            # lines.append(f"{out.strip().strip().splitlines()}")
            for idx, txt in enumerate(filter(None,out.strip().splitlines())):
                lines.append(f"  {idx+1}) {txt.strip()} \n")
    lines.append("")
    lines.append("---")

    # ── 5. 출력 형식 ──────────────────────────────────────────────────────────
    fmt_key = output_format.split("(")[0].strip()
    fmt_desc = OUTPUT_FORMAT_OPTIONS.get(output_format, "")
    lines.append("## 출력 형식")
    lines.append(f"반드시 **{fmt_key}** 형식으로 출력하세요.")
    if fmt_desc:
        lines.append(f"_(형식 참고: {fmt_desc})_")
    lines.append("")
    # lines.append("---")

    # ── 6. 언어 지시 ──────────────────────────────────────────────────────────
    lang_map = {
        "한국어": "모든 답변을 **한국어**로 작성하세요.",
        "영어 (English)": "Write all responses in **English**.",
        "한국어 + 영어": "한국어로 작성하되, 주요 용어는 영문을 병기하세요. 예: 머신러닝(Machine Learning)",
    }
    if language in lang_map:
        lines.append(lang_map[language])
    lines.append("")

    # ── 7. 마무리 지시 ────────────────────────────────────────────────────────
    lines.append("---")
    lines.append("위 조건을 모두 충족하는 최적의 답변을 작성해주세요.")

    return "\n".join(lines)