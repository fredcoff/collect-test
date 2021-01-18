# Collect

## Make Requests

Scheduled to run monthly.  
Generates SQS tasks and pushes to the queue.  
Read from S3.

## Get Content

Subscribed to the SQS topic.  
Get a request from SQS.  
Do request and save the result to S3.  
S3 Key: _year/month/no_

## Analyze Content

Subscribed to S3.  
Get one content from S3.  
Search keywords in the content.  
Add a result record to DynamoDB.

```json
{
    "id": "uuid",
    "url": "https://example.xn--com-9o0a",
    "status": "404",
    "content": "s3 key",
    "tags": "CMBS, loans",
    "lastUpdate": "date"
}
```

## Export to CSV

`collect/export`

## Update Emails

`update/emails`

```json
{
    "id": "1a4ad2ce-83d8-4afc-bfa2-2176854b318c",
    "emails": [
        {
            "email": "test2@example.com",
            "primary": "true",
            "type": "business"
        }
    ]
}
```

## Query DB

`search`

| Parameter          | Description                             | e.g.                                   |
| :----------------- | :-------------------------------------- | :------------------------------------- |
| `size`             | number of results needed                | `5`                                    |
| `from`             | search past this item (`id` of an item) | `3e112294-9bcf-49d9-9aa3-9ab5b3946edd` |
| `query/conditions` | conditions                              |                                        |

Condition details

| Name      | Description                                                                                      |
| :-------- | :----------------------------------------------------------------------------------------------- |
| `field`   | field name (`sourceCreateTimestamp`/`sourceModifyTimestamp`/`createTimestamp`/`modifyTimestamp`) |
| `op`      | operator (`gt`/`gte`/`lt`/`lte`)                                                                 |
| `value`   | value (e.g. `field` op `value`)                                                                  |
| `opmerge` | merge operator (`and`/`or`)                                                                      |

_Notes about merging_
_Merge operators are applied one by one from the first to last. `a or b and c` becomes `(a or b) and c`._

```json
// request
{
    "size": 3,
    "query": {
        "conditions": [
            {
                "field": "sourceCreateTimestamp",
                "op": "gt",
                "value": "2020-09-10"
            },
            {
                "field": "sourceCreateTimestamp",
                "op": "lt",
                "value": "2020-11-10",
                "opmerge": "or"
            }
        ]
    }
}

// response
{
    "count": 3,
    "result": [
        {
            "id": "3e112294-9bcf-49d9-9aa3-9ab5b3946edd",
            "content": "2020/6/3",
            "lastUpdate": "06/04/2020, 00:08:42",
            "status": 404,
            "url": "https://www.hklaw.com/en/professionals/s/stansbury-john-l",
            "tags": null,
            "emails": null,
            "sourceCreateTimestamp": "2021-02-10",
            "sourceModifyTimestamp": "2021-02-11",
            "createTimestamp": null,
            "modifyTimestamp": null
        },
        {
            "id": "3332db67-ebf2-4581-b366-910bf82a47ba",
            "content": "2020/11/1",
            "lastUpdate": "11/01/2020, 11:00:41",
            "status": 200,
            "url": "https://www.hklaw.com/en/professionals/d/driscoll-allison-k",
            "tags": "acquisition,acquisitions,CMBS,commercial,commercial real estate,complex commercial real estate finance transactions,finance,financing,financing transactions,hospitality,mezzanine loans,owners,securitizations,transactions,workouts",
            "emails": [],
            "sourceCreateTimestamp": "2021-01-10",
            "sourceModifyTimestamp": "2021-01-11",
            "createTimestamp": null,
            "modifyTimestamp": null
        },
        {
            "id": "1dc16f09-aaf2-45dc-9bfe-4c910e4d1373",
            "content": "2021/1/2",
            "lastUpdate": "01/01/2021, 11:00:41",
            "status": 200,
            "url": "https://www.hklaw.com/en/professionals/n/nolan-jeffrey-james",
            "tags": null,
            "emails": [],
            "sourceCreateTimestamp": "2020-10-10",
            "sourceModifyTimestamp": "2020-10-11",
            "createTimestamp": null,
            "modifyTimestamp": null
        }
    ],
    "last_id": "1dc16f09-aaf2-45dc-9bfe-4c910e4d1373"
}
```

