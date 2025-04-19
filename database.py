import pyodbc
from datetime import datetime

class Database:
    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.connection = None
        self.cursor = None
        
    def connect(self):
        try:
            self.connection = pyodbc.connect(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                f"UID={self.username};"
                f"PWD={self.password}"
            )
            self.cursor = self.connection.cursor()
            print("Connected to SQL Server successfully")
        except pyodbc.Error as e:
            print(f"Error connecting to SQL Server: {e}")
            raise
    
    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection closed")
    
    # Employee CRUD Operations
    def add_employee(self, emp_data):
        try:
            query = """
            INSERT INTO Employees (
                empid, name, email, gender, dob, contact, employment_type, 
                education, work_shift, address, doj, salary, usertype, password
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            # Convert string dates to datetime objects
            dob = datetime.strptime(emp_data['dob'], "%d/%m/%Y").date()
            doj = datetime.strptime(emp_data['doj'], "%d/%m/%Y").date()
            
            params = (
                emp_data['empid'], emp_data['name'], emp_data['email'], 
                emp_data['gender'], dob, emp_data['contact'], 
                emp_data['employment_type'], emp_data['education'], 
                emp_data['work_shift'], emp_data['address'], doj, 
                emp_data['salary'], emp_data['usertype'], emp_data['password']
            )
            
            self.cursor.execute(query, params)
            self.connection.commit()
            return True
        except pyodbc.Error as e:
            print(f"Error adding employee: {e}")
            self.connection.rollback()
            return False
    
    def get_all_employees(self):
        try:
            query = """
            SELECT 
                empid, name, email, gender, 
                CONVERT(varchar, dob, 103) as dob, 
                contact, employment_type, education, 
                work_shift, address, 
                CONVERT(varchar, doj, 103) as doj, 
                salary, usertype
            FROM Employees
            """
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Error fetching employees: {e}")
            return []
    
    def get_employee_by_id(self, empid):
        try:
            query = """
            SELECT 
                empid, name, email, gender, 
                CONVERT(varchar, dob, 103) as dob, 
                contact, employment_type, education, 
                work_shift, address, 
                CONVERT(varchar, doj, 103) as doj, 
                salary, usertype
            FROM Employees 
            WHERE empid = ?
            """
            self.cursor.execute(query, empid)
            return self.cursor.fetchone()
        except pyodbc.Error as e:
            print(f"Error fetching employee: {e}")
            return None
    
    def update_employee(self, empid, emp_data):
        try:
            query = """
            UPDATE Employees SET 
                name = ?, email = ?, gender = ?, dob = ?, 
                contact = ?, employment_type = ?, education = ?, 
                work_shift = ?, address = ?, doj = ?, 
                salary = ?, usertype = ?, password = ?
            WHERE empid = ?
            """
            
            # Convert string dates to datetime objects
            dob = datetime.strptime(emp_data['dob'], "%d/%m/%Y").date()
            doj = datetime.strptime(emp_data['doj'], "%d/%m/%Y").date()
            
            params = (
                emp_data['name'], emp_data['email'], emp_data['gender'], dob,
                emp_data['contact'], emp_data['employment_type'], 
                emp_data['education'], emp_data['work_shift'], 
                emp_data['address'], doj, emp_data['salary'], 
                emp_data['usertype'], emp_data['password'], empid
            )
            
            self.cursor.execute(query, params)
            self.connection.commit()
            return True
        except pyodbc.Error as e:
            print(f"Error updating employee: {e}")
            self.connection.rollback()
            return False
    
    def delete_employee(self, empid):
        try:
            query = "DELETE FROM Employees WHERE empid = ?"
            self.cursor.execute(query, empid)
            self.connection.commit()
            return True
        except pyodbc.Error as e:
            print(f"Error deleting employee: {e}")
            self.connection.rollback()
            return False
    
    def search_employees(self, search_by, search_value):
        try:
            if search_by == "Id":
                query = """
                SELECT 
                    empid, name, email, gender, 
                    CONVERT(varchar, dob, 103) as dob, 
                    contact, employment_type, education, 
                    work_shift, address, 
                    CONVERT(varchar, doj, 103) as doj, 
                    salary, usertype
                FROM Employees 
                WHERE empid = ?
                """
                self.cursor.execute(query, search_value)
            elif search_by == "Name":
                query = """
                SELECT 
                    empid, name, email, gender, 
                    CONVERT(varchar, dob, 103) as dob, 
                    contact, employment_type, education, 
                    work_shift, address, 
                    CONVERT(varchar, doj, 103) as doj, 
                    salary, usertype
                FROM Employees 
                WHERE name LIKE ?
                """
                self.cursor.execute(query, f"%{search_value}%")
            elif search_by == "Email":
                query = """
                SELECT 
                    empid, name, email, gender, 
                    CONVERT(varchar, dob, 103) as dob, 
                    contact, employment_type, education, 
                    work_shift, address, 
                    CONVERT(varchar, doj, 103) as doj, 
                    salary, usertype
                FROM Employees 
                WHERE email LIKE ?
                """
                self.cursor.execute(query, f"%{search_value}%")
            
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Error searching employees: {e}")
            return []
    
    # Dashboard statistics
    def get_employee_count(self):
        try:
            query = "SELECT COUNT(*) FROM Employees"
            self.cursor.execute(query)
            return self.cursor.fetchone()[0]
        except pyodbc.Error as e:
            print(f"Error getting employee count: {e}")
            return 0
    
    def get_supplier_count(self):
        try:
            query = "SELECT COUNT(*) FROM Suppliers"
            self.cursor.execute(query)
            return self.cursor.fetchone()[0]
        except pyodbc.Error as e:
            print(f"Error getting supplier count: {e}")
            return 0
    
    def get_category_count(self):
        try:
            query = "SELECT COUNT(*) FROM Categories"
            self.cursor.execute(query)
            return self.cursor.fetchone()[0]
        except pyodbc.Error as e:
            print(f"Error getting category count: {e}")
            return 0
    
    def get_product_count(self):
        try:
            query = "SELECT COUNT(*) FROM Products"
            self.cursor.execute(query)
            return self.cursor.fetchone()[0]
        except pyodbc.Error as e:
            print(f"Error getting product count: {e}")
            return 0
    
    def get_total_sales(self):
        try:
            query = "SELECT SUM(total_amount) FROM Sales"
            self.cursor.execute(query)
            result = self.cursor.fetchone()[0]
            return result if result is not None else 0
        except pyodbc.Error as e:
            print(f"Error getting total sales: {e}")
            return 0