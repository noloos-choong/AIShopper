import requests
import json
import datetime

# 네이버 API 인증 정보
CLIENT_ID = "1Vh7jUKindSD9TuhtG4O"  # 네이버 개발자센터에서 발급받은 클라이언트 ID
CLIENT_SECRET = "jl83Z217Yj"  # 네이버 개발자센터에서 발급받은 클라이언트 Secret


#50000001 - 패션 잡화
# 50000053 - 스포츠 악세서리


# 50000007 - 스포츠/레저
# 50000001 - 패션잡화
# 50000005 - 출산/육아
# 50000000 - 패션의류
# 50000008 - 생활/건강
# 50000004 - 가구/인테리어
# 50000003 - 디지털/가전
# 50000002 - 화장품/미용
# 50000006 - 식품
# 50000009 - 여가/생활편의



# API 요청 URL
API_URL = "https://openapi.naver.com/v1/datalab/shopping/categories"

# 최근 6개월 동안의 데이터 조회
end_date = datetime.date.today().strftime("%Y-%m-%d")
start_date = (datetime.date.today() - datetime.timedelta(days=180)).strftime("%Y-%m-%d")

# 요청 데이터
request_body = {
    "startDate": start_date,
    "endDate": end_date,
    "timeUnit": "month",
    "category": [
        {"name": "스포츠/레저", "param": ["50000007"]},
        {"name": "패션잡화", "param": ["50000001"]},
        {"name": "출산/육아", "param": ["50000005"]}
        #{"name": "패션의류", "param": ["50000000"]}
        # {"name": "생활/건강", "param": ["50000008"]},
        # {"name": "가구/인테리어", "param": ["50000004"]},
        # {"name": "디지털/가전", "param": ["50000003"]},
        # {"name": "화장품/미용", "param": ["50000002"]},
        # {"name": "식품", "param": ["50000006"]},
        # {"name": "여가/생활편의", "param": ["50000009"]}
    ],
    "device": "mo",  # 모바일 검색 기준
    "gender": "f",  # 여성
    "ages": ["20", "30", "40"]  # 20대~30대
}

# API 요청 헤더
headers = {
    "X-Naver-Client-Id": CLIENT_ID,
    "X-Naver-Client-Secret": CLIENT_SECRET,
    "Content-Type": "application/json",
}

# API 호출
response = requests.post(API_URL, headers=headers, data=json.dumps(request_body))

# 응답 처리
if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=4, ensure_ascii=False))  # JSON 데이터 보기 좋게 출력
else:
    print(f"Error Code: {response.status_code}")
    print(response.text)
