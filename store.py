from flask import Flask,jsonify,request,send_file
from flask_sqlalchemy import SQLAlchemy
from jinja2 import Template
from argon2 import PasswordHasher
import os
import jwt
from flask_cors import CORS
from datetime import datetime,timedelta
import pytz
from celery import Celery
from celery.schedules import crontab
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_caching import Cache
import flask_excel as excel
from celery.result import AsyncResult

app = Flask(__name__)
cache = Cache()


current_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(current_dir, "grocerystore.sqlite3")
app.config["CACHE_TYPE"]="RedisCache"
app.config["CACHE_REDIS_URL"] = "redis://localhost:6379/2"
app.config["CACHE_DEFAULT_TIMEOUT"] = 1000

db = SQLAlchemy()
db.init_app(app)
excel.init_excel(app)
cache.init_app(app)
CORS(app)

senderemail = 'grocerygenie23@gmail.com'
password = 'zghixbksvbsdzypg'

#making celery app

def make_celery(app):
    celery = Celery(app.import_name)
    celery.conf.update(app.config["CELERY_CONFIG"])

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


app.config.update(CELERY_CONFIG={
    'broker_url': 'redis://localhost:6379',
    'result_backend': 'redis://localhost:6379',
})

celery = make_celery(app)


'''Global variables'''
sk = os.urandom(32)
SECRET_KEY = sk.hex()

'''Models for database'''

class users(db.Model):
    __tablename__ = 'users'
    username  = db.Column(db.String , nullable = False)
    email = db.Column(db.String , primary_key = True , nullable = False)
    password = db.Column(db.String , nullable = False)
    lastvisited = db.Column(db.String)

class storemanagers(db.Model):
    __tablename__ = 'store_managers'
    username  = db.Column(db.String , nullable = False)
    email = db.Column(db.String , primary_key = True , nullable = False)
    password = db.Column(db.String , nullable = False)
    sm_id = db.Column(db.String , nullable = False,)
    status = db.Column(db.String , nullable = False , default = 'pending')

class admin(db.Model):
    __tablename__ = 'admin'
    username  = db.Column(db.String , nullable = False)
    email = db.Column(db.String , primary_key = True , nullable = False)
    password = db.Column(db.String , nullable = False)

class countervalues(db.Model):
    __tablename__ = 'countervalues'
    storecounter = db.Column(db.Integer)
    smcounter = db.Column(db.Integer)
    catcounter = db.Column(db.Integer)
    counter = db.Column(db.Integer , primary_key = True)
    pcounter = db.Column(db.Integer)
    reqcounter = db.Column(db.Integer)
    ordercounter = db.Column(db.Integer)

class categories(db.Model):
    __tablename__ = 'categories'
    CategoryId = db.Column(db.String , primary_key = True , nullable = False)
    CName = db.Column(db.String , nullable = False)

class products(db.Model):
    __tablename__ = 'products'
    productid = db.Column(db.String , nullable = False , primary_key = True)
    productname = db.Column(db.String , nullable = False)
    pcatid = db.Column(db.String , nullable = False)
    pcatname = db.Column(db.String , nullable = False)
    storeid = db.Column(db.String , nullable = False)
    mfgdate = db.Column(db.String , nullable = False)
    expdate = db.Column(db.String , nullable = False)
    description = db.Column(db.String , nullable = False)
    price = db.Column(db.Numeric(10,2) , nullable = False)
    qty = db.Column(db.Integer , nullable = False)
    wt = db.Column(db.String , nullable = False , primary_key = True)

class stores(db.Model):
    __tablename__ = 'stores'
    storeid = db.Column(db.String , nullable = False , primary_key = True)
    storename = db.Column(db.String , nullable = False)
    managerid = db.Column(db.String , nullable = False)

class requests(db.Model):
    __tablename__ = 'requests'
    requestid = db.Column(db.String , nullable = False , primary_key = True)
    title = db.Column(db.String , nullable = False)
    managerid = db.Column(db.String , nullable = False)
    status = db.Column(db.String , nullable = False , default = 'pending')
    username = db.Column(db.String)
    emailid = db.Column(db.String)
    categoryname = db.Column(db.String)

