from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from database import MongoDBConnection

class Products:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1045x650+225+160")
        self.root.title("Inventory Management System")
        self.root.focus_force()

        # Database connection
        self.db = MongoDBConnection()
        
        # Variables
        self.var_category = StringVar()
        self.var_supplier = StringVar()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_quantity = StringVar()
        self.var_status = StringVar()
        self.var_search_by = StringVar()
        self.var_search_text = StringVar()

        pro_left_frame=Frame(self.root, bd=2, relief=RIDGE)
        pro_left_frame.place(x=20,y=50)
        
        self.pro_header_label=Label(pro_left_frame, text="Manage Product Details",bg="#9370DB", fg="white", font=("Times New Roman", 25,"bold"), justify=CENTER)
        self.pro_header_label.grid(row=0,columnspan=2)

        cat_lbl=Label(pro_left_frame, text="Category", font=("Times New Roman", 15))
        cat_lbl.grid(row=1, column=0,sticky="w",pady=20,padx=20)
        self.cat_combobox=ttk.Combobox(pro_left_frame, textvariable=self.var_category, font=("Times New Roman", 15), state="readonly")
        self.cat_combobox.grid(row=1,column=1)

        sup_lbl=Label(pro_left_frame, text="Supplier", font=("Times New Roman", 15))
        sup_lbl.grid(row=2, column=0,sticky="w",pady=20,padx=20)
        self.sup_combobox=ttk.Combobox(pro_left_frame, textvariable=self.var_supplier, font=("Times New Roman", 15), state="readonly")
        self.sup_combobox.grid(row=2,column=1)

        name_lbl=Label(pro_left_frame, text="Name", font=("Times New Roman", 15))
        name_lbl.grid(row=3, column=0,sticky="w",pady=20,padx=20)
        name_entry=Entry(pro_left_frame, textvariable=self.var_name, font=("Times New Roman", 15),bg="light yellow")
        name_entry.grid(row=3, column=1,pady=20,padx=20)

        price_lbl=Label(pro_left_frame, text="Price", font=("Times New Roman", 15))
        price_lbl.grid(row=4, column=0,sticky="w",pady=20,padx=20)
        price_entry=Entry(pro_left_frame, textvariable=self.var_price, font=("Times New Roman", 15),bg="light yellow")
        price_entry.grid(row=4, column=1,pady=20,padx=20)


        quantity_lbl=Label(pro_left_frame, text="Quanity", font=("Times New Roman", 15))
        quantity_lbl.grid(row=5, column=0,sticky="w",pady=20,padx=20)
        quantity_entry=Entry(pro_left_frame, textvariable=self.var_quantity, font=("Times New Roman", 15),bg="light yellow")
        quantity_entry.grid(row=5, column=1,pady=20,padx=20)

        status_lbl=Label(pro_left_frame, text="Status", font=("Times New Roman", 15))
        status_lbl.grid(row=6, column=0,sticky="w",pady=20,padx=20)
        self.status_combobox=ttk.Combobox(pro_left_frame, textvariable=self.var_status, font=("Times New Roman", 15), state="readonly",values=("Active","Inactive"))
        self.status_combobox.grid(row=6,column=1)

        btn_frame=Frame(pro_left_frame)
        btn_frame.grid(row=7,columnspan=3)


        add_button=Button(btn_frame,text="Add", command=self.add_product, font=("Times New Roman", 20),bg="blue",fg="black",activeforeground="white",cursor = 'hand2',width=8)
        add_button.grid(row=7, column=0)


        update_button=Button(btn_frame,text="Update", command=self.update_product, font=("Times New Roman", 20),bg="blue",fg="black",activeforeground="white",cursor = 'hand2',width=8)
        update_button.grid(row=7, column=1)


        delete_button=Button(btn_frame,text="Delete", command=self.delete_product, font=("Times New Roman", 20),bg="blue",fg="black",activeforeground="white",cursor = 'hand2',width=8)
        delete_button.grid(row=7, column=2)


     
        clear_button=Button(btn_frame,text="Clear", command=self.clear_fields, font=("Times New Roman",20),bg="blue",fg="black",activeforeground="white",cursor = 'hand2',width=8)
        clear_button.grid(row=7, column=3)


        search_frame=LabelFrame(self.root, text="Search Product",font=("Times New Roman", 20))
        search_frame.place(x=500,y=40)

        self.search_combobox=ttk.Combobox(search_frame, textvariable=self.var_search_by, values=("Category", "Supplier", "Name", "Status"), font=("Times New Roman",14))
        self.search_combobox.grid(row=0, column=0)
        self.search_combobox.set("Select")
        
        search_entry=Entry(search_frame, textvariable=self.var_search_text, font=("Times New Roman", 14),bg="light yellow")
        search_entry.grid(row=0, column=1)


        search_button=Button(search_frame,text="Search", command=self.search_product, font=("Times New Roman", 18),bg="blue",fg="white",activeforeground="white",cursor = 'hand2',width=8)
        search_button.grid(row=0, column=2, padx=(10,0),pady=10)

        show_button=Button(search_frame,text="Show All", command=self.show_all_products, font=("Times New Roman", 18),bg="blue",fg="white",activeforeground="white",cursor = 'hand2',width=8)
        show_button.grid(row=0, column=3, pady=10)
        

        treeview_frame=Frame(self.root)
        treeview_frame.place(x=500,y=125, height=430, width=540)

        horizontal_scrollbar=Scrollbar(treeview_frame, orient="horizontal")
        vertcal_scrollbar=Scrollbar(treeview_frame,orient="vertical")

        self.treeview=ttk.Treeview(treeview_frame, columns=("pid", "category","supplier","name","price","qty","status"), show="headings",yscrollcommand=vertcal_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
 
        horizontal_scrollbar.pack(side=BOTTOM, fill=X)
        vertcal_scrollbar.pack(side=RIGHT,fill=Y,pady=(10,0))
        horizontal_scrollbar.config(command=self.treeview.xview)
        vertcal_scrollbar.config(command=self.treeview.yview)
        self.treeview.pack(fill=BOTH, expand=1) 

        self.treeview.heading("pid", text="Product ID")
        self.treeview.heading("category", text="Category")
        self.treeview.heading("supplier", text="Supplier")
        self.treeview.heading("name", text="Name")
        self.treeview.heading("price", text="Price")
        self.treeview.heading("qty", text="Quantity")
        self.treeview.heading("status", text="Status")
        
        self.treeview.column("pid", width=80)
        self.treeview.column("category", width=120)
        self.treeview.column("supplier", width=120)
        self.treeview.column("name", width=150)
        self.treeview.column("price", width=80)
        self.treeview.column("qty", width=80)
        self.treeview.column("status", width=80)
        
        # Bind treeview selection event
        self.treeview.bind("<ButtonRelease-1>", self.get_selected_row)
        
        # Initialize
        self.var_status.set("Active") # Default status
        self.generate_product_id()
        self.load_categories()
        self.load_suppliers()
        self.show_all_products()
    
    def generate_product_id(self):
        """Generate a unique product ID"""
        try:
            # Get the product count and add 1
            count = self.db.products.count_documents({})
            self.pid = f"P{str(count + 1).zfill(4)}"
        except Exception as e:
            self.pid = "P0001"  # Default if error occurs
            messagebox.showerror("Error", f"Error generating product ID: {str(e)}")
    
    def load_categories(self):
        """Load categories from database to combobox"""
        try:
            cat_list = []
            categories = self.db.categories.find()
            
            for category in categories:
                cat_list.append(category.get("name", ""))
            
            if cat_list:
                # Update the combobox values
                self.cat_combobox['values'] = cat_list
                self.var_category.set(cat_list[0])
            else:
                # Handle the case of no categories
                self.cat_combobox['values'] = ["No categories available"]
                self.var_category.set("No categories available")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading categories: {str(e)}")
    
    def load_suppliers(self):
        """Load suppliers from database to combobox"""
        try:
            sup_list = []
            suppliers = self.db.suppliers.find()
            
            for supplier in suppliers:
                sup_list.append(supplier.get("name", ""))
            
            if sup_list:
                # Update the combobox values
                self.sup_combobox['values'] = sup_list
                self.var_supplier.set(sup_list[0])
            else:
                # Handle the case of no suppliers
                self.sup_combobox['values'] = ["No suppliers available"]
                self.var_supplier.set("No suppliers available")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading suppliers: {str(e)}")
    
    def get_selected_row(self, event):
        """Get data from the selected row and fill the form fields"""
        try:
            selected_item = self.treeview.focus()
            if selected_item:
                values = self.treeview.item(selected_item, 'values')
                if values:
                    self.clear_fields()
                    self.pid = values[0]
                    self.var_category.set(values[1])
                    self.var_supplier.set(values[2])
                    self.var_name.set(values[3])
                    self.var_price.set(values[4])
                    self.var_quantity.set(values[5])
                    self.var_status.set(values[6])
        except Exception as e:
            messagebox.showerror("Error", f"Error selecting data: {str(e)}")
    
    def clear_fields(self):
        """Clear all form fields"""
        self.generate_product_id()
        self.var_name.set("")
        self.var_price.set("")
        self.var_quantity.set("")
        self.var_status.set("Active")
        
        # Use first value in the comboboxes if available
        if self.cat_combobox['values']:
            self.var_category.set(self.cat_combobox['values'][0])
        
        if self.sup_combobox['values']:
            self.var_supplier.set(self.sup_combobox['values'][0])
    
    def get_form_data(self):
        """Get form data and validate"""
        try:
            # Basic validation
            if not self.var_name.get().strip():
                messagebox.showerror("Error", "Product name is required")
                return None
            
            if not self.var_price.get().strip():
                messagebox.showerror("Error", "Price is required")
                return None
            
            if not self.var_quantity.get().strip():
                messagebox.showerror("Error", "Quantity is required")
                return None
            
            # Validate price and quantity are numbers
            try:
                price = float(self.var_price.get().strip())
                if price <= 0:
                    messagebox.showerror("Error", "Price must be greater than 0")
                    return None
            except ValueError:
                messagebox.showerror("Error", "Price must be a number")
                return None
            
            try:
                quantity = int(self.var_quantity.get().strip())
                if quantity < 0:
                    messagebox.showerror("Error", "Quantity cannot be negative")
                    return None
            except ValueError:
                messagebox.showerror("Error", "Quantity must be a whole number")
                return None
            
            return {
                "product_id": self.pid,
                "category": self.var_category.get(),
                "supplier": self.var_supplier.get(),
                "name": self.var_name.get().strip(),
                "price": float(self.var_price.get().strip()),
                "quantity": int(self.var_quantity.get().strip()),
                "status": self.var_status.get()
            }
        except Exception as e:
            messagebox.showerror("Error", f"Error validating data: {str(e)}")
            return None
    
    def add_product(self):
        """Add a new product to the database"""
        try:
            data = self.get_form_data()
            if not data:
                return
            
            # Check if product with this ID already exists
            existing = self.db.products.find_one({"product_id": data["product_id"]})
            if existing:
                # Generate a new ID if this one exists
                self.generate_product_id()
                data["product_id"] = self.pid
            
            # Insert into database
            result = self.db.products.insert_one(data)
            
            if result.inserted_id:
                messagebox.showinfo("Success", "Product added successfully")
                self.clear_fields()
                self.show_all_products()
                # Generate new ID for next product
                self.generate_product_id()
            else:
                messagebox.showerror("Error", "Failed to add product")
                
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")
    
    def update_product(self):
        """Update an existing product in the database"""
        try:
            data = self.get_form_data()
            if not data:
                return
            
            # Update in database
            result = self.db.products.update_one(
                {"product_id": data["product_id"]},
                {"$set": {
                    "category": data["category"],
                    "supplier": data["supplier"],
                    "name": data["name"],
                    "price": data["price"],
                    "quantity": data["quantity"],
                    "status": data["status"]
                }}
            )
            
            if result.modified_count > 0:
                messagebox.showinfo("Success", "Product updated successfully")
                self.show_all_products()
                self.clear_fields()
            elif result.matched_count > 0:
                messagebox.showinfo("Info", "No changes made")
            else:
                messagebox.showerror("Error", f"Product with ID {data['product_id']} not found")
                
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")
    
    def delete_product(self):
        """Delete a product from the database"""
        try:
            if not hasattr(self, 'pid') or not self.pid:
                messagebox.showerror("Error", "Please select a product to delete")
                return
            
            # Confirm deletion
            confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete product {self.pid}?")
            if not confirm:
                return
            
            # Delete from database
            result = self.db.products.delete_one({"product_id": self.pid})
            
            if result.deleted_count > 0:
                messagebox.showinfo("Success", "Product deleted successfully")
                self.clear_fields()
                self.show_all_products()
            else:
                messagebox.showerror("Error", f"Product with ID {self.pid} not found")
                
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")
    
    def search_product(self):
        """Search for products based on criteria"""
        try:
            search_by = self.var_search_by.get()
            search_text = self.var_search_text.get().strip()
            
            if search_by == "Select" or not search_text:
                messagebox.showerror("Error", "Please select search criteria and enter search text")
                return
            
            # Clear treeview
            for item in self.treeview.get_children():
                self.treeview.delete(item)
            
            # Convert search_by to database field name (lowercase)
            field = search_by.lower()
            
            # Find in database - case insensitive search using regex
            query = {field: {"$regex": search_text, "$options": "i"}}
            products = self.db.products.find(query)
            
            # Insert into treeview
            count = 0
            for product in products:
                self.treeview.insert('', END, values=(
                    product.get("product_id", ""),
                    product.get("category", ""),
                    product.get("supplier", ""),
                    product.get("name", ""),
                    product.get("price", ""),
                    product.get("quantity", ""),
                    product.get("status", "")
                ))
                count += 1
            
            if count == 0:
                messagebox.showinfo("Info", f"No products found matching '{search_text}' in {search_by}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Search error: {str(e)}")
    
    def show_all_products(self):
        """Show all products in the treeview"""
        try:
            # Clear treeview
            for item in self.treeview.get_children():
                self.treeview.delete(item)
            
            # Get all products from database
            products = self.db.products.find()
            
            # Insert into treeview
            for product in products:
                self.treeview.insert('', END, values=(
                    product.get("product_id", ""),
                    product.get("category", ""),
                    product.get("supplier", ""),
                    product.get("name", ""),
                    product.get("price", ""),
                    product.get("quantity", ""),
                    product.get("status", "")
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")


if __name__=="__main__":
        root = Tk()
        obj = Products(root)
        root.mainloop()