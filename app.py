from flask import Flask, request, abort, send_from_directory, jsonify, render_template
from werkzeug.utils import secure_filename
import os
import librosa

UPLOAD_DIRECTORY = "/Users/bransonbragg/Deepgram/api_uploaded_files"
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'aiff'}

app = Flask(__name__)
app.config['UPLOAD_DIRECTORY'] = UPLOAD_DIRECTORY

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

AUDIOS = {
    "myfile.wav": {"duration": 33.529625, "name": "myfile.wav"},
    "myfile2.wav": {"duration": 29.628662131519274, "name":"myfile2.wav"}
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
    return [obj for obj in AUDIOS if AUDIOS[obj]]

@app.route('/info', methods=['GET'])
def info():
    name = request.args.get('name')
    if not name:
        return AUDIOS
    elif name not in AUDIOS:
        abort(400, "Please specify a valid filename")
    return AUDIOS[name]

@app.route('/download', methods=['GET'])
def download():
    name = request.args.get('name')
    if not name or name not in AUDIOS:
        abort(400, "Please specify a valid filename")
    return send_from_directory(UPLOAD_DIRECTORY, name, as_attachment=True)

@app.route('/post', methods=['GET'])
def postPage():
    return render_template('upload.html')

@app.route('/post', methods=['POST'])
def post():
    if 'file' not in request.files:
        abort(400, 'No file part')
    file = request.files['file']
    if file.filename in AUDIOS:
        abort(400, "File already exists")
    if file.filename == '':
            abort(400, 'No selected file')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_DIRECTORY'], filename))
        AUDIOS[filename] = {'name': filename, 'duration': librosa.get_duration(filename=UPLOAD_DIRECTORY + '/' + filename)}
    else:
        abort(404, "Invalid file type")
    return jsonify({"response": "success"}), 201

@app.route('/')
def test():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(host="localhost")
    
    """
    Functionality FINISHED: 
    
    /list
        -maxduration
        -minduration
        e.g. curl http://localhost:5000/list
             curl "http://localhost:5000/list?minduration=30"
             curl "http://localhost:5000/list?maxduration=35&minduration=25"
    /info
        -name
        e.g. curl "http://localhost:5000/info?name=myfile2.wav"
             curl http://localhost:5000/info
    /download
        -name
        e.g. curl "http://localhost:5000/download?name=myfile.wav"
    /post
        -file
        e.g. curl -F "file=@myfile.wav" http://localhost:5000/post
        
    Functionality TODO
    
    /list
        Add more filtering functionality
         -- add something new to the AUDIOS json?
    /post
        Make it so that the prompt POST request works
         -- e.g. curl -X POST @myfile.wav http://localhost:5000/post
    """