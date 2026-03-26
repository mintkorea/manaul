import streamlit as st
import pandas as pd
from datetime import datetime, date
import calendar
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import io

# 1. 기본 설정
st.set_page_config(page_title="2026 성의교정 근무달력", layout="wide")

# 타이틀 폰트 크기를 절반 정도로 줄임 (h2 수준)
st.markdown("## 🏥 2026 성의교정 근무스케줄")

# 근무 패턴 정의 (이미지 기준: 1월 1일 B조부터 시작)
COLORS = {"A조": "#F39C12", "B조": "#C0392B", "C조": "#2980B9", "평시": "#FFFFFF"}
ORDER = ["B조", "C조", "A조"] 

def get_shift(target_date):
    start_date = date(2026, 1, 1)
    delta = (target_date - start_date).days
    return ORDER[delta % 3]

# 2. PDF 생성 함수 (상/하반기)
def create_pdf(half_year):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
    elements = []
    styles = getSampleStyleSheet()
    
    title = f"2026 Work Schedule ({'1st' if half_year == 1 else '2nd'} Half)"
    elements.append(Paragraph(title, styles['Title']))
    
    months = range(1, 7) if half_year == 1 else range(7, 13)
    
    for month in months:
        elements.append(Paragraph(f"{month} Month", styles['Heading2']))
        cal = calendar.monthcalendar(2026, month)
        data = [["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]]
        
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

# 3. 사이드바 UI
with st.sidebar:
    st.header("⚙️ 옵션")
    target_shift = st.selectbox("하이라이트할 조 선택", ["선택 안 함", "A조", "B조", "C조"])
    
    st.divider()
    half = st.radio("PDF 다운로드", ["상반기 (1-6월)", "하반기 (7-12월)"])
    pdf_data = create_pdf(1 if "상반기" in half else 2)
    st.download_button(
        label=f"⬇️ {half} PDF 저장",
        data=pdf_data,
        file_name=f"2026_calendar_{half}.pdf",
        mime="application/pdf"
    )

# 4. 메인 달력 출력 (그리드 배치)
cols = st.columns(2) # 모바일 가독성을 위해 2열로 조정 (또는 필요시 4열)
for m in range(1, 13):
    with cols[(m-1)%2]:
        st.markdown(f"#### {m}월")
        cal = calendar.monthcalendar(2026, m)
        
        html = "<table style='width:100%; border-collapse: collapse; text-align: center; font-size: 11px; table-layout: fixed;'>"
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
                    
                    is_target = (shift == target_shift)
                    opacity = "1.0" if (target_shift == "선택 안 함" or is_target) else "0.15"
                    border = "2px solid #000" if is_target else "1px solid #ddd"
                    
                    html += f"""
                    <td style='background-color: {color}; color: white; opacity: {opacity}; border: {border}; padding: 4px; height: 40px;'>
                        <div style='font-weight: bold;'>{day}</div>
                        <div style='font-size: 9px;'>{shift}</div>
                    </td>
                    """
            html += "</tr>"
        html += "</table>"
        st.write(html, unsafe_allow_allow_html=True)
        st.write("") 
