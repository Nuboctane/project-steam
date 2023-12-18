import tkinter as tk

root = tk.Tk()

canvas = tk.Canvas(root, borderwidth=0, background="#0e0e0f")
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.config(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

# Create a frame inside the canvas to hold the content
frame = tk.Frame(canvas, background="#0e0e0f")
canvas.create_window((0, 0), window=frame, anchor="nw")

# Function to update the scroll region
def update_scroll_region(event):
    canvas.config(scrollregion=canvas.bbox("all"))

# Bind frame resizing to update the scroll region
frame.bind("<Configure>", update_scroll_region)

# Add widgets/content to the frame
for i in range(20):
    tk.Label(frame, text=f"Label {i}").pack()

root.mainloop()