import streamlit as st
import pandas as pd
from datetime import datetime, date
import calendar
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import io

# 1. 기본 설정 및 데이터 정의
st.set_page_config(page_title="2026 성의교정 근무달력", layout="wide")

# 근무 패턴 정의 (이미지 기준: 1월 1일 B조부터 시작하는 로테이션)
# A: 주황(#F39C12), B: 빨강(#C0392B), C: 파랑(#2980B9)
COLORS = {"A조": "#F39C12", "B조": "#C0392B", "C조": "#2980B9", "평시": "#FFFFFF"}
ORDER = ["B조", "C조", "A조"] # 이미지의 1월 흐름 기준

def get_shift(target_date):
    start_date = date(2026, 1, 1)
    delta = (target_date - start_date).days
    return ORDER[delta % 3]

# 2. PDF 생성 함수
def create_pdf(half_year):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
    elements = []
    styles = getSampleStyleSheet()
    
    title = f"2026년 {'상반기' if half_year == 1 else '하반기'} 근무 스케줄"
    elements.append(Paragraph(title, styles['Title']))
    
    months = range(1, 7) if half_year == 1 else range(7, 13)
    
    for month in months:
        elements.append(Paragraph(f"{month}월", styles['Heading2']))
        cal = calendar.monthcalendar(2026, month)
        data = [["일", "월", "화", "수", "목", "금", "토"]]
        
        for week in cal:
            row = []
            for day in week:
                if day == 0:
                    row.append("")
                else:
                    shift = get_shift(date(2026, month, day))
                    row.append(f"{day}\n({shift})")
            data.append(row)
        
        t = Table(data, colWidths=80)
        t.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTSIZE', (0,0), (-1,-1), 8),
        ]))
        elements.append(t)
    
    doc.build(elements)
    return buffer.getvalue()

# 3. UI 구성
st.title("🏥 2026 성의교정 근무스케줄")

with st.sidebar:
    st.header("설정")
    target_shift = st.selectbox("본인 조 선택 (하이라이트)", ["선택 안 함", "A조", "B조", "C조"])
    
    st.divider()
    half = st.radio("PDF 다운로드 범위", ["상반기 (1-6월)", "하반기 (7-12월)"])
    pdf_data = create_pdf(1 if "상반기" in half else 2)
    st.download_button(
        label=f"{half} PDF 다운로드",
        data=pdf_data,
        file_name=f"2026_work_schedule_{half}.pdf",
        mime="application/pdf"
    )

# 4. 달력 출력 (4열 3행 구조)
cols = st.columns(4)
for m in range(1, 13):
    with cols[(m-1)%4]:
        st.markdown(f"### {m}월")
        cal = calendar.monthcalendar(2026, m)
        
        # HTML 달력 생성
        html = "<table style='width:100%; border-collapse: collapse; text-align: center; font-size: 12px;'>"
        html += "<tr style='background-color: #f0f2f6;'><th>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th>토</th></tr>"
        
        for week in cal:
            html += "<tr>"
            for day in week:
                if day == 0:
                    html += "<td></td>"
                else:
                    current_date = date(2026, m, day)
                    shift = get_shift(current_date)
                    color = COLORS[shift]
                    
                    # 하이라이트 로직
                    is_target = (shift == target_shift)
                    opacity = "1.0" if (target_shift == "선택 안 함" or is_target) else "0.2"
                    border = "2px solid black" if is_target else "none"
                    
                    html += f"""
                    <td style='background-color: {color}; color: white; opacity: {opacity}; border: {border}; padding: 5px; border-radius: 4px;'>
                        {day}<br/><b style='font-size: 10px;'>{shift}</b>
                    </td>
                    """
            html += "</tr>"
        html += "</table>"
        st.write(html, unsafe_allow_html=True)
        st.write("") # 간격 조절