class orders(db.Model):
    __tablename__ = 'orders'
    orderid = db.Column(db.String , nullable = False , primary_key = True)
    useremail = db.Column(db.String , nullable = False)
    storeid = db.Column(db.String , nullable = False)
    date = db.Column(db.String , nullable = False)
    time = db.Column(db.String , nullable = False)
    totalprice = db.Column(db.String , nullable = False)

class orderdetails(db.Model):
    __tablename__ = 'orderdetails'
    orderid = db.Column(db.String , nullable = False , primary_key = True)
    pcatname = db.Column(db.String , nullable = False)
    productid = db.Column(db.String , nullable = False , primary_key = True)
    productname = db.Column(db.String , nullable = False)
    qty = db.Column(db.String , nullable = False)
    price = db.Column(db.String , nullable = False)

'''Password encryption and decryption'''
def password_encrypt(passw):
    ph = PasswordHasher()
    enc_pass = ph.hash(passw)
    return enc_pass

def password_decrypt(passw):
    ph = PasswordHasher()
    try :
        ph.verify(passw , request.json["password"])
        return True
    except :
        return False 


'''routing'''

@app.route('/signup',methods = ['POST'])
def signup():
    if request.method == "POST":
        username = request.json['username']
        email = request.json['email']
        password = password_encrypt(request.json['password'])
        role = request.json['role']
        if role == "u":
            check = users.query.filter(users.email == email).all()
            if len(check) > 0:
                return jsonify({
                    'status':'unsuccessfull'
                })
            else:
                u = users(username = username, email=email, password = password)
                db.session.add(u)
        elif role == "sm":
            check = storemanagers.query.filter(storemanagers.email == email).all()
            c = countervalues.query.first()
            if len(check) > 0:
                return jsonify({
                    'status':'unsuccessfull'
                })
            else:
                sm = storemanagers(username=username , email=email , password=password , sm_id = 'SM'+str(c.smcounter))
                req = requests(requestid = 'R' + str(c.reqcounter) , title = "Sign Up request" , username = username , emailid = email , managerid = 'SM' + str(c.smcounter))
                c.smcounter += 1
                c.reqcounter += 1
                db.session.add(sm)
                db.session.add(req)
        db.session.commit()
        return jsonify({
            'status':'successfull'
        })
    
@app.route('/login',methods=['POST'])
def login():
    if request.method == "POST":
        email = request.json['email']
        checkuser = users.query.filter(users.email == email).first()
        checksm = storemanagers.query.filter(storemanagers.email == email).first()
        checkadmin = admin.query.filter(admin.email == email).first()
        d = datetime.today().strftime("%d-%m-%Y")
        if checksm and checksm.sm_id != "":
            store = stores.query.filter(stores.managerid == checksm.sm_id).first()
        if checkuser and checksm:
            if password_decrypt(checkuser.password):
                token = jwt.encode({
                    'email': email,
                    }, SECRET_KEY, algorithm='HS256')
                if checksm.status != 'approved':
                    checkuser.lastvisited = d
                    db.session.commit()
                    return jsonify({
                        'status' : 'successfull',
                        'token' : token,
                        'role' : ['user'],
                        'name' : [checkuser.username],
                        'email' : checkuser.email
                    })
                checkuser.lastvisited = d
                db.session.commit()
                return jsonify({
                    'status':'successfull',
                    'token': token,
                    'role' : ['user','sm'],
                    'storeid' : store.storeid,
                    'storename' : store.storename,
                    'name' : [checkuser.username,checksm.username],
                    'managerid' : checksm.sm_id,
                    'email' : checkuser.email
                })
            else:
                return jsonify({
                    'status':'incorrect'
                })
        elif checkuser:
            if password_decrypt(checkuser.password):
                token = jwt.encode({
                    'email': email,
                    }, SECRET_KEY, algorithm='HS256')
                checkuser.lastvisited = d
                db.session.commit()
                return jsonify({
                    'status':'successfull',
                    'token': token,
                    'role' : ['user'],
                    'name' : [checkuser.username],
                    'email' : checkuser.email
                })
            else:
                return jsonify({
                    'status':'incorrect'
                })
        elif checksm:
            if password_decrypt(checksm.password):
                if checksm.status == 'pending':
                    return jsonify({
                        'status' : 'pending'
                    })
                elif checksm.status == 'declined':
                    return jsonify({
                        'status' : 'declined'
                    })
                token = jwt.encode({
                    'email': email,
                    }, SECRET_KEY, algorithm='HS256')
                return jsonify({
                    'status':'successfull',
                    'token': token,
                    'role' : ['sm'],
                    'storeid' : store.storeid,
                    'storename' : store.storename,
                    'name' : [checksm.username],
                    'managerid' : checksm.sm_id,
                    'email' : checksm.email
                })
            else:
                return jsonify({
                    'status':'incorrect'
                })
        elif checkadmin:
            if checkadmin.password == request.json["password"]:
                token = jwt.encode({
                    'email': email,
                    }, SECRET_KEY, algorithm='HS256')
                return jsonify({
                    'status':'successfull',
                    'token': token,
                    'role' : ['admin'],
                    'name' : [checkadmin.username],
                    'email' : checkadmin.email
                })
            else:
                return jsonify({
                    'status':'incorrect'
                })
        else:
            return jsonify({
                'status' : 'unsuccessfull',
            })

