# 스마트 냉장고
## 조원 : 김경섭 김락준 박상원 장호균 최영준
## -개발 목표
스마트 냉장고
## -개발 내용
객체인식을 이용해 식품 DB에 저장

냉장고에 넣은 날짜, 유통기한 확인 기능

챗봇을 이용해 보관중인 식재료를 이용한 레시피 제공

라즈베리파이 서버를 이용해 냉장고에 보관중인 식품을 핸드폰에서 확인




![image](https://github.com/cubejun/capstone_design/assets/133946040/8f79bcb8-846f-4ac1-82cb-59325de95391)


----------------------------------------------------------------------------------------------------------------
4월 7일
![image](https://github.com/cubejun/capstone_design/assets/133946040/f8bd1b22-9b58-4da4-bc4b-ce2097b0458d)
![image](https://github.com/cubejun/capstone_design/assets/133946040/2483f560-f580-4110-9290-29c26e3a240c)
https://www.foodsafetykorea.go.kr/api/openApiInfo.do?menu_grp=MENU_GRP31&menu_no=656&show_cnt=10&start_idx=1&svc_no=I2570&svc_type_cd=API_TYPE06

http://openapi.foodsafetykorea.go.kr/api/{api_key}/I2570/json/1/5/BRCD_NO={barcode_data}
![image](https://github.com/cubejun/capstone_design/assets/133946040/9d2e6a4a-32d9-4b0f-837a-a4d45e25259e)

동작영상


https://github.com/cubejun/capstone_design/assets/133946040/c4126a41-9793-4a20-8e2c-39e15648f00f

----------------------------------------------------------------------------------------------------------------------

4월 28일

ollama 서버 구성
sudo nano /etc/systemd/system/ollama.service
수정 Environment="OLLAMA_HOST=0.0.0.0"

![image](https://github.com/cubejun/capstone_design/assets/133946040/aeb036d1-72f1-4b45-b19f-d29334712eb0)
https://github.com/ollama/ollama/blob/main/docs/faq.md




