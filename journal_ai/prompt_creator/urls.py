from django.urls import path
from .views import PromptView,getPromptsByDate

urlpatterns = [
    path('', PromptView.as_view(), name='promptView'),
    path('date/<int:user_id>', getPromptsByDate, name='getPromptByDate'),
] 