from tkinter import *
import ttk
from PIL import ImageTk, Image
from JSON import json_parser as JSON
import threading

class gui_class():
    def open_gui():
        root = Tk()
        root.configure(background='#171d25')
        icon_frame = Frame(root, bg="#ffc917")
        icon_frame.pack()

        def update(ind):
            frame = loading_frames[ind]
            label.configure(image=frame)
            ind += 1
            if ind == frame_count:
                ind = 0
            root.after(10, update, ind)
        
        frame_count = 63
        loading_frames = [PhotoImage(file='assets/qwe_download.gif', format='gif -index %i' % i) for i in range(frame_count)]
        label = Label(root)
        label.pack()

        # GUI data updaten terwijl we in root.mainloop zitten
        print("updating...")
        main_update_thread = threading.Thread(target=gui_class.update_gui, args=(50, "default"))
        main_update_thread.start()
        # main_update_thread.join()

        update(0)
        root.title("project steam")
        root.geometry('700x450')
        root.mainloop()
    
    def update_gui(fetch_limit, filter_type):
        # update json file
        json_update_thread = threading.Thread(target=JSON.do_all, args=(fetch_limit, filter_type))
        json_update_thread.start()
        json_update_thread.join()
        print("updated")
        
    def close_gui():
        exit()