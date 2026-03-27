import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, date, timedelta
import calendar

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 근무달력", layout="centered")

# CSS: 화면에는 한 달만, 인쇄 시에는 전체(3x4)를 출력하는 로직
st.markdown("""
    <style>
    /* 상단 여백 5mm(약 20px) 확보 */
    .block-container { padding-top: 20px !important; }
    
    /* 인쇄 전용 설정 */
    @media print {
        @page { size: A4 landscape; margin: 10mm; }
        body * { visibility: hidden; }
        .print-only, .print-only * { visibility: visible; }
        .print-only { 
            position: absolute; left: 0; top: 0; width: 100%; 
            display: grid !important; grid-template-columns: repeat(3, 1fr); gap: 10px;
        }
        .no-print { display: none !important; }
    }
    
    /* 화면용 스타일 */
    .screen-only { display: block; }
    .print-only { display: none; }
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

# 3. 상단 컨트롤러 (화면에만 보임)
st.subheader("🏥 성의교정 근무스케줄")

if st.button("🖨️ PDF 저장 / 1년치 인쇄하기"):
    components.html("<script>window.print();</script>", height=0)

c1, c2 = st.columns([1.2, 0.8])
with c1:
    offset = st.slider("📅 조회 범위(현재 달 기준)", -12, 12, 0)
with c2:
    hi_shift = st.selectbox("🎯 강조 조 선택", ["선택 안 함", "A", "B", "C"])

# 4. 달력 HTML 생성 함수 (날짜 폰트 +1pt & Bold 적용)
def generate_cal_html(y, m, highlight, is_print=False):
    cal = calendar.monthcalendar(y, m)
    font_size = "11px" if is_print else "14px"
    cell_height = "45px" if is_print else "60px"
    
    html = f"""
    <div style="font-family: 'Noto Sans KR', sans-serif; border: 1px solid #eee; padding: 5px; border-radius: 8px; background: white;">
        <div style="text-align: center; font-weight: bold; font-size: 1.2rem; margin-bottom: 5px;">{y}년 {m}월</div>
        <table style="width: 100%; border-collapse: collapse; table-layout: fixed; font-size: {font_size};">
            <tr style="border-bottom: 1px solid #eee;">
                <th style="color: #d32f2f;">일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th style="color: #1976d2;">토</th>
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
                <td style="background-color: {bg}; border: 1px solid #f2f2f2; height: {cell_height}; vertical-align: top;">
                    <div style="display: flex; flex-direction: column; height: 100%;">
                        <div style="height: 40%; background-color: {d_bg}; color: {t_clr if is_hi else day_clr}; font-weight: 900; font-size: 1.1em; display: flex; align-items: center; justify-content: center;">
                            {day}
                        </div>
                        <div style="height: 60%; color: {t_clr}; font-weight: 900; font-size: 1.3em; display: flex; align-items: center; justify-content: center;">
                            {s}
                        </div>
                    </div>
                </td>
                """
        html += "</tr>"
    return html + "</table></div>"

# 5. 화면 출력 (선택한 한 달만 크게)
target_dt = (datetime.now().replace(day=1) + timedelta(days=31 * offset)).replace(day=1)
st.markdown("<div class='screen-only'>", unsafe_allow_html=True)
st.markdown(generate_cal_html(target_dt.year, target_dt.month, hi_shift), unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# 6. 인쇄용 출력 (3x4 레이아웃, 화면에선 숨김)
st.markdown("<div class='print-only'>", unsafe_allow_html=True)
print_start = target_dt # 슬라이더로 선택한 달부터 12개월 출력
for i in range(12):
    curr_y, curr_m = print_start.year, print_start.month
    st.markdown(generate_cal_html(curr_y, curr_m, hi_shift, is_print=True), unsafe_allow_html=True)
    # 다음 달 계산
    last_day = calendar.monthrange(curr_y, curr_m)[1]
    print_start += timedelta(days=last_day)
st.markdown("</div>", unsafe_allow_html=True)
