import streamlit as st

st.set_page_config(page_title="성의교정 보고체계", layout="wide")

# 여백 극한 제거 및 표 스타일 (국번 대체 반영)
st.markdown("""
    <style>
    .block-container {padding: 0.2rem 0.2rem;}
    table {width: 100%; border-collapse: collapse; font-size: 0.82em; line-height: 1.1;}
    th, td {border: 1px solid #999; padding: 2px 4px; text-align: center;}
    th {background-color: #eee; font-weight: bold;}
    .tel-link {text-decoration: none; color: #007bff; font-weight: bold;}
    .emergency-row {background-color: #ffe6e6; font-weight: bold;}
    </style>
    """, unsafe_allow_html=True)

# 1. 상황실 (3147 제거) 
st.markdown("""
    <table>
        <tr class="emergency-row">
            <td style="width:50%;">🚨 성의교정 상황실</td>
            <td><a class="tel-link" href="tel:0231478000">-8000</a></td>
        </tr>
    </table>
    <div style='margin-bottom: 2px;'></div>
    """, unsafe_allow_html=True)

# 2. 메인 연락처 표 (PDF 레이아웃 유지 + 국번 변환) 
# 3147 -> 국번 삭제 (-) / 2258 -> *1- 로 표시
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
            <td><a class="tel-link" href="tel:0231478500">-8500</a></td>
            <td>통합관제실</td>
            <td><a class="tel-link" href="tel:0222585555">*1-5555</a></td>
        </tr>
        <tr>
            <td><a class="tel-link" href="tel:0231478600">-8600</a></td>
            <td>설비팀</td>
            <td><a class="tel-link" href="tel:0222585624">*1-5624</a></td>
        </tr>
        <tr>
            <td>성의회관</td>
            <td><a class="tel-link" href="tel:0231478300">-8300</a></td>
            <td>전기팀</td>
            <td><a class="tel-link" href="tel:0222585672">*1-5672</a></td>
        </tr>
        <tr>
            <td>의산연본관</td>
            <td><a class="tel-link" href="tel:0231478200">-8200</a></td>
            <td>통신실</td>
            <td><a class="tel-link" href="tel:0222585712">*1-5712</a></td>
        </tr>
        <tr>
            <td>의산연별관</td>
            <td><a class="tel-link" href="tel:0231478400">-8400</a></td>
            <td>반송통제실</td>
            <td><a class="tel-link" href="tel:0222585616">*1-5616</a></td>
        </tr>
        <tr>
            <td>병원별관</td>
            <td><a class="tel-link" href="tel:0222581115">*1-1115</a></td>
            <td>별관 전기팀</td>
            <td><a class="tel-link" href="tel:0222585673">*1-5673</a></td>
        </tr>
        <tr>
            <td>대학본관</td>
            <td><a class="tel-link" href="tel:0231478100">-8100</a></td>
            <td>별관 설비팀</td>
            <td><a class="tel-link" href="tel:0222585622">*1-5622</a></td>
        </tr>
    </table>
    """, unsafe_allow_html=True)

# 3. 유관기관 (PDF 하단) 
st.markdown("""
    <div style='margin-top: 5px;'></div>
    <table>
        <tr>
            <th colspan="2">🚑 유관기관</th>
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
