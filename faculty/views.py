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
import MySQLdb

@login_required(login_url='/home/')
def faculty_class_course(request):
	if request.user.last_name!="faculty":
		e="Not authrised"
		return render(request,'faculty_class_course.html',{'e':e,'flag': request.user.is_authenticated(),'user':request.user})
	if request.method=="GET":
		return render(request,'faculty_class_course.html',{'flag': request.user.is_authenticated(),'user':request.user})
	elif request.method=="POST":
		try:
	 		class_id=int(request.POST["class"])
	 		course=str(request.POST["course"])
	 		exam_type=str(request.POST["exam_type"])
	 		user_type="faculty"
	 		email=request.user.username
			print class_id,course,exam_type,email
	 		db = MySQLdb.connect("127.0.0.1","root","admin","school2")
	 		c = db.cursor()
			print "in"
			sql0="select course_id from course where name='%s'"%(course)
			print sql0
			c.execute(sql0)
			course_id=c.fetchone()
			print course_id
	 		sql1="select faculty_id from faculty where email='%s'"%(email)
	 		c.execute(sql1)
	 		faculty_id=c.fetchone()
	 		print faculty_id
	 		sql="INSERT INTO class_going_on(exam_type,faculty_id,course_id,class_id) values('%s',%d,%d,%d)"%(exam_type,int(faculty_id[0]),course_id[0],class_id)
	 		c.execute(sql)
	 		db.commit()
	 		post="Added successfully"
	 		return render(request,'faculty_class_course.html',{'post':post,'flag': request.user.is_authenticated(),'user':request.user})
	 		print "inserted"
		except Exception as e:
			print e
			return render(request,'faculty_class_course.html',{'e':e,'flag': request.user.is_authenticated(),'user':request.user})


@login_required(login_url='/home/')
def faculty_class_course_time(request):
	if request.user.last_name!="faculty":
		e="Not authrised"
		return render(request,'head.html',{'e':e,'flag': request.user.is_authenticated(),'user':request.user})
	if request.method=="GET":
		return render(request,'faculty_class_course_time.html',{'flag': request.user.is_authenticated(),'user':request.user})
	elif request.method=="POST":
		try:
	 		class_id=int(request.POST["class"])
			day=str(request.POST["day"])
			period=int(request.POST["period"])
	 		course=str(request.POST["course"])
	 		exam_type=str(request.POST["exam_type"])
	 		user_type="faculty"
	 		email=request.user.username
			print class_id,course,exam_type,email
	 		db = MySQLdb.connect("127.0.0.1","root","admin","school2")
	 		c = db.cursor()
			print "in"
			sql0="select course_id from course where name='%s'"%(course)
			print sql0
			c.execute(sql0)
			course_id=c.fetchone()
			print course_id
	 		sql1="select faculty_id from faculty where email='%s'"%(email)
	 		c.execute(sql1)
	 		faculty_id=c.fetchone()
	 		print faculty_id
			sql2="select class_going_on_id from class_going_on where exam_type='%s' and faculty_id=%d and course_id=%d and class_id=%d"%(exam_type,int(faculty_id[0]),course_id[0],class_id)
			c.execute(sql2)
			class_going_on_id=c.fetchone()
			sql="insert into time_slot(day,period,class_going_on_id) values('%s',%d,%d)"%(day,period,class_going_on_id[0])
			print "inserted"
	 		c.execute(sql)
	 		db.commit()
	 		post="Added successfully"
	 		return render(request,'faculty_class_course.html',{'post':post,'flag': request.user.is_authenticated(),'user':request.user})
	 		print "inserted"
		except Exception as e:
			print e
			return render(request,'faculty_class_course.html',{'e':e,'flag': request.user.is_authenticated(),'user':request.user})






def register_faculty(request):
	if request.method=="GET":
		return render(request,'register_faculty.html',{'flag': request.user.is_authenticated(),'user':request.user})
	elif request.method=="POST":
 		name=str(request.POST["name"])
 		user_type="faculty"
 		email=request.POST["email"]
 		username=email
 		password=request.POST["password"]
 		phone=int(request.POST["phone"])
 		print "user saved"
 		try:
	 		db = MySQLdb.connect("127.0.0.1","root","admin","school2")
			c = db.cursor()
			sql = "INSERT INTO faculty(name,email,phone) values ('%s','%s',%d)" % (name,email,phone)
			print sql
			c.execute(sql)
	 		user = User.objects.create_user(username,email,password)
	 		user.first_name = name
	 		user.last_name = user_type
	 		user.save()			
			db.commit()
			u=username
			p=password
			auth_login(request,authenticate(username=u, password=p))

			return redirect('/faculty_class_course/')
		except Exception as e:
			print e
			print "hello"
			context={ 'e':e[1],'flag': request.user.is_authenticated(),'user':request.user}
			return render(request,'register_faculty.html',context)


