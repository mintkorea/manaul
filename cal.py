import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, date, timedelta
import calendar

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 근무달력", layout="wide")

# 상단 여백 및 반응형 레이아웃 설정
st.markdown("""
    <style>
    .block-container { padding-top: 20px !important; }
    /* 모바일/PC 반응형 그리드 설정 */
    .grid-container { 
        display: grid; 
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
        gap: 20px; 
        padding: 10px; 
    }
    @media (min-width: 1000px) {
        .grid-container { grid-template-columns: repeat(3, 1fr); }
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

# 3. 컨트롤러
st.subheader("🏥 성의교정 근무스케줄")

c1, c2 = st.columns([1.2, 0.8])
with c1:
    offset = st.slider("📅 조회 시작 범위", -12, 12, 0)
with c2:
    hi_shift = st.selectbox("🎯 강조 조 선택", ["선택 안 함", "A", "B", "C"])

# 4. 12개월 반응형 HTML 생성
def get_responsive_calendar_html(start_dt, highlight):
    html_content = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
        body { font-family: 'Noto Sans KR', sans-serif; background: white; margin: 0; padding: 0; }
        .grid-container { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); 
            gap: 15px; padding: 10px; 
        }
        @media (min-width: 900px) { .grid-container { grid-template-columns: repeat(3, 1fr); } }
        
        .cal-box { border: 1px solid #eee; border-radius: 10px; padding: 10px; background: white; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        .month-title { text-align: center; font-weight: 900; font-size: 1.4rem; margin-bottom: 10px; color: #333; }
        table { width: 100%; border-collapse: collapse; table-layout: fixed; }
        th { border-bottom: 2px solid #eee; font-size: 14px; padding-bottom: 8px; }
        td { border: 1px solid #f2f2f2; height: 55px; vertical-align: top; padding: 0; }
        .sun { color: #d32f2f; } .sat { color: #1976d2; }
        .cell-content { display: flex; flex-direction: column; height: 100%; }
        /* 날짜 숫자: +1pt, 볼드 900 */
        .date-num { height: 40%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 16px; }
        .shift-name { height: 60%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 19px; }
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

# 5. 최종 렌더링
start_date = (datetime.now().replace(day=1) + timedelta(days=31 * offset)).replace(day=1)
components.html(get_responsive_calendar_html(start_date, hi_shift), height=2500, scrolling=False)
