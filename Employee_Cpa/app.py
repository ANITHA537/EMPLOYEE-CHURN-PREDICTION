from asyncio.windows_events import NULL
from flask import Flask, render_template, send_file, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from sklearn.preprocessing import OneHotEncoder
from datetime import datetime
import pandas as pd
import pickle
import csv
import os
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

import warnings
warnings.filterwarnings('ignore')


app = Flask(__name__)

# with open('C:/Users/ANITHA/Desktop/Project/Employee_Cpa/Employee Churn Predictor.ipynb') as f:
#     nb = nbformat.read(f, as_version=4)

# ep = ExecutePreprocessor(timeout=600, kernel_name='python3')


# ep.preprocess(nb, {'metadata': {'C:/Users/ANITHA/Desktop/Project/Employee_Cpa/Employee Churn Predictor.ipynb': 'notebooks/'}})
# with open('executed_notebook.ipynb', 'w', encoding='utf-8') as f:
#     nbformat.write(nb, f)

ALLOWED_EXTENSIONS = set(['csv'])

UPLOAD_FOLDER = 'C:/Users/ANITHA/Desktop/Project/Employee_Cpa/static/input'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/index', methods=['GET', 'POST'])
def nav():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def details():
    return render_template('home.html')

# @app.route('/important_Attributes')
# def Important_Attributes():
#     image = [i for i in os.listdir('static/images') if i.endswith('.png')][1]
#     return render_template('Important_Attributes.html', user_image = image)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        return redirect(url_for('')) 
    return render_template('index.html')

