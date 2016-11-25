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

# db = MySQLdb.connect("127.0.0.1","root","admin","myproject")
# c = db.cursor()
# sql = "CREATE TABLE YO (no int )"
# c.execute(sql)
# db.commit()
# #row = c.fetchall()
#print(row)



# Create your views here.

def home(request):
	user=request.user
	student=False
	faculty=False
	if(request.user.is_authenticated()):
		if(request.user.last_name=="student"):
			student=True
		if(request.user.last_name=="faculty"):
			faculty=True	
	context={user:'user','flag': request.user.is_authenticated(),'student':student,'faculty':faculty}
	print student
	return render(request,'home.html',context)

@login_required(login_url='/home/')
def change_pwd(request):
	if request.method=="GET":
		print "e"
		return render(request,'change_pwd.html')
	elif request.method=="POST":
 		# old=str(request.POST["old"])
 		new=str(request.POST["new"])
 		print new
 		username=request.user.username
 		u = User.objects.get(username__exact=username)
 		print u
 		u.set_password(new)
 		u.save()
 		print request.user.is_authenticated
 		return render(request,'home.html',{'post':"Password changed successfully"})


def register_student(request):
	if request.method=="GET":
		return render(request,'register_student.html')
	elif request.method=="POST":
 		name=str(request.POST["name"])
 		user_type="student"
 		email=request.POST["email"]
 		username=int(request.POST["username"])
 		password=request.POST["password"]
 		phone=int(request.POST["phone"])
 		class_id=int(request.POST["class"])
 		print "user saved"
 		try:
	 		user = User.objects.create_user(username,email,password)
	 		user.first_name = name
	 		user.last_name = user_type
	 		user.save()
	 		db = MySQLdb.connect("127.0.0.1","root","admin","school2")
			c = db.cursor()
			sql = "INSERT INTO student values (%d,'%s','%s',%d,%d)" % (username,name,email,phone,class_id)
			print sql
			c.execute(sql)
			db.commit()
			u=username
			p=password
			auth_login(request,authenticate(username=u, password=p))
			return redirect('/login_student/')
		except Exception as e:
			print e
			context={ 'e':e[1]}
			return render(request,'register_student.html',context)
		# finally:
		# 	db.close()

        
def login_student(request):
	if request.method=="GET":
		return render(request,'login_student.html')
	elif request.method=="POST":
 		u=request.POST["username"]
 		p=request.POST["password"]
 		user = authenticate(username=u, password=p)
 		
 		if user is not None:
 			if user.is_active:
 				
 				auth_login(request,user)
 				print "logged in"
 				return redirect('/home/')
 			else:
 				print "error"
 		else:
 			print "Invalid login"
 			return render(request,'login_student.html',{'e':"Username and password does not match"})

@login_required(login_url='/home/')
def logout_view(request):
	logout(request)
	print "logged out"
	return redirect('/home/')


@login_required(login_url='/home/')
def profile_student(request):
    		if request.user.last_name!="student":
	    		e="Not logged in as a student"
	    		return render(request,'head.html',{'e':e,'flag': request.user.is_authenticated(),'user':request.user})
 		try:
	 		db = MySQLdb.connect("127.0.0.1","root","admin","school2")
			c = db.cursor()
			user_type=request.user.last_name
			student_id=int(request.user.username)
			print user_type,student_id
			if(request.user.last_name=="student"):
				sql = "SELECT * FROM  student where student_id='%s'" % student_id	
				sql2= "SELECT DISTINCT course.name FROM  course,student,class_going_on where student.class_id=class_going_on.class_id and course.course_id=class_going_on.course_id and student.student_id=%d" % (student_id)	
			c.execute(sql)
			rows=c.fetchone()
			c.execute(sql2)
			courses=c.fetchall()

			col=['student_id','name','email','phone','class_id']
			print type(col)
			a=[]
			b=[]
			for i in range(len(col)):
				b=[]
				b.append(col[i])
				b.append(rows[i])
				a.append(b)

			user=request.user
	                context={ 'col':col,'rows':a,'user':user,'flag': request.user.is_authenticated(),'courses':courses}
	                return render(request,'profile_student.html',context)
		except Exception as e:
			print e
			print "hello"
			context={'e':e[1]}
			return render(request,'profile_student.html',context)
		finally:
			db.close()

