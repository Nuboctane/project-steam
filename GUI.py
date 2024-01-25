from tkinter import *
import ttk
from PIL import ImageTk, Image
from JSON import json_parser as JSON
from TI import TI
import threading
import requests
from io import BytesIO
import time
from ttkthemes import ThemedTk
from urllib.request import urlopen
import os
import json

class gui_class():
    def open_gui(self):
        self.root = ThemedTk(theme="arc")
        # self.root.resizable(0, 0)
        self.root.configure(background='#0e0e0f')
        icon_frame = Frame(self.root, bg="#0e0e0f")
        icon_frame.pack()
        self.canvas_frame = 0
        
        # GUI data updaten terwijl we in self.root.mainloop zitten
        print("fetching data...")

        main_update_thread = threading.Thread(target=gui_class.menu_gui, args=(self,))
        main_update_thread.start()
        self.root.title("project steam")
        # self.root.geometry('700x450')
        self.root.minsize(700, 450)
        self.root.mainloop()
    
    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def loading_icon(self):
        def update_loader(ind):
            if self.canvas_frame != 0:
                self.canvas_frame.pack_forget()

            frame = self.loading_frames[ind].subsample(3, 3)  # Adjust subsample values as needed
            try:
                self.loading_label.configure(image=frame)
                self.loading_label.image = frame  # Keep a reference to avoid garbage collection
            except:
                None
            ind += 1
            if ind == frame_count:
                ind = 0
            self.root.after(20, update_loader, ind)
        
        frame_count = 53
        self.loading_frames = [PhotoImage(file='assets/qwe_download.gif', format='gif -index %i' % i) for i in range(frame_count)]
        self.loading_label = Label(self.root, width=80, height=80, background="#0e0e0f")
        self.loading_label.pack()
        update_loader(0)

    def on_back_press(self, location):
        gui_class.clear_root(self)
        if location == "menu":
            main_update_thread = threading.Thread(target=gui_class.menu_gui, args=(self,))
        elif location == "gamelist":
            if os.stat("steam_search.json").st_size > 10:
                with open("steam_search.json", "r") as file:
                    file_as_json = json.load(file)
                    file.close()
                main_update_thread = threading.Thread(target=gui_class.game_list_gui, args=(self, 1, "default", False, file_as_json))
            else:
                main_update_thread = threading.Thread(target=gui_class.game_list_gui, args=(self, 1, "default", False, None))
        main_update_thread.start()
    
    def friends_status(self):
        gui_class.clear_root(self)
        self.back = Button(self.root, text="< Menu", bg="#3b6282", fg="#66c0f4", border=0, command=lambda: gui_class.on_back_press(self, "menu"))
        self.back.pack(anchor="w")
        self.frame_friends = Frame(self.root, bg="#0e0e0f")
        self.frame_friends.pack(pady=10)
        self.label = Label(self.frame_friends, text="search a username", bg="#0e0e0f", fg="#c7d5e0")
        self.label.grid(row=0, column=0)
        self.username_entry = Entry(self.frame_friends, bg="#1b1b1c", fg="#c7d5e0", border=0)
        self.username_entry.grid(row=1, column=0)
        self.count_friends = 0
        def on_search_press():
            username = self.username_entry.get()
            if username:
                user_info = JSON.get_user_info(username)
                username = user_info['response']['players'][0]['personaname']
                try:
                    country = user_info['response']['players'][0]['loccountrycode']
                except:
                    country = "Unknown"
                status = JSON.user_status(user_info)
                status = status.replace("status=", "")
                game_image = user_info['response']['players'][0]['avatarfull']
                response = urlopen(game_image)
                img = Image.open(BytesIO(response.read()))
                response.close()
                img = ImageTk.PhotoImage(img)
                self.count_friends
                if self.count_friends == 0:
                    self.count_friends += 1
                    self.image_label = Label(self.frame_friends, image=img)
                    self.image_label.image = img 
                    self.image_label.grid(row=2, column=0)
                    self.name_label = Label(self.frame_friends, text="Name: "+str(username), bg="#0e0e0f", fg="#c7d5e0", font=("Segoe UI", 16))
                    self.name_label.grid(row=3, column=0)
                    self.satus_label = Label(self.frame_friends, text="Status: "+str(status), bg="#0e0e0f", fg="#c7d5e0", font=("Segoe UI", 16))
                    self.satus_label.grid(row=4, column=0)
                    self.country_label = Label(self.frame_friends, text="Country: "+str(country), bg="#0e0e0f", fg="#c7d5e0", font=("Segoe UI", 16))
                    self.country_label.grid(row=5, column=0)
                else:
                    image_label = Label(self.frame_friends, image=img)
                    image_label.image = img 
                    image_label.grid(row=2, column=0)
                    self.name_label.config(text="Name: "+str(username))
                    self.satus_label.config(text="Status: "+str(status))
                    self.country_label.config(text="Country: "+str(country))
        self.search = Button(self.frame_friends, text="Search", bg="#3b6282", fg="#66c0f4", border=0, command=on_search_press)
        self.search.grid(row=1, column=1)
    
    def menu_gui(self):
        button_frame = Frame(self.root, bg="#0e0e0f")
        button_frame.pack(pady=10)
        self.label = Label(button_frame, text="Select one of the options", bg="#0e0e0f", fg="#c7d5e0", font=("Segoe UI", 16))
        self.label.pack(pady=10)

        def on_user_press():
            gui_class.clear_root(self)
            main_update_thread = threading.Thread(target=gui_class.friends_status, args=(self,))
            main_update_thread.start()

        self.users = Button(button_frame, text="Search Users", bg="#3b6282", fg="#66c0f4", border=0, command=on_user_press, height=2, width=15, font=("Segoe UI", 16))
        self.users.pack(side=LEFT, padx=10)

        def on_game_press():
            gui_class.clear_root(self)
            main_update_thread = threading.Thread(target=gui_class.game_list_gui, args=(self, 1, "default", False, None))
            main_update_thread.start()

        self.games = Button(button_frame, text="View Games", bg="#3b6282", fg="#66c0f4", border=0, command=on_game_press, height=2, width=15, font=("Segoe UI", 16))
        self.games.pack(side=LEFT, padx=10)

    def Show_game(self, game_id, json_data_array):
        gui_class.clear_root(self)
        gui_class.loading_icon(self)
        reviews = []
        positief = []
        current_review = None

        for card in json_data_array:
            for key, value in card.items():
                if 'data' in value:
                    card_data = value['data']
                    break
            for key, value in card_data.items():
                if 'steam_appid' in key:
                    app_id = value
                    break

            positief.insert(0, card["total_positive"])

            if app_id == game_id:
                current_review = card["total_reviews"]
            else:
                reviews.insert(0, card["total_reviews"])

        reviews.insert(0, current_review)

        def gradient_descent(x, y, num_iterations, learning_rate):
            coefficients = [0, 0]
            count = 0
            for _ in range(num_iterations):
                for i in range(len(x)):
                    prediction = coefficients[0] + coefficients[1] * x[i]
                    error = prediction - y[i]
                    coefficients[0] -= error * learning_rate
                    coefficients[1] -= error * x[i] * learning_rate
                    count += 1
            return coefficients
        a, b = gradient_descent(reviews, positief, 10, 0.000000000001)
        current = int(a+b*reviews[0])
        current = current*-1 if current<0 else current

        # remove loading icon
        gui_class.clear_root(self)
        
        self.previous = Button(self.root, text="< Back", bg="#3b6282", fg="#66c0f4", border=0, command=lambda: gui_class.on_back_press(self, "gamelist"))
        self.previous.pack(anchor="w")
        # get game data
        game_all = JSON.game_data(str(game_id))
        game_data = game_all[str(game_id)]['data']  
      
        # get game reviews
        game_reviews = game_all["review_score_desc"]

        # get game price
        if game_data['is_free'] == True:
            card_price = "Free To Play"
        else:
            try:
                card_price = game_data['price_overview']['final_formatted']
                card_price = card_price.replace("€", "")
                card_price = "€"+str(card_price)

            except:
                card_price = game_all["price"]
                if card_price > 0:
                    card_price = "€" + str(card_price)[:-2] + "." + str(card_price)[-2:]
                    
                if card_price == 0:
                    card_price = "3rd party"  

        # get game image
        game_image = game_data["header_image"]
        response = urlopen(game_image)
        img = Image.open(BytesIO(response.read()))
        response.close()
        
        # img = img.resize((200, 200), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)

        # get game genres
        game_genres = ""
        am = 0
        for genre in game_data['genres']:
            game_genres += (", " if am>0 else "") + genre['description']
            am+=1

        # get game categories
        # game_categories = ", ".join(category['description'] for category in game_data['categories'] if "Steam" not in category['description'] and "Valve" not in category['description'])
        game_categories = ''
        count = 0
        for category in game_data['categories']:
            if count == 6:
                break
            if count == 0:
                game_categories += category['description']
                count += 1
            else:
                if "Steam" not in category['description'] and "Valve" not in category['description']:
                    game_categories += ", " + category['description']
                    count += 1


        self.frame_game = LabelFrame(self.root, height=1, border=0, bg="#0e0e0f")
        self.frame_game.pack(anchor="w")
        
        Label(self.frame_game, text="Name: "+str(game_data['name']), bg="#0e0e0f", fg="#c7d5e0", font=("Segoe UI", 16)).grid(row=1, column=0, sticky='w')
        Label(self.frame_game, text="Price: "+str(card_price), bg="#0e0e0f", fg="#c7d5e0", font=("Segoe UI", 16)).grid(row=2, column=0, sticky='w')
        Label(self.frame_game, text="Review score: "+str(game_reviews)+" , Total/Positive: "+str(current), bg="#0e0e0f", fg="#c7d5e0", font=("Segoe UI", 16)).grid(row=3, column=0, sticky='w')
        Label(self.frame_game, text="Genres: "+str(game_genres), bg="#0e0e0f", fg="#c7d5e0", font=("Segoe UI", 16)).grid(row=4, column=0, sticky='w')
        Label(self.frame_game, text="Categories: "+str(game_categories), bg="#0e0e0f", fg="#c7d5e0", font=("Segoe UI", 16)).grid(row=5, column=0, sticky="w")
        image_label = Label(self.frame_game, image=img)
        image_label.image = img 
        image_label.grid(row=0, column=0)
        
    def game_search(self, search):
        gui_class.clear_root(self)
        gui_class.loading_icon(self)
        open('steam_search.json', 'w').close()

        def search_thread(a,b,search):
            JSON.game_search(search)

        main_update_thread = threading.Thread(target=search_thread, args=(search))
        main_update_thread.start()
        while os.stat("steam_search.json").st_size < 10:
            time.sleep(0.1)
        with open("steam_search.json", "r") as file:
            file_as_json = json.load(file)
            file.close()
        main_update_thread2 = threading.Thread(target=gui_class.game_list_gui, args=(self, 1, "default", False, file_as_json))
        main_update_thread2.start()

    def game_list_gui(self, fetch_limit, filter_type, fetch_api_bool, dataset):
        if dataset == None:
            gui_class.loading_icon(self)
        print("dataset:", len(dataset) if dataset != None else "None")
        # update json file
        if dataset == None:
            print("not using dataset")
            if fetch_api_bool:
                json_data_array = JSON.do_all(fetch_limit, filter_type)
                print("new json fetched")
            else:
                json_data_array = JSON.parse_json(JSON.get_json(), filter_type)
                try:
                    TI.send_serial("0")
                    TI.send_serial("1")
                except:
                    None
                print("current json fetched")
        else:
            print("using dataset")
            json_data_array = dataset
        
        # print(json_data_array[0])
        # remove loading icon
        time.sleep(1)
        gui_class.clear_root(self)

        # filter interface maken  
        filter_interface = LabelFrame(self.root, height=1, border=0, bg="#0e0e0f")
        self.back = Button(filter_interface, text="< Menu", bg="#3b6282", fg="#66c0f4", border=0, command=lambda: gui_class.on_back_press(self, "menu"))
        self.back.grid(row=0, column=0)
        
        self.game_entry = Entry(filter_interface, bg="#1b1b1c", fg="#c7d5e0", border=0)
        self.game_entry.grid(row=0, column=1)
        
        self.search = Button(filter_interface, text="Search", bg="#3b6282", fg="#66c0f4", border=0, command=lambda: gui_class.game_search(self, self.game_entry.get()))
        self.search.grid(row=0, column=2)
        
        filter_interface.pack(fill="x")

        # lijst data informatie koppen
        fake_game_card = LabelFrame(self.root, height=1, border=0, bg="#0e0e0f")
        fake_game_card.pack(anchor="w")

        Label(fake_game_card, text=f"[{len(json_data_array)}]", bg="#1b1b1c", fg="#c7d5e0", width=6).grid(row=0, column=0)
        Button(fake_game_card, border=0, text=" name ", bg="#1b1b1c", fg="#66c0f4", width=15, anchor='w').grid(row=0, column=1)
        Button(fake_game_card, border=0, text=" price ", bg="#1b1b1c", fg="#8eab11", width=10).grid(row=0, column=2)
        Button(fake_game_card, border=0, text=" score ", bg="#1b1b1c", fg="#c7d5e0", width=20).grid(row=0, column=3)
        Button(fake_game_card, border=0, text=" systems ", bg="#1b1b1c", fg="#4b5466", width=30).grid(row=0, column=4)
        Button(fake_game_card, border=0, text=" ages ", bg="#1b1b1c", fg="#c7d5e0", width=14).grid(row=0, column=5)

        # maak scroll frame
        self.canvas = Canvas(self.root, height=400, background="#0e0e0f", bd=0, highlightthickness=0)
        self.canvas.place(relx=0, rely=1, anchor='sw', relwidth=1)
        self.canvas_frame = Frame(self.canvas, background="#0e0e0f")
        self.canvas.create_window((0, 0), window=self.canvas_frame, anchor="nw")
        scroll = Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scroll.set)
        scroll.place(relx=0, rely=1, anchor='sw', relwidth=0)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.root.bind('<MouseWheel>', lambda scrollaction: self.canvas.yview_scroll(-5, "units") if scrollaction.delta > 0 else self.canvas.yview_scroll(5, "units")) 
        
        index = 1
        for card in json_data_array:
            # haal algemene game card data op
            for key, value in card.items():
                if 'data' in value:
                    card_data = value['data']
                    break
            
            card_age = "0"
            for key, value in card_data.items():
                if 'required_age' in key:
                    card_age = str(value)
                    break
            if card_age == "0":
                card_age = "All ages"
            else:
                card_age+="+"
            
            # haal game card review score op
            for key, value in card.items():
                if 'review_score_desc' in key:
                    card_score = value
                    break
            
            # haal game card systemen op
            card_systems = ""
            am = 0
            for key, value in card_data.items():
                if 'platforms' in key:
                    for system, bool in value.items():
                        if bool:
                            card_systems += (", " if am>0 else "") + system
                            am+=1

            for key, value in card.items():
                if 'price' in key:
                    card_price = value
                    break
            if card_data['is_free'] == True:
                card_pice = "Free To Play"
            else:
                try:
                    card_pice = card_data['price_overview']['final_formatted']
                    card_pice = card_pice.replace("€", "")
                    card_pice = "€"+str(card_pice)

                except:
                    card_pice = card_price 
                    if card_pice > 0:
                        card_pice = "€" + str(card_pice)[:-2] + "." + str(card_pice)[-2:]
                        
                    if card_pice == 0:
                        card_pice = "3rd party"
            
            # data formatten om netjes te tonen in de lijst (alleen voor de lijst weergave)
            
            # dit stukje code zorgt ervoor dat wanneer de game naam te lang is dat er ... wordt getoond
            # aan het einde van de naam
            game_name = str(card_data['name'])
            if len(game_name) > 15:
                game_name = game_name[:15] + "..."
            
            # haal game id op, deze id wordt gebruikt bij het clicken op de "view" knop
            for key, value in card_data.items():
                if 'steam_appid' in key:
                    card_id = value
                    break

            # Game card rij die in de lijst komt te staan
            game_card = LabelFrame(self.canvas_frame, height=8, relief="solid", border=0, bg="#0e0e0f")
            self.canvas.bind("<Configure>", self.canvas_frame.configure(height=self.canvas_frame.winfo_height() + 100))
            game_card.bind("<Configure>", self.canvas.configure(scrollregion=self.canvas.bbox("all")))
            game_card.pack(pady=1, fill="x", expand=True)

            Button(game_card, border=0, text='view', bg="#3b6282", fg="#66c0f4", height=2, width=6, command=lambda card_id=card_id: gui_class.Show_game(self, card_id, json_data_array)).grid(row=index, column=0)
            Label(game_card, text=" "+str(game_name)+" ", bg="#1b1b1c", fg="#66c0f4", height=2, width=15, anchor='w').grid(row=index, column=1)
            Label(game_card, text=" "+str(card_pice)+" ", bg="#1b1b1c", fg="#8eab11" if str(card_pice) == "Free To Play" else ("#f47b20" if str(card_pice) == "3rd party" else "#c7d5e0"), height=2, width=10).grid(row=index, column=2)
            Label(game_card, text=" "+str(card_score)+" ", bg="#1b1b1c", fg="#c7d5e0", height=2, width=20).grid(row=index, column=3)
            Label(game_card, text=" "+str(card_systems)+" ", bg="#1b1b1c", fg="#4b5466", height=2, width=30).grid(row=index, column=4)
            Label(game_card, text=" "+str(card_age)+" ", bg="#1b1b1c", fg="#c7d5e0", height=2, width=14).grid(row=index, column=5)
            
    def close_gui():
        exit()
