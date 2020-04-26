from flask import Flask, request, jsonify, render_template, session,
from flask_wtf import FlaskForm
from wtforms import TextField,SubmitField
from wtforms.validators import NumberRange
from predictor import get_predictions



app = Flask(__name__)

class FlowerForm(FlaskForm):
    sep_len = TextField(‘Sepal Length’)
    submit = SubmitField(‘Analyze’)

@app.route('/')
def handle_root():

@app.route('/result',methods = ['POST'])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        pred = get_predictions(to_predict_list)

        return render_template("result.html",prediction=pred)

@app.route('/automated_testing', methods=['GET', 'POST'])
def handle_req():
    if request.method == 'POST':
        file = request.files['file']
        text_file = file
        lines = text_file.readlines()
        dict_obj = {}
        urls = []
        for line in lines:
            url = line.strip()
            url_s = str(url, 'utf-8')
            urls.append(url_s)
        
        #   Call the function here:
        dict_obj = get_predictions(urls)
        #print(dict_obj)
        resp = {
            'status': 200,
            'message': 'The data is under data, Thanks',
            'data': dict_obj
        }

    else:
        resp = {
            'status': 400,
            'message': 'Please send a POST request',
        }
    return jsonify(resp)


if __name__ == '__main__':
    app.run(debug=True)