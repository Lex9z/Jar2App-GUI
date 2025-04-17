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
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from zipfile import ZipFile
import plistlib
import shutil
import subprocess

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
        messagebox.showerror("Error", f"Error al leer el archivo JAR: {e}")
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
        messagebox.showerror("Error", f"Error al leer el archivo JAR: {e}")
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
    os.makedirs(resources_dir, exist_ok=True)
    os.makedirs(java_dir, exist_ok=True)

    # Copiar el archivo JAR al directorio Java
    shutil.copy(jar_path, java_dir)

    # Encontrar la clase principal (Main-Class) en el archivo JAR
    main_class_name = find_jar_mainclass(jar_path)
    if not main_class_name:
        messagebox.showerror("Error", "No se encontró la clase principal (Main-Class) en el archivo JAR.")
        return

    print(f"Clase principal detectada: {main_class_name}")

    # Buscar el ícono si no se proporciona uno explícitamente
    if not icon_path:
        icon_path = Path(jar_path).parent / "icon.icns"
        if not icon_path.exists():
            icon_path = None

    if icon_path:
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
        "CFBundleIconFile": icon_filename,
        "CFBundleIdentifier": f"com.example.{app_name.lower()}",
        "CFBundleInfoDictionaryVersion": "6.0",
        "CFBundleName": app_name,
        "CFBundlePackageType": "APPL",
        "CFBundleVersion": version,
        "CFBundleShortVersionString": version,
        "NSHumanReadableCopyright": "© 2023 Your Company",
        "CFBundleAllowMixedLocalizations": True,
        "NSHighResolutionCapable": True,
        "CFBundleSignature": "????",
        "JVMMainClassName": main_class_name,
        "JVMOptions": [
            "-Dapple.laf.useScreenMenuBar=true",
            "-Duser.dir=$APP_ROOT/Contents/Java"
        ],
        "JVMArguments": [],
        "JVMVersion": sdk_version if sdk_version else "",
    }

    # Guardar el archivo Info.plist
    plist_path = contents_dir / "Info.plist"
    with open(plist_path, "wb") as plist_file:
        plistlib.dump(info_plist, plist_file)

    # Copiar el universalJavaApplicationStub desde el directorio datafiles
    script_dir = Path(__file__).parent
    datafiles_dir = script_dir / "datafiles"
    stub_source = datafiles_dir / "universalJavaApplicationStub"
    stub_target = macos_dir / "universalJavaApplicationStub"

    if not stub_source.exists():
        messagebox.showerror("Error", f"No se encontró el archivo 'universalJavaApplicationStub' en {datafiles_dir}.")
        return

    shutil.copy(stub_source, stub_target)
    os.chmod(stub_target, 0o755)

    messagebox.showinfo("Éxito", f"Aplicación creada en: {app_dir}")
    return app_dir

# Función para crear un archivo .dmg
def create_dmg(app_dir, output_dir):
    try:
        app_name = app_dir.stem
        dmg_path = Path(output_dir) / f"{app_name}.dmg"
        
        # Crear un archivo .dmg usando hdiutil
        temp_dmg = Path(output_dir) / "temp.dmg"
        subprocess.run(["hdiutil", "create", "-srcfolder", app_dir, "-volname", app_name, "-format", "UDZO", temp_dmg], check=True)
        shutil.move(temp_dmg, dmg_path)
        
        messagebox.showinfo("Éxito", f"Archivo .dmg creado en: {dmg_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al crear el archivo .dmg: {e}")

# Función para manejar el botón "Crear Aplicación"
def on_create_app():
    jar_path = jar_path_var.get()
    version = version_var.get() or find_jar_version(jar_path) or "1.0.0"
    sdk_version = sdk_version_var.get()
    output_dir = output_dir_var.get()
    icon_path = icon_path_var.get()
    create_dmg_flag = create_dmg_var.get()

    if not jar_path or not Path(jar_path).is_file():
        messagebox.showerror("Error", "Debe seleccionar un archivo JAR válido.")
        return

    if not output_dir or not Path(output_dir).is_dir():
        messagebox.showerror("Error", "Debe seleccionar un directorio de salida válido.")
        return

    if icon_path and not Path(icon_path).is_file():
        messagebox.showerror("Error", "El archivo de ícono seleccionado no es válido.")
        return

    app_name = Path(jar_path).stem
    app_dir = create_macos_app(app_name, version, jar_path, sdk_version, output_dir, icon_path)

    if create_dmg_flag and app_dir:
        create_dmg(app_dir, output_dir)

# Función para abrir el cuadro de diálogo de selección de archivos
def browse_file(entry_var, filetypes):
    filepath = filedialog.askopenfilename(filetypes=filetypes)
    if filepath:
        entry_var.set(filepath)

# Función para abrir el cuadro de diálogo de selección de directorios
def browse_directory(entry_var):
    dirpath = filedialog.askdirectory()
    if dirpath:
        entry_var.set(dirpath)

# Configuración de la GUI
root = tk.Tk()
root.title("Creador de Aplicaciones macOS (.app)")

# Variables para almacenar las entradas del usuario
jar_path_var = tk.StringVar()
version_var = tk.StringVar()
sdk_version_var = tk.StringVar()
output_dir_var = tk.StringVar()
icon_path_var = tk.StringVar()
create_dmg_var = tk.BooleanVar()

# Etiquetas y campos de entrada
tk.Label(root, text="Archivo JAR:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
tk.Entry(root, textvariable=jar_path_var, width=50).grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Buscar", command=lambda: browse_file(jar_path_var, [("JAR Files", "*.jar")])).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Versión:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
tk.Entry(root, textvariable=version_var, width=50).grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Versión SDK:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
tk.Entry(root, textvariable=sdk_version_var, width=50).grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Directorio de Salida:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
tk.Entry(root, textvariable=output_dir_var, width=50).grid(row=3, column=1, padx=10, pady=5)
tk.Button(root, text="Buscar", command=lambda: browse_directory(output_dir_var)).grid(row=3, column=2, padx=10, pady=5)

tk.Label(root, text="Ícono (.icns):").grid(row=4, column=0, sticky="w", padx=10, pady=5)
tk.Entry(root, textvariable=icon_path_var, width=50).grid(row=4, column=1, padx=10, pady=5)
tk.Button(root, text="Buscar", command=lambda: browse_file(icon_path_var, [("Icon Files", "*.icns")])).grid(row=4, column=2, padx=10, pady=5)

# Opción para crear un archivo .dmg
tk.Checkbutton(root, text="Crear archivo .dmg", variable=create_dmg_var).grid(row=5, column=0, columnspan=3, pady=10)

# Botón para crear la aplicación
tk.Button(root, text="Crear Aplicación", command=on_create_app).grid(row=6, column=1, pady=20)

# Ejecutar la GUI
root.mainloop()