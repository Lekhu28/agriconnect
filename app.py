import numpy as np
from flask import Flask, request, jsonify, render_template
import joblib
import sqlite3

import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
import pickle
import pandas as pd
import numpy as np
import pickle
import sqlite3
import random

import smtplib 
from email.message import EmailMessage
from datetime import datetime

from ultralytics import YOLO
import argparse
import io
import os
from PIL import Image
import datetime

import torch
from flask import Flask, render_template, request, redirect
import io

warnings.filterwarnings('ignore')



app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/home1')
def home1():
	return render_template('home1.html')


@app.route('/home2')
def home2():
	return render_template('home2.html')

@app.route('/logon')
def logon():
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('signin.html')


@app.route('/home')
def home():
	return render_template('home.html')


@app.route("/signup")
def signup():
    global otp, username, name, email, number, password
    username = request.args.get('user','')
    name = request.args.get('name','')
    email = request.args.get('email','')
    number = request.args.get('mobile','')
    password = request.args.get('password','')
    otp = random.randint(1000,5000)
    print(otp)
    msg = EmailMessage()
    msg.set_content("Your OTP is : "+str(otp))
    msg['Subject'] = 'OTP'
    msg['From'] = "evotingotp4@gmail.com"
    msg['To'] = email
    
    
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("evotingotp4@gmail.com", "xowpojqyiygprhgr")
    s.send_message(msg)
    s.quit()
    return render_template("val.html")

@app.route('/predict_lo', methods=['POST'])
def predict_lo():
    global otp, username, name, email, number, password
    if request.method == 'POST':
        message = request.form['message']
        print(message)
        if int(message) == otp:
            print("TRUE")
            con = sqlite3.connect('signup.db')
            cur = con.cursor()
            cur.execute("insert into `info` (`user`,`email`, `password`,`mobile`,`name`) VALUES (?, ?, ?, ?, ?)",(username,email,password,number,name))
            con.commit()
            con.close()
            return render_template("signin.html")
    return render_template("signup.html")

@app.route("/signin")
def signin():

    mail1 = request.args.get('user','')
    password1 = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `user`, `password` from info where `user` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()

    if data == None:
        return render_template("signin.html")    

    elif mail1 == str(data[0]) and password1 == str(data[1]):
        return render_template("home.html")
    else:
        return render_template("signin.html")

@app.route("/notebook1")
def notebook1():
    return render_template("Yield.html")

@app.route("/notebook2")
def notebook2():
    return render_template("Crop.html")

@app.route("/notebook3")
def notebook3():
    return render_template("Detection.html")

@app.route('/predict',methods=['POST'])
def predict():
    int_features= [float(x) for x in request.form.values()]
    print(int_features,len(int_features))
    final4=[np.array(int_features)]
    model = joblib.load('model_yeild.sav')
    predict = model.predict(final4)

    
    output = 'The Crop Yield is Predicted as ' + str(predict[0]) + ' Q/acre!' 
    
    
    return render_template('prediction.html', output=output)


@app.route('/predict1',methods=['POST'])
def predict1():
    int_features= [float(x) for x in request.form.values()]
    print(int_features,len(int_features))
    final4=[np.array(int_features)]
    model = joblib.load('model_crop.sav')
    predict = model.predict(final4)

    if predict == 0:
        output = "Recommended Crop is apple!"
    elif predict == 1:
        output = "Recommended Crop is banana!"
    elif predict == 2:
        output = "Recommended Crop is blackgram!"
    elif predict == 3:
        output = "Recommended Crop is chickpea!"
    elif predict == 4:
        output = "Recommended Crop is coconut!"
    elif predict == 5:
        output = "Recommended Crop is coffee!"
    elif predict == 6:
        output = "Recommended Crop is cotton!"
    elif predict == 7:
        output = "Recommended Crop is grapes!"
    elif predict == 8:
        output = "Recommended Crop is jute!"
    elif predict == 9:
        output = "Recommended Crop is kidneybeans!"
    elif predict == 10:
        output = "Recommended Crop is lentil!"
    elif predict == 11:
        output = "Recommended Crop is maize!"
    elif predict == 12:
        output = "Recommended Crop is mango!"
    elif predict == 13:
        output = "Recommended Crop is mothbeans!"
    elif predict == 14:
        output = "Recommended Crop is mungbean!"
    elif predict == 15:
        output = "Recommended Crop is muskmelon!"
    elif predict == 16:
        output = "Recommended Crop is orange!"
    elif predict == 17:
        output = "Recommended Crop is papaya!"
    elif predict == 18:
        output = "Recommended Crop is pigeonpeas!"
    elif predict == 19:
        output = "Recommended Crop is pomegranate!"
    elif predict == 20:
        output = "Recommended Crop is rice!"
    elif predict == 21:
        output = "Recommended Crop is watermelon!"
    
    
    return render_template('prediction.html', output=output)


model_8 = YOLO('best.pt')  # force_reload = recache latest code

@app.route("/predict2", methods=["POST","GET"])
def predict2():
    if request.method == "POST":
        file = request.files["file"]
    
    
        #print('Model 8')
        
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))
        results = model_8(img)
        res_plotted = results[0].plot()
        for result in results:
            boxes = result.boxes  # Boxes object for bbox outputs
            masks = result.masks  # Masks object for segmenation masks outputs
            probs = result.probs  # Class probabilities for classification outputs
            # updates results.imgs with boxes and labels
            #now_time = datetime.datetime.now().strftime(DATETIME_FORMAT)
        img_savename = f"static/image1.png"

        Image.fromarray(res_plotted).save(img_savename)
        return redirect(img_savename)
    
    
    return render_template('home2.html')

@app.route('/soil')
def soil():
	return render_template('soil.html')


@app.route('/black')
def black():
	return render_template('black.html')

@app.route('/clayey')
def clayey():
	return render_template('clayey.html')

@app.route('/loamy')
def loamy():
	return render_template('loamy.html')

@app.route('/red')
def red():
	return render_template('red.html')

@app.route('/sandy')
def sandy():
	return render_template('sandy.html')



if __name__ == "__main__":
    app.run()
