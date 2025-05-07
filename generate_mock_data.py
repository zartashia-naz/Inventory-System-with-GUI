import datetime
from datetime import timedelta
import random
import pymongo
from database import MongoDBConnection
import string

def main():
    """Generate comprehensive mock data for all collections in the database"""
    # Initialize database connection
    db = MongoDBConnection()
    
    print("Connected to MongoDB successfully!")
    print("Starting comprehensive mock data generation...")
    
    # Generate data for each collection
    create_categories(db)
    create_suppliers(db)
    create_employees(db)
    create_products(db)
    create_sales(db)
    
    print("Mock data generation complete!")
    print("You can now test the AI Assistant with various queries.")

def create_categories(db):
    """Create mock categories"""
    # Sample categories with descriptions
    categories = [
        {"category_id": "C0001", "name": "Electronics", "description": "Electronic devices and gadgets"},
        {"category_id": "C0002", "name": "Clothing", "description": "Apparel and fashion items"},
        {"category_id": "C0003", "name": "Groceries", "description": "Food and household supplies"},
        {"category_id": "C0004", "name": "Home Appliances", "description": "Kitchen and home equipment"},
        {"category_id": "C0005", "name": "Toys", "description": "Games and toys for children"},
        {"category_id": "C0006", "name": "Sports", "description": "Sporting goods and equipment"},
        {"category_id": "C0007", "name": "Books", "description": "Books, magazines and educational materials"},
        {"category_id": "C0008", "name": "Furniture", "description": "Home and office furniture"},
        {"category_id": "C0009", "name": "Beauty", "description": "Cosmetics and personal care products"},
        {"category_id": "C0010", "name": "Automotive", "description": "Car parts and accessories"}
    ]
    
    # Insert categories
    count = 0
    for category in categories:
        # Check if category already exists
        if db.categories.count_documents({"category_id": category["category_id"]}) == 0:
            db.categories.insert_one(category)
            count += 1
    
    print(f"Added {count} new categories. Total categories: {db.categories.count_documents({})}")

def create_suppliers(db):
    """Create mock suppliers"""
    # Sample suppliers
    suppliers = [
        {
            "supplier_id": "S0001",
            "name": "TechGiant",
            "contact": "John Smith",
            "email": "john@techgiant.com",
            "phone": "555-123-4567",
            "address": "123 Tech Blvd, Silicon Valley, CA"
        },
        {
            "supplier_id": "S0002",
            "name": "FashionWorld",
            "contact": "Emma Johnson",
            "email": "emma@fashionworld.com",
            "phone": "555-234-5678",
            "address": "456 Fashion Ave, New York, NY"
        },
        {
            "supplier_id": "S0003",
            "name": "FoodCorp",
            "contact": "David Lee",
            "email": "david@foodcorp.com",
            "phone": "555-345-6789",
            "address": "789 Food St, Chicago, IL"
        },
        {
            "supplier_id": "S0004",
            "name": "HomeEssentials",
            "contact": "Sarah Brown",
            "email": "sarah@homeessentials.com",
            "phone": "555-456-7890",
            "address": "321 Home Rd, Boston, MA"
        },
        {
            "supplier_id": "S0005",
            "name": "ToyLand",
            "contact": "Michael Wilson",
            "email": "michael@toyland.com",
            "phone": "555-567-8901",
            "address": "654 Toy Ln, Orlando, FL"
        },
        {
            "supplier_id": "S0006",
            "name": "SportsMaster",
            "contact": "Jessica Davis",
            "email": "jessica@sportsmaster.com",
            "phone": "555-678-9012",
            "address": "987 Sports Way, Denver, CO"
        },
        {
            "supplier_id": "S0007",
            "name": "BookHaven",
            "contact": "Robert Taylor",
            "email": "robert@bookhaven.com",
            "phone": "555-789-0123",
            "address": "246 Book Ct, Seattle, WA"
        },
        {
            "supplier_id": "S0008",
            "name": "FurniturePlus",
            "contact": "Jennifer Martin",
            "email": "jennifer@furnitureplus.com",
            "phone": "555-890-1234",
            "address": "135 Furniture Blvd, Atlanta, GA"
        },
        {
            "supplier_id": "S0009",
            "name": "BeautyGlow",
            "contact": "Patricia Moore",
            "email": "patricia@beautyglow.com",
            "phone": "555-901-2345",
            "address": "753 Beauty St, Los Angeles, CA"
        },
        {
            "supplier_id": "S0010",
            "name": "AutoParts",
            "contact": "Thomas Jackson",
            "email": "thomas@autoparts.com",
            "phone": "555-012-3456",
            "address": "951 Auto Dr, Detroit, MI"
        }
    ]
    
    # Insert suppliers
    count = 0
    for supplier in suppliers:
        # Check if supplier already exists
        if db.suppliers.count_documents({"supplier_id": supplier["supplier_id"]}) == 0:
            db.suppliers.insert_one(supplier)
            count += 1
    
    print(f"Added {count} new suppliers. Total suppliers: {db.suppliers.count_documents({})}")