@login_required(login_url='/home/')
def notice_student(request):
	user=request.user
	user_type=request.user.last_name
	if(user_type=="student"):
 		try:
	 		db = MySQLdb.connect("127.0.0.1","root","admin","school2")
			c = db.cursor()
			user_type=request.user.last_name
			student_id=request.user.username
			print user_type,student_id
			try:
				sql1="SELECT class_id FROM  student where student_id='%s'" % student_id
				c.execute(sql1)
				class_id=c.fetchall()
				print repr(class_id[0])
			except Exception as e:
				print e
			sql="SELECT notice_id,info,faculty.name FROM  notice,faculty where class_id='%s' and faculty.faculty_id=notice.faculty_id" % class_id[0]
			print sql
			c.execute(sql)		
			notices=c.fetchall()
			print notices,"hello"
			db.commit()

			#return redirect('/login_student/')
		except Exception as e:
			print e
			print "hello"
			return render(request,'head.html',{'flag': request.user.is_authenticated(),'user':request.user,'e':e})
		finally:
			db.close()
		context = {'notices': notices,'flag': request.user.is_authenticated(),'user':user}
		return render(request,'notice_board.html',context)
	else:
		e="Not logged in as a student"
		return render(request,'head.html',{'flag': request.user.is_authenticated(),'user':request.user,'e':e})

@login_required(login_url='/home/')
def update_StudentProfile(request):
	if request.method=="POST":
		email=request.POST["email"]
		phone=int(request.POST["phone"])
		try:
	 		db = MySQLdb.connect("127.0.0.1","root","admin","school2")
			c = db.cursor()
			user_type=request.user.last_name
			student_id=int(request.user.username)
			print user_type,student_id
			sql="UPDATE student set email='%s',phone=%d where student_id=%d" % (email,phone,student_id)
	                c.execute(sql)
	                db.commit()
	                print "done"
			post="Profile updated successfully"
			print post
			context = {'post': post ,'flag': request.user.is_authenticated(),'user':request.user}
			return render(request,'head.html',context)
		except Exception as e:
			print e
			context = {'e': e ,'flag': request.user.is_authenticated(),'user':request.user}
			return render(request,'head.html',context)
		finally:
			db.close()
		return redirect('/home/')

	else:
		print "Error"

@login_required(login_url='/home/')
def feedback_student(request):
        if request.user.last_name!="student":
	    	e="Not logged in as a student"
	    	return render(request,'head.html',{'e':e,'flag': request.user.is_authenticated(),'user':request.user})
        student_id=int(request.user.username)
        db = MySQLdb.connect("127.0.0.1","root","admin","school2")
	c = db.cursor()
        sql8= "SELECT DISTINCT course.name FROM  course,student,class_going_on where student.class_id=class_going_on.class_id and course.course_id=class_going_on.course_id and student.student_id=%d" % (student_id)
        c.execute(sql8)
        courses=c.fetchall()
       
	sql7="SELECT DISTINCT faculty.name FROM faculty,student,class_going_on where student.student_id=%d and student.class_id=class_going_on.class_id and class_going_on.faculty_id=faculty.faculty_id"% (student_id)
        c.execute(sql7)
        print sql7
        faculties=c.fetchall()
        print faculties
        v=(len(faculties)>0 and len(courses)>0)
	if request.method=="GET":

		context={'user':request.user,'flag': request.user.is_authenticated(),'courses':courses,'faculties':faculties,'v':v}
	        return render(request,'feedback.html',context)
	elif request.method=="POST":
		feedback=request.POST["feedback"]
		faculty=request.POST["faculty"]
                print faculty
		course=request.POST["course"]
		student_id=request.user.username
		user_type=request.user.last_name
		student_id=int(student_id)
		user=request.user
		print type(student_id)
		print user_type
		if(user_type=="student"):

	 		try:
				sql1="SELECT class_going_on_id  FROM  class_going_on,student,course,faculty where student.class_id=class_going_on.class_id and course.course_id=class_going_on.course_id and faculty.faculty_id=class_going_on.faculty_id and faculty.name='%s' and student.student_id=%d and course.name='%s'" % (faculty,student_id,course)
				c.execute(sql1)
				print sql1

				class_going_id = c.fetchone()
				print class_going_id

				sql2="INSERT INTO feedback(class_going_on_id,student_id,feedback) values(%d,%d,'%s')"%(class_going_id[0],student_id,feedback)
				c.execute(sql2)
				print "done"
				
				db.commit()
				print "done"
				a="Feedback submitted successfully"
				context={user:'user','flag': request.user.is_authenticated(),'a':a,'courses':courses,'faculties':faculties,'v':v}
				return render(request,'feedback.html',context)
				

			except Exception as e:
				print e
				context={user:'user','flag': request.user.is_authenticated(),'e':e}
				return render(request,'feedback.html',context)
			finally:
				db.close()

		else:
			print "Error"


