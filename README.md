# AI-A1-2 API 활용 국내 여행지 추천 프로그램 개발

---

# [기술 보고서] REST API 인증 메커니즘 및 보안 관리 체계 학습

**보고 일자:** 2024년 5월 22일
**작성자:** 학습자
**주제:** API Key 기반 인증 구현 및 보안 가이드라인 수립

---

### 1. 학습 목적 (Objective)
본 학습은 외부 서비스(SaaS, Data Provider)와의 인터페이스 연동을 위한 핵심 인증 수단인 **API Key의 동작 원리**를 파악하고, 코드 레벨에서의 **안전한 구현 방식**을 습득하는 것을 목적으로 함.

### 2. 기술적 명세 (Technical Specifications)

#### 2.1 API Key의 정의 및 역할
*   **정의:** 클라이언트 애플리케이션이 API 서버에 접근할 때 자신을 식별하기 위해 전달하는 고유한 문자열(Token).
*   **역할:** 
    *   **Authentication (인증):** 요청자가 누구인지 확인.
    *   **Authorization (인가):** 요청자가 해당 자원에 접근할 권한이 있는지 확인.
    *   **Usage Tracking:** API 호출 횟수 제한(Rate Limiting) 및 과금 관리.

#### 2.2 인증 전달 방식 비교
| 방식 | 위치 | 특징 | 보안성 |
| :--- | :--- | :--- | :--- |
| **HTTP Header** | `Authorization: Bearer <Key>` | 표준적인 방식, 로그에 노출될 위험이 적음 | **높음** |
| **Custom Header** | `X-API-KEY: <Key>` | 서비스별 고유 헤더 정의 시 사용 | **높음** |
| **Query Parameter** | `?api_key=<Key>` | 구현이 간편하나 브라우저 히스토리/로그에 노출됨 | **낮음** |

### 3. 구현 프로세스 분석 (Implementation Analysis)

Python `requests` 라이브러리를 활용한 표준 호출 프로세스는 다음과 같음:

1.  **환경 설정:** API 엔드포인트(URL) 및 인증 키 정의.
2.  **헤더 구성:** `Content-Type` 및 `Authorization` 명세 작성.
3.  **요청 실행:** HTTP Method(GET, POST 등)에 따른 동기적 호출.
4.  **예외 처리:** HTTP 상태 코드(Status Code) 기반의 에러 핸들링.
    *   `200 OK`: 요청 성공.
    *   `401 Unauthorized`: API 키 누락 또는 유효하지 않음.
    *   `403 Forbidden`: 권한 부족 (유료 플랜 미가입 등).
    *   `429 Too Many Requests`: 호출 제한 초과.

### 4. 보안 취약점 방지 대책 (Security Best Practices)

API 키 유출은 데이터 침해 및 금전적 손실로 직결되므로 아래의 보안 수칙을 준수해야 함:

*   **Hardcoding 금지:** 소스 코드 내에 API 키를 직접 입력하지 않음.
*   **환경 변수(Environment Variables) 활용:** `.env` 파일에 키를 저장하고 `python-dotenv` 등의 라이브러리로 로드.
*   **버전 관리 시스템(Git) 제외:** `.gitignore` 파일에 `.env`를 등록하여 원격 저장소(GitHub 등) 노출 차단.
*   **최소 권한 원칙:** 필요한 기능(Read/Write)에 대해서만 권한이 부여된 키를 생성 및 사용.
*   **Key Rotation:** 주기적으로 API 키를 갱신하여 유출 시 피해 최소화.

### 5. 결론 및 향후 과제
본 학습을 통해 API 연동의 기초인 인증 메커니즘을 명확히 이해하였음. 향후 **OAuth 2.0**과 같은 보다 복잡한 인증 체계로 학습 범위를 확장하고, 실제 데이터 파이프라인 구축 프로젝트에 적용할 계획임.

---
