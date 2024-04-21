from flask import Flask, request, jsonify

# Flask 애플리케이션 생성
app = Flask(__name__)

'''
Q. 안녕하세요, GI/GU team DHL 배송 입력기 입니다, 초기세팅에 필요한 내용 전달 부탁드립니다.
A
이름 :  # 엑셀 H5 부분에 기입
영어이름 : # invoice shippers name (200,745)에 기입
네이버 이메일 :  # ID
네이버 비밀번호 : # PW
invoice 받을 원내 이메일 : #himchan1.lee@sbri.co.kr(각자 원내 아이디 입력)
print ('초기 셋팅이 완료 되었습니다, 초기셋팅을 변경하고 싶으시면 "초기셋팅 변경" 이라고 해주세요.)
'''
@app.route('/message', methods=['POST']) # Test
def message():
    print('/message로 넘어왔습니다.')
    data = request.get_json()
    print(data)
    content = data['content']  # 사용자의 메시지 내용


    response = {
        "version": "2.0",
        "template": {
            "outputs": [{
                "simpleText": {
                    "text": "응답 메시지"
                }
            }]
        }
    }
    if content == "안녕하세요":
        response['template']['outputs'][0]['simpleText']['text'] = "GI/GU team DHL 배송 입력기 입니다, 초기세팅에 필요한 내용 전달 부탁드립니다."
    elif content == "교수님 설정을 해주세요":
        response['template']['outputs'][0]['simpleText']['text'] = "홍정용, 이지연 등 교수님 설정이 완료되었습니다."
    elif content == "픽업시간":
        response['template']['outputs'][0]['simpleText']['text'] = "설정이 완료되었습니다."
    elif "초기셋팅 변경" in content:
        response['template']['outputs'][0]['simpleText']['text'] = "초기셋팅 변경을 도와드리겠습니다."
    # 추가적인 조건과 로직을 여기에 구현합니다.

    return jsonify(response)



# 루트 URL에 대한 핸들러 함수
@app.route('/')
def hello_world():

    return '서버가 돌아가는 중입니다.'
 

# 애플리케이션 실행
if __name__ == '__main__':
    app.run(debug=True, port=8000)