def create_employees(db):
    """Create mock employees with only Employee or Admin roles"""
    # Sample employees
    employees = [
        {
            "employee_id": "E0001",
            "name": "Alex Johnson",
            "email": "alex@inventory.com",
            "phone": "555-111-2222",
            "gender": "Male",
            "dob": datetime.datetime(1985, 5, 15),
            "hire_date": datetime.datetime(2020, 1, 10),
            "salary": 55000,
            "address": "111 Employee St, New York, NY",
            "role": "Admin"
        },
        {
            "employee_id": "E0002",
            "name": "Samantha Wilson",
            "email": "samantha@inventory.com",
            "phone": "555-222-3333",
            "gender": "Female",
            "dob": datetime.datetime(1990, 8, 22),
            "hire_date": datetime.datetime(2021, 3, 15),
            "salary": 48000,
            "address": "222 Worker Ave, Chicago, IL",
            "role": "Employee"
        },
        {
            "employee_id": "E0003",
            "name": "Daniel Brown",
            "email": "daniel@inventory.com",
            "phone": "555-333-4444",
            "gender": "Male",
            "dob": datetime.datetime(1988, 2, 10),
            "hire_date": datetime.datetime(2019, 11, 5),
            "salary": 52000,
            "address": "333 Staff Blvd, Los Angeles, CA",
            "role": "Employee"
        },
        {
            "employee_id": "E0004",
            "name": "Emily Davis",
            "email": "emily@inventory.com",
            "phone": "555-444-5555",
            "gender": "Female",
            "dob": datetime.datetime(1992, 12, 3),
            "hire_date": datetime.datetime(2022, 1, 20),
            "salary": 45000,
            "address": "444 Team Rd, Houston, TX",
            "role": "Employee"
        },
        {
            "employee_id": "E0005",
            "name": "James Miller",
            "email": "james@inventory.com",
            "phone": "555-555-6666",
            "gender": "Male",
            "dob": datetime.datetime(1983, 7, 8),
            "hire_date": datetime.datetime(2018, 6, 12),
            "salary": 60000,
            "address": "555 Personnel St, Miami, FL",
            "role": "Admin"
        },
        {
            "employee_id": "E0006",
            "name": "Sophia Garcia",
            "email": "sophia@inventory.com",
            "phone": "555-666-7777",
            "gender": "Female",
            "dob": datetime.datetime(1995, 4, 17),
            "hire_date": datetime.datetime(2022, 2, 28),
            "salary": 47000,
            "address": "666 Worker Ln, Phoenix, AZ",
            "role": "Employee"
        },
        {
            "employee_id": "E0007",
            "name": "William Rodriguez",
            "email": "william@inventory.com",
            "phone": "555-777-8888",
            "gender": "Male",
            "dob": datetime.datetime(1987, 9, 25),
            "hire_date": datetime.datetime(2020, 8, 3),
            "salary": 53000,
            "address": "777 Staff Dr, Philadelphia, PA",
            "role": "Employee"
        },
        {
            "employee_id": "E0008",
            "name": "Olivia Martinez",
            "email": "olivia@inventory.com",
            "phone": "555-888-9999",
            "gender": "Female",
            "dob": datetime.datetime(1991, 1, 30),
            "hire_date": datetime.datetime(2021, 5, 17),
            "salary": 49000,
            "address": "888 Team Ct, San Antonio, TX",
            "role": "Employee"
        }
    ]
    
    # Insert employees
    count = 0
    for employee in employees:
        # Check if employee already exists
        if db.employees.count_documents({"employee_id": employee["employee_id"]}) == 0:
            db.employees.insert_one(employee)
            count += 1
    
    print(f"Added {count} new employees. Total employees: {db.employees.count_documents({})}")

