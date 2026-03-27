import streamlit as st
from datetime import datetime, timedelta, date
import pytz
import calendar

# --- [1] 페이지 설정 및 스타일 (가이드라인 준수) ---
st.set_page_config(page_title="C조 근무달력 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 50px !important; max-width: 500px; margin: auto; }
    
    /* 탭 디자인: 부드러운 스타일 */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; display: flex; width: 100%; }
    .stTabs [data-baseweb="tab"] { 
        flex: 1; text-align: center; height: 45px; 
        background-color: #f8f9fa; border: 1px solid #eee;
        border-radius: 10px 10px 0 0; font-weight: 700; color: #888;
    }
    .stTabs [aria-selected="true"] { 
        background-color: #ffffff !important; color: #2E4077 !important; 
        border-bottom: 3px solid #2E4077 !important;
    }

    .main-title { text-align: center; font-size: 20px; font-weight: 900; color: #2E4077; margin-bottom: 20px; }
    
    /* 월 표시 타이틀: 메인(20px)보다 2폰트 작게 (18px) */
    .month-title { text-align: center; font-weight: 900; font-size: 18px; margin-top: 20px; margin-bottom: 10px; color: #444; }

    /* 달력 테이블 스타일 */
    .cal-table { width: 100%; border-collapse: collapse; table-layout: fixed; border: 1px solid #ccc; margin-bottom: 40px; }
    .cal-table th { background: #f2f4f7; padding: 8px 0; font-size: 12px; border: 1px solid #ddd; }
    .cal-td { border: 1px solid #eee; height: 65px; vertical-align: top; padding: 0 !important; }
    
    /* 날짜(13px)와 조 표시(16px) 폰트 차이 적용 */
    .cal-date-part { height: 40%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 13px; }
    .cal-shift-part { height: 60%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 16px; }
    
    .sun { color: #d32f2f !important; }
    .sat { color: #1976d2 !important; }
    .hi-text { color: white !important; }
    .today-border { border: 3px solid #333 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 핵심 로직 ---
kst = pytz.timezone('Asia/Seoul')
today_kst = datetime.now(kst).date()
PATTERN_START = date(2026, 3, 9) # C조 기준일

def get_shift_simple(dt):
    """날짜별 A, B, C조 판별 로직"""
    diff = (dt - PATTERN_START).days
    return ["C", "A", "B"][diff % 3]

# --- [3] 화면 구성 (탭 유지) ---
tab1 = st.tabs(["🏥 근무달력"])[0] # 단일 탭으로 구성하되 구조 유지

with tab1:
    st.markdown('<div class="main-title">🏥 성의교정 근무 달력</div>', unsafe_allow_html=True)
    
    # 강조 기능: 선택 없음 포함
    options = ["선택 없음", "A", "B", "C"]
    current_shift = get_shift_simple(today_kst)
    hi = st.selectbox("🎯 강조 조 선택 (배경색 강조)", options, index=options.index(current_shift))
    
    # 색상 정의 (옅은 배경 / 진한 강조색)
    B_COLS = {"A": "#FFE0B2", "B": "#FFCDD2", "C": "#BBDEFB"} # 비강조시 배경
    S_COLS = {"A": "#FB8C00", "B": "#E53935", "C": "#1E88E5"} # 강조시 배경 및 글자바탕
    
    cal_html = ""
    curr = today_kst.replace(day=1) # 이번 달 1일부터 표시
    
    # 향후 12개월치 달력 생성
    for _ in range(12):
        y, m = curr.year, curr.month
        cal = calendar.monthcalendar(y, m)
        
        cal_html += f"<div class='month-title'>{y}년 {m}월</div>"
        cal_html += "<table class='cal-table'><tr><th class='sun'>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class='sat'>토</th></tr>"
        
        for week in cal:
            cal_html += "<tr>"
            for i, day in enumerate(week):
                if day == 0:
                    cal_html += "<td class='cal-td'></td>"
                else:
                    d_obj = date(y, m, day)
                    s = get_shift_simple(d_obj)
                    is_hi = (hi == s) # 선택된 조인지 확인
                    
                    # 배경색 및 텍스트 색상 결정
                    s_bg = S_COLS[s] if is_hi else B_COLS[s]
                    d_bg = S_COLS[s] if is_hi else "white"
                    td_cls = "today-border" if d_obj == today_kst else ""
                    txt_cls = "hi-text" if is_hi else ("sun" if i == 0 else "sat" if i == 6 else "")
                    
                    cal_html += f"""
                    <td class='cal-td {td_cls}' style='background:{s_bg};'>
                        <div class='cal-date-part {txt_cls}' style='background:{d_bg};'>{day}</div>
                        <div class='cal-shift-part {txt_cls}'>{s}</div>
                    </td>
                    """
            cal_html += "</tr>"
        cal_html += "</table>"
        
        # 다음 달로 이동
        curr = (curr.replace(day=1) + timedelta(days=32)).replace(day=1)
        
    st.markdown(cal_html, unsafe_allow_html=True)
