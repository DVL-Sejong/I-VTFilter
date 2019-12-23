## I-VT Fixation Filter

#### packaging

- data
  - raw data
  - csv 파일
- image
  - 배경
- result
  - 각 raw data마다 디렉토리 있음
    - 예) tdata1
    - 디렉토리 내부에 있는 디렉토리의 이름은 fixation 갯수 의미
  - 각 raw data마다 result 내부에 csv파일로 분석 결과 저장함
- source codes
  - constant.py
  - Data.py
  - FileHandler.py
  - ImageHandler.py
  - IVTUtil.py
  - main.py
  - VectorUtil.py



### Source Code

#### main.py

- raw data 분석: analyze_raw_data()
  - data 디렉토리에서 csv 파일 가져와 한꺼번에 분석
  - result에 이미지, 결과 csv 파일 저장
- 이미지 분류: move_images()
  - result 내부에 저장된 csv 파일 분석해 이미를 fixation 갯수를 기준으로 분류
- 결과 분석: main()
  - result 내부에 저장된 csv 파일 분석, velocity에 따른 fixaion 갯수 그래프로 표현해 저장
  - velocity 갯수, 평균 수, 최솟값, 최댓값, 표준편차, 분산
  - fixation 갯수, 평균 수, 최솟값, 최댓값, 표준편차. 분산



#### Data.py

- GazeData class
  - id, name, time, order, point, movement_type
  - VO처럼 사용함



#### FileHandler.py

- 파일 입출력과 관련 메소드



#### ImageHandler.py

- matplotlib 관련 메소드



#### I-VTUtil.py

- I-VT 구현과 관련 메소드



#### VectorUtil.py

- Point3D class
- Point2D class
- VO처럼 사용함