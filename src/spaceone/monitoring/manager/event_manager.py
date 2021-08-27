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

    def parse(self, options, data):
        """ data sample
            "event": {
                "status": "PROBLEM",
                "recovery_id": "{EVENT.RECOVERY.ID}",
                "id": "7458",
                "severity": "Average",
                "recovery_name": "{EVENT.RECOVERY.NAME} \u200b \u200b",
                "name": "Load average is too high (per CPU load over 1.5 for 5m)"
            },
            "item": {
                "value": "2",
                "id": "42529",
                "key": "system.cpu.load[all,avg1]"
            },
            "message": "Problem started at 11:58:49 on 2021.08.27\r\nProblem name: Load average is too high (per CPU load over 1.5 for 5m)\r\nHost: zabbix-test\r\nSeverity: Average\r\nOperational data: Load averages(1m 5m 15m): (2 1.66 1.67), # of CPUs: 1\r\nOriginal problem ID: 7458\r\n",
            "trigger": {
                "name": "Load average is too high (per CPU load over 1.5 for 5m)",
                "severity": "Average",
                "id": "21028",
                "status": "PROBLEM"
            },
            "title": "Problem: Load average is too high (per CPU load over 1.5 for 5m)",
            "to": "bluese05@gmail.com",
            "host": {
                "description": "",
                "name": "bastion-dev",
                "visible_name": "bastion-dev",
                "id": "10445",
                "connection_info": "172.16.2.66",
                "dns": ""
            }
        """

        try:
            event_status = data.get('event', {}).get('status')
            event_severity = data.get('event', {}).get('severity')

            event_dict = {
                'event_key': self._generate_event_key(data.get('event', {}), data.get('host', {})),
                'event_type': self._get_event_type(event_status),
                'severity': self._get_severity(event_severity, event_status),
                'resource': {
                    'resource_id': data.get('host', {}).get('name', ''),
                    'resource_type': '',
                    'name': self._get_resource_name(data.get('host', {}))
                },
                'description': data.get('message', ''),
                'title': data.get('title', ''),
                'rule': data.get('trigger', {}).get('name', ''),
                'occurred_at': datetime.now(),
                'additional_info': {}
            }

            event_model = EventModel(event_dict, strict=False)
            event_model.validate()
            return [event_model.to_native()]

        except Exception as e:
            raise ERROR_EVENT_PARSE()

    @staticmethod
    def _generate_event_key(event_info, host_info):
        host_id = host_info.get('id')
        event_id = event_info.get('id')

        raw_event_key = f'{host_id}:{event_id}'
        hash_object = hashlib.md5(raw_event_key.encode())
        md5_hash = hash_object.hexdigest()

        return md5_hash

    @staticmethod
    def _get_event_type(event_status):
        if event_status.upper() == 'RESOLVED':
            return 'RECOVERY'
        else:
            return 'ALERT'

    @staticmethod
    def _get_severity(event_severity, event_status):
        _status = event_status.upper()
        _severity = event_severity.upper()

        if _status == 'RESOLVED':
            return 'INFO'
        elif _severity == 'DISASTER':
            return 'CRITICAL'
        elif _severity == 'HIGH':
            return 'ERROR'
        elif _severity == 'AVERAGE':
            return 'WARNING'
        elif _severity == 'INFORMATION':
            return 'INFO'
        else:
            return None

    @staticmethod
    def _get_resource_name(host_info):
        resource_name = host_info.get('name', '')

        if conn := host_info.get('connection_info'):
            resource_name = f'{resource_name} ({conn})'

        return resource_name
