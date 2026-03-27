import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, date, timedelta
import calendar

# 1. 페이지 설정 및 인쇄 전용 CSS
st.set_page_config(page_title="성의교정 근무달력", layout="wide") # 3열 배치를 위해 wide 모드 사용

st.markdown("""
    <style>
    .block-container { padding-top: 2rem !important; }
    
    /* 인쇄 시 버튼 및 컨트롤러 숨기기 */
    @media print {
        .no-print { display: none !important; }
        .stButton { display: none !important; }
        .block-container { padding: 0 !important; }
    }
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

# 3. 상단 컨트롤러 (슬라이더와 강조 선택 위치 교체)
st.subheader("🏥 성의교정 근무스케줄 (1년)")

with st.container():
    c1, c2 = st.columns([1.2, 0.8])
    with c1:
        offset = st.slider("📅 조회 시작 범위", -12, 12, 0)
    with c2:
        hi_shift = st.selectbox("🎯 강조 조 선택", ["선택 안 함", "A", "B", "C"])

# 슬라이더 다음 줄에 PDF 출력(인쇄) 버튼 배치
if st.button("🖨️ PDF로 저장 / 인쇄하기"):
    js = "window.print();"
    st.components.v1.html(f"<script>{js}</script>", height=0)

# 시작 날짜 설정
start_dt = (datetime.now().replace(day=1) + timedelta(days=30 * offset)).replace(day=1)

# 4. 달력 생성 함수 (3x4에 맞게 크기 최적화)
def generate_calendar_html(y, m, highlight):
    cal = calendar.monthcalendar(y, m)
    html = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
        .cal-wrapper {{ font-family: 'Noto Sans KR', sans-serif; margin-bottom: 20px; border: 1px solid #ddd; padding: 5px; border-radius: 5px; }}
        .month-title {{ text-align: center; font-weight: bold; font-size: 1.3rem; margin: 5px 0; color: #333; }}
        .cal-table {{ width: 100%; border-collapse: collapse; table-layout: fixed; font-size: 11px; }}
        .cal-table th {{ border: 1px solid #eee; height: 22px; background: #f8f9fa; }}
        .cal-table td {{ border: 1px solid #eee; text-align: center; height: 40px !important; position: relative; }}
        .sun {{ color: #d32f2f; }} .sat {{ color: #1976d2; }}
        .day-num {{ font-weight: bold; margin-bottom: 2px; }}
        .shift-name {{ font-weight: 900; font-size: 14px; }}
    </style>
    <div class='cal-wrapper'>
        <div class='month-title'>{y}년 {m}월</div>
        <table class='cal-table'>
            <tr><th class='sun'>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class='sat'>토</th></tr>
    """
    for week in cal:
        html += "<tr>"
        for i, day in enumerate(week):
            if day == 0:
                html += "<td></td>"
            else:
                curr = date(y, m, day)
                s = get_shift(curr)
                day_class = "sun" if (i == 0 or is_holiday(curr)) else ("sat" if i == 6 else "")
                is_hi = (highlight == s)
                bg = STRONG_COLORS[s] if is_hi else BASE_COLORS[s]
                txt = "white" if is_hi else "#333"
                html += f"""
                <td style="background-color: {bg}; color: {txt};">
                    <div class='day-num {day_class if not is_hi else ""}'>{day}</div>
                    <div class='shift-name'>{s}</div>
                </td>
                """
        html += "</tr>"
    return html + "</table></div>"

# 5. 3x4 레이아웃 출력 (12개월)
months_data = []
for n in range(12):
    # 월 계산 로직 (간소화)
    current_month_dt = start_dt + timedelta(days=n*31)
    y, m = current_month_dt.year, current_month_dt.month
    if n > 0 and m == months_data[-1][1]: # 중복 달 방지
        current_month_dt += timedelta(days=15)
        y, m = current_month_dt.year, current_month_dt.month
    months_data.append((y, m))

# 3개씩 4줄 출력
for i in range(0, 12, 3):
    cols = st.columns(3)
    for j in range(3):
        idx = i + j
        if idx < 12:
            y, m = months_data[idx]
            with cols[j]:
                components.html(generate_calendar_html(y, m, hi_shift), height=320)
