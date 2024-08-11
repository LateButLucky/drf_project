from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_course_update_email(course_title, subscriber_email):
    subject = f'Обновления по курсу {course_title}'
    message = f'В курсе {course_title} появились новые материалы.'
    send_mail(subject, message, 'noreply@example.com', [subscriber_email])
