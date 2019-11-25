from flask import Flask
from flask import request,make_response,jsonify
app = Flask(__name__)

# web hook server
@app.route('/webhook',methods= ['POST','GET'])
def webhook():
    req = request.get_json(silent=True)
    return jsonify(req)
