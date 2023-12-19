from tkinter import *
import ttk
from PIL import ImageTk, Image
from JSON import json_parser as JSON
import threading
import requests
from io import BytesIO
import time
from ttkthemes import ThemedTk

class gui_class():
    def open_gui(self):
        self.root = ThemedTk(theme="arc")
        self.root.resizable(0, 0)
        self.root.configure(background='#0e0e0f')
        icon_frame = Frame(self.root, bg="#0e0e0f")
        icon_frame.pack()
        
        # GUI data updaten terwijl we in self.root.mainloop zitten
        print("fetching data...")

        main_update_thread = threading.Thread(target=gui_class.update_gui, args=(self, 1, "default", False))
        main_update_thread.start()
        self.root.title("project steam")
        self.root.geometry('700x450')
        self.root.mainloop()
    
    def update_gui(self, fetch_limit, filter_type, fetch_api_bool):
        
        def update_loader(ind):
            frame = loading_frames[ind].subsample(3, 3)  # Adjust subsample values as needed
            self.label.configure(image=frame)
            self.label.image = frame  # Keep a reference to avoid garbage collection
            ind += 1
            if ind == frame_count:
                ind = 0
            self.root.after(20, update_loader, ind)
        
        frame_count = 53
        loading_frames = [PhotoImage(file='assets/qwe_download.gif', format='gif -index %i' % i) for i in range(frame_count)]
        self.label = Label(self.root, width=80, height=80, background="#0e0e0f")
        self.label.pack()
        update_loader(0)

        # update json file
        if fetch_api_bool:
            json_data_array = JSON.do_all(fetch_limit, filter_type)
            print("new json fetched")
        else:
            json_data_array = JSON.parse_json(JSON.get_json(), filter_type)
            print("current json fetched")

        time.sleep(1)
        # remove loading icon
        self.label.pack_forget()

        # filter interface maken
        refresh = Button(self.root, text="refresh", border=0, bg="#2a475e", fg="#66c0f4")
        refresh.pack(pady=1, padx=5, anchor="w")
        
        # lijst data informatie koppen
        fake_game_card = LabelFrame(self.root, height=1, border=0, bg="#0e0e0f")
        fake_game_card.pack(anchor="w")

        Label(fake_game_card, bg="#1b1b1c", fg="#1b1b1c", width=6).grid(row=0, column=0)
        Label(fake_game_card, text=" name ", bg="#1b1b1c", fg="#66c0f4", width=15, anchor='w').grid(row=0, column=1)
        Label(fake_game_card, text=" price ", bg="#1b1b1c", fg="#2a475e", width=10).grid(row=0, column=2)
        Label(fake_game_card, text=" score ", bg="#1b1b1c", fg="#c7d5e0", width=20).grid(row=0, column=3)
        Label(fake_game_card, text=" systems ", bg="#1b1b1c", fg="#3e4554", width=30).grid(row=0, column=4)

        # maak scroll frame
        self.canvas = Canvas(self.root, height=385, background="#0e0e0f")
        self.canvas.place(relx=0, rely=1, anchor='sw', relwidth=1)
        self.canvas_frame = Frame(self.canvas, background="#0e0e0f")
        self.canvas.create_window((0, 0), window=self.canvas_frame, anchor="nw")
        scroll = Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scroll.set)
        scroll.place(relx=0, rely=1, anchor='sw', relwidth=0)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.root.bind('<MouseWheel>', lambda a: self.canvas.yview_scroll(-5, "units") if a.delta > 0 else self.canvas.yview_scroll(5, "units")) 
        
        index = 1
        for card in json_data_array:
            # haal algemene game card data op
            for key, value in card.items():
                if 'data' in value:
                    card_data = value['data']
                    break
            
            # haal game card review score op
            for key, value in card.items():
                if 'review_score_desc' in key:
                    card_score = value
                    break
                        
            for key, value in card.items():
                if 'price' in key:
                    card_price = value
                    break
            if card_data['is_free'] == True:
                card_pice = "€0.00"
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
            
            card_systems = "windows, mac, linux, vr, steamdeck"
            
            # data formatten om netjes te tonen in de lijst (alleen voor de lijst weergave)
            
            # dit stukje code zorgt ervoor dat wanneer de game naam te lang is dat er ... wordt getoond
            # aan het einde van de naam
            game_name = str(card_data['name'])
            if len(game_name) > 15:
                game_name = game_name[:15] + "..."
            
            # haal game id op, deze id wordt gebruikt bij het clicken op de "view" knop
            card_id = card_data['steam_appid']
            
            # Game card rij die in de lijst komt te staan
            game_card = LabelFrame(self.canvas_frame, height=8, relief="solid", border=0, bg="#0e0e0f")
            self.canvas.bind("<Configure>", self.canvas_frame.configure(height=self.canvas_frame.winfo_height() + 40))
            game_card.bind("<Configure>", self.canvas.configure(scrollregion=self.canvas.bbox("all")))
            game_card.pack(pady=1, fill="x", expand=True)

            Button(game_card, border=0, text='view', bg="#2a475e", fg="#66c0f4", height=2, width=6).grid(row=index, column=0)
            Label(game_card, text=" "+str(game_name)+" ", bg="#1b1b1c", fg="#66c0f4", height=2, width=15, anchor='w').grid(row=index, column=1)
            Label(game_card, text=" "+str(card_pice)+" ", bg="#1b1b1c", fg="#2a475e", height=2, width=10).grid(row=index, column=2)
            Label(game_card, text=" "+str(card_score)+" ", bg="#1b1b1c", fg="#c7d5e0", height=2, width=20).grid(row=index, column=3)
            Label(game_card, text=" "+str(card_systems)+" ", bg="#1b1b1c", fg="#3e4554", height=2, width=30).grid(row=index, column=4)

    def close_gui():
        exit()


           