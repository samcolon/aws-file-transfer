import json
import boto3
import os

s3 = boto3.client('s3')

def decrypt_file(file_content):
    # Mock decryption function (reverses content)
    decrypted_content = file_content[::-1]  # Reverse content for testing

    # Append the decryption message at the end
    decryption_message = "\n I Decrypted this - Samuel Colon\n"
    decrypted_content += decryption_message.encode('utf-8')

    return decrypted_content

def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event, indent=2))

        # Extract bucket name and object key from event
        bucket_name = event["detail"]["bucket"]["name"]
        object_key = event["detail"]["object"]["key"]

        print(f"Processing file: {object_key} from bucket: {bucket_name}")

        # Download the file
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        file_content = response['Body'].read()

        print("File downloaded successfully.")

        # Decrypt the file
        decrypted_content = decrypt_file(file_content)

        print("File decrypted successfully.")

        # Save the decrypted file in the `decrypted/` folder inside the same bucket
        new_key = f"decrypted/{object_key}"
        s3.put_object(Bucket=bucket_name, Key=new_key, Body=decrypted_content)

        print(f"Decrypted file saved at: {new_key}")

        return {
            "statusCode": 200,
            "body": json.dumps(f"Decrypted file saved at {new_key}")
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps(str(e))
        }
