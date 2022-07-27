import requests
import random
from flask import render_template,make_response,redirect,session,abort,request,flash,request,jsonify
from weddingapp import wed,db
from weddingapp.forms import *
from weddingapp.models import *

@wed.route('/')
def home():
    return render_template('user/index.html')

@wed.route('/signup/')
def usersignup():
    sform=UserSignup()
    return render_template('user/signup.html',sform=sform)


@wed.route('/message/')
def Contact_Us():
    if session.get('adminid') != None and session.get('adminname') != None:
        cform=ContactForm()
        return render_template('user/contactus.html',cform=cform)
    else:
        return redirect('/admin/')
    
@wed.route('/submitcontact/',methods=['POST'])
def submitcontact():
    cform=ContactForm()
    
    if request.method=='GET':
        return redirect('/message/')
    else:
        if cform.validate_on_submit():
            name=request.form.get('fullname')
            email=request.form.get('email')
            message=request.form.get('message')
            
            c=Contact(con_fullname=name,con_email=email,con_message=message)
            db.session.add(c)
            db.session.commit()
            flash('Successful',category='message_sent')
            return redirect('/message/')
        
@wed.route('/submitsignup/',methods=['POST'])
def submitsignup():
    sform=UserSignup()
    
    if request.method=='GET':
        return redirect('/signup/')
    else:
        if sform.validate_on_submit():
            firstname=request.form.get('g_firstname')
            lastname=request.form.get('g_lastname')
            uemail=request.form.get('g_email')
            uaddress=request.form.get('g_address')
            pswd=request.form.get('g_pswd')
            cpswd=request.form.get('g_confirmpswd')
            
            
            reg=Guests(guest_fname=firstname, guest_email=uemail, guest_lname=lastname, guest_pwd=cpswd,guest_address=uaddress)
            db.session.add(reg)
            db.session.commit()
            
            session['guest_id']=reg.guest_id
            session['name']=reg.guest_fname
            flash('Successful Registration',category='Reg Complete')
            return redirect('/profile/')
        else:
            flash('Signup Failed',category='failed signup')
            return redirect('/signup/')


@wed.route('/login/')
def userlogin():
    return render_template('user/login.html')

@wed.route('/submitlogin/',methods=['POST'])
def verifyuser():
    email=request.form.get('email')
    pskey=request.form.get('pswd1')
    
    allow=db.session.query(Guests).filter(Guests.guest_email==email,Guests.guest_pwd==pskey).first()
    if allow:
        session['guest_id']=allow.guest_id
        session['name']=allow.guest_fname
        return redirect('/profile/')
    else:
        flash(f'Incorrect Credentials',category='Wrong')
        return redirect('/login/')

@wed.route('/profile/')
def userprofile():
    return render_template('user/profile.html')

@wed.route('/uploadpic/')
def upload_picture():
    return render_template('user/uploadpic.html')

@wed.route('/registry/')
def displaygifts():
    if session.get('guest_id')!=None:
        giftschoice=db.session.query(Gifts).all()
        return render_template('user/usergift.html',giftschoice=giftschoice)
    else:
        return redirect('/login/')
    
    

@wed.route('/submitregistry/',methods=['POST'])
def submitregistry():
    if session.get('guest_id')!=None:
        login=session.get('guest_id')
        
        requestedgift=request.form.getlist('gifts_fromuser')
        
        #to have updated record
        db.session.execute(f"DELETE FROM guest_gift where g_guestid='{login}'")
        db.session.commit()
        
        for w in requestedgift:
            GG=Guest_gift()
            db.session.add(GG)
            GG.g_giftid = w
            GG.g_guestid = login
            db.session.commit()
        return 'Done'
    else:
        return redirect('/login/')
    
@wed.route('/forum/')
def forum():
    return render_template('user/forum.html')

@wed.route('/send_forum/')
def sendforum():
    msg=request.args.get('suggestion')
    user=session.get('guest_id')
    c=Comment(comment_guestID=user,comment_message=msg)
    db.session.add(c)
    db.session.commit()
    return f'Thank you message received'



####BELOW ARE FOR AJAX DEMO
@wed.route('/ajaxtests/')
def ajaxtests():
    states=db.session.query(State).all()
    return render_template('user/testing.html',states=states)

@wed.route('/ajaxtests/checkusername')
def ajaxtests_submit():
    user=request.values.get('username')
    check=db.session.query(Guests).filter(Guests.guest_email==user).first()
    if check!=None:
        return "Username has been taken"
    else:
        return "Username is available"
    
##AJAX STATES
@wed.route('/ajaxtests/state')
def ajaxtests_state():
    selected=request.args.get('stateid')
    statelga=db.session.query(Lga).filter(Lga.state_id==selected).all()
    
    lgachoices=""
    for x in statelga:
        lgachoices=lgachoices + f"<option value='{x.lga_id}' >{x.lga_name}</option>"
        
    return lgachoices

@wed.route('/ajaxtests/final',methods=['POST'])
def final_test():
    appended_data=request.form.get('missing')
    lastname=request.form.get('lastname')
    firstname=request.form.get('firstname')
    
    fileobj=request.files['image']
    original_filename=fileobj.filename
    fileobj.save(f'weddingapp/static/images/{original_filename}')
    
    return jsonify(firstname=firstname,lastname=lastname,appended_data=appended_data,filename=original_filename)

@wed.route('/accommodation/')
def accommodation():
    username='zaynab'
    password='abcd'
    try:
        rsp=requests.get("http://127.0.0.1:7000/api/v1.0/getall", auth=(username,password))
        rsp_json=rsp.json() #converts rsp from HTTP response to json
        return render_template('user/hotels.html',rsp_json=rsp_json)
    except:
        return "Please try again the server is currently down"
    
def getprice(itemID):
    deets=Uniform.query.get(itemID)
    if deets!=None:
        return deets.uni_price
    else:
        return 0
    
def generate_ref():
    ref=random.random() *1000000
    return int(ref)
    
@wed.route('/buyasoebi/',methods=['POST','GET'])
def purchase_asoebi():
    loggedin=session.get('guest_id')
    if loggedin != None:
        if request.method=='GET':
            asoebi=db.session.query(Uniform).all()
            return render_template('user/asoebi.html',asoebi=asoebi)
        else:
            uniform_selected=request.form.getlist('uniform')
            if uniform_selected:
                #inserting into order table
                ref=generate_ref()
                session['reference']=ref
                ord=Orders(order_by=loggedin,order_status='Pending',order_ref=ref)
                db.session.add(ord)
                db.session.commit()
                
                #inserting into order details
                orderid=ord.order_id
                total=0
                for i in uniform_selected:
                    price=getprice(i)
                    ord_det=Order_details(det_orderid=orderid, det_itemid=i, det_itemprice=price)
                    db.session.add(ord_det)
                    total=total+price
                ord.order_totalamt=total
                db.session.commit()
                return redirect('/confirmation/')
            else:
                flash('Please make a selection')
                return redirect('/buyasoebi')
    else:
        return redirect('/login')

@wed.route('/confirmation/')
def confirmation():
    loggedin=session.get('guest_id')
    ref=session.get('reference')
    if loggedin!=None:
        deets = db.session.query(Orders,Order_details,Uniform).join(Order_details,Orders.order_id==Order_details.det_orderid).join(Uniform,Order_details.det_itemid==Uniform.uni_id).filter(Orders.order_by==loggedin, Orders.order_ref==ref).all()
        
        t=Orders.query.filter(Orders.order_ref==ref).first()
        return render_template('user/confirmation_page.html',deets=deets,total=t.order_totalamt)
    else:
        return redirect('/login/')