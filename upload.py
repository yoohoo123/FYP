from flask import *
from flask_pymongo import PyMongo
from flask_mongoengine import MongoEngine
import pymongo
# import bcrypt
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'Fyp-Test'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Fyp-Test'

mongo = PyMongo(app)

UPLOAD_FOLDER = 'app/uploaded_files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #Max of 16MB
app.config['UPLOAD_PATH'] = ''
   
ALLOWED_EXTENSIONS = set(['csv', 'xlsx', 'xls', 'txt'])

db = MongoEngine()
db.init_app(app)  

class User(db.Document):
    filepath = db.StringField()
   
def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['inputFile']
    filename = secure_filename(file.filename)
   
    if file and allowed_file(file.filename):
       file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
       usersave = User(filepath=file.filename)
       usersave.save()
       flash('File successfully uploaded ' + file.filename + ' to the database!')
       return redirect('index.html')
    else:
       flash('Invalid Uplaod only csv , xlsx, xls, txt files') 
    return redirect('error.html')    

# if __name__ == '__main__':
#     app.run(debug=True)
    