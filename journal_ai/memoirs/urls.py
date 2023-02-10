from django.urls import path
from .views import MemoirView, getMemoirsByUser

urlpatterns = [
    path('', MemoirView.as_view(), name='memoirView'),
    path('<str:username>', getMemoirsByUser, name='getMemoirsByUser'),
] 