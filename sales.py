from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
import os
class Sales:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1045x650+225+160")
        self.root.title("Inventory Management System")
        self.root.focus_force()
        self.bill_list=[]
        self.var_invoice=StringVar()


        self.sales_header_label=Label(self.root, text="View Customer Bills", bg="#9370DB", fg="white", font=("Times New Roman", 30,"bold"), justify=CENTER)
        self.sales_header_label.place(x=0,y=0,relwidth=1)

        search_frame=Frame(self.root)
        search_frame.place(x=30,y=100,width=550)
       
        invoice_lbl=Label(search_frame,text="Invoice No.",font=("Times New Roman", 15))
        invoice_lbl.grid(row=0, column=0,sticky="w")
        invoice_entry=Entry(search_frame,textvariable=self.var_invoice,font=("Times New Roman", 15), bg="light yellow")
        invoice_entry.grid(row=0,column=1,padx=10)

        search_button=Button(search_frame,text="Search",font=("Times New Roman", 20),command=self.search,bg="blue",fg="white",activeforeground="white",cursor = 'hand2',width=8)
        search_button.grid(row=0,column=2,padx=5)

        clear_button=Button(search_frame,text="Clear",font=("Times New Roman", 20),command=self.clear,bg="blue",fg="white",activeforeground="white",cursor = 'hand2',width=8)
        clear_button.grid(row=0,column=3,padx=5)

        sales_frame=Frame(self.root, bd=2, relief=RIDGE)
        sales_frame.place(x=30,y=150,width=200,height=350)


        vertcal_scrollbar=Scrollbar(sales_frame,orient="vertical")
        self.sales_listbox=Listbox(sales_frame,font=("Times New Roman", 20),bg="white",yscrollcommand=vertcal_scrollbar)
        vertcal_scrollbar.pack(side=RIGHT,fill=Y)
        vertcal_scrollbar.config(command=self.sales_listbox.yview)
        self.sales_listbox.pack(fill=BOTH, expand=1)
        self.sales_listbox.bind("<ButtonRelease-1>",self.get_data)



        bill_frame=Frame(self.root, bd=2, relief=RIDGE)
        bill_frame.place(x=260,y=150,width=410,height=350)


        vertcal_scrollbar2=Scrollbar(bill_frame,orient="vertical")
        self.bill_area=Text(bill_frame,font=("Times New Roman", 20),bg="white",yscrollcommand=vertcal_scrollbar2)
        vertcal_scrollbar2.pack(side=RIGHT,fill=Y)
        vertcal_scrollbar2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH, expand=1)

        bill_area_label=Label(bill_frame, text="Customer Bill Area", bg="#9370DB", fg="white", font=("Times New Roman", 20,"bold"), justify=CENTER)
        bill_area_label.place(x=0,y=0,relwidth=1)


        self.sales_img = Image.open('/Users/macbookpro/Desktop/python projects/Inventory-System-with-GUI/assets/sales.png')
        self.sales_img = self.sales_img.resize((340, 370), Image.Resampling.LANCZOS)
        self.sales_img_tk = ImageTk.PhotoImage(self.sales_img)
            
        salesimg_lbl = Label(self.root, image=self.sales_img_tk)
        salesimg_lbl.place(x=700, y=150)

        self.show()

    def show(self):
         del self.bill_list[:]
         self.sales_listbox.delete(0,END)
         for i in os.listdir("bill"):
              if i.split(".")[-1]=="txt":
                   self.sales_listbox.insert(END,i)
                   self.bill_list.append(i.split(".")[0])
        
    def get_data(self, ev=None):  # Made event parameter optional
        try:
            index_ = self.sales_listbox.curselection()
            if not index_:  # If nothing selected
                return
                
            file_name = self.sales_listbox.get(index_)  # Get first selected item
            self.bill_area.delete('1.0', END)
            
            with open(f'bill/{file_name}', 'r') as fp:  # Using context manager
                for line in fp:
                    self.bill_area.insert(END, line)

            fp.close()       
                    
        except Exception as e:
            print(f"Error loading bill: {e}")
    


    def search(self):
      invoice_no = self.var_invoice.get().strip()  # Get and clean the input
    
      if not invoice_no:  # Check for empty string
        messagebox.showerror("Error", "Invoice no is required", parent=self.root)
        return
    
      if invoice_no in self.bill_list:
        try:
            with open(f'bill/{invoice_no}.txt', 'r') as fp:
                self.bill_area.delete('1.0', END)
                self.bill_area.insert(END, fp.read())  # More efficient reading
        except FileNotFoundError:
            messagebox.showerror("Error", "Bill file not found", parent=self.root)
      else:
        messagebox.showerror("Error", "Invalid Invoice No.", parent=self.root)



    def clear(self):
        self.show()
        self.bill_area.delete("1.0", END)



if __name__=="__main__":
        root = Tk()
        obj = Sales(root)
        root.mainloop()