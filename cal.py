import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import calendar

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 근무달력", layout="wide")

# 2. CSS 개선 (스크롤/모바일 대응)
st.markdown("""
<style>
.block-container { 
    padding-top: 60px !important; 
    padding-left: 20px !important; 
    padding-right: 20px !important; 
    max-width: 100% !important; 
}

.top-btn {
    position: fixed;
    bottom: 30px;
    right: 20px;
    background-color: #333;
    color: white;
    width: 50px;
    height: 50px;
    border-radius: 25px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    text-decoration: none;
    z-index: 9999;
}

iframe { width: 100% !important; border: none !important; }
</style>

<div id="top-anchor"></div>
<a href="#top-anchor" class="top-btn">▲</a>
""", unsafe_allow_html=True)

# 3. 근무 로직
ORDER = ["B", "C", "A"]
BASE_COLORS = {"A": "#FFE0B2", "B": "#FFCDD2", "C": "#BBDEFB"}
STRONG_COLORS = {"A": "#FB8C00", "B": "#E53935", "C": "#1E88E5"}

def get_shift(dt):
    base = date(2026, 1, 1)
    return ORDER[(dt - base).days % 3]

def is_holiday(dt):
    hols = [
        date(dt.year, 1, 1), date(dt.year, 3, 1), date(dt.year, 5, 5),
        date(dt.year, 6, 6), date(dt.year, 8, 15), date(dt.year, 10, 3),
        date(dt.year, 10, 9), date(dt.year, 12, 25)
    ]
    return dt in hols

# 4. 컨트롤러
st.subheader("🏥 성의교정 근무스케줄")
c1, c2, c3 = st.columns([1,1,1])

with c1:
    offset = st.slider("📅 시작 월", -12, 12, 0)

with c2:
    hi_shift = st.selectbox("🎯 강조 조", ["선택 안 함", "A", "B", "C"])

with c3:
    months = st.selectbox("📊 표시 개월", [3, 6, 12], index=2)

highlight = None if hi_shift == "선택 안 함" else hi_shift

# 5. HTML 생성 (캐싱 적용)
@st.cache_data
def render_calendar(start_dt, highlight, months):
    html = """
    <style>
    body { font-family: 'Noto Sans KR', sans-serif; margin:0; padding:0; }
    .grid { display:grid; gap:15px; padding:10px; }
    @media (min-width:800px){ .grid{grid-template-columns:repeat(3,1fr);} }
    table { width:100%; border-collapse:collapse; table-layout:fixed; }
    th { padding:5px; }
    td { min-height:60px; height:auto; border:1px solid #eee; }
    .sun{color:#d32f2f;} .sat{color:#1976d2;}
    .cell{display:flex; flex-direction:column; height:100%;}
    .date{font-weight:bold; text-align:center;}
    .shift{flex:1; display:flex; align-items:center; justify-content:center; font-weight:bold;}
    </style>
    <div class='grid'>
    """

    curr = start_dt

    for _ in range(months):
        y, m = curr.year, curr.month
        cal = calendar.monthcalendar(y, m)

        html += f"<div><h3 style='text-align:center'>{y}.{m}</h3><table>"
        html += "<tr><th class='sun'>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class='sat'>토</th></tr>"

        for week in cal:
            html += "<tr>"
            for i, d in enumerate(week):
                if d == 0:
                    html += "<td></td>"
                else:
                    dt = date(y, m, d)
                    s = get_shift(dt)
                    is_hi = (highlight == s)

                    if is_hi:
                        bg = STRONG_COLORS[s]
                        txt = "white"
                    else:
                        bg = BASE_COLORS[s]
                        txt = "#333"

                    day_cls = "sun" if (i==0 or is_holiday(dt)) else ("sat" if i==6 else "")

                    html += f"""
                    <td style='background:{bg}'>
                        <div class='cell'>
                            <div class='date {day_cls}'>{d}</div>
                            <div class='shift' style='color:{txt}'>{s}</div>
                        </div>
                    </td>
                    """
            html += "</tr>"

        html += "</table></div>"
        curr += relativedelta(months=1)

    return html + "</div>"

# 6. 실행
start_date = datetime.now().replace(day=1) + relativedelta(months=offset)

components.html(
    render_calendar(start_date, highlight, months),
    height=1200,
    scrolling=True
)
