#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# MIT License
# 
# Copyright (c) 2025 Lex9z (Alexis Arias)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 

import os
import argparse
import plistlib
import shutil
from pathlib import Path
from zipfile import ZipFile

# Función para encontrar la Main-Class en el archivo JAR
def find_jar_mainclass(jar_file):
    try:
        with ZipFile(jar_file, 'r') as f:
            for file in f.infolist():
                if file.filename.lower().endswith('manifest.mf'):
                    manifest = f.read(file).decode()
                    for line in manifest.splitlines():
                        if line.strip().lower().startswith('main-class'):
                            return line.split(':')[1].strip()
    except Exception as e:
        print(f"Error al leer el archivo JAR: {e}")
    return None

# Función para encontrar la versión en el archivo JAR
def find_jar_version(jar_file):
    try:
        with ZipFile(jar_file, 'r') as f:
            for file in f.infolist():
                if file.filename.lower().endswith('manifest.mf'):
                    manifest = f.read(file).decode()
                    for line in manifest.splitlines():
                        if line.strip().lower().startswith('implementation-version'):
                            return line.split(':')[1].strip()
                        elif line.strip().lower().startswith('specification-version'):
                            return line.split(':')[1].strip()
    except Exception as e:
        print(f"Error al leer el archivo JAR: {e}")
    return None

# Función para crear la estructura de la aplicación .app
def create_macos_app(app_name, version, jar_path, sdk_version, output_dir, icon_path=None):
    # Crear directorios base
    app_dir = Path(output_dir) / f"{app_name}.app"
    contents_dir = app_dir / "Contents"
    macos_dir = contents_dir / "MacOS"
    resources_dir = contents_dir / "Resources"
    java_dir = contents_dir / "Java"

    # Eliminar la aplicación si ya existe
    if app_dir.exists():
        shutil.rmtree(app_dir)

    # Crear directorios
    os.makedirs(macos_dir, exist_ok=True)
    os.makedirs(resources_dir, exist_ok=True)  # Siempre crea el directorio Resources
    os.makedirs(java_dir, exist_ok=True)

    # Copiar el archivo JAR al directorio Java
    shutil.copy(jar_path, java_dir)

    # Encontrar la clase principal (Main-Class) en el archivo JAR
    main_class_name = find_jar_mainclass(jar_path)
    if not main_class_name:
        print("Error: No se encontró la clase principal (Main-Class) en el archivo JAR.")
        return

    print(f"Clase principal detectada: {main_class_name}")

    # Buscar el ícono si no se proporciona uno explícitamente
    if not icon_path:
        icon_path = Path(jar_path).parent / "icon.icns"
        if not icon_path.exists():
            icon_path = None  # No se encontró el ícono

    if icon_path:
        # Copiar el ícono al directorio Resources
        shutil.copy(icon_path, resources_dir)
        icon_filename = Path(icon_path).name
        print(f"Ícono detectado y copiado: {icon_filename}")
    else:
        icon_filename = ""
        print("No se encontró ningún ícono.")

    # Escribir el archivo Info.plist
    info_plist = {
        "CFBundleDevelopmentRegion": "English",
        "CFBundleExecutable": "universalJavaApplicationStub",
        "CFBundleIconFile": icon_filename,  # Nombre del ícono sin extensión
        "CFBundleIdentifier": f"com.jar2app.{app_name.lower()}",
        "CFBundleInfoDictionaryVersion": "6.0",
        "CFBundleName": app_name,
        "CFBundlePackageType": "APPL",
        "CFBundleVersion": version,
        "CFBundleShortVersionString": version,
        "NSHumanReadableCopyright": "© 2025 Lex9z",
        "CFBundleAllowMixedLocalizations": True,
        "NSHighResolutionCapable": True,
        "CFBundleSignature": "????",
        "JVMMainClassName": main_class_name,  # Clase principal detectada
        "JVMOptions": [
            "-Dapple.laf.useScreenMenuBar=true",
            "-Duser.dir=$APP_ROOT/Contents/Java"
        ],
        "JVMArguments": [],
        "JVMVersion": sdk_version if sdk_version else "",  # Versión del SDK (puede estar vacía)
    }

    # Guardar el archivo Info.plist
    plist_path = contents_dir / "Info.plist"
    with open(plist_path, "wb") as plist_file:
        plistlib.dump(info_plist, plist_file)

    # Copiar el universalJavaApplicationStub desde el directorio datafiles
    script_dir = Path(__file__).parent  # Directorio donde está el script
    datafiles_dir = script_dir / "datafiles"
    stub_source = datafiles_dir / "universalJavaApplicationStub"
    stub_target = macos_dir / "universalJavaApplicationStub"

    if not stub_source.exists():
        print(f"Error: No se encontró el archivo 'universalJavaApplicationStub' en {datafiles_dir}.")
        return

    shutil.copy(stub_source, stub_target)
    os.chmod(stub_target, 0o755)  # Hacerlo ejecutable

    print(f"Aplicación creada en: {app_dir}")

# Configuración del parser de argumentos
def main():
    parser = argparse.ArgumentParser(description="Convierte un archivo JAR en una aplicación macOS (.app)")
    parser.add_argument("-sdk", help="Versión del JDK requerida (por ejemplo, 21). Puede omitirse.")
    parser.add_argument("-version", help="Versión de la aplicación. Si no se especifica, se toma del MANIFEST.MF o usa '1.0.0'.")
    parser.add_argument("-jar", required=True, help="Ruta al archivo JAR")
    parser.add_argument("-icon", help="Ruta al archivo de ícono (.icns)")
    parser.add_argument("-output", default=".", help="Directorio de salida para la aplicación")

    args = parser.parse_args()

    # Validar que el archivo JAR existe
    jar_path = Path(args.jar)
    if not jar_path.is_file():
        print(f"Error: El archivo JAR '{args.jar}' no existe.")
        return

    # Determinar la versión de la aplicación
    if args.version:
        version = args.version
    else:
        version = find_jar_version(args.jar)
        if not version:
            version = "1.0.0"
            print("No se encontró una versión en el MANIFEST.MF. Usando '1.0.0' como predeterminado.")
        else:
            print(f"Versión detectada en el MANIFEST.MF: {version}")

    # Validar que el ícono existe si se especifica
    icon_path = None
    if args.icon:
        icon_path = Path(args.icon)
        if not icon_path.is_file():
            print(f"Error: El archivo de ícono '{args.icon}' no existe.")
            return

    # Extraer el nombre de la aplicación del archivo JAR
    app_name = jar_path.stem

    # Crear la aplicación
    create_macos_app(app_name, version, args.jar, args.sdk, args.output, icon_path)

if __name__ == "__main__":
    main()