import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import calendar

# 1. 기본 설정 및 여백 최적화
st.set_page_config(page_title="성의교정 근무달력", layout="centered")

st.markdown("""
    <style>
    .block-container { padding-top: 1rem !important; }
    /* 테이블 칸 스타일: 내부 레이아웃 분리 */
    .stTable td { 
        padding: 0 !important; 
        height: 80px !important; 
        width: 14% !important;
        vertical-align: top !important;
    }
    .cell-container { display: flex; flex-direction: column; height: 100%; border: 0.5px solid #eee; }
    .date-part { background-color: white; height: 40%; font-size: 16px; font-weight: bold; padding-top: 5px; }
    .shift-part { height: 60%; font-size: 20px; font-weight: 900; display: flex; align-items: center; justify-content: center; }
    
    /* 요일별 색상 */
    .sun { color: #d32f2f !important; }
    .sat { color: #1976d2 !important; }
    .holiday { color: #d32f2f !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. 근무 로직 및 공휴일 데이터
ORDER = ["B", "C", "A"]
# 기본 파스텔톤 (조 표시 부분)
BASE_COLORS = {"A": "#FFE0B2", "B": "#FFCDD2", "C": "#BBDEFB"}
# 하이라이트 시 칸 전체에 적용될 진한 톤
STRONG_COLORS = {"A": "#FB8C00", "B": "#E53935", "C": "#1E88E5"}

def get_shift(target_date):
    base_date = date(2026, 1, 1)
    delta = (target_date - base_date).days
    return ORDER[delta % 3]

def is_holiday(dt):
    # 주요 공휴일 예시 (필요시 추가 가능)
    holidays = [date(dt.year, 1, 1), date(dt.year, 3, 1), date(dt.year, 5, 5), 
                date(dt.year, 8, 15), date(dt.year, 10, 3), date(dt.year, 10, 9), date(dt.year, 12, 25)]
    return dt in holidays

# 3. 상단 컨트롤러
st.subheader("🏥 성의교정 근무스케줄")

c1, c2 = st.columns([1, 2])
with c1:
    highlight_shift = st.selectbox("🎯 강조할 조", ["선택 안 함", "A", "B", "C"])
with c2:
    month_offset = st.slider("📅 조회 범위(현재 기준)", -12, 12, 0)

# 기준 날짜 계산
today = datetime.now()
start_date = (today.replace(day=1) + timedelta(days=32 * month_offset)).replace(day=1)

# 4. 달력 렌더링 함수 (HTML 직접 주입 방식으로 정밀 제어)
def render_calendar_html(year, month, highlight):
    cal = calendar.monthcalendar(year, month)
    html = f"<div style='text-align: center; margin-bottom: 10px;'><b>{year}년 {month}월</b></div>"
    html += "<table style='width: 100%; border-collapse: collapse; table-layout: fixed;'>"
    html += "<tr style='background: #f8f9fa;'><th class='sun'>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class='sat'>토</th></tr>"
    
    for week in cal:
        html += "<tr>"
        for i, day in enumerate(week):
            if day == 0:
                html += "<td style='border: 0.5px solid #eee;'></td>"
            else:
                curr_date = date(year, month, day)
                shift = get_shift(curr_date)
                is_h = is_holiday(curr_date)
                
                # 요일/공휴일 클래스 결정
                day_class = "sun" if i == 0 or is_h else ("sat" if i == 6 else "")
                
                # 배경색 결정 (하이라이트 여부)
                if highlight == shift:
                    full_bg = STRONG_COLORS[shift]
                    date_bg = STRONG_COLORS[shift] # 하이라이트 시 날짜 배경도 동일하게
                    text_color = "white"
                else:
                    full_bg = BASE_COLORS[shift]
                    date_bg = "white" # 기본 상태에서 날짜는 백색 배경
                    text_color = "#333"

                html += f"""
                <td style="background-color: {full_bg};">
                    <div class="cell-container">
                        <div class="date-part {day_class}" style="background-color: {date_bg}; color: {'inherit' if highlight != shift else 'white'};">
                            {day}
                        </div>
                        <div class="shift-part" style="color: {text_color};">
                            {shift}
                        </div>
                    </div>
                </td>
                """
        html += "</tr>"
    html += "</table>"
    return html

# 5. 세로 1열 출력
for i in range(12):
    # 월 계산 보정
    target_date = start_date + timedelta(days=i * 31)
    y, m = target_date.year, target_date.month
    
    # 중복 출력 방지 로직 (timedelta 오차 대응)
    if i > 0:
        prev_date = start_date + timedelta(days=(i-1)*31)
        if prev_date.month == m:
            target_date += timedelta(days=15)
            y, m = target_date.year, target_date.month

    st.markdown(render_calendar_html(y, m, highlight_shift), unsafe_allow_html=True)
    st.write("") # 간격
