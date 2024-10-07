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

def get_all_files_from_pasteleria(folder_name):
    """
    Obtiene todos los archivos de una pastelería (carpeta) y devuelve su contenido y nombre.
    """
    bucket = client.get_bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=f"{folder_name}/")  # Obtener todos los blobs en la carpeta de la pastelería

    files = []

    for blob in blobs:
        # Obtener el nombre del archivo
        file_name = blob.name.split(f"{folder_name}/")[-1]  # Extraer el nombre del archivo sin la ruta completa

        if file_name:  # Evitar entradas vacías que podrían surgir de la carpeta
            # Leer el contenido del archivo usando la función read_file
            file_data = read_file(folder_name, file_name)
            files.append(file_data)

    return files