def create_products(db):
    """Create mock products with realistic data"""
    # Get existing categories and suppliers
    categories = list(db.categories.find({}, {"name": 1}))
    suppliers = list(db.suppliers.find({}, {"name": 1}))
    
    if not categories or not suppliers:
        print("Error: Categories and suppliers must be created first")
        return
    
    # Sample products with varied details
    sample_products = [
        # Electronics
        {"product_id": "P0001", "name": "Smartphone X", "category": "Electronics", "supplier": "TechGiant", 
         "price": 699.99, "quantity": 25, "status": "Active"},
        {"product_id": "P0002", "name": "Laptop Pro", "category": "Electronics", "supplier": "TechGiant", 
         "price": 1299.99, "quantity": 15, "status": "Active"},
        {"product_id": "P0003", "name": "Wireless Earbuds", "category": "Electronics", "supplier": "TechGiant", 
         "price": 149.99, "quantity": 40, "status": "Active"},
        {"product_id": "P0004", "name": "Smart Watch", "category": "Electronics", "supplier": "TechGiant", 
         "price": 249.99, "quantity": 20, "status": "Active"},
        {"product_id": "P0005", "name": "Tablet Mini", "category": "Electronics", "supplier": "TechGiant", 
         "price": 399.99, "quantity": 18, "status": "Active"},
        {"product_id": "P0006", "name": "Bluetooth Speaker", "category": "Electronics", "supplier": "TechGiant", 
         "price": 89.99, "quantity": 35, "status": "Active"},
        {"product_id": "P0007", "name": "Gaming Console", "category": "Electronics", "supplier": "TechGiant", 
         "price": 499.99, "quantity": 12, "status": "Active"},
        {"product_id": "P0008", "name": "Wireless Mouse", "category": "Electronics", "supplier": "TechGiant", 
         "price": 29.99, "quantity": 50, "status": "Active"},
        
        # Clothing
        {"product_id": "P0009", "name": "Designer Jeans", "category": "Clothing", "supplier": "FashionWorld", 
         "price": 79.99, "quantity": 50, "status": "Active"},
        {"product_id": "P0010", "name": "Winter Jacket", "category": "Clothing", "supplier": "FashionWorld", 
         "price": 129.99, "quantity": 30, "status": "Active"},
        {"product_id": "P0011", "name": "Cotton T-shirt", "category": "Clothing", "supplier": "FashionWorld", 
         "price": 24.99, "quantity": 75, "status": "Active"},
        {"product_id": "P0012", "name": "Formal Shoes", "category": "Clothing", "supplier": "FashionWorld", 
         "price": 89.99, "quantity": 25, "status": "Active"},
        {"product_id": "P0013", "name": "Summer Dress", "category": "Clothing", "supplier": "FashionWorld", 
         "price": 59.99, "quantity": 35, "status": "Active"},
        
        # Groceries
        {"product_id": "P0014", "name": "Organic Apples (1kg)", "category": "Groceries", "supplier": "FoodCorp", 
         "price": 5.99, "quantity": 100, "status": "Active"},
        {"product_id": "P0015", "name": "Whole Grain Bread", "category": "Groceries", "supplier": "FoodCorp", 
         "price": 3.99, "quantity": 45, "status": "Active"},
        {"product_id": "P0016", "name": "Free-Range Eggs (12pk)", "category": "Groceries", "supplier": "FoodCorp", 
         "price": 4.99, "quantity": 60, "status": "Active"},
        {"product_id": "P0017", "name": "Organic Milk (1L)", "category": "Groceries", "supplier": "FoodCorp", 
         "price": 2.99, "quantity": 80, "status": "Active"},
        
        # Home Appliances
        {"product_id": "P0018", "name": "Coffee Maker", "category": "Home Appliances", "supplier": "HomeEssentials", 
         "price": 89.99, "quantity": 20, "status": "Active"},
        {"product_id": "P0019", "name": "Microwave Oven", "category": "Home Appliances", "supplier": "HomeEssentials", 
         "price": 149.99, "quantity": 15, "status": "Active"},
        {"product_id": "P0020", "name": "Toaster", "category": "Home Appliances", "supplier": "HomeEssentials", 
         "price": 49.99, "quantity": 30, "status": "Active"},
        {"product_id": "P0021", "name": "Blender", "category": "Home Appliances", "supplier": "HomeEssentials", 
         "price": 69.99, "quantity": 25, "status": "Active"},
        
        # Toys
        {"product_id": "P0022", "name": "Action Figure", "category": "Toys", "supplier": "ToyLand", 
         "price": 19.99, "quantity": 45, "status": "Active"},
        {"product_id": "P0023", "name": "Board Game", "category": "Toys", "supplier": "ToyLand", 
         "price": 29.99, "quantity": 35, "status": "Active"},
        {"product_id": "P0024", "name": "Building Blocks Set", "category": "Toys", "supplier": "ToyLand", 
         "price": 39.99, "quantity": 30, "status": "Active"},
        
        # Sports
        {"product_id": "P0025", "name": "Yoga Mat", "category": "Sports", "supplier": "SportsMaster", 
         "price": 24.99, "quantity": 40, "status": "Active"},
        {"product_id": "P0026", "name": "Basketball", "category": "Sports", "supplier": "SportsMaster", 
         "price": 29.99, "quantity": 25, "status": "Active"},
        {"product_id": "P0027", "name": "Tennis Racket", "category": "Sports", "supplier": "SportsMaster", 
         "price": 99.99, "quantity": 15, "status": "Active"},
        
        # Books
        {"product_id": "P0028", "name": "Bestseller Novel", "category": "Books", "supplier": "BookHaven", 
         "price": 14.99, "quantity": 50, "status": "Active"},
        {"product_id": "P0029", "name": "Cookbook", "category": "Books", "supplier": "BookHaven", 
         "price": 19.99, "quantity": 30, "status": "Active"},
        {"product_id": "P0030", "name": "Children's Book", "category": "Books", "supplier": "BookHaven", 
         "price": 9.99, "quantity": 45, "status": "Active"},
        
        # Furniture
        {"product_id": "P0031", "name": "Office Chair", "category": "Furniture", "supplier": "FurniturePlus", 
         "price": 149.99, "quantity": 10, "status": "Active"},
        {"product_id": "P0032", "name": "Coffee Table", "category": "Furniture", "supplier": "FurniturePlus", 
         "price": 199.99, "quantity": 8, "status": "Active"},
        {"product_id": "P0033", "name": "Bookshelf", "category": "Furniture", "supplier": "FurniturePlus", 
         "price": 129.99, "quantity": 12, "status": "Active"},
        
        # Beauty
        {"product_id": "P0034", "name": "Facial Cleanser", "category": "Beauty", "supplier": "BeautyGlow", 
         "price": 12.99, "quantity": 40, "status": "Active"},
        {"product_id": "P0035", "name": "Moisturizer", "category": "Beauty", "supplier": "BeautyGlow", 
         "price": 15.99, "quantity": 35, "status": "Active"},
        {"product_id": "P0036", "name": "Shampoo", "category": "Beauty", "supplier": "BeautyGlow", 
         "price": 8.99, "quantity": 50, "status": "Active"},
        
        # Automotive
        {"product_id": "P0037", "name": "Motor Oil", "category": "Automotive", "supplier": "AutoParts", 
         "price": 22.99, "quantity": 30, "status": "Active"},
        {"product_id": "P0038", "name": "Windshield Wipers", "category": "Automotive", "supplier": "AutoParts", 
         "price": 15.99, "quantity": 40, "status": "Active"},
        {"product_id": "P0039", "name": "Car Air Freshener", "category": "Automotive", "supplier": "AutoParts", 
         "price": 5.99, "quantity": 60, "status": "Active"},
        {"product_id": "P0040", "name": "Bluetooth Car Adapter", "category": "Automotive", "supplier": "AutoParts", 
         "price": 24.99, "quantity": 25, "status": "Active"}
    ]
    
    # Insert products
    count = 0
    for product in sample_products:
        # Check if product already exists
        if db.products.count_documents({"product_id": product["product_id"]}) == 0:
            db.products.insert_one(product)
            count += 1
    
    print(f"Added {count} new products. Total products: {db.products.count_documents({})}")

