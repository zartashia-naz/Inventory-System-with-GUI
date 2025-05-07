from tkinter import *
from PIL import Image, ImageTk
from database import MongoDBConnection
import time
import datetime
from tkinter import ttk, messagebox
import os
import random

class BillingClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System | Billing Area")
        
        # Variables
        self.cart_list = []
        self.search_var = StringVar()
        self.product_name = StringVar()
        self.product_price = StringVar()
        self.product_qty = StringVar()
        self.cust_name = StringVar()
        self.cust_contact = StringVar()
        self.bill_amount = StringVar()
        self.discount = StringVar()
        self.net_pay = StringVar()
        self.bill_no = ""  # Store current bill number
        
        # Initialize variables
        self.bill_amount.set('0')
        self.net_pay.set('0')
        self.discount.set('5')  # Default discount
        
        # Initialize database connection
        self.db = MongoDBConnection()

        # Colors
        self.bg_color = "purple"  
        self.fg_color = "white"
        self.header_bg = "#000080"
        self.header_fg = "white"
        self.btn_color = "#FFC107"  # Yellow
        
        # ===== TITLE BAR =====
        title_frame = Frame(self.root, bg=self.bg_color)
        title_frame.place(x=0, y=0, relwidth=1, height=70)
        
        # Logo
        self.logo_img = Image.open("/Users/macbookpro/Desktop/python projects/Inventory-System-with-GUI/img logo2.png")
        self.logo_img = self.logo_img.resize((50, 50), Image.Resampling.LANCZOS)
        self.logo_img_tk = ImageTk.PhotoImage(self.logo_img)
    



       
        logo_label = Label(title_frame, image=self.logo_img_tk, bg=self.bg_color)
        logo_label.place(x=10, y=5)
        
        # Title
        title = Label(title_frame, text="Inventory Management System", 
                      font=("times new roman", 30, "bold"), 
                      bg=self.bg_color, fg=self.fg_color)
        title.place(x=80, y=15)
        
        # Logout button
        logout_btn = Button(title_frame, text="Logout", 
                           font=("times new roman", 15, "bold"), command=self.logout,
                           bg=self.btn_color, cursor="hand2")
        logout_btn.place(x=1200, y=20, width=150, height=30)
        
        # ===== Second Header =====
        header_frame = Frame(self.root, bg="#E0E0E0")
        header_frame.place(x=0, y=70, relwidth=1, height=30)
        
        # Welcome text
        welcome_text = Label(header_frame, text="Welcome to Inventory Management System", 
                            font=("times new roman", 15), 
                            bg="#E0E0E0")
        welcome_text.pack(side=LEFT, padx=20)
        
        # Date and time
        self.clock_label = Label(header_frame, 
                               font=("times new roman", 15), 
                               bg="#E0E0E0")
        self.clock_label.pack(side=RIGHT, padx=20)
        self.update_date_time()
        
        # ===== Main Content Frames =====
        # 1. Product List Frame (LEFT)
        prod_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        prod_frame.place(x=10, y=110, width=410, height=550)
        
        prod_title = Label(prod_frame, text="All Products", 
                          font=("times new roman", 20, "bold"), 
                          bg="#262626", fg="white")
        prod_title.pack(side=TOP, fill=X)
        
        # Product Search Frame
        prod_search_frame = Frame(prod_frame, bd=2, relief=RIDGE, bg="white")
        prod_search_frame.place(x=2, y=42, width=398, height=90)
        
        search_label = Label(prod_search_frame, text="Search Product | By Name", 
                            font=("times new roman", 15, "bold"), 
                            bg="white", fg="green")
        search_label.place(x=2, y=5)
        
        # Show all button
        show_all_btn = Button(prod_search_frame, text="Show All", 
                             font=("times new roman", 13), 
                             bg="#083531", fg="black", cursor="hand2",
                             command=self.show_all_products)
        show_all_btn.place(x=300, y=5, width=90, height=30)
        
        # Product name search
        prod_name_label = Label(prod_search_frame, text="Product Name", 
                               font=("times new roman", 15), 
                               bg="white")
        prod_name_label.place(x=5, y=45)
        
        self.search_txt = Entry(prod_search_frame, 
                               textvariable=self.search_var, 
                               font=("times new roman", 15), 
                               bg="lightyellow")
        self.search_txt.place(x=130, y=47, width=150, height=22)
        
        # Search button
        search_btn = Button(prod_search_frame, text="Search", 
                           font=("times new roman", 15), 
                           bg="#2196f3", fg="black", cursor="hand2",
                           command=self.search_products)
        search_btn.place(x=290, y=45, width=100, height=25)
        
        # ===== Product Frame Enhancements =====
        # Add a section above the Products Table to display current stock status
        stock_status_frame = Frame(prod_frame, bg="white", bd=1, relief=RIDGE)
        stock_status_frame.place(x=2, y=140, width=398, height=30)

        # Dynamic stock status label
        self.stock_status_label = Label(stock_status_frame, text="Current Stock Status: No Product Selected", 
                                     font=("times new roman", 12), bg="white", fg="#333")
        self.stock_status_label.pack(side=LEFT, padx=10, fill=X, expand=True)

        # Move product list down a bit to accommodate the new label
        prod_list_frame = Frame(prod_frame, bd=3, relief=RIDGE)
        prod_list_frame.place(x=2, y=170, width=398, height=345)  # Adjusted height and y position
        
        scrolly = Scrollbar(prod_list_frame, orient=VERTICAL)
        scrollx = Scrollbar(prod_list_frame, orient=HORIZONTAL)
        
        # Products Table - Using Treeview instead of Listbox
        self.product_table = ttk.Treeview(prod_list_frame, 
                                       columns=("pid", "name", "price", "qty", "status"),
                                       yscrollcommand=scrolly.set, 
                                       xscrollcommand=scrollx.set)
        
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)
        self.product_table.pack(fill=BOTH, expand=1)
        
        # Format treeview
        self.product_table["show"] = "headings"  # Remove first empty column
        
        # Set column headings
        self.product_table.heading("pid", text="P ID")
        self.product_table.heading("name", text="Name")
        self.product_table.heading("price", text="Price")    
        self.product_table.heading("qty", text="QTY")
        self.product_table.heading("status", text="Status")
        
        # Set column widths
        self.product_table.column("pid", width=40)
        self.product_table.column("name", width=100)
        self.product_table.column("price", width=80)
        self.product_table.column("qty", width=50)
        self.product_table.column("status", width=80)
        
        self.product_table.bind("<ButtonRelease-1>", self.get_data)
        
        # Note at the bottom
        note_label = Label(prod_frame, text="Note: Enter 0 QTY to Remove the Product from Cart", 
                          font=("goudy old style", 12), 
                          bg="white", fg="red")
        note_label.pack(side=BOTTOM, fill=X)
        
        # 2. Customer Details Frame (MIDDLE)
        cust_frame = Frame(self.root, bd=2, relief=RIDGE, bg="#E0E0E0")
        cust_frame.place(x=430, y=110, width=530, height=550)
        
        # Customer details title
        cust_title = Label(cust_frame, text="Customer Details", 
                          font=("times new roman", 20, "bold"), 
                          bg="#f0f0f0")
        cust_title.pack(side=TOP, fill=X)
        
        # Customer details entry area
        cust_details_frame = Frame(cust_frame, bd=1, relief=RIDGE, bg="#f0f0f0")
        cust_details_frame.place(x=0, y=30, relwidth=1, height=80)
        
        # Name
        name_lbl = Label(cust_details_frame, text="Name", 
                        font=("times new roman", 15), 
                        bg="#f0f0f0")
        name_lbl.place(x=5, y=10)
        
        name_entry = Entry(cust_details_frame, 
                          textvariable=self.cust_name, 
                          font=("times new roman", 15), 
                          bg="white")
        name_entry.place(x=80, y=10, width=180)
        
        # Contact
        contact_lbl = Label(cust_details_frame, text="Contact No.", 
                           font=("times new roman", 15), 
                           bg="#f0f0f0")
        contact_lbl.place(x=270, y=10)
        
        contact_entry = Entry(cust_details_frame, 
                             textvariable=self.cust_contact, 
                             font=("times new roman", 15), 
                             bg="white")
        contact_entry.place(x=380, y=10, width=140)
        
        # Cart Area
        cart_frame = Frame(cust_frame, bd=2, relief=RIDGE)
        cart_frame.place(x=0, y=110, relwidth=1, height=320)
        
        # Cart header with add/update button
        cart_header_frame = Frame(cart_frame, bg="#1E88E5")
        cart_header_frame.pack(side=TOP, fill=X)
        
        self.cart_title = Label(cart_header_frame, text="Cart   Total Products: [0]", 
                               font=("times new roman", 15, "bold"), 
                               bg="#1E88E5", fg="white")
        self.cart_title.pack(side=LEFT, padx=10)
        
        # Add the ADD/UPDATE CART button to cart header
        add_update_btn = Button(cart_header_frame, text="ADD/UPDATE CART", command=self.add_update_cart,
                               font=("times new roman", 12, "bold"),
                               bg="#FFD700", fg="black", cursor="hand2")
        add_update_btn.pack(side=RIGHT, padx=10, pady=3)
        
        # Cart Table
        cart_table_frame = Frame(cart_frame)
        cart_table_frame.place(x=0, y=40, relwidth=1, height=275)  # Adjusted y position from 30 to 40 to account for header
        
        scrolly_cart = Scrollbar(cart_table_frame, orient=VERTICAL)
        scrollx_cart = Scrollbar(cart_table_frame, orient=HORIZONTAL)
        
        # Cart Table - Using Treeview
        self.cart_table = ttk.Treeview(cart_table_frame, 
                                    columns=("pid", "name", "price", "qty"),
                                    yscrollcommand=scrolly_cart.set, 
                                    xscrollcommand=scrollx_cart.set)
        
        scrollx_cart.pack(side=BOTTOM, fill=X)
        scrolly_cart.pack(side=RIGHT, fill=Y)
        scrollx_cart.config(command=self.cart_table.xview)
        scrolly_cart.config(command=self.cart_table.yview)
        self.cart_table.pack(fill=BOTH, expand=1)
        
        # Format cart treeview
        self.cart_table["show"] = "headings"  # Remove first empty column
        
        # Set column headings
        self.cart_table.heading("pid", text="PID")
        self.cart_table.heading("name", text="Product")
        self.cart_table.heading("price", text="Price")    
        self.cart_table.heading("qty", text="QTY")
        
        # Set column widths
        self.cart_table.column("pid", width=40)
        self.cart_table.column("name", width=200)
        self.cart_table.column("price", width=70)
        self.cart_table.column("qty", width=40)
        
        # Bind cart table selection event
        self.cart_table.bind("<ButtonRelease-1>", self.get_cart_data)
        
        # Calculator (Number Pad) and product entry area
        calc_frame = Frame(cust_frame, bd=1, relief=RIDGE, bg="#f0f0f0")
        calc_frame.place(x=0, y=440, relwidth=1, height=105)
        
        # Product entry part - more compact
        product_frame = Frame(calc_frame, bg="#f0f0f0", bd=1)
        product_frame.place(x=5, y=5, width=520, height=95)
        
        # Product Details for selection
        # Product Name
        pname_lbl = Label(product_frame, text="Product Name", font=("times new roman", 13), bg="#f0f0f0")
        pname_lbl.grid(row=0, column=0, padx=5, pady=3, sticky=W)
        
        pname_txt = Entry(product_frame, textvariable=self.product_name, 
                        font=("times new roman", 13), bg="lightyellow", state='readonly')
        pname_txt.grid(row=0, column=1, padx=5, pady=3, sticky=W)
        
        # Price 
        price_lbl = Label(product_frame, text="Price Per Qty", font=("times new roman", 13), bg="#f0f0f0")
        price_lbl.grid(row=1, column=0, padx=5, pady=3, sticky=W)
        
        price_txt = Entry(product_frame, textvariable=self.product_price, 
                        font=("times new roman", 13), bg="lightyellow", state='readonly')
        price_txt.grid(row=1, column=1, padx=5, pady=3, sticky=W)
        
        # Quantity
        qty_lbl = Label(product_frame, text="Quantity", font=("times new roman", 13), bg="#f0f0f0")
        qty_lbl.grid(row=2, column=0, padx=5, pady=3, sticky=W)
        
        qty_txt = Entry(product_frame, textvariable=self.product_qty, 
                      font=("times new roman", 13), bg="lightyellow")
        qty_txt.grid(row=2, column=1, padx=5, pady=3, sticky=W)
        
        # Stock status
        self.stock_lbl = Label(product_frame, text="In Stock", 
                             font=("times new roman", 13), bg="#f0f0f0")
        self.stock_lbl.grid(row=3, column=0, padx=5, pady=3, sticky=W)
        
        # Control buttons
        clear_btn = Button(product_frame, text="Clear", command=self.clear_cart, 
                         font=("times new roman", 13, "bold"), 
                         bg="lightgray", cursor="hand2")
        clear_btn.grid(row=3, column=1, padx=5, pady=3, sticky=W)
        
        # Calculator buttons (numpad)
        numpad_frame = Frame(calc_frame, bg="#f0f0f0")
        numpad_frame.place(x=320, y=5, width=215, height=95)
        
        # Create a grid of calculator buttons
        # Row 1
        btn_7 = Button(numpad_frame, text="7", font=("times new roman", 15, "bold"), 
                     bg="#f0f0f0", bd=1, cursor="hand2", command=lambda:self.get_input(7))
        btn_7.place(x=0, y=0, width=53, height=26)
        
        btn_8 = Button(numpad_frame, text="8", font=("times new roman", 15, "bold"), 
                     bg="#f0f0f0", bd=1, cursor="hand2", command=lambda:self.get_input(8))
        btn_8.place(x=53, y=0, width=53, height=26)
        
        btn_9 = Button(numpad_frame, text="9", font=("times new roman", 15, "bold"), 
                     bg="#f0f0f0", bd=1, cursor="hand2", command=lambda:self.get_input(9))
        btn_9.place(x=106, y=0, width=53, height=26)
        
        btn_plus = Button(numpad_frame, text="+", font=("times new roman", 15, "bold"), 
                        bg="#f0f0f0", bd=1, cursor="hand2", command=lambda:self.get_input('+'))
        btn_plus.place(x=159, y=0, width=53, height=26)
        
        # Row 2
        btn_4 = Button(numpad_frame, text="4", font=("times new roman", 15, "bold"), 
                     bg="#f0f0f0", bd=1, cursor="hand2", command=lambda:self.get_input(4))
        btn_4.place(x=0, y=26, width=53, height=26)
        
        btn_5 = Button(numpad_frame, text="5", font=("times new roman", 15, "bold"), 
                     bg="#f0f0f0", bd=1, cursor="hand2", command=lambda:self.get_input(5))
        btn_5.place(x=53, y=26, width=53, height=26)
        
        btn_6 = Button(numpad_frame, text="6", font=("times new roman", 15, "bold"), 
                     bg="#f0f0f0", bd=1, cursor="hand2", command=lambda:self.get_input(6))
        btn_6.place(x=106, y=26, width=53, height=26)
        
        btn_minus = Button(numpad_frame, text="-", font=("times new roman", 15, "bold"), 
                         bg="#f0f0f0", bd=1, cursor="hand2", command=lambda:self.get_input('-'))
        btn_minus.place(x=159, y=26, width=53, height=26)
        
        # Row 3
        btn_1 = Button(numpad_frame, text="1", font=("times new roman", 15, "bold"), 
                     bg="#f0f0f0", bd=1, cursor="hand2", command=lambda:self.get_input(1))
        btn_1.place(x=0, y=52, width=53, height=26)
        
        btn_2 = Button(numpad_frame, text="2", font=("times new roman", 15, "bold"), 
                     bg="#f0f0f0", bd=1, cursor="hand2", command=lambda:self.get_input(2))
        btn_2.place(x=53, y=52, width=53, height=26)
        
        btn_3 = Button(numpad_frame, text="3", font=("times new roman", 15, "bold"), 
                     bg="#f0f0f0", bd=1, cursor="hand2", command=lambda:self.get_input(3))
        btn_3.place(x=106, y=52, width=53, height=26)
        
        btn_multiply = Button(numpad_frame, text="*", font=("times new roman", 15, "bold"), 
                            bg="#f0f0f0", bd=1, cursor="hand2", command=lambda:self.get_input('*'))
        btn_multiply.place(x=159, y=52, width=53, height=26)
        
        # Row 4
        btn_0 = Button(numpad_frame, text="0", font=("times new roman", 15, "bold"), 
                     bg="#f0f0f0", bd=1, cursor="hand2", command=lambda:self.get_input(0))
        btn_0.place(x=0, y=78, width=53, height=26)
        
        btn_clear = Button(numpad_frame, text="C", font=("times new roman", 15, "bold"), 
                         bg="#f0f0f0", bd=1, cursor="hand2", command=self.clear_cal)
        btn_clear.place(x=53, y=78, width=53, height=26)
        
        btn_equal = Button(numpad_frame, text="=", font=("times new roman", 15, "bold"), 
                         bg="#f0f0f0", bd=1, cursor="hand2", command=self.perform_cal)
        btn_equal.place(x=106, y=78, width=53, height=26)
        
        btn_divide = Button(numpad_frame, text="/", font=("times new roman", 15, "bold"), 
                          bg="#f0f0f0", bd=1, cursor="hand2", command=lambda:self.get_input('/'))
        btn_divide.place(x=159, y=78, width=53, height=26)
        
        # 3. Billing Area (RIGHT)
        bill_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        bill_frame.place(x=970, y=110, width=360, height=550)
        
        bill_title = Label(bill_frame, text="Customer Billing Area", 
                         font=("times new roman", 20, "bold"), 
                         bg="#f43636", fg="white")
        bill_title.pack(side=TOP, fill=X)
        
        # Bill area with scrollable text
        bill_area_frame = Frame(bill_frame, bd=2, relief=RIDGE, bg="white")
        bill_area_frame.place(x=0, y=35, relwidth=1, height=365)
        
        scrolly = Scrollbar(bill_area_frame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)
        
        self.bill_area = Text(bill_area_frame, yscrollcommand=scrolly.set, bg="white", fg="black", font=("times new roman", 12))
        self.bill_area.pack(fill=BOTH, expand=1)
        scrolly.config(command=self.bill_area.yview)
        
        # Add initial text to bill area - show empty bill template
        self.clear_bill_area()
        
        # Buttons area - moved up to immediately follow the bill area
        btn_frame = Frame(bill_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame.place(x=0, y=400, relwidth=1, height=50)
        
        # Print button
        print_btn = Button(btn_frame, text="Print",
                         font=("goudy old style", 15, "bold"), 
                         bg="lightgreen", fg="black", cursor="hand2",
                         command=self.print_bill)
        print_btn.place(x=0, y=0, width=120, height=50)
        
        # Clear All button
        clear_all_btn = Button(btn_frame, text="Clear All", command=self.clear_all, 
                             font=("goudy old style", 15, "bold"), 
                             bg="gray", fg="black", cursor="hand2")
        clear_all_btn.place(x=120, y=0, width=120, height=50)
        
        # Generate Bill button
        gen_bill_btn = Button(btn_frame, text="Generate Bill", command=self.generate_bill,
                            font=("goudy old style", 15, "bold"), 
                            bg="blue", fg="black", cursor="hand2")
        gen_bill_btn.place(x=240, y=0, width=120, height=50)
        
        # Bill amount - moved down to follow the buttons
        bill_amount_frame = Frame(bill_frame, bd=2, relief=RIDGE, bg="#0676ad")
        bill_amount_frame.place(x=0, y=450, relwidth=1, height=100)
        
        self.lbl_bill_amount = Label(bill_amount_frame, text="Bill Amount", 
                          font=("goudy old style", 15, "bold"), 
                          bg="#0676ad", fg="white")
        self.lbl_bill_amount.place(x=2, y=10, width=120, height=30)
        
        self.lbl_bill_amount_value = Label(bill_amount_frame, textvariable=self.bill_amount,
                           font=("goudy old style", 25, "bold"), 
                           bg="#0676ad", fg="white")
        self.lbl_bill_amount_value.place(x=2, y=40, width=120, height=50)
        
        self.lbl_discount = Label(bill_amount_frame, text="Discount", 
                    font=("goudy old style", 15, "bold"), 
                    bg="#0676ad", fg="white")
        self.lbl_discount.place(x=124, y=10, width=120, height=30)
        
        self.lbl_discount_value = Label(bill_amount_frame, textvariable=self.discount,
                         font=("goudy old style", 25, "bold"), 
                         bg="#0676ad", fg="white")
        self.lbl_discount_value.place(x=124, y=40, width=120, height=50)
        
        self.lbl_net_pay = Label(bill_amount_frame, text="Net Pay", 
                   font=("goudy old style", 15, "bold"), 
                   bg="#0676ad", fg="white")
        self.lbl_net_pay.place(x=246, y=10, width=110, height=30)
        
        self.lbl_net_pay_value = Label(bill_amount_frame, textvariable=self.net_pay,
                        font=("goudy old style", 25, "bold"), 
                        bg="#0676ad", fg="white")
        self.lbl_net_pay_value.place(x=246, y=40, width=110, height=50)
        
        # Load initial products
        self.show_all_products()
        
        # Add stock management variable
        self.product_stock = {}  # Dictionary to track product stock {name: available_qty}
        
    # ===== Helper Functions =====
    def update_date_time(self):
        time_now = time.strftime("%I:%M:%S")
        date_now = time.strftime("%d-%m-%Y")
        self.clock_label.config(text=f"Date: {date_now} Time: {time_now}")
        self.clock_label.after(1000, self.update_date_time)
        
    def show_all_products(self):
        """Show all products with current quantities"""
        # Clear previous data
        for item in self.product_table.get_children():
            self.product_table.delete(item)
        
        try:
            # Reset the stock status label
            self.stock_status_label.config(text="Current Stock Status: No Product Selected")
            
            # Query products from the database
            products = self.db.products.find({})
            
            # Debug: Print some products to verify
            print("Loading all products...")
            
            for row in products:
                # Debug: Print each product to verify data
                print(f"Loading: {row.get('name')}, Qty: {row.get('quantity')}")
                
                # Insert directly from database
                self.product_table.insert("", END, values=(
                    row.get('_id', ''),
                    row.get('name', ''),
                    row.get('price', ''),
                    row.get('quantity', ''),
                    row.get('status', '')
                ))
        except Exception as e:
            print(f"Error loading products: {e}")
            
    def search_products(self):
        if self.search_var.get() == "":
            self.show_all_products()
        else:
            # Clear previous data
            for item in self.product_table.get_children():
                self.product_table.delete(item)
            
            query = {"name": {"$regex": self.search_var.get(), "$options": "i"}}
            try:
                products = self.db.products.find(query)
                for row in products:
                    # Insert into treeview
                    self.product_table.insert("", END, values=(
                        row.get('_id', ''),
                        row.get('name', ''),
                        row.get('price', ''),
                        row.get('quantity', ''),
                        row.get('status', '')
                    ))
            except Exception as e:
                print(f"Error searching products: {e}")
                
    def get_data(self, ev):
        """Get data from selected product in product table"""
        try:
            selected_row = self.product_table.focus()
            if selected_row:
                contents = self.product_table.item(selected_row)
                row = contents['values']
                if row and len(row) >= 4:
                    # Set values to variables (pid, name, price, qty, status)
                    product_name = str(row[1])
                    self.product_name.set(product_name)
                    
                    # Set price - handle potential non-numeric values
                    try:
                        price = float(row[2])
                        self.product_price.set(str(price))
                    except (ValueError, TypeError):
                        self.product_price.set("0.0")
                        
                    self.product_qty.set("1")  # Default quantity
                    
                    # Store stock information - handle potential non-numeric values
                    try:
                        stock_qty = int(row[3])
                    except (ValueError, TypeError):
                        stock_qty = 0
                        
                    self.product_stock[product_name] = stock_qty
                    
                    # Update the stock label based on cart contents
                    self.update_stock_label(product_name)
                    
                    # Update stock status label
                    if stock_qty > 0:
                        status_text = f"Current Stock: {product_name} - {stock_qty} units available"
                        status_color = "green"
                    else:
                        status_text = f"Out of Stock: {product_name}"
                        status_color = "red"
                        
                    self.stock_status_label.config(text=status_text, fg=status_color)
        except Exception as e:
            print(f"Error in get_data: {e}")

    def get_cart_data(self, ev):
        """Get data from the selected cart item for editing"""
        try:
            selected_row = self.cart_table.focus()
            if selected_row:
                contents = self.cart_table.item(selected_row)
                row = contents['values']
                if row and len(row) >= 4:
                    # pid, product, price, qty
                    # Set values to variables for editing
                    self.product_name.set(str(row[1]))
                    
                    # Set price - handle potential non-numeric values
                    try:
                        price = float(row[2])
                        self.product_price.set(str(price))
                    except (ValueError, TypeError):
                        self.product_price.set("0.0")
                    
                    # Set quantity - handle potential non-numeric values
                    try:
                        qty = int(row[3])
                        self.product_qty.set(str(qty))
                    except (ValueError, TypeError):
                        self.product_qty.set("1")
                    
                    # Update stock label
                    self.update_stock_label(str(row[1]))
        except Exception as e:
            print(f"Error in get_cart_data: {e}")

    def add_update_cart(self):
        """Add or update items in the cart"""
        if self.product_name.get() == "":
            messagebox.showerror("Error", "Please select a product first", parent=self.root)
            return
        
        if self.product_qty.get() == "":
            messagebox.showerror("Error", "Please enter quantity", parent=self.root)
            return
        
        try:
            # Try to convert quantity to integer, handle invalid input
            try:
                qty = int(self.product_qty.get())
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid numeric quantity", parent=self.root)
                return
            
            if qty < 0:
                messagebox.showerror("Error", "Please enter a valid quantity", parent=self.root)
                return
            
            # Check if we have enough stock
            product_name = self.product_name.get()
            
            # Get the latest product information from the database
            product = self.db.products.find_one({"name": product_name})
            
            if product:
                # Update our local stock tracking with the latest from DB
                try:
                    db_qty = int(product.get('quantity', 0))
                    self.product_stock[product_name] = db_qty
                    print(f"Database shows {product_name} has {db_qty} units")
                except (ValueError, TypeError):
                    self.product_stock[product_name] = 0
            
            # Get current stock
            available_stock = self.product_stock.get(product_name, 0)
            
            # Calculate current cart quantity
            curr_cart_qty = 0
            for item in self.cart_list:
                if item.get('name', '') == product_name:
                    try:
                        curr_cart_qty = int(item.get('qty', 0))
                    except (ValueError, TypeError):
                        curr_cart_qty = 0
                    break
            
            print(f"Current stock: {available_stock}, In cart: {curr_cart_qty}, Requested: {qty}")
            
            # Handle case when quantity is 0 - remove item from cart
            if qty == 0:
                # Find and remove the item from cart
                for index, item in enumerate(self.cart_list):
                    if item.get('name', '') == product_name:
                        self.cart_list.pop(index)
                        print(f"Removed {product_name} from cart")
                        break
                
                self.update_cart_display()
                self.calculate_totals()
                self.update_stock_label(product_name)
                self.clear_cart()
                
                # After updating cart, refresh product list to show updated quantities
                self.refresh_product_list()
                return
            
            # Calculate if requested quantity is available
            if qty > (available_stock + curr_cart_qty):
                messagebox.showerror("Error", f"Not enough stock available. Maximum: {available_stock + curr_cart_qty}", parent=self.root)
                return
            
            # Check if product exists in cart - update if it does
            found = False
            for index, item in enumerate(self.cart_list):
                if item.get('name', '') == product_name:
                    # Update quantity
                    self.cart_list[index]['qty'] = qty
                    found = True
                    print(f"Updated {product_name} in cart to qty: {qty}")
                    break
                
            # If it doesn't exist, add new item
            if not found:
                # Convert price to float, handle invalid input
                try:
                    price = float(self.product_price.get())
                except ValueError:
                    messagebox.showerror("Error", "Invalid price format", parent=self.root)
                    return
                
                # Add to cart
                cart_data = {
                    "name": product_name,
                    "price": price,
                    "qty": qty
                }
                self.cart_list.append(cart_data)
                print(f"Added {product_name} to cart, qty: {qty}")
            
            self.update_cart_display()
            self.calculate_totals()
            self.update_stock_label(product_name)
            
            # After updating cart, refresh product list to show updated quantities
            self.refresh_product_list()
            
            # Debug: Verify database contents directly
            self.debug_verify_product(product_name)
            
            self.clear_cart()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error adding to cart: {e}", parent=self.root)
            print(f"Error details: {e}")

    def update_cart_display(self):
        """Update the cart display with current cart items"""
        try:
            # Clear previous data
            for item in self.cart_table.get_children():
                self.cart_table.delete(item)
            
            for i, item in enumerate(self.cart_list):
                # Get values safely
                name = str(item.get('name', ''))
                
                # Format price
                try:
                    price = float(item.get('price', 0))
                    price_str = f"{price:.2f}"
                except (ValueError, TypeError):
                    price_str = "0.00"
                    
                # Format quantity
                try:
                    qty = int(item.get('qty', 0))
                    qty_str = str(qty)
                except (ValueError, TypeError):
                    qty_str = "0"
                    
                # Insert into treeview (pid, name, price, qty)
                self.cart_table.insert("", END, values=(i+1, name, price_str, qty_str))
                
            # Update cart title
            self.cart_title.config(text=f"Cart   Total Products: [{len(self.cart_list)}]")
        except Exception as e:
            print(f"Error updating cart display: {e}")

    def clear_cart(self):
        """Clear product selection fields"""
        self.product_name.set("")
        self.product_price.set("")
        self.product_qty.set("")
        self.stock_lbl.config(text="In Stock", fg="black")

    def clear_all(self):
        """Clear all cart data and reset fields"""
        self.cart_list = []
        self.product_stock = {}  # Reset stock tracking
        self.cust_name.set("")
        self.cust_contact.set("")
        self.update_cart_display()
        self.clear_cart()
        self.bill_amount.set("0")
        self.net_pay.set("0")
        self.bill_no = ""  # Reset bill number
        self.clear_bill_area()  # Reset bill area

    def calculate_totals(self):
        """Calculate bill amount, discount and net pay"""
        try:
            # Calculate total from cart
            total = 0
            for item in self.cart_list:
                try:
                    # Safely get price and quantity
                    price = float(item.get('price', 0))
                    qty = int(item.get('qty', 0))
                    total += price * qty
                except (ValueError, TypeError):
                    # Skip items with invalid values
                    print(f"Warning: Invalid price or quantity for {item.get('name', 'unknown')}")
            
            self.bill_amount.set(f"{total:.2f}")
            
            # Calculate discount - handle non-numeric values
            try:
                # Remove '%' if present
                discount_text = self.discount.get().replace('%', '')
                discount_percentage = float(discount_text)
            except ValueError:
                # Default to 0% if invalid
                discount_percentage = 0
                self.discount.set("0")
                
            discount_amount = total * (discount_percentage / 100)
            net_pay = total - discount_amount
            self.net_pay.set(f"{net_pay:.2f}")
        except Exception as e:
            print(f"Error calculating totals: {e}")
            self.bill_amount.set("0")
            self.net_pay.set("0")
        
    # Calculator functions
    def get_input(self, num):
        if self.product_qty.get() == "":
            self.product_qty.set(str(num))
        else:
            xnum = self.product_qty.get() + str(num)
            self.product_qty.set(xnum)
            
    def clear_cal(self):
        self.product_qty.set("")
        
    def perform_cal(self):
        if self.product_qty.get() != "":
            try:
                result = eval(self.product_qty.get())
                self.product_qty.set(result)
            except Exception as e:
                self.product_qty.set("")
                print(f"Error: {e}")

    def logout(self):
        self.root.destroy()
        import subprocess
        subprocess.Popen(["python3", "login.py"])

    def update_stock_label(self, product_name=None):
        """Update the stock label based on cart contents"""
        try:
            if not product_name:
                product_name = self.product_name.get()
                if not product_name:
                    return
            
            # If product is in our stock dictionary
            if product_name in self.product_stock:
                # Get original stock
                original_stock = self.product_stock[product_name]
                
                # Calculate how much is in cart currently
                in_cart = 0
                for item in self.cart_list:
                    if item.get('name', '') == product_name:
                        try:
                            in_cart = int(item.get('qty', 0))
                        except (ValueError, TypeError):
                            in_cart = 0
                        break
                
                # Calculate remaining stock
                remaining = original_stock - in_cart
                
                # Update labels
                if remaining > 0:
                    self.stock_lbl.config(text=f"In Stock [{remaining}]", fg="green")
                    self.stock_status_label.config(text=f"Current Stock: {product_name} - {remaining} units available", fg="green")
                else:
                    self.stock_lbl.config(text="Out of Stock", fg="red")
                    self.stock_status_label.config(text=f"Out of Stock: {product_name}", fg="red")
            else:
                # No stock info available
                self.stock_lbl.config(text="Stock Unknown", fg="orange")
                self.stock_status_label.config(text=f"Stock Unknown: {product_name}", fg="orange")
        except Exception as e:
            print(f"Error updating stock label: {e}")
            self.stock_lbl.config(text="Stock Error", fg="red")

    def refresh_product_list(self):
        """Refresh the product list to show current stock levels"""
        # Clear current display
        for item in self.product_table.get_children():
            self.product_table.delete(item)
        
        try:
            # Direct database query to get fresh data
            products = self.db.products.find({})
            
            # Debug: Print products to verify we're getting data
            print("Refreshing product list...")
            
            for row in products:
                # Debug: Print each product
                print(f"Product: {row.get('name')}, Qty: {row.get('quantity')}")
                
                # Insert with values directly from database
                self.product_table.insert("", END, values=(
                    row.get('_id', ''),
                    row.get('name', ''),
                    row.get('price', ''),
                    row.get('quantity', ''),  # This should be the updated quantity
                    row.get('status', '')
                ))
            
            # Update the stock status label
            self.stock_status_label.config(text="Current Stock Status: Product list refreshed")
        except Exception as e:
            print(f"Error refreshing product list: {e}")

    def generate_bill(self):
        """Generate and save bill, update product quantities in database"""
        if not self.cart_list:
            messagebox.showerror("Error", "No products in cart!", parent=self.root)
            return
        
        if not self.cust_name.get() or not self.cust_contact.get():
            messagebox.showerror("Error", "Customer information is required!", parent=self.root)
            return
        
        try:
            # Confirm with user
            if not messagebox.askyesno("Confirm", "Generate bill and update stock?", parent=self.root):
                return
            
            # Generate a simple bill number - just use current timestamp
            self.bill_no = str(int(time.time()) % 10000)  # Last 4 digits of current timestamp
            
            # Process each item in cart - update quantities
            for item in self.cart_list:
                product_name = item.get('name', '')
                qty_sold = item.get('qty', 0)
                
                # Skip invalid items
                if not product_name or not qty_sold:
                    continue
                
                # Find and update product in database
                try:
                    product = self.db.products.find_one({"name": product_name})
                    if product:
                        # Calculate new quantity
                        current_qty = int(product.get('quantity', 0))
                        new_qty = max(0, current_qty - int(qty_sold))
                        
                        # Update product
                        self.db.products.update_one(
                            {"name": product_name},
                            {"$set": {"quantity": new_qty}}
                        )
                        
                        # Update status if needed
                        if new_qty == 0:
                            self.db.products.update_one(
                                {"name": product_name},
                                {"$set": {"status": "Inactive"}}
                            )
                except Exception as e:
                    print(f"Error updating {product_name}: {e}")
            
            # Display the bill
            self.display_bill(self.bill_no)
            
            # Save sale to database
            try:
                sale_data = {
                    "bill_no": self.bill_no,
                    "customer_name": self.cust_name.get(),
                    "customer_contact": self.cust_contact.get(),
                    "items": self.cart_list,
                    "bill_amount": float(self.bill_amount.get()),
                    "discount": float(self.discount.get().replace('%', '')),
                    "net_amount": float(self.net_pay.get()),
                    "date": datetime.datetime.now()
                }
                
                self.db.sales.insert_one(sale_data)
                print(f"Sale saved with bill number: {self.bill_no}")
                
                # Save to file
                self.save_bill_to_file()
                
                # Show success message
                messagebox.showinfo("Success", "Bill generated successfully!", parent=self.root)
                
            except Exception as e:
                print(f"Error saving sale: {e}")
            
            # Clear cart and reload products
            self.clear_all()
            self.show_all_products()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error generating bill: {e}", parent=self.root)
            print(f"Error details: {e}")

    def display_bill(self, bill_no):
        """Display the bill in the billing area"""
        try:
            # Save the bill number for later use (like printing)
            self.bill_no = bill_no
            
            # Clear the bill area first
            self.bill_area.delete(1.0, END)
            
            # Ensure the text widget is editable
            self.bill_area.config(state="normal")
            
            # Get current date and time
            current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Shop information with proper formatting
            bill_text = ""
            bill_text += "\n"
            bill_text += "\t   INVENTORY MANAGEMENT SYSTEM\n"
            bill_text += "\t   ----------------------------\n"
            bill_text += "   Phone: 975242***** | Email: info@inventory.com\n"
            bill_text += "   Address: 123 Main Street, Lahore-154267\n\n"
            
            # Bill information
            bill_text += "="*50 + "\n"
            bill_text += f"Bill No: {bill_no}\t\tDate: {current_date}\n"
            bill_text += f"Customer Name: {self.cust_name.get()}\n"
            bill_text += f"Contact: {self.cust_contact.get()}\n"
            bill_text += "="*50 + "\n"
            
            # Column headers with proper spacing
            bill_text += f"{'Item':<25}{'Price':<10}{'Qty':<5}{'Total':<10}\n"
            bill_text += "-"*50 + "\n"
            
            # Add each product with better spacing
            for item in self.cart_list:
                name = item.get('name', '')
                if len(name) > 24:  # Truncate long names
                    name = name[:21] + "..."
                price = float(item.get('price', 0))
                qty = int(item.get('qty', 0))
                total = price * qty
                
                # Format each line with proper spacing
                bill_text += f"{name:<25}{price:<10.2f}{qty:<5}{total:<10.2f}\n"
            
            # Separator
            bill_text += "-"*50 + "\n"
            
            # Financial information with better alignment
            bill_amt = float(self.bill_amount.get())
            discount_percent = float(self.discount.get().replace('%', ''))
            discount_amount = bill_amt * (discount_percent / 100)
            net_pay = float(self.net_pay.get())
            
            bill_text += f"{'Subtotal:':<25}{bill_amt:>25.2f}\n"
            bill_text += f"{'Discount (' + str(discount_percent) + '%):':<25}{discount_amount:>25.2f}\n"
            bill_text += f"{'Net Amount:':<25}{net_pay:>25.2f}\n\n"
            
            # Add thank you message
            bill_text += "-"*50 + "\n"
            bill_text += f"{'Thank You For Shopping With Us!':<50}\n"
            bill_text += "-"*50 + "\n"
            
            # Add the whole text at once
            self.bill_area.insert("1.0", bill_text)
            
            # Make the text widget read-only to prevent editing
            self.bill_area.config(state="disabled")
            
            # Force update and show the beginning
            self.bill_area.update()
            self.bill_area.see("1.0")
            
            # For debugging
            print("Bill content generated:")
            print(bill_text)
            
        except Exception as e:
            print(f"Error displaying bill: {e}")
            # Show error in bill area
            self.bill_area.delete(1.0, END)
            self.bill_area.insert(END, f"Error generating bill: {e}")
            import traceback
            traceback.print_exc()

    def save_bill_to_file(self):
        """Save the bill content to a text file"""
        try:
            # Create bills directory if it doesn't exist
            if not os.path.exists("bills"):
                os.makedirs("bills")
            
            # Create simple filename
            bill_file = f"bills/Bill_{self.bill_no}.txt"
            
            # Open file and write bill content
            with open(bill_file, "w") as f:
                bill_content = self.bill_area.get(1.0, END)
                f.write(bill_content)
                
            print(f"Bill saved to {bill_file}")
            return True
        except Exception as e:
            print(f"Error saving bill to file: {e}")
            return False

    def debug_verify_product(self, product_name=None):
        """Debug function to verify database contents directly"""
        print("\n=== DATABASE VERIFICATION ===")
        
        if product_name:
            # Check specific product
            product = self.db.products.find_one({"name": product_name})
            if product:
                print(f"DB Entry - Name: {product.get('name')}, Qty: {product.get('quantity')}, Status: {product.get('status')}")
            else:
                print(f"Product '{product_name}' not found in database")
        else:
            # Check all products
            print("All products in database:")
            products = self.db.products.find({})
            for product in products:
                print(f"DB Entry - Name: {product.get('name')}, Qty: {product.get('quantity')}, Status: {product.get('status')}")
        
        print("===========================\n")

    def clear_bill_area(self):
        """Clear the bill area and add an empty bill template"""
        self.bill_area.delete(1.0, END)
        self.bill_area.insert(END, "\n")
        self.bill_area.insert(END, "\t   INVENTORY MANAGEMENT SYSTEM\n")
        self.bill_area.insert(END, "\t   ----------------------------\n")
        self.bill_area.insert(END, "   Phone: 975242***** | Email: info@inventory.com\n")
        self.bill_area.insert(END, "   Address: 123 Main Street, Lahore-154267\n\n")
        self.bill_area.insert(END, "="*50 + "\n")
        self.bill_area.insert(END, "Bill No: \t\t\tDate: \n")
        self.bill_area.insert(END, "Customer Name: \n")
        self.bill_area.insert(END, "Contact: \n")
        self.bill_area.insert(END, "="*50 + "\n")
        self.bill_area.insert(END, f"{'Item':<25}{'Price':<10}{'Qty':<5}{'Total':<10}\n")
        self.bill_area.insert(END, "-"*50 + "\n")
        self.bill_area.insert(END, "\n\n" + "-"*50 + "\n")
        self.bill_area.insert(END, f"{'Thank You For Shopping With Us!':<50}\n")
        self.bill_area.insert(END, "-"*50 + "\n")

    def print_bill(self):
        """Print the bill"""
        if not self.bill_no:
            messagebox.showerror("Error", "No bill to print! Please generate a bill first.", parent=self.root)
            return
            
        # Get the bill content
        bill_content = self.bill_area.get(1.0, END)
        if not bill_content.strip():
            messagebox.showerror("Error", "Bill is empty!", parent=self.root)
            return
            
        # Create bills directory if it doesn't exist
        if not os.path.exists("bills"):
            os.makedirs("bills")
            
        # Save to file for printing
        bill_file = f"bills/Bill_{self.bill_no}.txt"
        try:
            with open(bill_file, "w") as f:
                f.write(bill_content)
                
            # Confirm and open file
            if messagebox.askyesno("Print", "Bill saved. Do you want to open it?", parent=self.root):
                # Open with default application
                import webbrowser
                webbrowser.open(bill_file)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error printing bill: {e}", parent=self.root)
            print(f"Error printing bill: {e}")


if __name__=="__main__":
        root = Tk()
        obj = BillingClass(root)
        root.mainloop()