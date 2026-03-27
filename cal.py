import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, date, timedelta
import calendar

# 1. 페이지 설정 (레이아웃 최적화)
st.set_page_config(page_title="성의교정 근무달력", layout="wide")

# CSS: 상단 여백 8mm(55px) 및 좌우 균등 정렬
st.markdown("""
    <style>
    .block-container { 
        padding-top: 55px !important; 
        padding-left: 0 !important; 
        padding-right: 0 !important; 
        max-width: 100% !important; 
        display: flex;
        justify-content: center;
    }
    iframe { 
        width: 100vw !important; 
        margin: 0 auto !important;
    }
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

# 3. 컨트롤러 영역 (중앙 정렬박스 안으로 배치)
col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    st.subheader("🏥 성의교정 근무스케줄")
    c1, c2 = st.columns([1, 1])
    with c1:
        offset = st.slider("📅 조회 시작 범위", -12, 12, 0)
    with c2:
        hi_shift = st.selectbox("🎯 강조 조 선택", ["선택 안 함", "A", "B", "C"])

# 4. 12개월 HTML (테두리 제거 및 높이 최적화)
def get_final_calendar_html(start_dt, highlight):
    html_content = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
        body { 
            font-family: 'Noto Sans KR', sans-serif; 
            background-color: white; margin: 0; padding: 0;
            overflow: hidden; 
        }
        .grid-container { 
            display: grid; 
            grid-template-columns: 1fr; 
            gap: 0px; /* 월간 간격 최소화 */
            padding: 0;
            width: 100%;
        }
        @media (min-width: 800px) {
            .grid-container { 
                grid-template-columns: repeat(3, 1fr); 
                gap: 20px;
                padding: 10px;
            }
        }
        .cal-box { 
            border: none; /* 테두리 제거 */
            background: white; 
            width: 100%; 
            margin: 0 auto 30px auto; /* 아래쪽 여백만 유지 */
        }
        .month-title { text-align: center; font-weight: 900; font-size: 1.6rem; margin: 15px 0; color: #222; }
        table { width: 100%; border-collapse: collapse; table-layout: fixed; }
        th { border-bottom: 2px solid #eee; padding-bottom: 10px; font-size: 15px; }
        /* 한 화면에 한 달이 들어오도록 높이 미세 조정 */
        td { border: 1px solid #f8f8f8; height: 62px; vertical-align: top; padding: 0; }
        .sun { color: #d32f2f; } .sat { color: #1976d2; }
        .cell-content { display: flex; flex-direction: column; height: 100%; }
        .date-num { 
            height: 40%; display: flex; align-items: center; justify-content: center; 
            font-weight: 900; font-size: 17px; 
        }
        .shift-name { height: 60%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 20px; }
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
                    curr_d = date(y, m, day)
                    s = get_shift(curr_d)
                    day_clr = "sun" if (i == 0 or is_holiday(curr_d)) else ("sat" if i == 6 else "")
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
# 높이를 여유 있게 설정하여 12개월 전체 노출 보장
components.html(get_final_calendar_html(start_date, hi_shift), height=6000, scrolling=False)
