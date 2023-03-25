import boto3

def lambda_handler(event, context):
    translate = boto3.client(service_name='translate', use_ssl=True)
    result = translate.translate_text(Text=event['queryStringParameters']['input_text'], SourceLanguageCode="ja", TargetLanguageCode="en").get('TranslatedText')
    return {
        'statusCode': 200,
        'body': result
    }