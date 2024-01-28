from flask import Flask, render_template
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://todo-list-typescript-git-feat-todo-edit-ruubyme.vercel.app/"}})

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/print')
@cross_origin()
def print_hello():
  return("hello")

if __name__ == '__main__':
  app.run(port=5000)
