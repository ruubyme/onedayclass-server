import pymysql 
from dotenv import load_dotenv
import os 
from dbutils.pooled_db import PooledDB
from flask import g, current_app


# .env.local 파일 로드
load_dotenv('.env.local')

def conn_mysqldb():
  print(os.getenv('DB_HOST'))
  if 'db' not in g or not g.db.is_connected():
    g.db = pymysql.connect(
      host = os.getenv('DB_HOST'),
      user=os.getenv('DB_USER'),
      passwd=os.getenv('DB_PASSWORD'),
      database=os.getenv('DB_NAME'),
      ssl_mode = "VERIFY_IDENTITY",
      ssl_verify_identity=True,
      ssl_ca=os.getenv('SSL'),
      charset='utf8mb4',
    )
    conn, cur = g.db, g.db.cursor(dictionary=True)
  return conn, cur

def close_db(e=None):
  db = g.pop('db', None)
  
  if db is not None and db.is_connected():
    db.close()
    

