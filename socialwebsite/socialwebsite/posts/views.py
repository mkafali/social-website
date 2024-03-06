from django.shortcuts import render, redirect
from users.models import Profile
from .forms import PhotoPostForm, PhotoPostEditForm, ConfirmPasswordForm, ComplainPostForm, CommentForm, ComplainCommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import socialwebsite.settings
from django.core.mail import send_mail
from django.http import HttpResponse

@login_required
def crate_post(request):
    profile_instance = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = PhotoPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('user_profile')
            
    else:
        form = PhotoPostForm(instance=request.user)
    return render(request, 'create_post.html',{'profile':profile_instance,'form':form})

@login_required
def edit_post(request,username,post_slug):
    try:
        if username==request.user.username:
            profile_instance = Profile.objects.get(user=request.user)
            post_instance = Post.objects.get(user=request.user, slug=post_slug)
            if post_instance.user == request.user:
                if request.method == 'POST':
                    form = PhotoPostEditForm(request.POST,instance=post_instance)
                    if form.is_valid():
                        form.save()
                        return redirect('user_profile')
                else:
                    form = PhotoPostEditForm(instance=post_instance)

                return render(request, 'edit_post.html', {'profile':profile_instance, 'form':form, 'post':post_instance})
            else:
                messages.error(request,'How Dare You')
                return redirect('home')
        else:
            messages.error(request,'How Dare You!!!')
            return redirect('home')
        
    except Post.DoesNotExist:
        messages.error(request, 'How Dare You')
        return redirect('home')

@login_required
def delete_post(request, username, post_slug):
    try:
        if username==request.user.username:
            profile_instance = Profile.objects.get(user=request.user)
            post_instance = Post.objects.get(user=request.user, slug=post_slug)
            if post_instance.user == request.user:
                if request.method=='POST':
                    form = ConfirmPasswordForm(request.POST)
                    if form.is_valid():
                        password = form.cleaned_data['your_password']
                        user = authenticate(username=request.user.username, password=password)
                        if user is not None:
                            post_instance.delete()
                            return redirect('user_profile')
                        else:
                            messages.error(request, 'Wrong Password')

                        
                else:
                    form = ConfirmPasswordForm()

                return render(request, 'delete_post.html', {'profile':profile_instance,'form':form,'post':post_instance})
            else:
                messages.error(request,'How Dare You')
                return redirect('home')
        else:
            messages.error(request, 'Yok knk')
            return redirect('home')

        
    except Post.DoesNotExist:
        messages.error(request,'You can not. How dare you')
        return redirect('home')
    

@login_required    
def complain_post(request, username, post_slug):
    profile_instance = Profile.objects.get(user=request.user)
    try:
        user = request.user
        post_user = User.objects.get(username=username)
        if not post_user in profile_instance.blocked.all() and not request.user in post_user.profile.blocked.all():
            if profile_instance.follows.filter(username=username).exists() or not post_user.profile.private or post_user==user:
                post = Post.objects.get(slug=post_slug)
                if request.method == 'POST':
                    form = ComplainPostForm(request.POST)
                    if form.is_valid():
                        reason = form.cleaned_data['reason']
                        subject = f'Complain Post of {post_user.username}'
                        message = f'Hi I am {user.username}:  http://127.0.0.1:8000/user/{user.username}\n\nI complain this post because:\n{reason}\nThere is the link of the post:\nhttp://127.0.0.1:8000/post/{post_user.username}/{post_slug}' 
                        email_from = socialwebsite.settings.EMAIL_HOST_USER
                        recipient_list = ['bfbdhdbr@gmail.com', ]
                        send_mail( subject, message, email_from, recipient_list )
                        messages.success(request, 'Your complain has delivered ')
                        return redirect('home')

                else:
                    form = ComplainPostForm()

                return render(request, 'complain_post.html', {'profile':profile_instance,'form':form,'post':post})
            else:
                messages.error(request,'You Cannot')
                return redirect('home')
        
        else:
            messages.error(request,'Profile Does Not Exist')
            return redirect('home')
        
    except (Post.DoesNotExist, User.DoesNotExist):
        messages.error(request, 'Post Does not exist')
        return redirect('home')

