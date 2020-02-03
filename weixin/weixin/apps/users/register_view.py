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

# from thirdparty.yunxin.requests import YunxinRequests
from users import tasks
from users.models import User, Authentication, IdentityType
from utils.response import error_response
from utils.security import HashedPassword
from utils.status import Status
from utils.views import require_parameters

logger = logging.getLogger("apps")


class RegisterView(APIView):
    @method_decorator(require_parameters(["phone_number",
                                          "verification_code",
                                          "password"]))
    def get(self, request):
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

                # self.create_foreign_accounts(user)
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

    # @staticmethod
    # def create_foreign_accounts(user: User):
    #     from rooms.models import Room, RoomUser, Microphone, RoomTag
    #     from accounts.models import Account
    #     from profiles.models import UserProfile
    #
    #     user_id = str(user.id)
    #     yunxin_requests = YunxinRequests(settings.YUNXIN["APP_KEY"],
    #                                      settings.YUNXIN["APP_SECRET"])
    #     yunxin_id, yunxin_token = \
    #         yunxin_requests.create_user(user_id=user_id,
    #                                     refresh_token_on_exists=True,
    #                                     name=user.name,
    #                                     icon=user.avatar,
    #                                     )
    #     yunxin_room_id = yunxin_requests.create_chat_room(creator_user_id=yunxin_id,
    #                                                       chat_room_name=user_id)
    #     agora_channel = user_id
    #     agora_id = user.id
    #
    #     UserProfile.objects.create(user=user,
    #                                yunxin_token=yunxin_token,
    #                                yunxin_id=yunxin_id,
    #                                agora_id=agora_id,
    #                                cute_id=user.id,
    #                                )
    #     room = Room.objects.create(owner=user,
    #                                tag=RoomTag.SOCIAL.value,
    #                                agora_channel=agora_channel,
    #                                yunxin_room_id=yunxin_room_id,
    #                                cute_id=user.id,
    #                                )
    #     RoomUser.objects.create(room=room,
    #                             user=user,
    #                             is_owner=True,
    #                             )
    #     from rooms.microphones import MicrophoneManager
    #     for position in range(MicrophoneManager.kMinPosition,
    #                           MicrophoneManager.kMaxPosition + 1):
    #         Microphone.objects.create(room=room,
    #                                   position=position)
    #
    #     Account.objects.create(user=user)
