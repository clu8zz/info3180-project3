from flask import Flask,render_template,request
from forms import LoginForm

app=Flask(__name__)

@app.route("/", methods=['GET','POST'])
def home():
	form=LoginForm(request.form)

	return render_template('index.html',form=form)



@app.route("/login",methods=['GET','POST'])
def login():
	form=LoginForm(request.form)

	return render_template('login.html',form=form)




if __name__=="__main__":
	
	app.run(debug=True,host='0.0.0.0')
