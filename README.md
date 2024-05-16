# MinIO Upload Script

Este proyecto proporciona un script en Python para subir archivos y directorios completos a un servidor MinIO Object Store. También incluye un script de instalación en Bash que configura el entorno y crea un alias para facilitar la ejecución del script desde la terminal.

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

> Asegúrate de reemplazar los valores de ejemplo con tus propias credenciales y URL del servidor MinIO.

### Paso 2: Ejecuta el script de instalación

El script de instalación copiará el script de Python y el archivo .env al directorio .conf de tu usuario y creará un alias en tu archivo .zshrc.

1. Haz ejecutable el script de instalación:

```bash
chmod +x install.sh
```

2. Ejecuta el script de instalación:
```bash
./install.sh
```
> Esto añadirá un alias uploadminio en tu archivo .zshrc.

### Paso 3: Recarga .zshrc

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

### Ayuda

Para ver la ayuda del script y la descripción de los comandos, usa el parámetro --help:

```bash
uploadminio --help
```

## Ejemplo de uso

```bash
uploadminio my-bucket /home/user/documents --prefix docs
```
Esto subirá todos los archivos dentro del directorio documents al bucket my-bucket en MinIO, con el prefijo docs.

## Descripción del Script de Python

El script de Python proporciona las siguientes funcionalidades:

* upload_file_to_minio: Sube un archivo individual a MinIO.
* upload_directory_to_minio: Recorre un directorio y sube cada archivo encontrado.
    * Argumentos:
        - bucket_name: El nombre del bucket en MinIO.
        - file_path: La ruta al archivo o directorio a subir.
        - --prefix: Un prefijo opcional para los nombres de los objetos en MinIO.

## Contribuciones

Las contribuciones son bienvenidas. Si tienes sugerencias o mejoras, por favor crea un "pull request" o abre un "issue" en el repositorio.

Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT.
