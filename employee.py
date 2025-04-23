from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkcalendar import DateEntry
from database import MongoDBConnection 
from tkinter import messagebox
from datetime import datetime

class Employee:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1045x650+225+160")
        self.root.title("Inventory Management System")
        
        self.root.config(bg="white")
        self.root.focus_force()
        
        # Get database connection
        self.db = MongoDBConnection()
        
        # Employee Variables
        self.var_emp_id = StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_gender = StringVar()
        self.var_contact = StringVar()
        self.var_pass = StringVar()
        self.var_utype = StringVar()
        self.var_salary = StringVar()
        self.dob = None
        self.doj = None
        self.var_emp_type = StringVar()
        self.var_education = StringVar()
        self.var_work_shift = StringVar()
        self.var_address = StringVar()
        
        # Search Variables
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        
        # Track selected employee for update/delete
        self.selected_emp_id = None

        # Set next employee ID automatically
        self.generate_employee_id()
        
        self.emp_header_label=Label(self.root, text="Manage Employee Details", bg="#9370DB", fg="white", font=("Times New Roman", 30,"bold"), justify=CENTER)
        self.emp_header_label.place(x=0,y=0,relwidth=1)
        global back_image
        self.back_image=Image.open('/Users/macbookpro/Desktop/python projects/Inventory-System-with-GUI/back_btn.png')
        back_image=self.back_image.resize((50,50),Image.Resampling.LANCZOS)
        back_image=ImageTk.PhotoImage(back_image)

        back_button=Button(self.root,image=back_image,bg="white",cursor = 'hand2',command=lambda: self.root.place_forget())
        back_button.place(x=0,y=40)

        top_emp_frame=Frame(self.root)
        top_emp_frame.place(x=0,y=90,relwidth=1,height=250)

        search_frame=Frame(top_emp_frame)
        search_frame.pack()
        search_combobox=ttk.Combobox(search_frame, values=('Id', 'Name','Email'), textvariable=self.var_searchby,font=('times new roman',15),state= 'readonly')
        search_combobox.set('Search By')
        search_combobox.grid(row=0,column=0,padx=10)
        search_combobox.current(0)
        search_entry=Entry(search_frame,font=("Times New Roman", 15),textvariable=self.var_searchtxt,bg="light yellow")
        search_entry.grid(row=0,column=1)

        search_button = Button(search_frame, text='Search', font=('times new roman', 15), command=self.search_employees, width=10, cursor='hand2',
                               bg="#9370DB",fg='white')
        search_button.grid(row=0, column=2, padx=10)
        show_button = Button(search_frame, text='Show All', font=('times new roman', 15), command=self.show_employees,width=10, cursor='hand2',
                              bg="#9370DB",fg='white')
        show_button.grid(row=0, column=3)


        horizontal_scrollbar=Scrollbar(top_emp_frame, orient="horizontal")
        vertcal_scrollbar=Scrollbar(top_emp_frame,orient="vertical")

        self.employee_treeview=ttk.Treeview(top_emp_frame,columns=('empid', 'name','email', 'gender', 'dob', 'contact', 'employment_type','education','work_shift','address', 'doj','salary','usertype'),show="headings", yscrollcommand=vertcal_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
        horizontal_scrollbar.pack(side=BOTTOM, fill=X,pady=5)
        vertcal_scrollbar.pack(side=RIGHT,fill=Y,pady=(10,0))
        horizontal_scrollbar.config(command=self.employee_treeview.xview)
        vertcal_scrollbar.config(command=self.employee_treeview.yview)
        self.employee_treeview.pack() 
        
        # Bind treeview selection event
        self.employee_treeview.bind("<ButtonRelease-1>", self.get_data)

        self.employee_treeview.heading('empid',text='Employment ID')
        self.employee_treeview.heading('name', text='Name')
        self.employee_treeview.heading('email', text='Email')
        self.employee_treeview.heading('gender' ,text='Gender')
        self.employee_treeview.heading('dob', text='Date of birth')
        self.employee_treeview.heading('contact', text='Contact')
        self.employee_treeview.heading('employment_type',text='Employment Type')
        self.employee_treeview.heading('education', text='Education')
        self.employee_treeview.heading('work_shift',text='Work Shift')
        self.employee_treeview.heading('address', text='Address')
        self.employee_treeview.heading('doj', text='Date of Joining')
        self.employee_treeview.heading('salary' ,text='Salary')
        self.employee_treeview.heading('usertype', text='User Type')

        self.employee_treeview.column('empid', width=90)
        self.employee_treeview.column('name', width=140)
        self.employee_treeview.column('email', width=180)
        self.employee_treeview.column('gender', width=80)
        self.employee_treeview.column('contact',width=100)
        self.employee_treeview.column('dob', width=100)
        self.employee_treeview.column('employment_type', width=120)
        self.employee_treeview.column('education', width=120)
        self.employee_treeview.column('work_shift', width=100)
        self.employee_treeview.column('address', width=200)
        self.employee_treeview.column('doj', width=100)
        self.employee_treeview.column('salary', width=140)
        self.employee_treeview.column('usertype', width=120)
        

        employee_details_frame=Frame(self.root)
        employee_details_frame.place(x=0,y=340)

        employee_details_label=Label(employee_details_frame, text= "EmployeeID", font=("Times New Roman", 15))
        employee_details_label.grid(row=0, column=0,padx=10,pady=10)
        # Make employee ID entry readonly since it's auto-generated
        employee_details_entry=Entry(employee_details_frame,textvariable=self.var_emp_id,bg="light grey",state="readonly")
        employee_details_entry.grid(row=0,column=1,padx=10,pady=10)


        employee_details_label=Label(employee_details_frame, text= "Name", font=("Times New Roman", 15))
        employee_details_label.grid(row=0, column=2,padx=10,pady=10)
        employee_details_entry=Entry(employee_details_frame, textvariable=self.var_name,bg="light yellow")
        employee_details_entry.grid(row=0,column=3,padx=10,pady=10)


        employee_details_label=Label(employee_details_frame, text= "Email", font=("Times New Roman", 15))
        employee_details_label.grid(row=0, column=4,padx=10,pady=10)
        employee_details_entry=Entry(employee_details_frame, textvariable=self.var_email,bg="light yellow")
        employee_details_entry.grid(row=0,column=5,padx=10,pady=10)


        employee_details_label=Label(employee_details_frame, text="Gender",font=("Times New Roman", 15))
        employee_details_label.grid(row=1,column=0,padx=10,pady=10)
        employee_details_entry_combo=ttk.Combobox(employee_details_frame, values=("Male","Female"),textvariable=self.var_gender,width=18,state='readonly')
        employee_details_entry_combo.set("Search Gender")
        employee_details_entry_combo.grid(row=1,column=1,padx=10,pady=10)
        
        employee_details_label=Label(employee_details_frame, text="Date of Birth",font=("Times New Roman", 15))
        employee_details_label.grid(row=1,column=2,padx=10,pady=10)
        self.cal_dob=DateEntry(employee_details_frame,width=18,state="readonly",date_pattern="dd/mm/yyyy",mindate=datetime(1900, 1, 1),maxdate=datetime.now())
        self.cal_dob.grid(row=1,column=3,padx=10,pady=10)

        employee_details_label=Label(employee_details_frame, text="Contact",font=("Times New Roman", 15))
        employee_details_label.grid(row=1,column=4,padx=10,pady=10)
        employee_details_entry=Entry(employee_details_frame, textvariable= self.var_contact,bg="light yellow")
        employee_details_entry.grid(row=1,column=5,padx=10,pady=10)

        employee_details_label=Label(employee_details_frame, text="Employment Type",font=("Times New Roman", 15))
        employee_details_label.grid(row=2,column=0, padx=10,pady=10)
        employee_details_entry_combo=ttk.Combobox(employee_details_frame,textvariable=self.var_emp_type, values=('Full time','Part time', 'Intern','Contract'),font=("Times New Roman",15),width=18,state='readonly')
        employee_details_entry_combo.set("Select Employment type")
        employee_details_entry_combo.grid(row=2,column=1,padx=10,pady=10)
        employee_details_entry_combo.current(0)

        employee_details_label=Label(employee_details_frame, text="Education",font=("Times New Roman", 15))
        employee_details_label.grid(row=2,column=2, padx=10,pady=10)
        employee_details_entry_combo=ttk.Combobox(employee_details_frame,textvariable=self.var_education, values=('FSc','ICOM','ICS','LLB','B.COM','M.Tech','MBA','B.Sc','BBA','LLM','B.ARC','M.Arc'),font=("Times New Roman",15),width=18,state='readonly')
        employee_details_entry_combo.set("Select Education")
        employee_details_entry_combo.grid(row=2,column=3,padx=10,pady=10)

        employee_details_label=Label(employee_details_frame, text="Working Shift",font=("Times New Roman", 15))
        employee_details_label.grid(row=2,column=4,padx=10,pady=10)
        employee_details_entry_combo=ttk.Combobox(employee_details_frame,textvariable=self.var_work_shift, values=("Morning","Evening","Night"),font=("Times New Roman",15),width=18,state='readonly')
        employee_details_entry_combo.set("Search Shift")
        employee_details_entry_combo.grid(row=2,column=5,padx=10,pady=10)

        employee_details_label=Label(employee_details_frame, text="Address",font=("Times New Roman", 15))
        employee_details_label.grid(row=3,column=0,padx=10,pady=10, sticky="w")
        self.emp_detail_address_Txt=Text(employee_details_frame,width=18, height=4,font=("Times New Roman", 15),wrap=WORD, bg="Light yellow")
        self.emp_detail_address_Txt.grid(row=3, column=1,padx=10, pady=10,rowspan=2)


        employee_details_label=Label(employee_details_frame, text="Date of Joining",font=("Times New Roman", 15))
        employee_details_label.grid(row=3,column=2,padx=10,pady=10)
        self.cal_doj=DateEntry(employee_details_frame,width=18, font=("Times New Roman", 15),state="readonly",date_pattern="dd/mm/yyyy",mindate=datetime(1900, 1, 1),
            maxdate=datetime.now())
        self.cal_doj.grid(row=3,column=3,padx=10,pady=10)

        employee_details_label=Label(employee_details_frame, text="User Type",font=("Times New Roman", 15))
        employee_details_label.grid(row=4,column=2,padx=10,pady=10)
        employee_details_entry_combo=ttk.Combobox(employee_details_frame, values=("Admin","Employee"),textvariable=self.var_utype,font=("Times New Roman",15),width=18,state='readonly')
        employee_details_entry_combo.set("Search User Type")
        employee_details_entry_combo.grid(row=4,column=3,padx=10,pady=10)

        employee_details_label=Label(employee_details_frame, text="Salary",font=("Times New Roman", 15))
        employee_details_label.grid(row=3,column=4,padx=10,pady=10)
        employee_details_entry=Entry(employee_details_frame, textvariable=self.var_salary,bg="light yellow")
        employee_details_entry.grid(row=3,column=5,padx=10,pady=10)

        employee_details_label=Label(employee_details_frame, text="Password",font=("Times New Roman", 15))
        employee_details_label.grid(row=4,column=4,padx=10,pady=10)
        employee_details_entry=Entry(employee_details_frame, textvariable=self.var_pass,bg="light yellow")
        employee_details_entry.grid(row=4,column=5,padx=10,pady=10)

        add_button=Button(self.root,text="ADD",font=("Times New Roman", 15),command=self.add_employee,bg="purple",activebackground="purple",fg="white",activeforeground="white",cursor = 'hand2',width=10,)
        add_button.place(x=200,y=600)
        
    
        update_button=Button(self.root,text="UPDATE",font=("Times New Roman", 15),command=self.update_employee,bg="purple",activebackground= "#7B68EE",fg="white",cursor = 'hand2',width=10)
        update_button.place(x=350,y=600)

        delete_button=Button(self.root,text="DELETE",font=("Times New Roman", 15),command=self.delete_employee,bg="purple",activebackground= "#7B68EE",fg="white",cursor = 'hand2',width=10)
        delete_button.place(x=500,y=600)

        clear_button=Button(self.root,text="CLEAR",font=("Times New Roman", 15),command=self.clear_fields,bg="purple",activebackground= "#7B68EE",fg="white",cursor = 'hand2',width=10)
        clear_button.place(x=650,y=600)
        
        # Load employees when window opens
        self.show_employees()

    def get_data(self, event):
        """Get data from selected row in treeview and populate form fields"""
        try:
            # Get the selected item from treeview
            selected_row = self.employee_treeview.focus()
            contents = self.employee_treeview.item(selected_row)
            row = contents['values']
            
            if not row:
                return
            
            # Debug: Print the row values to see what we're getting
            print(f"Selected row data: {row}")
            
            # Clear fields before populating with new data
            self.clear_fields()
            
            # Store employee_id for update/delete operations
            self.selected_emp_id = str(row[0])  # Convert to string to ensure consistent type
            print(f"Stored employee ID: {self.selected_emp_id}")
            
            # Set values to fields
            self.var_emp_id.set(row[0])
            self.var_name.set(row[1])
            self.var_email.set(row[2])
            self.var_gender.set(row[3] if row[3] else "Select")
            
            # Set DOB if present
            if row[4]:
                try:
                    dob_date = datetime.strptime(row[4], "%Y-%m-%d").date()
                    self.cal_dob.set_date(dob_date)
                except Exception as e:
                    print(f"Error setting DOB: {str(e)}")
                    
            self.var_contact.set(row[5] if row[5] else "")
            self.var_emp_type.set(row[6] if row[6] else "Select Employment type")
            self.var_education.set(row[7] if row[7] else "Select Education")
            self.var_work_shift.set(row[8] if row[8] else "Search Shift")
            
            # Set address
            if row[9]:
                self.emp_detail_address_Txt.delete(1.0, END)
                self.emp_detail_address_Txt.insert(END, row[9])
                self.var_address.set(row[9])
            
            # Set DOJ if present
            if row[10]:
                try:
                    doj_date = datetime.strptime(row[10], "%Y-%m-%d").date()
                    self.cal_doj.set_date(doj_date)
                except Exception as e:
                    print(f"Error setting DOJ: {str(e)}")
                    
            self.var_salary.set(row[11] if row[11] else "")
            self.var_utype.set(row[12] if row[12] else "Select")
            
        except Exception as e:
            print(f"Error in get_data: {str(e)}")
            messagebox.showerror("Error", f"Error loading data: {str(e)}")

    def generate_employee_id(self):
        """Generate a new auto-incremented employee ID"""
        try:
            # Get the highest employee ID from the database
            highest_id = 0
            
            # Find the highest numeric employee ID
            employees = self.db.employees.find({}, {"employee_id": 1})
            for emp in employees:
                emp_id = emp.get('employee_id', '0')
                # Convert to integer if possible
                try:
                    if isinstance(emp_id, str) and emp_id.isdigit():
                        emp_id = int(emp_id)
                    elif isinstance(emp_id, int):
                        pass
                    else:
                        continue
                        
                    if emp_id > highest_id:
                        highest_id = emp_id
                except:
                    continue
            
            # Generate next ID (highest + 1)
            next_id = highest_id + 1
            
            # Format with leading zeros (EMP001, EMP002, etc.)
            next_id_str = f"{next_id:03d}"
            
            # Set the employee ID
            self.var_emp_id.set(next_id_str)
            print(f"Generated new employee ID: {next_id_str}")
            
        except Exception as e:
            print(f"Error generating employee ID: {str(e)}")
            # Fallback to a timestamp-based ID if database query fails
            import time
            fallback_id = f"{int(time.time())}"[-4:]
            self.var_emp_id.set(fallback_id)

    def add_employee(self):
        """Add a new employee to the database"""
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Employee Name is required")
                return
                
            # Employee ID is now auto-generated, no need to check if it's empty
                
            # Convert date objects to datetime objects for MongoDB storage
            dob_date = self.cal_dob.get_date()
            doj_date = self.cal_doj.get_date()
            
            # Convert date to string for MongoDB storage
            dob_string = dob_date.strftime("%Y-%m-%d")
            doj_string = doj_date.strftime("%Y-%m-%d")
            
            # Get address from Text widget
            address = self.emp_detail_address_Txt.get(1.0, END).strip()
            
            # Store employee_id consistently as string
            emp_id = str(self.var_emp_id.get()).strip()
                
            employee_data = {
                "employee_id": emp_id,
                "name": self.var_name.get(),
                "email": self.var_email.get(),
                "gender": self.var_gender.get(),
                "contact": self.var_contact.get(),
                "dob": dob_string,
                "doj": doj_string,
                "password": self.var_pass.get(),
                "user_type": self.var_utype.get(),
                "salary": self.var_salary.get(),
                "created_at": datetime.now(),
                "employment_type": self.var_emp_type.get(),
                "education": self.var_education.get(),
                "work_shift": self.var_work_shift.get(),
                "address": address
            }
            
            # Check if employee ID already exists (try both string and int versions)
            existing = self.db.employees.find_one({"employee_id": emp_id})
            if not existing and emp_id.isdigit():
                existing = self.db.employees.find_one({"employee_id": int(emp_id)})
                
            if existing:
                messagebox.showerror("Error", f"Employee ID {emp_id} already exists!")
                # Generate a new ID since this one is taken
                self.generate_employee_id()
                return
            
            # Insert into MongoDB
            result = self.db.employees.insert_one(employee_data)
            
            if result.inserted_id:
                messagebox.showinfo("Success", "Employee added successfully")
                self.clear_fields()
                self.show_employees()  # Refresh the employee list
            else:
                messagebox.showerror("Error", "Failed to add employee")
                
        except Exception as e:
            print(f"Add employee error details: {str(e)}")
            messagebox.showerror("Error", f"Failed to add employee: {str(e)}")

    def update_employee(self):
        """Update an existing employee in the database"""
        try:
            if not self.selected_emp_id:
                messagebox.showerror("Error", "Please select an employee to update")
                return
                
            # Debug: Print the selected employee ID
            print(f"Attempting to update employee with ID: {self.selected_emp_id}")
            print(f"Type of selected_emp_id: {type(self.selected_emp_id)}")
                
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Employee Name is required")
                return
                
            # Ask for confirmation
            confirm = messagebox.askyesno("Confirm", "Are you sure you want to update this employee?")
            if not confirm:
                return
            
            # First check if employee exists in database
            employee = self.db.employees.find_one({"employee_id": self.selected_emp_id})
            if not employee:
                # Try with int if the ID looks like a number
                try:
                    if self.selected_emp_id.isdigit():
                        employee = self.db.employees.find_one({"employee_id": int(self.selected_emp_id)})
                except:
                    pass
                    
            if not employee:
                messagebox.showerror("Error", f"Employee with ID {self.selected_emp_id} not found in database")
                print("No employee found with query:", {"employee_id": self.selected_emp_id})
                
                # List all employees in the database for debugging
                print("Listing all employee IDs in database:")
                all_employees = list(self.db.employees.find({}, {"employee_id": 1}))
                for emp in all_employees:
                    print(f"DB employee ID: {emp.get('employee_id')} (type: {type(emp.get('employee_id'))})")
                return
                
            # Convert date objects to string for MongoDB storage
            dob_date = self.cal_dob.get_date()
            doj_date = self.cal_doj.get_date()
            
            # Convert date to string
            dob_string = dob_date.strftime("%Y-%m-%d")
            doj_string = doj_date.strftime("%Y-%m-%d")
            
            # Get address from Text widget
            address = self.emp_detail_address_Txt.get(1.0, END).strip()
                
            # Prepare update data
            update_data = {
                "$set": {
                    "name": self.var_name.get(),
                    "email": self.var_email.get(),
                    "gender": self.var_gender.get(),
                    "contact": self.var_contact.get(),
                    "dob": dob_string,
                    "doj": doj_string,
                    "password": self.var_pass.get(),
                    "user_type": self.var_utype.get(),
                    "salary": self.var_salary.get(),
                    "updated_at": datetime.now(),
                    "employment_type": self.var_emp_type.get(),
                    "education": self.var_education.get(),
                    "work_shift": self.var_work_shift.get(),
                    "address": address
                }
            }
            
            # Try to update with string ID
            result = self.db.employees.update_one({"employee_id": self.selected_emp_id}, update_data)
            
            # If update failed, try with integer ID if it looks like a number
            if result.matched_count == 0 and self.selected_emp_id.isdigit():
                result = self.db.employees.update_one({"employee_id": int(self.selected_emp_id)}, update_data)
            
            # Check for success - use matched_count instead of modified_count
            if result.matched_count > 0:
                messagebox.showinfo("Success", "Employee updated successfully")
                self.clear_fields()
                self.show_employees()  # Refresh the employee list
            else:
                # More detailed error message
                messagebox.showerror("Error", f"Failed to update employee. ID: {self.selected_emp_id}")
                
        except Exception as e:
            # Show the full error details for debugging
            print(f"Update error details: {str(e)}")
            messagebox.showerror("Error", f"Failed to update employee: {str(e)}")
            
    def delete_employee(self):
        """Delete an employee from the database"""
        try:
            if not self.selected_emp_id:
                messagebox.showerror("Error", "Please select an employee to delete")
                return
                
            # Debug: Print the selected employee ID to verify it's what we expect
            print(f"Attempting to delete employee with ID: {self.selected_emp_id}")
            print(f"Type of selected_emp_id: {type(self.selected_emp_id)}")
                
            # Ask for confirmation
            confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete employee {self.var_name.get()}?")
            if not confirm:
                return
            
            # First check if employee exists in database
            # Try both string and integer comparison to handle potential type differences
            employee = self.db.employees.find_one({"employee_id": self.selected_emp_id})
            if not employee:
                # Try with int if the ID looks like a number
                try:
                    if self.selected_emp_id.isdigit():
                        employee = self.db.employees.find_one({"employee_id": int(self.selected_emp_id)})
                except:
                    pass
                    
            if not employee:
                messagebox.showerror("Error", f"Employee with ID {self.selected_emp_id} not found in database")
                print("No employee found with query:", {"employee_id": self.selected_emp_id})
                
                # List all employees in the database for debugging
                print("Listing all employee IDs in database:")
                all_employees = list(self.db.employees.find({}, {"employee_id": 1}))
                for emp in all_employees:
                    print(f"DB employee ID: {emp.get('employee_id')} (type: {type(emp.get('employee_id'))})")
                return
                
            # Delete from MongoDB - try with both string and int variations if needed
            result = self.db.employees.delete_one({"employee_id": self.selected_emp_id})
            
            # If deletion failed, try with integer ID if it looks like a number
            if result.deleted_count == 0 and self.selected_emp_id.isdigit():
                result = self.db.employees.delete_one({"employee_id": int(self.selected_emp_id)})
            
            if result.deleted_count > 0:
                messagebox.showinfo("Success", "Employee deleted successfully")
                self.clear_fields()
                self.show_employees()  # Refresh the employee list
            else:
                # More detailed error message
                messagebox.showerror("Error", f"Failed to delete employee. ID: {self.selected_emp_id}")
                
        except Exception as e:
            # Show the full error details for debugging
            print(f"Delete error details: {str(e)}")
            messagebox.showerror("Error", f"Failed to delete employee: {str(e)}")

    def search_employees(self):
        """Search for employees based on selected criteria"""
        try:
            search_by = self.var_searchby.get()
            search_text = self.var_searchtxt.get()
            
            if not search_by or search_by == "Search By" or not search_text:
                messagebox.showerror("Error", "Please select search criteria and enter search text")
                return
                
            # Map search_by to actual field name in database
            field_map = {
                "Id": "employee_id",
                "Name": "name",
                "Email": "email"
            }
            
            field_name = field_map.get(search_by)
            if not field_name:
                messagebox.showerror("Error", "Invalid search criteria")
                return
                
            # Clear existing data in treeview
            for item in self.employee_treeview.get_children():
                self.employee_treeview.delete(item)
            
            # Create query for case-insensitive search
            query = {field_name: {"$regex": search_text, "$options": "i"}}
            
            # Fetch matching employees from MongoDB
            employees = self.db.employees.find(query).sort("name", 1)
            count = 0
            
            for employee in employees:
                self.employee_treeview.insert('', 'end', values=(
                    employee.get('employee_id', ''),
                    employee.get('name', ''),
                    employee.get('email', ''),
                    employee.get('gender', ''),
                    employee.get('dob', ''),
                    employee.get('contact', ''),
                    employee.get('employment_type', ''),
                    employee.get('education', ''),
                    employee.get('work_shift', ''),
                    employee.get('address', ''),
                    employee.get('doj', ''),
                    employee.get('salary', ''),
                    employee.get('user_type', '')
                ))
                count += 1
                
            if count == 0:
                messagebox.showinfo("Info", "No matching employees found")
                
        except Exception as e:
            messagebox.showerror("Error", f"Search error: {str(e)}")

    def show_employees(self):
        """Display all employees in the treeview"""
        try:
            # Clear existing data in treeview
            for item in self.employee_treeview.get_children():
                self.employee_treeview.delete(item)
            
            # Fetch all employees from MongoDB
            employees = self.db.employees.find().sort("name", 1)
            count = 0
            
            for employee in employees:
                try:
                    # Ensure employee_id is consistently a string
                    emp_id = str(employee.get('employee_id', ''))
                    
                    self.employee_treeview.insert('', 'end', values=(
                        emp_id,
                        employee.get('name', ''),
                        employee.get('email', ''),
                        employee.get('gender', ''),
                        employee.get('dob', ''),
                        employee.get('contact', ''),
                        employee.get('employment_type', ''),
                        employee.get('education', ''),
                        employee.get('work_shift', ''),
                        employee.get('address', ''),
                        employee.get('doj', ''),
                        employee.get('salary', ''),
                        employee.get('user_type', '')
                    ))
                    count += 1
                except Exception as row_error:
                    print(f"Error adding row to treeview: {str(row_error)}")
                    print(f"Problematic employee data: {employee}")
                
            print(f"Loaded {count} employees into treeview")
                
        except Exception as e:
            print(f"Show employees error details: {str(e)}")
            messagebox.showerror("Error", f"Failed to load employees: {str(e)}")

    def clear_fields(self):
        """Clear all form fields"""
        # Don't clear employee ID, regenerate it
        self.generate_employee_id()
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.cal_dob.set_date(datetime.now())  # Reset to today or another default
        self.cal_doj.set_date(datetime.now())
        self.var_pass.set("")
        self.var_utype.set("Select")
        self.var_salary.set("")
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
        self.var_emp_type.set("Select")
        self.var_education.set("Select")
        self.var_work_shift.set("Select")
        self.var_address.set("")
        self.emp_detail_address_Txt.delete(1.0, END)
        self.selected_emp_id = None

if __name__=="__main__":
        root = Tk()
        obj = Employee(root)
        root.mainloop() 