@login_required(login_url='/home/')
def marks_subject(request):
    if request.user.last_name!="student":
	    	e="Not logged in as a student"
	    	return render(request,'head.html',{'e':e,'flag': request.user.is_authenticated(),'user':request.user})
    student_id=int(request.user.username)
    db = MySQLdb.connect("127.0.0.1","root","admin","school2")
    c = db.cursor()
    sql8= "SELECT course.name FROM  course,student,class_going_on where student.class_id=class_going_on.class_id and course.course_id=class_going_on.course_id and student.student_id=%d" % (student_id)
    c.execute(sql8)
    courses=c.fetchall()
    if (request.method=="POST"):
		course=request.POST.get("course1", False)
		user=request.user
		user_type=request.user.last_name
		student_id=request.user.username
		student_id=int(student_id)
		print type(student_id)
		if(user_type=="student"):
			db = MySQLdb.connect("127.0.0.1","root","admin","school2")
			c = db.cursor()
	 		try:
	                        sql="SELECT mark.self_mark,mark.exam_type FROM  mark,student,class_going_on,course where student.student_id=%d and    student.class_id=class_going_on.class_id and course.course_id=class_going_on.course_id and course.name='%s' and class_going_on.exam_type=mark.exam_type and mark.student_id=student.student_id "%(student_id,course)
				print sql
				c.execute(sql)
				marks=c.fetchall()
				print marks
				print marks
				print "done"
			        context = {'marks': marks,'flag': request.user.is_authenticated(),'user':user,'courses':courses,'course':course}
			        return render(request,'marks_student.html',context)

			except Exception as e:
				print e
				return render(request,'marks_student.html',{'e':e[1],'flag': request.user.is_authenticated(),'user':user,'courses':courses,'course':course})
			finally:
				db.close()

		else:
			e="Not logged in as a student"
			return render(request,'marks_student.html',{'e':e,'flag': request.user.is_authenticated(),'user':user})
			print "Error"

@login_required(login_url='/home/')
def marks_student(request):
    if request.user.last_name!="student":
	    	e="Not logged in as a student"
	    	return render(request,'head.html',{'e':e,'flag': request.user.is_authenticated(),'user':request.user})
    student_id=int(request.user.username)
    db = MySQLdb.connect("127.0.0.1","root","admin","school2")
    c = db.cursor()
    sql8= "SELECT course.name FROM  course,student,class_going_on where student.class_id=class_going_on.class_id and course.course_id=class_going_on.course_id and student.student_id=%d" % (student_id)
    c.execute(sql8)
    courses=c.fetchall()
    if request.method=="GET":
		return render(request,'getMarks.html',{'flag': request.user.is_authenticated(),'user':request.user,'courses':courses})

    elif request.method=="POST":

		course=request.POST.get('course', False)
		user=request.user
		exam_type=request.POST["exam_type"]
		user_type=request.user.last_name
		student_id=request.user.username
		student_id=int(student_id)
		print type(student_id)
		if(user_type=="student"):
			db = MySQLdb.connect("127.0.0.1","root","admin","school2")
			c = db.cursor()
	 		try:
	                        sql="SELECT mark.self_mark FROM  mark,student,class_going_on,course where student.student_id=%d and    student.class_id=class_going_on.class_id and course.course_id=class_going_on.course_id and course.name='%s' and class_going_on.exam_type=mark.exam_type and mark.student_id=student.student_id and mark.exam_type ='%s'"%(student_id,course,exam_type)
				c.execute(sql)
				print sql
				marks=c.fetchall()
				print marks
				print "done"
			        context = {'marks': marks,'flag': request.user.is_authenticated(),'user':user,'course':course,'exam_type':exam_type,'courses':courses}
			        return render(request,'marks_student.html',context)

			except Exception as e:
				print e
				return render(request,'marks_student.html',{'e':e,'flag': request.user.is_authenticated(),'user':user,'courses':courses})
			finally:
				db.close()

		else:
			e="Not logged in as a student"
			return render(request,'marks_student.html',{'e':e,'flag': request.user.is_authenticated(),'user':user,'course':course,'courses':courses})
			print "Error"


