import os
import re
from groq import Groq
from config import BASE_DIR
from dotenv import load_dotenv
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def buscar_archivo(nombre_archivo):
    coincidencias = []

    for base in BASE_DIR:
        for root, dirs, files in os.walk(base):
            for file in files:
                if file.lower() == nombre_archivo.lower():
                    ruta_completa = os.path.join(root, file)
                    coincidencias.append(ruta_completa)

    if len(coincidencias) == 0:
        return None

    if len(coincidencias) == 1:
        return coincidencias[0]

    return coincidencias


def extraer_datos_codigo(comando):
    prompt = f"""
    Eres un filtro de código. Extrae SOLO el nombre con su extensión y la instrucción para editar el código del siguiente comando,
      sin explicaciones ni texto adicional. El bloque de código estará em el siguiente formato JSON:
 
    {{
        "archivo": "nombre_del_archivo.extensión",
        "instruccion": "instrucción para editar el código"
    }}

    importante: si recives la ruta completa de un archivo, devuelve la ruta completa o la parte de la ruta que corresponde al nombre del archivo.
    
    Ejemplo de comando: 
    "edita mi código en main.html para que imprima 'Hola Mundo' color rojo al ejecutarse"->{{"archivo": "main.html", "instruccion": "modifica el código para que imprima 'Hola Mundo' al ejecutarse"}}
    "edita mi programa llamado calculadora.py para que sume dos números" -> {{"archivo": "calculadora.py", "instruccion": "modifica el código para que sume dos números"}}
    "quiero que el archivo C:/Users/User/Documents/script.js tenga una función que muestre un alert" -> {{"archivo": "C:/Users/User/Documents/script.js", "instruccion": "agrega una función que muestre un alert"}}
    "modifica el código de mi proyecto para que el archivo documents/app.py imprima 'Proyecto actualizado'" -> {{"archivo": "app.py", "instruccion": "modifica el código para que imprima 'Proyecto actualizado'"}}

    Comando: {comando}
    """
    
    respuesta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return respuesta.choices[0].message.content

def limpiar_codigo(respuesta):

    codigo = re.sub(r"```[a-zA-Z]*\n?", "", respuesta)
    codigo = codigo.replace("```", "")

    return codigo.strip()