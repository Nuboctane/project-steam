import json
import requests

class json_parser():
# voert de gehele json functionalitijd uit
    def do_all():
        # update het json bestand met x games
        json_parser.update_json(50)
        file_as_json = json_parser.get_json()
        json_as_array = json_parser.parse_json(file_as_json)
        return json_as_array
    
    # json apparte functies uitvoeren (mocht het nodig zijn)
    def update_json(fetch_limit):
        # steam game id's ophalen van een lijst met steam games
        url_game_id = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=B963C6F4BBFDDBE51DF25EA01CCF94A1&format=json"
        list_id_game = []
        response = requests.get(url_game_id)
        response_id = response.json()
        for i in range(0, len(response_id["applist"]["apps"])):
            if response_id["applist"]["apps"][i]["name"] == '':
                pass
            else:    
                list_id_game.append(response_id["applist"]["apps"][i]["appid"])
        
        response_data = []
        x=0
        for game_id in list_id_game:
            x+=1
            url_game_data = f"https://steamspy.com/api.php?request=appdetails&appid={game_id}"
            response = requests.get(url_game_data)
            response_data.append(response.json())
            if x == fetch_limit:
                break

        # response data naar steam.json schrijven
        with open("steam.json", "w") as file:
            json_object = json.dumps(response_data, indent=4)
            file.write(json_object)
            file.close()

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