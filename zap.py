from bson import ObjectId
from flask import Flask, render_template, request, url_for, redirect,session
from pymongo import Connection
app = Flask(__name__)
app.debug=True


@app.route('/')
def hello():
	return render_template("index.html")

@app.route('/login-signup.html')
def both():
	return render_template("login-signup.html")


@app.route('/signup', methods = ['POST', 'GET'])
def signup():
	if request.method=='POST':
		fname= request.form['fnm']
		lname=request.form['lnm']
		email=request.form['email']
		password=request.form['password']
		con=Connection()
		db=con.userinfo
		signup=db.signup
		signup.insert({'fname':fname,'lname':lname,'email':email, 'password':password})
		return redirect(url_for('both'))

@app.route('/login', methods = ['POST', 'GET'])
def login():
	if request.method=='POST':
		email=request.form['email']
		password=request.form['password']
		con=Connection()
		db=con.userinfo
		signup=db.signup
		obj = signup.find({'email':email,'password':password})
		if obj.count()==1:
			return redirect(url_for('blogs'))
		else:
			return redirect(url_for('both'))



@app.route('/blogs-dashboard')
def blogs():
		con=Connection()
		db=con.CRAWLY
		blog=db.blog
		news=blog.find()
		return render_template("blogs-dashboard.html",tmp=news)


@app.route('/news-entertainment')
def newsent():
	con=Connection()
	db=con.CRAWLY
	ent=db.ent
	news=ent.find()
	return render_template("news-entertainment.html",tmp=news)


@app.route('/news-world')
def news():
	con=Connection()
	db=con.CRAWLY
	world=db.world
	news=world.find()
	return render_template("news-world.html",tmp=news)

@app.route('/news-india')
def newsIndia():
	con=Connection()
	db=con.CRAWLY
	India=db.India
	news=India.find()
	return render_template("news-India.html",tmp=news)


@app.route('/single-standard-world/<id>')
def standardworld(id):
	con=Connection()
	db=con.CRAWLY
	world=db.world
	news=world.find({"_id": ObjectId(id)})
	return render_template("single-standard-world.html",tmp=news)

@app.route('/ieee-cse')
def ieeecse():
	con=Connection()
	db=con.CRAWLY
	Computerieee=db.Computerieee
	news=Computerieee.find()
	return render_template("ieee-cse.html",tmp=news)	

@app.route('/ieee-eln')
def ieeeeln():
	con=Connection()
	db=con.CRAWLY
	CELNieee=db.CELNieee
	news=CELNieee.find()
	return render_template("ieee-eln.html",tmp=news)	

@app.route('/ieee-mech')
def ieeemech():
	con=Connection()
	db=con.CRAWLY
	Mechieee=db.Mechieee
	news=Mechieee.find()
	return render_template("ieee-mech.html",tmp=news)	

@app.route('/single-standard-ent/<id>')
def standardent(id):
	con=Connection()
	db=con.CRAWLY
	CELNieee=db.CELNieee
	news=CELNieee.find({"_id": ObjectId(id)})
	return render_template("single-standard-ent.html",tmp=news)

@app.route('/single-standard-india/<id>')
def standardindia(id):
	con=Connection()
	db=con.CRAWLY
	India=db.India
	news=India.find({"_id": ObjectId(id)})
	return render_template("single-standard-india.html",tmp=news)


@app.route('/single-standard-blog/<id>')
def standardblog(id):
	con=Connection()
	db=con.CRAWLY
	blog=db.blog
	news=blog.find({"_id": ObjectId(id)})
	return render_template("single-standard-blog.html",tmp=news)

@app.route('/single-ieee-cse/<id>')
def stdieeecse(id):
	con=Connection()
	db=con.CRAWLY
	Computerieee=db.Computerieee
	news=Computerieee.find({"_id": ObjectId(id)})
	return render_template("single-ieee-cse.html",tmp=news)

@app.route('/add-url/<name>')
def addurl(name):
	return render_template("add-url.html",name=name)

@app.route('/add-url/')
def addurl1():
	return render_template("add-url.html")


@app.route('/add-url-form',methods=['POST','GET'])
def addurlform():
	if request.method=='POST':
		url=request.form['url']
		name='Url Added Successfully!'
		con=Connection()
		db=con.CRAWLY
		addurl=db.addurl
		addurl.insert({'url':url})
		return redirect(url_for('addurl',name=name))

@app.route('/single-standard-mech/<id>')
def stdieeemech(id):
	con=Connection()
	db=con.CRAWLY
	Mechieee=db.Mechieee
	news=Mechieee.find({"_id": ObjectId(id)})
	return render_template("single-standard-mech.html",tmp=news)

@app.route('/single-standard-entertain/<id>')
def stdardnentertain(id):
	con=Connection()
	db=con.CRAWLY
	ent=db.ent
	news=ent.find({"_id": ObjectId(id)})
	return render_template("single-standard-entertain.html",tmp=news)

if __name__ == '__main__':
	app.run()