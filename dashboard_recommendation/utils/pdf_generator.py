import os
from io import BytesIO
import tempfile
from fpdf import FPDF

class PDFReport(FPDF):
    def header(self):
        # 폰트가 추가된 후에만 출력
        if 'Nanum' in self.fonts:
            self.set_font('Nanum', '', 12)
            self.cell(0, 10, 'Tableau AI Dashboard Recommendation', border=0, align='C')
            self.ln(15)

    def footer(self):
        self.set_y(-15)
        if 'Nanum' in self.fonts:
            self.set_font('Nanum', '', 9)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf_report(result_json, dashboard_img) -> bytes:
    """
    JSON 결과와 PIL 이미지를 받아 PDF 파일(bytes)을 생성합니다.
    """
    pdf = PDFReport()
    
    # 한글 폰트 로드
    font_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'fonts', 'NanumGothic.ttf')
    
    # fpdf2에서는 폰트를 add_font로 추가. 
    pdf.add_font('Nanum', '', font_path, uni=True)
    
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # 1. 개요
    pdf.set_font('Nanum', '', 15)
    pdf.cell(0, 10, "1. 대시보드 개요", ln=True)
    pdf.set_font('Nanum', '', 11)
    
    summary_text = result_json.get("summary", "")
    pdf.multi_cell(0, 8, summary_text)
    pdf.ln(5)
    
    # 2. 메타 정보
    pdf.set_font('Nanum', '', 12)
    pdf.cell(0, 8, "■ 상세 정보", ln=True)
    pdf.set_font('Nanum', '', 11)
    pdf.cell(0, 8, f"- 신뢰도 점수: {result_json.get('confidence_score', 'N/A')}", ln=True)
    pdf.cell(0, 8, f"- 데이터 소스: {result_json.get('data_source', 'N/A')}", ln=True)
    pdf.cell(0, 8, f"- 업데이트 주기: {result_json.get('update_cycle', 'N/A')}", ln=True)
    pdf.cell(0, 8, f"- 사용자 그룹: {result_json.get('user_group', 'N/A')}", ln=True)
    pdf.ln(10)
    
    # 3. 프리뷰 이미지
    if dashboard_img:
        pdf.set_font('Nanum', '', 15)
        pdf.cell(0, 10, "2. 대시보드 예상 프리뷰", ln=True)
        pdf.ln(5)
        
        # 임시 파일로 저장 후 삽입
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            dashboard_img.save(tmp.name, format="PNG")
            img_path = tmp.name
        
        # 너비를 페이지 너비(약 190)에 맞춤
        pdf.image(img_path, w=170)
        os.unlink(img_path)
        pdf.ln(10)
    
    # 4. 추천 뷰 구성
    pdf.add_page()
    pdf.set_font('Nanum', '', 15)
    pdf.cell(0, 10, "3. 추천 뷰 구성", ln=True)
    views = result_json.get("views", [])
    for view in views:
        pdf.set_font('Nanum', '', 12)
        v_name = view.get('name', '')
        v_type = view.get('chart_type', '')
        pdf.cell(0, 8, f"▶ {v_name} ({v_type})", ln=True)
        
        pdf.set_font('Nanum', '', 10)
        pdf.multi_cell(0, 7, view.get('purpose', ''))
        pdf.ln(4)
        
    # 5. 전문가 팁
    pdf.ln(5)
    pdf.set_font('Nanum', '', 15)
    pdf.cell(0, 10, "4. 전문가 팁", ln=True)
    tips = result_json.get("pro_tips", [])
    for tip in tips:
        if isinstance(tip, dict):
            pdf.set_font('Nanum', '', 12)
            pdf.cell(0, 8, f"💡 {tip.get('title', '')}", ln=True)
            pdf.set_font('Nanum', '', 10)
            
            # 내용에서 줄바꿈 처리
            content = tip.get('content', '').replace('\r', '')
            pdf.multi_cell(0, 7, content)
            pdf.ln(4)
            
    # PDF 바이트 반환
    return bytes(pdf.output())