def create_sales(db):
    """Create mock sales data for the last 3 months with realistic patterns"""
    # Get all product IDs
    products = list(db.products.find({}, {"product_id": 1, "name": 1, "price": 1}))
    
    if not products:
        print("Error: Products must be created first")
        return
    
    # Get employees for associating with sales
    employees = list(db.employees.find({}, {"employee_id": 1, "name": 1}))
    if not employees:
        employees = [{"employee_id": "E0001", "name": "Default Employee"}]
    
    # Generate sales for last 3 months
    end_date = datetime.datetime.now()
    start_date = end_date - timedelta(days=90)  # 3 months
    
    # Clear existing sales if needed
    existing_sales = db.sales.count_documents({"date": {"$gte": start_date, "$lte": end_date}})
    if existing_sales > 0:
        # Automatically delete existing sales to avoid user input prompt
        db.sales.delete_many({"date": {"$gte": start_date, "$lte": end_date}})
        print(f"Deleted {existing_sales} existing sales records.")
    
    # Generate sales records with realistic patterns
    sales_records = []
    sale_id_counter = db.sales.count_documents({}) + 1
    
    # Create customer names for invoices
    first_names = ["John", "Emma", "Michael", "Sophia", "William", "Olivia", "James", "Ava", "Robert", "Mia", 
                  "David", "Isabella", "Joseph", "Charlotte", "Thomas", "Amelia", "Charles", "Harper", "Daniel", "Evelyn"]
    last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", 
                 "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson"]
    
    print(f"Generating sales data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}...")
    
    # Different patterns for weekdays vs weekends
    current_date = start_date
    while current_date <= end_date:
        # More sales on weekends and at month end
        is_weekend = current_date.weekday() >= 5  # 5 = Saturday, 6 = Sunday
        is_month_end = current_date.day >= 25
        
        # Determine number of sales based on day type
        if is_weekend:
            daily_sales = random.randint(5, 15)  # More sales on weekends
        elif is_month_end:
            daily_sales = random.randint(6, 12)  # More sales at month end
        else:
            daily_sales = random.randint(3, 8)   # Normal weekdays
        
        # Generate specific time for each sale
        for _ in range(daily_sales):
            # Random time between 9 AM and 9 PM
            hour = random.randint(9, 21)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            sale_timestamp = current_date.replace(hour=hour, minute=minute, second=second)
            
            # Random customer name
            customer_name = f"{random.choice(first_names)} {random.choice(last_names)}"
            
            # Random employee handling the sale
            employee = random.choice(employees)
            
            # Generate items for this sale (1-5 items per sale)
            num_items = random.randint(1, 5)
            items = []
            total_amount = 0
            
            # Choose random products
            sale_products = random.sample(products, min(num_items, len(products)))
            
            for product in sale_products:
                # Random quantity between 1 and 3 for each product
                quantity = random.randint(1, 3)
                
                # Calculate item total
                item_price = product["price"]
                item_total = quantity * item_price
                total_amount += item_total
                
                # Add item to sale
                items.append({
                    "product_id": product["product_id"],
                    "product_name": product["name"],
                    "quantity": quantity,
                    "price": item_price,
                    "item_total": item_total
                })
            
            # Apply random discount occasionally (10% of sales)
            discount = 0
            if random.random() < 0.1:  # 10% chance of discount
                discount_rate = random.choice([0.05, 0.1, 0.15])  # 5%, 10%, or 15% discount
                discount = total_amount * discount_rate
                total_amount -= discount
            
            # Add tax (varies by category)
            tax_rate = 0.085  # 8.5% tax
            tax = total_amount * tax_rate
            grand_total = total_amount + tax
            
            # Create sale record
            invoice_no = f"INV{str(sale_id_counter).zfill(5)}"
            sale_record = {
                "sale_id": f"S{str(sale_id_counter).zfill(5)}",
                "invoice_no": invoice_no,
                "date": sale_timestamp,
                "customer_name": customer_name,
                "employee_id": employee.get("employee_id"),
                "employee_name": employee.get("name"),
                "items": items,
                "subtotal": total_amount,
                "discount": discount,
                "tax": tax,
                "amount": grand_total,
                "payment_method": random.choice(["Cash", "Credit Card", "Debit Card", "Mobile Payment"]),
                "status": "Completed"
            }
            
            sales_records.append(sale_record)
            sale_id_counter += 1
        
        # Move to next day
        current_date += timedelta(days=1)
    
    # Insert sales records
    if sales_records:
        # Insert in batches to avoid large transactions
        batch_size = 100
        for i in range(0, len(sales_records), batch_size):
            batch = sales_records[i:i+batch_size]
            db.sales.insert_many(batch)
            print(f"Added batch of {len(batch)} sales records...")
        
        print(f"Added total of {len(sales_records)} sales records for the last 3 months.")
    else:
        print("No sales records were created.")

if __name__ == "__main__":
    main() 