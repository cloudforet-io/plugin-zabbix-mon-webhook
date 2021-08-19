from spaceone.core.error import *


class ERROR_REQUIRED_FIELDS(ERROR_BASE):
    _message = 'Required field is missing(field= {field}'


class ERROR_EVENT_PARSE(ERROR_BASE):
    _message = 'Fail to parse the event'