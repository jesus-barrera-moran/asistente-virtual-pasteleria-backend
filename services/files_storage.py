from google.cloud import storage

client = storage.Client()

def read_file(bucket_name, source_blob_name):
    """Reads a file from the GCP bucket."""
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    content = blob.download_as_string()
    return {"name": source_blob_name, "content": content}

def write_file(bucket_name, destination_blob_name, content):
    """Writes a file to the GCP bucket."""
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(content)
