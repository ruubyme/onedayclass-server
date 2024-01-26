from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/print')
def print_hello():
  return("hello")

if __name__ == '__main__':
  app.run(port=5000)
