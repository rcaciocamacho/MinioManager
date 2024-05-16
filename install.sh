#!/bin/bash

# Directorio de instalación
INSTALL_DIR="$HOME/.conf"
SCRIPT_NAME="upload_to_minio.py"
ENV_FILE=".env"
SCRIPT_PATH="$INSTALL_DIR/$SCRIPT_NAME"
ENV_PATH="$INSTALL_DIR/$ENV_FILE"
ALIAS_NAME="upmin"

# Crear el directorio de instalación si no existe
mkdir -p "$INSTALL_DIR"

# Copiar el script de Python y el archivo .env al directorio de instalación
cp "$SCRIPT_NAME" "$SCRIPT_PATH"
cp "$ENV_FILE" "$ENV_PATH"

# Añadir el alias a .zshrc
ZSHRC="$HOME/.zshrc"

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
