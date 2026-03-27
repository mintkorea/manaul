
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, date, timedelta
import calendar

# 1. 페이지 설정 (3x4 레이아웃)
st.set_page_config(page_title="성의교정 근무달력", layout="wide")

# 상단 여백 5mm 확보 및 기본 스타일
st.markdown("""
    <style>
    .block-container { padding-top: 20px !important; }
    .no-print { margin-bottom: 10px; }
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

# 3. 컨트롤러 영역 (인쇄 버튼 포함)
st.subheader("🏥 성의교정 근무스케줄")

col_btn, col_empty = st.columns([1, 2])
with col_btn:
    if st.button("🖨️ PDF 저장 / 인쇄하기"):
        components.html("<script>window.print();</script>", height=0)

c1, c2 = st.columns([1.2, 0.8])
with c1:
    offset = st.slider("📅 조회 시작 범위", -12, 12, 0)
with c2:
    hi_shift = st.selectbox("🎯 강조 조 선택", ["선택 안 함", "A", "B", "C"])

# 4. 달력 생성 함수 (HTML 노출 방지를 위해 내부에 모든 CSS 포함)
def get_calendar_full_html(months_data, highlight):
    html_content = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
        body { font-family: 'Noto Sans KR', sans-serif; background-color: white; margin: 0; padding: 0; }
        .grid-container { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; padding: 10px; }
        .cal-box { border: 1px solid #eee; border-radius: 8px; padding: 5px; background: white; }
        .month-title { text-align: center; font-weight: bold; font-size: 1.1rem; margin-bottom: 5px; }
        table { width: 100%; border-collapse: collapse; table-layout: fixed; font-size: 11px; }
        th { border-bottom: 1px solid #eee; padding-bottom: 3px; }
        td { border: 1px solid #f2f2f2; height: 45px; vertical-align: top; padding: 0; position: relative; }
        .cell-content { display: flex; flex-direction: column; height: 100%; }
        .date-num { height: 40%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 13px; }
        .shift-name { height: 60%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 15px; }
        .sun { color: #d32f2f; } .sat { color: #1976d2; }
        @media print { .grid-container { gap: 5px; } }
    </style>
    <div class="grid-container">
    """
    
    for y, m in months_data:
        cal = calendar.monthcalendar(y, m)
        html_content += f"<div class='cal-box'><div class='month-title'>{y}년 {m}월</div><table>"
        html_content += "<tr><th class='sun'>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class='sat'>토</th></tr>"
        
        for week in cal:
            html_content += "<tr>"
            for i, day in enumerate(week):
                if day == 0:
                    html_content += "<td></td>"
                else:
                    curr = date(y, m, day)
                    s = get_shift(curr)
                    day_clr = "sun" if (i == 0 or is_holiday(curr)) else ("sat" if i == 6 else "")
                    is_hi = (highlight == s)
                    
                    bg = STRONG_COLORS[s] if is_hi else BASE_COLORS[s]
                    d_bg = STRONG_COLORS[s] if is_hi else "white"
                    t_clr = "white" if is_hi else "#333"
                    
                    html_content += f"""
                    <td style="background-color: {bg};">
                        <div class="cell-content">
                            <div class="date-num {day_clr if not is_hi else ''}" style="background-color: {d_bg}; color: {t_clr if is_hi else ''};">
                                {day}
                            </div>
                            <div class="shift-name" style="color: {t_clr};">
                                {s}
                            </div>
                        </div>
                    </td>
                    """
            html_content += "</tr>"
        html_content += "</table></div>"
    
    html_content += "</div>"
    return html_content

# 5. 12개월 데이터 준비 및 렌더링
start_dt = (datetime.now().replace(day=1) + timedelta(days=31 * offset)).replace(day=1)
months_to_show = []
temp_dt = start_dt
for _ in range(12):
    months_to_show.append((temp_dt.year, temp_dt.month))
    last_day = calendar.monthrange(temp_dt.year, temp_dt.month)[1]
    temp_dt += timedelta(days=last_day)

# 한 번의 components.html 호출로 3x4 전체를 렌더링 (코드 노출 방지)
components.html(get_calendar_full_html(months_to_show, hi_shift), height=1400, scrolling=False)
