import mysql.connector
import requests
import json
import sys
from gtts import gTTS
from playsound import playsound

# MySQL 서버 연결 정보
db_connection = mysql.connector.connect(
    host="localhost",
    user="plab",
    password="plab",
    database="exampledb"
)

# 커서 생성
db_cursor = db_connection.cursor()

try:
    # ingredient_name 가져오기 쿼리 실행
    query = "SELECT ingredient_name FROM ingredient_storage"
    db_cursor.execute(query)

    # 결과 가져오기
    ingredient_names = db_cursor.fetchall()

    # 식재료 리스트 생성
    ingredients = [name[0] for name in ingredient_names]

    # 음식 추천을 위한 챗봇 API 요청
    url = "http://192.168.0.4:11434/api/generate"
    payload = {
        "model": "tinyllama",
        "prompt": "Tell me what food I can make with {}?".format(", ".join(ingredients))
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        response_text = ""
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                if "response" in data:
                    response_text += data["response"]
        print("Response:", response_text.strip())
        tts = gTTS(text=response_text, lang='en')
        tts.save("output.mp3")
        # 음성 재생
        playsound("output.mp3")

    else:
        print("Error:", response.status_code)

except mysql.connector.Error as err:
    print("MySQL 오류: {}".format(err))

finally:
    # 연결 닫기
    if db_connection.is_connected():
        db_cursor.close()
        db_connection.close()
