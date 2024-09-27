## 디스코드 음악봇 "Raccoon"

![다운로드](https://github.com/user-attachments/assets/d0f28f10-28d5-4baf-8a12-88a458aaf1a5)

### 제작 목적
- 최근 퍼블릭 음악봇들이 자주 고장나는 바람에 사람들이 불편을 호소함.
- 이로 인해 서버 고유의 음악봇을 의뢰 받아 제작하게 됨.

### 지원되는 기능
- 입장 : >j 혹은 >p
- 퇴장 : >x
- 재생 : >p (Playlist 목록 추가 가능)
- 볼륨 조절 : >v 0 ~ 100
- 일시 중지 : >ps 혹은 Pause 버튼
- 다시 재생 : >rs 혹은 Resume 버튼
- 이전 재생 : >b 혹은 Back 버튼
- 예약 취소 : >e int
- 순서 변경 : >m int int (현재 위치, 이동할 위치)
- 셔플 : >sh 혹은 Shuffle 버튼
- 재생 목록 : >pl 혹은 Playlist 버튼
- 스킵 : >s 혹은 Skip 버튼
- 반복 : >r 혹은 Repeat 버튼
- 도움말 : >h 혹은 Help 버튼

### 주의 사항
- dico_token.py 는 직접 만들어야 합니다.
- dico_token.py 에는 Token 변수와 ID 변수가 들어있습니다.
  - Token : Discord Developer 에서 발급받은 봇 token
  - ID : 적용하고자 하는 서버의 채널 ID (개발자 모드로 확인 가능)
- 배포는 docker 로 진행했습니다. Dockerfile 은 다음과 같습니다.
```python
# 베이스 이미지로 Python 3.8 사용
FROM python:3.8-slim

# 작업 디렉토리 설정
WORKDIR /app

# ffmpeg 및 기타 필수 패키지 설치
RUN apt-get update && apt-get install -y ffmpeg

# 필요 파일을 컨테이너로 복사
COPY requirements.txt requirements.txt
COPY . .

# 필요한 Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 디스코드 봇 실행
CMD ["python", "main.py"]
```

- 위 requirements.txt 은 해당 레포지토리를 clone 받은 위치에 생성하면 됩니다.
```
discord.py
yt-dlp
pynacl
ffmpeg-python
```
- AWS EC2 나 Google Cloud 와 같은 곳에서 배포를 진행할 경우 다음과 같은 에러가 발생할 수 있습니다. 
```
ERROR: [youtube] xxxxxxxx: Sign in to confirm you’re not a bot. This helps protect our community.
```
- 이 경우 웹 브라우저에서 로그인한 상태로 Cookies.txt 를 뽑아내 서버로 옮겨 속이는 방법이나 VPN을 사용하는 방식 등을 사용해야 합니다. 
- 환경에 따라 다르니 직접 확인하시길 바랍니다.