@login_required
def post_pages(request,username,post_slug):
    try:
        profile_instance = Profile.objects.get(user=request.user)
        user_of_searched = User.objects.get(username=username)
        if not user_of_searched in profile_instance.blocked.all() and not request.user in user_of_searched.profile.blocked.all():
            if profile_instance.follows.filter(username=username).exists() or not user_of_searched.profile.private or user_of_searched==request.user:
                profile_of_searched = Profile.objects.get(user=user_of_searched)
                user_post = Post.objects.get(slug=post_slug)
                return render(request, 'post_pages.html', {'profile':profile_instance,'searched_profile':profile_of_searched,'searched_user':user_of_searched,'post':user_post})
            else:
                messages.error(request, 'You cannot see a post which shared by a user which you do not')
                return redirect('home')
        else:
            messages.error(request,'Profile Does Not Exist')
            return redirect('home')

    except (Profile.DoesNotExist,User.DoesNotExist):
        messages.error(request, f'There is no user which username: {username}')
        return redirect('home')
    except Post.DoesNotExist:
        messages.error(request, 'Post Does Not Exist')
        return redirect('home')

@login_required
def like_post(request, post_user, post_slug):
    try:
        profile_instance = Profile.objects.get(user=request.user)
        user = User.objects.get(username=post_user)
        if not user in profile_instance.blocked.all() and not request.user in user.profile.blocked.all():
            if profile_instance.follows.filter(username=post_user).exists() or not user.profile.private or user==request.user:
                post = Post.objects.get(user=user,slug=post_slug)
                if post.liked_by.filter(username=request.user.username).exists():
                    post.liked_by.remove(request.user)
                    profile_instance.liked_posts.remove(post)
                    return HttpResponse(status=204)
                else:
                    post.liked_by.add(request.user)
                    profile_instance.liked_posts.add(post)
                    return HttpResponse(status=204)
            else:
                messages.error(request,'you cannot?')
                return redirect('home')
        else:
            messages.error(request,'Profile Does Not Exist')
            return redirect('home')
    except Post.DoesNotExist:
        messages.error(request,'Profile Does Not Exist')
        

@login_required
def who_liked(request,post_user,post_slug):
    try:
        profile_instance = Profile.objects.get(user=request.user)
        user = User.objects.get(username=post_user)
        if not user in profile_instance.blocked.all() and not request.user in user.profile.blocked.all():
            if profile_instance.follows.filter(username=post_user).exists() or not user.profile.private or user==request.user:
                post = Post.objects.get(user=user,slug=post_slug)
                liked_list = post.liked_by.all()
                liked_users = [user for user in liked_list]
                liked_profiles = []
                for i in liked_users:
                    liked_profiles.append(Profile.objects.get(user=i))
                return render(request, 'who_liked.html', {'profile':profile_instance,'liked_by':liked_profiles})
            else:
                messages.error(request,'you cannot?')
                return redirect('home')
        else:
            messages.error(request,'Profile Does Not Exist')
            return redirect('home')
    except (User.DoesNotExist,Post.DoesNotExist):
        messages.error(request,'Profile Does Not Exist')
        return HttpResponse(status=204)


@login_required
def comment_post(request,post_user,post_slug):
    try:
        profile_instance = Profile.objects.get(user=request.user)
        user = User.objects.get(username=post_user)
        if not user in profile_instance.blocked.all() and not request.user in user.profile.blocked.all():
            if profile_instance.follows.filter(username=post_user).exists() or not user.profile.private or user==request.user:
                post = Post.objects.get(user=user, slug=post_slug)
                if request.method == 'POST':
                    form = CommentForm(request.POST)
                    if form.is_valid():
                        comment = form.save(commit=False)
                        comment.post = post
                        comment.commented_by = request.user
                        comment.save()
                        profile_instance.comments.add(comment)
                        post.comments.add(comment)
                        return HttpResponse(status=204)

                else:
                    form = CommentForm()

                return render(request, 'comment.html', {'profile':profile_instance,'form':form,'post':post})
            else:
                messages.error(request,'you cannot?')
                return redirect('home')
        else:
            messages.error(request,'Profile Does Not Exist')
            return redirect('home')
    
    except (User.DoesNotExist,Post.DoesNotExist):
        messages.error(request,'Post Does Not Exist')
        return HttpResponse(status=204)
    

