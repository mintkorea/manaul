import streamlit as st
import pandas as pd
from datetime import datetime, date
import calendar

# 1. 기본 설정
st.set_page_config(page_title="성의교정 근무달력", layout="centered")

st.markdown("""
    <style>
    /* 테이블 스타일 최적화 */
    .stTable td { 
        font-size: 18px !important; 
        height: 70px !important; 
        vertical-align: middle !important;
        white-space: pre-line !important;
        text-align: center !important;
    }
    .stTable th { font-size: 16px !important; text-align: center !important; }
    /* 버튼 및 입력창 간격 조절 */
    div[data-testid="stHorizontalBlock"] {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 근무 로직 및 컬러 (파스텔 & 진한 톤)
ORDER = ["B조", "C조", "A조"]
# 기본 파스텔 톤
BASE_COLORS = {
    "A조": "background-color: #FFE0B2; color: #333;",
    "B조": "background-color: #FFCDD2; color: #333;",
    "C조": "background-color: #BBDEFB; color: #333;"
}
# 하이라이트 진한 톤
STRONG_COLORS = {
    "A조": "background-color: #FB8C00; color: #fff; font-weight: bold; border: 2px solid #333;",
    "B조": "background-color: #E53935; color: #fff; font-weight: bold; border: 2px solid #333;",
    "C조": "background-color: #1E88E5; color: #fff; font-weight: bold; border: 2px solid #333;"
}

def get_shift(target_date):
    base_date = date(2026, 1, 1)
    delta = (target_date - base_date).days
    return ORDER[delta % 3]

# 3. 메인 상단 컨트롤러 (사이드바 대신 사용)
st.title("🏥 성의교정 근무스케줄")

c1, c2, c3 = st.columns([2, 1, 1])
with c1:
    my_shift = st.selectbox("🎯 강조할 조 선택", ["선택 안 함", "A조", "B조", "C조"])
with c2:
    today = datetime.now()
    sel_year = st.number_input("연도", 2020, 2035, today.year)
with c3:
    sel_month = st.number_input("월", 1, 12, today.month)

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
                
                # 하이라이트 여부에 따른 색상 결정
                if highlight != "선택 안 함" and shift == highlight:
                    style = STRONG_COLORS.get(shift, "")
                else:
                    style = BASE_COLORS.get(shift, "")
                
                styles.iloc[r, c] = style
    return styles

# 5. 달력 1열 나열 출력 (12개월)
for i in range(12):
    curr_m = (sel_month + i - 1) % 12 + 1
    curr_y = sel_year + (sel_month + i - 1) // 12
    
    st.write(f"### 📅 {curr_y}년 {curr_m}월")
    
    cal = calendar.monthcalendar(curr_y, curr_m)
    display_data = []
    for week in cal:
        row = [f"{d}\n{get_shift(date(curr_y, curr_m, d))}" if d != 0 else "" for d in week]
        display_data.append(row)
    
    df = pd.DataFrame(display_data, columns=['일', '월', '화', '수', '목', '금', '토'])
    
    # 스타일 적용 및 테이블 출력
    styled_df = df.style.apply(lambda d: style_calendar(df, curr_y, curr_m, my_shift), axis=None)
    st.table(styled_df)
    st.divider()
