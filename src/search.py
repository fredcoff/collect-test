try:
    import unzip_requirements
except ImportError:
    pass

import sys
import json
from .common import ResultModel, EmailMap
from .constants import DEFAULT_SIZE


def get_field(field):
    if field == "sourceCreateTimestamp":
        return ResultModel.sourceCreateTimestamp
    if field == "sourceModifyTimestamp":
        return ResultModel.sourceModifyTimestamp
    if field == "createTimestamp":
        return ResultModel.createTimestamp
    if field == "modifyTimestamp":
        return ResultModel.modifyTimestamp
    raise NameError(f"Unknown field - {field}")


def get_condition(condition):
    field = get_field(condition["field"])
    op = condition["op"]
    if op == "gt":
        return field > condition["value"]
    if op == "gte":
        return field >= condition["value"]
    if op == "lt":
        return field < condition["value"]
    if op == "lte":
        return field <= condition["value"]
    raise NameError(f"Unknown operator - {op}")


def merge_conditions(a, b, opmerge):
    if opmerge == "or":
        return a | b
    if opmerge == "and":
        return a & b
    raise NameError(f"Unknown operator for merge - {opmerge}")


def serialize_emails(emails):
    if emails is None:
        return None

    ret = []
    for email in emails:
        ret.append({
            "email": email.email,
            "primary": email.primary,
            "email_type": email.email_type
        })
    return ret


def handle(event, context):

    req = json.loads(event["body"])

    last_id = req.get("from")
    size = req.get("size", DEFAULT_SIZE)

    conditions = req["query"]["conditions"]

    try:
        filter_condition = None
        if len(conditions) > 0:
            filter_condition = get_condition(conditions[0])
            for condition in conditions[1:]:
                tmp = get_condition(condition)
                filter_condition = merge_conditions(
                    filter_condition, tmp, condition["opmerge"])

            if last_id:
                result = ResultModel.scan(filter_condition, limit=size, last_evaluated_key={
                                          "id": {"S": last_id}})
            else:
                result = ResultModel.scan(filter_condition, limit=size)

        else:
            if last_id:
                result = ResultModel.scan(limit=size, last_evaluated_key={
                                          "id": {"S": last_id}})
            else:
                result = ResultModel.scan(limit=size)

        ret = []
        for item in result:
            ret.append({
                "id": item.id,
                "content": item.content,
                "lastUpdate": item.lastUpdate,
                "status": item.status,
                "url": item.url,
                "tags": item.tags,
                "emails": serialize_emails(item.emails),
                "sourceCreateTimestamp": item.sourceCreateTimestamp,
                "sourceModifyTimestamp": item.sourceModifyTimestamp,
                "createTimestamp": item.createTimestamp,
                "modifyTimestamp": item.modifyTimestamp,
            })

        if len(ret) > 0:
            last_id = ret[-1]["id"]
        else:
            last_id = None

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True
            },
            "body": json.dumps({
                "count": len(ret),
                "result": ret,
                "last_id": last_id
            })
        }
    except:
        exc, exc_val, trace = sys.exc_info()
        print(exc, exc_val, trace)
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True
            },
            "body": str(exc_val)
        }


if __name__ == "__main__":
    print(
        handle(
            {
                "body": json.dumps({
                    "from": "1dc16f09-aaf2-45dc-9bfe-4c910e4d1373",
                    "size": 3,
                    "query": {
                        "conditions": [
                            {
                                "field": "sourceCreateTimestamp",
                                "op": "gt",
                                "value": "2020-12-10"
                            },
                            {
                                "field": "sourceModifyTimestamp",
                                "op": "lte",
                                "value": "2020-11-10",
                                "opmerge": "or"
                            }
                        ]
                    }
                })
            },
            None,
        )
    )
