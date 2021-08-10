from django.core import paginator
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dm.models import Message

from django.db.models import Q
from django.core.paginator import Paginator

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

@login_required
def SendDm(request):
    from_user = request.user
    to_user_username = request.POST.get('to_user')
    body = request.POST.get('body')

    if request.method == 'POST':
        to_user = User.objects.get(username=to_user_username)
        Message.send_message(from_user, to_user, body)
        return redirect('messages')
    else:
        HttpResponseBadRequest()

@login_required
def SearchUser(request):
    query = request.GET.get('q')
    context = {}

    if query:
        users = User.objects.filter(Q(username__icontains=query))
        #Pagination
        paginator = Paginator(users, 6)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)

        context = {
            'users': users_paginator,
        }

    return render(request, 'dm/user_search.html', context)