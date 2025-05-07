from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from tkvideo import tkvideo
import os
from database import MongoDBConnection

class Category:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1045x650+225+160")
        self.root.title("Inventory Management System")
        
        # Initialize database connection
        self.db = MongoDBConnection()
        
        # Variables
        self.var_cat_id = StringVar()
        self.var_cat_name = StringVar()
        
        self.emp_header_label=Label(self.root, text="Manage Category Details", bg="#9370DB", fg="white", font=("Times New Roman", 30,"bold"), justify=CENTER)
        self.emp_header_label.place(x=0,y=0,relwidth=1)


        cat_details_frame=Frame(self.root)
        cat_details_frame.place(x=0, y=100)

        cat_name_lbl=Label(cat_details_frame, text="Category ID", font=("Times new roman", 15))
        cat_name_lbl.grid(row=0,column=0,padx=20,pady=15,sticky="w")
        cat_entry=Entry(cat_details_frame, textvariable=self.var_cat_id, font=("Times new roman", 15),bg="light yellow")
        cat_entry.grid(row=0, column=1, padx=20,pady=15)

        cat_name_lbl=Label(cat_details_frame, text="Category Name", font=("Times new roman", 15))
        cat_name_lbl.grid(row=1,column=0,padx=20,pady=15,sticky="w")
        cat_name_entry=Entry(cat_details_frame, textvariable=self.var_cat_name, font=("Times new roman", 15),bg="light yellow")
        cat_name_entry.grid(row=1, column=1, padx=20,pady=20)

        cat_desc_lnl=Label(cat_details_frame, text="Category Description", font=("Times new roman", 15))
        cat_desc_lnl.grid(row=2,column=0,padx=20,pady=15,sticky="nw")
        self.cat_desc_txt=Text(cat_details_frame, width=20, height=6,font=("Times new roman", 15),bg="light yellow")
        self.cat_desc_txt.grid(row=2,column=1, padx=20,pady=15)

        btn_frame=Frame(self.root)
        btn_frame.place(x=30, y=350)

        add_button=Button(btn_frame,text="Add", command=self.add_category, font=("Times New Roman", 20),bg="blue",fg="black",activeforeground="white",cursor = 'hand2',width=8)
        add_button.grid(row=0, column=0,padx=10,pady=10)

        update_button=Button(btn_frame,text="Update", command=self.update_category, font=("Times New Roman", 20),bg="blue",fg="black",activeforeground="white",cursor = 'hand2',width=8)
        update_button.grid(row=0, column=1,padx=10,pady=10)

        delete_button=Button(btn_frame,text="Delete", command=self.delete_category, font=("Times New Roman", 20),bg="blue",fg="black",activeforeground="white",cursor = 'hand2',width=8)
        delete_button.grid(row=0, column=2,padx=10,pady=10)
        
        clear_button=Button(btn_frame,text="Clear", command=self.clear_fields, font=("Times New Roman", 20),bg="blue",fg="black",activeforeground="white",cursor = 'hand2',width=8)
        clear_button.grid(row=0, column=3,padx=10,pady=10)


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
        
        # Bind treeview selection
        self.treeview.bind("<ButtonRelease-1>", self.get_selected_row)

        video_label = Label(self.root)
        video_label.place(x=600,y=100)
        video_file = "/Users/macbookpro/Desktop/python projects/Inventory-System-with-GUI/assets/Inventory.mp4"

        if os.path.exists(video_file):
            # Simple video player with tkvideo
            player = tkvideo(video_file, video_label, loop=1, size=(400, 500))
            player.play()
        else:
            Label(self.root, text="Video file not found!").pack()
            
        # Generate default category ID
        self.generate_category_id()
        
        # Load existing categories
        self.show_all_categories()

    def generate_category_id(self):
        """Generate a unique category ID"""
        try:
            # Get the category count and add 1
            count = self.db.categories.count_documents({})
            self.var_cat_id.set(f"C{str(count + 1).zfill(3)}")
        except Exception as e:
            self.var_cat_id.set("C001")  # Default if error occurs
            messagebox.showerror("Error", f"Error generating category ID: {str(e)}")
    
    def get_selected_row(self, event):
        """Get data from the selected row and fill the form fields"""
        try:
            selected_item = self.treeview.focus()
            if selected_item:
                values = self.treeview.item(selected_item, 'values')
                if values:
                    self.clear_fields()
                    self.var_cat_id.set(values[0])
                    self.var_cat_name.set(values[1])
                    
                    # For description (text widget)
                    description = values[2]
                    self.cat_desc_txt.delete(1.0, END)
                    self.cat_desc_txt.insert(END, description)
        except Exception as e:
            messagebox.showerror("Error", f"Error selecting data: {str(e)}")
    
    def clear_fields(self):
        """Clear all form fields"""
        self.generate_category_id()
        self.var_cat_name.set("")
        self.cat_desc_txt.delete(1.0, END)
    
    def get_form_data(self):
        """Get form data and validate"""
        try:
            category_id = self.var_cat_id.get().strip()
            category_name = self.var_cat_name.get().strip()
            description = self.cat_desc_txt.get(1.0, END).strip()
            
            # Basic validation
            if not category_id:
                messagebox.showerror("Error", "Category ID is required")
                return None
            
            if not category_name:
                messagebox.showerror("Error", "Category name is required")
                return None
            
            return {
                "category_id": category_id,
                "name": category_name,
                "description": description
            }
        except Exception as e:
            messagebox.showerror("Error", f"Error validating data: {str(e)}")
            return None
    
    def add_category(self):
        """Add a new category to the database"""
        try:
            data = self.get_form_data()
            if not data:
                return
            
            # Check if category with this ID already exists
            existing = self.db.categories.find_one({"category_id": data["category_id"]})
            if existing:
                messagebox.showerror("Error", f"Category with ID {data['category_id']} already exists")
                return
            
            # Check if category with this name already exists
            existing_name = self.db.categories.find_one({"name": data["name"]})
            if existing_name:
                messagebox.showerror("Error", f"Category with name '{data['name']}' already exists")
                return
            
            # Insert into database
            result = self.db.categories.insert_one(data)
            
            if result.inserted_id:
                messagebox.showinfo("Success", "Category added successfully")
                self.clear_fields()
                self.show_all_categories()
            else:
                messagebox.showerror("Error", "Failed to add category")
                
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")
    
    def update_category(self):
        """Update an existing category in the database"""
        try:
            data = self.get_form_data()
            if not data:
                return
            
            # Check if category with this name already exists (but not this ID)
            existing_name = self.db.categories.find_one({
                "name": data["name"],
                "category_id": {"$ne": data["category_id"]}
            })
            
            if existing_name:
                messagebox.showerror("Error", f"Category with name '{data['name']}' already exists")
                return
            
            # Update in database
            result = self.db.categories.update_one(
                {"category_id": data["category_id"]},
                {"$set": {
                    "name": data["name"],
                    "description": data["description"]
                }}
            )
            
            if result.modified_count > 0:
                messagebox.showinfo("Success", "Category updated successfully")
                self.show_all_categories()
                self.clear_fields()
            elif result.matched_count > 0:
                messagebox.showinfo("Info", "No changes made")
            else:
                messagebox.showerror("Error", f"Category with ID {data['category_id']} not found")
                
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")
    
    def delete_category(self):
        """Delete a category from the database"""
        try:
            category_id = self.var_cat_id.get().strip()
            
            if not category_id:
                messagebox.showerror("Error", "Please select a category to delete")
                return
            
            # Check if category is used in any products
            products_using_category = self.db.products.count_documents({"category": self.var_cat_name.get().strip()})
            
            if products_using_category > 0:
                messagebox.showerror("Error", f"Cannot delete this category as it is used by {products_using_category} product(s)")
                return
            
            # Confirm deletion
            confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete category {category_id}?")
            if not confirm:
                return
            
            # Delete from database
            result = self.db.categories.delete_one({"category_id": category_id})
            
            if result.deleted_count > 0:
                messagebox.showinfo("Success", "Category deleted successfully")
                self.clear_fields()
                self.show_all_categories()
            else:
                messagebox.showerror("Error", f"Category with ID {category_id} not found")
                
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")
    
    def show_all_categories(self):
        """Show all categories in the treeview"""
        try:
            # Clear treeview
            for item in self.treeview.get_children():
                self.treeview.delete(item)
            
            # Get all categories from database
            categories = self.db.categories.find()
            
            # Insert into treeview
            for category in categories:
                self.treeview.insert('', END, values=(
                    category.get("category_id", ""),
                    category.get("name", ""),
                    category.get("description", "")
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")


if __name__=="__main__":
        root = Tk()
        obj = Category(root)
        root.mainloop()