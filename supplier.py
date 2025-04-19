from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkcalendar import DateEntry
class Supplier:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1045x650+225+160")
        self.root.title("Inventory Management System")

        self.supplier_header_lbl=Label(self.root, text="Manage Supplier Details", bg="#9370DB", fg="white", font=("Times New Roman", 30,"bold"), justify=CENTER)
        self.supplier_header_lbl.place(x=0,y=0,relwidth=1)


        self.left_frame=Frame(self.root)
        self.left_frame.place(x=10,y=100)

        self.sup_name=Label(self.left_frame, text="Invoice No.", font=("Times New Roman", 15))
        self.sup_name.grid(row=0, column=0, padx=(20,20),sticky="w")
        self.invoice_entry=Entry(self.left_frame, font=("Times new roman", 15),bg="light yellow")
        self.invoice_entry.grid(row=0, column=1,pady=15, padx=20)


        self.sup_name=Label(self.left_frame, text="Supplier Name", font=("Times New Roman", 15))
        self.sup_name.grid(row=1, column=0, padx=20, pady=20,sticky="w")
        self.sup_entry=Entry(self.left_frame, font=("Times new roman", 15),bg="light yellow")
        self.sup_entry.grid(row=1, column=1,pady=15, padx=20)
                                 

        self.contact=Label(self.left_frame, text="Contact No.", font=("Times New Roman", 15))
        self.contact.grid(row=2, column=0, padx=20, pady=20,sticky="w")
        self.contact_entry=Entry(self.left_frame, font=("Times new roman", 15),bg="light yellow")
        self.contact_entry.grid(row=2, column=1,pady=15, padx=20)


        self.description=Label(self.left_frame, text="Description", font=("Times New Roman", 15))
        self.description.grid(row=3, column=0, padx=20, pady=20,sticky="nw")
        self.description_entry=Text(self.left_frame,font=("Times new roman", 15), height=6, width=20, bd=2, bg="light yellow")
        self.description_entry.grid(row=3, column=1, padx=20)


        self.btn_frame=Frame(self.left_frame)
        self.btn_frame.grid(row=4,columnspan=2, pady=15)

        add_button=Button(self.btn_frame,text="Add",font=("Times New Roman", 20),bg="blue",fg="white",activeforeground="white",cursor = 'hand2',width=8)
        add_button.grid(row=4, column=1,padx=10)


        update_button=Button(self.btn_frame,text="Update",font=("Times New Roman", 20),bg="blue",fg="white",activeforeground="white",cursor = 'hand2',width=8)
        update_button.grid(row=4, column=2,padx=10)


        delete_button=Button(self.btn_frame,text="Delete",font=("Times New Roman", 20),bg="blue",fg="white",activeforeground="white",cursor = 'hand2',width=8)
        delete_button.grid(row=4, column=3,padx=10)


     
        clear_button=Button(self.btn_frame,text="Clear",font=("Times New Roman",20),bg="blue",fg="white",activeforeground="white",cursor = 'hand2',width=8)
        clear_button.grid(row=4, column=4,padx=10)


        self.right_frame=Frame(self.root)
        self.right_frame.place(x=550, y=110,width=500, height=340)

        self.search_frame=Frame(self.right_frame)
        self.search_frame.pack(pady=20)


        self.search_by_inv=Label(self.search_frame, text="Invoice No.", font=("Times New Roman", 15))
        self.search_by_inv.grid(row=0, column=0, padx=10,sticky="w")
        self.invoice_entry=Entry(self.search_frame, font=("Times new roman", 15),bg="light yellow",width=10)
        self.invoice_entry.grid(row=0, column=1, padx=10)

        search_button=Button(self.search_frame,text="Search",font=("Times New Roman", 20),bg="blue",fg="white",activeforeground="white",cursor = 'hand2',width=8)
        search_button.grid(row=0,column=2,padx=5)



        show_all_button=Button(self.search_frame,text="Show All",font=("Times New Roman", 20),bg="blue",fg="white",activeforeground="white",cursor = 'hand2',width=8)
        show_all_button.grid(row=0,column=3)


        horizontal_scrollbar=Scrollbar(self.right_frame, orient="horizontal")
        vertcal_scrollbar=Scrollbar(self.right_frame,orient="vertical")

        self.treeview=ttk.Treeview(self.right_frame, columns=("invoice","name","contact","description"), show="headings",yscrollcommand=vertcal_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
 
        horizontal_scrollbar.pack(side=BOTTOM, fill=X)
        vertcal_scrollbar.pack(side=RIGHT,fill=Y,pady=(10,0))
        horizontal_scrollbar.config(command=self.treeview.xview)
        vertcal_scrollbar.config(command=self.treeview.yview)
        self.treeview.pack(fill=BOTH, expand=1) 


        self.treeview.heading("invoice",text="Invoice Id")
        self.treeview.heading("name",text="Name")
        self.treeview.heading("contact",text="Contact")    
        self.treeview.heading("description",text="Description")

        self.treeview.column('invoice', width=80)
        self.treeview.column('name', width=160)
        self.treeview.column('contact', width=120)
        self.treeview.column('description', width=300)


if __name__=="__main__":
        root = Tk()
        obj = Supplier(root)
        root.mainloop()