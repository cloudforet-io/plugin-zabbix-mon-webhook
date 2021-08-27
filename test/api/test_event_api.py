import logging
import unittest
import os
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.tester import TestCase, print_json

_LOGGER = logging.getLogger(__name__)
TEST_JSON = os.environ.get('test_json', None)


class TestEvent(TestCase):

    def test_parse(self):
        params = {
            "options": {

            },
            "data": {
                "to": "abc@localhost.net",
		        "event": {
                    "name": "Load average is too high (per CPU load over 1.5 for 5m)",
                    "recovery_id": "{EVENT.RECOVERY.ID}",
                    "id": "7467",
                    "severity": "Average",
                    "recovery_name": "{EVENT.RECOVERY.NAME}",
                    "status": "PROBLEM"
                },
                "message": "Problem started at 12:51:50 on 2021.08.27\r\nProblem name: Load average is too high (per CPU load over 1.5 for 5m)\r\nHost: zabbix-test\r\nSeverity: Average\r\nOperational data: Load averages(1m 5m 15m): (1.69 1.39 1.01), # of CPUs: 1\r\nOriginal problem ID: 7467\r\n",
                "title": "Problem: Load average is too high (per CPU load over 1.5 for 5m)",
                "item": {
                    "key": "system.cpu.load[all,avg1]",
                    "id": "42529",
                    "value": "1.69"
                },
                "host": {
                    "name": "zabbix-test",
                    "description": "",
                    "dns": "",
                    "connection_info": "172.31.4.239",
                    "id": "10490",
                    "visible_name": "zabbix-test"
                },
                "trigger": {
                    "severity": "Average",
                    "name": "Load average is too high (per CPU load over 1.5 for 5m)",
                    "status": "PROBLEM",
                    "id": "21028"
                }
            }
        }

        test_cases = [params]

        for idx, test_case in enumerate(test_cases):
            print(f'###### {idx} ########')
            parsed_data = self.monitoring.Event.parse({'options': {}, 'data': test_case.get('data')})
            print_json(parsed_data)
            print()



if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
