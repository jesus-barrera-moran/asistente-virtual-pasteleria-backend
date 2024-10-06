from google.cloud import storage

client = storage.Client()

bucket_name = "asistentes-virtuales-pastelerias-documentos-bucket"

def read_file(folder_name, source_blob_name):
    bucket = client.get_bucket(bucket_name)
    # Concatenar el nombre de la carpeta y el archivo para crear una jerarquía de carpetas
    blob_name = f"{folder_name}/{source_blob_name}"
    blob = bucket.blob(blob_name)

    # Verificar si el blob existe
    if not blob.exists():
        return {"name": source_blob_name, "content": ""}
    
    # Descargar el contenido como una cadena de texto
    content = blob.download_as_string()
    return {"name": source_blob_name, "content": content}

def write_file(folder_name, destination_blob_name, content):
    """Writes a file to the GCP bucket within a 'folder'."""
    bucket = client.get_bucket(bucket_name)
    # Concatenar el nombre de la carpeta y el archivo para simular una estructura de carpetas
    blob_name = f"{folder_name}/{destination_blob_name}"
    blob = bucket.blob(blob_name)
    # Subir el contenido
    blob.upload_from_string(content)
    print(f"File {destination_blob_name} uploaded to folder {folder_name} in bucket {bucket_name}.")
