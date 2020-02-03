from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View

from utils.views import require_parameters
from wx.models import Article


class Test(View):
    # @method_decorator(login_required)
    @method_decorator(require_parameters(["id", "name"]))
    def get(self, request):
        data = Article.objects.all()
        print(data)
        return HttpResponse("好的，主人！")
