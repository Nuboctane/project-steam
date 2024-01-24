import json
import requests
import os
from TI import TI
from crawler import Crawler
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
        # reviews = []
        # positief = []
        for initial_segment in json_data:
            # def gradient_descent(x, y, num_iterations=1000, learning_rate=0.0001):
            #     coefficients = [0, 0]
            #     count = 0
            #     for _ in range(num_iterations):
            #         for i in range(len(x)):
            #             prediction = coefficients[0] + coefficients[1] * x[i]
            #             error = prediction - y[i]
            #             coefficients[0] -= error * learning_rate
            #             coefficients[1] -= error * x[i] * learning_rate
            #             print(f"{count} :{coefficients}")
            #             count += 1
            #     return coefficients
            # a, b = gradient_descent(reviews, positief, 10000, 0.000000000001)
            # print(a+b*reviews[1])
            match filter_type:
                case "default":
                    # filterd niks
                    main_segments.append(initial_segment)
                case "popular":
                    # maak hier een filter voor populaire spellen
                    def review_score(json_data):
                        n = len(json_data)
                        for i in range(n):
                            for j in range(0, n - i - 1):
                                if json_data[j].get('review_score') < json_data[j + 1].get('review_score'):
                                    json_data[j], json_data[j + 1] = json_data[j + 1], json_data[j]
                        return json_data
                    main_segments = review_score(json_data)
                case "price1":
                    # maak hier een filter voor prijs (laag > hoog)
                    def price1(json_data):
                        n = len(json_data)
                        
                        for i in range(n):
                                for j in range(0, n - i - 1):
                                    print(json_data[3].get('price_overview').get('final'))
                                    try:
                                        if json_data[j].get('price_overview').get('final') > json_data[j + 1].get('price_overview').get('final'):
                                            json_data[j], json_data[j + 1] = json_data[j + 1], json_data[j]
                                    except:
                                        try:
                                            if json_data[j].get('price') < json_data[j + 1].get('price'):
                                                json_data[j], json_data[j + 1] = json_data[j + 1], json_data[j]
                                        except:
                                            if json_data[j].get('is_free') == True:
                                                json_data[j], json_data[j + 1] = json_data[j + 1], json_data[j]
                        return json_data
                    main_segments = price1(json_data)
                case "price2":
                    # maak hier een filter voor prijs (hoog > laag)
                    None
                # maar zelf andere filters die je er in wilt hebben
                case "statistieken":
                    None
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

    def game_data(game_id):
        url_game_data = f"https://store.steampowered.com/api/appdetails?appids={game_id}&cc=nl"
        url_game_reviews = f"https://store.steampowered.com/appreviews/{game_id}?json=1&num_per_page=0"
        url_game_price = f"https://steamspy.com/api.php?request=appdetails&appid={game_id}"
        response_review = requests.get(url_game_reviews)
        response_game = requests.get(url_game_data)
        response_price = requests.get(url_game_price)
        if "price_overview" not in response_game.json()[str(game_id)]["data"] and response_game.json()[str(game_id)]["data"]["is_free"] == False:
                price_dict = json.loads(response_price.json()["price"])
                new_response = {**response_game.json(), **response_review.json()["query_summary"], "price": price_dict}
                return new_response
        else:
            new_response = {**response_game.json(), **response_review.json()["query_summary"]}
            return new_response

    def get_game_reviews(game_id):
        url_game_reviews = f"https://store.steampowered.com/appreviews/{game_id}?json=1&num_per_page=5"
        response_review = requests.get(url_game_reviews)
        response_review = response_review.json()
        reviews = response_review['reviews']
        lst_reviews = []
        for i in range(len(reviews)):
            user = reviews[i]['author']['steamid']
            url_id = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={os.getenv('STEAM_API_KEY')}&steamids={user}"
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
    
    def get_user_info(user_name):
        output = Crawler().crawl(user_name, validator=(lambda x: x == user_name))
        if output == []:
            return print("user not found")
        steam_id = str(output[0])
        steam_id = steam_id.split(",")
        if "profiles/" in steam_id[1]:
            steam_id = str(steam_id[1])
            steam_id = steam_id.replace("profiles/", "")
            url_id = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={os.getenv('STEAM_API_KEY')}&steamids={steam_id}"
            response_id = requests.get(url_id)
            response_id_data = response_id.json()
            return response_id_data
        else:
            steam_id = str(steam_id[1])
            steam_id = steam_id.replace("id/", "")
            url_naam = f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={os.getenv('STEAM_API_KEY')}&vanityurl={user_name}"
            response = requests.get(url_naam)
            response_data = response.json()
            if response_data["response"]["success"] == 42:
                url_naam = f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={os.getenv('STEAM_API_KEY')}&vanityurl={steam_id}"
                response = requests.get(url_naam)
                response_data = response.json()
            steam_id = response_data["response"]["steamid"]
            url_id = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={os.getenv('STEAM_API_KEY')}&steamids={steam_id}"
            response_id = requests.get(url_id)
            response_id_data = response_id.json()
            return response_id_data
        
    def user_status(response_id_data):
        status = response_id_data['response']['players'][0]['personastate']
        if status == 0:
            status = "status=Offline"
        elif status == 1:
            status = "status=Online"

        elif status == 2:
            status = "status=Busy"

        elif status == 3:
            status = "status=Away"

        elif status == 4:
            status = "status=Snooze"

        elif status == 5:
            status = "status=Looking to trade"

        elif status == 6:
            status = "status=Looking to play"
        try:
            TI.send_serial(status)
        except:
            None
        return status