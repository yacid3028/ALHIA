import json
from core.ai import Consulta_ia
from actions.sys_actions import editar_codigo, execute_action
from utils.helpers import extraer_datos_codigo
from web.web_actions import buscar_web
from core.interpreter import evaluar_comando, interpretar_comando

def process_command(comando):
    try:
        tipo = evaluar_comando(comando)

        if tipo == "accion":
            raw = interpretar_comando(comando)
            raw = raw.strip().strip("```json").strip("```").strip()
            datos = json.loads(raw)
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
            else:
                return f"Acción '{accion}' aún no implementada"

        elif tipo == "pregunta":
            return Consulta_ia(comando)

        elif tipo == "busqueda":
            return buscar_web(comando)
        
        else:
            return f"No entendí el tipo de comando: '{tipo}'"

    except Exception as e:
        return f"Error: {e}"
    
