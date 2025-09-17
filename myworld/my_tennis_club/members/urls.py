from django.urls import path
from . import views

urlpatterns = [
    path('members/',views.list_members,name='members'),
    path('',views.members_home,name='index'),
    path('members/details/<int:id>',views.user_details,name='details')
]
