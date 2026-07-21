from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Haseeb's Dockerized App — deployed via GitHub Actions to GHCR!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)