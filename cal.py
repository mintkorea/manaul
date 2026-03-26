import streamlit as st
import pandas as pd
from datetime import datetime, date
import calendar
import io
import streamlit.components.v1 as components

# 1. 기본 설정
st.set_page_config(page_title="2026 성의교정 근무달력", layout="wide")

# 타이틀 (폰트 크기 대폭 축소)
st.markdown("<h5 style='margin-bottom: 0px;'>🏥 2026 성의교정 근무스케줄</h5>", unsafe_allow_html=True)

# 근무 패턴 정의
COLORS = {"A조": "#F39C12", "B조": "#C0392B", "C조": "#2980B9"}
ORDER = ["B조", "C조", "A조"] 

def get_shift(target_date):
    start_date = date(2026, 1, 1)
    delta = (target_date - start_date).days
    return ORDER[delta % 3]

# 2. 사이드바 (필요한 기능만 유지)
with st.sidebar:
    st.header("⚙️ 옵션")
    target_shift = st.selectbox("하이라이트", ["선택 안 함", "A조", "B조", "C조"])
    st.info("PDF 다운로드 기능은 현재 페이지 레이아웃 최적화 중입니다.")

# 3. 달력 렌더링 함수 (HTML Component 방식)
def render_calendar(month, target_shift):
    cal = calendar.monthcalendar(2026, month)
    
    html_content = f"""
    <div style="font-family: sans-serif;">
        <h4 style="margin: 5px 0; font-size: 14px;">{month}월</h4>
        <table style="width:100%; border-collapse: collapse; text-align: center; font-size: 10px; table-layout: fixed;">
            <tr style="background-color: #f0f2f6; height: 20px;">
                <th>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th>토</th>
            </tr>
    """
    
    for week in cal:
        html_content += "<tr style='height: 35px;'>"
        for day in week:
            if day == 0:
                html_content += "<td style='border: 1px solid #eee;'></td>"
            else:
                current_date = date(2026, month, day)
                shift = get_shift(current_date)
                color = COLORS[shift]
                
                # 하이라이트 로직
                is_target = (shift == target_shift)
                opacity = "1.0" if (target_shift == "선택 안 함" or is_target) else "0.1"
                border = "2px solid #333" if is_target else "1px solid #eee"
                
                html_content += f"""
                <td style="background-color: {color}; color: white; opacity: {opacity}; border: {border}; padding: 2px;">
                    <div style="font-weight: bold; font-size: 11px;">{day}</div>
                    <div style="font-size: 8px;">{shift}</div>
                </td>
                """
        html_content += "</tr>"
    
    html_content += "</table></div>"
    
    # 컴포넌트 높이 자동 조절 (약 200px~250px)
    components.html(html_content, height=230)

# 4. 메인 화면 출력 (2열 배치)
cols = st.columns(2)
for m in range(1, 13):
    with cols[(m-1)%2]:
        render_calendar(m, target_shift)
