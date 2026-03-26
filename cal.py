import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import calendar

# 1. 페이지 설정 및 상단 여백 (1cm 이상 확보)
st.set_page_config(page_title="성의교정 근무달력", layout="centered")

st.markdown("""
    <style>
    /* 상단 여백 증설 */
    .block-container { padding-top: 4rem !important; }
    
    /* 월 표시 폰트 크기 증량 (기존 대비 약 5pt 커진 1.8rem) */
    .month-title { 
        text-align: center; 
        font-weight: bold; 
        font-size: 1.8rem !important; 
        margin: 30px 0 15px 0;
        color: #333;
    }

    /* 테이블 레이아웃 및 HTML 노출 방지 스타일 */
    .cal-table { width: 100%; border-collapse: collapse; table-layout: fixed; border: 1px solid #eee; }
    .cal-table th, .cal-table td { border: 1px solid #eee; text-align: center; padding: 0 !important; height: 85px !important; }
    
    .sun-head { color: #d32f2f; background: #f8f9fa; font-weight: bold; }
    .sat-head { color: #1976d2; background: #f8f9fa; font-weight: bold; }
    
    .cell-wrapper { display: flex; flex-direction: column; height: 100%; width: 100%; }
    .date-box { height: 35%; display: flex; align-items: center; justify-content: center; font-size: 16px; font-weight: bold; background-color: white; }
    .shift-box { height: 65%; display: flex; align-items: center; justify-content: center; font-size: 22px; font-weight: 900; }
    
    .text-sun { color: #d32f2f; }
    .text-sat { color: #1976d2; }
    </style>
    """, unsafe_allow_html=True)

# 2. 근무 및 공휴일 로직
ORDER = ["B", "C", "A"]
BASE_COLORS = {"A": "#FFE0B2", "B": "#FFCDD2", "C": "#BBDEFB"}
STRONG_COLORS = {"A": "#FB8C00", "B": "#E53935", "C": "#1E88E5"}

def get_shift(dt):
    base = date(2026, 1, 1)
    return ORDER[(dt - base).days % 3]

def is_holiday(dt):
    hols = [date(dt.year, 1, 1), date(dt.year, 3, 1), date(dt.year, 5, 5), date(dt.year, 6, 6),
            date(dt.year, 8, 15), date(dt.year, 10, 3), date(dt.year, 10, 9), date(dt.year, 12, 25)]
    return dt in hols

# 3. 상단 컨트롤러
st.subheader("🏥 성의교정 근무스케줄")

c1, c2 = st.columns([1, 2])
with c1:
    hi_shift = st.selectbox("🎯 강조할 조", ["선택 안 함", "A", "B", "C"])
with c2:
    offset = st.slider("📅 조회 범위(현재 기준)", -12, 12, 0)

# 기준 날짜 계산
start_dt = (datetime.now().replace(day=1) + timedelta(days=31 * offset)).replace(day=1)

# 4. 달력 렌더링 함수
def render_month(y, m, highlight):
    cal = calendar.monthcalendar(y, m)
    # 월 타이틀 (폰트 크기 적용)
    html = f"<div class='month-title'>{y}년 {m}월</div>"
    html += "<table class='cal-table'>"
    html += "<tr><th class='sun-head'>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class='sat-head'>토</th></tr>"
    
    for week in cal:
        html += "<tr>"
        for i, day in enumerate(week):
            if day == 0:
                html += "<td></td>"
            else:
                curr = date(y, m, day)
                s = get_shift(curr)
                day_clr = "text-sun" if (i == 0 or is_holiday(curr)) else ("text-sat" if i == 6 else "")
                
                # 하이라이트 여부에 따른 색상 및 텍스트 설정
                is_hi = (highlight == s)
                bg = STRONG_COLORS[s] if is_hi else BASE_COLORS[s]
                d_bg = STRONG_COLORS[s] if is_hi else "white"
                txt_clr = "white" if is_hi else "#333"

                html += f"""
                <td style="background-color: {bg};">
                    <div class="cell-wrapper">
                        <div class="date-box {day_clr}" style="background-color: {d_bg}; color: {txt_clr if is_hi else ''};">
                            {day}
                        </div>
                        <div class="shift-box" style="color: {txt_clr};">
                            {s}
                        </div>
                    </div>
                </td>
                """
        html += "</tr>"
    html += "</table>"
    return html

# 5. 12개월 연속 출력
for n in range(12):
    target = start_dt + timedelta(days=n * 31)
    y, m = target.year, target.month
    
    # 월 중복 방지 보정
    if n > 0:
        prev_m = (start_dt + timedelta(days=(n-1)*31)).month
        if m == prev_m:
            target += timedelta(days=15)
            y, m = target.year, target.month
            
    # 핵심: markdown 내부에서 공백이나 줄바꿈에 의한 깨짐 방지
    st.markdown(render_month(y, m, hi_shift), unsafe_allow_html=True)
