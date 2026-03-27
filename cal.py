import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, date, timedelta
import calendar

# 1. 페이지 설정 (3x4 레이아웃 최적화)
st.set_page_config(page_title="성의교정 근무달력", layout="wide")

st.markdown("""
    <style>
    /* 상단 타이틀 가려짐 방지: 정확히 20px(약 5mm) 확보 */
    .block-container { padding-top: 20px !important; }
    
    /* 인쇄 전용 설정: 백지 현상 방지 및 레이아웃 유지 */
    @media print {
        @page { size: A4 landscape; margin: 10mm; }
        body { visibility: hidden; }
        .print-area, .print-area * { visibility: visible; }
        .print-area { position: absolute; left: 0; top: 0; width: 100%; }
        .no-print { display: none !important; }
    }
    
    /* 버튼 스타일 */
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; background-color: #f0f2f6; }
    </style>
    """, unsafe_allow_html=True)

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

# 3. 상단 컨트롤러 (인쇄 버튼 상단)
st.markdown("<div class='no-print'>", unsafe_allow_html=True)
st.subheader("🏥 성의교정 근무스케줄")

if st.button("🖨️ PDF 저장 / 인쇄하기"):
    components.html("<script>window.print();</script>", height=0)

c1, c2 = st.columns([1.2, 0.8])
with c1:
    offset = st.slider("📅 조회 시작 범위", -12, 12, 0)
with c2:
    hi_shift = st.selectbox("🎯 강조 조 선택", ["선택 안 함", "A", "B", "C"])
st.markdown("</div>", unsafe_allow_html=True)

# 4. 달력 HTML 생성 함수
def generate_calendar_html(y, m, highlight):
    cal = calendar.monthcalendar(y, m)
    html = f"""
    <div style="font-family: 'Noto Sans KR', sans-serif; border: 1px solid #eee; padding: 5px; border-radius: 8px; background: white; margin-bottom: 10px;">
        <div style="text-align: center; font-weight: bold; font-size: 1.1rem; margin: 5px 0;">{y}년 {m}월</div>
        <table style="width: 100%; border-collapse: collapse; table-layout: fixed; font-size: 11px;">
            <tr>
                <th style="color: #d32f2f; border-bottom: 1px solid #eee;">일</th>
                <th style="border-bottom: 1px solid #eee;">월</th><th style="border-bottom: 1px solid #eee;">화</th>
                <th style="border-bottom: 1px solid #eee;">수</th><th style="border-bottom: 1px solid #eee;">목</th>
                <th style="border-bottom: 1px solid #eee;">금</th>
                <th style="color: #1976d2; border-bottom: 1px solid #eee;">토</th>
            </tr>
    """
    for week in cal:
        html += "<tr>"
        for i, day in enumerate(week):
            if day == 0:
                html += "<td></td>"
            else:
                curr = date(y, m, day)
                s = get_shift(curr)
                day_clr = "#d32f2f" if (i == 0 or is_holiday(curr)) else ("#1976d2" if i == 6 else "#333")
                
                is_hi = (highlight == s)
                bg = STRONG_COLORS[s] if is_hi else BASE_COLORS[s]
                d_bg = STRONG_COLORS[s] if is_hi else "white"
                t_clr = "white" if is_hi else "#333"

                html += f"""
                <td style="background-color: {bg}; border: 1px solid #f2f2f2; height: 45px; vertical-align: top;">
                    <div style="display: flex; flex-direction: column; height: 100%;">
                        <div style="height: 40%; background-color: {d_bg}; color: {t_clr if is_hi else day_clr}; font-weight: 900; font-size: 13px; display: flex; align-items: center; justify-content: center;">
                            {day}
                        </div>
                        <div style="height: 60%; color: {t_clr}; font-weight: 900; font-size: 15px; display: flex; align-items: center; justify-content: center;">
                            {s}
                        </div>
                    </div>
                </td>
                """
        html += "</tr>"
    return html + "</table></div>"

# 5. 인쇄 영역 렌더링 (3x4 레이아웃)
st.markdown("<div class='print-area'>", unsafe_allow_html=True)
start_dt = (datetime.now().replace(day=1) + timedelta(days=31 * offset)).replace(day=1)
months = []
temp_dt = start_dt
for _ in range(12):
    months.append((temp_dt.year, temp_dt.month))
    last_day = calendar.monthrange(temp_dt.year, temp_dt.month)[1]
    temp_dt += timedelta(days=last_day)

for r in range(4):
    cols = st.columns(3)
    for c in range(3):
        idx = r * 3 + c
        y, m = months[idx]
        with cols[c]:
            st.markdown(generate_calendar_html(y, m, hi_shift), unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
