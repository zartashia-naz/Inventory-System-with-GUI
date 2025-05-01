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
        self.connected = False
        try:
            # # Local MongoDB connection
            # self.client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
            
            # For MongoDB Atlas (cloud), use:
            self.client = MongoClient('mongodb+srv://zartashianazz:Db_12345@cluster0.sflddnu.mongodb.net/', 
                                   serverSelectionTimeoutMS=5000, tlsAllowInvalidCertificates=True)
    # mongodb+srv://zartashianazz:<db_password>@cluster0.sflddnu.mongodb.net/
            # Test connection
            self.client.admin.command('ping')
            
            self.db = self.client['inventory_management_system']
            
            # Initialize collections
            self.employees = self.db['employees']
            self.suppliers = self.db['suppliers']
            self.categories = self.db['categories']
            self.products = self.db['products']
            self.sales = self.db['sales']
            
            # Create indexes for better performance - only if collections exist
            try:
                self._create_indexes()
            except Exception as e:
                print(f"Warning: Could not create indexes: {str(e)}")
                
            self.connected = True
            print("Connected to MongoDB successfully!")
            
        except Exception as e:
            print(f"Warning: Failed to connect to MongoDB: {str(e)}")
            messagebox.showwarning("Database Warning", 
                               "Could not connect to MongoDB. Application will run with limited functionality.")
    
    def _create_indexes(self):
        # Create indexes for faster queries - only if we're connected
        if self.connected:
            try:
                self.employees.create_index("employee_id", unique=True)
                self.suppliers.create_index("supplier_id", unique=True)
                self.categories.create_index("category_id", unique=True)
                self.products.create_index("product_id", unique=True)
                self.sales.create_index("sale_id", unique=True)
            except Exception as e:
                print(f"Warning: Failed to create indexes: {str(e)}")
    
    def get_employee_count(self):
        if not self.connected:
            return 0
        return self.employees.count_documents({})
    
    def get_supplier_count(self):
        if not self.connected:
            return 0
        return self.suppliers.count_documents({})
    
    def get_category_count(self):
        if not self.connected:
            return 0
        return self.categories.count_documents({})
    
    def get_product_count(self):
        if not self.connected:
            return 0
        return self.products.count_documents({})
    
    def get_total_sales(self):
        if not self.connected:
            return 0
        pipeline = [
            {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
        ]
        result = list(self.sales.aggregate(pipeline))
        return result[0]['total'] if result else 0