from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models import Max

class Message(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    body = models.TextField(max_length=500, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def send_message(from_user, to_user, body):
        sender_message = Message(
            user = from_user,
            send = from_user,
            recipient = to_user,
            body = body,
            is_read = True)
        sender_message.save()

        recipient_message = Message(
            user = to_user,
            sender = from_user,
            body = body,
            recipient = from_user)
        recipient_message.save()

        return sender_message

    # list of different messages from different users
    def get_messages(user):
        users = []
        d_messages = Message.objects.filter(user=user).values('recipient').annotate(last=Max('date')).order_by('last')
        for d_message in d_messages:
            users.append({
                'user': User.objects.get(pk=d_message['recipient']),
                'last': d_message['last'],
                'unread': Message.objects.filter(user=user, recipient__pk=d_message['recipient'], is_read=False).count()
            })
        return users