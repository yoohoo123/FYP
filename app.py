#Restrictions
#Can only import csv files
#No logout yet
#Localhost only



from unittest import TestCase
from flask import Flask, render_template,request, url_for, redirect ,flash, session , jsonify
from flask_mongoengine import MongoEngine
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from flask_pymongo import PyMongo
import os
import urllib.request
import pandas as pd
import glob
from pandas import DataFrame, json_normalize
# import bcrypt

#Connect to localhost mongodb
app = Flask(__name__)

#Root File
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

#Mongodb details
app.config['MONGO_DBNAME'] = 'Fyp-Test'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Fyp-Test'

mongo = PyMongo(app)

# app.Configuration for uploading
app.config['UPLOAD_FOLDER'] = '../uploaded_files'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024 #Max of 16MB
app.config['UPLOAD_PATH'] = ''
   
ALLOWED_EXTENSIONS = set(['csv', 'xlsx', 'xls', 'txt'])

#User
db = MongoEngine()
db.init_app(app)  

#call default csv from collection and turn into df
database = mongo.db
client = MongoClient('localhost', 27017)

dbase = client['Fyp-Test']

collection = dbase.list_collection_names()

class User(db.Document):
    filepath = db.StringField()
    

#Main Page
@app.route('/')
def main():
    #default admin account
    admin = {
        "name" : "admin",
        "password" : "hashpw",
        "mainpassword" : "1234"
    }
    
    user = "users"
    #Create default admin account
    for collectionName in collection:
        mydata = dbase[collectionName].find({})
        
        #Will prompt error when the collection have already exists
        if mydata.collection.name != user:
            #Insert df to mongodb
            collectionNew = dbase[user]
    
    result = dbase[user].find({"name" : "admin"})
    
    if result == "":
        return render_template('loginpage.html')
    else:
        collectionNew.insert_one(admin)
        return render_template('loginpage.html')

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

#Going to profile page
@app.route('/profile', methods=['POST', 'GET'])
def profile():
    if request.method == 'POST':
        #post the username
        users = mongo.db.users
        userProfileName = users.find_one({'name' : request.form['username']})
        #Get the username
        name = request.form.get('name')
        return render_template('profile.html',userProfileName = userProfileName)
    return render_template('profile.html')

#Going to Home page
@app.route('/home', methods=['POST', 'GET'])
def home():
    return render_template('home.html')

#Going to the setting page
@app.route('/settings', methods=['POST', 'GET'])
def settings():
    return render_template('settings.html')

#Going to the logoutpage
@app.route('/logout', methods=['POST', 'GET'])
def logout():
    return render_template('logout.html')

# @app.route('/upload', methods=['POST', 'GET'])
# def upload():
#     return render_template('upload.html')

#Going to the table page
@app.route('/table', methods=['POST', 'GET'])
def tables():
    #Get collection name
    collection = dbase.list_collection_names()
    #Get selectedvalue
    filename = str(request.form.get("columnname"))
    
    #get the table with the selected value from db
    df = pd.DataFrame.from_dict(json_normalize(dbase[filename].find({})))
    
    return render_template('tables.html',  columnnames = collection , df_html = [df.to_html()], titles=[''])    

# @app.route('/printtable', methods=['POST', 'GET'])
# def dropdownlist():
#     #Get selectedvalue
#     filename = request.form.get("columnname")
#     #get the table with the selected value from db
#     table = dbase[filename].find({})
    
#     return render_template('tables.html', table = table)

#Going to the chart page
@app.route('/chart', methods=['POST', 'GET'])
def chart():
    #Get collection name
    collection = dbase.list_collection_names()
    #Get selectedvalue
    filename = str(request.form.get("columnname"))
    
    #get the table with the selected value from db
    df = pd.DataFrame.from_dict(json_normalize(dbase[filename].find({})))
    
    return render_template('chart.html',columnnames = collection , df_html = [df.to_html()], titles=[''])    

#Going to the graph page
@app.route('/graph2', methods=['POST', 'GET'])
def graph2():
    #Get collection name
    collection = dbase.list_collection_names()
    #Get selectedvalue
    filename = str(request.form.get("columnname"))
    
    #get the table with the selected value from db
    df = pd.DataFrame.from_dict(json_normalize(dbase[filename].find({})))
    return render_template('graph2.html',columnnames = collection , df_html = [df.to_html()], titles=['']) 
        
@app.route('/graph2', methods=['POST', 'GET'])
def showgraph():
    df = DataFrame(list(collection.find({})))
    dfhtml = df.head(30).to_html(index=False)
    graphJSON = figPlotly(df)
    figstatic= figStatic(df)
    return render_template('graph.html', table=dfhtml,graphJSON=graphJSON,figstatic=figstatic) 

#Login session
@app.route('/loginpage', methods=['POST'])
def login():
    users = dbase["users"]
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if request.form['password'] == login_user['mainpassword']:
            session['username'] = request.form['username']
            return redirect(url_for('upload'))

    return render_template('error.html')

#Register session
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            # hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'name' : request.form['username'], 'mainpassword' : request.form['pass']})
            session['username'] = request.form['username']
            return 'Successfully created!'
        
        return 'That username already exists!'

    return render_template('register.html')

# @app.route('/logout')
# def logout():
#     # remove the username from the session if it's there
#     session.pop('username', None)
#     return render_template('loginpage.html')

@app.route('/upload' , methods=['GET', 'POST'])
def movetoupload():
    return render_template('upload2.html')
    
@app.route('/graph' , methods=['GET', 'POST'])
def movetoindex():
    df = DataFrame(list(dbase["disney_movies.csv"].find({})))
    dfhtml = df.head(30).to_html(index=False)
    graphJSON = figPlotly(df)
    figstatic= figStatic(df)
    return render_template('graph.html', table=dfhtml,graphJSON=graphJSON,figstatic=figstatic)                                           
    
    
