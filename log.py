from flask import Flask,request,render_template,flash
from flaskext.mysql import MySQL 

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path
import os
import mysql.connector as my

mysql=MySQL()
app=Flask(__name__)
skey=os.urandom(12).hex()
# print(skey)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] ='your pass'
app.config['MYSQL_DATABASE_DB'] = 'your db name'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['SECRET_KEY'] = skey
mysql.init_app(app)

msg=''
db = my.connect(
		    host = "localhost",
		    user = "root",
		    passwd = "your pass",
		    database = "your db name"
		)

@app.route('/dash')
def renderdash():
	return render_template('dash.html')

@app.route('/land-3')
def location():
	return render_template('land-3.html')

@app.route('/landing')
def landing():
	return render_template('landing.html')

@app.route('/')
def renderhome():
	return render_template('land-3.html')

@app.route('/',methods=['POST','GET'])
def home():
  if request.form['logbtn'] == 'Login':
  	return render_template('login.html')
  else:
  	return render_template('land-3.html')

@app.route('/login')
def renderform():
	return render_template('login.html')

@app.route('/login',methods=['POST'])
def authenticate():
	username = request.form['un1']	
	passw = request.form['pass1']

	cursor=mysql.connect().cursor()
	cursor.execute("SELECT * FROM USER WHERE uname='"+ username +"' and passwd='"+ passw +"'")
	data=cursor.fetchone()
	
	if data is None:
		#flash("username or passsword is incorrect")
		return render_template('landing.html')
	else:
		return render_template('login.html')

@app.route('/login_v')
def vendorform():
	return render_template('login_v.html')

@app.route('/login_v',methods=['POST'])
def auth_v():
	username = request.form['un2']	
	passw=request.form['pass2']
	# type_var='user'
	conn=mysql.connect()
	cursor=mysql.connect().cursor()
	cursor.execute("SELECT * FROM VENDOR WHERE vname='"+ username +"' and vpass='"+ passw +"'")
	data=cursor.fetchone()
	
	if data is None:
		msg="username or passsword is incorrect"
		return render_template('login_v.html', msg=msg)
	else:
		return render_template('landing.html')

@app.route('/for')
def forgotpass():
	return render_template('for.html')


@app.route('/for', methods=['POST'])
def sendmail():
	sender_email = "sender_email@gmail.com"
	receiver_email = "rec_email@gmail.com" #request.form['mail']
	password = 'abcde'                #input("Type your password and press enter:")
	subject='this is test mail'
	file_location = 'c:\\newfile.txt'
	message='This is the message to be sent, the link for password reset'

	msg = MIMEMultipart()
	msg['From'] = sender_email
	msg['To'] = receiver_email
	msg['Subject'] = subject

	msg.attach(MIMEText(message, 'plain'))

	# Setting up the attachment,change file loc to the path in your comp
	filename = os.path.basename(file_location)
	attachment = open(file_location, "rb")
	part = MIMEBase('application', 'octet-stream')
	part.set_payload(attachment.read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

	# Attach the attachment to the MIMEMultipart object
	msg.attach(part)

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(sender_email, password)
	text = msg.as_string()
	server.sendmail(sender_email, receiver_email, text)
	#print("mail sent")
	server.quit()

	return render_template('newpass.html')
	#the mail script here n then the redirect or render templ for new passwd


@app.route('/newpass')
def setpass():
	return render_template('newpass.html')

@app.route('/newpass', methods=['POST'])
def updatepass():
	msg=''
	# if request.method == 'POST' and 'pass' in request.form and 'confirmpass' in request.form:	
	username = request.form['username']
	new_p = request.form['pass']	
	confi=request.form['confirmpass']

	if (new_p == confi):
		cursor = db.cursor()
		query = "UPDATE user SET passwd = '"+new_p+"' WHERE uname = '"+username+"' "
		cursor.execute(query)
		## final step to tell the database that we have changed the table data
		db.commit()
		return render_template('land-3.html')
	else:
		msg="new password and confirm password donot match"
		return render_template('login.html', msg=msg)

	# if data is None:
	# 	return "Enter the password "
	# else:
	# 	return "Password updated successfully"

@app.route('/reg_user')
def reg_user():
    return render_template('reg_user.html')

@app.route('/reg_user', methods=['POST'])
def add_reguser():
    UNAME = request.form.get('name')
    PASSWD = request.form.get('pass')
    UMAIL = request.form.get('mail')

    cursor=db.cursor()
    cursor.execute("""INSERT INTO `USER` (`UID`, `UNAME`, `PASSWD`, `UMAIL`) VALUES (100, '{}', '{}', '{}')""".format(UNAME, PASSWD, UMAIL))
    conn.commit()

    cursor.execute("""SELECT * FROM `USER` WHERE `UMAIL` LIKE '{}'""".format(UMAIL))
    myuser = cursor.fetchall()
    # session['UID'] = myuser[0][0]
    return render_template('login.html')

@app.route('/reg_vendor')
def reg_vendor():
    return render_template('reg_vendor.html')

@app.route('/reg_vendor', methods=['POST'])
def add_regvendor():
    VNAME = request.form.get('name')
    VSHOP = request.form.get('shopname')
    address = request.form.get('address')
    VPASS = request.form.get('passw')
    cpass = request.form.get('cpass')
    VMAIL = request.form.get('mail')
    url = request.form.get('url')

    cursor.execute("""INSERT INTO `vendor` (`VID`, `VNAME`, `VPASS`, `VMAIL`, `VSHOP`) VALUES (100, '{}', '{}', '{}', '{}')""".format(VNAME, VPASS, VMAIL, VSHOP))
    conn.commit()

    cursor.execute("""SELECT * FROM `USER` WHERE `umail` LIKE '{}'""".format(VMAIL))
    myuser = cursor.fetchall()
    session['user_id'] = myuser[0][0]
    return redirect('/login_v')


@app.route('/media')
def rendermedia():
	return render_template('media.html')

# @app.route('/media', methods=['GET','POST'])
# def mediapage():
# 	if request.form['logbtn'] == 'Login':
# 		return render_template('login.html')
# 	else:
# 		return render_template('media.html')



@app.route('/cart')
def rendercart():
	return render_template('cart.html')

@app.route('/index')
def renderindex():
	return render_template('index.html')

@app.route('/checkout')
def rendercheckout():
	return render_template('checkout.html')


@app.route('/order')
def renderorder():
	return render_template('order.html')


@app.route('/video')
def rendervideo():
	return render_template('video.html')

@app.route('/policy')
def renderpolicy():
	return render_template('policy.html')

@app.route('/history')
def hist():
	return render_template('history.html')

@app.route('/history',methods=['GET','POST'])
def renderhist():
	if request.form['logbtn'] == 'Login':
		return render_template('login.html')

	return render_template('history.html')


if __name__ == '__main__':
	app.run(debug = True)
