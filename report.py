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

# 1. 최상단 상황실 (PDF 상단)
st.markdown('<div class="main-head">🚨 성의교정 상황실 : 3147-8000</div>', unsafe_allow_html=True)

# 2. 메인 연락처 리스트 (좌: 건물명 / 우: 부서명)
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🏢 건물명")
    # PDF 1페이지 왼쪽 '건물명' 열 순서대로 나열
    building_list = [
        ("옴니버스 (1)", "3147-8500"), [cite: 2]
        ("옴니버스 (2)", "3147-8600"), [cite: 2]
        ("성의회관", "3147-8300"), [cite: 2]
        ("의산연본관", "3147-8200"), [cite: 2]
        ("의산연별관", "3147-8400"), [cite: 2]
        ("병원별관", "2258-1115"), [cite: 2]
        ("대학본관", "3147-8100") [cite: 2]
    ]
    for name, phone in building_list:
        if st.button(f"{name} : {phone}", key=f"B_{name}_{phone}"):
            st.markdown(f'<meta http-equiv="refresh" content="0; url=tel:02{phone.replace("-","")}">', unsafe_allow_html=True)

with col_right:
    st.subheader("📂 부서명")
    # PDF 1페이지 오른쪽 '부서명' 및 '전화번호' 열 순서대로 나열
    dept_list = [
        ("통합관제실", "2258-5555"), [cite: 2]
        ("설비팀", "2258-5624"), [cite: 2]
        ("전기팀", "2258-5672"), [cite: 2]
        ("통신실", "2258-5712"), [cite: 2]
        ("반송통제실", "2258-5616"), [cite: 2]
        ("병원별관 전기팀", "2258-5673"), [cite: 2]
        ("병원별관 설비팀", "2258-5622") [cite: 2]
    ]
    for dept, phone in dept_list:
        if st.button(f"{dept} : {phone}", key=f"D_{dept}_{phone}"):
            st.markdown(f'<meta http-equiv="refresh" content="0; url=tel:02{phone.replace("-","")}">', unsafe_allow_html=True)

st.divider()

# 3. 최하단 유관기관
st.subheader("🚑 유관기관")
u_col1, u_col2, u_col3 = st.columns(3)
with u_col1:
    if st.button("🔥 서초소방서: 532-0119"): [cite: 2]
        st.markdown('<meta http-equiv="refresh" content="0; url=tel:025320119">', unsafe_allow_html=True)
with u_col2:
    if st.button("🚔 서초경찰서: 532-0112"): [cite: 2]
        st.markdown('<meta http-equiv="refresh" content="0; url=tel:025320112">', unsafe_allow_html=True)
with u_col3:
    if st.button("🏘️ 반포지구대: 536-8477"): [cite: 2]
        st.markdown('<meta http-equiv="refresh" content="0; url=tel:025368477">', unsafe_allow_html=True)