@login_required(login_url='/home/')
def assignment_submit(request):
	if request.user.last_name!="student":
	    	e="Not logged in as a student"
	    	return render(request,'head.html',{'e':e,'flag': request.user.is_authenticated(),'user':request.user})
	student_id=int(request.user.username)
	db = MySQLdb.connect("127.0.0.1","root","admin","school2")
	c = db.cursor()
	sql7="SELECT DISTINCT faculty.name FROM faculty,student,class_going_on where student.student_id=%d and student.class_id=class_going_on.class_id and class_going_on.faculty_id=faculty.faculty_id"% (student_id)
	c.execute(sql7)
	faculties=c.fetchall()
	v=len(faculties)>0
	
	if(request.method=="GET"):
		return render(request,'assignment_submit.html',{'flag': request.user.is_authenticated(),'user':request.user,'faculties':faculties,'v':v})

	assignment=request.POST["assignment"]
	faculty=request.POST["faculty"]
	user_type=request.user.last_name
	student_id=request.user.username
	student_id=int(student_id)
	print student_id,faculty,user_type,assignment
	if(user_type=="student"):
		
		
		d = db.cursor()
 		try:
			sql2="SELECT email FROM  student where student_id=%d" % student_id
			c.execute(sql2)
			print sql2
			smail=c.fetchone()

			sql3="SELECT email FROM  faculty where name='%s'" % faculty
			c.execute(sql3)
			email=c.fetchone()
			print email
			from_email = settings.EMAIL_HOST_USER
			send_mail("assignment",assignment,from_email,[email[0]], fail_silently=False)
			#mail assignment to email
			db.commit()
			post="Submitted successfully"
			return render(request,'assignment_submit.html',{'flag': request.user.is_authenticated(),'user':request.user,'faculties':faculties,'v':v,'post':post})


		except Exception as e:
			
			return render(request,'assignment_submit.html',{'flag': request.user.is_authenticated(),'user':request.user,'faculties':faculties,'v':v,'e':e})
		finally:
			db.close()

	else:
		print "Error"


@login_required(login_url='/home/')
def timetable(request):
	        if request.user.last_name!="student":
	                e="Not logged in as a student"
	                return render(request,'timetable.html',{'e':e,'flag': request.user.is_authenticated(),'user':request.user})
		db = MySQLdb.connect("127.0.0.1","root","admin","school2")
		c = db.cursor()
		dic=["monday","tuesday","wednesday","thursday","friday","saturday"]
		student_id=int(request.user.username)
		tt=[]
 		try:
 			for i in dic:
				sql="select period,day,course.name from time_slot,class_going_on,course where time_slot.class_going_on_id in (select class_going_on.class_going_on_id from class_going_on,student where student.student_id=%d and student.class_id=class_going_on.class_id) and class_going_on.class_going_on_id=time_slot.class_going_on_id and course.course_id=class_going_on.course_id and day='%s'" % (student_id,i)
				c.execute(sql)
				t=c.fetchall()
				tt.append(t)
			print tt
			db.commit()
			print "done"
			

		except Exception as e:
			print e
			return render(request,'timetable.html',{'e':e[1],'flag': request.user.is_authenticated(),'user':request.user})
		finally:
			db.close()
		user=request.user
		context={'tts':tt,'flag': request.user.is_authenticated(),'user':request.user}
		return render(request,'timetable.html',context)


































# select period,day,course.name from time_slot,class_going_on,course where time_slot.class_going_on_id in (select class_going_on.class_going_on_id from class_going_on,student where student.student_id=1 and student.class_id=class_going_on.class_id) and class_going_on.class_going_on_id=time_slot.class_going_on_id and course.course_id=class_going_on.course_id and day="monday";

	





