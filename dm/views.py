from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from dm.models import Message

@login_required
def inbox(request):
    user = request.user
    messages = Message.get_messages(user=user)
    active_dm = None
    dms = None

    if messages:
        message = messages[0]
        active_dm = message['user'].username
        dms = Message.objects.filter(user=user, recipient=message['user'])
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

    return render(request, 'dm/messages.html')