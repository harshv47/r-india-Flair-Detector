from flask import Flask, request, jsonify
from predictor import get_predictions


app = Flask(__name__)

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
            urls.append(url)
        
        #   Call the function here:
        dict_obj = get_predictions(urls)
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