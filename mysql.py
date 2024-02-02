import pymysql 
from dotenv import load_dotenv
import os 
from dbutils.pooled_db import PooledDB
from flask import g


# .env.local 파일 로드
load_dotenv('.env.local')

def conn_mysqldb():
  print(os.getenv('MYSQLHOST'))
  if 'db' not in g or not g.db.is_connected():
    g.db = pymysql.connect(
      host = os.getenv('MYSQLHOST'),
      user= os.getenv('MYSQLUSER'),
      passwd=os.getenv('MYSQLPASSWORD'),
      database=os.getenv('MYSQLDATABASE'),
      port=int(os.getenv('MYSQLPORT')),
      charset='utf8mb4',
    )
    conn, cur = g.db, g.db.cursor(pymysql.cursors.DictCursor)
  return conn, cur

def close_db(e=None):
  db = g.pop('db', None)
  
  if db is not None and not db.closed:
    db.close()
    

