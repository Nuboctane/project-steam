from tkinter import *
import ttk
from PIL import ImageTk, Image
from JSON import json_parser as JSON
import threading

class gui_class():
    def open_gui(self):
        root = Tk()
        root.configure(background='#0e0e0f')
        icon_frame = Frame(root, bg="#0e0e0f")
        icon_frame.pack()
        
        # GUI data updaten terwijl we in root.mainloop zitten
        print("fetching data...")

        main_update_thread = threading.Thread(target=gui_class.update_gui, args=(self, 50, "default", False, root))
        main_update_thread.start()
        root.title("project steam")
        root.geometry('700x450')
        root.mainloop()
    
    def update_gui(self, fetch_limit, filter_type, fetch_api_bool, root):
        
        def update_loader(ind):
            frame = loading_frames[ind].subsample(3, 3)  # Adjust subsample values as needed
            self.label.configure(image=frame)
            self.label.image = frame  # Keep a reference to avoid garbage collection
            ind += 1
            if ind == frame_count:
                ind = 0
            root.after(20, update_loader, ind)
        
        frame_count = 53
        loading_frames = [PhotoImage(file='assets/qwe_download.gif', format='gif -index %i' % i) for i in range(frame_count)]
        self.label = Label(root, width=80, height=80, background="#0e0e0f")
        self.label.pack()
        update_loader(0)

        # update json file
        if False:
            json_data_array = JSON.do_all(fetch_limit, filter_type)
            print("new json fetched")
        else:
            json_data_array = JSON.parse_json(JSON.get_json())
            print("current json fetched")

        # remove loading icon
        self.label.pack_forget()

        # nieuwe container maken om nieuwe data in te tonen
        self.card_container = LabelFrame(root, width=600, height=500)
        self.card_container.pack()

        # laadt game cards
        for card in json_data_array:
            # voor elke game in json array doe:
            None
        
    def close_gui():
        exit()