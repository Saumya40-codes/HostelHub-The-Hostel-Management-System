from flask import Blueprint,render_template,request,flash,redirect,url_for,send_from_directory
from .models import User,hostellite,mess,message,info,infow,fee
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_user , login_required , logout_user , current_user
from . import hostellite_db
from . import mess_db
from . import message_db
from . import info_db
from . import infow_db
from . import fee_db

auth = Blueprint('auth',__name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hostel = request.form.get('hostel')

        user = User.query.filter_by(username=username).first()
        hostel_exists = User.query.filter_by(hostel=hostel).first()
        if user:
            if hostel_exists:
                if check_password_hash(user.password,password):
                    return render_template('warden_dashboard.html',username=username,hostel=hostel)
                else:
                    flash('Incorrect Password Entered',category='error')
                    return render_template('warden_login.html')
            else:
                 flash('Hostel name not found correct for given username',category='error')
                 return render_template('warden_login.html')       
        else:
            flash("Username doesn\'t exists. Please signup to get your hostel access to our site",category='error')    
            return render_template('warden_login.html')

    return render_template('warden_login.html')


@auth.route('/logout')
def logout():
    return "logout"

@auth.route('/signup',methods=['GET','POST'])
def signup():
    if(request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        hostel = request.form.get('hostel')

        user = User.query.filter_by(username=username).first()
        hostel_h = User.query.filter_by(hostel=hostel).first()

        if user:
            flash('Username already exists',category='error')
            return render_template('warden_register.html')
        if len(username) < 1:
            flash("Please enter a valid username.",category='error')
        elif len(password) < 7:
            flash("Please enter a password having length more than 7",category='error')
        else:
            new_user = User(username=username,password=generate_password_hash(password ,method='sha256'),hostel=hostel)
            db.session.add(new_user)
            db.session.commit()
            redirect(url_for('views.home'))
            flash('Account created. Now please redirect to login page to access your account ',category='success')

    return render_template("warden_register.html")

@auth.route('/add_info',methods=['GET','POST'])
def add_info():
    if request.method == 'POST':
        new_name = request.form.get('new_name')
        new_floor = request.form.get('new_floor')
        new_room = request.form.get('new_room')
        new_hostel = request.form.get('hostel_name')
        new_entry = hostellite(username=new_name,hostel=new_hostel,room=new_room,floor=new_floor)
        to_check = hostellite.query.filter_by(username=new_name,hostel=new_hostel,room=new_room,floor=new_floor).first()
        already_full = hostellite.query.filter_by(hostel=new_hostel,room=new_room,floor=new_floor).first()
        if(not(to_check) or not(already_full)):
            hostellite_db.session.add(new_entry)
            hostellite_db.session.commit()
            data = hostellite.query.order_by(hostellite.username).all()
            flash("Database created",category='success')
            return render_template('add_hostellite.html', datas=data)
        else:
            flash("The given room has already been occupied by other hostellites",category='error')
            return render_template('add_hostellite.html')

    else:
        data = hostellite.query.order_by(hostellite.username).all()
        return render_template('add_hostellite.html',datas = data)

@auth.route('/add_mess',methods=['GET','POST'])
def add_mess():
    if(request.method == 'POST'):
        food = request.form.get('food')
        tye = request.form.get('type')
        day = request.form.get('day')

        new_entry = mess(food=food,type = tye,day = day)
        order = mess.query.order_by(mess.day).all()
        try:
            mess_db.session.add(new_entry)
            mess_db.session.commit()
            return render_template('add_mess.html',orders = order)
        except:
            return render_template('add_mess.html')
    else:
        return render_template('add_mess.html',orders = order)

@auth.route('/hostellite_login',methods=['GET','POST'])
def hostellite_login():
    if request.method == 'POST':
        username_h = request.form.get('username')
        hostel_h = request.form.get('hostel')
        user_h = hostellite.query.filter_by(username=username_h).first()
        hostel_exists_h = hostellite.query.filter_by(hostel=hostel_h).first()
        if hostel_exists_h:
            if user_h:               
                order = mess.query.order_by(mess.day).all() 
                print(username_h,'logged in !!')  
                return render_template('dashboard_hostellite.html',hostel = hostel_h,username=username_h,orders= order)
            else:
                flash("Username does\'nt exists please contact your hostel authoraties to create your account",category='error')
                return render_template('login.html')
        else:
            flash("Your hostel name doesnt exists on our database",category='error')
            return render_template('login.html')
    return render_template('login.html')

@auth.route('/send_message/<username>/<hostel>',methods=['GET','POST'])
def send_message(username,hostel):
    if request.method == 'POST':
        name = request.form.get('username')
        subject = request.form.get('Subject')
        query = request.form.get('Query')
        to_add = message(username = name,subject=subject,info=query)
        try:
            message_db.session.add(to_add)
            message_db.session.commit()
            flash("Message sent",category='success')
            redirect(url_for('roomands',username=username,hostel=hostel))
        except:
            return render_template('RoomandServices.html',username=username,hostel=hostel)
    else:
        return render_template('RoomandServices.html',username=username,hostel=hostel)


@auth.route('/get_message')
def read_messages():
    if request.method == 'GET':
        info = message.query.order_by(message.username).all()
        return render_template('message_for_warden.html',infos=info)

@auth.route('/search_hostellites/<username>/<hostel>', methods=['GET','POST'])
def search(username,hostel):
    if request.method == 'POST':
        name = request.form.get('name')
        hoste = request.form.get('hostel')
        details = hostellite.query.filter_by(username=name, hostel=hoste).first()
        add_details = info.query.filter_by(name=name).order_by(info.id.desc()).first()
        if(details):
            return render_template('search.html', info=details, more_info=add_details,username=username,hostel=hostel)
        else:
            return render_template('search.html',info=None, more_info=None,username=username,hostel=hostel,notfound = True)
    else:
        return render_template('search.html', info=None,more_info = None,username=username,hostel=hostel)


@auth.route('/show_profile/<username>/<hostel>', methods=['GET', 'POST'])
def show_profile(username,hostel):
    if request.method == 'GET':
        user_detail = hostellite.query.filter_by(username=username).first()
        data = info.query.filter_by(name=username).order_by(info.id.desc()).first()
        return render_template('profile_user.html',  user=user_detail,datas=data,username=username,hostel=hostel)
    else:
        clg = request.form.get('college')
        stream = request.form.get('stream')
        name = request.form.get('name')
        phone = request.form.get('phone')
        infos = info(name=name,college=clg,stream=stream,phone=phone)
        try:
            info_db.session.add(infos)
            info_db.session.commit()
            user_detail = hostellite.query.filter_by(username=username).first()
            data = info.query.filter_by(name=username).order_by(info.id.desc()).first()
            return render_template('profile_user.html',  user=user_detail,datas = data,username=username,hostel=hostel)
        except:
            flash("Couldn't excess database",category='error')
            return render_template('profile_user.html',username=username,hostel=hostel)

@auth.route('/warden_profile/<username>/<hostel>', methods=['GET', 'POST'])
def warden_profile(username, hostel):
    if request.method == 'GET':
        user_detail = User.query.filter_by(username=username).first()
        data = infow.query.filter_by(name=username).order_by(infow.id.desc()).first()
        return render_template('warden_profile.html', user=user_detail, datas=data,username=username,hostel=hostel)
    elif request.method == 'POST':
        phone = request.form.get('phone')
        add = request.form.get('add')
        name = request.form.get('name')
        infos = infow(name=name, add=add, phone=phone)
        try:
            infow_db.session.add(infos)
            infow_db.session.commit()
            user_detail = User.query.filter_by(username=username).first()
            data = infow.query.filter_by(name=username).order_by(infow.id.desc()).first()
            return render_template('warden_profile.html', user=user_detail, datas=data,username=username,hostel=hostel)
        except:
            flash("Couldn't access database", category='error')
            return render_template('warden_profile.html.html', username=username, hostel=hostel)


@auth.route('/fee_status/<hostel>')
def fee_status(hostel):
    has_paid = fee.query.filter_by(hostel=hostel).all()
    not_paid = hostellite.query.filter_by(hostel=hostel).all()
    return render_template('fee_status.html',hostel=hostel, fee_info = has_paid , np = not_paid)