@app.route('/upload2', methods=['POST','GET'],)
def upload():
        return render_template('upload2.html')

@app.route('/uploadfile', methods=['POST','GET'],)
def uploadfile():
    #Upload file flask
    file = request.files['inputFile']   
    #Extract upload data file name
    filename = secure_filename(file.filename)
   
    #Upload to local filepaths
    if (".csv" in filename) and (file !=''): 
        #Can only import csv
        df = pd.read_csv(file)
        #Upload to mongodb
        dbase = client['Fyp-Test']
        
        collection = dbase.list_collection_names()
        
        #Get collections
        for collectionName in collection:
            mydata = dbase[collectionName].find({})
            
            #Will prompt error when the collection have already exists
            if mydata.collection.name != filename:
                try:
                    #Insert df to mongodb
                    collectionNew = dbase[filename]
                    collectionNew.insert_many(df.to_dict('records'))
                    
                    #Display the table 
                    df_html = df.to_html()
                    
                    return render_template('upload2.html',df_html = [df.to_html()], titles=[''])
                except: 
                    flash('Collection name has already exists')
                    return render_template('upload2.html')
                
            else:
                flash('File name is repeated. Please try again.')
                return render_template('upload2.html')
        

            flash('File successfully uploaded ' + file.filename + ' to the database!')
            return render_template('upload2.html')
    else:
        flash('Unable to upload') 
        return render_template('error.html')    

#Use disney_movies.csv
#indexpage
import matplotlib.pyplot as plt
import json
from io import BytesIO
import base64
import plotly
import plotly.graph_objects as go

#class for data
class data():
    def cleandata():
        collection = dbase.list_collection_names()
        
        #Get collections
        for collectionName in collection:
            mydata = dbase[collectionName].find({})
            
        return mydata

def figStatic(df):
    df = DataFrame(list(dbase["disney_movies.csv"].find({})))
    df["release_date"] = pd.to_datetime(df["release_date"])
    df["release_date"] = pd.DatetimeIndex(df['release_date']).year
    with plt.style.context('ggplot'):
        plt.rcParams['lines.linewidth'] = 2
        plt.rcParams['lines.linestyle'] = '-.'
        plt.rc('lines', marker='o', markerfacecolor='r', markersize=8, markeredgecolor="r")
        #plt.rc('lines', linewidth=2, color='red',linestyle='-.')
        plt.rcParams['figure.figsize'] = (20,9)
        plt.rc("axes",titlesize=30, titlecolor="cyan",titlepad=10)
        plt.rcParams.update({"axes.grid" : True, "grid.color": "red", "grid.alpha" : 0.5})
        plt.rc("font", family="DejaVu Serif", fantasy="Comic Neue", size=20)
        plt.rcParams["date.autoformatter.day"]= "%m-%d" #"%Y-%m"
        # Sample half element of a series
        xlist = []
        data_list = list(df['release_date'])
        for i in range(0, len(data_list),4):
            xlist.append(data_list[i])
        fig, ax = plt.subplots()
        plt.plot(df["release_date"], df["total_gross"])
        ax.set_title("Amount Earn")
        ax.set_xticks( xlist)
        ax.tick_params(axis='x',labelrotation=45,labelcolor='orange')
        #ax.yaxis.grid(False)

        figfile = BytesIO()
        plt.savefig(figfile, format='png')
        figfile.seek(0)  # rewind to beginning of file
        #figdata_png = base64.b64encode(figfile.read())
        figdata_png = base64.b64encode(figfile.getvalue())

        #plt.savefig("static/image.png")
        #fig.savefig("matplotlib_rcparams.png")
        fig_decoded = figdata_png.decode('utf8')
        return fig_decoded
    
def figPlotly(df):
    df = DataFrame(list(dbase["disney_movies.csv"].find({})))
    df["release_date"] = pd.to_datetime(df["release_date"])
    #change to year only
    df["release_date"] = pd.DatetimeIndex(df['release_date']).year
    xx = df["release_date"].values.tolist()
    yy = df["total_gross"].values.tolist()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
            x = xx,
            y = yy,
            name="Totale Gross",
            mode="lines+markers",
            showlegend=True,
            marker=dict(
                symbol="circle-dot",
                size=6,
            ),
            line=dict(
                width=1,
                color="rgb(0,0,0)",
                dash="longdashdot"
            )
        )
    )
    fig.update_layout(
        title=dict(
            text ="Amount Earn",
            y = 0.9,
            x = 0.5,
            xanchor = "center",
            yanchor = "top",
        ),
        legend=dict(
            y = 0.9,
            x = 0.03,
        ),
        xaxis_title="release_date",
        yaxis_title="total_gross",
        font=dict(
            family="Courier New, monospace",
            size=20,
            color="orange", #"#7f7f7f", 
        ),
        hovermode='x',  #['x', 'y', 'closest', False]
        plot_bgcolor = "rgb(200,200,200)",
        paper_bgcolor="rgb(255,255,255)"
    )

    #htmlfig = fig.write_html("fig.html")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


##Error handling
# @app.errorhandler(404)
# def resource_not_found(e):
#     """
#     An error-handler to ensure that 404 errors are returned as JSON.
#     """
#     return jsonify(error=str(e)), 404


# @app.errorhandler(DuplicateKeyError)
# def resource_not_found(e):
#     """
#     An error-handler to ensure that MongoDB duplicate key errors are returned as JSON.
#     """
#     return jsonify(error=f"Duplicate key error."), 400

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.debug = True
    app.run()
    
def api_response():
    from flask import jsonify
    if request.method == 'POST':
        return jsonify(**request.json)
    