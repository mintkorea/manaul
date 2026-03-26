import streamlit as st
import pandas as pd
from datetime import datetime, date
import calendar

# 1. 기본 설정 및 스타일
st.set_page_config(page_title="성의교정 근무달력", layout="wide")

st.markdown("""
    <style>
    /* 타이틀 및 텍스트 크기 확대 */
    .stMarkdown h3 { font-size: 20px !important; }
    .stMarkdown p { font-size: 16px !important; }
    /* 테이블 가독성 향상 */
    table { font-size: 16px !important; text-align: center !important; }
    th { background-color: #f0f2f6 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. 근무 로직 및 파스텔 컬러
ORDER = ["B조", "C조", "A조"]
PASTEL_COLORS = {
    "A조": "background-color: #FFCC80; color: #333;",
    "B조": "background-color: #EF9A9A; color: #333;",
    "C조": "background-color: #90CAF9; color: #333;"
}

def get_shift_info(target_date):
    base_date = date(2026, 1, 1)
    delta = (target_date - base_date).days
    return ORDER[delta % 3]

# 3. 사이드바 제어
with st.sidebar:
    st.header("⚙️ 옵션")
    my_shift = st.selectbox("👉 내 조 선택 (하이라이트)", ["선택 안 함", "A조", "B조", "C조"])
    st.divider()
    today = datetime.now()
    sel_year = st.number_input("조회 연도", min_value=2020, max_value=2035, value=today.year)
    sel_month = st.slider("시작 월", 1, 12, today.month)

# 4. 달력 데이터 생성 함수
def make_cal_df(year, month):
    cal = calendar.monthcalendar(year, month)
    df = pd.DataFrame(cal, columns=['일', '월', '화', '수', '목', '금', '토'])
    return df

def apply_style(val, year, month, highlight):
    if val == 0:
        return ""
    curr_date = date(year, month, val)
    shift = get_shift_info(curr_date)
    style = PASTEL_COLORS[shift]
    
    # 하이라이트 로직
    if highlight != "선택 안 함":
        if shift == highlight:
            style += " font-weight: bold; border: 3px solid #333 !important;"
        else:
            style += " opacity: 0.2;"
    
    return style

# 5. 메인 화면 출력
st.write(f"### 🏥 성의교정 근무스케줄 ({sel_year}년 {sel_month}월부터 1년)")

cols = st.columns(2)
for i in range(12):
    curr_m = (sel_month + i - 1) % 12 + 1
    curr_y = sel_year + (sel_month + i - 1) // 12
    
    with cols[i % 2]:
        st.write(f"#### 📅 {curr_y}년 {curr_m}월")
        df = make_cal_df(curr_y, curr_m)
        
        # 데이터프레임에 근무 조 표시 및 스타일 적용
        styled_df = df.style.apply(lambda x: [
            apply_style(v, curr_y, curr_m, my_shift) for v in x
        ], axis=None)
        
        # 0(빈 날짜)을 공백으로 표시
        display_df = df.copy().astype(str).replace('0', '')
        for col in df.columns:
            for idx in df.index:
                day_val = df.at[idx, col]
                if day_val != 0:
                    shift = get_shift_info(date(curr_y, curr_m, day_val))
                    display_df.at[idx, col] = f"{day_val}\n({shift})"

        st.table(display_df.style.apply(lambda x: [
            apply_style(v, curr_y, curr_m, my_shift) for v in df.values.flatten()
        ], axis=None).set_table_styles([
            {'selector': 'td', 'props': [('height', '60px'), ('width', '14%')]}
        ]))
