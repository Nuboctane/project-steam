import json

class json_parser():
    def do_all():
        # voert de gehele json functionalitijd uit
        json_parser.update_json()
        file_as_json = json_parser.get_json()
        json_as_array = json_parser.parse_json(file_as_json)
        return json_as_array
    
    # json apparte functies uitvoeren (mocht het nodig zijn)
    def update_json():
        """
            json data ophalen van steam api,
            steam.json updaten met deze data
        """
        return None

    def get_json():
        # json data op halen uit bestand "steam.json"
        with open("steam.json", "r") as file:
            file_as_json = json.load(file)
            file.close()
        return file_as_json

    def parse_json(json_data):
        # json data segmenteren om te gebruiken
        main_segments = [] # hoofd segmenten zijn de objecten in de eerste tak van de json
        for initial_segment in json_data:
            main_segments.append(initial_segment)

        return main_segments