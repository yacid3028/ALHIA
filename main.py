from core.brain import process_command

def main():
    print("ALHIA iniciada...")
    
    while True:
        comando = input("Tú: ")
        
        if comando.lower() == "salir":
            break
        
        respuesta = process_command(comando)
        print("ALHIA:", respuesta)

