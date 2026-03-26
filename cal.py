import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import calendar

# 1. 기본 설정 및 상단 여백 증설 (1cm 추가)
st.set_page_config(page_title="성의교정 근무달력", layout="centered")

st.markdown("""
    <style>
    /* 상단 여백을 약 1cm(40px) 늘림 */
    .block-container { padding-top: 3.5rem !important; }
    
    /* 타이틀 및 서브헤더 스타일 */
    .stSubheader { margin-top: -10px; margin-bottom: 20px; }

    /* 테이블 레이아웃 정밀 제어 */
    table { width: 100%; border-collapse: collapse; table-layout: fixed; }
    th, td { border: 1px solid #eee; text-align: center; padding: 0 !important; height: 85px !important; }
    
    /* 요일 헤더 */
    .sun-head { color: #d32f2f; background: #f8f9fa; font-weight: bold; }
    .sat-head { color: #1976d2; background: #f8f9fa; font-weight: bold; }
    
    /* 내부 셀 구조 */
    .cell-wrapper { display: flex; flex-direction: column; height: 100%; width: 100%; }
    .date-box { height: 35%; display: flex; align-items: center; justify-content: center; font-size: 16px; font-weight: bold; background-color: white; }
    .shift-box { height: 65%; display: flex; align-items: center; justify-content: center; font-size: 22px; font-weight: 900; }
    
    /* 요일/공휴일 텍스트 색상 */
    .text-sun { color: #d32f2f; }
    .text-sat { color: #1976d2; }
    </style>
    """, unsafe_allow_html=True)

# 2. 로직 정의
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

# 시작 날짜 계산
start_dt = (datetime.now().replace(day=1) + timedelta(days=31 * offset)).replace(day=1)

# 4. 달력 생성 함수 (st.write(html) 대신 텍스트 조합 방식)
def draw_month(y, m, highlight):
    cal = calendar.monthcalendar(y, m)
    tbl = f"<div style='text-align:center; font-weight:bold; margin: 20px 0 10px;'>{y}년 {m}월</div>"
    tbl += "<table><tr><th class='sun-head'>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class='sat-head'>토</th></tr>"
    
    for week in cal:
        tbl += "<tr>"
        for i, day in enumerate(week):
            if day == 0:
                tbl += "<td></td>"
            else:
                curr = date(y, m, day)
                s = get_shift(curr)
                day_clr = "text-sun" if (i == 0 or is_holiday(curr)) else ("text-sat" if i == 6 else "")
                
                if highlight == s:
                    bg, d_bg, txt = STRONG_COLORS[s], STRONG_COLORS[s], "white"
                else:
                    bg, d_bg, txt = BASE_COLORS[s], "white", "#333"

                tbl += f"""
                <td style="background-color: {bg};">
                    <div class="cell-wrapper">
                        <div class="date-box {day_clr}" style="background-color: {d_bg}; color: {txt if highlight==s else ''};">
                            {day}
                        </div>
                        <div class="shift-box" style="color: {txt};">
                            {s}
                        </div>
                    </div>
                </td>
                """
        tbl += "</tr>"
    return tbl + "</table>"

# 5. 12개월 출력
for n in range(12):
    target = start_dt + timedelta(days=n * 31)
    y, m = target.year, target.month
    
    # 월 중복 방지 보정
    if n > 0:
        prev_m = (start_dt + timedelta(days=(n-1)*31)).month
        if m == prev_m:
            target += timedelta(days=15)
            y, m = target.year, target.month
            
    st.markdown(draw_month(y, m, hi_shift), unsafe_allow_html=True)
