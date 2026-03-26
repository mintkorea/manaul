import streamlit as st

st.set_page_config(page_title="성의교정 보고체계", layout="wide")

# 여백 제거 및 표 스타일 설정
st.markdown("""
    <style>
    .block-container {padding: 1rem 0.5rem;}
    table {width: 100%; border-collapse: collapse; font-size: 0.85em;}
    th, td {border: 1px solid #ddd; padding: 6px; text-align: center;}
    th {background-color: #f2f2f2; font-weight: bold;}
    .tel-link {text-decoration: none; color: #007bff; font-weight: bold; display: block;}
    .emergency-row {background-color: #ffe6e6; font-weight: bold;}
    </style>
    """, unsafe_allow_html=True)

# 1. 상황실 (표 상단 별도 표시) [cite: 1, 2]
st.markdown("""
    <table>
        <tr class="emergency-row">
            <td colspan="2">🚨 성의교정 상황실</td>
            <td><a class="tel-link" href="tel:0231478000">3147-8000</a></td>
        </tr>
    </table>
    <div style='margin-bottom: 5px;'></div>
    """, unsafe_allow_html=True)

# 2. 메인 연락처 표 (PDF 1페이지 레이아웃 복제) 
st.markdown("""
    <table>
        <tr>
            <th>건물명</th>
            <th>전화번호</th>
            <th>부서명</th>
            <th>전화번호</th>
        </tr>
        <tr>
            <td rowspan="2">옴니버스</td>
            <td><a class="tel-link" href="tel:0231478500">3147-8500</a></td>
            <td>통합관제실</td>
            <td><a class="tel-link" href="tel:0222585555">2258-5555</a></td>
        </tr>
        <tr>
            <td><a class="tel-link" href="tel:0231478600">3147-8600</a></td>
            <td>설비팀</td>
            <td><a class="tel-link" href="tel:0222585624">2258-5624</a></td>
        </tr>
        <tr>
            <td>성의회관</td>
            <td><a class="tel-link" href="tel:0231478300">3147-8300</a></td>
            <td>전기팀</td>
            <td><a class="tel-link" href="tel:0222585672">2258-5672</a></td>
        </tr>
        <tr>
            <td>의산연본관</td>
            <td><a class="tel-link" href="tel:0231478200">3147-8200</a></td>
            <td>통신실</td>
            <td><a class="tel-link" href="tel:0222585712">2258-5712</a></td>
        </tr>
        <tr>
            <td>의산연별관</td>
            <td><a class="tel-link" href="tel:0231478400">3147-8400</a></td>
            <td>반송통제실</td>
            <td><a class="tel-link" href="tel:0222585616">2258-5616</a></td>
        </tr>
        <tr>
            <td>병원별관</td>
            <td><a class="tel-link" href="tel:0222581115">2258-1115</a></td>
            <td>병원별관 전기팀</td>
            <td><a class="tel-link" href="tel:0222585673">2258-5673</a></td>
        </tr>
        <tr>
            <td>대학본관</td>
            <td><a class="tel-link" href="tel:0231478100">3147-8100</a></td>
            <td>병원별관 설비팀</td>
            <td><a class="tel-link" href="tel:0222585622">2258-5622</a></td>
        </tr>
    </table>
    """, unsafe_allow_html=True)

# 3. 유관기관 표 (하단) 
st.markdown("""
    <div style='margin-top: 10px;'></div>
    <h4 style='margin: 5px 0;'>🚑 유관기관</h4>
    <table>
        <tr>
            <th>기관명</th>
            <th>전화번호</th>
        </tr>
        <tr>
            <td>서초소방서</td>
            <td><a class="tel-link" href="tel:025320119">532-0119</a></td>
        </tr>
        <tr>
            <td>서초경찰서</td>
            <td><a class="tel-link" href="tel:025320112">532-0112</a></td>
        </tr>
        <tr>
            <td>반포지구대</td>
            <td><a class="tel-link" href="tel:025368477">536-8477</a></td>
        </tr>
    </table>
    """, unsafe_allow_html=True)
