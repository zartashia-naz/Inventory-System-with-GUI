from tkinter import *
from PIL import Image, ImageTk
from employee import Employee
from supplier import Supplier
from category import Category
class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1270x800+0+0")
        self.root.title("Inventory Management System")

        # Store all images as instance variables to prevent garbage collection
        self.logo = PhotoImage(file="/Users/macbookpro/Desktop/python projects/Inventory-System-with-GUI/img logo2.png")
        lableTitle = Label(self.root, text="INVENTORY MANAGEMENT SYSTEM", image=self.logo, compound=LEFT, padx=10,
                         font=("Arial", 40, "bold"), bg="purple", fg="white", anchor="w")
        lableTitle.place(x=0, y=0, relwidth=1, height=70)

        logout_btn = Button(self.root, text="LOGOUT", font=("Arial", 15), bg="light yellow", fg="black", cursor="hand2")
        logout_btn.place(x=1150, y=20, height=25)  # Adjusted x position

        lbl_header = Label(self.root, text="Welcome to Inventory Management System",
                          font=("Arial", 25), bg="light gray", fg="white", justify=CENTER)
        lbl_header.place(x=0, y=70, relwidth=1, height=40)

        # Left Menu
        self.Menuimg = Image.open("/Users/macbookpro/Desktop/python projects/Inventory-System-with-GUI/IMS img.jpeg")
        self.Menuimg = self.Menuimg.resize((200, 200), Image.Resampling.LANCZOS)
        self.Menuimg = ImageTk.PhotoImage(self.Menuimg)

        left_menu = Frame(self.root, bd=3, relief=GROOVE)
        left_menu.place(x=0, y=110, height=550, width=225)

        lable_MenuLogo = Label(left_menu, image=self.Menuimg)
        lable_MenuLogo.pack(side=TOP, fill=X)

        lbl_menu = Label(left_menu, text="Menu", font=("times new roman", 20), bg="#009688")
        lbl_menu.pack(side=TOP, fill=X)
        
        btn_emp = Button(left_menu, text="Employee",command=self.employee, bd=4, padx=5, bg="#009688", cursor="hand2", 
                        font=("Times New Roman", 20, "bold"))
        btn_emp.pack(side=TOP, fill=X)
        
        btn_Supplier = Button(left_menu, text="Supplier", command=self.supplier, bd=4, padx=5, bg="#009688", cursor="hand2", 
                             font=("Times New Roman", 20, "bold"))
        btn_Supplier.pack(side=TOP, fill=X)
        
        btn_Category = Button(left_menu, text="Category",command=self.category, bd=4, padx=5, bg="#009688", cursor="hand2", 
                             font=("Times New Roman", 20, "bold"))
        btn_Category.pack(side=TOP, fill=X)

        btn_products= Button(left_menu, text="Products", bd=4, padx=5, bg="#009688", cursor="hand2", 
                             font=("Times New Roman", 20, "bold"))
        btn_products.pack(side=TOP, fill=X)
        
        btn_Sales = Button(left_menu, text="Sales", bd=4, padx=5, bg="#009688", cursor="hand2", 
                          font=("Times New Roman", 20, "bold"))
        btn_Sales.pack(side=TOP, fill=X)
        
        btn_Exit = Button(left_menu, text="Exit", bd=4, padx=5, bg="#009688", cursor="hand2", 
                         font=("Times New Roman", 20, "bold"))
        btn_Exit.pack(side=TOP, fill=X)

        # Employee Frame with Image
        emp_frame = Frame(root, bg='#2C3E50', bd=3, relief=RIDGE)
        emp_frame.place(x=400, y=125, height=170, width=280)
        
        try:
            # Use absolute path for the employee image
            emp_img_path = "/Users/macbookpro/Desktop/python projects/Inventory-System-with-GUI/employee.png"
            self.total_emp_icon = Image.open(emp_img_path)
            self.total_emp_icon = self.total_emp_icon.resize((80, 80), Image.Resampling.LANCZOS)  # Resize appropriately
            self.total_emp_icon = ImageTk.PhotoImage(self.total_emp_icon)
            
            total_emp_icon_label = Label(emp_frame, image=self.total_emp_icon, bg='#2C3E50')
            total_emp_icon_label.pack(pady=5)
            
            total_emp_label = Label(emp_frame, text='Total Employees', bg='#2C3E50', fg='white',
                                  font=('Times New Roman', 15, "bold"))
            total_emp_label.pack()
            
            total_emp_count_label = Label(emp_frame, text='0', bg='#2C3E50', fg='white',
                                        font=("Times New Roman", 30, "bold"))
            total_emp_count_label.pack()
        except Exception as e:
            print(f"Error loading employee image: {e}")
            Label(emp_frame, text="Image not found", bg='#2C3E50', fg='white').pack()


        supplier_frame = Frame(root, bg='#2C3E50', bd=3, relief=RIDGE)
        supplier_frame.place(x=800, y=125, height=170, width=280)

        supplier_img_path = "/Users/macbookpro/Desktop/python projects/Inventory-System-with-GUI/supplier.png"
        self.supplier_icon = Image.open(supplier_img_path)
        self.supplier_icon = self.supplier_icon.resize((80, 80), Image.Resampling.LANCZOS)  # Resize appropriately
        self.supplier_icon = ImageTk.PhotoImage(self.supplier_icon)
            
        supplier_icon_label = Label(supplier_frame, image=self.supplier_icon, bg='#2C3E50')
        supplier_icon_label.pack(pady=5)
            
        supplier_label = Label(supplier_frame, text='Total Suppliers', bg='#2C3E50', fg='white',
                                  font=('Times New Roman', 15, "bold"))
        supplier_label.pack()
            
        supplier_count_label = Label(supplier_frame, text='0', bg='#2C3E50', fg='white',
                                        font=("Times New Roman", 30, "bold"))
        supplier_count_label.pack()



        cat_frame = Frame(root, bg='#2C3E50', bd=3, relief=RIDGE)
        cat_frame.place(x=400, y=330, height=170, width=280)

        cat_img_path = "/Users/macbookpro/Desktop/python projects/Inventory-System-with-GUI/category.png"
        self.cat_icon = Image.open(cat_img_path)
        self.cat_icon = self.cat_icon.resize((80, 80), Image.Resampling.LANCZOS)  # Resize appropriately
        self.cat_icon = ImageTk.PhotoImage(self.cat_icon)
            
        cat_icon_label = Label(cat_frame, image=self.cat_icon, bg='#2C3E50')
        cat_icon_label.pack(pady=5)
            
        cat_label = Label(cat_frame, text='Total Categories', bg='#2C3E50', fg='white',
                                  font=('Times New Roman', 15, "bold"))
        cat_label.pack()
            
        cat_count_label = Label(cat_frame, text='0', bg='#2C3E50', fg='white',
                                        font=("Times New Roman", 30, "bold"))
        cat_count_label.pack()


        product_frame=Frame(root, bg="#2C3E50", bd=3, relief=RIDGE)
        product_frame.place(x=800, y=330, height=170, width=280)

        product_image_path="/Users/macbookpro/Desktop/python projects/Inventory-System-with-GUI/image.png"
        self.product_icon=Image.open(product_image_path)
        self.product_icon=self.product_icon.resize((80,80), Image.Resampling.LANCZOS)
        self.product_icon=ImageTk.PhotoImage(self.product_icon)

        self.product_icon_label=Label(product_frame, image=self.product_icon, bg='#2C3E50')
        self.product_icon_label.pack(pady=5)

        self.product_lable=Label(product_frame, text="Total Products", bg='#2C3E50', fg="white", font=("Times New Roman",15, "bold"))
        self.product_lable.pack()


        self.product_count_lable=Label(product_frame, text="0", bg='#2C3E50', fg="white", font=("Times New Roman",30, "bold"))
        self.product_count_lable.pack()


        sales_icon=Frame(root, bg="#2C3E50", bd=3, relief=RIDGE)
        sales_icon.place(x=600, y=535, height=170, width=280)

        sales_image_path="/Users/macbookpro/Desktop/python projects/Inventory-System-with-GUI/sales.png"
        self.sales_icon=Image.open(sales_image_path)
        self.sales_icon=self.sales_icon.resize((80,80), Image.Resampling.LANCZOS)
        self.sales_icon=ImageTk.PhotoImage(self.sales_icon)

        self.sales_icon_label=Label(sales_icon, image=self.sales_icon, bg='#2C3E50')
        self.sales_icon_label.pack(pady=5)

        self.sales_lable=Label(sales_icon, text="Total Sales", bg='#2C3E50', fg="white", font=("Times New Roman",15, "bold"))
        self.sales_lable.pack()


        self.total_sales_lable=Label(sales_icon, text="0", bg='#2C3E50', fg="white", font=("Times New Roman",30, "bold"))
        self.total_sales_lable.pack()


        lb1_footer = Label(self.root, text="Inventory Management System\nFor Any queries contact",
                                font=("Arial", 25), bg="light gray", fg="white", justify=CENTER)
        lb1_footer.pack(side=BOTTOM, fill=X)


    def employee(self):
         self.emp_window=Toplevel(self.root)
         self.emp_obj=Employee(self.emp_window)

    def supplier(self):
         self.sup_window=Toplevel(self.root)
         self.sup_obj=Supplier(self.sup_window)

    def category(self):
        self.cat_window=Toplevel(self.root)
        self.cat_obj=Category(self.cat_window)

if __name__=="__main__":
        root = Tk()
        obj = IMS(root)
        root.mainloop()