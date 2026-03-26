import streamlit as st
import pandas as pd
from datetime import datetime, date
import calendar

# 1. 기본 설정
st.set_page_config(page_title="성의교정 근무달력", layout="wide")

st.markdown("""
    <style>
    .stMarkdown h3 { font-size: 1.2rem !important; }
    /* 테이블 내부 텍스트 가독성 강화 */
    .stTable td { font-size: 16px !important; white-space: pre-wrap !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. 근무 로직 및 컬러 (파스텔 유지)
ORDER = ["B조", "C조", "A조"]
COLOR_MAP = {
    "A조": "background-color: #FFCC80; color: #333;",
    "B조": "background-color: #EF9A9A; color: #333;",
    "C조": "background-color: #90CAF9; color: #333;"
}

def get_shift(target_date):
    base_date = date(2026, 1, 1)
    delta = (target_date - base_date).days
    return ORDER[delta % 3]

# 3. 사이드바 제어
with st.sidebar:
    st.header("⚙️ 옵션")
    my_shift = st.selectbox("👉 내 조 강조하기", ["선택 안 함", "A조", "B조", "C조"])
    st.divider()
    today = datetime.now()
    sel_year = st.number_input("연도", min_value=2020, max_value=2035, value=today.year)
    sel_month = st.slider("시작 월", 1, 12, today.month)

# 4. 스타일 적용 함수 (투명도 제거, 테두리 강조형)
def style_calendar(df, year, month, highlight):
    styles = pd.DataFrame('', index=df.index, columns=df.columns)
    for r in range(len(df)):
        for c in range(len(df.columns)):
            val = df.iloc[r, c]
            if val != "":
                day_int = int(val.split('\n')[0])
                curr_date = date(year, month, day_int)
                shift = get_shift(curr_date)
                
                # 기본 파스텔 색상 적용 (투명도 없음)
                base_style = COLOR_MAP.get(shift, "")
                
                # 본인 조 하이라이트 (강한 테두리와 굵은 글씨)
                if highlight != "선택 안 함" and shift == highlight:
                    base_style += " border: 3px solid #000 !important; font-weight: 900 !important;"
                
                styles.iloc[r, c] = base_style
    return styles

# 5. 메인 화면 출력
st.markdown(f"### 🏥 성의교정 근무스케줄 ({sel_year}년 {sel_month}월부터 1년)")

cols = st.columns(2)
for i in range(12):
    curr_m = (sel_month + i - 1) % 12 + 1
    curr_y = sel_year + (sel_month + i - 1) // 12
    
    with cols[i % 2]:
        st.write(f"#### 📅 {curr_y}년 {curr_m}월")
        
        cal = calendar.monthcalendar(curr_y, curr_m)
        display_data = []
        for week in cal:
            row = [f"{d}\n({get_shift(date(curr_y, curr_m, d))})" if d != 0 else "" for d in week]
            display_data.append(row)
        
        df = pd.DataFrame(display_data, columns=['일', '월', '화', '수', '목', '금', '토'])
        
        # Styler 적용
        styled_df = df.style.apply(lambda d: style_calendar(df, curr_y, curr_m, my_shift), axis=None)
        
        st.table(styled_df)
