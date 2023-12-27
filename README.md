# [HI041]PC 로그 이상탐지
- 프로젝트 KPT회고 링크 : https://codingjang.tistory.com/74
- 시연 연상 링크: https://youtu.be/JTNASB0PRjg
--- 
## 프로젝트 소개
- IT기술이 발전함에 따라 pc 내에서 관리해야 할 자원들이 많아지고 복잡해지고 있다. 이에 따라 pc에 이상이 발생할 경우 문제의 원인을 파악하기 어려운 현상이 발생한다.
- 사용자 pc를 안정적으로 운용하기 위해 pc에서 발생하는 성능 및 이벤트 로그 데이터를  수집 후 저장 및 시각화하는 서비스를 제작하려고 한다.

## 적용기술 및 아키텍처
-  Isolation Forest: 이상치 탐지(anomaly detection)를 위한 기계 학습 알고리즘 모델이다. 이 알고리즘은 특히 대규모 데이터 세트에 효과적이며, 이상치가 상대적으로 적은 경우에 특히 유용하다.
- 지표 모니터링: kibana를 사용하여 실시간 사용자 PC의 지표를 시각화하여 확인 및 대응 할 수 있도록 도움을 준다.
- PC 지표 추출: metricbeat를 이용하여 PC의 주요 리소스인 메모리, 네트워크를 추출

### 개발 환경
![개발환경 이미지](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcvrDt9%2FbtsCF8GMuRF%2FtGCC9UT2GRn4wK72kWLN21%2Fimg.png)

### 아키텍처
![아키텍처 이미지](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FdvOX7J%2FbtsCG1t9YsZ%2FM8PZuu4MKgS4EmcZLt54D1%2Fimg.png)

## 주요기능
- 지표 추출 : metricbeat를 사용하여 사용자의 network 지표를 추출
- 실시간 데이터 처리 : kafka를 사용하여 네트워크 지표 전달 
- 데이터 시각화 : ELK Stack을 사용하여 전달받은 지표를 시각화
- DB: DynamoDB를 사용하여 네트워크 지표 저장
- 알람 서비스: 이상치가 탐지되면 노션에 문제상황 자동으로 글쓰기

## 수행 일정
![수행일정 이미지](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FdM8a0G%2FbtsCy6Q1A8a%2Fw4mC4hP18zAvHyrrkenaKk%2Fimg.png)