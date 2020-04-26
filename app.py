from flask import Flask, render_template, flash, request, jsonify, redirect
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from predictor import get_predictions
from forms import DataForm


app = Flask(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6145f'

@app.route('/', methods=['GET', 'POST'])
def handle_root():
    form = DataForm()
    if form.validate_on_submit():
        urls = [form.url.data]
        pred = get_predictions(urls)
        
        flash('The flair is {}'.format(pred[urls[0]]))
        return redirect('/')
    return render_template('index.html', title='Reddit Flair Predictor', form=form)


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