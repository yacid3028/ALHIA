import json
from core.ai import Consulta_ia
from actions.sys_actions import editar_codigo, ejecutar, execute_action
from utils.helpers import extraer_datos_codigo
from web.web_actions import buscar_web
from core.interpreter import interpreter

def process_command(comando):
    try:
        resp = interpreter(comando)
        resp = resp.strip().strip("```json").strip("```").strip()
        datos = json.loads(resp)
        

        if datos.get("tipo") == "accion":
            accion = datos.get("accion")
            if accion == "abrir_app":
                return execute_action(datos.get("parametro"))
            elif accion == "editar_codigo":
                resultado = extraer_datos_codigo(comando)
                resultado = resultado.strip().strip("```json").strip("```").strip()
                datos_codigo = json.loads(resultado)
                nombre_archivo = datos_codigo.get("archivo")
                instruccion = datos_codigo.get("instruccion")
                if nombre_archivo:
                    nombre_archivo = nombre_archivo.replace("\\", "/")
                return editar_codigo(nombre_archivo, instruccion)
            elif accion == "eliminar_archivo":
                return ejecutar(datos)
            elif accion == "crear_archivo":
                return ejecutar(datos)
            elif accion == "crear_carpeta":
                return ejecutar(datos)
            else:
                return f"Acción '{accion}' aún no implementada"

        elif datos.get("tipo") == "pregunta": 
            return Consulta_ia(comando)

        elif datos.get("tipo") == "busqueda":
            return buscar_web(comando)
        
        else:
            return f"No entendí el tipo de comando: '{datos.get('tipo')}'"

    except Exception as e:
        return f"Error: {e}"
    
