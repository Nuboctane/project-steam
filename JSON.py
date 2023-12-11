import json
import requests
import os
from dotenv import load_dotenv
load_dotenv()

class json_parser():
# voert de gehele json functionalitijd uit
    def do_all(fetch_limit, filter_type):
        # update het json bestand met x games en str filter type
        json_parser.update_json(fetch_limit, filter_type)
        file_as_json = json_parser.get_json()
        json_as_array = json_parser.parse_json(file_as_json)
        return json_as_array
    
    # json apparte functies uitvoeren (mocht het nodig zijn)
    def update_json(fetch_limit, filter_type):
        # steam game id's ophalen van een lijst met steam games
        url_game_id = f"http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key={os.getenv('STEAM_API_KEY')}&format=json"
        list_id_game = []
        response = requests.get(url_game_id)
        response_id = response.json()
        x=0
        for i in range(0, len(response_id["applist"]["apps"])):
            if response_id["applist"]["apps"][i]["name"] == '':
                pass
            else: 
                x+=1   
                list_id_game.append(response_id["applist"]["apps"][i]["appid"])
            if x == fetch_limit:
                    break
            
        # data van game id's ophalen
        response_data = []
        for game_id in list_id_game:
            url_game_data = f"https://store.steampowered.com/api/appdetails?appids={game_id}"
            response = requests.get(url_game_data)
            if response.json()[str(game_id)]["success"]:
                response_data.append(response.json())

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
    
    def user_name(user_name):
        #checkt wat het steam id is van de user_name
        url_naam = f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=B963C6F4BBFDDBE51DF25EA01CCF94A1&vanityurl={user_name}"
        response = requests.get(url_naam)
        response_data = response.json()
        steam_id = response_data["response"]["steamid"]
        #checkt de data van de user_name met de steam id die gevonden is
        url_id = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=B963C6F4BBFDDBE51DF25EA01CCF94A1&steamids={steam_id}"
        response_id = requests.get(url_id)
        response_id_data = response_id.json()
        return response_id_data