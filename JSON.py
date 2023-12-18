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
        json_as_array = json_parser.parse_json(file_as_json, filter_type)
        return json_as_array
    
    # json apparte functies uitvoeren (mocht het nodig zijn)
    def update_json(fetch_limit, filter_type):
        # steam game id's ophalen van een lijst met steam games
        url_game_id = f"http://steamspy.com/api.php?request=top100forever"
        list_id_game = []
        response = requests.get(url_game_id)
        response_id = response.json()
        for game in response_id.values():
            list_id_game.append(game['appid'])
            
        # data van game id's ophalen
        response_data = []
        for game_id in list_id_game:
            url_game_data = f"https://store.steampowered.com/api/appdetails?appids={game_id}&cc=nl"
            url_game_reviews = f"https://store.steampowered.com/appreviews/{game_id}?json=1&num_per_page=0"
            url_game_price = f"https://steamspy.com/api.php?request=appdetails&appid={game_id}"
            response_review = requests.get(url_game_reviews)
            response_game = requests.get(url_game_data)
            response_price = requests.get(url_game_price)
            if "price_overview" not in response_game.json()[str(game_id)]["data"] and response_game.json()[str(game_id)]["data"]["is_free"] == False:
                 price_dict = json.loads(response_price.json()["price"])
                 new_response = {**response_game.json(), **response_review.json()["query_summary"], "price": price_dict}
            else:
                new_response = {**response_game.json(), **response_review.json()["query_summary"]}
            if response_game.json()[str(game_id)]["success"] and response_review.json()["success"]:
                response_data.append(new_response)

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

    def parse_json(json_data, filter_type):
        # json data segmenteren om te gebruiken
        main_segments = [] # hoofd segmenten zijn de objecten in de eerste tak van de json
        for initial_segment in json_data:
            match filter_type:
                case "default":
                    # filterd niks
                    main_segments.append(initial_segment)
                case "popular":
                    # maak hier een filter voor populaire spellen
                    None
                case "price1":
                    # maak hier een filter voor prijs (laag > hoog)
                    None
                case "price2":
                    # maak hier een filter voor prijs (hoog > laag)
                    None
                # maar zelf andere filters die je er in wilt hebben
                case _:
                    # filterd niks
                    main_segments.append(initial_segment)

        return main_segments
    
    def game_search(game_name):
        url_game_id = f"http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key={os.getenv('STEAM_API_KEY')}&format=json"
        response = requests.get(url_game_id)
        response_id = response.json()
        matching_games = []
        for i in range(0, len(response_id["applist"]["apps"])):
            if game_name.lower() in response_id["applist"]["apps"][i]["name"].lower():
                matching_games.append(response_id["applist"]["apps"][i])
        return matching_games

    def game_data(list_id_game):
        response_data = []
        for game in list_id_game:
            game_id = game["appid"]
            url_game_data = f"https://store.steampowered.com/api/appdetails?appids={game_id}"
            url_game_reviews = f"https://store.steampowered.com/appreviews/{game_id}?json=1&num_per_page=0"
            response_review = requests.get(url_game_reviews)
            response_game = requests.get(url_game_data)
            new_response = {**response_game.json(), **response_review.json()["query_summary"]}
            if response_game.json()[str(game_id)]["success"] and response_review.json()["success"]:
                #hier onder check hij als de game een game is en niet een dlc
                if response_game.json()[str(game_id)]["data"]["type"] == "game":
                    response_data.append(new_response)
                    with open("tmp.json", "w") as file:
                        json_object = json.dumps(response_data, indent=4)
                        file.write(json_object,)

    def get_game_reviews(game_id):
        url_game_reviews = f"https://store.steampowered.com/appreviews/{game_id}?json=1&num_per_page=5"
        response_review = requests.get(url_game_reviews)
        response_review = response_review.json()
        reviews = response_review['reviews']
        lst_reviews = []
        for i in range(len(reviews)):
            user = reviews[i]['author']['steamid']
            url_id = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=B963C6F4BBFDDBE51DF25EA01CCF94A1&steamids={user}"
            response_id = requests.get(url_id)
            response_id_data = response_id.json()
            user = response_id_data['response']['players'][0]['personaname']
            review = reviews[i]['review']
            if len(review) > 45:
                review = review[:150] + "..."
                lst_reviews.append([user, review])
            else:
                lst_reviews.append([user, review])
        return lst_reviews