@login_required
def who_comment_what(request,post_user,post_slug):
    try:
        profile_instance = Profile.objects.get(user=request.user)
        user = User.objects.get(username=post_user)
        if not user in profile_instance.blocked.all() and not request.user in user.profile.blocked.all():
            if profile_instance.follows.filter(username=post_user).exists() or not user.profile.private or user==request.user :
                post = Post.objects.get(user=user,slug=post_slug)
                comment_list = post.comments.all()
                return render(request, 'who_comments_what.html', {'profile':profile_instance,'comments':comment_list})
            else:
                messages.error(request,'You CANNOT')
                return redirect('home')
        else:
            messages.error(request,'Profile Does Not Exist')
            return redirect('home')

    except (User.DoesNotExist, Post.DoesNotExist):
        messages.error(request,'Post Does Not Exist')
        return HttpResponse(status=204)


@login_required
def delete_comment(request, post_slug, commented_by, comment_slug):
    try:
        comment_user = User.objects.get(username=commented_by)
        if comment_user == request.user:
            post = Post.objects.get(slug=post_slug)
            comment = post.comments.get(commented_by=comment_user, comment_slug=comment_slug)
            deleted_comment = Comment.objects.get(post=post, commented_by=comment_user, comment_slug=comment_slug)
            post.comments.remove(comment)
            comment_user.profile.comments.remove(comment)
            deleted_comment.delete()
            return HttpResponse(status=204)
        else:
            messages.error(request,'How Dare You')
            return redirect('home')

    except (Post.DoesNotExist, User.DoesNotExist):
        messages.error(request,'Post Does Not Exist')
        return HttpResponse(status=204)
    
    except Comment.DoesNotExist:
        messages.error(request,'Comment Does Not Exist')
        return HttpResponse(status=204)

@login_required
def complain_comment(request, post_slug, commented_by, comment_slug):
    profile_instance = Profile.objects.get(user=request.user)
    try:
        profile_instance = Profile.objects.get(user=request.user)
        post = Post.objects.get(slug=post_slug)
        if not post.user in profile_instance.blocked.all() and not request.user in post.user.profile.blocked.all():  
            comment_user = User.objects.get(username=commented_by)
            comment = Comment.objects.get(commented_by=comment_user, comment_slug=comment_slug)
            if profile_instance.follows.filter(username=post.user.username).exists() or not post.user.profile.private or comment_user==request.user: 
                if request.method == 'POST':
                    form = ComplainCommentForm(request.POST)
                    if form.is_valid():
                        reason = form.cleaned_data['reason']
                        subject = f'Complain Comment of {comment_user.username}'
                        message = f'Hi I am {request.user.username}:  http://127.0.0.1:8000/user/{request.user.username}\n\nI complain this comment because:\n{reason}\nThere is the link of the comment:\nhttp://127.0.0.1:8000/comment_page/{post_slug}/{commented_by}/{comment_slug}' 
                        email_from = socialwebsite.settings.EMAIL_HOST_USER
                        recipient_list = ['bfbdhdbr@gmail.com', ]
                        send_mail( subject, message, email_from, recipient_list )
                        messages.success(request, 'Your complain has delivered ')
                        return HttpResponse(status=204)
                else:
                    form = ComplainCommentForm()
                return render(request, 'complain_comment.html', {'profile':profile_instance, 'form':form ,'comment':comment,'post':post})
            else:
                messages.error(request,'YOU CANNOT')
                return redirect('home')
        else:
            messages.error(request,'You Cannot')
            return redirect('home')
        
    except (Post.DoesNotExist, User.DoesNotExist, Comment.DoesNotExist):
        messages.error(request, 'Comment Does Not Exist')
        return redirect('home')



@login_required
def comment_page(request, post_slug, commented_by, comment_slug):
    try:
        profile_instance = Profile.objects.get(user=request.user)
        comment_user = User.objects.get(username=commented_by)
        post = Post.objects.get(slug=post_slug)
        user_of_post = post.user
        if not user_of_post in profile_instance.blocked.all() and not request.user in user_of_post.profile.blocked.all():
            if profile_instance.follows.filter(username=user_of_post.username).exists() or not user_of_post.profile.private or comment_user==request.user:
                comment = Comment.objects.get(commented_by=comment_user, comment_slug=comment_slug)
                return render(request, 'comment_page.html', {'profile':profile_instance, 'post':post, 'comment':comment})
            else:
                messages.error(request, 'no')
                return redirect('home')
        else:
            messages.error(request,'NO')
            return redirect('home')

    except (Post.DoesNotExist, User.DoesNotExist):
        messages.error(request,'Post Does Not Exist')
        return HttpResponse(status=204)
    
    except Comment.DoesNotExist:
        messages.error(request,'Comment Does Not Exist')
        return HttpResponse(status=204)


