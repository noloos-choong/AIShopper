import streamlit as st
import requests
import json
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ✅ 한글 폰트 자동 설정 (NanumGothic이 있으면 자동 적용)
def set_korean_font():
    font_path = None
    for font in fm.findSystemFonts():
        if "NanumGothic" in font:
            font_path = font
            break
    if font_path:
        font_prop = fm.FontProperties(fname=font_path)
        plt.rc("font", family=font_prop.get_name())
    else:
        st.warning("⚠️ 시스템에서 'NanumGothic' 폰트를 찾을 수 없습니다.")

set_korean_font()

# 네이버 API 인증 정보 (보안상 환경변수로 관리하는 것이 좋음)
CLIENT_ID = "1Vh7jUKindSD9TuhtG4O"
CLIENT_SECRET = "jl83Z217Yj"

# API 요청 URL
API_URL = "https://openapi.naver.com/v1/datalab/shopping/categories"

# ✅ 최근 1년(365일) 동안의 데이터 조회
end_date = datetime.date.today().strftime("%Y-%m-%d")
start_date = (datetime.date.today() - datetime.timedelta(days=365)).strftime("%Y-%m-%d")

# Streamlit UI
st.title("📊 네이버 쇼핑 트렌드 분석")
st.write("최근 1년 동안 특정 카테고리의 검색량을 분석합니다.")

# 선택할 카테고리 목록
category_options = {
    "스포츠/레저": "50000007",
    "패션잡화": "50000001",
    "출산/육아": "50000005",
    "패션의류": "50000000",
    "생활/건강": "50000008",
    "가구/인테리어": "50000004",
    "디지털/가전": "50000003",
    "화장품/미용": "50000002",
    "식품": "50000006",
    "여가/생활편의": "50000009"
}

# 멀티 선택 (Streamlit의 multiselect 사용)
selected_categories = st.multiselect(
    "조회할 카테고리를 선택하세요",
    list(category_options.keys()), 
    default=["스포츠/레저", "패션잡화"]  # 기본 선택
)

# API 요청 데이터 구성
if st.button("데이터 조회"):
    request_body = {
        "startDate": start_date,
        "endDate": end_date,
        "timeUnit": "month",  # ✅ 월 단위로 1년치 데이터 조회
        "category": [{"name": name, "param": [category_options[name]]} for name in selected_categories],
        "device": "mo",
        "gender": "f",
        "ages": ["20", "30", "40"]
    }

    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET,
        "Content-Type": "application/json",
    }

    # API 호출
    response = requests.post(API_URL, headers=headers, data=json.dumps(request_body))

    if response.status_code == 200:
        data = response.json()
        
        # JSON 데이터를 DataFrame으로 변환
        results = []
        for category_data in data["results"]:
            category_name = category_data["title"]
            for entry in category_data["data"]:
                results.append({
                    "카테고리": category_name,
                    "기간": entry["period"],
                    "검색량 비율": entry["ratio"]
                })
        
        df = pd.DataFrame(results)

        # 📈 라인 차트 (월별 검색량 추이) - Matplotlib 활용
        st.subheader("📈 최근 1년간 월별 검색량 추이")

        # 피벗 테이블로 변환 (기간 기준)
        pivot_df = df.pivot(index="기간", columns="카테고리", values="검색량 비율")

        # Matplotlib 차트 생성
        fig, ax = plt.subplots(figsize=(12, 5))

        # 데이터 라인 및 값 표시
        for category in pivot_df.columns:
            ax.plot(pivot_df.index, pivot_df[category], marker="o", label=category)
            for i, txt in enumerate(pivot_df[category]):
                ax.text(i, txt, f"{txt:.1f}", ha="center", va="bottom", fontsize=9)  # 값 표시

        # ✅ X축 설정 (12개월을 보기 쉽게 가로로 표시)
        ax.set_xticks(range(len(pivot_df.index)))
        ax.set_xticklabels([x[2:] for x in pivot_df.index], rotation=0)  # "YYYY-MM" → "MM" 으로 축약

        # 차트 설정
        ax.set_xlabel("월")
        ax.set_ylabel("검색량 비율")
        ax.set_title("카테고리별 검색량 추이")
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.7)

        # Streamlit에 차트 표시
        st.pyplot(fig)

        # 📊 막대 차트 (카테고리별 평균 검색량)
        st.subheader("📊 카테고리별 평균 검색량")
        bar_chart_data = df.groupby("카테고리")["검색량 비율"].mean().reset_index()
        st.bar_chart(bar_chart_data.set_index("카테고리"))

    else:
        st.error(f"API 호출 실패: {response.status_code}")
        st.text(response.text)
