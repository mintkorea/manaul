import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, date, timedelta
import calendar

# 1. 페이지 설정 (중앙 정렬 최적화)
st.set_page_config(page_title="성의교정 근무달력", layout="centered")

# CSS: 상단 여백 확보 및 외부/내부 중앙 정렬
st.markdown("""
    <style>
    /* 상단 여백 8mm(약 32px) + 기본 여백 포함 (총 55px) */
    .block-container { 
        padding-top: 55px !important; 
        padding-left: 0 !important; 
        padding-right: 0 !important; 
        max-width: 1000px !important; /* PC 중앙 정렬 범위 설정 */
        margin: 0 auto !important;
    }
    
    /* 외부 스크롤바 디자인 */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-thumb { background: #ccc; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. 근무 로직 및 색상 정의
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

c1, c2 = st.columns([1.2, 0.8])
with c1:
    offset = st.slider("📅 조회 시작 범위", -12, 12, 0)
with c2:
    hi_shift = st.selectbox("🎯 강조 조 선택", ["선택 안 함", "A", "B", "C"])

# 시작 날짜 계산
start_date = (datetime.now().replace(day=1) + timedelta(days=31 * offset)).replace(day=1)

# 4. 12개월 HTML 생성 함수 (중앙 정렬 강화 버전)
def get_centered_12months_html(start_dt, highlight):
    html_content = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
        body { 
            font-family: 'Noto Sans KR', sans-serif; 
            background-color: white; 
            margin: 0; 
            padding: 0;
            overflow: hidden; /* 내부 스크롤 완벽 제거 */
        }
        .grid-container { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); 
            gap: 20px; 
            padding: 10px;
            margin: 0 auto; /* 그리드 박스를 화면 중앙으로 정렬 */
            max-width: 980px; /* PC 중앙 정렬 범위 제한 */
        }
        /* PC 환경 (넓은 화면) 중앙 정렬 */
        @media (min-width: 1000px) {
            .grid-container { grid-template-columns: repeat(3, 1fr); }
        }
        .cal-box { border: 1px solid #eee; border-radius: 12px; padding: 12px; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
        .month-title { text-align: center; font-weight: 900; font-size: 1.5rem; margin: 10px 0; color: #333; }
        table { width: 100%; border-collapse: collapse; table-layout: fixed; }
        th { border-bottom: 2px solid #eee; padding-bottom: 8px; font-size: 15px; }
        td { border: 1px solid #f2f2f2; height: 65px; vertical-align: top; padding: 0; }
        .sun { color: #d32f2f; } .sat { color: #1976d2; }
        .cell-content { display: flex; flex-direction: column; height: 100%; }
        
        /* 날짜 숫자: 크기 +1pt 키우고 900 볼드 적용 */
        .date-num { 
            height: 40%; display: flex; align-items: center; justify-content: center; 
            font-weight: 900 !important; font-size: 17px !important; 
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
        
        # 다음 달 계산
        last_day = calendar.monthrange(y, m)[1]
        curr += timedelta(days=last_day)
        
    html_content += "</div>"
    return html_content

# 5. 실행 및 렌더링 (height를 5500px로 늘려 12개월 전체 노출 조치)
components.html(get_centered_12months_html(start_date, hi_shift), height=5500, scrolling=False)
