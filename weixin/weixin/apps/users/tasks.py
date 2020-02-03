# -*- coding: UTF-8 -*-

from __future__ import absolute_import, unicode_literals

import json
import logging

import redis_lock
import requests
# Create your tasks here
from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage, get_connection
from django_redis import get_redis_connection

# from profiles.models import UserProfile
from users.models import UserLoginLog
from utils.redis import redis_key
from utils.signature import Signature

logger = logging.getLogger("mq")


@shared_task(max_retries=3)
def notify_cpa(user_id, channel):
    req = {"id": user_id,
           "user_id": user_id,
           "channel": channel,
           "type": 1
           }

    req["signature"] = Signature.rsa_sign(req, settings.CPS_PRIVATE_KEY)

    logger.info(req)

    rsp = requests.post(settings.CPS_NOTIFY_URL, data=req)

    data = json.loads(rsp.content)

    logger.info(data)


@shared_task(max_retries=3)
def notify_user_login(user_id):
    UserLoginLog.objects.create(user_id=user_id)


# @shared_task(max_retries=1)
# def notify_big_boss(user_id):
#     """ 大老板触发邮件 """
#     key = redis_key('mixiu', 'big_boss', 'send_email', user_id)
#     logger.info(key)
#     rds = get_redis_connection()
#     if rds.exists(key):
#         return
#     with redis_lock.Lock(rds, redis_key('redlock', key), expire=60):
#         user_profile = UserProfile.objects.select_related('user').filter(user_id=user_id).first()
#         if not user_profile:
#             return
#         # 发送通知邮件
#         # 不用celery的backend
#         connection = get_connection(backend='django.core.mail.backends.smtp.EmailBackend')
#         EmailMessage(
#             connection=connection,
#             subject='大老板通知',
#             body='大老板({}, 靓号{})已经上线啦，赶紧上线去关注下他的砸蛋情况吧！'.format(user_profile.user.name, user_profile.cute_id),
#             to=settings.MAILER_LIST,
#         ).send()
#         # 设置key有效时间
#         # 生产环境每小时通知一次，其他一天一次
#         expire = 60 * 60 if settings.ENVIRONMENT == 'production' else 60 * 60 * 24
#         rds.set(key, 'foobar', ex=expire)
