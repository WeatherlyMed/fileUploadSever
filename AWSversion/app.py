import os
from quart import Quart, jsonify, request
import boto3
from botocore.exceptions import NoCredentialsError

app = Quart(__name__)

S3_BUCKET = 'your-bucket-name'
AWS_ACCESS_KEY = 'your-access-key'
AWS_SECRET_KEY = 'your-secret-key'
S3_REGION = 'your-region'

s3_client = boto3.client(
    's3',
    region_name=S3_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)


# this will be posted to webpage in next version current requires personal intergration
@app.route('/generate-presigned-url', methods=['POST'])
async def generate_presigned_url():
    data = await request.json
    file_name = data.get('file_name')
    folder = data.get('folder')
    file_type = data.get('file_type')

    key = f"{folder}/{file_name}"

    try:
        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={'Bucket': S3_BUCKET, 'Key': key, 'ContentType': file_type},
            ExpiresIn=3600
        )

        return jsonify({'url': presigned_url, 'key': key})
    except NoCredentialsError:
        return jsonify({'error': 'AWS credentials not found.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
