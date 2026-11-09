import requests
import json
import os
from datetime import datetime

# =====================================================================
# 🔑 [카카오 API 키 설정] 카카오 디벨로퍼스에서 발급받은 'REST API 키'를 입력하세요.
# =====================================================================
KAKAO_REST_API_KEY = "6a132dbb80c9250761200aeb05d55c8b"

# ---------------------------------------------------------
# 1. 날씨 자동 생성 함수
# ---------------------------------------------------------
def get_expected_weather(date_str):
    month = int(date_str.split("-")[1])
    if month in [3, 4, 5]: return "🌸 맑고 따뜻함 (봄옷 추천)"
    elif month in [6, 7, 8]: return "☀️ 덥고 습함 (자외선 차단제 필수)"
    elif month in [9, 10, 11]: return "🍁 선선하고 맑음 (여행하기 최고!)"
    else: return "❄️ 춥고 건조함 (따뜻한 겉옷 필수)"

# ---------------------------------------------------------
# 2. 카카오 로컬 API 검색 함수 (터미널 실시간 출력 추가)
# ---------------------------------------------------------
def search_kakao_places(keyword):
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"}
    params = {"query": keyword, "size": 3}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        places = []
        
        for document in data.get("documents", []):
            # 장소 이름뿐만 아니라 '주소'도 함께 추출하여 터미널에 보여줍니다.
            place_name = document["place_name"]
            address = document.get("road_address_name") or document.get("address_name")
            places.append(f"{place_name} ({address})")
            
        # 💡 [터미널 실시간 출력] 검색된 결과를 터미널에 바로 보여줍니다!
        if places:
            print(f"   ✔️ [{keyword}] 검색 성공! ➔ {places[0].split(' (')[0]} 등 {len(places)}곳 발견")
        else:
            print(f"   ⚠️ [{keyword}] 검색 결과가 없습니다.")
            
        return places if places else ["검색 결과가 없습니다."]
        
    except Exception as e:
        print(f"   ❌ [{keyword}] API 통신 실패: {e}")
        return [f"[가상] {keyword} 추천 장소"]

# ---------------------------------------------------------
# 3. 전체 여행 데이터 수집
# ---------------------------------------------------------
def fetch_travel_data(date_str):
    print(f"\n📡 [API 통신 시작] 카카오 서버에서 데이터를 실시간으로 검색합니다...")
    
    weather_info = get_expected_weather(date_str)
    target_cities = ["부산", "제주"]
    destinations = []
    
    for city in target_cities:
        print(f"\n 🔎 <{city}> 지역 정보 검색 중...")
        events = search_kakao_places(f"{city} 가볼만한곳")
        restaurants = search_kakao_places(f"{city} 맛집")
        
        destinations.append({
            "city": f"{city}광역시/특별자치도",
            "weather": weather_info,
            "events": events,
            "restaurants": restaurants
        })
        
    return {"target_date": date_str, "destinations": destinations}

# ---------------------------------------------------------
# 4. 데이터 관리 (JSON 캐싱)
# ---------------------------------------------------------
def get_travel_data(date_str):
    json_filename = f"travel_data_{date_str}.json"
    
    if os.path.exists(json_filename):
        print(f"\n📂 [캐시 확인] '{json_filename}' 파일이 존재합니다. API를 호출하지 않고 바로 불러옵니다.")
        with open(json_filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    data = fetch_travel_data(date_str)
    
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"\n💾 [저장 완료] 검색된 데이터를 '{json_filename}'에 안전하게 저장했습니다.")
    
    return data

# ---------------------------------------------------------
# 5. 리포트 생성 및 터미널 최종 출력 (UI 개선)
# ---------------------------------------------------------
def generate_markdown_report(data):
    date_str = data["target_date"]
    md_filename = f"travel_report_{date_str}.md"
    
    # 마크다운 파일 내용 구성
    md_content = f"# 🎒 {date_str} 국내 여행지 추천 리포트\n\n"
    for dest in data["destinations"]:
        md_content += f"## 📍 {dest['city']}\n"
        md_content += f"**🌤 예상 날씨:** {dest['weather']}\n\n"
        md_content += "**🎉 추천 명소:**\n" + "\n".join([f"- {e}" for e in dest['events']]) + "\n\n"
        md_content += "**🍽 추천 맛집:**\n" + "\n".join([f"- {r}" for r in dest['restaurants']]) + "\n\n"
        md_content += "---\n\n"
        
    with open(md_filename, 'w', encoding='utf-8') as f:
        f.write(md_content)
        
    # 💡 [터미널 최종 출력] 사용자가 보기 편하게 터미널 UI를 예쁘게 꾸몄습니다.
    print("\n" + "=" * 60)
    print(f" 📱 [터미널 리포트] {date_str} 맞춤 여행 정보가 도착했습니다!")
    print("=" * 60)
    
    for dest in data["destinations"]:
        print(f"\n 📍 [ {dest['city']} ]")
        print(f"  🌤  날씨: {dest['weather']}")
        print("  🎉 명소:")
        for event in dest['events']:
            print(f"     - {event}")
        print("  🍽  맛집:")
        for rest in dest['restaurants']:
            print(f"     - {rest}")
    print("\n" + "=" * 60)
    print(f" 📝 (상세 내용은 '{md_filename}' 파일에서도 확인할 수 있습니다.)\n")

# ---------------------------------------------------------
# 6. 메인 실행 함수
# ---------------------------------------------------------
def main():
    print("="*60)
    print(" ✈️  국내 여행지 추천 챗봇 (카카오 API 실시간 터미널 버전) ")
    print("="*60)
    
    while True:
        date_input = input("\n📅 여행 날짜를 입력하세요 (YYYY-MM-DD) [종료: q]: ").strip()
        
        if date_input.lower() == 'q':
            print("👋 프로그램을 종료합니다. 즐거운 하루 보내세요!")
            break
            
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
        except ValueError:
            print("❌ [오류] 날짜 형식이 올바르지 않습니다. (예: 2023-10-25)")
            continue
            
        travel_data = get_travel_data(date_input)
        generate_markdown_report(travel_data)

if __name__ == "__main__":
    main()