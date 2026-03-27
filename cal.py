import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, date, timedelta
import calendar

# 1. 페이지 설정 (1년치 3x4 배치를 위해 wide)
st.set_page_config(page_title="성의교정 근무달력", layout="wide")

# 상단 여백 5mm(20px) 확보
st.markdown("<style>.block-container { padding-top: 20px !important; }</style>", unsafe_allow_html=True)

# 2. 근무 및 색상 정의
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

# 3. 상단 컨트롤러 (인쇄 버튼 삭제, 슬라이더 유지)
st.subheader("🏥 성의교정 근무스케줄")

c1, c2 = st.columns([1.2, 0.8])
with c1:
    offset = st.slider("📅 조회 시작 범위(현재 달 기준)", -12, 12, 0)
with c2:
    hi_shift = st.selectbox("🎯 강조 조 선택", ["선택 안 함", "A", "B", "C"])

# 4. 12개월 3x4 그리드 HTML 생성
def get_3x4_html(start_dt, highlight):
    html_content = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
        body { font-family: 'Noto Sans KR', sans-serif; background: white; margin: 0; padding: 0; }
        .grid-container { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; padding: 10px; }
        .cal-box { border: 1px solid #eee; border-radius: 8px; padding: 8px; background: white; }
        .month-title { text-align: center; font-weight: 900; font-size: 1.3rem; margin-bottom: 8px; color: #333; }
        table { width: 100%; border-collapse: collapse; table-layout: fixed; }
        th { border-bottom: 2px solid #eee; font-size: 14px; padding-bottom: 5px; }
        td { border: 1px solid #f2f2f2; height: 50px; vertical-align: top; padding: 0; }
        .sun { color: #d32f2f; } .sat { color: #1976d2; }
        .cell-content { display: flex; flex-direction: column; height: 100%; }
        /* 날짜 숫자: +1pt 키우고 900 볼드 */
        .date-num { height: 40%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 15px; }
        .shift-name { height: 60%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 17px; }
        @media print { .grid-container { gap: 10px; } }
    </style>
    <div class="grid-container">
    """
    
    curr = start_dt
    for _ in range(12):
        y, m = curr.year, curr.month
        cal = calendar.monthcalendar(y, m)
        html_content += f"<div class='cal-box'><div class='month-title'>{y}년 {m}월</div><table>"
        html_content += "<tr><th class='sun'>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class='sat'>토</th></tr>"
        for week in cal:
            html_content += "<tr>"
            for i, day in enumerate(week):
                if day == 0: html_content += "<td></td>"
                else:
                    d_obj = date(y, m, day)
                    s = get_shift(d_obj)
                    day_clr = "sun" if (i == 0 or is_holiday(d_obj)) else ("sat" if i == 6 else "")
                    is_hi = (highlight == s)
                    bg = STRONG_COLORS[s] if is_hi else BASE_COLORS[s]
                    d_bg = STRONG_COLORS[s] if is_hi else "white"
                    txt = "white" if is_hi else "#333"
                    html_content += f"""
                    <td style="background-color: {bg};">
                        <div class="cell-content">
                            <div class="date-num {day_clr if not is_hi else ''}" style="background-color: {d_bg}; color: {txt if is_hi else ''};">{day}</div>
                            <div class="shift-name" style="color: {txt};">{s}</div>
                        </div>
                    </td>"""
            html_content += "</tr>"
        html_content += "</table></div>"
        last_day = calendar.monthrange(y, m)[1]
        curr += timedelta(days=last_day)
    return html_content + "</div>"

# 5. 실행
start_date = (datetime.now().replace(day=1) + timedelta(days=31 * offset)).replace(day=1)
components.html(get_3x4_html(start_date, hi_shift), height=1600)
