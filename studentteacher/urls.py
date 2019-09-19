from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


urlpatterns=[
    path('',views.home,name='home'), 
    path('signup',views.signup,name='signup'),  
    path('signup1',views.signup1,name='signup1'),  
    path('base',views.base,name='base'), 
    path('teacher_base',views.teacher_base,name='teacher_base'), 
    path('student_base',views.student_base,name='student_base'), 
    path('student_added',views.student_added,name='student_added'), 
    path('get_students',views.get_students,name='get_students'), 
    path('get_teachers',views.get_teachers,name='get_teachers'), 
    path('login_user',views.login_user,name='login_user'), 
    path('dashboard',views.dashboard,name='dashboard'),

    # path('student_dashboard',views.student_dashboard,name='student_dashboard'),
    # path('teacher_dashboard',views.teacher_dashboard,name='teacher_dashboard'),
    path('account_activated',views.account_activated,name='account_activated'), 
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    path('setpassword/<int:uid>',views.setpassword,name='setpassword'),
    path('user_profile',views.user_profile,name='user_profile'),

    # path('profile',views.get_user_profile,name='profile'),
    # path('get_student_profile',views.get_student_profile,name='get_student_profile'),
    # path('update_student_profile',views.update_student_profile,name='update_student_profile'), 
    path('unauth_log',views.unauth_log,name='unauth_log'), 

    path('editprofile',views.update_profile,name='editprofile'), 
    path('passwordsetdone',views.passwordsetdone,name='passwordsetdone'),
    path('password/', views.change_password, name='change_password'),
    path('passwordchanged/', views.change_password_done, name='passwordchanged'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView, name='password_reset_complete'),
    # path('assignment_form',views.assignment_form,name='assignment_form'),
    path('assignment/<int:stu_id>',views.assignment,name='assignment'),
    path('assign_added',views.assign_added,name='assign_added'),
    path('request_teacher/<int:teacher_id>',views.friendship_add_friend,name='request_teacher'),
    path('request_list',views.friendship_request_list,name='request_list'),
    path('request_detail/<int:friendship_request_id>',views.friendship_requests_detail,name='request_detail'),
    path('friend_request_accept/<int:friendship_request_id>',views.friendship_accept,name='friend_request_accept'),
    path('friend_request_reject/<int:friendship_request_id>',views.friendship_reject,name='friend_request_reject'),
    path('viewfriends/<int:teacher_id>',views.view_friends,name='viewfriends'),
    path('view_studentfriends/<int:teacher_id>',views.view_student_friends,name='view_studentfriends'),
    path('request_assign/<int:tea_id>',views.request_assign,name='request_assign'),
    path('get_assign_requests',views.get_assign_requests,name='get_assign_requests'),
    path('assign_requested',views.assign_requested,name='assign_requested'),
    path('get_assignments',views.get_assignments,name='get_assignments'),
    path('submit_assignment/<int:stu_id>/',views.submit_assignment,name='submit_assignment'),
    path('assign_submitted',views.assign_submitted,name='assign_submitted'),
    path('get_submitted_assignments',views.get_submitted_assignments,name='get_submitted_assignments'),
    path('review_assignment/<int:stud_id>/',views.review_assignment,name='review_assignment'),
    path('assign_reviewed',views.assign_reviewed,name='assign_reviewed'),
    path('get_reviews',views.get_reviews,name='get_reviews'),

    path('message_post/<int:user_id>/',views.message_post,name='message_post'),
    path('message_post_student/<int:user_id>/',views.message_post_student,name='message_post_student'),

]
