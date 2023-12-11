from GUI import gui_class as GUI
from JSON import json_parser as JSON
# main python class
class main():
    # noobs please read:
    # 
    # deze functie wordt gerund wanneer "main()" wordt genoemt (onder aan de code)
    # de innit functie serveert als default functie waar class "main()" mee opstart
    # als de class geen __init__ heeft dan moet je zelf handmatig zijn functies aanroepen
    # bekijk GUI gui_class als voorbeeld

    def __init__(self):
        GUI.open_gui(self)

main()