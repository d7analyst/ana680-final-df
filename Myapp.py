import pickle
import joblib
import numpy as np
from flask import Flask,render_template, request
app = Flask(__name__)
filename = 'Titanic_Model.pkl'
model = joblib.load(filename) 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])  # The user input is processed here
def predict():
    age = int(request.form['Age'])
    sex = request.form['Sex'].upper()
    WS  = request.form['Spouse'].upper()
    F   = int(request.form['Family'])
    P   = request.form['Port'].upper()
    

    iPort = getPortInt(P)
    sPort = getPortName(P)

    iSex = int(getSexInt(sex))
    sSex = getSexName(sex)

    iSpouse = int(getSpouseInt(WS))
    sSpouse = getSpouseName(WS)

    sFamily = getFamilyName(F)

    prediction =  model.predict(np.array([[age, iSpouse, F, iSex, iPort[0], iPort[1], iPort[2]]]))

    iSurvived = getSurvived(prediction)
    pred = f"A {sSex}, {age} years of age, traveling {sSpouse} Spouse and {sFamily} relatives "
    pred+= f"embarking from {sPort} is predicted to have {iSurvived}"
    
    return render_template('index.html', predict=str(pred))

def getPortInt(port):
        #create model imputs from port
    iport=[0,0,0]
    if port == "C":
        iport[0]= 1
        iport[1]= 0
        iport[2]= 0
    elif port == "Q":
        iport[0]= 0
        iport[1]= 1
        iport[2]= 0
    else:
        iport[0]= 0
        iport[1]= 0
        iport[2]= 1
    return iport

def getPortName(port):   
    if port == "C":
        iPort = "Cherbourg, France"
    elif port == "Q":
        iPort = "Queenstown, England"
    else:
        iPort = "Shouthampton, Ireland"
    return iPort

def getSexName(sex):
    if sex == "F":
        nSex = "Female"
    else:
        nSex = "Male"
    return nSex
def getSexInt(sex):
    if sex == "F":
        nSex = 0
    else:
        nSex = 1
    return nSex

def getSpouseName(spouse):
    #spouse
    if spouse == "Y":
        iSpouse = "with"
    else:
        iSpouse = "without"
    return iSpouse

def getSpouseInt(spouse):
    if spouse == "N":
        mSpouse = 0
    else:
        mSpouse = 1
    return mSpouse

def getFamilyName(F):    
    if F == 0:
        iRelative = "no"
    else:
        iRelative = F
    return iRelative
    
def getSurvived(prediction):
    if prediction == 1:
        iSurvived = "survived"
    else:
        iSurvived = "not survived"
    return iSurvived

    #return render_template('index.html', predict=str(pred))

if __name__ == '__main__':
    app.run(debug=True)
