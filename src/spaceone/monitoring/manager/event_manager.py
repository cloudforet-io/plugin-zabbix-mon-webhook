import logging
import hashlib
from spaceone.core import utils
from datetime import datetime
from spaceone.core.manager import BaseManager
from spaceone.monitoring.model.event_response_model import EventModel
from spaceone.monitoring.error.event import *
_LOGGER = logging.getLogger(__name__)
_INTERVAL_IN_SECONDS = 600
_EXCEPTION_TO_PASS = ["Test notification"]


class EventManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, options, raw_data):
        try:
            event_dict = {
                'event_key': 'test',
                'event_type': 'ERROR',
                'severity': 'CRITICAL',
                'resource': {},
                'description': 'test...',
                'title': 'Test for Zabbix Webhook',
                'rule': '',
                'occurred_at': datetime.now(),
                'additional_info': {}
            }

            return event_dict
        except Exception as e:
            raise ERROR_EVENT_PARSE()
