import tkinter as tk
from tkinter import ttk
from datetime import datetime

class InventoryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Main frame
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.create_header()
        
        # Stats section
        self.create_stats_section()
        
        # Menu section
        self.create_menu_section()
        
        # Footer
        self.create_footer()
    
    def create_header(self):
        header_frame = tk.Frame(self.main_frame, bg="#2c3e50")
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title = tk.Label(
            header_frame, 
            text="Inventory Management System", 
            font=("Helvetica", 20, "bold"), 
            bg="#2c3e50", 
            fg="white"
        )
        title.pack(pady=10)
        
        # Date and time
        now = datetime.now()
        date_time = tk.Label(
            header_frame,
            text=f"Date: {now.strftime('%d-%m-%Y')}  |  Time: {now.strftime('%H:%M:%S')}",
            font=("Helvetica", 10),
            bg="#2c3e50",
            fg="white"
        )
        date_time.pack(pady=(0, 10))
    
    def create_stats_section(self):
        stats_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Employee count
        emp_frame = tk.Frame(stats_frame, bg="#f0f0f0")
        emp_frame.pack(side=tk.LEFT, expand=True)
        tk.Label(
            emp_frame, 
            text="Total Employee", 
            font=("Helvetica", 12, "bold"), 
            bg="#f0f0f0"
        ).pack()
        tk.Label(
            emp_frame, 
            text="[ 2 ]", 
            font=("Helvetica", 14), 
            bg="#f0f0f0"
        ).pack()
        
        # Supplier count
        sup_frame = tk.Frame(stats_frame, bg="#f0f0f0")
        sup_frame.pack(side=tk.LEFT, expand=True)
        tk.Label(
            sup_frame, 
            text="Total Supplier", 
            font=("Helvetica", 12, "bold"), 
            bg="#f0f0f0"
        ).pack()
        tk.Label(
            sup_frame, 
            text="[ 2 ]", 
            font=("Helvetica", 14), 
            bg="#f0f0f0"
        ).pack()
        
        # Category count
        cat_frame = tk.Frame(stats_frame, bg="#f0f0f0")
        cat_frame.pack(side=tk.LEFT, expand=True)
        tk.Label(
            cat_frame, 
            text="Total Category", 
            font=("Helvetica", 12, "bold"), 
            bg="#f0f0f0"
        ).pack()
        tk.Label(
            cat_frame, 
            text="[ 3 ]", 
            font=("Helvetica", 14), 
            bg="#f0f0f0"
        ).pack()
    
    def create_menu_section(self):
        menu_frame = tk.Frame(self.main_frame, bg="#ecf0f1", bd=2, relief=tk.GROOVE)
        menu_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Menu title
        tk.Label(
            menu_frame, 
            text="Menu", 
            font=("Helvetica", 14, "bold"), 
            bg="#3498db", 
            fg="white"
        ).pack(fill=tk.X, pady=(5, 10))
        
        # Menu items
        menu_items = ["Employee", "Supplier", "Category", "Products", "Sales", "Exit"]
        for item in menu_items:
            btn = tk.Button(
                menu_frame,
                text=item,
                font=("Helvetica", 12),
                bg="#3498db",
                fg="white",
                activebackground="#2980b9",
                activeforeground="white",
                bd=0,
                padx=20,
                pady=10,
                width=20,
                anchor="w"
            )
            btn.pack(fill=tk.X, padx=10, pady=2)
    
    def create_footer(self):
        footer_frame = tk.Frame(self.main_frame, bg="#2c3e50")
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Product and Sales count
        stats_frame = tk.Frame(footer_frame, bg="#2c3e50")
        stats_frame.pack(side=tk.LEFT, padx=20, pady=10)
        
        tk.Label(
            stats_frame, 
            text="Total Product [ 5 ]", 
            font=("Helvetica", 10), 
            bg="#2c3e50", 
            fg="white"
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Label(
            stats_frame, 
            text="Total Sales [ 1 ]", 
            font=("Helvetica", 10), 
            bg="#2c3e50", 
            fg="white"
        ).pack(side=tk.LEFT, padx=10)
        
        # Copyright
        tk.Label(
            footer_frame, 
            text="IMS-Inventory Management System | Developed By Kangesh", 
            font=("Helvetica", 10), 
            bg="#2c3e50", 
            fg="white"
        ).pack(side=tk.RIGHT, padx=20, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryManagementSystem(root)
    root.mainloop()