from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Member

def members_home(request):
    template = loader.get_template("membersHome.html")
    context = {
        "username":"Hopkins",
    }
    return HttpResponse(template.render(context,request))

def list_members(request):
    template = loader.get_template("list_members.html")
    members = Member.objects.all().values()
    context ={
        "members":members
    }
    return HttpResponse(template.render(context,request))

def user_details(request,id):
    member = Member.objects.get(id = id)
    template = loader.get_template("memberDetail.html")
    context = {
        "member":member
    }
    return HttpResponse(template.render(context,request))