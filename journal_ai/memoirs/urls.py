from django.urls import path
from .views import MemoirView, getMemoirsByUser

urlpatterns = [
    path('', MemoirView.as_view(), name='memoirView'),
    path('<int:user_id>', getMemoirsByUser, name='getMemoirsByUser'),
] 