# plugin-zabbix-mon-webhook
webhook for zabbix

# Data Model

## Zabbix Raw Data
'''
 "event": {
                "status": "PROBLEM",
                "id": "7458",
                "severity": "Average",
                "date": "",
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
            "to": "xxxxx@gmail.com",
            "host": {
                "name": "bastion-dev",
                "visible_name": "bastion-dev",
                "id": "10445",
                "connection_info": "xxx.xx.x.xx",
            }
'''

## SpaceONE Event Model

| Field		| Type | Description	| Example	|
| ---      | ---     | ---           | ---           |
| event_id | str  | auto generation | event-1234556  |
| event_key | str | hash key of host.host_id, event.event_id | b5dfksdfjskfsdfklsf3423432dff |
| event_type |  str  | RECOVERY , ALERT based on raw_data.state | RECOVERY	|
| title | str	| title	| Problem: Load average is too high (per CPU load over 1.5 for 5m)	|
| description | str | message	| Problem started at 11:58:49 on 2021.08.27\r\nProblem name: Load average is too high ..	|
| severity | str  | alert level based event_status (RESOLVED, INFORMATION -> INFO, DISASTER -> CRITICAL, HIGH -> ERROR, AVERAGE -> WARNING | ERROR	|
| resource | dict | resource_id(host.id), resource_type(N/A), name(host.visible_name)	| {"resource_id":"10445", "resource_type":"", "name":"bastion-dev"}	|
| addtional_info | dict | zabbix_host_visible_name, zabbix_trigger_id, zabbix_event_id, zabbix_host_id, zabbix_item_key, zabbix_item_value| {"zabbix_host_visible_name": "bastion-dev", "zabbix_trigger_id":"10445" } |
| occured_at | datetime | webhook received time | "2021-08-23T06:47:32.753Z" |
| alert_id | str | mapped alert_id	| alert-3243434343 |
| webhook_id | str  | webhook_id	| webhook-34324234234234 |
| project_id | str	| project_id	| project-12312323232    |
| domain_id | str	| domain_id	| domain-12121212121	|
| created_at | datetime | created time | "2021-08-23T06:47:32.753Z"	|
