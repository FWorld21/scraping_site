import os
import sys

import django
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model

sys.path.append(os.getcwd())
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

django.setup()
from scraping.models import Vacancy
from scraping_service.settings import EMAIL_HOST_USER
subject, text_content, from_email = "Рассылка вакансий", "Рассылка вакансий", EMAIL_HOST_USER
empty = "<h2>К сожалению на сегодня по вашим предпочтениям, данных нету.</h2>"
User = get_user_model()
queryset = User.objects.filter(send_email=True).values("city", "lang", "email")
user_dict = {}
for i in queryset:
    user_dict.setdefault((i['city'], i['lang']), [])
    user_dict[(i['city'], i['lang'])].append(i['email'])
if user_dict:
    parameters = {"city_id__in": [], "language_id__in": []}
    for pair in user_dict.keys():
        parameters['city_id__in'].append(pair[0])
        parameters['language_id__in'].append(pair[1])
    queryset = Vacancy.objects.filter(**parameters).values()[:10]
    vacancies = {}
    for i in queryset:
        vacancies.setdefault((i['city_id'], i['language_id']), [])
        vacancies[(i['city_id'], i['language_id'])].append(i)
    for keys, emails in user_dict.items():
        rows = vacancies.get(keys, [])
        html = ''
        for row in rows:
            html += f'<a href="{row["url"]}">{row["title"]}</a>'
            html += f'<p>{row["description"]}</p>'
            html += f'<p>{row["company"]}</p><br><hr>'
        _html = html if html else empty
        for email in emails:
            to = email

            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(_html, "text/html")
            msg.send()
