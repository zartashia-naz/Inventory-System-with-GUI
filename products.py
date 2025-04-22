from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkcalendar import DateEntry
class Products:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1045x650+225+160")
        self.root.title("Inventory Management System")
        self.root.focus_force()


        pro_left_frame=Frame(self.root, bd=2, relief=RIDGE)
        pro_left_frame.place(x=20,y=50)
        
        self.pro_header_label=Label(pro_left_frame, text="Manage Employee Details",bg="#9370DB", fg="white", font=("Times New Roman", 25,"bold"), justify=CENTER)
        self.pro_header_label.grid(row=0,columnspan=2)

        cat_lbl=Label(pro_left_frame, text="Category", font=("Times New Roman", 15))
        cat_lbl.grid(row=1, column=0,sticky="w",pady=20,padx=20)
        cat_combobox=ttk.Combobox(pro_left_frame,font=("Times New Roman", 15), state="readonly")
        cat_combobox.set("Empty")
        cat_combobox.grid(row=1,column=1)

        sup_lbl=Label(pro_left_frame, text="Supplier", font=("Times New Roman", 15))
        sup_lbl.grid(row=2, column=0,sticky="w",pady=20,padx=20)
        sup_combobox=ttk.Combobox(pro_left_frame,font=("Times New Roman", 15), state="readonly")
        sup_combobox.set("Empty")
        sup_combobox.grid(row=2,column=1)

        name_lbl=Label(pro_left_frame, text="Name", font=("Times New Roman", 15))
        name_lbl.grid(row=3, column=0,sticky="w",pady=20,padx=20)
        name_entry=Entry(pro_left_frame, font=("Times New Roman", 15),bg="light yellow")
        name_entry.grid(row=3, column=1,pady=20,padx=20)

        price_lbl=Label(pro_left_frame, text="Price", font=("Times New Roman", 15))
        price_lbl.grid(row=4, column=0,sticky="w",pady=20,padx=20)
        price_entry=Entry(pro_left_frame, font=("Times New Roman", 15),bg="light yellow")
        price_entry.grid(row=4, column=1,pady=20,padx=20)


        quantity_lbl=Label(pro_left_frame, text="Quanity", font=("Times New Roman", 15))
        quantity_lbl.grid(row=5, column=0,sticky="w",pady=20,padx=20)
        quantity_entry=Entry(pro_left_frame, font=("Times New Roman", 15),bg="light yellow")
        quantity_entry.grid(row=5, column=1,pady=20,padx=20)

        status_lbl=Label(pro_left_frame, text="Status", font=("Times New Roman", 15))
        status_lbl.grid(row=6, column=0,sticky="w",pady=20,padx=20)
        status_combobox=ttk.Combobox(pro_left_frame,font=("Times New Roman", 15), state="readonly",values=("Active","Inactive"))
        status_combobox.set("Search")
        status_combobox.grid(row=6,column=1)

        btn_frame=Button(pro_left_frame)
        btn_frame.grid(row=7,columnspan=3)


        add_button=Button(btn_frame,text="Add",font=("Times New Roman", 20),bg="blue",fg="white",activeforeground="white",cursor = 'hand2',width=8)
        add_button.grid(row=7, column=0)


        update_button=Button(btn_frame,text="Update",font=("Times New Roman", 20),bg="blue",fg="white",activeforeground="white",cursor = 'hand2',width=8)
        update_button.grid(row=7, column=1)


        delete_button=Button(btn_frame,text="Delete",font=("Times New Roman", 20),bg="blue",fg="white",activeforeground="white",cursor = 'hand2',width=8)
        delete_button.grid(row=7, column=2)


     
        clear_button=Button(btn_frame,text="Clear",font=("Times New Roman",20),bg="blue",fg="white",activeforeground="white",cursor = 'hand2',width=8)
        clear_button.grid(row=7, column=3)


        search_frame=LabelFrame(self.root, text="Search Product",font=("Times New Roman", 20))
        search_frame.place(x=500,y=40)

        search_combobox=ttk.Combobox(search_frame, values=("Category", "Supplier", "Name", "Status"), font=("Times New Roman",14))
        search_combobox.grid(row=0, column=0)
        search_entry=Entry(search_frame, font=("Times New Roman", 14),bg="light yellow")
        search_entry.grid(row=0, column=1)


        search_button=Button(search_frame,text="Search",font=("Times New Roman", 18),bg="blue",fg="white",activeforeground="white",cursor = 'hand2',width=8)
        search_button.grid(row=0, column=2, padx=(10,0),pady=10)

        show_button=Button(search_frame,text="Show All",font=("Times New Roman", 18),bg="blue",fg="white",activeforeground="white",cursor = 'hand2',width=8)
        show_button.grid(row=0, column=3, pady=10)
        

        treeview_frame=Frame(self.root)
        treeview_frame.place(x=500,y=125, height=430, width=540)

        horizontal_scrollbar=Scrollbar(treeview_frame, orient="horizontal")
        vertcal_scrollbar=Scrollbar(treeview_frame,orient="vertical")

        self.treeview=ttk.Treeview(treeview_frame, columns=("category","supplier","name","price","quantity","status"), show="headings",yscrollcommand=vertcal_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
 
        horizontal_scrollbar.pack(side=BOTTOM, fill=X)
        vertcal_scrollbar.pack(side=RIGHT,fill=Y,pady=(10,0))
        horizontal_scrollbar.config(command=self.treeview.xview)
        vertcal_scrollbar.config(command=self.treeview.yview)
        self.treeview.pack(fill=BOTH, expand=1) 


        self.treeview.heading("category", text="Category")
        self.treeview.heading("supplier", text="Supplier")
        self.treeview.heading("name", text="Name")
        self.treeview.heading("price", text="Price")
        self.treeview.heading("quantity", text="Quantity")
        self.treeview.heading("status", text="Status")




if __name__=="__main__":
        root = Tk()
        obj = Products(root)
        root.mainloop()