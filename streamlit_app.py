import streamlit as st
from openai import OpenAI

def main():
    # 페이지 설정
    st.set_page_config(page_title="하나투어 여행 챗봇", page_icon="✈️")
    
    # 타이틀 및 소개
    st.title("🌍 하나투어 여행 길라잡이")
    st.markdown("**당신의 여행을 더욱 특별하고 편리하게 만들어드립니다!**")
    
    # 사이드바 설정
    st.sidebar.image("https://www.hananatour.com/resources/images/hananatour_logo.png", width=200)
    st.sidebar.header("여행 설정")
    
    # 여행 관련 선택지
    travel_type = st.sidebar.selectbox(
        "여행 유형을 선택하세요",
        ["패키지 여행", "자유 여행", "허니문", "가족 여행", "친구와 여행"]
    )
    
    # 목적지 선택
    destinations = {
        "국내 여행": ["서울", "부산", "제주도", "강릉", "여수"],
        "해외 여행": ["일본", "유럽", "미국", "동남아", "중국"]
    }
    
    travel_region = st.sidebar.selectbox(
        "여행 지역", list(destinations.keys())
    )
    
    destination = st.sidebar.selectbox(
        "세부 목적지", destinations[travel_region]
    )
    
    # API 키 입력
    api_key = st.sidebar.text_input("OpenAI API 키", type="password")
    
    # 사용자 입력 영역
    user_message = st.text_area(
        f"{destination} 여행에 대해 무엇을 알고 싶으신가요?", 
        placeholder="여행 일정, 추천 관광지, 맛집, 숙소 등에 대해 물어보세요."
    )
    
    # 메시지 전송 버튼
    if st.button("여행 정보 찾기"):
        # API 키 유효성 검사
        if not api_key:
            st.error("API 키를 입력해주세요.")
            return
        
        try:
            # OpenAI 클라이언트 초기화
            client = OpenAI(api_key=api_key)
            
            # 컨텍스트를 추가한 프롬프트 생성
            enhanced_prompt = f"""
            당신은 전문 여행 가이드입니다. 다음 조건을 고려하여 답변해주세요:
            - 여행 유형: {travel_type}
            - 목적지: {destination}
            - 여행자 질문: {user_message}
            
            구체적이고 실용적이며 현지 감성이 담긴 답변을 제공하세요.
            """
            
            # 메시지 생성
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "당신은 전문 여행 가이드입니다."},
                    {"role": "user", "content": enhanced_prompt}
                ]
            )
            
            # 응답 출력
            st.success(f"{destination} 여행 정보:")
            st.write(response.choices[0].message.content)
        
        except Exception as e:
            st.error(f"여행 정보 검색 중 오류 발생: {e}")
    
    # 추가 정보 섹션
    st.sidebar.markdown("---")
    st.sidebar.info(
        "💡 Tip: 여행 전 항상 최신 현지 정보와 "
        "여행 경보를 확인하세요!"
    )

# 메인 앱 실행
if __name__ == "__main__":
    main()