```json
// request
{
    "from": "1dc16f09-aaf2-45dc-9bfe-4c910e4d1373",
    "size": 3,
    "query": {
        "conditions": [
            {
                "field": "sourceCreateTimestamp",
                "op": "gt",
                "value": "2020-09-10"
            },
            {
                "field": "sourceCreateTimestamp",
                "op": "lt",
                "value": "2020-11-10",
                "opmerge": "or"
            }
        ]
    }
}

// response
{
    "count": 3,
    "result": [
        {
            "id": "3129eddd-7702-49f4-8a2d-3c1eee960a9e",
            "content": "2020/10/5",
            "lastUpdate": "10/01/2020, 11:00:14",
            "status": 200,
            "url": "https://www.hklaw.com/en/professionals/c/covitt-renee-i",
            "tags": "acquisition,CMBS,commercial,Commercial Real Estate,complex real estate transactions,finance,financing,hospitality,owners,real estate matters,real estate transactions,real estate transactions,representation of owners,transactions",
            "emails": null,
            "sourceCreateTimestamp": "2020-12-10",
            "sourceModifyTimestamp": "2020-12-11",
            "createTimestamp": null,
            "modifyTimestamp": null
        },
        {
            "id": "1a4ad2ce-83d8-4afc-bfa2-2176854b318c",
            "content": "2020/10/3",
            "lastUpdate": "10/01/2020, 11:00:14",
            "status": 200,
            "url": "https://www.hklaw.com/en/professionals/s/stansbury-john-l",
            "tags": null,
            "emails": [
                {
                    "email": "test2@example.com",
                    "primary": true,
                    "email_type": "personal"
                }
            ],
            "sourceCreateTimestamp": "2020-09-10",
            "sourceModifyTimestamp": "2020-09-11",
            "createTimestamp": null,
            "modifyTimestamp": null
        },
        {
            "id": "234c7a5f-1d12-4bbd-82fb-da4e022b44ce",
            "content": "2020/11/5",
            "lastUpdate": "11/01/2020, 11:00:14",
            "status": 200,
            "url": "https://www.hklaw.com/en/professionals/c/covitt-renee-i",
            "tags": "acquisition,CMBS,commercial,Commercial Real Estate,complex real estate transactions,finance,financing,hospitality,owners,real estate matters,real estate transactions,real estate transactions,representation of owners,transactions",
            "emails": [],
            "sourceCreateTimestamp": "2020-11-10",
            "sourceModifyTimestamp": "2020-11-11",
            "createTimestamp": null,
            "modifyTimestamp": null
        }
    ],
    "last_id": "234c7a5f-1d12-4bbd-82fb-da4e022b44ce"
}
```

```json
// request
{
    "from": "234c7a5f-1d12-4bbd-82fb-da4e022b44ce",
    "size": 3,
    "query": {
        "conditions": [
            {
                "field": "sourceCreateTimestamp",
                "op": "gt",
                "value": "2020-09-10"
            },
            {
                "field": "sourceCreateTimestamp",
                "op": "lt",
                "value": "2020-11-10",
                "opmerge": "or"
            }
        ]
    }
}

// response
{
    "count": 0,
    "result": [],
    "last_id": null
}
```

## Prerequisites

Created a SQS queue, a DynamoDB table, a S3 bucket and required files in S3.  
Created a [scraperapi](https://www.scraperapi.com/) account.

| Key                  | Description            | e.g.                                                         |
| :------------------- | :--------------------- | :----------------------------------------------------------- |
| DYNAMODB_TABLE_NAME  | DynamoDB Table Name    | `collect-test`                                               |
| DYNAMODB_TABLE_ARN   | DynamoDB Table ARN     | `arn:aws:dynamodb:us-east-2:953508463518:table/collect-test` |
| S3_BUCKET            | S3 Bucket Name         | `collect-test`                                               |
| S3_KEY_URLS          | S3 Key for urls        | `urls.csv`                                                   |
| S3_KEY_KEYWORDS      | S3 Key for keywords    | `keywords.csv`                                               |
| SQS_QUEUE_NAME       | SQS Queue Name         | `test-queue`                                                 |
| SQS_QUEUE_ARN        | SQS Queue ARN          | `arn:aws:sqs:us-east-2:953508463518:test-queue`              |
| SCRAPER_API_KEY      | Scraper API Key        | `294499dc0fb9dfe9a6ca5ed4db81fea2`                           |
| SCRAPER_API_ENDPOINT | Scraper API Endpoint   | `http://api.scraperapi.com`                                  |
| HEADERS              | CSV Headers for Export | `content,id,url,lastUpdate,tags,status`                      |

## Development & Deployment

### Environment

-   [serverless](https://www.serverless.com/framework/docs/getting-started#via-npm)
-   [NPM](https://nodejs.org/en/download/package-manager/)
-   [Python](https://www.python.org/)
-   [Docker](https://www.docker.com/)

### Development

-   Create python virtual environment.
-   Set environment variables. A good practice is to insert commands in file `activate` in virtual environment. Exact filename can vary according to OS.
-   Run `pip install -r requirements.txt` to install dependencies.
-   Run `pip install boto3` to install `boto3`. It's not included in `requirements.txt` because it's built-in in AWS Python Lambda environment.
-   Run `npm install` to install _serverless_ plugins.
-   Run scripts, e.g. `python src/update_emails.py`

    _If you encounter `ModuleNotFoundError: No module named '__main__.common'; '__main__' is not a package`, please use relative imports for modules. (`common` and `constants`)_

### Deployment

-   `serverless deploy`

    _If you encounter `TypeError: this.awsPackagePlugin.validateStatements is not a function`, run `npm i serverless-iam-roles-per-function@next`._
