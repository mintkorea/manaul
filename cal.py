import streamlit as st
import pandas as pd
from datetime import datetime, date
import calendar

# 1. 기본 설정
st.set_page_config(page_title="성의교정 근무달력", layout="wide")

# CSS 주입: 폰트 크기 확대 및 스타일 고정
st.markdown("""
    <style>
    .cal-table { width:100%; border-collapse: collapse; text-align: center; table-layout: fixed; margin-bottom: 20px; }
    .cal-table th { background-color: #f8f9fa; padding: 5px; font-size: 15px; border: 1px solid #eee; }
    .cal-table td { padding: 8px; border: 1px solid #eee; height: 55px; vertical-align: middle; }
    .date-num { font-weight: bold; font-size: 18px; margin-bottom: 2px; }
    .shift-name { font-size: 13px; font-weight: 500; }
    .sun { color: #e74c3c; }
    .sat { color: #3498db; }
    </style>
    """, unsafe_allow_html=True)

# 타이틀
st.markdown("### 🏥 성의교정 근무스케줄")

# 2. 근무 로직 및 컬러 (파스텔 톤)
PASTEL_COLORS = {"A조": "#FFCC80", "B조": "#EF9A9A", "C조": "#90CAF9"}
ORDER = ["B조", "C조", "A조"]

def get_shift(target_date):
    base_date = date(2026, 1, 1) # 기준일
    delta = (target_date - base_date).days
    return ORDER[delta % 3]

# 3. 사이드바 제어
with st.sidebar:
    st.header("⚙️ 옵션")
    target_shift = st.selectbox("👉 하이라이트할 조", ["선택 안 함", "A조", "B조", "C조"])
    
    st.divider()
    today = datetime.now()
    sel_year = st.number_input("연도 선택", min_value=2020, max_value=2035, value=today.year)
    sel_month = st.slider("시작 월 선택", 1, 12, today.month)

# 4. 달력 생성 함수 (st.write 방식 사용 - 기능 연동 확실함)
def draw_calendar(year, month, highlight):
    cal = calendar.monthcalendar(year, month)
    
    html = f"<div style='text-align: center; margin-top:15px;'><b>{year}년 {month}월</b></div>"
    html += "<table class='cal-table'>"
    html += "<tr><th class='sun'>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class='sat'>토</th></tr>"
    
    for week in cal:
        html += "<tr>"
        for i, day in enumerate(week):
            if day == 0:
                html += "<td></td>"
            else:
                curr_date = date(year, month, day)
                shift = get_shift(curr_date)
                color = PASTEL_COLORS[shift]
                
                # 하이라이트 조건
                is_target = (shift == highlight)
                opacity = "1.0" if (highlight == "선택 안 함" or is_target) else "0.15"
                border = "3px solid #333" if is_target else "1px solid #eee"
                
                # 요일 색상
                d_cls = "sun" if i == 0 else ("sat" if i == 6 else "")
                
                html += f"""
                <td style="background-color: {color}; opacity: {opacity}; border: {border};">
                    <div class="date-num {d_cls}">{day}</div>
                    <div class="shift-name" style="color: #444;">{shift}</div>
                </td>
                """
        html += "</tr>"
    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

# 5. 메인 레이아웃 (선택 월부터 12개월 출력)
st.info(f"📅 {sel_year}년 {sel_month}월부터 1년간의 일정입니다.")

cols = st.columns(2)
for i in range(12):
    # 연/월 계산 로직 보정
    m = (sel_month + i - 1) % 12 + 1
    y = sel_year + (sel_month + i - 1) // 12
    
    with cols[i % 2]:
        draw_calendar(y, m, target_shift)
