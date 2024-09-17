from flask import Flask
import random

app = Flask(__name__)

@app.route('/')
def random_response():
    if random.choice([True, False]):
        return "OK", 200
    else:
        return "Internal Server Error", 500

if __name__ == '__main__':
    app.run(debug=True)
