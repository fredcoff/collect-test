# Collect


## Make Requests

Scheduled to run monthly.  
Generates SQS tasks and pushes to the queue.  
Read from S3.



## Get Content

Subscribed to the SQS topic.  
Get a request from SQS.  
Do request and save the result to S3.  
S3 Key: *year/month/no*



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
        },
    ]
}
```

## Prerequisites

Created a SQS queue, a DynamoDB table, a S3 bucket and required files in S3.  
Created a [scraperapi](https://www.scraperapi.com/) account.  


| Key | Description | e.g. |
| :------------- | :------------- | :--- |
|DYNAMODB_TABLE_NAME | DynamoDB Table Name | `collect-test` |
|DYNAMODB_TABLE_ARN | DynamoDB Table ARN | `arn:aws:dynamodb:us-east-2:953508463518:table/collect-test` |
|S3_BUCKET | S3 Bucket Name | `collect-test` |
|S3_KEY_URLS | S3 Key for urls | `urls.csv` |
|S3_KEY_KEYWORDS | S3 Key for keywords | `keywords.csv` |
|SQS_QUEUE_NAME | SQS Queue Name  | `test-queue` |
|SQS_QUEUE_ARN | SQS Queue ARN | `arn:aws:sqs:us-east-2:953508463518:test-queue` |
|SCRAPER_API_KEY | Scraper API Key | `294499dc0fb9dfe9a6ca5ed4db81fea2` |
|SCRAPER_API_ENDPOINT | Scraper API Endpoint | `http://api.scraperapi.com` |
|HEADERS | CSV Headers for Export | `content,id,url,lastUpdate,tags,status` |


## Development & Deployment

### Environment
- [serverless](https://www.serverless.com/framework/docs/getting-started#via-npm)
- [NPM](https://nodejs.org/en/download/package-manager/)
- [Python](https://www.python.org/)
- [Docker](https://www.docker.com/)

### Development
- Create python virtual environment.
- Set environment variables. A good practice is to insert commands in file `activate` in virtual environment. Exact filename can vary according to OS.
- Run `pip install -r requirements.txt` to install dependencies.
- Run `pip install boto3` to install `boto3`. It's not included in `requirements.txt` because it's built-in in AWS Python Lambda environment.
- Run `npm install` to install *serverless* plugins.
- Run scripts, e.g. `python src/update_emails.py`
  
  *If you encounter `ModuleNotFoundError: No module named '__main__.common'; '__main__' is not a package`, please use relative imports for modules. (`common` and `constants`)*

### Deployment
- `serverless deploy`

    *If you encounter `TypeError: this.awsPackagePlugin.validateStatements is not a function`, run `npm i serverless-iam-roles-per-function@next`.*