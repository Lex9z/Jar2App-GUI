### README.md

---
[Creador de Aplicaciones macOS en Java](#creador-de-aplicaciones-macos-en-java)

# macOS Java Application Creator

This tool allows you to convert a Java JAR file into a macOS `.app` application bundle. Optionally, it can also create a `.dmg` disk image for distribution.

---

## Table of Contents

1. [Features](#features)
2. [Dependencies](#dependencies)
3. [How to Use](#how-to-use)
4. [GUI Instructions](#gui-instructions)
5. [Command-Line Usage (Optional)](#command-line-usage-optional)
6. [License](#license)

---

## Features

- Converts a `.jar` file into a macOS `.app` application.
- Automatically detects the `Main-Class` and version from the JAR manifest.
- Supports custom icons (`.icns`) for the application.
- Optionally creates a `.dmg` disk image for easy distribution.
- Provides a graphical user interface (GUI) for ease of use.

---

## Dependencies

### Required:

1. **Python 3.x**: The script is written in Python and requires Python 3 or higher.
   - Install Python: https://www.python.org/downloads/
2. **universalJavaApplicationStub**:
   - This script uses the `universalJavaApplicationStub` to launch the Java application.
   - Place the `universalJavaApplicationStub` file in a folder named `datafiles` in the same directory as the script.
   - Download it from: https://github.com/tofi86/universalJavaApplicationStub
3. **hdiutil** (for `.dmg` creation):
   - This is a built-in macOS utility. No additional installation is required if you're on macOS.

### Optional:

- A `.icns` icon file for your application (if you want a custom icon).

---

## How to Use

### GUI Instructions

1. **Download the Script**:
   - Clone or download this repository to your local machine.

2. **Prepare Your Files**:
   - Ensure you have a `.jar` file ready.
   - Optionally, prepare an `.icns` icon file for your application.

3. **Run the Script**:
   - Open a terminal and navigate to the directory containing the script.
   - Run the script using the following command:
     ```bash
     python3 jar2app-gui.py
     ```

4. **Use the GUI**:
   - Fill in the required fields:
     - **JAR File**: Select your `.jar` file.
     - **Version**: Enter the application version (or leave blank to auto-detect).
     - **SDK Version**: Enter the JDK version required by your app (optional).
     - **Output Directory**: Choose where the `.app` will be created.
     - **Icon File**: Select an `.icns` file for the app icon (optional).
   - Check the box "Create .dmg" if you want to generate a disk image.
   - Click "Create Application" to generate the `.app` and optionally the `.dmg`.

5. **Locate the Output**:
   - The `.app` will be created in the specified output directory.
   - If you selected the `.dmg` option, the `.dmg` file will also be created in the same directory.

---

## Command-Line Usage (Optional)

If you prefer using the command line, you can run the script without the GUI. Here's how:

```bash
python3 jar2app.py \
    -jar /path/to/your/app.jar \
    -version 1.0.0 \
    -sdk 21 \
    -output /path/to/output/directory \
    -icon /path/to/icon.icns
```

Arguments:
- `-jar`: Path to the JAR file (required).
- `-version`: Application version (optional, defaults to `1.0.0` or detected from the manifest).
- `-sdk`: JDK version required by the app (optional).
- `-output`: Directory where the `.app` will be created (defaults to the current directory).
- `-icon`: Path to the `.icns` icon file (optional).

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

---

# Creador de Aplicaciones macOS en Java

Esta herramienta permite convertir un archivo JAR de Java en una aplicación macOS `.app`. Opcionalmente, también puede crear un archivo `.dmg` para distribución.

---

## Tabla de Contenidos

1. [Características](#características)
2. [Dependencias](#dependencias)
3. [Cómo Usar](#cómo-usar)
4. [Instrucciones de la GUI](#instrucciones-de-la-gui)
5. [Uso de Línea de Comandos (Opcional)](#uso-de-línea-de-comandos-opcional)
6. [Licencia](#licencia)

---

## Características

- Convierte un archivo `.jar` en una aplicación macOS `.app`.
- Detecta automáticamente la `Main-Class` y la versión del manifiesto del JAR.
- Soporta íconos personalizados (`.icns`) para la aplicación.
- Opcionalmente crea un archivo `.dmg` para facilitar la distribución.
- Proporciona una interfaz gráfica de usuario (GUI) para facilitar el uso.

---

## Dependencias

### Requeridas:

1. **Python 3.x**: El script está escrito en Python y requiere Python 3 o superior.
   - Instala Python: https://www.python.org/downloads/
2. **universalJavaApplicationStub**:
   - Este script utiliza `universalJavaApplicationStub` para lanzar la aplicación Java.
   - Coloca el archivo `universalJavaApplicationStub` en una carpeta llamada `datafiles` en el mismo directorio que el script.
   - Descárgalo desde: https://github.com/tofi86/universalJavaApplicationStub
3. **hdiutil** (para la creación de `.dmg`):
   - Esta es una utilidad integrada de macOS. No se requiere instalación adicional si estás en macOS.

### Opcionales:

- Un archivo `.icns` de ícono para tu aplicación (si deseas un ícono personalizado).

---

## Cómo Usar

### Instrucciones de la GUI

1. **Descarga el Script**:
   - Clona o descarga este repositorio en tu máquina local.

2. **Prepara Tus Archivos**:
   - Asegúrate de tener un archivo `.jar` listo.
   - Opcionalmente, prepara un archivo `.icns` de ícono para tu aplicación.

3. **Ejecuta el Script**:
   - Abre una terminal y navega al directorio que contiene el script.
   - Ejecuta el script usando el siguiente comando:
     ```bash
     python3 jar2app-gui.py
     ```

4. **Usa la GUI**:
   - Completa los campos requeridos:
     - **Archivo JAR**: Selecciona tu archivo `.jar`.
     - **Versión**: Ingresa la versión de la aplicación (o déjalo en blanco para detectar automáticamente).
     - **Versión SDK**: Ingresa la versión del JDK requerida por tu aplicación (opcional).
     - **Directorio de Salida**: Elige dónde se creará la aplicación `.app`.
     - **Archivo de Ícono**: Selecciona un archivo `.icns` para el ícono de la aplicación (opcional).
   - Marca la casilla "Crear .dmg" si deseas generar una imagen de disco.
   - Haz clic en "Crear Aplicación" para generar la `.app` y, opcionalmente, el `.dmg`.

5. **Ubica la Salida**:
   - La `.app` se creará en el directorio de salida especificado.
   - Si seleccionaste la opción `.dmg`, el archivo `.dmg` también se creará en el mismo directorio.

---

## Uso de Línea de Comandos (Opcional)

Si prefieres usar la línea de comandos, puedes ejecutar el script sin la GUI. Así es como:

```bash
python3 jar2app.py \
    -jar /ruta/a/tu/app.jar \
    -version 1.0.0 \
    -sdk 21 \
    -output /ruta/a/directorio/de/salida \
    -icon /ruta/a/icono.icns
```

Argumentos:
- `-jar`: Ruta al archivo JAR (requerido).
- `-version`: Versión de la aplicación (opcional, predeterminado es `1.0.0` o detectado del manifiesto).
- `-sdk`: Versión del JDK requerida por la aplicación (opcional).
- `-output`: Directorio donde se creará la `.app` (predeterminado es el directorio actual).
- `-icon`: Ruta al archivo `.icns` de ícono (opcional).

---

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---