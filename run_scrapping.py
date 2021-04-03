import os
import sys

from django.contrib.auth import get_user_model
import asyncio

sys.path.append(os.getcwd())
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django
django.setup()
from django.db import DatabaseError

from scraping.parser import *
from scraping.models import Vacancy, City, Language, Errors, Url

user = get_user_model()

parsers = (
    (work, "work"),
    (rabota, "rabota"),
    (dou, "dou"),
    (djinni, "djinni"),
)

jobs, errors = [], []


def get_settings():
    queryset = user.objects.filter(send_email=True).values()
    settings_list = set((q['city_id'], q['lang_id']) for q in queryset)
    return settings_list


def get_urls(_settings):
    queryset = Url.objects.all().values()
    url_dict = {(q['city_id'], q['lang_id']): q['url_data'] for q in queryset}
    urls = []
    for pair in _settings:
        tmp = {}
        tmp['city'] = pair[0]
        tmp['lang'] = pair[1]
        tmp['data'] = url_dict[pair]
        urls.append(tmp)
    return urls


async def main(value):
    func, url, city, lang = value
    job, err = await loop.run_in_executor(None, func, url, city, lang)
    errors.extend(err)
    jobs.extend(job)


settings = get_settings()
url_list = get_urls(settings)

loop = asyncio.get_event_loop()
tmp_task = [
    (func, data['data'][key], data['city'], data['lang'])
    for data in url_list
    for func, key in parsers
]
tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_task])

#
# for data in url_list:
#     for func, key in parsers:
#         url = data['data'][key]
#         j, e = func(url, city=data['city'], language=data['lang'])
#         jobs += j
#         errors += e

loop.run_until_complete(tasks)
loop.close()

for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass
if errors:
    err = Errors(data=errors).save()

handler = open("work.txt", "w")
handler.write(str(jobs))
handler.close()
