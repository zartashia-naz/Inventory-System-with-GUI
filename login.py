from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
from database import MongoDBConnection
import os
import sys

class Login:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1045x650+225+160")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")

        self.username_var=StringVar()
        self.password_var=StringVar()
        self.reset_id_var=StringVar()
        self.new_password_var=StringVar()
        self.confirm_password_var=StringVar()
        
        # Initialize database connection
        self.db = MongoDBConnection()

        self.login_img = Image.open("/Users/macbookpro/Desktop/python projects/Inventory-System-with-GUI/assets/20945760.jpg")
        self.login_img = self.login_img.resize((400, 500), Image.Resampling.LANCZOS)
        self.login_img_tk = ImageTk.PhotoImage(self.login_img)
    
        img_lbl=Label(self.root, image=self.login_img_tk, bd=0)
        img_lbl.place(x=90, y=70)

        right_frame=Frame(self.root, bd=2, relief=RIDGE, bg='white')
        right_frame.place(x=500, y=70, height=410, width=400)

        login_lbl=Label(right_frame, text="LOGIN SYSTEM",font=("Times new roman", 35, "bold"), bg="white")
        login_lbl.place(x=0, y=0,relwidth=1)

        username_lbl=Label(right_frame, text="Employee ID", font=("Times new roman", 20, "bold"), bg="white")
        username_lbl.place(x=20, y=70)
        username_entry=Entry(right_frame, textvariable=self.username_var,font=("Times new roman", 20))
        username_entry.place(x=20, y=110,width=350)


        password_lbl=Label(right_frame, text="Password", font=("Times new roman", 20, "bold"), bg="white")
        password_lbl.place(x=20, y=180)
        password_entry=Entry(right_frame, textvariable=self.password_var,font=("Times new roman", 20), show="*")
        password_entry.place(x=20, y=210,width=350)
        

        login_btn=Button(right_frame, text="LOGIN", command=self.login, font=("Times new roman", 20),relief=FLAT,borderwidth=0, bg="#00B0F0",fg="white",activebackground='#00B0F0',activeforeground='white', cursor="hand2")
        login_btn.place(x=20,y=280, width=350 )

        hr_lbl=Label(right_frame, bg="lightgray", font=("Times new roman", 20))
        hr_lbl.place(x=20, y=350,width=350, height=2)

        or_lbl=Label(right_frame, text="OR", font=("Times new roman", 20), fg="light gray", bg="white")
        or_lbl.place(x=170, y=335)

        forget_pass_btn=Button(right_frame,text="Forget Password?",command=self.forget_password_window,font=("Times new roman", 13),relief=FLAT,borderwidth=0,bg="white",activebackground="white",activeforeground='white', fg="blue",cursor="hand2")
        forget_pass_btn.place(x=120,y=370 )

        reg_frame=Frame(self.root, bd=2, relief=RIDGE, bg="white")
        reg_frame.place(x=500, y=490, width=400, height=40)

        reg_lbl=Label(reg_frame, text="Don't have an account?",font=("Times new roman", 18), bg="white")
        reg_lbl.place(x=40, y=5)
        reg_btn=Button(reg_frame, text="SIGN UP", font=("Times new roman", 13),fg="blue")
        reg_btn.place(x=230, y=5)

    def login(self):
        """Verify user login credentials and redirect based on user type"""
        try:
            # Get input values
            employee_id = self.username_var.get().strip()
            password = self.password_var.get().strip()
            
            # Validate inputs
            if not employee_id or not password:
                messagebox.showerror("Error", "Employee ID and Password are required")
                return
            
            # Find employee in database
            # Try string version first
            employee = self.db.employees.find_one({"employee_id": employee_id})
            
            # If not found, try with integer version if it's a number
            if not employee and employee_id.isdigit():
                employee = self.db.employees.find_one({"employee_id": int(employee_id)})
            
            # Check if employee exists and password matches
            if employee and employee.get("password") == password:
                messagebox.showinfo("Success", f"Welcome {employee.get('name', 'User')}")
                
                # Clear login fields
                self.username_var.set("")
                self.password_var.set("")
                
                # Destroy current window 
                self.root.destroy()
                
                # Check user type and redirect to appropriate screen
                user_type = employee.get("user_type", "").lower()
                
                if user_type == "admin":
                    # Launch dashboard
                    self._launch_dashboard()
                elif user_type == "employee":
                    # Launch billing
                    self._launch_billing()
                else:
                    messagebox.showerror("Error", "Invalid user type. Please contact administrator.")
            else:
                messagebox.showerror("Error", "Invalid Employee ID or Password")
                
        except Exception as e:
            messagebox.showerror("Error", f"Login error: {str(e)}")
    
    def forget_password_window(self):
        """Open a window to start password reset process"""
        self.forget_win = Toplevel(self.root)
        self.forget_win.title("Forgot Password")
        self.forget_win.geometry("400x350+550+200")
        self.forget_win.focus_force()
        self.forget_win.grab_set()
        self.forget_win.config(bg="white")
        
        # Heading
        title_lbl = Label(self.forget_win, text="Forgot Password", font=("times new roman", 22, "bold"), bg="white", fg="#00B0F0")
        title_lbl.pack(side=TOP, fill=X, pady=10)
        
        # Employee ID
        id_lbl = Label(self.forget_win, text="Enter Employee ID", font=("times new roman", 15, "bold"), bg="white")
        id_lbl.place(x=20, y=60)
        
        self.reset_id_var.set("")  # Clear any existing value
        id_entry = Entry(self.forget_win, textvariable=self.reset_id_var, font=("times new roman", 15), bg="lightyellow")
        id_entry.place(x=20, y=90, width=350, height=30)
        
        # Submit button
        submit_btn = Button(self.forget_win, text="Submit", command=self.check_employee_exists, font=("times new roman", 15, "bold"), bg="#00B0F0", fg="white", cursor="hand2")
        submit_btn.place(x=20, y=140, width=350, height=35)
        
        # Cancel button
        cancel_btn = Button(self.forget_win, text="Cancel", command=self.forget_win.destroy, font=("times new roman", 15, "bold"), bg="gray", fg="white", cursor="hand2")
        cancel_btn.place(x=20, y=190, width=350, height=35)
    
    def check_employee_exists(self):
        """Check if employee ID exists and has an email associated with it"""
        employee_id = self.reset_id_var.get().strip()
        
        if not employee_id:
            messagebox.showerror("Error", "Please enter your Employee ID", parent=self.forget_win)
            return
        
        # Try string version first
        employee = self.db.employees.find_one({"employee_id": employee_id})
        
        # If not found, try with integer version if it's a number
        if not employee and employee_id.isdigit():
            employee = self.db.employees.find_one({"employee_id": int(employee_id)})
        
        if not employee:
            messagebox.showerror("Error", "Invalid Employee ID", parent=self.forget_win)
            return
        
        # Check if employee has an email
        if not employee.get("email"):
            messagebox.showerror("Error", "No email associated with this Employee ID. Please contact administrator.", parent=self.forget_win)
            return
        
        # Proceed to password reset window
        self.show_reset_password_window(employee)
    
    def show_reset_password_window(self, employee):
        """Show window for entering new password"""
        # Close the previous window
        self.forget_win.destroy()
        
        # Create new window for password reset
        self.reset_win = Toplevel(self.root)
        self.reset_win.title("Reset Password")
        self.reset_win.geometry("400x400+550+200")
        self.reset_win.focus_force()
        self.reset_win.grab_set()
        self.reset_win.config(bg="white")
        
        # Heading
        title_lbl = Label(self.reset_win, text="Reset Password", font=("times new roman", 22, "bold"), bg="white", fg="#00B0F0")
        title_lbl.pack(side=TOP, fill=X, pady=10)
        
        # Employee info
        info_lbl = Label(self.reset_win, text=f"Employee: {employee.get('name', 'Unknown')}", font=("times new roman", 15), bg="white")
        info_lbl.place(x=20, y=50)
        
        email = employee.get('email', '')
        # Mask email for privacy (show only first 3 chars and domain)
        if '@' in email:
            username, domain = email.split('@')
            if len(username) > 3:
                masked_email = username[:3] + '*' * (len(username) - 3) + '@' + domain
            else:
                masked_email = username + '@' + domain
        else:
            masked_email = email
            
        email_lbl = Label(self.reset_win, text=f"Email: {masked_email}", font=("times new roman", 15), bg="white")
        email_lbl.place(x=20, y=80)
        
        # New password
        new_pass_lbl = Label(self.reset_win, text="New Password", font=("times new roman", 15, "bold"), bg="white")
        new_pass_lbl.place(x=20, y=120)
        
        self.new_password_var.set("")  # Clear any existing value
        new_pass_entry = Entry(self.reset_win, textvariable=self.new_password_var, font=("times new roman", 15), bg="lightyellow", show="*")
        new_pass_entry.place(x=20, y=150, width=350, height=30)
        
        # Confirm password
        confirm_pass_lbl = Label(self.reset_win, text="Confirm Password", font=("times new roman", 15, "bold"), bg="white")
        confirm_pass_lbl.place(x=20, y=190)
        
        self.confirm_password_var.set("")  # Clear any existing value
        confirm_pass_entry = Entry(self.reset_win, textvariable=self.confirm_password_var, font=("times new roman", 15), bg="lightyellow", show="*")
        confirm_pass_entry.place(x=20, y=220, width=350, height=30)
        
        # Reset button
        reset_btn = Button(self.reset_win, text="Reset Password", command=lambda: self.update_password(employee), font=("times new roman", 15, "bold"), bg="#00B0F0", fg="white", cursor="hand2")
        reset_btn.place(x=20, y=270, width=350, height=35)
        
        # Cancel button
        cancel_btn = Button(self.reset_win, text="Cancel", command=self.reset_win.destroy, font=("times new roman", 15, "bold"), bg="gray", fg="white", cursor="hand2")
        cancel_btn.place(x=20, y=320, width=350, height=35)
    
    def update_password(self, employee):
        """Update the employee's password in the database"""
        new_password = self.new_password_var.get().strip()
        confirm_password = self.confirm_password_var.get().strip()
        
        # Validate passwords
        if not new_password or not confirm_password:
            messagebox.showerror("Error", "Please enter both password fields", parent=self.reset_win)
            return
        
        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match", parent=self.reset_win)
            return
        
        if len(new_password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters", parent=self.reset_win)
            return
        
        try:
            # Update password in database
            result = self.db.employees.update_one(
                {"_id": employee["_id"]},
                {"$set": {"password": new_password}}
            )
            
            if result.modified_count > 0:
                messagebox.showinfo("Success", "Password reset successfully", parent=self.reset_win)
                self.reset_win.destroy()
            else:
                messagebox.showerror("Error", "Failed to update password", parent=self.reset_win)
                
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {str(e)}", parent=self.reset_win)
    
    def _launch_dashboard(self):
        """Launch the dashboard window for admin users"""
        try:
            import dashboard
            dashboard_root = Tk()
            dashboard_obj = dashboard.IMS(dashboard_root)
            dashboard_root.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open dashboard: {str(e)}")
    
    def _launch_billing(self):
        """Launch the billing window for regular employees"""
        try: 
            import billing
            billing_root=Tk()
            billing_obj=billing.BillingClass(billing_root)
            billing_root.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open employee panel: {str(e)}")
 
   

if __name__=="__main__":
        root = Tk()
        obj = Login(root)
        root.mainloop()


