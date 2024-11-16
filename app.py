from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime

app = Flask(__name__)

# Flask-Mail 설정
app.config['MAIL_SERVER'] = 'smtp.gmail.com' # SMTP 서버 주소
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'example@gmail.com' # 이메일 계정
app.config['MAIL_PASSWORD'] = '1234' # 발급받은 이메일 계정 비밀번호
app.config['MAIL_DEFAULT_SENDER'] = 'example@gmail.com'
mail = Mail(app)
serializer = URLSafeTimedSerializer("your-secret-key")

# 간단한 메모리 저장소
users={}
tokens={}


# 0. 기본 홈페이지
@app.route('/')
def index():
    return render_template('index.html')

# 1. 회원 가입
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    birthday = data.get('birthday')
    
    if not username or not password or not birthday:
        return jsonify({"success" : False, "error" : "입력 양식 오류"}), 400
    
    if not username in users:
        return jsonify({"success" : False, "error" : "이미 존재하는 사용자"}), 400
    
    # 사용자 저장
    users[username] = {
        "password" : password,
        "birthday" : birthday,
        "verified-email" : False        
    }
    return jsonify({"message" : "회원 가입 성공!"}), 201

# 2. 이메일 입력
@app.route('/verify_email', methods=['POST'])
def verify_email():
    if request.method == 'GET':
        return render_template('verify_email.html')
    # POST 요청 처리    
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({"success" : False, "error" : "입력 양식 오류"}), 400
    
    try:
        # 토큰 생성
        token = serializer.dumps(email, salt="email-confirm")
        tokens[email] = token
        
        # 이메일 전송
        msg = Message("익명 투표를 위한 인증 링크", recipients=[email])
        msg.body = f"다음 링크를 클릭하여 이메일을 인증해주세요 : http://localhost:5000/api/auth/confirm-email?email={email}&token={token}"
        mail.send(msg)
        return jsonify({"success" : True, "data" : {}}), 201
    
    except Exception as e:
        print(e)
        return jsonify({"success" : False, "error" : "이메일 전송 실패"}), 500

# 3. 이메일 인증
@app.route('/confirm_email', methods=['POST'])
def confirm_email():
    if request.method == 'GET':
        return render_template('confirm_email.html')
    # POST 요청 처리
    data = request.get_json()
    email = data.get('email')
    token = data.get('token')
    
    if not email or not token:
        return jsonify({"success" : False, "error" : "입력 양식 오류"}), 400
    
    try:
        # 토큰 검증
        decoded_email = serializer.loads(token, salt="email-confirm", max_age=3600)
        
        if decoded_email != email:
            return jsonify({"success" : False, "error" : "잘못된 코드"}), 400
        
        # 사용자 이메일 인증
        for user in users.values():
            if user.get("email") == email:
                user["verified_email"] = True
                break
        
        return jsonify({"success":True, "data":{}}), 201
    
    except Exception as e:
        print(e)
        return jsonify({"success":False, "error":"토큰 인증 실패!"}), 500

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)


