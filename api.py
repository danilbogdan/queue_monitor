import secrets
import string
import settings

PHONE = 'step/phone'
SELECT_PHONE = 'step/phone/select'
REGION = 'step/region'
REGION_SELECT = 'step/region/select'
ORGANIZATION = 'step/organization'
ORGANIZATION_SELECT = 'step/organization/select'
SERVICE = 'step/service'
SERVICE_SELECT = 'step/service/select'
DATELINE = 'step/dateline'
DATELINE_SELECT = 'step/dateline/select'
TIME = 'step/time'
TIME_SELECT = 'step/time/select'


def get_session_id():
    return ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(26))


def get_headers():
    return {
        "Origin": settings.QUEUE_SITE,
        "Referer": settings.QUEUE_SITE + "?region_id=",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
