"""school URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', 'student.views.home', name='home'),
    url(r'^home/$', 'student.views.home', name='home'),
    url(r'^principal_feedback/$', 'principal.views.principal_feedback', name='principal_feedback'),
    url(r'^marks_subject/$','student.views.marks_subject', name='marks_subject'),
    url(r'^timetable/$','student.views.timetable', name='timetable'),
    url(r'^update_StudentProfile/$','student.views.update_StudentProfile', name='update_StudentProfile'),
    url(r'^update_FacultyProfile/$','faculty.views.update_FacultyProfile', name='update_FacultyProfile'),
    url(r'^notice_faculty/$','faculty.views.notice_faculty', name='notice_faculty'),
    url(r'^profile_student/$','student.views.profile_student', name='profile_student'),
    url(r'^profile_faculty/$','faculty.views.profile_faculty', name='profile_faculty'),
    url(r'^marks_student/$','student.views.marks_student', name='marks_student'),
    url(r'^marks_faculty/$','faculty.views.marks_faculty', name='marks_faculty'),
    url(r'^feedback_student/$','student.views.feedback_student', name='feedback_student'),
    url(r'^notice_student/$','student.views.notice_student', name='notice_student'),
    url(r'^register_student/$','student.views.register_student', name='register_student'),
    url(r'^register_faculty/$','faculty.views.register_faculty', name='register_faculty'),
    url(r'^login_student/$','student.views.login_student', name='login_student'),
    url(r'^login_faculty/$','faculty.views.login_faculty', name='login_faculty'),
    url(r'^logout/$','student.views.logout_view', name='logout_view'),
    url(r'^faculty_class_course/$','faculty.views.faculty_class_course', name='faculty_class_course'),
    url(r'^faculty_class_course_time/$','faculty.views.faculty_class_course_time', name='faculty_class_course_time'),
    url(r'^assignment_faculty/$','faculty.views.assignment_faculty', name='assignment_faculty'),
    url(r'^change_pwd/$','student.views.change_pwd', name='change_pwd'),
    url(r'^principal/$','principal.views.principal', name='principal'),
    url(r'^class_insert/$','principal.views.class_insert', name='class_insert'),
    url(r'^class_going_on_insert/$','principal.views.class_going_on_insert', name='class_going_on'),
    url(r'^assignment_submit/$','student.views.assignment_submit', name='assignment_submit'),

    # url(r'^profile_student/$','student.views.profile_student', name='profile_student'),

    # url(r'^noticeboard/$','student.views.noticeboard', name='noticeboard'),

    # url(r'^profile_student/$','student.views.profile_student', name='profile_student'),
    # url(r'^login_student/$','student.views.login_student', name='login_student'),
    # url(r'^logout_student/$','student.views.logout_student', name='logout_student'),
]
