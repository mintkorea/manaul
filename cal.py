import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 근무달력", layout="wide")

# 2. CSS (스크롤 문제 제거)
st.markdown("""
<style>
.block-container { padding-top:60px; }
iframe { width:100% !important; border:none !important; }
</style>
""", unsafe_allow_html=True)

# 3. 근무 로직
ORDER = ["B","C","A"]
STRONG_COLORS = {"A":"#FB8C00","B":"#E53935","C":"#1E88E5"}

def get_shift(dt):
    base = date(2026,1,1)
    return ORDER[(dt-base).days % 3]

def is_holiday(dt):
    hols = [
        date(dt.year,1,1), date(dt.year,3,1), date(dt.year,5,5),
        date(dt.year,6,6), date(dt.year,8,15), date(dt.year,10,3),
        date(dt.year,10,9), date(dt.year,12,25)
    ]
    return dt in hols

# 4. 컨트롤
st.subheader("🏥 성의교정 근무스케줄")
c1,c2 = st.columns(2)

with c1:
    offset = st.slider("📅 시작 월", -12, 12, 0)

with c2:
    hi_shift = st.selectbox("🎯 강조 조", ["선택 안 함","A","B","C"])

highlight = None if hi_shift=="선택 안 함" else hi_shift

# 5. HTML
@st.cache_data
def render(start_dt, highlight):
    html = """
    <style>
    body { margin:0; padding:0; }
    .grid { display:grid; gap:15px; padding:10px; }
    @media(min-width:800px){ .grid{grid-template-columns:repeat(3,1fr);} }
    table { width:100%; border-collapse:collapse; table-layout:fixed; }
    td { height:70px; border:1px solid #eee; background:white; }
    .sun{color:#d32f2f;} .sat{color:#1976d2;}
    .cell{display:flex; flex-direction:column; height:100%;}
    .date{font-weight:bold; text-align:center;}
    .shift{flex:1; display:flex; align-items:center; justify-content:center; font-size:26px; font-weight:900;}
    </style>
    <div class='grid'>
    """

    curr = start_dt

    for _ in range(12):  # 🔥 12개월 고정
        y,m = curr.year, curr.month
        cal = calendar.monthcalendar(y,m)

        html += f"<div><h3 style='text-align:center'>{y}.{m}</h3><table>"
        html += "<tr><th class='sun'>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class='sat'>토</th></tr>"

        for week in cal:
            html += "<tr>"
            for i,d in enumerate(week):
                if d==0:
                    html += "<td></td>"
                else:
                    dt = date(y,m,d)
                    s = get_shift(dt)
                    is_hi = (highlight==s)

                    bg = STRONG_COLORS[s] if is_hi else "white"
                    txt = "white" if is_hi else "#333"

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
    render(start_date, highlight),
    height=1400,
    scrolling=True  # 🔥 전체 하나만 스크롤
)
