from flask import Flask,render_template,url_for,request,jsonify
import joblib,os,pandas,sqlite3


app=Flask(__name__)

data_insert_query = """
insert into project (age,gender,bmi,children,region,smoker,health,prediction)
values(?,?,?,?,?,?,?,?)
"""

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/project")
def project():
    return render_template('project.html')

@app.route('/data',methods=['GET','POST'])
def data():
    if request.method=="POST":
        age=request.form['age']
        region=request.form['region']
        children=request.form['children']
        health=request.form['health']
        gender=request.form['gender']
        smoker=request.form['smoker']
        bmi=request.form['bmi']


        region_northeast=0
        region_northwest=0	
        region_southeast=0	
        region_southwest=0

        if region=='northeast':
            region_northeast=1
        elif region=='northwest':  
            region_northwest=1
        elif region=='southeast':  
            region_southeast=1
        else:
            region_southwest=1

        ls={"age":[age],"sex":[gender],"bmi":[bmi],"children":[children],"smoker":[smoker],"health":[health],"region_northeast":[region_northeast],"region_northwest":[region_northwest],"region_southeast":[region_southeast],"region_southwest":[region_southwest]}

        df=pandas.DataFrame(ls)
        lnr=joblib.load('linear_model.lb')
        dtr=joblib.load('./models/decision_tree.lb')
        rfr=joblib.load('./models/randomforest.lb')
        xx=lnr.predict(df)
        yy=dtr.predict(df)
        zz=rfr.predict(df)

        conn=sqlite3.connect('insurance.db')
        cur=conn.cursor()
        Data=(age,gender,bmi,children,region,smoker,health,xx[0][0])
        cur.execute(data_insert_query,Data)
        conn.commit()
        cur.close()
        conn.close()


        a=str(xx[0][0])
        b=str(yy[0])
        c=str(zz[0])
        #lst=[a,b,c]
        lst={"Prediction by linear":a,"Prediction by Decision_Tree":b,"Prediction by Random_Forest":c}
        #lst1=tuple(a)
        #lst1="Linear: "+a+"\t"+"Decision: "+b+"\t"+"Forest: "+c
        return render_template('final.html',output=xx[0][0])

if __name__=="__main__":
    app.run(debug=True)

