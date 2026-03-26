import streamlit as st

st.set_page_config(page_title="성의교정 보고체계", layout="wide")

# 버튼 및 레이아웃 스타일 설정
st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        margin-bottom: 5px;
        font-weight: bold;
    }
    /* 상황실 버튼 강조 */
    .emergency-btn > div > button {
        background-color: #e74c3c !important;
        color: white !important;
        height: 4em;
        font-size: 1.2em !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 최상단: 성의교정 상황실 (PDF 상단 중앙 데이터)
st.markdown("<h2 style='text-align: center;'>📞 성의교정 보고체계</h2>", unsafe_allow_html=True)
st.container()
col_sec = st.columns([1, 2, 1])
with col_sec[1]:
    st.markdown('<div class="emergency-btn">', unsafe_allow_html=True)
    if st.button("🚨 상황실 즉시 연결 (3147-8000)", key="sos"):
        st.markdown('<meta http-equiv="refresh" content="0; url=tel:0231478000">', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# 메인 섹션: 2열 배치
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🏢 건물별 주요 보고처")
    # PDF 1페이지 좌측: 통합관제실 및 주요 건물 연락처 
    building_contacts = [
        ("옴니버스 통합관제실", "3147-8500", "2258-5555"),
        ("의산연본관", "3147-8200", "2258-5712"),
        ("의산연별관", "3147-8400", "2258-5616"),
        ("대학본관", "3147-8100", "2258-5622"),
        ("병원별관", "2258-1115", "2258-5673")
    ]
    for name, num1, num2 in building_contacts:
        with st.expander(f"📍 {name}"):
            c1, c2 = st.columns(2)
            if c1.button(f"📞 {num1}", key=f"l_{num1}"):
                st.markdown(f'<meta http-equiv="refresh" content="0; url=tel:02{num1.replace("-","")}">', unsafe_allow_html=True)
            if c2.button(f"📱 {num2}", key=f"l_{num2}"):
                st.markdown(f'<meta http-equiv="refresh" content="0; url=tel:02{num2.replace("-","")}">', unsafe_allow_html=True)

with col_right:
    st.subheader("🛠️ 주요 팀별 연락처")
    # PDF 1페이지 우측: 설비, 전기, 통신팀 데이터 
    team_contacts = [
        ("옴니버스 설비팀", "3147-8600", "2258-5624"),
        ("성의회관 전기팀", "3147-8300", "2258-5672"),
        ("병원별관 설비팀", "3147-8100", "2258-5622"),
        ("반송통제실", "3147-8400", "2258-5616"),
    ]
    for name, num1, num2 in team_contacts:
        with st.expander(f"⚙️ {name}"):
            c1, c2 = st.columns(2)
            if c1.button(f"📞 {num1}", key=f"r_{num1}"):
                st.markdown(f'<meta http-equiv="refresh" content="0; url=tel:02{num1.replace("-","")}">', unsafe_allow_html=True)
            if c2.button(f"📱 {num2}", key=f"r_{num2}"):
                st.markdown(f'<meta http-equiv="refresh" content="0; url=tel:02{num2.replace("-","")}">', unsafe_allow_html=True)

st.divider()

# 하단: 유관기관 (서초소방서, 서초경찰서, 반포지구대)
st.subheader("🚑 유관기관 연락처")
# PDF 1페이지 하단 유관기관 데이터 
u1, u2, u3 = st.columns(3)
with u1:
    if st.button("🔥 서초소방서 (532-0119)"):
        st.markdown('<meta http-equiv="refresh" content="0; url=tel:025320119">', unsafe_allow_html=True)
with u2:
    if st.button("🚔 서초경찰서 (532-0112)"):
        st.markdown('<meta http-equiv="refresh" content="0; url=tel:025320112">', unsafe_allow_html=True)
with u3:
    if st.button("🏘️ 반포지구대 (536-8477)"):
        st.markdown('<meta http-equiv="refresh" content="0; url=tel:025368477">', unsafe_allow_html=True)
