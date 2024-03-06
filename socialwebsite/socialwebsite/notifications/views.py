from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from users.models import Profile
from .models import MyFollowNotification


@login_required
def my_follow_notifications(request):
    profile_instance = Profile.objects.get(user=request.user)
    my_notifications,_ = MyFollowNotification.objects.get_or_create(follow_reciever=request.user)
    senders = []
    for sender in my_notifications.follow_sender.all():
        senders.append(sender)

    return render(request, 'my_follow_notifications.html', {'profile':profile_instance,'senders':senders})

@login_required
def accept_follow_request(request,sender):
    profile_instance = Profile.objects.get(user=request.user)
    try:
        sender_user = User.objects.get(username=sender)
        sender_profile = Profile.objects.get(user=sender_user)
        my_notifications = MyFollowNotification.objects.get(follow_reciever=request.user)
        if sender_user in my_notifications.follow_sender.all():
            my_notifications.follow_sender.remove(sender_user)
            profile_instance.followers.add(sender_user)
            sender_profile.follows.add(request.user)
            messages.success(request,'Accepted')
            return redirect('my_follow_notifications')
        else:
            messages.error(request,'This Follow Request Does Not Exist')
            return redirect('home')
    except User.DoesNotExist:
        messages.error(request,'Profile Does Not Exist')
        return HttpResponse(status=204)
    
@login_required
def deny_follow_request(request,sender):
    profile_instance = Profile.objects.get(user=request.user)
    try:
        sender_user = User.objects.get(username=sender)
        my_notifications = MyFollowNotification.objects.get(follow_reciever=request.user)
        if sender_user in my_notifications.follow_sender.all():
            my_notifications.follow_sender.remove(sender_user)
            messages.success(request,'Denied')
            return redirect('my_follow_notifications')
        else:
            messages.error(request,'This Follow Request Does Not Exist')
            return redirect('home')
    except User.DoesNotExist:
        messages.error(request,'Profile Does Not Exist')
        return HttpResponse(status=204)
    
@login_required
def undo_follow_request(request,reciever):
    try:
        recievers_user = User.objects.get(username=reciever)
        notification = MyFollowNotification.objects.get(follow_reciever=recievers_user)
        if request.user in notification.follow_sender.all():
            notification.follow_sender.remove(request.user)
            messages.success(request,'Undo!')
            return HttpResponse(status=204)
        else:
            messages.error(request,'You Do Not Follow Anyway')
            return HttpResponse(status=204)
    except User.DoesNotExist:
        messages.error(request,'Profile Does Not Exist')
        return redirect('home')
    except MyFollowNotification.DoesNotExist:
        messages.error(request,'Error')
        return redirect('home')