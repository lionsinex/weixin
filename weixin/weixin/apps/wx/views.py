from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from wx.models import Article


class Test(View):
    def get(self, request):
        data = Article.objects.all()
        print(data)
        return HttpResponse("好的，主人！")
