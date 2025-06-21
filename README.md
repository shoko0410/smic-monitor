# SMIC Research 페이지 자동 알리미

**이 프로젝트는 서울대학교 투자연구학회 SMIC의 Research 페이지에 새로운 게시물이 올라오는지 감시하기 위해 특별히 설정되었습니다.**

지정된 웹사이트의 RSS 피드를 주기적으로 모니터링하여 새로운 게시물이 등록되면, 게시물 정보와 PDF 다운로드 링크를 포함하여 이메일로 알려주는 시스템입니다. 

## ✨ 주요 기능

- **RSS 기반 모니터링**: 1분마다 SMIC의 RSS 피드를 확인하여 신규 게시물을 안정적으로 감지합니다.
- **PDF 링크 자동 추출**: 게시물 내용에서 PDF 다운로드 링크를 추출하여 알림 메일에 포함합니다.
- **Docker 기반**: Docker만 설치되어 있으면 단 한 줄의 명령어로 실행 가능합니다.
- **쉬운 설정**: `.env` 파일을 통해 알림받을 이메일 정보를 쉽게 설정할 수 있습니다.

## 🚀 시작하기

### 사전 준비 사항

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### 설치 및 실행

1.  **프로젝트 클론**
    ```bash
    git clone https://github.com/shoko0410/smic-monitor.git
    cd smic-monitor
    ```

2.  **환경 변수 설정**
    `.env.example` 파일을 복사하여 `.env` 파일을 만듭니다.
    ```bash
    cp .env.example .env
    ```
    그런 다음, `.env` 파일을 열어 자신의 환경에 맞게 값을 수정합니다.

3.  **Docker 컨테이너 실행**
    ```bash
    docker-compose up -d --build
    ```

## 🛠️ 사용법

- **로그 확인**: `docker-compose logs -f`
- **서비스 중지**: `docker-compose down`

## 📄 라이선스

This project is licensed under the MIT License.
