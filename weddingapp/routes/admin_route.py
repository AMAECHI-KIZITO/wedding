from flask import Flask,render_template,make_response,abort,request,redirect,flash,session,url_for
from weddingapp import wed,db,csrf
from datetime import datetime
from weddingapp.models import *


@wed.route('/admin/',methods=['POST','GET'])
@csrf.exempt
def admin_home():
    if request.method=='GET':
        return render_template('admin/admin_login.html')
    else:
        #form submitted
        username=request.form['username']
        pwd=request.form['pswd']
        
        ad=Admin.query.filter(Admin.admin_username==username,Admin.admin_pwd==pwd).first()
        if ad:
            adminid=ad.admin_id
            admin_fullname=ad.admin_name
            session['adminid']=adminid
            session['adminname']=admin_fullname
            return redirect(url_for('admin_board'))
        else:
            flash('Invalid Credentials')
            return redirect('/admin')
        
@wed.route('/dashboard/')
def admin_board():
    if session.get('adminid') != None and session.get('adminname') != None:
        return render_template('admin/admin_dashboard.html')
    else:
        return redirect('/admin/')
    
@wed.route('/logout/')
def admin_logout():
    session.pop('adminid',None)
    session.pop('adminname',None)
    return redirect('/admin/')

@wed.after_request
def clearcache(response):
    response.headers['Cache-Control']='no-cache, no store, must-revalidate'
    return response

@wed.route('/gift/')
def manage_gifts():
    if session.get('adminid') != None and session.get('adminname') != None:
        ag=db.session.query(Gifts).order_by(Gifts.gift_name).all()
        return render_template('admin/all_gifts.html',ag=ag)
    else:
        return redirect('/admin/')
    
@wed.route('/addgift/',methods=['POST','GET'])
def addgifts():
    if session.get('adminid') != None and session.get('adminname') != None:
        if request.method=='GET':
            return render_template('admin/addgift.html')
        else:
                newgift=request.form.get('giftname')
                g=Gifts(gift_name=newgift)
                db.session.add(g)
                db.session.commit()
                
                
                flash('Successfully Added',category='added')
                return redirect('/gift/')
    else:
        return redirect('/admin/')
    
@wed.route('/deletegift/<gift_id>')
def del_gifts(gift_id):
    x=db.session.query(Gifts).get(gift_id)
    db.session.delete(x)
    db.session.commit()
    flash('Gift Deleted',category='delete')
    return redirect('/gift')


@wed.route('/allguests/')
def view_all_guests():
    if session.get('adminid') != None and session.get('adminname') != None:
        coming=db.session.query(Guests).all()
        return render_template('admin/allguests.html',invite=coming)
    else:
        return redirect('/admin/')

@wed.route('/editgift/<gift_id>')
def edit_gifts(gift_id):
    data=db.session.query(Gifts).get(gift_id)
    return render_template('admin/editgift.html',data=data)

@wed.route('/update/',methods=['POST'])
def update_gifts():
    newgiftname=request.form.get('giftname')
    id=request.form.get('g_id')
    changes=db.session.query(Gifts).get(id)
    if changes:
        changes.gift_name=newgiftname
        db.session.commit()
        flash('Gift name updated',category='updatedgift')
        return redirect('/gift/')
