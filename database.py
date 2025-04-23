from pymongo import MongoClient
from tkinter import messagebox
from datetime import datetime

class MongoDBConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
            cls._instance._initialize_connection()
        return cls._instance
    
    def _initialize_connection(self):
        try:
            # # Local MongoDB connection
            # self.client = MongoClient('mongodb://localhost:27017/')
            
            # For MongoDB Atlas (cloud), use:
            self.client = MongoClient('mongodb+srv://zartashianazz:Db_12345@cluster0.sflddnu.mongodb.net/')
            
            self.db = self.client['inventory_management_system']
            
            # Initialize collections
            self.employees = self.db['employees']
            self.suppliers = self.db['suppliers']
            self.categories = self.db['categories']
            self.products = self.db['products']
            self.sales = self.db['sales']
            
            # Create indexes for better performance
            self._create_indexes()
            
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to connect to MongoDB: {str(e)}")
            raise
    
    def _create_indexes(self):
        # Create indexes for faster queries
        self.employees.create_index("employee_id", unique=True)
        self.suppliers.create_index("supplier_id", unique=True)
        self.categories.create_index("category_id", unique=True)
        self.products.create_index("product_id", unique=True)
        self.sales.create_index("sale_id", unique=True)
    
    def get_employee_count(self):
        return self.employees.count_documents({})
    
    def get_supplier_count(self):
        return self.suppliers.count_documents({})
    
    def get_category_count(self):
        return self.categories.count_documents({})
    
    def get_product_count(self):
        return self.products.count_documents({})
    
    def get_total_sales(self):
        pipeline = [
            {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
        ]
        result = list(self.sales.aggregate(pipeline))
        return result[0]['total'] if result else 0