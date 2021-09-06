from flask import Flask,render_template,request

app = Flask(__name__)

@app.route('/')
def mode():
    return render_template('mode.html')

app.route('/setting.html',methods=['POST'])
def getValue():
    B0 = request.form['B0']
    B1 = request.form['B1']
    B2 = request.form['B2']
    B3 = request.form['B3']
    B4 = request.form['B4']
    B5 = request.form['B5']
    B6 = request.form['B6']
    return 