import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv() 
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def evaluar_comando(comando):
    prompt = f"""
    Eres un clasificador de intenciones. Responde SOLO con una palabra:
    accion, pregunta o busqueda.

    Reglas:

    1. "accion" → SOLO si la instrucción es para ejecutar algo en el sistema operativo LOCAL
       (programas instalados, archivos, configuraciones).
       Ejemplos:
       - "abre calculadora"
       - "abre bloc de notas"
       - "apaga la computadora"

    2. "busqueda" → si:
       - menciona "web", "internet", "google", "youtube", "navegador"
       - quiere abrir un sitio en internet (aunque diga "abre")
       - quiere ver contenido online
       - ejemplos:
         - "abre whatsapp en la web"
         - "abre facebook"
         - "busca videos de gatos"
         - "quiero ver memes"
         - "abre youtube"

    3. "pregunta" → si es conversación o consulta sin intención de ejecutar ni buscar directamente
       Ejemplos:
       - "¿qué es la inteligencia artificial?"
       - "dime una receta de pasta"
       - "cómo funciona un motor"

    4. Prioridad IMPORTANTE:
       - Si hay duda entre "accion" y "busqueda", elige "busqueda"
       - Si menciona algo que normalmente está en internet (redes sociales, sitios web), es "busqueda"
       - Frases como "abre X en la web" SIEMPRE son "busqueda"

    5. Lenguaje flexible:
       - interpreta errores ortográficos ("whats" = "whatsapp")
       - lenguaje informal ("abre face", "pon youtube")

    Ejemplos:

    "abre calculadora" → accion
    "abre spotify" → accion
    "abre code" → accion
    "abre whatsapp en la web" → busqueda
    "abre face" → busqueda
    "quiero ver videos de risa" → busqueda
    "busca recetas de pasta" → busqueda
    "¿qué es python?" → pregunta

    Comando: {comando}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip().strip('"').lower()


def interpretar_comando(comando):
    prompt = f"""
    Eres un asistente que convierte instrucciones en acciones.
    Devuelve SOLO un JSON con este formato:
    {{
    "accion": "nombre_accion",
    "parametro": "valor"
    }}
    importante: mi navegador predeterminado es microsoft edge.

    Ejemplos:
    "edita mi código en main.html" → {{"accion": "editar_codigo", "parametro": "code_modificacion"}}
    "modifica el archivo script.js para que imprima 'Hola Mundo' al ejecutarse" → {{"accion": "editar_codigo", "parametro": "code_modificacion"}}
    "abre el archivo de texto notas.txt" → {{"accion": "abrir_archivo", "parametro": "notas.txt"}}
    "abre el archivo de excel datos.xlsx" → {{"accion": "abrir_archivo", "parametro": "datos.xlsx"}} 
    "abre el archivo de word informe.py y agrega una línea que diga 'Hola, mundo!'" → {{"accion": "editar_codigo", "parametro": "code_modificacion"}}
    "abre bloc de notas" → {{"accion": "abrir_app", "parametro": "notepad"}}
    "ejecuta visual studio code" → {{"accion": "abrir_app", "parametro": "code"}}
    "abre spotify" → {{"accion": "abrir_app", "parametro": "spotify"}}

    IMPORTANTE: en parametro pon el nombre del ejecutable real, no el nombre comercial.

    Comando: {comando}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

    