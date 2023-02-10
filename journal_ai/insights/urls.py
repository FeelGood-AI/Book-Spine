from django.urls import path
from .views import InsightView, getInsightByMemoir,MarkInsightHelpful

urlpatterns = [
    path('', InsightView.as_view(), name='insightView'),
    path('<int:memoir_id>', getInsightByMemoir, name='getInsightByMemoir'),
    path('mark_helpful/<int:insight_id>', MarkInsightHelpful.as_view(), name='markInsightHelpful')
] 