def login_faculty(request):
	if request.method=="GET":
		return render(request,'login_faculty.html',{'flag': request.user.is_authenticated(),'user':request.user})
	elif request.method=="POST":
 		u=request.POST["email"]
 		p=request.POST["password"]
 		print u,p
 		user = authenticate(username=u, password=p)
 		
 		if user is not None:
 			if user.is_active:
 				
 				auth_login(request,user)
 				print "logged in"
 				return redirect('/home/')
 			else:
 				print "error"
 				return render(request,'login_faculty.html',{'e':"User not active"})
 		else:
 			print "Invalid login"
 			return render(request,'login_faculty.html',{'e':"Username and password does not match"})

@login_required(login_url='/home/')
def profile_faculty(request):
 		try:
	 		db = MySQLdb.connect("127.0.0.1","root","admin","school2")
			c = db.cursor()
			user_type=request.user.last_name
			email=request.user.username
			print user_type,email
			if(request.user.last_name=="faculty"):
				sql = "SELECT * FROM  faculty where email='%s'" % email	
				#sql2= "SELECT course.name FROM  course,student,class_going_on where student.class_id=class_going_on.class_id and course.course_id=class_going_on.course_id and student.student_id=%d" % (student_id)	
			c.execute(sql)
			rows=c.fetchone()
			col=['faculty_id','name','email','phone']
			print type(col)
			a=[]
			b=[]
			for i in range(len(col)):
				b=[]
				b.append(col[i])
				b.append(rows[i])
				a.append(b)

			user=request.user
	                context={ 'col':col,'rows':a,'user':user,'flag': request.user.is_authenticated()}
	                return render(request,'profile_faculty.html',context)
		except Exception as e:
			print e
			print "hello"
			context={'e':e[1],'user':user,'flag': request.user.is_authenticated()}
			return render(request,'profile_faculty.html',context)
		finally:
			db.close()

@login_required(login_url='/home/')
def update_FacultyProfile(request):
	if request.method=="POST" and request.user.last_name=="faculty":
		#email=request.POST["email"]
		phone=int(request.POST["phone"])
		try:
	 		db = MySQLdb.connect("127.0.0.1","root","admin","school2")
			c = db.cursor()
			user_type=request.user.last_name
			email=request.user.username
			print user_type,email
			sql="UPDATE faculty set phone=%d where email='%s'" % (phone,email)
	                c.execute(sql)
	                db.commit()
			post="Profile updated successfully"
			context = {'post': post ,'flag': request.user.is_authenticated(),'user':request.user}
			return render(request,'head2.html',context)
	                print "done"
		except Exception as e:
			print e
			context = {'e': e ,'flag': request.user.is_authenticated(),'user':request.user}
			return render(request,'head2.html',context)
			print "hello"
		finally:
			db.close()
		return redirect('/home/')

	else:
		print "Error"
		e="Only faculties have access to it"
		context = {'e': e ,'flag': request.user.is_authenticated(),'user':request.user}
		return render(request,'head2.html',context)

@login_required(login_url='/home/')
def notice_faculty(request):
        if request.user.last_name!="faculty":
		e="Only faculties have access to it"
		return render(request,'head2.html',{'e':e,'flag': request.user.is_authenticated(),'user':request.user})
	if request.method=="GET":
		print "e"
		return render(request,'notice_faculty.html',{'flag': request.user.is_authenticated(),'user':request.user})
	elif request.method=="POST":		

		class_id=request.POST["class_id"]
		info=request.POST["info"]

		user_type=request.user.last_name
		email=request.user.username
	        if(user_type=="faculty"):
	                try:
	                        db = MySQLdb.connect("127.0.0.1","root","admin","school2")
	  	                c = db.cursor()
			        print user_type
	 		        sql2="SELECT faculty_id FROM  faculty where email='%s'" % email
	  		        c.execute(sql2)
	  		        faculty_id=c.fetchone()
	  		        sql="INSERT INTO notice(info,class_id,faculty_id) values('%s',%d,%d)" % (info,int(class_id),int(faculty_id[0]))
	  		        c.execute(sql)
	 		        db.commit()	
	 		        print "done"
	 		        post="Notice Posted"
	 		        return render(request,'notice_faculty.html',{'post':post,'flag': request.user.is_authenticated(),'user':request.user})
	                except Exception as e:
	                        print e
	                        return render(request,'notice_faculty.html',{'e':e[1],'flag': request.user.is_authenticated(),'user':request.user})

