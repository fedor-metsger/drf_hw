
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from learning.models import Intent
from learning.services import retrieve_pi


@shared_task
def send_course_update_alert(course_title, user_email):
    count = send_mail(
        subject=f'Обновление курса "{course_title}"',
        message=f'Курс \"{course_title}\" обновился, приглашаем ознакомиться.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email]
    )

@shared_task
def check_pi_status():
    with open("/tmp/learning.log", "a") as f:
        f.write(f'Запускаю проверку статусов платежей:\n')
        for pi in Intent.objects.all():
            pi_id, pi_status = retrieve_pi(pi.pi_id)
            if pi_status != pi.status:
                pi.status = pi_status
                pi.save()
            f.write(f'Payment intent {pi.pk} ("{pi_id}"): "{pi_status}"\n')

