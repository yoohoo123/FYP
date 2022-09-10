#Restrictions
#Can only import csv files
#No logout yet
#Localhost only



from flask import Flask, render_template,request, url_for, redirect ,flash
from flask_mongoengine import MongoEngine
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from flask_pymongo import PyMongo
import os
import urllib.request
import pandas as pd
import glob

from login import *
from upload import *

#Connect to localhost mongodb
app = Flask(__name__)

#Mongodb details
app.config['MONGO_DBNAME'] = 'Fyp-Test'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Fyp-Test'

mongo = PyMongo(app)

#Conditions for uploading
UPLOAD_FOLDER = 'app/uploaded_files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #Max of 16MB
app.config['UPLOAD_PATH'] = ''
   
ALLOWED_EXTENSIONS = set(['csv', 'xlsx', 'xls', 'txt'])

#User
db = MongoEngine()
db.init_app(app)  

class User(db.Document):
    filepath = db.StringField()
    

client = MongoClient("localhost", 27017, maxPoolSize=50)


@app.route('/')
def main():
    return render_template('loginpage.html')

#Login session
@app.route('/loginpage', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return render_template('upload.html')

    return render_template('error.html')

#Register session
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return 'Successfully created!'
        
        return 'That username already exists!'

    return render_template('register.html')

# @app.route('/logout')
# def logout():
#     # remove the username from the session if it's there
#     session.pop('username', None)
#     return redirect(url_for('index'))

def allowed_file(filename):
     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
def ReadALLFiles(filepath):
        #Import all csv files in the directory
        all_files = glob.glob(filepath)
        data_file = []
        for filename in all_files:
            df = pd.read_csv(filename, index_col=None, header=0,encoding='latin-1')
            data_file.append(df)

        df = pd.concat(data_file, axis=0, ignore_index=False)
        
        return df
    
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['inputFile']
    filename = secure_filename(file.filename)
   
    # create the folders when setting up your app
    os.makedirs(os.path.join(app.instance_path, 'uploaded_files'), exist_ok=True)

    if file and allowed_file(file.filename):
        #Upload to local filepaths
        if file !='': 
            file_path = os.path.join(app.instance_path,'uploaded_files' , filename)
            file.save(file_path)
            usersave = User(filepath=file.filename)
            usersave.save()
            #Can only import csv
            df = pd.read_csv(file_path)
            #Upload to mongodb
            dbase = client['Fyp-Test']
            
            collection = dbase.list_collection_names()
            
            #Create collections
            for collectionName in collection:
                mydata = dbase[collectionName].find({})
                
                #Will prompt error when the collection have already exists
                if mydata.collection.name != filename:
                    try:
                        dbase.create_collection(filename)
                        #Insert df to mongodb
                        collectionNew = dbase[filename]
                        collectionNew.insert_many(df.to_dict('records'))
                        flash('Successful')
                        # return render_template('upload.html')
                    except: 
                        flash('Collection has already exists')
                        # return render_template('upload.html')
                    
                else:
                    flash('File name is repeated. Please try again.')
                    # return render_template('upload.html')
            

            

            flash('File successfully uploaded ' + file.filename + ' to the database!')
            return render_template('upload.html')
        else:
            flash('Unable to upload') 
            # return redirect('error.html')    
        

    
if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
    