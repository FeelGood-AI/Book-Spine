from django.urls import path
from .views import InsightView, getInsightByMemoir,MarkInsightHelpful,MarkInsightRead

urlpatterns = [
    path('', InsightView.as_view(), name='insightView'),
    path('<uuid:memoir_id>', getInsightByMemoir, name='getInsightByMemoir'),
    path('mark_helpful/<uuid:insight_id>', MarkInsightHelpful.as_view(), name='markInsightHelpful'),
    path('mark_read/<uuid:insight_id>', MarkInsightRead.as_view(), name='markInsightHelpful')
] 