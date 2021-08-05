from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dm.models import Message

@login_required
def inbox(request):
    messages = Message.get_messages(user=request.user)
    active_dm = None
    dms = None

    if messages:
        message = messages[0]
        active_dm = message['user'].username
        dms = Message.objects.filter(user=request.user, recipient=message['user'])
        dms.update(is_read=True)

        # visual display to show number of unread messages
        for message in messages:
            if message['user'].username == active_dm:
                message['unread'] = 0
        
        context = {
            'dms': dms,
            'messages': messages,
            'active_dm': active_dm,
        }
    try:
        return render(request, 'dm/messages.html', context)
    except:
        return render(request, 'dm/messages.html')

@login_required
def Dms(request, username):
    user = request.user
    messages = Message.get_messages(user=user)
    active_dm = username
    dms = Message.objects.filter(user=user, recipient__username=username)
    dms.update(is_read=True)
    for message in messages:
        if message['user'].username == username:
            message['unread'] = 0

    context = {
        'dms': dms,
        'messages': messages,
        'active_direct':active_dm,
    }
    return render(request, 'dm/messages.html', context)