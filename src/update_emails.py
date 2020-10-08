try:
    import unzip_requirements
except ImportError:
    pass

import sys
import json
from common import ResultModel, EmailMap


def handle(event, context):

    req = json.loads(event["body"])

    try:
        result = ResultModel.get(req["id"])
        emails = result.emails
        if emails is None:
            emails = []
        
        idxs = {}
        for item, i in zip(emails, range(len(emails))):
            idxs[item.email] = i
        
        for item in req["emails"]:
            if item["email"] in idxs.keys():
                i = idxs[item["email"]]
                
                primary = item.get("primary", emails[i].primary)
                if primary == "true" or primary == "True" or primary == "1":
                    emails[i].primary = True
                else:
                    emails[i].primary = False

                emails[i].email_type = item.get("type", emails[i].email_type)
            else:
                emails.append(
                    EmailMap(
                        email=item["email"],
                        primary=item.get("primary", False),
                        email_type=item.get("type", "")
                    )
                )
        
        result.emails = emails
        result.save()

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True
            },
            "body": "success"
        }
    except:
        exc, exc_val, trace = sys.exc_info()
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True
            },
            "body": str(exc_val)
        }

if __name__ == "__main__":
    print (
        handle(
            {
                "body": json.dumps({
                    "id": "1a4ad2ce-83d8-4afc-bfa2-2176854b318c",
                    "emails": [
                        {
                            "email": "test2@example.com",
                            "primary": False,
                            "type": "business"
                        },
                    ]
                })
            }, 
            None,
        )
    )
