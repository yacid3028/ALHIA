import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv() 
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def interpreter(comando):
    prompt = f"""Eres un sistema inteligente que analiza instrucciones del usuario y responde SIEMPRE con un JSON estructurado.
      Respondes SOLO con un JSON válido que clasifica la intención del comando, determina si es ejecutable y genera la acción adecuada (si aplica).
      Tu objetivo es:
      1. Clasificar la intención
      2. Determinar si es ejecutable
      3. Generar la acción adecuada (si aplica)


      FORMATO DE RESPUESTA (OBLIGATORIO):

      Responde SOLO con un JSON válido:

      {{
        "tipo": "accion | busqueda | pregunta",
        "accion": "nombre_accion | null",
        "parametro": "valor | null",
        "ejecutable": true | false
      }}


      DEFINICIONES:

      1. "accion" → SOLO si es algo que se ejecuta en el SISTEMA LOCAL:
         - abrir programas instalados
         - crear, editar o eliminar archivos
         - acciones del sistema operativo

      2. "busqueda" → si:
         - menciona web, internet, navegador
         - redes sociales o sitios web
         - contenido online
         - aunque diga "abre", si es web → ES busqueda

      3. "pregunta" → si:
         - es conversación
         - consulta informativa
         - no ejecuta ni busca directamente


      REGLAS IMPORTANTES:

      - Si hay duda entre "accion" y "busqueda" → SIEMPRE "busqueda"
      - Redes sociales → SIEMPRE "busqueda"
      - "abre X en la web" → SIEMPRE "busqueda"
      - Corrige errores ortográficos automáticamente
      - Interpreta lenguaje informal


      ACCIONES PERMITIDAS (solo si tipo = "accion"):

      - abrir_app → abrir programa local
      - abrir_archivo → abrir archivo
      - renombrar_archivo → cambiar nombre de archivo,reordenar archivo
      - eliminar_carpeta → eliminar carpeta, borrar carpeta
      - crear_archivo → crear archivo, agregar archivo
      - eliminar_archivo → eliminar archivo, borrar archivo
      - editar_codigo → modificar contenido de archivo

      IMPORTANTE:
      - En "parametro" usa el ejecutable real (ej: "notepad", "code", "excel.exe")
      - Para edición de código usa: "code_modificacion"


      CASO ESPECIAL (BUSQUEDA):

      Si es "busqueda":
      - "accion" = "abrir_navegador"
      - "parametro" = lo que se debe buscar o abrir
      - Usa lenguaje limpio para búsqueda
      - El navegador predeterminado es Microsoft Edge


      CASO PREGUNTA:

      Si es "pregunta":
      - "accion" = null
      - "parametro" = null
      - "ejecutable" = false


      EJEMPLOS:

      "abre calculadora"
       {{
        "tipo": "accion",
        "accion": "abrir_app",
        "parametro": "calc.exe",
        "ejecutable": true
      }}

      "abre whatsapp en la web"
      {{
        "tipo": "busqueda",
        "accion": "abrir_navegador",
        "parametro": "whatsapp web",
        "ejecutable": true
      }}

      "abre facebook"
      {{
        "tipo": "busqueda",
        "accion": "abrir_navegador",
        "parametro": "facebook",
        "ejecutable": true
      }}

      "elimina el archivo viejo.txt"
      {{
        "tipo": "accion",
        "accion": "eliminar_archivo",
        "parametro": "viejo.txt",
        "ejecutable": true
      }}

      "¿qué es python?"
      {{
       "tipo": "pregunta",
        "accion": null,
        "parametro": null,
        "ejecutable": false
      }}


      Comando: {comando} 

   """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip().strip('"').lower()

