from flask import *

from src.dbconnection import *

app=Flask(__name__)

@app.route('/login_post',methods=['post'])
def login_post():
    uname=request.form['uname']
    psw=request.form['pswd']
    qry="SELECT * FROM `login` WHERE `username`=%s AND `password`=%s "
    val=(uname,psw)
    res=selectone(qry,val)
    print(res)
    if res is None:
        return jsonify({"task":"invalid"})
    else:
        return jsonify({"task": "valid","id":res['login_id']})




@app.route('/addcamera1',methods=['post'])
def addcamera1():

    place=request.form['place']
    lid=request.form['lid']


    qry1="INSERT INTO `camera` VALUES(NULL,%s,%s)"
    val1=(lid,place)
    iud(qry1,val1)
    res = selectone(qry1, val1)
    print(res)
    if res is None:
        return jsonify({"task":"invalid"})
    else:
        return jsonify({"task": "valid"})

@app.route('/manage_camera',methods=['post'])
def manage_camera():
    qry="SELECT * FROM `camera` "
    res=selectall(qry)
    return jsonify(res)

@app.route('/view_cust_emotion',methods=['post'])
def view_cust_emotion():
    qry="SELECT * FROM `customer_emotion` JOIN `camera` ON `camera`.`cam_id`=`customer_emotion`.`cam_id` where `customer_emotion`.`emotions`='fear' OR `customer_emotion`.`emotions`='angry'"
    res=selectall(qry)
    print(res)
    return jsonify(res)

@app.route('/send_complaint',methods=['post'])
def send_complaint():
    lid = request.form['lid']
    compt = request.form['complaint']
    qry1 = "INSERT INTO `complaint` VALUES (NULL,%s,%s,curdate(),'pending')"
    val1 = (lid, compt)
    iud(qry1, val1)


    return jsonify({"task": "valid"})

@app.route('/view_reply',methods=['post'])
def view_reply():
    lid=request.form['lid']
    qry = "SELECT * FROM `complaint` where Login_id=%s"
    res = selectall2(qry,lid)
    print(res)
    return jsonify(res)

@app.route('/view_work',methods=['post'])
def view_work():
    wid=request.form['lid']
    qry = "SELECT `assign_work`.assign_id,assign_work.staff_lid,`assign_work`.status,`work`.* FROM `assign_work` JOIN `work` ON `assign_work`.wid=`work`.wid WHERE `assign_work`.staff_lid=%s  "
    res = selectall2(qry,wid)
    print(res)
    return jsonify(res)

@app.route('/updatestatus',methods=['post'])
def updatestatus():
    lid = request.form['wid']
    print(lid,"kkkkkkkkkkkkkkkkk")
    compt = request.form['status']
    qry1 = "UPDATE `assign_work` set status=%s where wid=%s"
    val1 = (compt, lid)
    iud(qry1, val1)
    return jsonify({"task": "valid"})

@app.route('/notification',methods=['post'])
def notification():

    return jsonify({"task":"yes"})

app.run(host="0.0.0.0",port="5000")



