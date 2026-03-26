import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import calendar
import streamlit.components.v1 as components

# 1. 기본 설정
st.set_page_config(page_title="성의교정 근무달력", layout="wide")

# 타이틀 (작게 유지)
st.markdown("<h5 style='margin-bottom: 0px;'>🏥 성의교정 근무스케줄</h5>", unsafe_allow_html=True)

# 2. 파스텔 톤 컬러 및 폰트 설정 (폰트 크기 3pt 확대)
# 파스텔 배경색
PASTEL_COLORS = {
    "A조": "#FFCC80", # 연한 주황
    "B조": "#EF9A9A", # 연한 빨강
    "C조": "#90CAF9"  # 연한 파랑
}
# 폰트 색상 (진한 회색으로 가독성 확보)
FONT_COLOR = "#333333"

# 폰트 크기 설정 (기존보다 약 3pt 확대)
FONT_SIZES = {
    "month_title": "18px", # 월 표시
    "day_header": "14px",  # 요일 (일~토)
    "date_num": "15px",    # 날짜 숫자 (굵게)
    "shift_name": "11px"   # 조 이름
}

# 3. 근무 로직 및 조회 기능
ORDER = ["B조", "C조", "A조"] # 2026-01-01 기준 순서

def get_shift(target_date):
    """지정한 날짜의 근무 조를 계산합니다."""
    # 기준일: 2026-01-01 (B조 시작)
    base_date = date(2026, 1, 1)
    delta = (target_date - base_date).days
    return ORDER[delta % 3]

# 사이드바 설정
with st.sidebar:
    st.header("⚙️ 조회 옵션")
    
    # 3-1. 본인 조 하이라이트
    target_shift = st.selectbox("👉 하이라이트할 조", ["선택 안 함", "A조", "B조", "C조"])
    
    st.divider()
    
    # 3-2. 무한 조회 기능 (연도 및 월 선택)
    today = datetime.now()
    current_year = today.year
    current_month = today.month
    
    # 조회할 연도 (과거~미래 범위 넉넉히 설정)
    selected_year = st.number_input("조회 연도", min_value=2020, max_value=2035, value=current_year, step=1)
    # 조회 시작 월
    selected_month = st.slider("시작 월", min_value=1, max_value=12, value=current_month)

    st.divider()
    st.info(f"현재 선택: {selected_year}년 {selected_month}월부터 1년")

# 4. 달력 렌더링 함수 (HTML Component 방식, 폰트/컬러 수정)
def render_calendar(year, month, target_shift):
    cal = calendar.monthcalendar(year, month)
    
    # HTML 시작
    html_content = f"""
    <div style="font-family: sans-serif; color: {FONT_COLOR};">
        <h4 style="margin: 10px 0 5px 0; font-size: {FONT_SIZES['month_title']}; text-align: center;">{year}년 {month}월</h4>
        <table style="width:100%; border-collapse: collapse; text-align: center; font-size: {FONT_SIZES['day_header']}; table-layout: fixed;">
            <tr style="background-color: #f7f7f7; height: 25px;">
                <th style="color: #e74c3c;">일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th style="color: #3498db;">토</th>
            </tr>
    """
    
    # 날짜 채우기
    for week in cal:
        html_content += "<tr style='height: 45px;'>" # 칸 높이 확대
        for day in week:
            if day == 0:
                html_content += "<td style='border: 1px solid #f1f1f1;'></td>"
            else:
                current_date = date(year, month, day)
                shift = get_shift(current_date)
                color = PASTEL_COLORS[shift]
                
                # 하이라이트 및 요일별 색상 로직
                is_target = (shift == target_shift)
                # 투명도 조정 (하이라이트 시 나머지 조는 매우 연하게)
                opacity = "1.0" if (target_shift == "선택 안 함" or is_target) else "0.15"
                # 테두리 강조
                border = "2.5px solid #555" if is_target else "1px solid #f1f1f1"
                # 토/일 요일 폰트 색상
                date_color = "#e74c3c" if calendar.weekday(year, month, day) == 6 else ("#3498db" if calendar.weekday(year, month, day) == 5 else FONT_COLOR)

                html_content += f"""
                <td style="background-color: {color}; color: {date_color}; opacity: {opacity}; border: {border}; padding: 3px; position: relative;">
                    <div style="font-weight: bold; font-size: {FONT_SIZES['date_num']}; margin-bottom: 2px;">{day}</div>
                    <div style="font-size: {FONT_SIZES['shift_name']}; color: #555; font-weight: 500;">{shift}</div>
                </td>
                """
        html_content += "</tr>"
    
    html_content += "</table></div>"
    
    # 컴포넌트 높이 자동 조절 (폰트 확대에 맞춰 늘림)
    components.html(html_content, height=290)

# 5. 메인 화면 출력 (선택한 달부터 12개월 표출)
st.markdown(f"**🗓️ {selected_year}년 {selected_month}월 기준 1년 달력**")

cols = st.columns(2) # 2열 배치
for i in range(12):
    # 조회 시작 날짜 계산
    start_date = date(selected_year, selected_month, 1)
    # 현재 달의 연도/월 계산 (12개월 순환)
    target_date = start_date + timedelta(days=i*31) # 대략적인 계산 (calendar 모듈로 보정 예정)
    
    # 1년치 월을 순서대로 계산 (calendar.month_name은 안 쓰고 직접 연/월 계산)
    y = selected_year + (selected_month + i - 1) // 12
    m = (selected_month + i - 1) % 12 + 1
    
    with cols[i % 2]:
        render_calendar(y, m, target_shift)