@app.route('/admin/pendingrequests',methods = ['GET','POST'])
def req():
    if request.method == 'GET':
        req = requests.query.filter(requests.status == 'pending').all()
        l = []
        for i in req:
            l.append([i.requestid , i.title , i.username , i.emailid , i.managerid , i.categoryname])
        return jsonify({
            'req' : l
        })
    
    if request.method == 'POST':
        if request.json['type'] == 's':
            m = storemanagers.query.filter(storemanagers.sm_id == request.json['managerid']).first()
            req = requests.query.filter(requests.managerid == request.json['managerid'] , requests.title == 'Sign Up request' , requests.status == 'pending').first()
            if request.json['status'] == 'approved':
                counter = countervalues.query.first()
                s = stores(storeid = 'ST' + str(counter.storecounter) , storename = 'ST' + str(counter.storecounter) , managerid = m.sm_id)
                counter.storecounter += 1
                m.status = 'approved'
                req.status = 'approved'
                db.session.add(s)
                db.session.commit()
            if request.json['status'] == 'declined':
                m.status = 'declined'
                req.status = 'declined'
                db.session.commit()
        if request.json['type'] == 'c':
            req = requests.query.filter(requests.managerid == request.json['managerid'] , requests.title == 'Category addition request' , requests.categoryname == request.json['catname'] , requests.status == 'pending').first()
            if request.json['status'] == 'approved':
                counter = countervalues.query.first()
                cat = categories(CategoryId = 'C' + str(counter.catcounter) , CName = str(request.json['catname']))
                counter.catcounter += 1
                req.status = 'approved'
                db.session.add(cat)
                db.session.commit()
            if request.json['status'] == 'declined':
                req.status = 'declined'
                db.session.commit()
        req = requests.query.filter(requests.status == 'pending').all()
        l = []
        for i in req:
            l.append([i.requestid , i.title , i.username , i.emailid , i.managerid , i.categoryname])
        return jsonify({
            'req' : l
        })
    
@app.route('/admin/addcategory',methods = ['GET','POST','DELETE'])
def category():
    if request.method == "GET":
        cat = categories.query.all()
        c = []
        for i in cat:
            c .append([i.CategoryId,i.CName])
        return jsonify({
            'categories' : c
        })
    
    if request.method == "DELETE":
        cat = categories.query.filter(categories.CategoryId == request.json['catid']).first()
        db.session.delete(cat)
        db.session.commit()
        category = categories.query.all()
        c = []
        for i in category:
            c .append([i.CategoryId,i.CName])
        return jsonify({
            'categories' : c
        })
    
    if request.method == "POST":
        check = categories.query.filter(categories.CName == str(request.json['catname'])).all()
        if len(check) > 0:
            return jsonify({
                'status' : 'unsuccessfull'
            })
        if request.json['addstatus'] == 'add':
            counter = countervalues.query.first()
            cat = categories(CategoryId = 'C' + str(counter.catcounter) , CName = str(request.json['catname']))
            counter.catcounter += 1
            db.session.add(cat)
            db.session.commit()
            category = categories.query.all()
            c = []
            for i in category:
                c .append([i.CategoryId,i.CName])
            return jsonify({
                'status' : 'successfull',
                'categories' : c
            })
        
        if request.json['addstatus'] == 'update':
            check = categories.query.filter(categories.CategoryId == request.json['catid']).first()
            check.CName = request.json['catname']
            db.session.commit()
            category = categories.query.all()
            c = []
            for i in category:
                c .append([i.CategoryId,i.CName])
            return jsonify({
                'status' : 'successfull',
                'categories' : c
            })
        
