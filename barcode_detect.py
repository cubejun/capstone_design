import cv2
from pyzbar.pyzbar import decode
import requests
import mysql.connector
import pyttsx3
import time
import numpy as np

# MySQL 데이터베이스 연결 설정
db_connection = mysql.connector.connect(
    host="localhost",
    user="plab",
    password="plab",
    database="exampledb"
)
db_cursor = db_connection.cursor()

# 카메라 설정
cap = cv2.VideoCapture(0)

# Pyttsx3 초기화
engine = pyttsx3.init()

# 이전에 바코드를 인식한 시간
last_barcode_time = 0

# 카메라 영역 설정
# 좌상단과 우하단 좌표 (x, y, width, height)
camera_roi = (100, 100, 400, 300)  # 예시: (100, 100)에서 (500, 400)까지의 영역

while True:
    ret, frame = cap.read()

    current_time = time.time()
    # 바코드 인식 후 5초가 지나면 다시 바코드를 인식하도록 합니다.
    if current_time - last_barcode_time > 5:
        # 카메라 영역 내에서만 프레임 자르기
        roi_frame = frame[camera_roi[1]:camera_roi[1] + camera_roi[3], camera_roi[0]:camera_roi[0] + camera_roi[2]]

        # 프레임에서 바코드 읽기
        decoded_objects = decode(roi_frame)

        for obj in decoded_objects:
            # 바코드가 카메라 영역 내에 있을 때만 처리
            if obj.rect[0] >= 0 and obj.rect[1] >= 0 and obj.rect[0] + obj.rect[2] <= camera_roi[2] and obj.rect[1] + obj.rect[3] <= camera_roi[3]:
                # 바코드 정보 출력
                print("바코드 타입:", obj.type)
                print("바코드 데이터:", obj.data.decode())

                # 바코드 번호 추출
                barcode_data = obj.data.decode()

                # 데이터베이스에 이미 존재하는지 확인
                db_cursor.execute("SELECT * FROM Barcode_prototype WHERE barcode_data = %s", (barcode_data,))
                existing_barcode = db_cursor.fetchone()

                if existing_barcode:
                    # 이미 존재하는 경우, 검출 횟수를 증가시키고 업데이트
                    update_sql = "UPDATE Barcode_prototype SET detection_count = detection_count + 1 WHERE barcode_data = %s"
                    db_cursor.execute(update_sql, (barcode_data,))
                    db_connection.commit()
                    message = "바코드 정보가 업데이트되었습니다."
                else:
                    # 바코드 API를 통해 바코드 정보 가져오기
                    api_key = "1ea48afacf1b417c95ce"
                    service_name = "I2570"
                    file_type = "json"
                    start_pos = 1
                    end_pos = 5
                    api_url = f"http://openapi.foodsafetykorea.go.kr/api/{api_key}/{service_name}/{file_type}/{start_pos}/{end_pos}/BRCD_NO={barcode_data}"
                    
                    response = requests.get(api_url)

                    if response.status_code == 200:
                        barcode_info = response.json()
                        print("바코드 정보:", barcode_info)
                        
                        # 데이터베이스에 바코드 정보 저장
                        if 'row' in barcode_info[service_name]:
                            for row in barcode_info[service_name]['row']:
                                prdlst_report_no = row['PRDLST_NM']
                                prdlst_nm = row['PRDT_NM']
                                price = row['CMPNY_NM']

                                sql = "INSERT INTO Barcode_prototype (barcode_data, prdlst_report_no, prdlst_nm, price, detection_count) VALUES (%s, %s, %s, %s, 1)"
                                val = (barcode_data, prdlst_report_no, prdlst_nm, price)
                                db_cursor.execute(sql, val)
                                db_connection.commit()
                                message = "바코드 정보가 데이터베이스에 저장되었습니다."
                        else:
                            message = "바코드 정보가 없습니다."
                    else:
                        message = "바코드 API에 접근할 수 없습니다."

                # 바운딩 박스 그리기 (카메라 영역 내에서의 위치로 변경)
                (x, y, w, h) = obj.rect
                cv2.rectangle(roi_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                # 바코드 데이터 표시 (카메라 영역 내에서의 위치로 변경)
                cv2.putText(roi_frame, obj.data.decode(), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # TTS로 메시지 출력
                engine.say(message)
                engine.runAndWait()

                # 바코드가 인식되었음을 표시하고 현재 시간 기록
                last_barcode_time = current_time

    # 프레임에 배경 어둡게 만들기
    background = np.ones(frame.shape, dtype=np.uint8) * 50
    cv2.rectangle(background, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 0), -1)  # 프레임 전체를 어둡게 만듦
    cv2.rectangle(background, (camera_roi[0], camera_roi[1]), (camera_roi[0] + camera_roi[2], camera_roi[1] + camera_roi[3]), (255, 255, 255), -1)  # 관심 영역은 원래 밝기로 유지
    frame_darkened = cv2.addWeighted(frame, 0.7, background, 0.3, 0)

    cv2.imshow('frame', frame_darkened)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 종료
cap.release()
cv2.destroyAllWindows()
