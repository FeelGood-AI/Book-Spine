import hashlib
import os
from django.shortcuts import render
import datetime
from django.shortcuts import render
import pytz
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from journal_ai.insights.models import Insight
from journal_ai.memoirs.models import Memoir

def index(request):
    return render(
        request,
        "index.html",
        {
            "title": "Django example",
        },
    )

@api_view(['GET'])
def getStats(request, auth_key):
    test = bytes(auth_key, 'utf-8')
    result = hashlib.md5(test).hexdigest()
    if result != os.getenv('AUTH_KEY'):
        return render(
            request,
            "index.html",
            {
                "title": "Django example",
            },
        )
    userCount = User.objects.all().count()
    now = datetime.datetime.now(pytz.timezone('US/Eastern'))
    yesterday = datetime.datetime.now(pytz.timezone('US/Eastern')) - datetime.timedelta(days=1)
    memoirsCount = Memoir.objects.filter(prompt__date=now).count()
    insights = Insight.objects.filter(memoir__prompt__date=now)
    insightCount = insights.count()
    totalTrue = insights.filter(helpful=True).count()
    totalFalse = insights.filter(helpful=False).count()

    memoirsCountY = Memoir.objects.filter(prompt__date=yesterday).count()
    insightsY = Insight.objects.filter(memoir__prompt__date=yesterday)
    insightCountY = insightsY.count()
    totalTrueY = insightsY.filter(helpful=True).count()
    totalFalseY = insightsY.filter(helpful=False).count()


    return render(request, "stats.html",{'userCount':userCount,'entriesToday':memoirsCount, 
                                         'insightToday': insightCount, 'helpful': 
                                         totalTrue, 'notHelpful': totalFalse,
                                         'feedbackInsight': totalFalse+totalTrue, 
                                         'entriesY':memoirsCountY, 'insightY': insightCountY, 
                                         'helpfulY': totalTrueY, 'notHelpfulY': totalFalseY,
                                         'feedbackInsightY': totalFalseY+totalTrueY })