@app.route('/storemanager/addproduct' ,methods = ['GET','POST'])
def product():
    if request.method == "GET":
        cat = categories.query.all()
        c = []
        for i in cat:
            c .append([i.CategoryId,i.CName])
        return jsonify({
            'categories' : c
        })

    if request.method == "POST":
        p = products.query.filter(products.productname == request.json['pname'] , products.wt == str(request.json['weight'])).all()
        if len(p) > 0:
            return jsonify({
                'status' : 'unsuccessfull'
            })
        else:
            cat = categories.query.filter(categories.CName == request.json['pcatname']).first()
            counter = countervalues.query.first()
            product = products(productid = 'P' + str(counter.pcounter) , productname = request.json['pname'] , pcatid = cat.CategoryId , pcatname = request.json['pcatname'] , storeid = request.json['storeid'], mfgdate = request.json['mfg'] , expdate = request.json['exp'] , description = request.json['desc'] , price = request.json['price'] , qty = request.json['pqty'] , wt = request.json['weight'])
            counter.pcounter += 1
            db.session.add(product)
            db.session.commit()
            return jsonify({
                'status' : 'successfull'
            })
        
@app.route('/storemanager/removeproduct' , methods = ['GET','POST','DELETE'])
def remove():
    if request.method == "GET":
        pro = products.query.all()
        p = []
        for i in pro:
            p.append([i.productid,i.productname,i.pcatid,i.pcatname,i.storeid,i.mfgdate,i.expdate,i.description,i.price,i.qty,i.wt])
        return jsonify({
            'products' : p
        })
    
    if request.method == "DELETE":
        product = products.query.filter(products.productid == request.json['productid']).first()
        db.session.delete(product)
        db.session.commit()
        pro = products.query.all()
        p = []
        for i in pro:
            p.append([i.productid,i.productname,i.pcatid,i.pcatname,i.storeid,i.mfgdate,i.expdate,i.description,i.price,i.qty,i.wt])
        return jsonify({
            'status' : 'successfull',
            'products' : p
        })
    
    if request.method == "POST":
        p = products.query.filter(products.productid == request.json['pid']).first()
        p.productname = request.json['pname']
        p.pcatname = request.json['pcatname']
        p.description = request.json['desc']
        p.price = request.json['price']
        p.qty = request.json['pqty']
        db.session.commit()
        pro = products.query.all()
        p = []
        for i in pro:
            p.append([i.productid,i.productname,i.pcatid,i.pcatname,i.storeid,i.mfgdate,i.expdate,i.description,i.price,i.qty,i.wt])
        return jsonify({
            'products' : p
        })
    
@app.route('/storemanager/addcategory' , methods = ['GET' , 'POST'])
def addcat():
    if request.method == 'GET':
        req = requests.query.filter(requests.title == "Category addition request").all()
        r = []
        for i in req:
            r.append([i.title , i.managerid , i.categoryname , i.status])
        print(r)
        return jsonify({
            'requests' : r
        })

    if request.method == 'POST':
        c = countervalues.query.first()
        req = requests(requestid = 'R' + str(c.reqcounter) , title = "Category addition request" , managerid = request.json['smid'] , categoryname = request.json['catname'])
        c.reqcounter += 1
        db.session.add(req)
        db.session.commit()
        return jsonify({
            'status' : 'successfull'
        })
    
@app.route('/user/getstores' , methods = ['GET'])
def store():
    if request.method == "GET":
        st = stores.query.all()
        s = []
        for i in st:
            s.append([i.storeid , i.storename])
        return jsonify({
            'stores' : s
        })
    
@app.route('/user/getproducts' , methods = ['GET'])
@cache.cached(timeout=50)
def getproducts():
    if request.method == "GET":
        pr = products.query.all()
        p = []
        d = datetime.today().strftime("%Y-%m-%d")
        for i in pr:
            if i.expdate > d:
                p.append([i.productid,i.productname,i.pcatid,i.pcatname,i.storeid,i.mfgdate,i.expdate,i.description,i.price,i.qty,i.wt])
        return jsonify({
            'products' : p
        })
    
