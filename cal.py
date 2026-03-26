import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import calendar

# 1. 기본 설정 및 여백 최적화
st.set_page_config(page_title="성의교정 근무달력", layout="centered")

st.markdown("""
    <style>
    /* 상단 여백 1cm 줄임 */
    .block-container { padding-top: 1rem !important; }
    
    /* 타이틀 폰트 60% 축소 */
    .custom-title { font-size: 1.5rem !important; font-weight: bold; margin-bottom: 10px; }
    
    /* 테이블 스타일: 날짜 아래 조 이름 확실히 표기 */
    .stTable td { 
        font-size: 19px !important; 
        height: 65px !important; 
        line-height: 1.2 !important;
        text-align: center !important;
        white-space: pre-line !important;
    }
    .stTable th { font-size: 15px !important; text-align: center !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. 근무 로직 및 컬러 (하이라이트 시 진한 톤)
ORDER = ["B", "C", "A"] # 조 이름 단축 표기
BASE_COLORS = {
    "A": "background-color: #FFE0B2; color: #333;",
    "B": "background-color: #FFCDD2; color: #333;",
    "C": "background-color: #BBDEFB; color: #333;"
}
STRONG_COLORS = {
    "A": "background-color: #FB8C00; color: #fff; font-weight: bold; border: 2px solid #000;",
    "B": "background-color: #E53935; color: #fff; font-weight: bold; border: 2px solid #000;",
    "C": "background-color: #1E88E5; color: #fff; font-weight: bold; border: 2px solid #000;"
}

def get_shift(target_date):
    base_date = date(2026, 1, 1)
    delta = (target_date - base_date).days
    return ORDER[delta % 3]

# 3. 상단 컨트롤러 (타이틀 축소 및 슬라이더)
st.markdown('<div class="custom-title">🏥 성의교정 근무스케줄</div>', unsafe_allow_html=True)

# 조 선택 및 슬라이더 배치
highlight_shift = st.selectbox("🎯 강조할 조 선택", ["선택 안 함", "A", "B", "C"])
month_offset = st.slider("📅 조회 범위 조절 (현재 기준)", -12, 12, 0)

# 기준 날짜 계산
today = datetime.now()
start_date = (today.replace(day=1) + timedelta(days=31 * month_offset)).replace(day=1)

# 4. 스타일 적용 함수
def style_calendar(df, year, month, highlight):
    styles = pd.DataFrame('', index=df.index, columns=df.columns)
    for r in range(len(df)):
        for c in range(len(df.columns)):
            val = df.iloc[r, c]
            if val != "":
                day_int = int(val.split('\n')[0])
                curr_date = date(year, month, day_int)
                shift = get_shift(curr_date)
                
                if highlight != "선택 안 함" and shift == highlight:
                    style = STRONG_COLORS.get(shift, "")
                else:
                    style = BASE_COLORS.get(shift, "")
                styles.iloc[r, c] = style
    return styles

# 5. 달력 세로 1열 출력 (12개월)
for i in range(12):
    # 각 달의 연도와 월 계산
    target_month_date = start_date + timedelta(days=i * 31)
    curr_y = target_month_date.year
    curr_m = target_month_date.month
    
    # 겹침 방지 및 정확한 월 계산 보정
    if i > 0:
        prev_m = (start_date + timedelta(days=(i-1)*31)).month
        if curr_m == prev_m: # timedelta 오차 보정
            target_month_date += timedelta(days=10)
            curr_y = target_month_date.year
            curr_m = target_month_date.month

    st.write(f"#### 📅 {curr_y}년 {curr_m}월")
    
    cal = calendar.monthcalendar(curr_y, curr_m)
    display_data = []
    for week in cal:
        row = [f"{d}\n{get_shift(date(curr_y, curr_m, d))}" if d != 0 else "" for d in week]
        display_data.append(row)
    
    df = pd.DataFrame(display_data, columns=['일', '월', '화', '수', '목', '금', '토'])
    styled_df = df.style.apply(lambda d: style_calendar(df, curr_y, curr_m, highlight_shift), axis=None)
    
    st.table(styled_df)
    st.write("") # 간격 확보
