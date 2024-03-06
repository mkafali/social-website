from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from .forms import SignUpForm,UserProfileUpdateForm,ProfileEditForm, PasswordReset, ForgotMyPassword, PasswordMailCode, ComplainProfileForm, HaveProblemForm
from .models import Profile
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.contrib.auth.models import User
import random
import socialwebsite.settings 
from django.contrib.auth.decorators import login_required
from posts.models import Post
from django.http import HttpResponse
from notifications.models import MyFollowNotification



def home(request):
    if request.user.is_authenticated:
        profile, created = Profile.objects.get_or_create(user=request.user)
        user_follows = profile.follows.all()
        posts = []
        for each_user in user_follows:
            posts.extend(Post.objects.filter(user=each_user))
        
        posts = sorted(posts, key=lambda x: x.slug)
        return render(request, 'home.html', {'profile':profile,'posts':posts})
    return render(request, 'home.html', {})

def user_login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"You have been Logged In {user.username}")
            return redirect('home')
        else:
            messages.success(request, f"Username or Password is wrong")
            return render(request, 'user_login.html', {})

    return render(request, 'user_login.html', {})

@login_required
def log_out(request):
    logout(request)
    messages.success(request, "You have successfully log out")
    return redirect('home')

@login_required
def user_profile(request):
    posts = Post.objects.filter(user=request.user)
    profile = Profile.objects.get(user=request.user)
    return render(request, 'user_profile.html', {"profile":profile,"posts":posts})


def user_register(request):
    if request.method=='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            Profile.objects.create(user=user)
            messages.success(request, 'WELCOME')
            return redirect('home')
    else:
        form = SignUpForm()


    return render(request, 'register.html', {'form':form})

@login_required
def profile_edit(request):
    profile_instance = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile_instance)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = ProfileEditForm(instance=profile_instance)
    return render(request, 'profile_edit.html', {'form':form,'profile':profile_instance})
    
