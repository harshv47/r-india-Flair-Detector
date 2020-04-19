from flask import Flask, request, jsonify
# Import your python file for prediting flair


app = Flask(__name__)

@app.route('/automated_testing', method=['POST'])
def handle_req():
    if request.method == 'POST':
        text_file = request.files['.+.txt']
        lines = text_file.readlines()
        dict_obj = {}
        resp = {
            'status': 200,
            'message': 'The data is under data, Thanks',
            'data': dict_obj
        }
        for line in lines:
            url = line.strip()
            # Call the function here to predict flair
            flair = "Flair"
            # Assuming the flair data is strored in flair
            dict_obj[url] = flair
    else:
        resp = {
            'status': 400,
            'message': 'Please send a POST request',
        }
    return jsonify(resp)


if __name__ == '__main__':
    app.run(debug=True)