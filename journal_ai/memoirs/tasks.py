from celery import shared_task
import os
import requests
import time
from celery.utils.log import get_task_logger
from django.contrib.auth.models import User
from journal_ai.memoirs.models import Memoir
from journal_ai.memoirs.encryption import AESCipher
from ..insights.models import Insight
from django.utils import timezone

BASE_ENDPOINT = os.environ.get('BASE_ENDPOINT')
DEBUG = os.environ.get('CALL_ORACLE')

logger = get_task_logger(__name__)
ENCRYPTER = AESCipher(os.getenv('AES_CIPHER_KEY'))


# create a shared task to call an external API for getting insight given prompt and journal entry


@shared_task
def get_insight(journaler_id, memoir_id, memoir_text):
    try:
        user = User.objects.filter(pk=journaler_id).first()
        if not user:
            logger.info(
                'user not found for journaler id: {0}'.format(journaler_id))
            return
        memoir = Memoir.objects.filter(pk=memoir_id).first()
        jprompt = memoir.getPrompt()
        logger.info(f"jprompt: {jprompt.keys()}")
        jprompt = jprompt['text']

        if DEBUG == '0':
            time.sleep(5)
            insight_text = 'This is a hardcoded test insight.'
        else:
            url = f"{BASE_ENDPOINT}/get_insight?entry={memoir_text}&jprompt={jprompt}"
            try:
                response = requests.request("GET", url)
                insight_text = eval(response.text)['insight']
                insight_text = insight_text.encode('raw_unicode_escape').decode(
                    'unicode_escape').encode('utf-16_BE', 'surrogatepass').decode('utf-16_BE')
            except Exception as e:
                logger.info(f"Exception in accessing oracle: {e}")
                return

        if not memoir:
            logger.info('memoir not found for memoir id: {0}'.format(memoir_id))
            return

        insight = Insight.objects.filter(memoir=memoir, journaler=user).first()
        insight = Insight(memoir=memoir, journaler=user,
                        release_timestamp=timezone.now(), text=insight_text)
        insight.save()
        logger.info('insight saved for memoir id: {0}'.format(memoir_id))
    except Exception as e:
        logger.info(f"Exception: {e}")
        return


@shared_task
def encrypt_memoir(memoir_id):
    try:
        memoir = Memoir.objects.filter(pk=memoir_id).first()
        if not memoir:
            logger.info(
                'unable to find memoir to encrypt'
            )
            return

        # encrypt data (not best way but can live with it for now)
        memoir.text = ENCRYPTER.encrypt(memoir.text)
        memoir.encrypted = True
        memoir.save()
    except Exception as e:
        logger.info(f"Exception: {e}")
        return