@app.route('/user/orders' , methods = ['POST'])
def placeorder():
    if request.method == "POST":
        c = countervalues.query.first()
        items = request.json['cart']
        d = datetime.today().strftime("%d-%m-%Y")
        IST = pytz.timezone('Asia/Kolkata')
        t = datetime.now(IST).strftime('%H:%M:%S')
        ordid = 'OD' + str(c.ordercounter)
        ord = orders(orderid = ordid , useremail = request.json['email'] , storeid = request.json['storeid'] , date = d , time = t , totalprice = request.json['totalprice'])
        db.session.add(ord)
        for i in items:
            orddetails = orderdetails(orderid = ordid , pcatname =  items[i]['details'][3] , productid = i , productname = items[i]['details'][1] , qty = items[i]['qty'] , price = items[i]['details'][8])
            pr = products.query.filter(products.productid == i).first()
            pr.qty -= items[i]['qty']
            db.session.add(orddetails)
        c.ordercounter += 1
        db.session.commit()
        ordersummary.delay(ordid,request.json['email'])
        return jsonify({
            'status' : 'successfull'
        })

@app.route('/myaccount/<string:email>', methods = ['GET'])
def userorders(email):
    if request.method == "GET":
        ord = orders.query.filter(orders.useremail == email).all()
        l = []
        for i in ord:
            l.append([i.orderid,i.useremail,i.storeid,i.date,i.time,i.totalprice])
        return jsonify({
            'orders' : l
        })
    
@app.route('/myaccount/<string:email>/<string:orderid>', methods = ['GET'])
def orddetails(orderid,email):
    if request.method == "GET":
        ord = orderdetails.query.filter(orderdetails.orderid == orderid).all()
        l = []
        for i in ord:
            l.append([i.orderid,i.productid,i.productname,i.qty,i.price])
        return jsonify({
            'orderdetails' : l
        })
    
@app.route('/productsreport/<string:storeid>' , methods = ['GET'])
def prodreport(storeid):
    if request.method == "GET":
        task = productssummaryreport.delay(storeid)
        return jsonify({
            'taskid' : task.id
        })

@app.route('/productsreportstatus/<string:taskid>' , methods = ['GET'])
def p(taskid):
    res =  productssummaryreport.AsyncResult(taskid)
    if res.ready():
        filename = res.result
        file_path = f'{filename}'
        return send_file(file_path,as_attachment=True,download_name=filename)
    else:
        return jsonify({
            'status' : True
        })
    
@app.route('/ordersreport/<string:storeid>' , methods = ['GET'])
def ordreport(storeid):
    if request.method == "GET":
        task = orderssummaryreport.delay(storeid)
        return jsonify({
            'taskid' : task.id
        })
    
@app.route('/orderreportstatus/<string:taskid>' , methods = ['GET'])
def o(taskid):
    res = orderssummaryreport.AsyncResult(taskid)
    if res.ready():
        filename = res.result
        file_path = f'{filename}'
        return send_file(file_path,as_attachment=True,download_name=filename)
    else:
        return jsonify({
            'status' : True
        })
    

@app.route('/storemanager/changestorename/<string:storeid>' , methods = ['POST'])
def change(storeid):
    if request.method == "POST":
        print("entered")
        s = stores.query.filter(stores.storeid == storeid).first()
        s.storename = request.json['newname']
        db.session.commit()
        return jsonify({
                'status' : 'successfull'
            })


#<------------------------------------------------------------------------------->
#<--------------------------------Celery Tasks ---------------------------------->
#<------------------------------------------------------------------------------->


@celery.on_after_configure.connect
def setup_periodic_emails(sender, **kwargs):
    sender.add_periodic_task(crontab(minute=0,hour=17),dailyremainder.s(),name = 'every day at 5pm')


@celery.on_after_configure.connect
def setup_periodic_emails(sender, **kwargs):
    sender.add_periodic_task(crontab(0,0,day_of_month='1'),monthlyreport.s(),name = 'monthly report')


@celery.task(name="main.dailyremainder")
def dailyremainder():
    visitors = users.query.all()
    d = datetime.today().strftime("%d-%m-%Y")
    for i in visitors:
        if i.lastvisited != d or i.lastvisited == '':
            with open('./grocery-store/dailyremainder.html','r') as f:
                temp = Template(f.read())
            send_dailyrem(i.email,temp.render())

