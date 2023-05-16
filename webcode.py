from flask import *

from src.dbconnection import *


app=Flask(__name__)
app.secret_key="ndfdjf"

import functools

def login_required(func):
    @functools.wraps(func)
    def secure_function():
        if "lid" not in session:
            return render_template('login_index.html')
        return func()

    return secure_function


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')




@app.route('/')
def login():
    return render_template('login_index.html')

@app.route('/login_post',methods=['post'])
def login_post():
    uname=request.form['textfield']
    psw=request.form['textfield2']
    qry="SELECT * FROM `login` WHERE `username`=%s AND `password`=%s"
    val=(uname,psw)
    res=selectone(qry,val)
    print(res)
    if res is None:
        return '''<script>alert("Invalid username or password");window.location='/'</script>'''
    elif res['type']=='admin':
        session['lid']=res['login_id']
        return '''<script>alert("Welcome admin");window.location='/admin_home'</script>'''
    else:
        return '''<script>alert("Invalid");window.location='/'</script>'''


#=============================================ADMIN====================================
@app.route('/admin_home')
def admin_home():
    return render_template('admin_home.html')

@app.route('/view_staff')
def view_staff():
    qry="SELECT * FROM `staff` "
    res=selectall(qry)
    return render_template('view_staff.html',val=res)

@app.route('/add_staff')
@login_required
def add_staff():
    return render_template('add_staff.html')


@app.route('/addstaff1',methods=['post'])
@login_required
def addstaff1():
    firstname=request.form['textfield']
    lastname=request.form['textfield2']
    place=request.form['textfield3']

    pin=request.form['textfield5']
    phone=request.form['textfield6']
    email=request.form['textfield7']
    gender=request.form['radiobutton']
    username=request.form['textfield9']
    password=request.form['textfield10']
    qry="INSERT INTO login VALUES(NULL,%s,%s,'staff')"
    val=(username,password)
    id=iud(qry,val)
    qry1="INSERT INTO `staff` VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s)"
    val1=(id,firstname,lastname,gender,place,pin,phone,email)
    iud(qry1,val1)
    return '''<script>alert("STAFF ADDED");window.location='view_staff'</script>'''


@app.route('/edit_staff')
@login_required
def edit_staff():
    id = request.args.get('id')
    session['se_id'] = id
    qry="SELECT * FROM `staff` WHERE `Login_id`=%s"
    res=selectone(qry,id)

    return render_template('edit_staff.html',val=res)


@app.route('/edit_staff1',methods=['post'])
@login_required
def edit_staff1():
    firstname=request.form['textfield']
    lastname=request.form['textfield2']
    place=request.form['textfield3']

    pin=request.form['textfield5']
    phone=request.form['textfield6']
    email=request.form['textfield7']
    gender=request.form['radiobutton']
    qry1="UPDATE `staff` SET `first_name`=%s,`last_name`=%s,`gender`=%s,`place`=%s,`pin`=%s,`phone`=%s,`email`=%s WHERE `Login_id`=%s"
    val1=(firstname,lastname,gender,place,pin,phone,email,session['se_id'])
    iud(qry1,val1)
    return '''<script>alert("EDITED SUCCESSFULLY");window.location='view_staff'</script>'''




@app.route('/view_works')
@login_required
def view_works():
    qry="SELECT * FROM `work`"
    res=selectall(qry)
    return render_template('view_works.html',val=res)

@app.route('/add_work',methods=['post'])
@login_required
def add_work():
    return render_template('add_work.html')

@app.route('/addwork1',methods=['post'])
@login_required
def addwork1():
    work=request.form['textfield']
    qry1="INSERT INTO `work` VALUES (NULL,%s,CURDATE())"
    val1=(work)
    iud(qry1,val1)
    return '''<script>alert("WORK ADDED");window.location='view_works'</script>'''

@app.route('/assign_work')
@login_required
def assign_work():
    wid=request.args.get('id')
    session['wid']=wid
    qry="SELECT * FROM `staff`"
    res=selectall(qry)
    return render_template('assign_work.html',val=res)

@app.route('/assign_post',methods=['post'])
@login_required
def assign_post():
    staff=request.form['select']
    q="INSERT INTO `assign_work` VALUES (NULL,%s,%s,CURDATE(),'pending')"
    val=(session['wid'],staff)
    iud(q,val)
    return '''<script>alert("Assigned");window.location='view_works'</script>'''

@app.route('/view_work_status')
@login_required
def view_work_status():
    qry="SELECT `assign_work`.*,`work`.*,`staff`.* FROM `assign_work` JOIN `staff` ON `assign_work`.`staff_lid`=`staff`.`Login_id` JOIN `work` ON `assign_work`.`wid`=`work`.`wid`"
    res=selectall(qry)
    return render_template('view_work_status.html',val=res)

@app.route('/view_complaint')
@login_required
def view_complaint():
    qry="SELECT `staff`.`first_name`,`last_name` ,`complaint`.* FROM `staff` JOIN `complaint` ON `staff`.`Login_id`=`complaint`.`Login_id`"
    res=selectall(qry)
    return render_template('view_complaint.html',val=res)

@app.route('/send_reply')
@login_required
def send_reply():
    id=request.args.get('cid')
    session['Com_id']=id
    return render_template('send_reply.html')

@app.route('/sendreply1',methods=['post'])
@login_required
def sendreply1():
    reply=request.form['textarea']

    qry1="UPDATE `complaint` SET `reply`=%s WHERE `comp_id`=%s"
    val1=(reply,session['Com_id'])
    iud(qry1,val1)
    return '''<script>alert("REPLY SEND");window.location='view_complaint#about'</script>'''


@app.route('/delete_staff')
@login_required
def delete_staff():
    id=request.args.get('id')
    qry="DELETE FROM `login` WHERE `login_id`=%s"
    val=(id)
    iud(qry,val)
    qry1="DELETE FROM `staff` WHERE `Login_id`=%s"
    iud(qry1,id)
    return '''<script>alert("DELETED ");window.location='view_staff'</script>'''

@app.route('/delete_work')
@login_required
def delete_work():
    id=request.args.get('id')
    qry="DELETE FROM `work` WHERE `wid`=%s"
    iud(qry,id)
    return '''<script>alert("DELETED ");window.location='view_works'</script>'''

@app.route('/add_camera',methods=['post'])
@login_required
def add_camera():
    return render_template('add_camera.html')

@app.route('/addcamera1',methods=['post'])
@login_required
def addcamera1():
    place=request.form['textfield2']
    camera_no=request.form['textfield']
    qry1="INSERT INTO `camera` VALUES (NULL,%s,%s)"
    val1=(place,camera_no)
    iud(qry1,val1)
    return '''<script>alert("CAMERA ADDED");window.location='manage_camera'</script>'''

@app.route('/manage_camera')
@login_required
def manage_camera():
    qry="SELECT * FROM `camera`"
    res=selectall(qry)
    return render_template('manage_camera.html',val=res)

@app.route('/delete_camera')
@login_required
def delete_camera():
    id=request.args.get('id')
    qry="DELETE FROM `camera` WHERE `cam_id`=%s"
    iud(qry,id)
    return '''<script>alert("DELETED ");window.location='manage_camera'</script>'''











app.run(debug=True)