from django.urls import path
from .views import MemoirView, getMemoirsByDate, getMemoirsByUser

urlpatterns = [
    path('', MemoirView.as_view(), name='memoirView'),
    path('date/<str:auth_key>', getMemoirsByDate,name='getMemoirsByDate' ),
    path('<str:username>', getMemoirsByUser, name='getMemoirsByUser'),
] 