from django.urls import path
from .views import PromptView,getPromptsByDate,addPrompt

urlpatterns = [
    path('', PromptView.as_view(), name='promptView'),
    path('date/<int:user_id>', getPromptsByDate, name='getPromptByDate'),
    path('<str:auth_key>',addPrompt, name='add_prompt')
] 