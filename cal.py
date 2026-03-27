import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, date, timedelta
import calendar

# 1. 페이지 설정 (3x4 배치를 위해 wide)
st.set_page_config(page_title="성의교정 근무달력", layout="wide")

st.markdown("""
    <style>
    /* 상단 여백: 너무 넓지 않게 적절히 조정 */
    .block-container { padding-top: 2.8rem !important; }
    
    /* 인쇄 시 불필요한 UI 숨기기 */
    @media print {
        .no-print, .stButton, .stSlider, .stSelectbox, header { display: none !important; }
        .block-container { padding: 0 !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 근무 및 색상 로직
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

# 3. 상단 컨트롤러 (인쇄 버튼이 맨 위)
st.subheader("🏥 성의교정 근무스케줄")

# PDF 저장/인쇄 버튼 (클릭 시 브라우저 인쇄창 호출)
if st.button("🖨️ PDF 저장 / 인쇄하기"):
    components.html("<script>window.print();</script>", height=0)

c1, c2 = st.columns([1.2, 0.8])
with c1:
    offset = st.slider("📅 조회 시작 범위", -12, 12, 0)
with c2:
    hi_shift = st.selectbox("🎯 강조 조 선택", ["선택 안 함", "A", "B", "C"])

# 시작 날짜 계산
start_dt = (datetime.now().replace(day=1) + timedelta(days=31 * offset)).replace(day=1)

# 4. 달력 HTML 생성 (날짜 +1pt & Bold 적용)
def generate_calendar_html(y, m, highlight):
    cal = calendar.monthcalendar(y, m)
    html = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
        .cal-wrapper {{ font-family: 'Noto Sans KR', sans-serif; border: 1px solid #eee; padding: 5px; border-radius: 8px; background: white; }}
        .month-title {{ text-align: center; font-weight: bold; font-size: 1.2rem; margin: 8px 0; }}
        .cal-table {{ width: 100%; border-collapse: collapse; table-layout: fixed; font-size: 11px; }}
        .cal-table th {{ border-bottom: 2px solid #eee; height: 25px; }}
        .cal-table td {{ border: 1px solid #f2f2f2; text-align: center; height: 48px !important; }}
        
        .sun {{ color: #d32f2f; }} .sat {{ color: #1976d2; }}
        
        .cell-content {{ display: flex; flex-direction: column; height: 100%; width: 100%; }}
        /* 날짜 폰트 1pt 크게 + 볼드 */
        .date-num {{ 
            height: 40%; display: flex; align-items: center; justify-content: center; 
            font-size: 14px; font-weight: 900 !important; 
        }}
        .shift-name {{ height: 60%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 16px; }}
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
                is_selected = (highlight == s)
                
                bg = STRONG_COLORS[s] if is_selected else BASE_COLORS[s]
                d_bg = STRONG_COLORS[s] if is_selected else "white"
                txt = "white" if is_selected else "#333"

                html += f"""
                <td style="background-color: {bg};">
                    <div class='cell-content'>
                        <div class='date-num {day_class if not is_selected else ""}' 
                             style='background-color: {date_bg}; color: {txt if is_selected else ""};'>
                            {day}
                        </div>
                        <div class='shift-name' style='color: {txt};'>
                            {s}
                        </div>
                    </div>
                </td>
                """
        html += "</tr>"
    return html + "</table></div>"

# 5. 3x4 레이아웃 (12개월) 출력
months_list = []
temp_dt = start_dt
for _ in range(12):
    months_list.append((temp_dt.year, temp_dt.month))
    last_day = calendar.monthrange(temp_dt.year, temp_dt.month)[1]
    temp_dt += timedelta(days=last_day)

for i in range(0, 12, 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < 12:
            y, m = months_list[i + j]
            with cols[j]:
                st.components.v1.html(generate_calendar_html(y, m, hi_shift), height=340)
