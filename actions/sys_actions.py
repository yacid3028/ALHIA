import subprocess
import shutil
import os
import winreg

from config import BASE_DIR
from core.ai import analizar_codigo
from utils.helpers import buscar_archivo

def buscar_en_path(nombre):
    return shutil.which(nombre)

def buscar_en_registro(nombre):
    rutas_registro = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\App Paths",
    ]
    nombre_exe = nombre if nombre.endswith(".exe") else nombre + ".exe"
    
    for ruta in rutas_registro:
        try:
            clave = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, f"{ruta}\\{nombre_exe}")
            ruta_exe, _ = winreg.QueryValueEx(clave, "")
            winreg.CloseKey(clave)
            if os.path.exists(ruta_exe):
                return ruta_exe
        except:
            continue
    return None

def buscar_en_carpetas(nombre):
    
    carpetas = [
        os.environ.get("PROGRAMFILES", "C:\\Program Files"),
        os.environ.get("PROGRAMFILES(X86)", "C:\\Program Files (x86)"),
        os.environ.get("LOCALAPPDATA", ""),
        os.environ.get("APPDATA", ""),
    ]
    nombre_exe = nombre if nombre.endswith(".exe") else nombre + ".exe"
    
    for carpeta in carpetas:
        if not carpeta:
            continue
        for raiz, dirs, archivos in os.walk(carpeta):
            if nombre_exe.lower() in [a.lower() for a in archivos]:
                return os.path.join(raiz, nombre_exe)
    return None

def execute_action(nombre_app):
    #PATH del sistema
    ruta = buscar_en_path(nombre_app)
    
    #Registro de Windows
    if not ruta:
        ruta = buscar_en_registro(nombre_app)
    
    #Buscar en carpetas (más lento)
    if not ruta:
        print(f"Buscando {nombre_app} en el sistema...")
        ruta = buscar_en_carpetas(nombre_app)
    
    if ruta:
        try:
            subprocess.Popen(ruta, shell=True)
            return f"Abriendo {nombre_app}..."
        except Exception as e:
            return f"Encontré {nombre_app} pero no pude abrirlo: {e}"
    else:
        return f"No encontré '{nombre_app}' instalado en el sistema"


def leer_archivo(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()


def escribir_archivo(ruta, contenido):
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)
        

def backup_archivo(ruta):
    shutil.copy(ruta, ruta + ".bak")


def editar_codigo(nombre_archivo, instruccion):

    if os.path.exists(nombre_archivo):
        ruta = nombre_archivo.replace("\\", "/")

    else:
        resultado = buscar_archivo(nombre_archivo)

        if not resultado:
            return f"No encontré el archivo {nombre_archivo}"

        if isinstance(resultado, list):
            lista = "\n".join([f"{i+1}. {ruta}" for i, ruta in enumerate(resultado)])
            return f"Encontré varios archivos:\n{lista}\n\nEspecifica cuál quieres editar."

        ruta = resultado

    codigo = leer_archivo(ruta)

    backup_archivo(ruta)

    nuevo_codigo = analizar_codigo(codigo, instruccion)

    escribir_archivo(ruta, nuevo_codigo)

    return f"Archivo editado correctamente:\n{ruta}"




def ejecutar(data):

    accion = data["accion"]

    if accion == "eliminar_archivo":
        resultado = buscar_archivo(data["parametro"])

        if isinstance(resultado, list):
            lista = "\n".join([f"{i+1}. {r}" for i, r in enumerate(resultado)])
            return f"Encontré varios archivos:\n{lista}\nElige cuál eliminar."

        elif resultado:
            os.remove(resultado)
            return f"Archivo eliminado: {resultado}"

        else:
            return "No encontré el archivo"

    elif accion == "crear_carpeta":
        ruta = os.path.join(os.path.expanduser("~\\OneDrive\\Desktop"), data["parametro"])
        os.makedirs(ruta, exist_ok=True)
        return f"Carpeta creada en : {ruta}"
    
    elif accion == "crear_archivo":
        ruta = os.path.join(os.path.expanduser("~\\OneDrive\\Desktop"), data["parametro"])
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("")
        return f"Archivo creado en: {ruta}"

    elif accion == "renombrar":
        ruta = buscar_archivo(data["origen"])
        if isinstance(ruta, list):
            lista = "\n".join([f"{i+1}. {r}" for i, r in enumerate(ruta)])
            return f"Hay varios archivos:\n{lista}\nElige cuál renombrar."

        elif ruta:
            nueva_ruta = os.path.join(os.path.dirname(ruta), data["nuevo"])
            os.rename(ruta, nueva_ruta)
            return f"Archivo renombrado a: {nueva_ruta}"

        else:
            return "No encontré el archivo"

    return "Acción no válida"


        # leer y eliminar mails, resumen de noticias, clima, etc.
        #  se pueden agregar como acciones ejecutables 
        # responder leer whatsapp, telegram, etc. con la api de cada uno 
        # y mostrar un resumen en la terminal o incluso responder mensajes desde la terminal.