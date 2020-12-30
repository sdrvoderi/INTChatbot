from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/webhook",methods=['POST'])
def responseCreator():
    return {
            "fulfillmentMessages": [
                {
                "text": {
                    "text": [
                    "Text response from weabhook"
                    ]
                }
                }
            ]
            }