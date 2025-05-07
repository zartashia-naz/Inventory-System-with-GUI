import datetime
import pymongo
from database import MongoDBConnection

def fix_sales_data():
    """
    Fix sales data in MongoDB:
    1. Ensure dates are stored as datetime objects
    2. Ensure the items structure is correct
    3. Print statistics on the sales data
    """
    # Connect to the database
    db = MongoDBConnection()
    
    print("Connected to MongoDB")
    print("Checking sales data format...")
    
    # Count total sales records
    total_sales = db.sales.count_documents({})
    print(f"Total sales records: {total_sales}")
    
    # Check date format
    non_date_records = db.sales.count_documents({"date": {"$not": {"$type": 9}}})  # 9 is the BSON type for date
    if non_date_records > 0:
        print(f"Found {non_date_records} records with incorrect date format. Fixing...")
        cursor = db.sales.find({"date": {"$not": {"$type": 9}}})
        for doc in cursor:
            if isinstance(doc["date"], str):
                try:
                    # Try to parse date if it's a string
                    date_obj = datetime.datetime.strptime(doc["date"], "%Y-%m-%d")
                    db.sales.update_one({"_id": doc["_id"]}, {"$set": {"date": date_obj}})
                except:
                    # If parse fails, set to current date
                    db.sales.update_one({"_id": doc["_id"]}, {"$set": {"date": datetime.datetime.now()}})
    else:
        print("All records have correct date format.")
    
    # Check the items array structure
    records_without_items = db.sales.count_documents({"items": {"$exists": False}})
    if records_without_items > 0:
        print(f"Found {records_without_items} records without items array. Fixing...")
        
        # Get a sample record with correct structure
        sample_with_items = db.sales.find_one({"items": {"$exists": True}})
        
        if sample_with_items:
            # Use structure from a good record
            cursor = db.sales.find({"items": {"$exists": False}})
            for doc in cursor:
                # Create default items array based on product_id, name, etc.
                if "product_id" in doc and "product_name" in doc:
                    items = [{
                        "product_id": doc["product_id"],
                        "product_name": doc["product_name"],
                        "quantity": doc.get("quantity", 1),
                        "price": doc.get("price", 0),
                        "item_total": doc.get("amount", 0)
                    }]
                    
                    # Update record with items array
                    db.sales.update_one({"_id": doc["_id"]}, {"$set": {"items": items}})
        else:
            print("No sample with items structure found. Cannot fix records without items.")
    else:
        print("All records have items array.")
    
    # Get date range statistics for sales data
    earliest_cursor = db.sales.find().sort("date", 1).limit(1)
    latest_cursor = db.sales.find().sort("date", -1).limit(1)
    
    earliest_records = list(earliest_cursor)
    latest_records = list(latest_cursor)
    
    earliest_date = earliest_records[0]["date"] if earliest_records else "none"
    latest_date = latest_records[0]["date"] if latest_records else "none"
    
    print(f"\nSales Data Date Range:")
    print(f"Earliest record: {earliest_date}")
    print(f"Latest record: {latest_date}")
    
    # Count sales by month
    pipeline = [
        {"$group": {
            "_id": {
                "year": {"$year": "$date"},
                "month": {"$month": "$date"}
            },
            "count": {"$sum": 1},
            "total": {"$sum": "$amount"}
        }},
        {"$sort": {"_id.year": 1, "_id.month": 1}}
    ]
    
    monthly_results = list(db.sales.aggregate(pipeline))
    
    print("\nSales by Month:")
    for result in monthly_results:
        year = result["_id"]["year"]
        month = result["_id"]["month"]
        count = result["count"]
        total = result["total"]
        print(f"{year}-{month:02d}: {count} sales, ${total:.2f}")
    
    print("\nSales data check complete.")

if __name__ == "__main__":
    fix_sales_data() 