#!/bin/bash

# Directorio de instalación
INSTALL_DIR="$HOME/.config"
SCRIPT_NAME="upload_to_minio.py"
PYTHON_FILES="*.py"
ENV_FILE=".env"
ALIAS_NAME="upmin"
SCRIPT_PATH="$INSTALL_DIR/$ALIAS_NAME/$SCRIPT_NAME"

# Crear el directorio de instalación si no existe
mkdir -p "$INSTALL_DIR/$ALIAS_NAME"

# Copiar el script de Python y el archivo .env al directorio de instalación
cp $PYTHON_FILES "$INSTALL_DIR/$ALIAS_NAME/"
cp $ENV_FILE "$INSTALL_DIR/$ALIAS_NAME/$ENV_FILE"

# Añadir el alias a .zshrc
ZSHRC="$HOME/.zshrc"

# Instalación de Dependencias con pip
pip install -r requirements.txt --break-system-packages

# Verificar si el alias ya existe y agregarlo si no está presente
if ! grep -q "alias $ALIAS_NAME=" "$ZSHRC"; then
    echo "alias $ALIAS_NAME='python3 $SCRIPT_PATH'" >>"$ZSHRC"
    echo "Alias $ALIAS_NAME added to $ZSHRC"
else
    echo "Alias $ALIAS_NAME already exists in $ZSHRC"
fi

# Recargar .zshrc para que el alias esté disponible de inmediato
source "$ZSHRC"

echo "Installation complete. You can now use the alias '$ALIAS_NAME' to run the script."
