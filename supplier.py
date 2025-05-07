from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from database import MongoDBConnection

class Supplier:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1045x650+225+160")
        self.root.title("Inventory Management System")
        
        # Initialize database connection
        self.db = MongoDBConnection()
        
        # Variables for form fields
        self.var_invoice = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()
        self.var_search_invoice = StringVar()

        self.supplier_header_lbl=Label(self.root, text="Manage Supplier Details", bg="#9370DB", fg="white", font=("Times New Roman", 30,"bold"), justify=CENTER)
        self.supplier_header_lbl.place(x=0,y=0,relwidth=1)


        self.left_frame=Frame(self.root)
        self.left_frame.place(x=10,y=100)

        self.sup_name=Label(self.left_frame, text="Invoice No.", font=("Times New Roman", 15))
        self.sup_name.grid(row=0, column=0, padx=(20,20),sticky="w")
        self.invoice_entry=Entry(self.left_frame, textvariable=self.var_invoice, font=("Times new roman", 15),bg="light yellow")
        self.invoice_entry.grid(row=0, column=1,pady=15, padx=20)


        self.sup_name=Label(self.left_frame, text="Supplier Name", font=("Times New Roman", 15))
        self.sup_name.grid(row=1, column=0, padx=20, pady=20,sticky="w")
        self.sup_entry=Entry(self.left_frame, textvariable=self.var_name, font=("Times new roman", 15),bg="light yellow")
        self.sup_entry.grid(row=1, column=1,pady=15, padx=20)
                                 

        self.contact=Label(self.left_frame, text="Contact No.", font=("Times New Roman", 15))
        self.contact.grid(row=2, column=0, padx=20, pady=20,sticky="w")
        self.contact_entry=Entry(self.left_frame, textvariable=self.var_contact, font=("Times new roman", 15),bg="light yellow")
        self.contact_entry.grid(row=2, column=1,pady=15, padx=20)


        self.description=Label(self.left_frame, text="Description", font=("Times New Roman", 15))
        self.description.grid(row=3, column=0, padx=20, pady=20,sticky="nw")
        self.description_entry=Text(self.left_frame,font=("Times new roman", 15), height=6, width=20, bd=2, bg="light yellow")
        self.description_entry.grid(row=3, column=1, padx=20)


        self.btn_frame=Frame(self.left_frame)
        self.btn_frame.grid(row=4,columnspan=2, pady=15)

        add_button=Button(self.btn_frame,text="Add", command=self.add_supplier, font=("Times New Roman", 20),bg="red",fg="black",activeforeground="red",cursor = 'hand2',width=8)
        add_button.grid(row=4, column=1,padx=10)


        update_button=Button(self.btn_frame,text="Update", command=self.update_supplier, font=("Times New Roman", 20),bg="blue",fg="black",activeforeground="white",cursor = 'hand2',width=8)
        update_button.grid(row=4, column=2,padx=10)


        delete_button=Button(self.btn_frame,text="Delete", command=self.delete_supplier, font=("Times New Roman", 20),bg="blue",fg="black",activeforeground="white",cursor = 'hand2',width=8)
        delete_button.grid(row=4, column=3,padx=10)


     
        clear_button=Button(self.btn_frame,text="Clear", command=self.clear_fields, font=("Times New Roman",20),bg="blue",fg="black",activeforeground="white",cursor = 'hand2',width=8)
        clear_button.grid(row=4, column=4,padx=10)


        self.right_frame=Frame(self.root)
        self.right_frame.place(x=550, y=110,width=500, height=340)

        self.search_frame=Frame(self.right_frame)
        self.search_frame.pack(pady=20)


        self.search_by_inv=Label(self.search_frame, text="Invoice No.", font=("Times New Roman", 15))
        self.search_by_inv.grid(row=0, column=0, padx=10,sticky="w")
        self.search_invoice_entry=Entry(self.search_frame, textvariable=self.var_search_invoice, font=("Times new roman", 15),bg="light yellow",width=10)
        self.search_invoice_entry.grid(row=0, column=1, padx=10)

        search_button=Button(self.search_frame,text="Search", command=self.search_supplier, font=("Times New Roman", 20),bg="blue",fg="white",activeforeground="white",cursor = 'hand2',width=8)
        search_button.grid(row=0,column=2,padx=5)



        show_all_button=Button(self.search_frame,text="Show All", command=self.show_all_suppliers, font=("Times New Roman", 20),bg="blue",fg="white",activeforeground="white",cursor = 'hand2',width=8)
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
        
        # Bind treeview selection event
        self.treeview.bind("<ButtonRelease-1>", self.get_selected_row)
        
        # Load suppliers from database when initialized
        self.show_all_suppliers()
    
    def get_selected_row(self, event):
        """Get data from the selected row and fill the form fields"""
        try:
            selected_item = self.treeview.focus()
            if selected_item:
                values = self.treeview.item(selected_item, 'values')
                if values:
                    self.clear_fields()
                    self.var_invoice.set(values[0])
                    self.var_name.set(values[1])
                    self.var_contact.set(values[2])
                    
                    # For description (text widget)
                    description = values[3]
                    self.description_entry.delete(1.0, END)
                    self.description_entry.insert(END, description)
        except Exception as e:
            messagebox.showerror("Error", f"Error selecting data: {str(e)}")
    
    def clear_fields(self):
        """Clear all form fields"""
        self.var_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.description_entry.delete(1.0, END)
    
    def get_form_data(self):
        """Get form data and validate"""
        invoice = self.var_invoice.get().strip()
        name = self.var_name.get().strip()
        contact = self.var_contact.get().strip()
        description = self.description_entry.get(1.0, END).strip()
        
        # Basic validation
        if not invoice:
            messagebox.showerror("Error", "Invoice number is required")
            return None
        
        if not name:
            messagebox.showerror("Error", "Supplier name is required")
            return None
        
        return {
            "supplier_id": invoice,  # Using invoice as the supplier_id
            "name": name,
            "contact": contact,
            "description": description
        }
    
    def add_supplier(self):
        """Add a new supplier to the database"""
        try:
            data = self.get_form_data()
            if not data:
                return
            
            # Check if supplier with this invoice already exists
            existing = self.db.suppliers.find_one({"supplier_id": data["supplier_id"]})
            if existing:
                messagebox.showerror("Error", f"Supplier with Invoice {data['supplier_id']} already exists")
                return
            
            # Insert into database
            result = self.db.suppliers.insert_one(data)
            
            if result.inserted_id:
                messagebox.showinfo("Success", "Supplier added successfully")
                self.clear_fields()
                self.show_all_suppliers()
            else:
                messagebox.showerror("Error", "Failed to add supplier")
                
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")
    
    def update_supplier(self):
        """Update an existing supplier in the database"""
        try:
            data = self.get_form_data()
            if not data:
                return
            
            # Update in database
            result = self.db.suppliers.update_one(
                {"supplier_id": data["supplier_id"]},
                {"$set": {
                    "name": data["name"],
                    "contact": data["contact"],
                    "description": data["description"]
                }}
            )
            
            if result.modified_count > 0:
                messagebox.showinfo("Success", "Supplier updated successfully")
                self.show_all_suppliers()
            elif result.matched_count > 0:
                messagebox.showinfo("Info", "No changes made")
            else:
                messagebox.showerror("Error", f"Supplier with Invoice {data['supplier_id']} not found")
                
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")
    
    def delete_supplier(self):
        """Delete a supplier from the database"""
        try:
            invoice = self.var_invoice.get().strip()
            
            if not invoice:
                messagebox.showerror("Error", "Please select a supplier to delete")
                return
            
            # Confirm deletion
            confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete supplier with Invoice {invoice}?")
            if not confirm:
                return
            
            # Delete from database
            result = self.db.suppliers.delete_one({"supplier_id": invoice})
            
            if result.deleted_count > 0:
                messagebox.showinfo("Success", "Supplier deleted successfully")
                self.clear_fields()
                self.show_all_suppliers()
            else:
                messagebox.showerror("Error", f"Supplier with Invoice {invoice} not found")
                
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")
    
    def search_supplier(self):
        """Search for suppliers by invoice number"""
        try:
            invoice = self.var_search_invoice.get().strip()
            
            if not invoice:
                messagebox.showerror("Error", "Please enter an invoice number to search")
                return
            
            # Find in database
            supplier = self.db.suppliers.find_one({"supplier_id": invoice})
            
            # Clear treeview
            for item in self.treeview.get_children():
                self.treeview.delete(item)
            
            if supplier:
                # Insert the found supplier into treeview
                self.treeview.insert('', END, values=(
                    supplier.get("supplier_id", ""),
                    supplier.get("name", ""),
                    supplier.get("contact", ""),
                    supplier.get("description", "")
                ))
            else:
                messagebox.showinfo("Info", f"No supplier found with Invoice {invoice}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Search error: {str(e)}")
    
    def show_all_suppliers(self):
        """Show all suppliers in the treeview"""
        try:
            # Clear treeview
            for item in self.treeview.get_children():
                self.treeview.delete(item)
            
            # Get all suppliers from database
            suppliers = self.db.suppliers.find()
            
            # Insert into treeview
            for supplier in suppliers:
                self.treeview.insert('', END, values=(
                    supplier.get("supplier_id", ""),
                    supplier.get("name", ""),
                    supplier.get("contact", ""),
                    supplier.get("description", "")
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")


if __name__=="__main__":
        root = Tk()
        obj = Supplier(root)
        root.mainloop()