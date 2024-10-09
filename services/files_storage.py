import os  # Importar para usar os.path.splitext
from google.cloud import storage

client = storage.Client()

documents_bucket_name = "asistentes-virtuales-pastelerias-documentos-bucket"
images_bucket_name = "asistentes-virtuales-pastelerias-imagenes-bucket"

def read_file(folder_name, source_blob_name):
    bucket = client.get_bucket(documents_bucket_name)
    # Concatenar el nombre de la carpeta y el archivo para crear una jerarquía de carpetas
    blob_name = f"{folder_name}/{source_blob_name}"
    blob = bucket.blob(blob_name)

    # Verificar si el blob existe
    if not blob.exists():
        return {"name": source_blob_name, "content": ""}
    
    # Descargar el contenido como una cadena de texto
    content = blob.download_as_string()
    return {"name": source_blob_name, "content": content}

def write_file(folder_name, destination_blob_name, content, isImage=False):
    """Writes a file to the GCP bucket within a 'folder'."""
    bucket_name = images_bucket_name if isImage else documents_bucket_name
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
    bucket = client.get_bucket(documents_bucket_name)
    blobs = bucket.list_blobs(prefix=f"{folder_name}/")  # Obtener todos los blobs en la carpeta de la pastelería

    files = []

    for blob in blobs:
        # Obtener el nombre del archivo
        file_name = blob.name.split(f"{folder_name}/")[-1]  # Extraer el nombre del archivo sin la ruta completa

        if file_name:  # Evitar entradas vacías que podrían surgir de la carpeta
            # Eliminar la extensión del archivo
            file_name_without_extension = os.path.splitext(file_name)[0]

            # Leer el contenido del archivo usando la función read_file
            file_data = read_file(folder_name, file_name)
            
            # Reemplazar el nombre con el nombre sin la extensión
            file_data["name"] = file_name_without_extension

            files.append(file_data)

    return files

def get_public_image_urls_from_pasteleria(folder_name: str):
    """
    Obtiene todas las URLs públicas de las imágenes almacenadas para una pastelería en la bucket de imágenes.
    Devuelve una lista de diccionarios con el nombre del archivo (sin extensión) y su URL pública.
    """
    bucket = client.get_bucket(images_bucket_name)
    blobs = bucket.list_blobs(prefix=f"{folder_name}/")  # Obtener todos los blobs en la carpeta de la pastelería

    image_urls = []

    for blob in blobs:
        # Verificar si el archivo tiene un nombre válido
        if blob.name:
            # Construir la URL pública manualmente
            public_url = f"https://storage.googleapis.com/{bucket.name}/{blob.name}"
            
            # Extraer el nombre del archivo sin la carpeta
            file_name_with_extension = blob.name.split("/")[-1]
            
            # Quitar la extensión del nombre del archivo
            file_name = os.path.splitext(file_name_with_extension)[0]
            
            # Agregar el nombre del archivo (sin extensión) y la URL a la lista
            image_urls.append({
                "file_name": file_name,
                "url": public_url
            })

    return image_urls
