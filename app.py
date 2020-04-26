from flask import Flask, render_template, flash, request, jsonify
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from predictor import get_predictions



app = Flask(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6145f'

class ReusableForm(Form):
    url = TextField('Please enter the post link', validators=[validators.required()])
    
    @app.route("/", methods=['GET', 'POST'])
    def hello():
        form = ReusableForm(request.form)
    
        print(form.errors)
        if request.method == 'POST':
            url=request.form['url']
            pred = get_predictions(url)
    
        if form.validate():
            flash(pred)
        else:
            flash('Link is required. ')
    
        return render_template('index.html', form=form)

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