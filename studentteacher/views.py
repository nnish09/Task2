from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.contrib.auth import login, authenticate,logout,update_session_auth_hash
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from studentteacher.models import User,AssignRequest,Assignment,Submission,Review,Message
from .forms import SignUpForm,SetPasswordForm,LoginForm,UpdateProfile,SignUpForm1,AssignmentForm,RequestForm,SubmitAssignmentForm,ReviewAssignmentForm,MessageForm
import json
from django.urls import reverse_lazy
from django.views import generic
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from friendship.exceptions import AlreadyExistsError
from friendship.models import Friend,FriendshipRequest
from django.conf import settings
from friendship.exceptions import AlreadyExistsError,AlreadyFriendsError
from django.views import View
from django.db.models import Q



user_model = User






def base(request):
    return render(request, 'base.html')

def home(request):
    return render(request, 'home.html')


def account_activated(request):
    return render(request, 'account_activated.html')

def passwordsetdone(request):
    return render(request, 'passwordsetdone.html')



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # print(form.is_valid())
        if form.is_valid():
            user= form.save(commit=False)
            # user.refresh_from_db()  # load the profile instance created by the signal
            user.phone_no = form.cleaned_data.get('phone_no')
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)) ,
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
          
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:      
        form = SignUpForm()
        
    return render(request, 'registration/signup.html', {'form': form})



def signup1(request):
    if request.method == 'POST':
        form = SignUpForm1(request.POST)
        # print(form.is_valid())
        if form.is_valid():
            user= form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)) ,
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
          
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return redirect('student_added')
    else:      
        form = SignUpForm1()
        
    return render(request, 'registration/signup1.html', {'form': form})





def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        return HttpResponseRedirect(reverse('setpassword',args=(uid,)))
    else:
        return HttpResponse('Activation link is expired!')

def setpassword(request,uid):
    if request.method=='POST':
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=uid)
            password=request.POST.get('password')
            password = form.cleaned_data['password']
            confirm_password=request.POST.get('confirm_password')
            confirm_password = form.cleaned_data['confirm_password']
         
            # print(password)
            # a=User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            # print(user.password)
            # login(request, user)
            return redirect('passwordsetdone')

            
    else:
        form = SetPasswordForm()

    return render(request,"passwordset.html",{'form':form})


def login_user(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username=username, password=password)          
            if user is not None:
                if user.is_active:
                    login(request, user)                                                            
                    return redirect('dashboard')                  
    else:
        login_form = LoginForm()
    return render(request, 'registration/login.html', {'login_form': login_form,})




@login_required
def dashboard(request):
    if request.user.role is 1: 
        return render(request, 'student_dashboard.html')
    elif request.user.role is 2:
        return render(request, 'teacher_dashboard.html')




@login_required
def user_profile(request):
    user=request.user
    users = User.objects.all()
    if request.user.role is 1: 
        return render(request, 'student_profile.html', {"users":users})
    elif request.user.role is 2:
        return render(request, 'profile.html', {"users":users})



# @login_required
# def get_user_profile(request):
#     user=request.user
#     users = User.objects.all()
#     return render(request, 'profile.html', {"users":users})

# @login_required
# def get_student_profile(request):
#     user=request.user
#     users = User.objects.all()
#     return render(request, 'student_profile.html', {"users":users})



@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UpdateProfile(request.POST, request.FILES , instance=request.user)
        
        if (user_form.is_valid()):
           
            user_form.save()                      
            return HttpResponseRedirect(reverse('user_profile'))
        
    else:
        user_form = UpdateProfile(instance=request.user)
    if request.user.role is 2: 
        return render(request, 'registration/update_profile.html', {'user_form': user_form })
    elif request.user.role is 1:
        return render(request, 'registration/update_student_profile.html', {'user_form': user_form })

    
# @login_required
# def update_profile(request):
#     if request.method == 'POST':
#         user_form = UpdateProfile(request.POST, request.FILES , instance=request.user)
        
