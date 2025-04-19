from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkcalendar import DateEntry
from tkvideo import tkvideo
import os
class Category:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1045x650+225+160")
        self.root.title("Inventory Management System")
        
        self.emp_header_label=Label(self.root, text="Manage Category Details", bg="#9370DB", fg="white", font=("Times New Roman", 30,"bold"), justify=CENTER)
        self.emp_header_label.place(x=0,y=0,relwidth=1)


        cat_details_frame=Frame(self.root)
        cat_details_frame.place(x=0, y=100)

        cat_name_lbl=Label(cat_details_frame, text="Category ID", font=("Times new roman", 15))
        cat_name_lbl.grid(row=0,column=0,padx=20,pady=15,sticky="w")
        cat_entry=Entry(cat_details_frame, font=("Times new roman", 15),bg="light yellow")
        cat_entry.grid(row=0, column=1, padx=20,pady=15)

        cat_name_lbl=Label(cat_details_frame, text="Category Name", font=("Times new roman", 15))
        cat_name_lbl.grid(row=1,column=0,padx=20,pady=15,sticky="w")
        cat_name_entry=Entry(cat_details_frame, font=("Times new roman", 15),bg="light yellow")
        cat_name_entry.grid(row=1, column=1, padx=20,pady=20)

        cat_desc_lnl=Label(cat_details_frame, text="Category Description", font=("Times new roman", 15))
        cat_desc_lnl.grid(row=2,column=0,padx=20,pady=15,sticky="nw")
        cat_desc_txt=Text(cat_details_frame, width=20, height=6,font=("Times new roman", 15),bg="light yellow")
        cat_desc_txt.grid(row=2,column=1, padx=20,pady=15)

        btn_frame=Frame(self.root)
        btn_frame.place(x=80, y=350)

        add_button=Button(btn_frame,text="Add",font=("Times New Roman", 20),bg="blue",fg="white",activeforeground="white",cursor = 'hand2',width=8)
        add_button.grid(row=0, column=1,padx=20,pady=10)


        delete_button=Button(btn_frame,text="Delete",font=("Times New Roman", 20),bg="blue",fg="white",activeforeground="white",cursor = 'hand2',width=8)
        delete_button.grid(row=0, column=2,padx=5,pady=10)


        treeview_frame=Frame(self.root)
        treeview_frame.place(x=30, y=430,height=200,width=500)


        horizontal_scrollbar=Scrollbar(treeview_frame, orient="horizontal")
        vertcal_scrollbar=Scrollbar(treeview_frame,orient="vertical")

        self.treeview=ttk.Treeview(treeview_frame, columns=("catID","cat_name","cat_desc"), show="headings",yscrollcommand=vertcal_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
 
        horizontal_scrollbar.pack(side=BOTTOM, fill=X)
        vertcal_scrollbar.pack(side=RIGHT,fill=Y,pady=(10,0))
        horizontal_scrollbar.config(command=self.treeview.xview)
        vertcal_scrollbar.config(command=self.treeview.yview)
        self.treeview.pack(fill=BOTH, expand=1) 

        self.treeview.heading("catID", text="Category ID")
        self.treeview.heading("cat_name", text="Category Name")
        self.treeview.heading("cat_desc", text="Description")


        self.treeview.column("catID", width=80)
        self.treeview.column("cat_name", width=180)
        self.treeview.column("cat_desc", width=200)

        video_label = Label(self.root)
        video_label.place(x=600,y=100)
        video_file = "/Users/macbookpro/Desktop/python projects/Inventory-System-with-GUI/assets/Inventory.mp4"

        if os.path.exists(video_file):
            # Simple video player with tkvideo
            player = tkvideo(video_file, video_label, loop=1, size=(400, 500))
            player.play()
        else:
            Label(self.root, text="Video file not found!").pack()


if __name__=="__main__":
        root = Tk()
        obj = Category(root)
        root.mainloop()