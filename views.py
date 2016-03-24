from flask import Flask,render_template,request,session,url_for,redirect

from forms import LoginForm,fetchUrl
from dbModel import db,Userinfo



app=Flask(__name__)
app.secret_key="kdsjfiuh&^ITUGkug7il!!!~^hIU)(&*^$##H7++))(LGIBKji"
router={'loggedin':''}

@app.route("/", methods=['GET','POST'])
def home():
	form=LoginForm(request.form)
	if request.method=='POST' and form.validate():
		todb=Userinfo(form.username.data,form.password.data)
		db.session.add(todb)
		db.session.commit()
		return redirect(url_for('login'))
	return render_template('index.html',form=form)



@app.route("/login",methods=['GET','POST'])
def login():
	router['loggedin']=''
	form=LoginForm(request.form)
	if request.method=='POST' and form.validate():
		query=db.session.query(Userinfo).filter_by(username=form.username.data).first()
		if str(query.password)==form.password.data:
			router['loggedin']=form.username.data
			return redirect(url_for('wishlist'))
	return render_template('login.html',form=form,test=router['loggedin'])


@app.route('/wishlist')
def wishlist():
	form=fetchUrl(request.form)
	if router['loggedin']=='':
		return redirect(url_for('login'))
	else:
		return render_template('wishlist.html',user=router['loggedin'],form=form)

@app.route('/wishlist/add')
def add():
	pass


@app.route('/wishlist/delete')
def delete():
	pass

@app.route('/wishlist/share')
def share():
	pass

def logout():
	router['loggedin']=''
	return redirect(url_for('login'))	

if __name__=="__main__":
	
	app.run(debug=True,host='0.0.0.0')
