# MinIO Upload and Download Script

Este proyecto proporciona un script en Python para subir y descargar archivos y directorios completos a y desde un servidor MinIO Object Store. También incluye un script de instalación en Bash que configura el entorno y crea un alias para facilitar la ejecución del script desde la terminal.

## Requisitos

- Python 3
- MinIO server
- Biblioteca `minio`
- Biblioteca `python-dotenv`

## Instalación

### Paso 1: Configura el archivo `.env`

Crea un archivo `.env` en el mismo directorio que el script de Python `upload_to_minio.py`. El archivo `.env` debe contener las siguientes variables:

```dotenv
SERVER_URL=play.min.io:9000
ACCESS_KEY=Q3AM3UQ867SPQQA43P2F
SECRET_KEY=zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG
```

Asegúrate de reemplazar los valores de ejemplo con tus propias credenciales y URL del servidor MinIO.

### Paso 2: Instala las dependencias

Crea un archivo llamado requirements.txt con el siguiente contenido:

```text
minio
python-dotenv
```

Luego instala las dependencias usando pip:

```bash
pip install -r requirements.txt
```

### Paso 3: Ejecuta el script de instalación

El script de instalación copiará el script de Python y el archivo .env al directorio .conf de tu usuario y creará un alias en tu archivo .zshrc.

1. Haz ejecutable el script de instalación:

```bash
chmod +x install_script.sh
```

Ejecuta el script de instalación:

```bash
./install_script.sh
```

Esto añadirá un alias uploadminio en tu archivo .zshrc.

## Paso 4: Recarga .zshrc

Recarga tu archivo .zshrc para que el alias esté disponible de inmediato:

```bash
source ~/.zshrc
```

## Uso

### Subir un archivo

Para subir un archivo a MinIO, usa el alias uploadminio seguido del nombre del bucket y la ruta del archivo:

```bash
uploadminio my-bucket path/to/your/file.txt --prefix optional/prefix
```

### Subir un directorio

Para subir un directorio completo a MinIO, usa el alias uploadminio seguido del nombre del bucket y la ruta del directorio:

```bash
uploadminio my-bucket path/to/your/directory --prefix optional/prefix
```

### Descargar un objeto específico (última versión)

Para descargar un objeto específico, usa el alias uploadminio con la opción --download seguida del nombre del bucket, el nombre del objeto y la ruta donde se guardará el archivo:

```bash
uploadminio my-bucket path/to/save/file.txt --download --object_name object_name
```

### Descargar una versión específica de un objeto

Para descargar una versión específica de un objeto, añade la opción --version_id:

```bash
uploadminio my-bucket path/to/save/file.txt --download --object_name object_name --version_id version_id
```

### Listar versiones de un objeto

Para listar las versiones de un objeto, usa el alias uploadminio con la opción --download y el nombre del objeto:

```bash
uploadminio my-bucket path/to/save/file.txt --download --object_name object_name
```

## Ayuda

Para ver la ayuda del script y la descripción de los comandos, usa el parámetro --help:

```bash
uploadminio --help
```

El resultado será algo similar a esto:

```vbnet
usage: upload_to_minio.py [-h] [--prefix PREFIX] [--download] [--object_name OBJECT_NAME] [--version_id VERSION_ID] bucket_name file_path

Upload files or directories to MinIO Object Store or download object versions.

positional arguments:
  bucket_name           The name of the bucket in MinIO where the file or directory will be uploaded or downloaded.
  file_path             The path to the file or directory to be uploaded, or the path where the downloaded file will be saved.

optional arguments:
  -h, --help            show this help message and exit
  --prefix PREFIX       An optional prefix for the object names in MinIO when uploading.
  --download            Download mode. Specify the object name and optionally the version ID to download.
  --object_name OBJECT_NAME
                        The name of the object to be downloaded.
  --version_id VERSION_ID
                        The version ID of the object to be downloaded.
```

## Ejemplo de Uso

Subir un archivo
```bash
uploadminio my-bucket path/to/your/file.txt --prefix optional/prefix
```

Subir un directorio
```bash
uploadminio my-bucket path/to/your/directory --prefix optional/prefix
```

Descargar un objeto específico (última versión)
```bash
uploadminio my-bucket path/to/save/file.txt --download --object_name object_name
```

Descargar una versión específica de un objeto
```bash
uploadminio my-bucket path/to/save/file.txt --download --object_name object_name --version_id version_id
```

Listar versiones de un objeto
```bash
uploadminio my-bucket path/to/save/file.txt --download --object_name object_name
```

## Descripción del Script de Python

El script de Python proporciona las siguientes funcionalidades:

> upload_file_to_minio: Sube un archivo individual a MinIO.
> upload_directory_to_minio: Recorre un directorio y sube cada archivo encontrado.
> list_object_versions: Lista las versiones de un objeto en MinIO, mostrando el ID de la versión y la fecha en formato dd/mm/yyyy.
> download_object_version: Descarga una versión específica de un objeto de MinIO.

Argumentos
> bucket_name: El nombre del bucket en MinIO donde se subirá o descargará el archivo o directorio.
> file_path: La ruta al archivo o directorio a subir, o la ruta donde se guardará el archivo descargado.
> --prefix: Un prefijo opcional para los nombres de los objetos en MinIO al subir.
> --download: Modo de descarga. Especifica que deseas descargar un objeto en lugar de subir.
> --object_name: El nombre del objeto que deseas descargar.
> --version_id: El ID de la versión específica que deseas descargar.

## Contribuciones

Las contribuciones son bienvenidas. Si tienes sugerencias o mejoras, por favor crea un "pull request" o abre un "issue" en el repositorio.

## Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT.

Este documento `README.md` proporciona una guía completa sobre cómo instalar, usar y contribuir al proyecto. Incluye instrucciones detalladas para la instalación de dependencias, el uso del script para subir y descargar archivos y directorios a MinIO, y ejemplos de comandos.