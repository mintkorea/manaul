import streamlit as st

st.set_page_config(page_title="성의교정 보고체계", layout="wide")

# 여백 극소화 및 버튼 밀도 향상
st.markdown("""
    <style>
    .block-container {padding-top: 1rem; padding-bottom: 0rem;}
    .stButton > button {
        width: 100%;
        height: 2.2em;
        margin: 1px 0px;
        padding: 0px;
        font-size: 0.85em;
        text-align: left;
        padding-left: 8px;
    }
    hr {margin: 0.5rem 0rem;}
    h3 {margin-top: 0rem; font-size: 1.1em;}
    </style>
    """, unsafe_allow_html=True)

# 1. 상황실 상단 고정 (PDF 상단) [cite: 1, 2]
if st.button("🚨 상황실: 3147-8000"):
    st.markdown('<meta http-equiv="refresh" content="0; url=tel:0231478000">', unsafe_allow_html=True)

st.divider()

# 2. 2열 밀집 리스트 (PDF 1페이지 표 기반) 
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏢 건물명")
    b_list = [
        ("옴니버스(1)", "3147-8500"), ("옴니버스(2)", "3147-8600"),
        ("성의회관", "3147-8300"), ("의산연본관", "3147-8200"),
        ("의산연별관", "3147-8400"), ("병원별관", "2258-1115"),
        ("대학본관", "3147-8100")
    ]
    for name, num in b_list:
        if st.button(f"{name}:{num}", key=f"B_{num}"):
            st.markdown(f'<meta http-equiv="refresh" content="0; url=tel:02{num.replace("-","")}">', unsafe_allow_html=True)

with col2:
    st.subheader("📂 부서명")
    d_list = [
        ("통합관제실", "2258-5555"), ("설비팀", "2258-5624"),
        ("전기팀", "2258-5672"), ("통신실", "2258-5712"),
        ("반송통제실", "2258-5616"), ("병원별관전기", "2258-5673"),
        ("병원별관설비", "2258-5622")
    ]
    for name, num in d_list:
        if st.button(f"{name}:{num}", key=f"D_{num}"):
            st.markdown(f'<meta http-equiv="refresh" content="0; url=tel:02{num.replace("-","")}">', unsafe_allow_html=True)

st.divider()

# 3. 유관기관 하단 밀집 배치 (PDF 1페이지 하단) 
st.subheader("🚑 유관기관")
u1, u2, u3 = st.columns(3)
u_list = [("소방", "532-0119"), ("경찰", "532-0112"), ("지구대", "536-8477")]
for col, (name, num) in zip([u1, u2, u3], u_list):
    if col.button(f"{name}:{num}"):
        st.markdown(f'<meta http-equiv="refresh" content="0; url=tel:02{num.replace("-","")}">', unsafe_allow_html=True)
