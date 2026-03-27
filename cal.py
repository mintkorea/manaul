import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, date, timedelta
import calendar

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 근무달력", layout="centered")

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

# 3. 상단 컨트롤러
st.subheader("🏥 성의교정 근무스케줄")

if st.button("🖨️ PDF 저장 / 1년치 인쇄하기"):
    components.html("<script>window.print();</script>", height=0)

c1, c2 = st.columns([1.2, 0.8])
with c1:
    offset = st.slider("📅 조회 범위(현재 달 기준)", -12, 12, 0)
with c2:
    hi_shift = st.selectbox("🎯 강조 조 선택", ["선택 안 함", "A", "B", "C"])

# 4. 전체 HTML 패키지 생성 (화면용 1달 + 인쇄용 12달 통합)
def get_final_html(target_dt, highlight):
    # 공통 스타일
    style = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
        body {{ font-family: 'Noto Sans KR', sans-serif; background: white; margin: 0; padding: 0; }}
        .cal-box {{ border: 1px solid #eee; border-radius: 8px; padding: 5px; background: white; margin-bottom: 10px; }}
        .month-title {{ text-align: center; font-weight: bold; font-size: 1.2rem; margin: 5px 0; }}
        table {{ width: 100%; border-collapse: collapse; table-layout: fixed; }}
        th {{ border-bottom: 1px solid #eee; font-size: 13px; padding-bottom: 5px; }}
        td {{ border: 1px solid #f2f2f2; height: 60px; vertical-align: top; padding: 0; }}
        .sun {{ color: #d32f2f; }} .sat {{ color: #1976d2; }}
        .cell-content {{ display: flex; flex-direction: column; height: 100%; }}
        .date-num {{ height: 40%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 15px; }}
        .shift-name {{ height: 60%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 18px; }}
        
        /* 인쇄 시 레이아웃 제어 */
        @media print {{
            @page {{ size: A4 landscape; margin: 10mm; }}
            .screen-only {{ display: none !important; }}
            .print-only {{ display: grid !important; grid-template-columns: repeat(3, 1fr); gap: 10px; visibility: visible; }}
            td {{ height: 45px !important; }}
            .date-num {{ font-size: 13px !important; }}
            .shift-name {{ font-size: 16px !important; }}
        }}
        .print-only {{ display: none; }}
    </style>
    """

    def make_table(y, m):
        cal = calendar.monthcalendar(y, m)
        t_html = f"<div class='cal-box'><div class='month-title'>{y}년 {m}월</div><table>"
        t_html += "<tr><th class='sun'>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class='sat'>토</th></tr>"
        for week in cal:
            t_html += "<tr>"
            for i, day in enumerate(week):
                if day == 0: t_html += "<td></td>"
                else:
                    curr = date(y, m, day)
                    s = get_shift(curr)
                    day_clr = "sun" if (i == 0 or is_holiday(curr)) else ("sat" if i == 6 else "")
                    is_hi = (highlight == s)
                    bg = STRONG_COLORS[s] if is_hi else BASE_COLORS[s]
                    d_bg = STRONG_COLORS[s] if is_hi else "white"
                    txt = "white" if is_hi else "#333"
                    t_html += f"""
                    <td style="background-color: {bg};">
                        <div class="cell-content">
                            <div class="date-num {day_clr if not is_hi else ''}" style="background-color: {d_bg}; color: {txt if is_hi else ''};">{day}</div>
                            <div class="shift-name" style="color: {txt};">{s}</div>
                        </div>
                    </td>"""
            t_html += "</tr>"
        return t_html + "</table></div>"

    # 화면용 (1달)
    screen_html = f"<div class='screen-only'>{make_table(target_dt.year, target_dt.month)}</div>"
    
    # 인쇄용 (12달)
    print_html = "<div class='print-only'>"
    p_dt = target_dt
    for _ in range(12):
        print_html += make_table(p_dt.year, p_dt.month)
        last_day = calendar.monthrange(p_dt.year, p_dt.month)[1]
        p_dt += timedelta(days=last_day)
    print_html += "</div>"

    return style + screen_html + print_html

# 5. 최종 렌더링
target_date = (datetime.now().replace(day=1) + timedelta(days=31 * offset)).replace(day=1)
components.html(get_final_html(target_date, hi_shift), height=1200, scrolling=True)
