import json

# main python class
class main():
    # deze functie wordt gerund wanneer "main()" wordt genoemt (onder aan de code)
    # de innit functie serveert als default functie waar class "main()" mee opstart
    def __init__(self):
        # main.update_json(self)
        file_as_json = main.get_json(self)
        main.parse_json(self, file_as_json)

    def update_json(self):
        """
            json data ophalen van steam api,
            steam.json updaten met deze data
        """
        return None

    def get_json(self):
        # json data op halen uit bestand "steam.json"
        with open("steam.json", "r") as file:
            file_as_json = json.load(file)
            file.close()
        return file_as_json

    def parse_json(self, json_data):
        # json data segmenteren om te gebruiken
        main_segments = [] # hoofd segmenten zijn de objecten in de eerste tak van de json
        for initial_segment in json_data:
            main_segments.append(initial_segment)

        return main_segments

main()