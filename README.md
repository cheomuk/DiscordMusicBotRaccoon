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
