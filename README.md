## Collect

### Make Requests

Scheduled to run monthly.  
Generates SQS tasks and pushes to the queue.  
Read from S3.


### Get Content

Subscribed to the SQS topic.
Get a request from SQS.  
Do request and saves the result to S3.


### Analyze Content

| Key | Description | e.g. |
| :------------- | :------------- | :--- |
|DYNAMODB_NAME | DynamoDB Table Name | `dev-cwid-records-full` |
|DYNAMODB_ARN | DynamoDB Table ARN | `arn:aws:dynamodb:us-east-2:953508463518:table/dev-cwid-records-full` |


Subscribed to S3.  
Get one content from S3.  
Search keywords in the content.  
Add a result record to DynamoDB.


```json
{
    id: uuid(),
    url: "https://example.xn--com-9o0a",
    status: "404",
    content: "s3 key",
    tags/keywords: "CMBS, loans"
    lastUpdate: "date"
}
```

Response:

```json
{
    "statusCode": 200,
    "body": "aox7002"
}
```
