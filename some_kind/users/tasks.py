# import uuid
# from celery import shared_task
# from datetime import timedelta

# from users.models import User, EmailVerification

# from django.utils import timezone


# @shared_task
# def send_email_verify(user_id):
#     pass
    # user = User.objects.get(id=user_id)
    # expiration = timezone.now() + timedelta(hours=48)
    # record = EmailVerification.objects.create(user=user, code=uuid.uuid4(), expiration=expiration)
    # record.send_verification_email()