#         if (user_form.is_valid()):
           
#             user_form.save()            
#             return HttpResponseRedirect(reverse('profile'))
        
#     else:
#         user_form = UpdateProfile(instance=request.user)
#     return render(request, 'registration/update_profile.html', {
#         'user_form': user_form
#     })


# @login_required
# def update_student_profile(request):
#     if request.method == 'POST':
#         user_form = UpdateProfile(request.POST, request.FILES , instance=request.user)
        
#         if (user_form.is_valid()):
           
#             user_form.save()            
#             return HttpResponseRedirect(reverse('get_student_profile'))
        
#     else:
#         user_form = UpdateProfile(instance=request.user)
#     return render(request, 'registration/update_student_profile.html', {
#         'user_form': user_form
#     })


@login_required
def change_password_done(request):
    return render(request, 'registration/password_changed.html')

# @login_required
# def student_dashboard(request):
#     return render(request, 'student_dashboard.html')

# @login_required
# def teacher_dashboard(request):
#     return render(request, 'teacher_dashboard.html')


@login_required
def student_added(request):
    return render(request, 'student_added.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('passwordchanged')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form})



@login_required
def get_students(request):
    if request.user.role is 2: 
        stud = User.objects.filter(role=1)
        return render(request, 'students.html', {"stud":stud})
    else:
        return HttpResponse('you are not authenticated to access this page')


# @login_required
# def assignment_form(request):
#     return render(request, 'assignment_form.html')


@login_required
def assignment(request,stu_id):
    if request.user.role is 2: 
        if request.method == 'POST':
            assign_form = AssignmentForm(request.POST, request.FILES)
            
            if  assign_form.is_valid():
                assign=assign_form.save() 
                assign.student=User.objects.get(pk=stu_id)  
                assign.teacher=request.user   
                assign.save() 
                return HttpResponseRedirect(reverse('assign_added'))
        else:
            assign_form = AssignmentForm()
        return render(request, 'assignment_form.html', {'assign_form': assign_form })
    else:
        return HttpResponse('you are not authenticated to access this page')

@login_required
def submit_assignment(request,stu_id):
    if request.user.role is 1:
        if request.method == 'POST':
            submit_assign_form = SubmitAssignmentForm(request.POST, request.FILES) 
            if  submit_assign_form.is_valid():                  
                submit_assign=submit_assign_form.save() 
                submit_assign.sub_student=request.user 
                submit_assign.sub_teacher=User.objects.get(pk=stu_id) 
                submit_assign.save()  
                return HttpResponseRedirect(reverse('assign_submitted'))
            
        else:
            submit_assign_form = SubmitAssignmentForm()
        return render(request, 'submit_assignment.html', {'submit_assign_form': submit_assign_form })

    else:
        return HttpResponse('you are not authenticated to access this page')


@login_required
def assign_added(request):
    return render(request, 'assign_added.html')


@login_required
def teacher_base(request):
    return render(request, 'teacher_base.html')

@login_required
def student_base(request):
    return render(request, 'student_base.html')


@login_required
def get_teachers(request):
    if request.user.role is 1:
        teach = User.objects.filter(role=2)
        return render(request, 'teachers.html', {"teach":teach})
    else:
        return HttpResponse('you are not authenticated to access this page')



@login_required
def friendship_add_friend(request, teacher_id):
    if request.user.role is 1:
        ctx = {"teacher_id": teacher_id}
        if request.method == "POST":
            to_user = User.objects.get(pk=teacher_id)
            from_user = request.user
            try:
                Friend.objects.add_friend(from_user, to_user)
            except AlreadyFriendsError as e:
                ctx["errors"] = ["%s" % e]
            except AlreadyExistsError as e:
                ctx["errors"] = ["%s" % e]
            else:
                return redirect("user_profile")
        return render(request, "friendship/friend/add.html", ctx)
    else:
        return HttpResponse('you are not authenticated to access this page')


@login_required
def friendship_request_list(request):
    if request.user.role is 2:
        friendship_requests = Friend.objects.requests(request.user)
        # This shows all friendship requests in the database
        # friendship_requests = FriendshipRequest.objects.filter(rejected__isnull=True)
        return render(request, "friendship/friend/requests_list.html", {"requests": friendship_requests})
    else:
        return HttpResponse('you are not authenticated to access this page')



@login_required
def friendship_requests_detail(request, friendship_request_id):
    if request.user.role is 2:
        f_request = get_object_or_404(FriendshipRequest, id=friendship_request_id)

        return render(request, "friendship/friend/request.html", {"friendship_request": f_request})

    else:
        return HttpResponse('you are not authenticated to access this page')



get_friendship_context_object_name = lambda: getattr(
    settings, "FRIENDSHIP_CONTEXT_OBJECT_NAME", "user"
)
get_friendship_context_object_list_name = lambda: getattr(
    settings, "FRIENDSHIP_CONTEXT_OBJECT_LIST_NAME", "users"
)

@login_required
def view_friends(request, teacher_id):
    if request.user.role is 2:
        user = get_object_or_404(user_model, pk=teacher_id)
        friends = Friend.objects.friends(user)
        return render(request, "friendship/friend/user_list.html", {
            get_friendship_context_object_name(): user,
            'friendship_context_object_name': get_friendship_context_object_name(),
            'friends': friends,
        })
    else:
        return HttpResponse('you are not authenticated to access this page')


@login_required
def view_student_friends(request, teacher_id):
    if request.user.role is 1:
        user = get_object_or_404(user_model, pk=teacher_id)
        friends = Friend.objects.friends(user)
        return render(request, "friendship/friend/student_friends.html", {
        get_friendship_context_object_name(): user,
        'friendship_context_object_name': get_friendship_context_object_name(),
        'friends': friends,
        })
    else:
        return HttpResponse('you are not authenticated to access this page')



@login_required
def friendship_accept(request, friendship_request_id):
    if request.user.role is 2:
        if request.method == "POST":
            f_request = get_object_or_404(
                request.user.friendship_requests_received, id=friendship_request_id
            )
            f_request.accept()

            return redirect("viewfriends", username=request.user.username)

        return redirect(
            "requests_detail", friendship_request_id=friendship_request_id
        )
    else:
        return HttpResponse('you are not authenticated to access this page')


@login_required
def friendship_reject(request, friendship_request_id):
    if request.user.role is 2:
        if request.method == "POST":
            f_request = get_object_or_404(
                request.user.friendship_requests_received, id=friendship_request_id
            )
            f_request.reject()
            return redirect("request_list")

        return redirect(
            "requests_detail", friendship_request_id=friendship_request_id
        )
    else:
        return HttpResponse('you are not authenticated to access this page')


@login_required
def request_assign(request,tea_id):
    if request.user.role is 1:
        if request.method == 'POST':
            request_form = RequestForm(request.POST,initial={'requested': True})
            if  request_form.is_valid():
                print(request_form.is_valid())            
                request_assign=request_form.save() 
                request_assign.req_teacher=User.objects.get(pk=tea_id)  
                request_assign.req_student=request.user   
                request_assign.save()  
                return HttpResponseRedirect(reverse('assign_requested'))
            
        else:
            request_form = RequestForm()
        return render(request, 'student_friends.html', {
            'request_form': request_form
        })
    else:
        return HttpResponse('you are not authenticated to access this page')


@login_required
def get_assign_requests(request):
    if request.user.role is 2:
        print(request.user)
        assign_req = AssignRequest.objects.filter(req_teacher=request.user)
        return render(request, 'req_assign.html', {"assign_req":assign_req})
    else:
        return HttpResponse('you are not authenticated to access this page')


@login_required
def assign_requested(request):
    return render(request, 'assignment_requested.html')


@login_required
def get_assignments(request):
    if request.user.role is 1:
        getassignments = Assignment.objects.filter(student=request.user)
        return render(request, 'get_assignment.html', {"getassignments":getassignments})
    else:
        return HttpResponse('you are not authenticated to access this page')


@login_required
def assign_submitted(request):
    if request.user.role is 1:
        return render(request, 'assignment_submitted.html')
    else:
        return HttpResponse('you are not authenticated to access this page')



# 
@login_required
def get_submitted_assignments(request):
    if request.user.role is 2:
        get_submit_assignments = Submission.objects.filter(sub_teacher=request.user)
        return render(request, 'get_submitted_assignments.html', {"get_submit_assignments":get_submit_assignments})
    else:
        return HttpResponse('you are not authenticated to access this page')


@login_required
def review_assignment(request,stud_id):
    if request.user.role is 2:
        if request.method == 'POST':
            review_assign_form = ReviewAssignmentForm(request.POST, request.FILES)   
            if  review_assign_form.is_valid():
                review_assign=review_assign_form.save() 
                review_assign.review_student=User.objects.get(pk=stud_id)  
                review_assign.review_teacher=request.user
                review_assign.save()  
                return HttpResponseRedirect(reverse('assign_reviewed'))
            
        else:
            review_assign_form = ReviewAssignmentForm()
        return render(request, 'review_assignment.html', {
            'review_assign_form': review_assign_form
        })
    else:
        return HttpResponse('you are not authenticated to access this page')


@login_required
def assign_reviewed(request):
    if request.user.role is 2:
        return render(request, 'assign_reviewed.html')
    else:
        return HttpResponse('you are not authenticated to access this page')


@login_required
def get_reviews(request):
    if request.user.role is 1:
        get_review = Review.objects.filter(review_student=request.user)
        return render(request, 'get_reviews.html', {"get_review":get_review})
    else:
        return HttpResponse('you are not authenticated to access this page')


# def get_users(request):
#     users = User.objects.all()
#     return render(request, "users.html", {'users': users})


# def get_users_student(request):
#     users = User.objects.all()
#     return render(request, "student_users.html", {'users': users})



@login_required
def message_post(request,user_id):
    if request.user.role is 2:
        if request.method == 'POST':
            msg_form = MessageForm(request.POST)
            
            if  msg_form.is_valid():
                message_form=msg_form.save() 
                message_form.to_user=User.objects.get(pk=user_id)  
                message_form.from_user=request.user   
                message_form.save()  
                return HttpResponseRedirect(reverse('message_post',args=(user_id,)))
            
        else:
            msg_form = MessageForm()
            query = Q(Q(from_user=request.user)&Q(to_user=user_id))|Q(Q(to_user=request.user)&Q(from_user=user_id))
            mess = Message.objects.filter(query)
        return render(request, 'messages.html', {
            'msg_form': msg_form,'mess':mess
        })

    else:
        return HttpResponse('you are not authenticated to access this page')


@login_required
def message_post_student(request,user_id):
    if request.user.role is 1:
        if request.method == 'POST':
            msg_form1 = MessageForm(request.POST)
            
            if  msg_form1.is_valid():
                message_form1=msg_form1.save() 
                message_form1.to_user=User.objects.get(pk=user_id)  
                message_form1.from_user=request.user   
                message_form1.save()  
                return HttpResponseRedirect(reverse('message_post_student',args=(user_id,)))
            
        else:
            msg_form1 = MessageForm()
            query = Q(Q(from_user=request.user)&Q(to_user=user_id))|Q(Q(to_user=request.user)&Q(from_user=user_id))
            mess1 = Message.objects.filter(query)
        return render(request, 'mess_form.html', {
            'msg_form1': msg_form1,'mess1':mess1
        })

    else:
        return HttpResponse('you are not authenticated to access this page')




def unauth_log(request):
    return render(request, 'unauth.html')

