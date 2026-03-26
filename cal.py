import streamlit as st
import pandas as pd
from datetime import datetime, date
import calendar

# 1. 기본 설정
st.set_page_config(page_title="성의교정 근무달력", layout="wide")

st.markdown("""
    <style>
    .stMarkdown h3 { font-size: 1.2rem !important; }
    .stTable { font-size: 16px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. 근무 로직 및 컬러 (파스텔)
ORDER = ["B조", "C조", "A조"]
# 배경색과 글자색 매핑
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
    my_shift = st.selectbox("👉 내 조 하이라이트", ["선택 안 함", "A조", "B조", "C조"])
    st.divider()
    today = datetime.now()
    sel_year = st.number_input("연도", min_value=2020, max_value=2035, value=today.year)
    sel_month = st.slider("시작 월", 1, 12, today.month)

# 4. 스타일 적용 함수 (에러 방지를 위해 구조 단순화)
def style_calendar(df, year, month, highlight):
    styles = pd.DataFrame('', index=df.index, columns=df.columns)
    for r in range(len(df)):
        for c in range(len(df.columns)):
            day_val = df.iloc[r, c]
            if day_val != "":
                day_int = int(day_val.split('\n')[0])
                curr_date = date(year, month, day_int)
                shift = get_shift(curr_date)
                base_style = COLOR_MAP.get(shift, "")
                
                # 하이라이트 처리
                if highlight != "선택 안 함":
                    if shift == highlight:
                        base_style += " font-weight: bold; border: 2.5px solid #333;"
                    else:
                        base_style += " opacity: 0.15;"
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
        
        # 달력 데이터 생성
        cal = calendar.monthcalendar(curr_y, curr_m)
        display_data = []
        for week in cal:
            row = []
            for day in week:
                if day == 0:
                    row.append("")
                else:
                    shift = get_shift(date(curr_y, curr_m, day))
                    row.append(f"{day}\n({shift})")
            display_data.append(row)
        
        df = pd.DataFrame(display_data, columns=['일', '월', '화', '수', '목', '금', '토'])
        
        # 스타일 수동 적용 (Styler 사용)
        styled_df = df.style.apply(lambda d: style_calendar(df, curr_y, curr_m, my_shift), axis=None)
        
        # 출력
        st.table(styled_df)
