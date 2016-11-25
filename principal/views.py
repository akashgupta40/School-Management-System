from django.shortcuts import render,HttpResponseRedirect,render_to_response,RequestContext
#from .models import Question
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib import messages
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.db.models import F
from django.db.models.expressions import CombinedExpression, Value
from django.shortcuts import redirect
from django.core.mail import send_mail
import MySQLdb


@login_required(login_url='/admin/')
def principal_feedback(request):
	if(request.user.last_name!="principal"):
		e="Not authorised to view it.Only principal has access."
		return render(request,'head.html',{'e':e})
	db = MySQLdb.connect("127.0.0.1","root","admin","school2")
	c = db.cursor()
	sql1="SELECT name from faculty"
	c.execute(sql1)
	faculties=c.fetchall()
	v=len(faculties)>0

	if(request.method=="GET"):
		context={'user':request.user,'flag': request.user.is_authenticated(),'faculties':faculties,'v':v}
		return render(request,'principal_feedback.html',context)
	name=str(request.POST["name"])
	sql2="select DISTINCT feedback from feedback,class_going_on,faculty where class_going_on.faculty_id=faculty.faculty_id and faculty.name='%s'"%(name) 
	c.execute(sql2)
	feedbacks=c.fetchall()
	t=len(feedbacks)>0
	context={'user':request.user,'flag': request.user.is_authenticated(),'faculties':faculties,'v':v,'t':t,'feedbacks':feedbacks,'name':name}
	return render(request,'principal_feedback.html',context)
	



def principal(request):
	if(request.method=="GET"):
		t=["class","class_going_on","course","faculty","feedback","mark","notice","student","time_slot"]
		db = MySQLdb.connect("127.0.0.1","root","admin","school2")
		c = db.cursor()
                ans=[]
		for table in t:
			sql="desc %s"%(table)
			print sql
			c.execute(sql)
			col=c.fetchall()
			attr=[]
			for row in col:
				attr.append(row[0])
			pair=[]
			pair.append(table)
			pair.append(attr)
			ans.append(pair)
		print ans
		context={'user':request.user,'flag': request.user.is_authenticated(),'maps':ans}
		return render(request,'principal.html',context)

def class_insert(request):
    if(request.method=="POST" ):
	    try:
		    class_id=int(request.POST["class_id"])
		    classs=int(request.POST["class"])
		    room=int(request.POST["room"])
		    db = MySQLdb.connect("127.0.0.1","root","admin","school2")
		    c = db.cursor()
		    sql="INSERT INTO class values(%d,%d,%d)"%(class_id,classs,room)
		    c.execute(sql)
		    db.commit()
		    print "inserted"
		    post="Data is successfully inserted into table CLASS"
		    context={'post':post,'user':request.user,'flag': request.user.is_authenticated()}
		    return render(request,'principal.html',context)
	    except Exception as e:
	    	    print e
		    print "yo"
		    context={'e':e,'user':request.user,'flag': request.user.is_authenticated()}
		    return render(request,'principal.html',context)
    else:
	    e="Operation not supported or you are not authorised"
	    context={'e':e,'user':request.user,'flag': request.user.is_authenticated() }
	    return render(request,'principal.html',context)


def class_going_on_insert(request):
    if(request.method=="POST" ):
	    try:
		    class_going_on_id=int(request.POST["class_going_on_id"])
		    exam_type=str(request.POST["exam_type"])
		    course_id=int(request.POST["course_id"])
		    class_id=int(request.POST["class_id"])
		    faculty_id=int(request.POST["faculty_id"])
		    db = MySQLdb.connect("127.0.0.1","root","admin","school2")
		    c = db.cursor()
		    sql="INSERT INTO class_going_on(class_going_on_id,exam_type,course_id,class_id,faculty_id) values(%d,'%s',%d,%d,%d)"%(class_going_on_id,exam_type,course_id,class_id,faculty_id)
		    c.execute(sql)
		    db.commit()
		    print "inserted"
		    post="Data is successfully inserted into table CLASS_GOING_ON"
		    context={'post':post,'user':request.user,'flag': request.user.is_authenticated()}
		    return render(request,'principal.html',context)
	    except Exception as e:
	    	    print e
		    print "yo"
		    context={'e':e,'user':request.user,'flag': request.user.is_authenticated()}
		    return render(request,'principal.html',context)
    else:
	    e="Operation not supported or you are not authorised"
	    context={'e':e,'user':request.user,'flag': request.user.is_authenticated() }
	    return render(request,'principal.html',context)










