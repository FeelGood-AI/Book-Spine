from django.urls import path
from .views import InsightView, getInsightByMemoir,MarkInsightHelpful,MarkInsightRead, putInsightIntoMemoir

urlpatterns = [
    path('', InsightView.as_view(), name='insightView'),
    path('<uuid:memoir_id>', getInsightByMemoir, name='getInsightByMemoir'),
    path('<str:auth_key>/<uuid:memoir_id>', putInsightIntoMemoir, name='putInsightIntoMemoir'),
    path('mark_helpful/<uuid:insight_id>', MarkInsightHelpful.as_view(), name='markInsightHelpful'),
    path('mark_read/<uuid:insight_id>', MarkInsightRead.as_view(), name='markInsightHelpful')
] 