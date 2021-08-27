from schematics.models import Model
from schematics.types import DictType, StringType, ModelType, DateTimeType

__all__ = ['EventModel']


class ResourceModel(Model):
    resource_id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    resource_type = StringType(serialize_when_none=False)


class EventModel(Model):
    event_key = StringType(required=True)
    event_type = StringType(choices=['RECOVERY', 'ALERT', 'ERROR'], default='ALERT')
    title = StringType(required=True)
    description = StringType(default='')
    severity = StringType(choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'NOT_AVAILABLE'], default=None)
    resource = ModelType(ResourceModel)
    rule = StringType(default='')
    occurred_at = DateTimeType()
    additional_info = DictType(StringType(), default={})
