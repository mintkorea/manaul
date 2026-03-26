import streamlit as st

st.set_page_config(page_title="성의교정 보고체계", layout="wide")

st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        border-radius: 5px;
        margin-bottom: 2px;
        text-align: left;
        padding-left: 12px;
        font-size: 0.95em;
        height: 3em;
    }
    .main-head {
        background-color: #2c3e50;
        color: white;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. 최상단 상황실 (PDF 1페이지 상단)
st.markdown('<div class="main-head">🚨 성의교정 상황실 : 3147-8000</div>', unsafe_allow_html=True)

# 2. 메인 연락처 리스트 (좌: 건물명 / 우: 부서명)
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🏢 건물명")
    # PDF 1페이지 왼쪽 '건물명' 열 데이터
    building_list = [
        ("옴니버스 (1)", "3147-8500"),
        ("옴니버스 (2)", "3147-8600"),
        ("성의회관", "3147-8300"),
        ("의산연본관", "3147-8200"),
        ("의산연별관", "3147-8400"),
        ("병원별관", "2258-1115"),
        ("대학본관", "3147-8100")
    ]
    for name, phone in building_list:
        if st.button(f"{name} : {phone}", key=f"B_{name}_{phone}"):
            st.markdown(f'<meta http-equiv="refresh" content="0; url=tel:02{phone.replace("-","")}">', unsafe_allow_html=True)

with col_right:
    st.subheader("📂 부서명")
    # PDF 1페이지 오른쪽 '부서명' 열 데이터
    dept_list = [
        ("통합관제실", "2258-5555"),
        ("설비팀", "2258-5624"),
        ("전기팀", "2258-5672"),
        ("통신실", "2258-5712"),
        ("반송통제실", "2258-5616"),
        ("병원별관 전기팀", "2258-5673"),
        ("병원별관 설비팀", "2258-5622")
    ]
    for dept, phone in dept_list:
        if st.button(f"{dept} : {phone}", key=f"D_{dept}_{phone}"):
            st.markdown(f'<meta http-equiv="refresh" content="0; url=tel:02{phone.replace("-","")}">', unsafe_allow_html=True)

st.divider()

# 3. 최하단 유관기관 (PDF 1페이지 하단)
st.subheader("🚑 유관기관")
u_col1, u_col2, u_col3 = st.columns(3)
with u_col1:
    if st.button("🔥 서초소방서: 532-0119"):
        st.markdown('<meta http-equiv="refresh" content="0; url=tel:025320119">', unsafe_allow_html=True)
with u_col2:
    if st.button("🚔 서초경찰서: 532-0112"):
        st.markdown('<meta http-equiv="refresh" content="0; url=tel:025320112">', unsafe_allow_html=True)
with u_col3:
    if st.button("🏘️ 반포지구대: 536-8477"):
        st.markdown('<meta http-equiv="refresh" content="0; url=tel:025368477">', unsafe_allow_html=True)
