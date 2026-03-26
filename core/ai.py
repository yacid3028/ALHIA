import os, json, re
from groq import Groq
from dotenv import load_dotenv

from utils.helpers import limpiar_codigo

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def Consulta_ia(pregunta):
    prompt = f"""Eres un asistente que responde preguntas de forma clara, proporcionando información útil y relevante.
        Devolviendo el texto en formato de cmd para que pueda ser mostrado en la terminal con tabulaciones y saltos de linea.
        y sin formato markdown ni emojis ni nada, solo texto plano con tabulaciones y saltos de linea bien alineados y en los titulos marcandolos con guiones.
        dejando preguntas sobre el tema para que generes curiosidad el usuario y quiera poder seguir preguntando sin necesidad de reformular la pregunta anterior.
        Pregunta: {pregunta}
        """

    return client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    ).choices[0].message.content


def ev_url(comando, palabras_ignorar):
    prompt = f"""
    Responde ÚNICAMENTE con un JSON válido. No expliques nada. No agregues texto antes ni después.

    Formato exacto:
    {{"frase": "...", "url": "..."}}

    Reglas:

    1. Interpreta la intención del usuario aunque:
       - haya errores ortográficos (ej: "whats" → "whatsapp")
       - palabras incompletas (ej: "face" → "facebook")
       - lenguaje informal (ej: "buscame", "quiero ver", "abre")

    2. Normaliza la búsqueda:
       - corrige palabras mal escritas
       - completa nombres conocidos (apps, sitios, etc.)

    3. Detecta si es una web conocida:
       - whatsapp → https://www.whatsapp.com
       - facebook → https://www.facebook.com
       - youtube → https://www.youtube.com
       - gmail → https://mail.google.com
       - instagram → https://www.instagram.com

    4. Si NO es un sitio específico:
       - usa Google:
         https://www.google.com/search?q=

    5. Si menciona "video", "youtube", "ver":
       - usa YouTube:
         https://www.youtube.com/results?search_query=

    6. Reemplaza espacios por "+"

    7. Si no hay intención clara:
       {{"frase": "", "url": ""}}

    Ejemplos:

    "busca whats" → {{"frase": "whatsapp", "url": "https://www.whatsapp.com"}}
    "abre face" → {{"frase": "facebook", "url": "https://www.facebook.com"}}
    "quiero ver videos de risa" → {{"frase": "videos de risa", "url": "https://www.youtube.com/results?search_query=videos+de+risa"}}
    "investiga ia" → {{"frase": "inteligencia artificial", "url": "https://www.google.com/search?q=inteligencia+artificial"}}

    Entrada: {comando}
    """
    

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    print("Respuesta de ev_url:", response.choices[0].message.content)
    return response.choices[0].message.content


def analizar_codigo(codigo, instruccion):
    prompt = f"""
    Eres un experto programador.

    Tarea:
    {instruccion}

    Código:
    {codigo}

    Devuelve SOLO el código corregido y mejorado y cometarios cortos en las modificaciones.
    """
    
    respuesta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    contenido = respuesta.choices[0].message.content

    return limpiar_codigo(contenido)




def detectar_imports(codigo):
    imports = re.findall(r'import\s+(\w+)', codigo)
    return imports