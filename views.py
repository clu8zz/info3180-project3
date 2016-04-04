from flask import Flask,render_template,request,session,url_for,redirect,g,session
import urllib
from bs4 import BeautifulSoup
from forms import LoginForm,fetchUrl,WishInfo
from dbModel import db,Userinfo,Wishlist
import time



app=Flask(__name__)
app.secret_key="kdsjfiuh&ugiug&&&fkgvi"
router={'loggedin':''}


@app.route("/", methods=['GET','POST'])
def home():
	unique=""
	form=LoginForm(request.form)
	if request.method=='POST' and form.validate():
		try:
			todb=Userinfo(form.username.data,form.password.data)
			db.session.add(todb)
			db.session.commit()
			return redirect(url_for('login'))
		except:
			unique="Username is already registered with us"
			db.session.rollback()
	return render_template('index.html',form=form,unique=unique)



@app.route("/login",methods=['GET','POST'])
def login():
	router['loggedin']=''
	notUser=""
	found=0
	form=LoginForm(request.form)
	if request.method=='POST' and form.validate():
		query=db.session.query(Userinfo).filter_by(username=form.username.data).first()
		if query is None:
			notUser="Incorrect username/password combination"
			found+=1
		if found==0:
			session['user']=form.username.data
			session['user_id']=query.id
			return redirect(url_for('wishlist'))
	return render_template('login.html',form=form,notUser=notUser)





@app.route('/wishlist')
def wishlist():
	query=db.session.query(Wishlist).filter_by(user_id=session['user_id'])
	if query.first() is None:
		query={'none':'none'}
	return render_template("wishlist.html",user=session['user'],query=query)





@app.route('/wishlist/add',methods=['GET','POST'])
def addtowishlist():
	query=""
	found=""
	href=""
	session['href']=[]
	form=fetchUrl(request.form)
	
	# if router['loggedin']=='':
	# 	return redirect(url_for('login'))
	if request.method=="POST" and form.validate():
		url=form.query.data
		session['url']=url
		fetchurl=urllib.urlopen(url)
		content=fetchurl.read()
		fetchurl.close()
		soup=BeautifulSoup(content,'html.parser')
		for i in soup.find_all('img'):
			if str(i.get('src')[-3:])=='gif':
				continue
			if str(i.get('src'))[:4]!='http':
				session['href'].append(session['url'][:-1]+i.get('src'))
			else:
				session['href'].append(i.get('src'))

		if len(session['href'])==0:
			found="No suitable Wish item could be found on this page!"
		

	# if request.method=="POST":
	# 	return redirect(url_for('wishlist'))

	return render_template('addtowishlist.html',user=session['user'],form=form,thumbs=session['href'],found=found)


@app.route('/wishlist/added',methods=['POST','GET'])
def added():
	href=request.args.get('href')
	form=WishInfo(request.form)
	success=""
	if request.method=="POST" and form.validate():
		wish=Wishlist(session['url'],href,time.strftime("%d/%m/%Y"),session['user_id'],form.category.data,form.quantity.data,form.description.data)
		db.session.add(wish)
		db.session.commit()
		success='Your wish has been added!'
	return render_template("added.html",form=form,user=session['user'],href=href,success=success)

@app.route('/wishlist/delete',methods=['POST','GET'])
def delete():
	href=request.args.get('href')
	delete=""
	if request.method=="POST":
		query=db.session.query(Wishlist).filter_by(href=href,user_id=session['user_id']).first()
		db.session.delete(query)
		db.session.commit()
		return(redirect(url_for("wishlist")))
		
	return render_template('delete.html',href=href,user=session['user'])
	

@app.route('/wishlist/share')
def share():
	pass

def logout():
	router['loggedin']=''
	return redirect(url_for('login'))	

if __name__=="__main__":
	
	app.run(debug=True,host='0.0.0.0')