def send_dailyrem(receiver,message):
    msg = MIMEMultipart()
    msg['Subject'] = '🌟 Your Grocery Genie Awaits! Unleash the Magic Today! 🛒✨'
    msg['From'] = senderemail
    msg['To']= receiver

    server = SMTP('smtp.gmail.com',587)
    server.starttls()

    msg.attach(MIMEText(message,'html'))
    server.login(senderemail,password)
    server.send_message(msg)
    server.quit()

@celery.task(name="main.monthlyreport")
def monthlyreport():
    visitors = users.query.all()
    d = datetime.now()
    d = d - timedelta(days=d.day)
    ord = orders.query.all()
    orddetails = orderdetails.query.all()
    month = d.strftime('%B')
    monthnum = d.month
    d = {}
    monthlyexpenditure = 0
    totalitems = 0
    for i in visitors:
        for j in ord:
            if j.useremail == i.email and str(j.date[3:5]) == str(monthnum):
                for k in orddetails:
                    if j.orderid == k.orderid:
                        if k.pcatname in d:
                            if k.productname in d[k.pcatname]:                                
                                d[k.pcatname][k.productname]+= k.qty
                            else:
                                d[k.pcatname][k.productname] = k.qty
                            totalitems += k.qty
                            monthlyexpenditure += k.qty*k.price
                        else:
                            d[k.pcatname] = {k.productname:k.qty}
                            totalitems += k.qty
                            monthlyexpenditure += k.qty*k.price
        with open('./grocery-store/monthlyreport.html','r') as f:
            temp = Template(f.read())
            send_monthreport(i.email,month,temp.render(username = i.username , month = month , d = d , monthlyexpenditure = monthlyexpenditure , totalitems = totalitems))

def send_monthreport(receiver,month,message):
    msg = MIMEMultipart()
    msg['Subject'] = '🌟 Your Monthly Grocery Explorer Report - ' + month + ' Edition 🛒✨'
    msg['From'] = senderemail
    msg['To']= receiver

    server = SMTP('smtp.gmail.com',587)
    server.starttls()

    msg.attach(MIMEText(message,'html'))
    server.login(senderemail,password)
    server.send_message(msg)
    server.quit()

@celery.task(name="main.ordersummary")
def ordersummary(ordid,email):
    orddetails = orderdetails.query.filter(orderdetails.orderid == ordid).all()
    l = []
    total = 0
    d = datetime.today().strftime("%d-%m-%Y")
    for i in orddetails:
        l.append([i.orderid,i.productname,i.qty,i.price])
        total += int(i.qty)*int(i.price)
    with open('./grocery-store/ordersummary.html','r') as f:
        temp = Template(f.read())
        send_ordersummary(email,ordid,temp.render(ordnum = ordid , date = d , l = l , total = total))

def send_ordersummary(receiver,ordid,message):
    msg = MIMEMultipart()
    msg['Subject'] = '🌟 Your Grocery Genie Order Summary - Order ' + ordid + ' 🛒✨'
    msg['From'] = senderemail
    msg['To']= receiver

    server = SMTP('smtp.gmail.com',587)
    server.starttls()

    msg.attach(MIMEText(message,'html'))
    server.login(senderemail,password)
    server.send_message(msg)
    server.quit()

@celery.task(name="main.productssummaryreport")
def productssummaryreport(storeid):
    p = products.query.filter(products.storeid == storeid).all()
    csv_output = excel.make_response_from_query_sets(p, ["productid" , "productname" , "pcatid" , "pcatname" , "mfgdate" , "expdate" , "description" , "price" , "qty" , "wt"] , "csv") 
    filename="productssummary.csv"
    with open(filename , 'wb') as f:
        f.write(csv_output.data)

    return filename

@celery.task(name="main.orderssummaryreport")
def orderssummaryreport(storeid):
    o = orders.query.join(orderdetails, orders.orderid == orderdetails.orderid).add_columns(orders.orderid,orders.date,orderdetails.pcatname,orderdetails.productid,orderdetails.productname,orderdetails.qty,orderdetails.price).filter(orders.storeid == storeid)
    csv_output = excel.make_response_from_query_sets(o, ["orderid" , "date" , "pcatname" , "productid" , "productname" , "qty" , "price"] , "csv")
    filename = "orderssummary.csv"
    with open(filename , 'wb') as f:
        f.write(csv_output.data)

    return filename


if __name__ == "__main__":
    app.run(debug=True)