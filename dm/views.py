from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dm.models import Message

@login_required
def inbox(request):
    d_messages = Message.get_messages(user=request.user)
    active_dm = None
    dms = None

    if d_messages:
        d_message = d_messages[0]
        active_dm = d_message['user'].username
        dms = Message.objects.filter(user=request.user, recipient=d_message['user'])
        dms.update(is_read=True)

        # visual display to show number of unread d_messages
        for d_message in d_messages:
            if d_message['user'].username == active_dm:
                d_message['unread'] = 0
        
        context = {
            'dms': dms,
            'd_messages': d_messages,
            'active_dm': active_dm,
        }
    try:
        return render(request, 'dm/messages.html', context)
    except:
        return render(request, 'dm/messages.html')

@login_required
def Dms(request, username):
    user = request.user
    d_messages = Message.get_messages(user=user)
    active_dm = username
    dms = Message.objects.filter(user=user, recipient__username=username)
    dms.update(is_read=True)
    for d_message in d_messages:
        if d_message['user'].username == username:
            d_message['unread'] = 0

    context = {
        'dms': dms,
        'd_messages': d_messages,
        'active_direct':active_dm,
    }
    return render(request, 'dm/messages.html', context)