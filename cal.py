import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, date, timedelta
import calendar

# 1. 페이지 설정 및 상단 여백 최적화
st.set_page_config(page_title="성의교정 근무달력", layout="centered")

st.markdown("""
    <style>
    .block-container { padding-top: 2rem !important; padding-bottom: 0 !important; }
    .stSelectbox, .stSlider { margin-bottom: 5px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. 근무 로직
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

# 3. 상단 컨트롤러 (위치 교체: 슬라이더가 왼쪽, 강조 선택이 오른쪽)
st.subheader("🏥 성의교정 근무스케줄")

c1, c2 = st.columns([1.2, 0.8]) # 슬라이더 공간을 조금 더 넓게 배분
with c1:
    offset = st.slider("📅 조회 범위", -12, 12, 0) # 위치 변경
with c2:
    hi_shift = st.selectbox("🎯 강조 조", ["선택 안 함", "A", "B", "C"]) # 위치 변경

start_dt = (datetime.now().replace(day=1) + timedelta(days=31 * offset)).replace(day=1)

# 4. 달력 생성 함수 (높이 최적화 유지)
def generate_compact_calendar(y, m, highlight):
    cal = calendar.monthcalendar(y, m)
    
    html = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
        body {{ font-family: 'Noto Sans KR', sans-serif; margin: 0; padding: 0; overflow: hidden; }}
        .month-title {{ text-align: center; font-weight: bold; font-size: 1.8rem; margin: 8px 0; color: #333; }}
        .cal-table {{ width: 100%; border-collapse: collapse; table-layout: fixed; }}
        .cal-table th {{ border: 1px solid #eee; height: 28px; background: #f8f9fa; font-size: 13px; }}
        .cal-table td {{ border: 1px solid #eee; text-align: center; padding: 0; height: 52px !important; }}
        
        .sun-head {{ color: #d32f2f; }}
        .sat-head {{ color: #1976d2; }}
        
        .cell-wrapper {{ display: flex; flex-direction: column; height: 100%; width: 100%; }}
        .date-box {{ height: 38%; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: bold; background-color: white; }}
        .shift-box {{ height: 62%; display: flex; align-items: center; justify-content: center; font-size: 17px; font-weight: 900; }}
        
        .text-sun {{ color: #d32f2f; }}
        .text-sat {{ color: #1976d2; }}
    </style>
    <div class='month-title'>{y}년 {m}월</div>
    <table class='cal-table'>
        <tr><th class='sun-head'>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class='sat-head'>토</th></tr>
    """
    
    for week in cal:
        html += "<tr>"
        for i, day in enumerate(week):
            if day == 0:
                html += "<td></td>"
            else:
                curr = date(y, m, day)
                s = get_shift(curr)
                day_clr = "text-sun" if (i == 0 or is_holiday(curr)) else ("text-sat" if i == 6 else "")
                
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

# 5. 12개월 출력
for n in range(12):
    target = start_dt + timedelta(days=n * 31)
    y, m = target.year, target.month
    
    if n > 0:
        prev_m = (start_dt + timedelta(days=(n-1)*31)).month
        if m == prev_m:
            target += timedelta(days=15)
            y, m = target.year, target.month
            
    # 컴포넌트 높이를 420px로 살짝 더 줄여 한 화면에 더 잘 들어오게 조정
    components.html(generate_compact_calendar(y, m, hi_shift), height=420, scrolling=False)
