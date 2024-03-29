from flask import Flask, render_template
from flask_cors import CORS, cross_origin
from flask_session import Session
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from mysql import conn_mysqldb
from control.user_mgmt import User 
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://onedayclass-frontend-euu7.vercel.app"}})
app.secret_key= os.getenv('SECRET_KEY')
@app.route('/')
def index():
  return render_template('index.html')


#세션 관련 설정 
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#jwtManager 초기화 
jwt = JWTManager(app)

#jwt 토큰의 위치 설정
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"

login_manager = LoginManager()
login_manager.init_app(app)

#사용자 로그인 (login_user 함수 호출 시 자동으로 호출)
@login_manager.user_loader
def load_user(user_id):
  #user_id를 기반으로 사용자 정보 가져오기 
  conn, cur = conn_mysqldb()
  try: 
    cur.execute("SELECT * FROM user_info WHERE user_id = %s", (user_id,))
    user_data = cur.fetchone()
    if user_data:
      return User(user_data['id'], user_data['email'], user_data['name'], user_data['role'], user_data['address'])
    
  except Exception as e:
    print(f"Error fetching user: {e}")
    return None 
  finally:
    cur.close()
    conn.close()

from routes.login import login_blueprint
from routes.signup import signup_blueprint
from routes.class_registration import register_class_blueprint
from routes.class_info import class_info_blueprint
from routes.class_booking import class_booking_blueprint
from routes.user_info import user_info_blueprint
from routes.instructor import instructor_blueprint
from routes.review import review_blueprint
#블루프린트 등록 
app.register_blueprint(login_blueprint)
app.register_blueprint(signup_blueprint)
app.register_blueprint(register_class_blueprint)
app.register_blueprint(class_info_blueprint)
app.register_blueprint(class_booking_blueprint)
app.register_blueprint(user_info_blueprint)
app.register_blueprint(instructor_blueprint)
app.register_blueprint(review_blueprint)

@app.route('/print')
@cross_origin()
def print_hello():
  return("hello")

if __name__ == '__main__':
  app.run(port=5000)
