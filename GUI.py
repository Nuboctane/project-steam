import tkinter
from JSON import json_parser as JSON
import threading
class gui_class():
    def open_gui():
        """
            GUI openen
        """
        print('open gui')
    
    def update_gui(data):
        # update json file
        json_update_thread = threading.Thread(target=JSON.do_all, args=(50,"default"))
        json_update_thread.start()
        json_update_thread.join()


        """
            GUI content updaten met gegeven data
        """

    def close_gui():
        """
            GUI sluiten
        """
        print('close gui')