import streamlit as st

st.set_page_config(page_title="성의교정 보고체계", layout="wide")

# 여백 극한 제거 및 표 스타일 설정
st.markdown("""
    <style>
    /* 페이지 전체 여백 제거 */
    .block-container {padding: 0.5rem 0.2rem !important;}
    
    /* 타이틀 스타일 */
    .app-title {font-size: 1.2em; font-weight: bold; text-align: center; margin-bottom: 5px;}
    
    /* 표 기본 스타일: 여백 0, 줄간격 최소 */
    table {width: 100%; border-collapse: collapse; font-size: 0.82em; line-height: 1.0; table-layout: fixed;}
    th, td {border: 1px solid #444; padding: 1px 2px !important; text-align: center; height: 1.8em;}
    th {background-color: #f0f0f0; font-weight: bold;}
    
    /* 전화번호 링크 스타일 */
    .tel-link {text-decoration: none; color: #007bff; font-weight: bold; display: block; width: 100%; height: 100%;}
    
    /* 상황실 강조 행 */
    .emergency-row {background-color: #ffcccc; font-weight: bold;}
    </style>
    """, unsafe_allow_html=True)

# 1. 타이틀 [cite: 1]
st.markdown('<div class="app-title">성의교정 보고체계</div>', unsafe_allow_html=True)

# 2. 성의교정 상황실 
st.markdown("""
    <table>
        <tr class="emergency-row">
            <td style="width:40%;">🚨 상황실</td>
            <td><a class="tel-link" href="tel:0231478000">-8000</a></td>
        </tr>
    </table>
    <div style='margin-bottom: 3px;'></div>
    """, unsafe_allow_html=True)

# 3. 메인 연락처 표 (3147 삭제, 2258 -> *1 변환) 
st.markdown("""
    <table>
        <tr>
            <th style="width:25%;">건물명</th>
            <th style="width:25%;">번호</th>
            <th style="width:25%;">부서명</th>
            <th style="width:25%;">번호</th>
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
            <td>별관 전기</td>
            <td><a class="tel-link" href="tel:0222585673">*1-5673</a></td>
        </tr>
        <tr>
            <td>대학본관</td>
            <td><a class="tel-link" href="tel:0231478100">-8100</a></td>
            <td>별관 설비</td>
            <td><a class="tel-link" href="tel:0222585622">*1-5622</a></td>
        </tr>
    </table>
    """, unsafe_allow_html=True)

# 4. 유관기관 
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
