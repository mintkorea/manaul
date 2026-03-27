import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, date, timedelta
import calendar

# 1. 페이지 설정 및 상단 여백 (기존보다 5mm 더 추가)
st.set_page_config(page_title="성의교정 근무달력", layout="centered")

st.markdown("""
    <style>
    /* 상단 여백 약 5mm(20px) 추가 증설 */
    .block-container { padding-top: 5.5rem !important; padding-bottom: 0 !important; }
    .stButton { margin-bottom: 10px !important; }
    .stSelectbox, .stSlider { margin-top: -10px !important; }
    
    /* 인쇄 시 컨트롤러 숨기기 */
    @media print {
        .stButton, .stSelectbox, .stSlider, .stHeader, [data-testid="stSidebar"] {
            display: none !important;
        }
        .block-container { padding-top: 0 !important; }
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

# 3. 상단 컨트롤러 레이아웃 (문구 수정 및 버튼 상단 배치)
st.subheader("🏥 성의교정 근무스케줄") # '(1년)' 문구 삭제됨

# 인쇄 버튼을 슬라이더 위로 배치
if st.button("🖨️ PDF 저장 / 인쇄하기"):
    components.html("<script>window.print();</script>", height=0)

c1, c2 = st.columns([1.2, 0.8])
with c1:
    offset = st.slider("📅 조회 범위", -12, 12, 0)
with c2:
    hi_shift = st.selectbox("🎯 강조 조", ["선택 안 함", "A", "B", "C"])

# 시작 날짜 계산
target_date = (datetime.now().replace(day=1) + timedelta(days=31 * offset)).replace(day=1)
y, m = target_date.year, target_date.month

# 4. 달력 HTML 생성 (날짜 폰트 +1 및 Bold 적용)
def generate_calendar_html(y, m, highlight):
    cal = calendar.monthcalendar(y, m)
    html = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
        body {{ font-family: 'Noto Sans KR', sans-serif; margin: 0; padding: 0; overflow: hidden; }}
        .month-title {{ text-align: center; font-weight: bold; font-size: 1.8rem; margin: 10px 0; color: #333; }}
        .cal-table {{ width: 100%; border-collapse: collapse; table-layout: fixed; border: 1px solid #eee; }}
        .cal-table th {{ border: 1px solid #eee; height: 30px; background: #f8f9fa; font-size: 14px; }}
        .cal-table td {{ border: 1px solid #eee; text-align: center; padding: 0; height: 55px !important; }}
        
        .sun-head {{ color: #d32f2f; }} .sat-head {{ color: #1976d2; }}
        
        .cell-wrapper {{ display: flex; flex-direction: column; height: 100%; width: 100%; }}
        
        /* 날짜 폰트 크기 1pt 증가 및 볼드 적용 */
        .date-box {{ 
            height: 40%; display: flex; align-items: center; justify-content: center; 
            font-size: 15px; font-weight: 900 !important; 
        }}
        
        .shift-box {{ height: 60%; display: flex; align-items: center; justify-content: center; font-size: 18px; font-weight: 900; }}
        
        .text-sun {{ color: #d32f2f !important; }}
        .text-sat {{ color: #1976d2 !important; }}
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
                if is_hi:
                    bg, d_bg, txt = STRONG_COLORS[s], STRONG_COLORS[s], "white"
                else:
                    bg, d_bg, txt = BASE_COLORS[s], "white", "#333"

                html += f"""
                <td style="background-color: {bg};">
                    <div class="cell-wrapper">
                        <div class="date-box {day_clr}" style="background-color: {d_bg}; color: {txt if is_hi else ''};">
                            {day}
                        </div>
                        <div class="shift-box" style="color: {txt};">
                            {s}
                        </div>
                    </div>
                </td>
                """
        html += "</tr>"
    html += "</table>"
    return html

# 5. 한 달 출력
components.html(generate_calendar_html(y, m, hi_shift), height=450, scrolling=False)
