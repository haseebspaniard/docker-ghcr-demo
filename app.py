from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Haseeb's Dockerized App v2 — CI/CD pipeline confirmed working on every release!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)