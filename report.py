import streamlit as st


# 페이지 설정
st.set_page_config(page_title="성의교정 보고체계", layout="wide")

# CSS를 이용해 버튼 디자인 및 가독성 향상
st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #f0f2f6;
        font-weight: bold;
    }
    .emergency-btn > div > button {
        background-color: #ff4b4b !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📞 성의교정 긴급 연락처")

# 1. 최상단 긴급 연락처 (상황실)
st.subheader("🚨 통합 상황실")
col_main = st.columns(1)[0]
with col_main:
    # PDF 1페이지: 상황실 3147-8000 
    if st.button("🚨 상황실 즉시 연결 (3147-8000)", key="main_sos", help="클릭 시 전화 앱으로 연결됩니다."):
        st.markdown('<meta http-equiv="refresh" content="0; url=tel:0231478000">', unsafe_allow_html=True)

st.divider()

# 2. 건물별/부서별 연락처 (Page 1 데이터 기반)
st.subheader("🏢 건물별 연락처")

# PDF 1페이지 표 데이터를 기반으로 구성 [cite: 2]
contact_data = [
    {"건물": "옴니버스", "부서": "통합관제실", "번호": "02-3147-8500", "직통": "02-2258-5555"},
    {"건물": "옴니버스", "부서": "설비팀", "번호": "02-3147-8600", "직통": "02-2258-5624"},
    {"건물": "성의회관", "부서": "전기팀", "번호": "02-3147-8300", "직통": "02-2258-5672"},
    {"건물": "의산연본관", "부서": "통신실", "번호": "02-3147-8200", "직통": "02-2258-5712"},
    {"건물": "의산연별관", "부서": "반송통제실", "번호": "02-3147-8400", "직통": "02-2258-5616"},
    {"건물": "병원별관", "부서": "전기팀", "번호": "02-2258-1115", "직통": "02-2258-5673"},
    {"건물": "대학본관", "부서": "설비팀", "번호": "02-3147-8100", "직통": "02-2258-5622"},
]

for item in contact_data:
    with st.expander(f"{item['건물']} - {item['부서']}"):
        c1, c2 = st.columns(2)
        with c1:
            if st.button(f"📞 일반: {item['번호']}", key=f"btn_{item['번호']}"):
                st.markdown(f'<meta http-equiv="refresh" content="0; url=tel:{item["번호"].replace("-","")}">', unsafe_allow_html=True)
        with c2:
            if st.button(f"📱 직통: {item['직통']}", key=f"btn_{item['직통']}"):
                st.markdown(f'<meta http-equiv="refresh" content="0; url=tel:{item["직통"].replace("-","")}">', unsafe_allow_html=True)

st.divider()

# 3. 유관기관 연락처 (Page 1 하단)
st.subheader("🚑 유관기관")
# PDF 1페이지: 서초소방서, 서초경찰서, 반포지구대 [cite: 2]
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔥 소방서 (532-0119)"):
        st.markdown('<meta http-equiv="refresh" content="0; url=tel:025320119">', unsafe_allow_html=True)
with col2:
    if st.button("🚔 경찰서 (532-0112)"):
        st.markdown('<meta http-equiv="refresh" content="0; url=tel:025320112">', unsafe_allow_html=True)
with col3:
    if st.button("🏘️ 지구대 (536-8477)"):
        st.markdown('<meta http-equiv="refresh" content="0; url=tel:025368477">', unsafe_allow_html=True)
