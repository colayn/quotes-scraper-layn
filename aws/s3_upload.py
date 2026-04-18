import boto3


def upload_to_s3(file_path: str, bucket_name: str, object_name: str):
    """
    Upload a file to AWS S3 bucket
    """

    try:
        s3 = boto3.client("s3")

        s3.upload_file(
            Filename=file_path,
            Bucket=bucket_name,
            Key=object_name
        )

        print("\n====================")
        print("UPLOAD SUCCESS")
        print(f"s3://{bucket_name}/{object_name}")
        print("====================\n")

    except Exception as e:
        print("S3 Upload Failed:", str(e))