@login_required
def user_edit(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method=='POST':
        form = UserProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_edit')
    else:
        form = UserProfileUpdateForm(instance=request.user)

    return render(request, 'user_edit.html', {'form':form,'profile':profile})

@login_required 
def password_change(request):
    profile = Profile.objects.get(user=request.user)
    if request.method=='POST':
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password_change')
        else:
            messages.error(request, 'There was some mistakes')
            return redirect('password_change')
    else:
        form = PasswordChangeForm(request.user)
        
    return render(request, 'password_change.html', {'form':form, 'profile':profile})

@login_required
def password_reset(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = PasswordReset(request.POST)
        if form.is_valid():
            new_password1 = form.cleaned_data["new_password1"]
            new_password2 = form.cleaned_data["new_password2"]
            if new_password1==new_password2:
                request.user.set_password(new_password1)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Your password was successfully updated!')
            else:
                messages.error(request, 'Password confirmation is wrong.')
            return redirect('password_reset')
        else:
            messages.error(request, 'There were some mistakes in the form.')
    else:
        form = PasswordReset()
        
    return render(request, 'password_reset.html', {'form': form, 'profile': profile})


def forgot_my_password(request):
    if request.method=='POST':
        form = ForgotMyPassword(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(username=form.cleaned_data["username"])
                if form.cleaned_data["mail"] == user.email:
                    code = random.randrange(100000,1000000)
                    subject = 'Forgot My Password'
                    message = f'Hi {user.username}, this is your validation code:\n\n{code}'
                    email_from = socialwebsite.settings.EMAIL_HOST_USER
                    recipient_list = [user.email, ]
                    send_mail( subject, message, email_from, recipient_list )
                    request.session['password_reset_code'] = code
                    request.session['userusername'] = user.username
                    return redirect('confirm_password_code')
                else:
                    messages.error(request, 'Mail address is wrong.')

            except User.DoesNotExist:
                messages.error(request, 'Username does not exist.')

    else:
        form = ForgotMyPassword()

    return render(request, 'forgot_my_password.html', {'form':form})




def confirm_password_code(request):
    code = request.session.get('password_reset_code')
    if not code:
        messages.error(request, 'Validation code is missing.')
        return redirect('forgot_my_password')
    else:
        if request.method == 'POST':
            form = PasswordMailCode(data=request.POST)
            if form.is_valid():
                verify_code = form.cleaned_data["mail_code"]
                if int(verify_code) == int(code):
                    del request.session['password_reset_code']
                    new_code = random.randrange(10000000,100000000)
                    request.session['control_section2'] = new_code
                    return redirect('new_password')
                else:
                    messages.error(request, 'Code is wrong.')
        else:
            form = PasswordMailCode()
        return render(request, 'confirm_password_code.html', {'form': form,'code':code})


def new_password(request):
    new_code = request.session.get('control_section2')
    if not new_code:
        messages.error(request, 'Validation code is missing.')
        return redirect('forgot_my_password')
    
    else:
        if request.method == 'POST':
            form = PasswordReset(request.POST)
            if form.is_valid():
                new_password1 = form.cleaned_data["new_password1"]
                new_password2 = form.cleaned_data["new_password2"]
                if new_password1 == new_password2:
                    user = User.objects.get(username=request.session['userusername'])
                    user.set_password(new_password1)
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, 'Your password was successfully updated!')
                    del request.session['control_section2'] 
                    return redirect('user_login')
                else:
                    messages.error(request, 'Password confirmation is wrong.')
                    return redirect('new_password')
            else:
                messages.error(request, 'There were some mistakes in the form.')
        else:
            form = PasswordReset()

        return render(request, 'new_password.html', {'form':form})
    

@login_required
def user_pages(request, username):
    try:
        if username!=request.user.username:

            profile_instance = Profile.objects.get(user=request.user)
            user_of_searched = User.objects.get(username=username)
            profile_of_searched = Profile.objects.get(user=user_of_searched)
            if not request.user in profile_of_searched.blocked.all():
                user_posts = Post.objects.filter(user=user_of_searched)
                notification,_ = MyFollowNotification.objects.get_or_create(follow_reciever=user_of_searched)
                sent = False
                if request.user in notification.follow_sender.all():
                    sent = True
                return render(request, 'user_pages.html', {'profile':profile_instance,'searched_profile':profile_of_searched,'searched_user':user_of_searched,'posts':user_posts,'sent':sent})
            else:
                messages.error(request,'Profile Does Not Exist')
                return redirect('home')
        else:
            return redirect('user_profile')
    except User.DoesNotExist:
        messages.error(request,f'There is no user which username: {username}')
        return redirect('home')
    
@login_required
def search_something(request):
    profile_instance = Profile.objects.get(user=request.user)
    if request.method=='POST':
        searched = request.POST.get('searched','')
        if not searched:
             return render(request, 'search.html', {'profile': profile_instance})
        else:
            istartw = []
            startw = []
            equalw = []
            elsew = []
            
            try:
                user_equal = User.objects.get(username=searched)
                equalw.append(user_equal)
            except User.DoesNotExist:
                pass
            
            user_start = User.objects.filter(username__startswith=searched)
            for i in user_start:
                startw.append(i)   

            user_istart = User.objects.filter(username__istartswith=searched)
            for i in user_istart:
                istartw.append(i)       

            new_searched = searched.lower()
            users_all = User.objects.filter(username__contains=new_searched)
            for i in users_all:
                elsew.append(i)
           

            istartw_control = []
            elsew_control = []
            for i in istartw:
                if not i in startw:
                    istartw_control.append(i)

            for i in elsew:
                if not i in startw and not i in istartw:
                    elsew_control.append(i)
                    
            def sort_users(request,lists):
                user_list = []
                for i in lists:
                    user_list.append(i.username)

                sorted_list = sorted(user_list, key=lambda x: (len(x), x))
                user_sorted = []
                for i in sorted_list:
                    for q in lists:
                        if q.username == i:
                            user_sorted.append(q)
                
                return user_sorted, sorted_list
            
            istart_updated, istartw_username = sort_users(request,istartw_control)
            start_updated, startw_username = sort_users(request, startw)
            else_updated, none_list = sort_users(request, elsew_control)

            def merge(request, list1,list2):
                new_list = []
                index1 = 0
                index2 = 0
                while index1 < len(list1) and index2 < len(list2):
                    if len(list1[index1]) <= len(list2[index2]):
                        new_list.append(list1[index1])
                        index1 += 1

                    else:
                        new_list.append(list2[index2])
                        index2 += 1

                new_list.extend(list1[index1:])
                new_list.extend(list2[index2:])
                return new_list

            extended_starts = merge(request, startw_username,istartw_username)
            extended_users = []
            for i in extended_starts:
                control = 0
                for q in start_updated:
                    if q.username == i:
                        control = 1
                        extended_users.append(q)
                        break

                if control==0:
                    for q in istart_updated:
                        if q.username == i:
                            extended_users.append(q)
                            break

            extended_users.extend(else_updated)
            if len(extended_users)>50:
                extended_users = extended_users[:50]

            all_profiles = []
            for i in users_all:
                if request.user != i:
                    each_profile = Profile.objects.get(user=i)
                    all_profiles.append(each_profile)

            for each_user in extended_users:
                if request.user in each_user.profile.blocked.all():
                    extended_users.remove(each_user)
            
            if extended_users:
                return render(request, 'search.html', {'profile':profile_instance,'searched':searched,'users':extended_users,'all_profiles':all_profiles})
            else:
                return render(request, 'search.html', {'profile':profile_instance,'searched':searched})
        
@login_required
def complain_user(request, profile_username):
    profile_instance = Profile.objects.get(user=request.user)
    try:
        complained_user = User.objects.get(username = profile_username)
        if request.method == 'POST':
            form = ComplainProfileForm(request.POST)
            if form.is_valid():
                reason = form.cleaned_data['reason']
                subject = f'Complain Profile of {complained_user.username}'
                message = f'Hi I am {request.user.username}:  http://127.0.0.1:8000/user/{request.user.username}\n\nI complain this profile because:\n{reason}\nThere is the link of the profile:\nhttp://127.0.0.1:8000/user/{complained_user.username}' 
                email_from = socialwebsite.settings.EMAIL_HOST_USER
                recipient_list = ['bfbdhdbr@gmail.com', ]
                send_mail( subject, message, email_from, recipient_list )
                messages.success(request, 'Your complain has delivered ')
                return redirect('home')
        else:
            form = ComplainProfileForm()

        return render(request, 'complain_profile.html', {'profile':profile_instance, 'form':form,'complained':complained_user})
    except User.DoesNotExist:
        messages.error(request, 'Profile does not exist')
        return redirect('home')


@login_required
def have_problem(request):
    profile_instance = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = HaveProblemForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            reason = form.cleaned_data['reason']
            subject = f'{title}'
            message = f'{reason}\nfrom: http://127.0.0.1:8000/user/{request.user.username}' 
            email_from = socialwebsite.settings.EMAIL_HOST_USER
            recipient_list = ['bfbdhdbr@gmail.com', ]
            send_mail( subject, message, email_from, recipient_list )
            messages.success(request, 'Your complain has delivered ')
            return redirect('home')
    else:
        form = HaveProblemForm()

    return render(request, 'have_problem.html', {'profile':profile_instance,'form':form})

@login_required
def my_likes(request):
    profile_instance = Profile.objects.get(user=request.user)
    posts = profile_instance.liked_posts.all()
    return render(request, 'my_likes.html', {'profile':profile_instance,'posts':posts})

@login_required
def my_comments(request):
    profile_instance = Profile.objects.get(user=request.user)
    comments = profile_instance.comments.all()
    return render(request, 'my_comments.html', {'profile':profile_instance,'comments':comments})

@login_required
def follow(request, follow_username):
    try:
        profile_instance = Profile.objects.get(user=request.user)
        follow_user = User.objects.get(username=follow_username)
        follow_profile = Profile.objects.get(user=follow_user)
        if profile_instance.follows.filter(username=follow_user.username).exists():
            profile_instance.follows.remove(follow_user)
            follow_profile.followers.remove(request.user)
            messages.success(request,f'you do not follow {follow_username} anymore')
            return HttpResponse(status=204)
        else:
            if not follow_profile.private:
                profile_instance.follows.add(follow_user)
                follow_profile.followers.add(request.user)
                messages.success(request,f'you follow {follow_username}')
                return HttpResponse(status=204)
            else:
                notification,_ = MyFollowNotification.objects.get_or_create(follow_reciever=follow_user)
                notification.follow_sender.add(request.user) 
                messages.success(request,'Your request has delivered')
                return HttpResponse(status=204)
    except User.DoesNotExist:
        messages.error(request,'Profile Does Not Exist')
        return redirect('home')


@login_required
def display_followers(request,username):
    try:
        profile_instance = Profile.objects.get(user=request.user)
        user = User.objects.get(username=username)
        profile_of_user = Profile.objects.get(user=user)
        if profile_instance.follows.filter(username=user.username).exists() or not profile_of_user.private or profile_of_user==profile_instance:
            followers = profile_of_user.followers.all()
            return render(request,'followers.html', {'profile':profile_instance, 'profile_of_user':profile_of_user, 'followers':followers})

        else:
            messages.error(request,f'You cannot see the followers of the {profile_of_user.user.username} because you do not follow its profile ')
            return HttpResponse(status=204)

    except User.DoesNotExist:
        messages.error(request,'Profile Does Not Exist')
        return redirect('home')
    
@login_required
def display_follows(request,username):
    try:
        profile_instance = Profile.objects.get(user=request.user)
        user = User.objects.get(username=username)
        profile_of_user = Profile.objects.get(user=user)
        if profile_instance.follows.filter(username=user.username).exists() or not profile_of_user.private or profile_of_user==profile_instance:
            follows = profile_of_user.follows.all()
            return render(request,'follows.html', {'profile':profile_instance, 'profile_of_user':profile_of_user, 'follows':follows})

        else:
            messages.error(request,f'You cannot see the followers of the {profile_of_user.user.username} because you do not follow its profile ')
            return HttpResponse(status=204)

    except User.DoesNotExist:
        messages.error(request,'Profile Does Not Exist')
        return redirect('home')
    

@login_required
def block(request,username):
    try:
        profile_instance = Profile.objects.get(user=request.user)
        blocked_user = User.objects.get(username=username)
        blocked_profile = Profile.objects.get(user=blocked_user)
        if not blocked_user in profile_instance.blocked.all():
            profile_instance.blocked.add(blocked_user)
            if blocked_user in profile_instance.follows.all():
                profile_instance.follows.remove(blocked_user)

            if blocked_user in profile_instance.followers.all():
                profile_instance.followers.remove(blocked_user)

            if request.user in blocked_profile.followers.all():
                blocked_profile.followers.remove(request.user)

            if request.user in blocked_profile.follows.all():
                blocked_profile.follows.remove(request.user)
            
            return HttpResponse(status=204)
        else:
            profile_instance.blocked.remove(blocked_user)
            return HttpResponse(status=204)

    except User.DoesNotExist:
        messages.error(request,'Profile Does Not Exist')
        return redirect('home')