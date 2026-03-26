import webbrowser
import urllib.parse
import json
from core.ai import ev_url

def buscar_web(comando):
    palabras_ignorar = ["busca", "buscar", "busque", "googlea", "encuentra", "busqueda","investiga", "investiga sobre", "investiga acerca de", "busca información sobre", "busca información acerca de"]
    termino = ev_url(comando, palabras_ignorar)

    if not termino:
        return "No sé qué buscar"
    termino = termino.strip().strip("```json").strip("```").strip()
    datos = json.loads(termino)
    url = datos["url"]
    webbrowser.open(url)
    return f"Buscando: {datos['frase']} en la web..."

