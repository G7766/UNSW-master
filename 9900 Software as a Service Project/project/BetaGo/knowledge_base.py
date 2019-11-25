from flask import Flask, render_template,request
import requests



app = Flask(__name__)

@app.route('/')
def knowledge_base():
    return render_template('knowledge_base.html')

@app.route('/submit_knowledge', methods=['POST'])
def create_knowledge():
    keyword = request.form["keyword"]
    description = request.form["description"]
    print(keyword)
    print(description)

    return render_template('knowledge_base.html')
# @app.route('/submit_knowledge', methods=['GET'])
# def create_knowledge():
#     response = requests.get('http://127.0.0.1:5000/submit_knowledge')
#     print(response)
#     item = response.json()
#     print(item)

if __name__ == "__main__":
    app.run(debug=True)
    a = "http://google.com/search?q=what is CNN"