@login_required(login_url='/home/')
def marks_faculty(request):
        if request.user.last_name!="faculty":
		e="Only faculties have access to it"
		return render(request,'head2.html',{'e':e,'flag': request.user.is_authenticated(),'user':request.user})
	db = MySQLdb.connect("127.0.0.1","root","admin","school2")
	c = db.cursor()
	sql6="SELECT DISTINCT course.name FROM  course,faculty,class_going_on where faculty.faculty_id=class_going_on.faculty_id and course.course_id=class_going_on.course_id and faculty.email='%s'"%(request.user.username)
	c.execute(sql6)
	courses=c.fetchall()
	v=len(courses)>0
	if request.method=="GET":
		return render(request,'marks_faculty.html',{'flag': request.user.is_authenticated(),'user':request.user,'courses':courses,'v':v})
	elif request.method=="POST":
		student_id=request.POST["student_id"]
		exam_type=request.POST["exam_type"]
		email=request.user.username
		marks=request.POST["marks"]
		course=request.POST["course"]
		try:
			db = MySQLdb.connect("127.0.0.1","root","admin","school2")
			c = db.cursor()
			sql1="select class_going_on.class_going_on_id from class_going_on,student,faculty,course where class_going_on.course_id=course.course_id and course.name='%s' and student.class_id=class_going_on.class_id and student.student_id=%d and faculty.email='%s' and class_going_on.exam_type='%s'"%(course,int(student_id),email,exam_type)
			c.execute(sql1)
			class_going_on_id=c.fetchone()
			print class_going_on_id
			sql2="INSERT INTO mark(class_going_on_id,self_mark,exam_type,student_id) values(%d,%d,'%s',%d)"%(int(class_going_on_id[0]),int(marks),exam_type,int(student_id))
			print sql2
			c.execute(sql2)
			db.commit()
			post=marks+" are added to student with student_id "+student_id+" in exam "+exam_type
			return render(request,'marks_faculty.html',{'post':post,'flag': request.user.is_authenticated(),'user':request.user,'courses':courses,'v':v})
		except Exception as e:
			print e
			return render(request,'marks_faculty.html',{'e':e,'flag': request.user.is_authenticated(),'user':request.user,'courses':courses,'v':v})

@login_required(login_url='/home/')
def assignment_faculty(request):
        if request.user.last_name!="faculty":
		e="Only faculties have acces to it"
		return render(request,'head2.html',{'e':e,'flag': request.user.is_authenticated(),'user':request.user})
	if request.method=="GET":
		return render(request,'assignment_faculty.html',{'flag': request.user.is_authenticated(),'user':request.user})
	elif request.method=="POST":
	        request.user.password="123"		

		class_id=request.POST["class_id"]
		assignment=request.POST.get('assignment',False)
		print assignment

		user_type=request.user.last_name
		email=request.user.username
	        if(user_type=="faculty"):
	                try:
	                        db = MySQLdb.connect("127.0.0.1","root","admin","school2")
	  	                c = db.cursor()
			        print user_type
	 		        sql2="SELECT faculty_id FROM  faculty where email='%s'" % email
	  		        c.execute(sql2)
	  		        faculty_id=c.fetchone()
	  		        sql="INSERT INTO notice(info,class_id,faculty_id) values('%s',%d,%d)" % (assignment,int(class_id),int(faculty_id[0]))
	  		        c.execute(sql)
	 		        db.commit()	
	 		        print "done"
	 		        post="Assignment is successfully sent to the students"
	 		        return render(request,'assignment_faculty.html',{'post':post,'flag': request.user.is_authenticated(),'user':request.user})
	                except Exception as e:
	                        print e
	                        return render(request,'assignment_faculty.html',{'e':e[1],'flag': request.user.is_authenticated(),'user':request.user})



