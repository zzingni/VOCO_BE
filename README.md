# 🎙️ VOCO - AI Interview Service (Backend)

VOCO는 AI 기반 맞춤형 면접 연습 서비스를 제공하는 백엔드 API 서버입니다.  
사용자의 자기소개서, 지원 기업 및 직무 정보를 유기적으로 분석하여 고도화된 맞춤형 질문을 생성하고, 다각도 AI 엔진을 통해 답변을 정밀하게 채점합니다.

---

## 🧱 Tech Stack

* **Framework:** FastAPI
* **Language:** Python
* **ORM:** SQLAlchemy
* **Database:** PostgreSQL
* **AI Model:** OpenAI GPT-4o-mini / Whisper API
* **External Data:** Web Crawling (BeautifulSoup / Selenium)
* **Env Management:** python-dotenv

---

## 🚀 Key Features

### 1. Kakao OAuth 2.0 인증 및 회원 관리
* 카카오 인증 서버를 통한 안전한 로그인 처리 및 사용자 정보 연동
* **최초 로그인 시:** 유저 정보(ID, 이메일, 닉네임)를 PostgreSQL에 자동 적재(회원가입)
* **기존 회원:** 세션/토큰 발행을 통한 즉각적인 로그인 처리

### 2. 컨텍스트 기반 AI 질문 생성
* 사용자의 자기소개서(장단점, 지원동기, 문제해결, 포부)와 크롤링된 기업 정보를 매핑
* GPT-4o-mini 엔진과 프롬프트 엔지니어링을 활용해 **맞춤형 면접 질문 5개** 생성
* 안정적인 데이터 파싱을 위해 **Structured JSON Outputs** 형식 강제 적용

### 3. 직무(Field)별 질문 조회
* 프론트엔드에서 요청한 직무 식별자(`field_id`)를 기반으로 타겟팅된 질문 리스트 필터링 및 응답

### 4. 듀얼 모드 AI 답변 평가 시스템 (핵심 기능)
* 사용자의 답변 품질을 평가 유형(`question_type`)에 따라 이원화된 로직으로 채점

> **📐 공통 평가 지표 (총점 100점)**
> * 질문 적합성 (40점) / 답변 구조 (20점) / 전달력 (20점) / 반복 표현 (20점)

* **FIELD (직무 질문) 타입:** 기업/문화적 요소는 완전히 배제하고, 해당 직무를 수행하기 위한 **핵심 하드 스킬과 전문 역량**만을 집중 평가
* **RESUME (자소서 질문) 타입:** 수집된 **기업의 인재상, 조직 문화, 기술적 방향성**과의 정렬도를 반영하여 종합 평가 (단, 답변 자체의 논리 구조 품질을 최우선으로 산정)

---

## 🔗 API Specifications

### Auth (인증)
* `/auth/kakao/login` - 카카오 로그인 페이지 리다이렉트
* `/auth/kakao/callback` - 인가 코드를 통한 토큰 발급 및 유저 검증

### Questions (질문 서비스)
* `/questions` - 특정 직무(`fieldId`) 전용 면접 질문 데이터 로드
* `/questions/generate` - 자기소개서 및 기업 정보 기반 AI 질문 생성 

### Answers & Feedback (평가 서비스)
* `/answers` - 오디오(Whisper STT 변환) 및 텍스트 답변 수령 및 저장
* `/feedback` - `FIELD` / `RESUME` 타입별 채점 알고리즘이 적용된 피드백 및 스코어 반환

---

## 📁 Project Structure

```bash
app/
├── api/          # API 엔드포인트 라우터 정의 (auth, questions, feedback 등)
├── core/         # 외부 API 커넥터 및 환경 설정 (OpenAI, Kakao Config)
├── db/           # 데이터베이스 연결 설정 및 SQLAlchemy 세션 관리
├── models/       # 데이터베이스 테이블 관계 및 스키마 정의 (User, Question, Answer 등)
├── services/     # 핵심 도메인 비즈니스 로직 (AI 프롬프팅, 타입별 평가 알고리즘, 크롤링)
└── utils/        # 공통 가독성을 위한 파서 및 헬퍼 함수
