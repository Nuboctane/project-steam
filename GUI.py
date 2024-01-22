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
        # main_update_thread = threading.Thread(target=gui_class.login_gui, args=(self,))
        # main_update_thread = threading.Thread(target=gui_class.game_list_gui, args=(self, 1, "default", False))
        main_update_thread.start()
        self.root.title("project steam")
        # self.root.geometry('700x450')
        self.root.minsize(700, 450)
        self.root.mainloop()

    def friends_status(self):
        self.frame_friends = Frame(self.root, bg="#0e0e0f")
        self.frame_friends.pack(pady=10)

        self.label = Label(self.frame_friends, text="Put in a username", bg="#0e0e0f", fg="#c7d5e0")
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

        def on_back_press():
            self.back.pack_forget()
            self.frame_friends.pack_forget()
            main_update_thread = threading.Thread(target=gui_class.menu_gui, args=(self,))
            main_update_thread.start()
        self.back = Button(self.root, text="< Back", bg="#3b6282", fg="#66c0f4", border=0, command=lambda: on_back_press())
        self.back.pack()


    
    
    def menu_gui(self):
        button_frame = Frame(self.root, bg="#0e0e0f")
        button_frame.pack(pady=10)
        self.label = Label(button_frame, text="Select one of the options", bg="#0e0e0f", fg="#c7d5e0", font=("Segoe UI", 16))
        self.label.pack(pady=10)

        def on_user_press():
            self.label.pack_forget()
            button_frame.pack_forget()
            main_update_thread = threading.Thread(target=gui_class.friends_status, args=(self,))
            main_update_thread.start()
        self.users = Button(button_frame, text="Friends", bg="#3b6282", fg="#66c0f4", border=0, command=on_user_press, height=2, width=15, font=("Segoe UI", 16))
        self.users.pack(side=LEFT, padx=10)

        def on_game_press():
            self.label.pack_forget()
            button_frame.pack_forget()
            main_update_thread = threading.Thread(target=gui_class.game_list_gui, args=(self, 1, "default", False))
            main_update_thread.start()
        self.games = Button(button_frame, text="Game List", bg="#3b6282", fg="#66c0f4", border=0, command=on_game_press, height=2, width=15, font=("Segoe UI", 16))
        self.games.pack(side=LEFT, padx=10)
        
        def on_game_search_press():
            self.label.pack_forget()
            button_frame.pack_forget()
            main_update_thread = threading.Thread(target=gui_class.game_search_gui, args=(self,))
            main_update_thread.start()
        self.settings = Button(button_frame, text="Game search", bg="#3b6282", fg="#66c0f4", border=0, command=on_game_search_press, height=2, width=15, font=("Segoe UI", 16))
        self.settings.pack(padx=10)

    def game_search_gui(self):
        self.label = Label(self.root, text="Input game name", bg="#0e0e0f", fg="#c7d5e0")
        self.label.pack()
        self.game_name = Entry(self.root, bg="#1b1b1c", fg="#c7d5e0", border=0)
        self.game_name.pack()

        def on_button_press(self):
            game_name = self.game_name.get()
            if game_name:
                list_games = JSON.game_search(game_name)
                self.label.pack_forget()
                self.game_name.pack_forget()
                self.button.pack_forget()
                self.back.pack_forget()
                frame_games = Frame(self.root, bg="#0e0e0f")
                frame_games.pack(pady=10)

                # Create a dictionary with game names as keys and game IDs as values
                games_dict = {game['name']: game['appid'] for game in list_games}

                selected_option = StringVar()
                dropdown = ttk.Combobox(master=frame_games, textvariable=selected_option, values=list(games_dict.keys()), background='#ffd53c', width=50)
                button = Button(master=frame_games, text="Volgende", command=lambda: on_view_press(self, selected_option.get()))
                dropdown.pack()
                button.pack()
                def on_view_press(self, game_name):
                    dropdown.pack_forget()
                    button.pack_forget()
                    game_id = games_dict[game_name]
                    try:
                        TI.send_serial(game_name)
                    except:
                        None
                    gui_class.Show_game(self, game_id)

        self.button = Button(self.root, text="Search", bg="#3b6282", fg="#66c0f4", border=0, command=lambda: on_button_press(self))
        self.button.pack()

        def on_back_press():
            self.label.pack_forget()
            self.game_name.pack_forget()
            self.button.pack_forget()
            self.back.pack_forget()
            main_update_thread = threading.Thread(target=gui_class.menu_gui, args=(self,))
            main_update_thread.start()
        self.back = Button(self.root, text="< Back", bg="#3b6282", fg="#66c0f4", border=0, command=lambda: on_back_press())
        self.back.pack()

    def Show_game(self, game_id):
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

        def on_back_press():
            self.frame_game.pack_forget()
            self.canvas.place_forget()
            main_update_thread = threading.Thread(target=gui_class.game_list_gui, args=(self, 1, "default", False))
            main_update_thread.start()
        Button(self.frame_game, text="< Back", border=0, bg="#3b6282", fg="#66c0f4", width=13, command=lambda: on_back_press()).grid(row=6, column=0)
        Label(self.frame_game, text="Name: "+str(game_data['name']), bg="#0e0e0f", fg="#c7d5e0", font=("Segoe UI", 16)).grid(row=1, column=0, sticky='w')
        Label(self.frame_game, text="Price: "+str(card_price), bg="#0e0e0f", fg="#c7d5e0", font=("Segoe UI", 16)).grid(row=2, column=0, sticky='w')
        Label(self.frame_game, text="Review score: "+str(game_reviews), bg="#0e0e0f", fg="#c7d5e0", font=("Segoe UI", 16)).grid(row=3, column=0, sticky='w')
        Label(self.frame_game, text="Genres: "+str(game_genres), bg="#0e0e0f", fg="#c7d5e0", font=("Segoe UI", 16)).grid(row=4, column=0, sticky='w')
        Label(self.frame_game, text="Categories: "+str(game_categories), bg="#0e0e0f", fg="#c7d5e0", font=("Segoe UI", 16)).grid(row=5, column=0, sticky="w")
        image_label = Label(self.frame_game, image=img)
        image_label.image = img 
        image_label.grid(row=0, column=0)
        
    def game_list_gui(self, fetch_limit, filter_type, fetch_api_bool):
        
        def update_loader(ind):
            if self.canvas_frame != 0:
                self.canvas_frame.pack_forget()

            frame = self.loading_frames[ind].subsample(3, 3)  # Adjust subsample values as needed
            self.loading_label.configure(image=frame)
            self.loading_label.image = frame  # Keep a reference to avoid garbage collection
            ind += 1
            if ind == frame_count:
                ind = 0
            self.root.after(20, update_loader, ind)
        
        frame_count = 53
        self.loading_frames = [PhotoImage(file='assets/qwe_download.gif', format='gif -index %i' % i) for i in range(frame_count)]
        self.loading_label = Label(self.root, width=80, height=80, background="#0e0e0f")
        self.loading_label.pack()
        update_loader(0)

        # update json file
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
            
        time.sleep(1)
        # remove loading icon
        self.loading_label.pack_forget()

        # filter interface maken
        def on_back_press():
            self.loading_label.pack_forget()
            filter_interface.pack_forget()
            fake_game_card.pack_forget()
            game_card.pack_forget()
            self.canvas.place_forget()
            main_update_thread = threading.Thread(target=gui_class.menu_gui, args=(self,))
            main_update_thread.start()
        filter_interface = LabelFrame(self.root, height=1, border=0, bg="#0e0e0f")
        filter_interface.pack(anchor="w")
        Button(filter_interface, text="< Back", border=0, bg="#3b6282", fg="#66c0f4", width=13, command=lambda: on_back_press()).grid(row=0, column=0)
        
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
            # card_id = card_data['steam_appid']
            
            def on_view_press(self, card_id):
                filter_interface.pack_forget()
                fake_game_card.pack_forget()
                game_card.pack_forget()
                self.canvas.place_forget()
                gui_class.Show_game(self, card_id)
            
            # Game card rij die in de lijst komt te staan
            game_card = LabelFrame(self.canvas_frame, height=8, relief="solid", border=0, bg="#0e0e0f")
            self.canvas.bind("<Configure>", self.canvas_frame.configure(height=self.canvas_frame.winfo_height() + 100))
            game_card.bind("<Configure>", self.canvas.configure(scrollregion=self.canvas.bbox("all")))
            game_card.pack(pady=1, fill="x", expand=True)

            Button(game_card, border=0, text='view', bg="#3b6282", fg="#66c0f4", height=2, width=6, command=lambda card_id=card_id: on_view_press(self, card_id)).grid(row=index, column=0)
            Label(game_card, text=" "+str(game_name)+" ", bg="#1b1b1c", fg="#66c0f4", height=2, width=15, anchor='w').grid(row=index, column=1)
            Label(game_card, text=" "+str(card_pice)+" ", bg="#1b1b1c", fg="#8eab11" if str(card_pice) == "Free To Play" else ("#f47b20" if str(card_pice) == "3rd party" else "#c7d5e0"), height=2, width=10).grid(row=index, column=2)
            Label(game_card, text=" "+str(card_score)+" ", bg="#1b1b1c", fg="#c7d5e0", height=2, width=20).grid(row=index, column=3)
            Label(game_card, text=" "+str(card_systems)+" ", bg="#1b1b1c", fg="#4b5466", height=2, width=30).grid(row=index, column=4)
            Label(game_card, text=" "+str(card_age)+" ", bg="#1b1b1c", fg="#c7d5e0", height=2, width=14).grid(row=index, column=5)
            
    def close_gui():
        exit()
