from flask import Flask, request, abort, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os
import librosa

UPLOAD_DIRECTORY = "/Users/bransonbragg/Deepgram/api_uploaded_files"
ALLOWED_EXTENSIONS = {'wav'}

app = Flask(__name__)
app.config['UPLOAD_DIRECTORY'] = UPLOAD_DIRECTORY

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

AUDIOS = {
    'myfile.wav': {'name': 'myfile.wav', 'duration': 34},
    'myfile2.wav': {'name': 'myfile2.wav', 'duration': 40}
}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/list', methods=['GET'])
def list():
    max_duration = request.args.get('maxduration')
    min_duration = request.args.get('minduration')
    if min_duration and max_duration:
        return [obj for obj in AUDIOS if (AUDIOS[obj]['duration'] <= int(max_duration) 
                                          and AUDIOS[obj]['duration'] >= int(min_duration))]
    elif max_duration:
        return [obj for obj in AUDIOS if (AUDIOS[obj]['duration'] <= int(max_duration))]
    elif min_duration:
        return [obj for obj in AUDIOS if (AUDIOS[obj]['duration'] >= int(min_duration))]
    return AUDIOS

@app.route('/info', methods=['GET'])
def info():
    name = request.args.get('name')
    if not name:
        return AUDIOS
    elif name not in AUDIOS:
        abort(404, "Please specify a valid filename")
    return AUDIOS[name]

@app.route('/download', methods=['GET'])
def download():
    name = request.args.get('name')
    if not name or name not in AUDIOS:
        abort(404, "Please specify a valid filename")
    return send_from_directory(UPLOAD_DIRECTORY, name, as_attachment=True)

@app.route('/post', methods=['POST'])
def post():
    # return jsonify(request.files['file'])
    if 'file' not in request.files:
        abort(404, 'No file part')
    file = request.files['file']
    if file.filename == '':
            abort(404, 'No selected file')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_DIRECTORY'], filename))
        AUDIOS[filename] = {'name': filename}
    else:
        abort(404, "Invalid file type")
    return jsonify({"response": "success"})

@app.route('/')
def test():
    return "Hello World!"

if __name__ == '__main__':
    app.run(host="localhost")