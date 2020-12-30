from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/webhook",methods=['POST'])
def responseCreator():
    req = request.get_json(silent=True, force=True)
    print(req)
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