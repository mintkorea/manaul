import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, date, timedelta
import calendar

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 근무달력", layout="wide")

# 2. CSS: 여백 및 플로팅 버튼, 스크롤 최적화
st.markdown("""
    <style>
    /* 상단/좌우 베젤 여백 확보 */
    .block-container { 
        padding-top: 70px !important; 
        padding-left: 25px !important; 
        padding-right: 25px !important; 
        max-width: 100% !important; 
    }
    
    /* 컨트롤러(슬라이더, 셀렉트박스) 스타일 */
    .stSlider, .stSelectbox {
        margin-bottom: 20px !important;
    }

    /* 플로팅 탑 버튼 */
    .top-btn {
        position: fixed;
        bottom: 30px;
        right: 25px;
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
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        border: 2px solid white;
    }
    
    /* 아이프레임 테두리 및 스크롤 제거 (통합 스크롤용) */
    iframe { width: 100% !important; border: none !important; }
    </style>
    
    <div id="top-anchor"></div>
    <a href="#top-anchor" class="top-btn">▲</a>
    """, unsafe_allow_html=True)

# 3. 근무 로직 및 색상
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

# 4. 상단 컨트롤러
st.subheader("🏥 성의교정 근무스케줄")
c1, c2 = st.columns([1, 1])
with c1:
    # 기준 시점 선택 (현재 달 기준 +- 12개월)
    offset = st.slider("📅 조회 시작 달 설정 (현재 기준)", -12, 12, 0)
with c2:
    hi_shift = st.selectbox("🎯 강조할 근무 조 선택", ["선택 안 함", "A", "B", "C"])

# 기준 날짜 계산 (슬라이더 값 적용)
base_start_date = (datetime.now().replace(day=1) + timedelta(days=31 * offset)).replace(day=1)

# 5. 12개월 동적 생성 HTML
def get_dynamic_calendar_html(start_dt, highlight):
    html_content = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
        body { font-family: 'Noto Sans KR', sans-serif; background-color: white; margin: 0; padding: 0; }
        .grid-container { 
            display: grid; 
            grid-template-columns: 1fr; 
            gap: 10px;
            padding: 0 5px;
            box-sizing: border-box;
            width: 100%;
        }
        @media (min-width: 800px) {
            .grid-container { grid-template-columns: repeat(3, 1fr); gap: 25px; padding: 20px; }
        }
        .cal-box { border: none; background: white; width: 100%; margin-bottom: 25px; }
        .month-title { text-align: center; font-weight: 900; font-size: 1.6rem; margin: 15px 0; color: #222; }
        table { width: 100%; border-collapse: collapse; table-layout: fixed; }
        th { border-bottom: 2px solid #eee; padding-bottom: 10px; font-size: 14px; }
        td { border: 1px solid #f2f2f2; height: 62px; vertical-align: top; padding: 0; }
        .sun { color: #d32f2f; } .sat { color: #1976d2; }
        .cell-content { display: flex; flex-direction: column; height: 100%; }
        /* 날짜 배경 흰색 고정 */
        .date-num { height: 40%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 16px; background-color: #FFFFFF; }
        .date-num.hi { color: white !important; }
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
                    is_hi = (highlight == s)
                    
                    day_clr = "sun" if (i == 0 or is_holiday(curr_d)) else ("sat" if i == 6 else "")
                    
                    # 날짜 배경 로직 (하이라이트 시에만 색상 적용)
                    d_bg = STRONG_COLORS[s] if is_hi else "#FFFFFF"
                    d_txt = "white" if is_hi else ""
                    
                    # 근무 조 배경 및 텍스트 로직
                    s_bg = STRONG_COLORS[s] if is_hi else BASE_COLORS[s]
                    s_txt = "white" if is_hi else "#333"

                    html_content += f"""
                    <td style="background-color: {s_bg};">
                        <div class="cell-content">
                            <div class="date-num {day_clr if not is_hi else 'hi'}" style="background-color: {d_bg}; color: {d_txt};">{day}</div>
                            <div class="shift-name" style="color: {s_txt};">{s}</div>
                        </div>
                    </td>"""
            html_content += "</tr>"
        html_content += "</table></div>"
        # 다음 달로 이동
        curr = (curr.replace(day=1) + timedelta(days=32)).replace(day=1)
    
    return html_content + "</div>"

# 6. 렌더링 (높이를 충분히 주어 메인 페이지 스크롤과 일체화)
components.html(get_dynamic_calendar_html(base_start_date, hi_shift), height=7600, scrolling=False)