def process_file(save_location):
    data = pd.read_csv(save_location)
    temp=data
    namedata=data['Name'].to_list()
    nameList=[]
    for i in namedata:
        lst=[]
        lst.append(i)
        nameList.append(lst)
    data_main = data.drop(['Name','EmployeeCount', 'Over18', 'StandardHours','Attrition'], axis=1)
    
    # temp['Attrition']=0
    data = pd.get_dummies(data_main)
    data.to_csv("processed HR.csv")
    lr_from_pickle = pickle.load(open('C:/Users/ANITHA/Desktop/Project/Employee_Cpa/model.pkl', 'rb'))
    with open('processed HR.csv') as file_obj:
        reader_obj = csv.reader(file_obj)
    # lr_from_pickle.predict(data)
    res = []
    res = lr_from_pickle.predict(data)
    df = pd.read_csv("processed HR.csv")
    empId = df['EmployeeNumber'].tolist()
    empIdList = []
    for id in empId:
        lst = []
        lst.append(id)
        empIdList.append(lst)
    # print('Employee Details: ')
    # print(empIdList)
    fields1 = ['Employee Number','Name','Attrition']
    fields2=['Employee Number','Name']
    with open('Entire.csv', 'w') as file1,open('leave.csv','w') as file2,open('stay.csv','w') as file3:
        # print('Result')
        # print(res)
        idx1 = 0
        writer1=csv.DictWriter(file1, fieldnames=fields1)
        writer2=csv.DictWriter(file2,fieldnames=fields2)
        writer3=csv.DictWriter(file3,fieldnames=fields2)

        writer1.writeheader()
        writer2.writeheader()
        writer3.writeheader()
        
        for i in range(len(res)):
            if res[i] == 1:
                writer1.writerow({'Employee Number': empIdList[idx1], 'Name': nameList[idx1],'Attrition':"Might Leave"})
                temp["Attrition"][idx1]="leave"
                writer2.writerow({'Employee Number': empIdList[idx1], 'Name': nameList[idx1]})
            else:
                writer1.writerow({'Employee Number': empIdList[idx1], 'Name': nameList[idx1],'Attrition':"May stay"})
                temp["Attrition"][idx1]="stay"
                writer3.writerow({'Employee Number': empIdList[idx1], 'Name': nameList[idx1]})
            idx1 = idx1 + 1

        temp.to_csv('C:/Users/ANITHA/Desktop/Project/Employee_Cpa/Data Sets/result.csv')
        with open('C:/Users/ANITHA/Desktop/Project/Employee_Cpa/result_Analysis.ipynb') as f:
            nb = nbformat.read(f, as_version=4)

        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')


        ep.preprocess(nb, {'metadata': {'C:/Users/ANITHA/Desktop/Project/Employee_Cpa/result_analysis.ipynb': 'notebooks/'}})
        with open('executed_result_analysis.ipynb', 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        file1.close()
        file2.close()
        file3.close()

    return empIdList


@app.route('/upload', methods=['GET', 'POST'])
def upload():
        if request.method == 'POST':
            file = request.files['csvfile']
            if file and allowed_file(file.filename):
                # warnings.filterwarnings('ignore')
                filename: str = secure_filename(file.filename)
                save_location = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(save_location)
                res=process_file(save_location)
                result=res
                return render_template('downloadDetails.html', data1=res)
                
        return render_template('downloadDetails.html')



@app.route('/res', methods=['GET', 'POST'])
def res():
    d=""
    if request.method=='POST':
        num=request.form['ID']
        frame1=pd.read_csv("C:/Users/ANITHA/Desktop/Project/leave.csv")
        frame2=pd.read_csv("C:/Users/ANITHA/Desktop/Project/stay.csv")
        res1=frame1['Employee Number']
        res2=frame2['Employee Number']
        result1=[]
        # print(num)
        for id in res1:
            lst = []
            lst.append(id)
            result1.append(lst)
        # print(type(result))
        l1=[]
        la1=[]
        la1.append(int(num))
        l1.append(str(la1))
        result2=[]
        # print(num)
        for id in res2:
            lst = []
            lst.append(id)
            result2.append(lst)
        # print(type(result))
        l2=[]
        la2=[]
        la2.append(int(num))
        l2.append(str(la2))
        
        for i in range(len(result1)):
            # print(result[i],"fh",str(l))
            if(result1[i]==l1):
                d="Might leave"
                return render_template('downloadDetails.html',data=d)
            
        for i in range(len(result2)):
            if(result2[i]==l2):
                d="Might Stay"
                return render_template('downloadDetails.html',data=d)
        d="It is invalid id"
    return render_template('downloadDetails.html',data=d)      
        
    
@app.route('/Download_file', methods=['GET', 'POST'])
def Download_file():
    path = "C:/Users/ANITHA/Desktop/Project/Entire.csv"
    return send_file(path, as_attachment=True)

@app.route('/Download_file_leave', methods=['GET', 'POST'])
def Download_file_leave():
    path = "C:/Users/ANITHA/Desktop/Project/leave.csv"
    return send_file(path, as_attachment=True)

@app.route('/Download_file_stay', methods=['GET', 'POST'])
def Download_file_stay():
    path = "C:/Users/ANITHA/Desktop/Project/stay.csv"
    return send_file(path, as_attachment=True)




@app.route('/attributes', methods=['GET', 'POST'])
def required_attributes():
    return render_template('requiredAttributes.html')


@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    return render_template('analysis.html')


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route('/Nav', methods=['GET', 'POST'])
def return_home():
    return render_template('home.html')

@app.route('/lr', methods=['GET', 'POST'])
def lr():
    return render_template('lr.html')

@app.route('/rfc', methods=['GET', 'POST'])
def rfc():
    return render_template('rfc.html')

@app.route('/bg', methods=['GET', 'POST'])
def bg():
    return render_template('bg.html')

@app.route('/svm', methods=['GET', 'POST'])
def svm():
    return render_template('svm.html')

@app.route('/knn', methods=['GET', 'POST'])
def knn():
    return render_template('knn.html')

@app.route('/gbc', methods=['GET', 'POST'])
def gbc():
    return render_template('gbc.html')

@app.route('/xgbc', methods=['GET', 'POST'])
def xgbc():
    return render_template('xgbc.html')



if __name__ == '__main__':
    app.run(debug=True)