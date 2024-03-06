from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from users.models import Profile
from .forms import ChatForm
from .models import MessagesOfUser
from .models import Chat
# Create your views here.

@login_required
def send_message(request,username):
    profile_instance = Profile.objects.get(user=request.user)
    try:
        user_of_message = User.objects.get(username=username)
        if request.method=='POST':
            form = ChatForm(request.POST)
            if form.is_valid():
                content = form.save(commit=False)
                content.sent_by = request.user
                content.sent_to = user_of_message
                content.save()
                owner_messages, _ = MessagesOfUser.objects.get_or_create(owner=request.user)
                owner_messages.to_who.add(user_of_message)
                owner_messages.message_content.add(content)
                return redirect('conversation', username=username)


        else:
            form = ChatForm()

        return render(request, 'send_message.html', {'profile':profile_instance,'form':form,'user_of_message':user_of_message})

    except User.DoesNotExist:
        messages.error(request,'Profile Does Not Exist')
        return redirect('home')
    

@login_required
def messenger(request):
    profile_instance = Profile.objects.get(user=request.user)
    my_messages_user = MessagesOfUser.objects.filter(owner=request.user)
    users = set()
    all_messages = list()
    last_messages_users = list()
    last_messages = list()
    last_version_of_messages = dict()
    for messages_user in my_messages_user:
        for each_message in messages_user.message_content.all():
            all_messages.append(each_message)
    
    for message_user in my_messages_user:
        for i in message_user.to_who.all():
            users.add(i.username)

    for chat in Chat.objects.filter(sent_to=request.user):
        all_messages.append(chat)
        users.add(chat.sent_by.username)

    all_messages = sorted(all_messages, key=lambda x: x.slug, reverse=True)

    for message in all_messages:
        if message.sent_to.username != request.user.username and message.sent_to.username not in last_messages_users:
            last_messages_users.append(message.sent_to.username)
            last_messages.append(message)

        elif message.sent_by.username!=request.user.username and message.sent_by.username not in last_messages_users:
            last_messages_users.append(message.sent_by.username)
            last_messages.append(message)
    
    for i in range(len(last_messages_users)):
        messenger_user = User.objects.get(username=last_messages_users[i])
        last_version_of_messages[messenger_user] = last_messages[i]

    new_chat_user = set()
    for i in profile_instance.follows.all():
        if i.username not in users:
            new_chat_user.add(i.username)
    return render(request, 'messenger.html', {'profile': profile_instance, 'last_messages': last_version_of_messages,'new_chat_user':new_chat_user})

@login_required
def conversation(request,username):
    profile_instance = Profile.objects.get(user=request.user)
    try:
        all_messages = []
        user_chat = User.objects.get(username=username)
        sent_messages,_ = MessagesOfUser.objects.get_or_create(owner=request.user)
        for i in sent_messages.message_content.all():
            if i.sent_to == user_chat:
                all_messages.append(i)

        for chat in Chat.objects.filter(sent_by=user_chat,sent_to=request.user):
            all_messages.append(chat)
            chat.seen = True
            chat.save()

        all_messages = sorted(all_messages, key=lambda x: x.slug)
        return render(request, 'conversation.html', {'profile':profile_instance, 'all_messages':all_messages,'user_chat':user_chat})

    except User.DoesNotExist:
        messages.error(request,'Profile Does Not Exist')
        return HttpResponse(status=204)

@login_required  
def delete_message(request,username,message_slug):
    try:
        user_of_message = User.objects.get(username=username)
        deleted_message = Chat.objects.get(sent_by=request.user,sent_to=user_of_message,slug=message_slug)
        deleted_message.delete()
        my_messages = MessagesOfUser.objects.get(owner=request.user)
        other_messages = Chat.objects.filter(sent_by=request.user,sent_to=user_of_message)
        if other_messages:
            messages.success(request,'Message Deleted')
            return redirect('conversation', username=username)
        else:
            my_messages.to_who.remove(user_of_message)
            messages.success(request,'Message Deleted')
        return redirect('conversation', username=username)

    except Chat.DoesNotExist:
        messages.error(request,'Message Does Not Exist')
        return redirect('home')
    
    except User.DoesNotExist:
        messages.error(request,'Profile Does Not Exist')
        return redirect('home')