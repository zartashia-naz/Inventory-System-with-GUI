import random
import datetime
import pymongo
import os
from database import MongoDBConnection
from bson import ObjectId

def generate_sales_data():
    """
    Generate sales data for the last 3 months and store it in MongoDB
    Also generate bill text files for each sale
    """
    # Connect to the database
    db_conn = MongoDBConnection()
    print("Connected to MongoDB")
    
    # Get existing product data to use in sales
    products = list(db_conn.products.find({"status": "Active"}))
    if not products:
        print("No active products found in database. Creating sample products.")
        # Create some sample products if none exist
        sample_products = [
            {"name": "Laptops", "price": 75000, "quantity": 50, "category": "Electronics", "supplier": "Tech Inc", "status": "Active"},
            {"name": "Smartphones", "price": 45000, "quantity": 100, "category": "Electronics", "supplier": "Mobile World", "status": "Active"},
            {"name": "Tablets", "price": 35000, "quantity": 75, "category": "Electronics", "supplier": "Tech Inc", "status": "Active"},
            {"name": "Headphones", "price": 8500, "quantity": 200, "category": "Accessories", "supplier": "Audio Plus", "status": "Active"},
            {"name": "Monitors", "price": 25000, "quantity": 40, "category": "Electronics", "supplier": "Display Solutions", "status": "Active"}
        ]
        
        for product in sample_products:
            db_conn.products.insert_one(product)
        
        products = list(db_conn.products.find({"status": "Active"}))
    
    # Define customer information
    customers = [
        {"name": "ali", "contact": "03314526625"},
        {"name": "sara", "contact": "03224578932"},
        {"name": "ahmed", "contact": "03331234567"},
        {"name": "fatima", "contact": "03002345678"},
        {"name": "hassan", "contact": "03115678901"},
        {"name": "zainab", "contact": "03448765432"}
    ]
    
    # Create bills directory if it doesn't exist
    bills_dir = os.path.join(os.getcwd(), "bills")
    if not os.path.exists(bills_dir):
        os.makedirs(bills_dir)
        print(f"Created bills directory at {bills_dir}")
    
    # Get current date
    end_date = datetime.datetime.now()
    # Start date (3 months ago)
    start_date = end_date - datetime.timedelta(days=90)
    
    # Generate sales for each day
    current_date = start_date
    day_count = 0
    bill_number = 6480  # Starting bill number from your example
    total_sales_generated = 0
    
    print(f"Generating sales data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    while current_date <= end_date:
        # Determine number of sales for this day
        # More sales on weekends and month end
        is_weekend = current_date.weekday() >= 5  # 5 and 6 are weekend days
        is_month_end = current_date.day >= 25
        
        if is_weekend and is_month_end:
            num_sales = random.randint(8, 15)  # More sales on weekend month end
        elif is_weekend:
            num_sales = random.randint(5, 10)  # More sales on weekends
        elif is_month_end:
            num_sales = random.randint(5, 8)   # More sales on month end
        else:
            num_sales = random.randint(2, 5)   # Normal days
        
        # Generate sales for the day
        for _ in range(num_sales):
            # Create a sale at a random time on the current date
            sale_time = current_date.replace(
                hour=random.randint(9, 20),
                minute=random.randint(0, 59),
                second=random.randint(0, 59)
            )
            
            # Select a random customer
            customer = random.choice(customers)
            
            # Determine number of items in this sale (1-3 items)
            num_items = random.randint(1, 3)
            
            # Create items for the sale
            items = []
            bill_amount = 0
            
            for _ in range(num_items):
                # Select a random product
                product = random.choice(products)
                
                # Determine quantity (1-3 units)
                qty = random.randint(1, 3)
                
                # Calculate item total
                price = product["price"]
                item_total = price * qty
                bill_amount += item_total
                
                # Create items entry for MongoDB document
                items.append({
                    "product_id": str(product["_id"]),
                    "product_name": product["name"],
                    "quantity": qty,
                    "price": price,
                    "item_total": item_total
                })
            
            # Apply a random discount (0%, 5%, or 10%)
            discount_percentage = random.choice([0, 5, 10])
            discount_amount = (bill_amount * discount_percentage) / 100
            net_amount = bill_amount - discount_amount
            
            # Format sale ID
            sale_id = f"SALE_{sale_time.strftime('%Y%m%d%H%M%S')}_{bill_number}"
            
            # Create the sale document
            sale_doc = {
                "_id": ObjectId(),
                "sale_id": sale_id,
                "bill_no": str(bill_number),
                "customer_name": customer["name"],
                "customer_contact": customer["contact"],
                "items": items,
                "bill_amount": bill_amount,
                "discount": discount_percentage,
                "net_amount": net_amount,
                "date": sale_time,
                "amount": net_amount  # For compatibility with existing queries
            }
            
            # Insert the sale into the database
            db_conn.sales.insert_one(sale_doc)
            
            # Generate bill text file
            bill_filename = f"bill_{bill_number}.txt"
            bill_path = os.path.join(bills_dir, bill_filename)
            
            with open(bill_path, 'w') as bill_file:
                bill_file.write("=" * 50 + "\n")
                bill_file.write("           INVENTORY MANAGEMENT SYSTEM\n")
                bill_file.write("                  CUSTOMER BILL\n")
                bill_file.write("=" * 50 + "\n\n")
                
                bill_file.write(f"Bill No: {bill_number}\n")
                bill_file.write(f"Date: {sale_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                bill_file.write(f"Customer Name: {customer['name']}\n")
                bill_file.write(f"Contact: {customer['contact']}\n\n")
                
                bill_file.write("-" * 50 + "\n")
                bill_file.write(f"{'Item':<20}{'Price':<10}{'Qty':<10}{'Total':<10}\n")
                bill_file.write("-" * 50 + "\n")
                
                for item in items:
                    bill_file.write(f"{item['product_name']:<20}{item['price']:<10}{item['quantity']:<10}{item['item_total']:<10}\n")
                
                bill_file.write("-" * 50 + "\n")
                bill_file.write(f"Subtotal: {bill_amount:.2f}\n")
                bill_file.write(f"Discount: {discount_percentage}% ({discount_amount:.2f})\n")
                bill_file.write(f"Net Amount: {net_amount:.2f}\n\n")
                
                bill_file.write("=" * 50 + "\n")
                bill_file.write("                Thank You For Shopping!\n")
                bill_file.write("=" * 50 + "\n")
            
            bill_number += 1
            total_sales_generated += 1
        
        # Move to next day
        current_date += datetime.timedelta(days=1)
        day_count += 1
        
        # Print progress every 10 days
        if day_count % 10 == 0:
            print(f"Generated sales for {day_count} days...")
    
    print(f"Sales data generation complete!")
    print(f"Total sales records generated: {total_sales_generated}")
    print(f"Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print(f"Bill numbers: 6480 to {bill_number - 1}")
    print(f"Bill text files saved in: {bills_dir}")

if __name__ == "__main__":
    generate_sales_data() 