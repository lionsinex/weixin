# -*- coding: UTF-8 -*-

import logging

import requests
from django.conf import settings
from django.db import transaction
from django.db.utils import IntegrityError
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User, Authentication
from utils.response import error_response
from utils.views import require_parameters
from utils.security import HashedPassword
from utils.status import Status
logger = logging.getLogger("apps")


class RegisterView(APIView):
    @method_decorator(require_parameters(["phone_number",
                                          "verification_code",
                                          "password"]))
    def post(self, request):
        phone_number = request.POST["phone_number"]
        verification_code = request.POST["verification_code"]
        password = request.POST["password"]
        credential = HashedPassword.get_hashed_credential(password)

        if not self.verify_code(phone_number, verification_code):
            return error_response(Status.VERIFICATION_FAILED,
                                  Status.VERIFICATION_FAILED.phrase,
                                  _("Verification Code Incorrect"))

        try:
            with transaction.atomic():
                user = User.objects.create(phone=int(phone_number))
                Authentication.objects.create(user=user,
                                              identity_type=IdentityType.LOCAL.value,
                                              identifier=user.id,
                                              credential=credential,
                                              )


        except IntegrityError as e:
            transaction.rollback()
            logger.error(e)
            return error_response(Status.REGISTER_FAILED,
                                  Status.REGISTER_FAILED.phrase,
                                  )

        tasks.notify_cpa.delay(user.id, request.qua.channel)

        return Response()

    @staticmethod
    def verify_code(phone_number, verification_code):
        url = settings.VERIFY_URL
        verification_request = {"identity_type": "phone",
                                "identifier": phone_number,
                                "verification_code": verification_code,
                                "verification_type": "register",
                                }
        verification_response = requests.post(url, data=verification_request)
        if not verification_response.ok:
            try:
                logger.error(verification_response.json())
            except ValueError:
                logger.error("Verify code failed")
            finally:
                return False

        return True

