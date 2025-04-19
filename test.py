from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkvideo import tkvideo
import os

class Category:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x700+100+50")
        self.root.title("Inventory Management System")
        
        # Header
        self.emp_header_label = Label(self.root, text="Manage Category Details", bg="#9370DB", 
                                    fg="white", font=("Times New Roman", 30, "bold"), justify=CENTER)
        self.emp_header_label.place(x=0, y=0, relwidth=1)

        # Left Frame (Existing Form)
        left_frame = Frame(self.root, bg="white")
        left_frame.place(x=20, y=100, width=500, height=580)

        # Your existing form components
        cat_details_frame = Frame(left_frame, bg="white")
        cat_details_frame.pack(pady=20)

        # Category ID
        Label(cat_details_frame, text="Category ID", font=("Times new roman", 15), bg="white").grid(row=0, column=0, padx=20, pady=15, sticky="w")
        Entry(cat_details_frame, font=("Times new roman", 15), bg="light yellow").grid(row=0, column=1, padx=20, pady=15)

        # Category Name
        Label(cat_details_frame, text="Category Name", font=("Times new roman", 15), bg="white").grid(row=1, column=0, padx=20, pady=15, sticky="w")
        Entry(cat_details_frame, font=("Times new roman", 15), bg="light yellow").grid(row=1, column=1, padx=20, pady=20)

        # Description
        Label(cat_details_frame, text="Category Description", font=("Times new roman", 15), bg="white").grid(row=2, column=0, padx=20, pady=15, sticky="nw")
        Text(cat_details_frame, width=20, height=6, font=("Times new roman", 15), bg="light yellow").grid(row=2, column=1, padx=20, pady=15)

        # Buttons
        btn_frame = Frame(left_frame, bg="white")
        btn_frame.pack(pady=20)
        Button(btn_frame, text="Add", font=("Times New Roman", 20), bg="blue", fg="white", width=8).grid(row=0, column=1, padx=20, pady=10)
        Button(btn_frame, text="Delete", font=("Times New Roman", 20), bg="blue", fg="white", width=8).grid(row=0, column=2, padx=5, pady=10)

        # Treeview
        treeview_frame = Frame(left_frame, bg="white")
        treeview_frame.pack(pady=20)
        
        # Scrollbars and Treeview (your existing code)
        # ...

        # Right Frame (Video)
        right_frame = Frame(self.root, bg="white")
        right_frame.place(x=550, y=100, width=600, height=580)
        
        # Video Label
        video_label = Label(right_frame, bg="black")
        video_label.pack(pady=20, fill=BOTH, expand=True)
        
        # Load and play video
        video_file = "/Users/macbookpro/Desktop/python projects/Inventory-System-with-GUI/assets/Inventory.mp4"
        
        if os.path.exists(video_file):
            # Simple video player with tkvideo
            player = tkvideo(video_file, video_label, loop=1, size=(600, 400))
            player.play()
        else:
            Label(right_frame, text="Video file not found!", fg="red").pack()

if __name__ == "__main__":
    root = Tk()
    obj = Category(root)
    root.mainloop()