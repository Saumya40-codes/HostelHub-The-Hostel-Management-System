#we will store standard route of our website
from flask import Blueprint,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required,current_user
from .models import User,hostellite,message,fee
from . import mess_db
from . import message_db
from . import fee_db
from .models import mess
views = Blueprint('views',__name__)

@views.route('/')
def home():
    return render_template('profiles.html')

@views.route('/hostelliteLogin')
def hostellitelogin():
    return render_template('login.html')

@views.route('/wardenLogin')
def wardenlogin():
    return render_template('warden_login.html')

@views.route('/wardenRegister')
def wardenRegister():
    return render_template('warden_register.html')

@views.route('/add_hostellite')
def add_hostellite():
    return render_template('add_hostellite.html')

@views.route('/add_mess')
def add_mess():
    return render_template('add_mess.html')


@views.route('/warden_dahsboard')
def warden_dashboard():
    return render_template('warden_dashboard.html')

@views.route('/roomsandservices/<username>/<hostel>')
def roomands(username,hostel):
    order = mess.query.order_by(mess.day).all()
    return render_template('RoomandServices.html',username=username,orders= order,hostel=hostel)


@views.route('/rent/<username>/<hostel>', methods=['GET', 'POST'])
def rent(username, hostel):
    from content import app
    import os
    if request.method == 'GET':
        order = mess.query.order_by(mess.day).all() 
        return render_template('hhpaymentform.html', username=username, orders=order, hostel=hostel)
    elif request.method == 'POST':
        order = mess.query.order_by(mess.day).all() 
        name = request.form.get('name')
        hoste = request.form.get('hostel')
        phone = request.form.get('phone')
        file = request.files['file'] 
        room = request.form.get('room')
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        details = fee(name=name, hostel=hoste, phone=phone, file=file.filename, room=room) 
        try:
            fee_db.session.add(details)
            fee_db.session.commit()
            return render_template('hhpaymentform.html', username=username, orders=order, hostel=hostel)
        except:
            return render_template('hhpayment.html', username=username, orders=order, hostel=hostel)


@views.route('/messageforwardem', methods=['GET','POST'])
def message_for_warden():
    if request.method == 'GET':
        info = message.query.order_by(message.username).all()
        return render_template('message_for_warden.html',infos=info)
    elif request.method == 'POST':
        message_id = request.form.get('message_id')
        message_to_delete = message.query.filter_by(id=message_id).first()
        try:
            message_db.session.delete(message_to_delete)
            message_db.session.commit()
            return redirect(url_for('auth.read_messages'))
        except:
            return render_template('message_for_warden.html')
    
@views.route('/search_hostellite/<username>/<hostel>')
def search(username,hostel):
    order = mess.query.order_by(mess.day).all() 
    return render_template('search.html',info=None,more_info = None,username=username,orders= order,hostel=hostel,nothing=True)

@views.route('/hostellite_dashboard/<username>/<hostel>',methods=['GET'])
def hostellite_dashboard(username,hostel):
    order = mess.query.order_by(mess.day).all() 
    return render_template('dashboard_hostellite.html',username=username,orders= order,hostel=hostel)
