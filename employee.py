from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkcalendar import DateEntry
class Employee:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1045x650+225+160")
        self.root.title("Inventory Management System")
        

        
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

        search_frame=Frame (top_emp_frame)
        search_frame.pack()
        search_combobox=ttk.Combobox(search_frame, values=('Id', 'Name','Email'), font=('times new roman',15),state= 'readonly')
        search_combobox.set('Search By')
        search_combobox.grid(row=0,column=0,padx=10)
        search_entry=Entry(search_frame,font=("Times New Roman", 15),bg="light yellow")
        search_entry.grid(row=0,column=1)

        search_button = Button(search_frame, text='Search', font=('times new roman', 15), width=10, cursor='hand2',
                               bg="#9370DB",fg='white')
        search_button.grid(row=0, column=2, padx=10)
        show_button = Button (search_frame, text='Show All', font=('times new roman', 15), width=10, cursor='hand2',
                              bg="#9370DB",fg='white')
        show_button.grid(row=0, column=3)


        horizontal_scrollbar=Scrollbar(top_emp_frame, orient="horizontal")
        vertcal_scrollbar=Scrollbar(top_emp_frame,orient="vertical")

        employee_treeview=ttk.Treeview(top_emp_frame,columns=('empid', 'name','email', 'gender', 'dob', 'contact', 'employment_type','education','work_shift','address', 'doj','salary','usertype'),show="headings", yscrollcommand=vertcal_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
        horizontal_scrollbar.pack(side=BOTTOM, fill=X,pady=5)
        vertcal_scrollbar.pack(side=RIGHT,fill=Y,pady=(10,0))
        horizontal_scrollbar.config(command=employee_treeview.xview)
        vertcal_scrollbar.config(command=employee_treeview.yview)
        employee_treeview.pack() 


        employee_treeview.heading('empid',text='Employment ID')
        employee_treeview.heading ('name', text='Name')
        employee_treeview.heading('email', text='Email')
        employee_treeview.heading('gender' ,text='Gender')
        employee_treeview.heading('dob', text='Date of birth')
        employee_treeview.heading('contact', text='Contact')
        employee_treeview.heading('employment_type',text='Employment Type')
        employee_treeview.heading('education', text='Education')
        employee_treeview.heading('work_shift',text='Work Shift')
        employee_treeview.heading('address', text='Address')
        employee_treeview.heading('doj', text='Date of Joining')
        employee_treeview.heading('salary' ,text='Salary')
        employee_treeview.heading('usertype', text='User Type')

        employee_treeview.column('empid', width=90)
        employee_treeview.column('name', width=140)
        employee_treeview.column('email', width=180)
        employee_treeview.column('gender', width=80)
        employee_treeview.column('contact',width=100)
        employee_treeview.column('dob', width=100)
        employee_treeview.column('employment_type', width=120)
        employee_treeview.column('education', width=120)
        employee_treeview.column('work_shift', width=100)
        employee_treeview.column('address', width=200)
        employee_treeview.column('doj', width=100)
        employee_treeview.column('salary', width=140)
        employee_treeview.column('usertype', width=120)
        

        employee_details_frame=Frame(self.root)
        employee_details_frame.place(x=0,y=340)

        employee_details_label=Label(employee_details_frame, text= "EmployeeID", font=("Times New Roman", 15))
        employee_details_label.grid(row=0, column=0,padx=10,pady=10)
        employee_details_entry=Entry(employee_details_frame, font=("Times New Roman", 15),bg="light yellow")
        employee_details_entry.grid(row=0,column=1,padx=10,pady=10)


        employee_details_label=Label(employee_details_frame, text= "Name", font=("Times New Roman", 15))
        employee_details_label.grid(row=0, column=2,padx=10,pady=10)
        employee_details_entry=Entry(employee_details_frame, font=("Times New Roman", 15),bg="light yellow")
        employee_details_entry.grid(row=0,column=3,padx=10,pady=10)


        employee_details_label=Label(employee_details_frame, text= "Email", font=("Times New Roman", 15))
        employee_details_label.grid(row=0, column=4,padx=10,pady=10)
        employee_details_entry=Entry(employee_details_frame, font=("Times New Roman", 15),bg="light yellow")
        employee_details_entry.grid(row=0,column=5,padx=10,pady=10)


        employee_details_label=Label(employee_details_frame, text="Gender",font=("Times New Roman", 15))
        employee_details_label.grid(row=1,column=0,padx=10,pady=10)
        employee_details_entry_combo=ttk.Combobox(employee_details_frame, values=("Male","Female"),font=("Times New Roman",15),width=18,state='readonly')
        employee_details_entry_combo.set("Search Gender")
        employee_details_entry_combo.grid(row=1,column=1,padx=10,pady=10)

        employee_details_label=Label(employee_details_frame, text="Date of Birth",font=("Times New Roman", 15))
        employee_details_label.grid(row=1,column=2,padx=10,pady=10)
        employee_details_entry_calender=DateEntry(employee_details_frame,width=18, font=("Times New Roman", 15),state="readonly",date_pattern="dd/mm/yyyy")
        employee_details_entry_calender.grid(row=1,column=3,padx=10,pady=10)

        employee_details_label=Label(employee_details_frame, text="Contact",font=("Times New Roman", 15))
        employee_details_label.grid(row=1,column=4,padx=10,pady=10)
        employee_details_entry=Entry(employee_details_frame, font=("Times New Roman", 15),bg="light yellow")
        employee_details_entry.grid(row=1,column=5,padx=10,pady=10)

        employee_details_label=Label(employee_details_frame, text="Employment Type",font=("Times New Roman", 15))
        employee_details_label.grid(row=2,column=0, padx=10,pady=10)
        employee_details_entry_combo=ttk.Combobox(employee_details_frame, values=('Full time','Part time', 'Intern','Contract'),font=("Times New Roman",15),width=18,state='readonly')
        employee_details_entry_combo.set("Select Employment type")
        employee_details_entry_combo.grid(row=2,column=1,padx=10,pady=10)

        employee_details_label=Label(employee_details_frame, text="Education",font=("Times New Roman", 15))
        employee_details_label.grid(row=2,column=2, padx=10,pady=10)
        employee_details_entry_combo=ttk.Combobox(employee_details_frame, values=('FSc','ICOM','ICS','LLB','B.COM','M.Tech','MBA','B.Sc','BBA','LLM','B.ARC','M.Arc'),font=("Times New Roman",15),width=18,state='readonly')
        employee_details_entry_combo.set("Select Education")
        employee_details_entry_combo.grid(row=2,column=3,padx=10,pady=10)

        employee_details_label=Label(employee_details_frame, text="Working Shift",font=("Times New Roman", 15))
        employee_details_label.grid(row=2,column=4,padx=10,pady=10)
        employee_details_entry_combo=ttk.Combobox(employee_details_frame, values=("Morning","Evening","Night"),font=("Times New Roman",15),width=18,state='readonly')
        employee_details_entry_combo.set("Search Shift")
        employee_details_entry_combo.grid(row=2,column=5,padx=10,pady=10)

        employee_details_label=Label(employee_details_frame, text="Address",font=("Times New Roman", 15))
        employee_details_label.grid(row=3,column=0,padx=10,pady=10, sticky="w")
        emp_detail_address_Txt=Text(employee_details_frame,width=18, height=4,font=("Times New Roman", 15), bg="Light yellow")
        emp_detail_address_Txt.grid(row=3, column=1,padx=10, pady=10,rowspan=2)


        employee_details_label=Label(employee_details_frame, text="Date of Joining",font=("Times New Roman", 15))
        employee_details_label.grid(row=3,column=2,padx=10,pady=10)
        employee_details_entry_calender=DateEntry(employee_details_frame,width=18, font=("Times New Roman", 15),state="readonly",date_pattern="dd/mm/yyyy")
        employee_details_entry_calender.grid(row=3,column=3,padx=10,pady=10)

        employee_details_label=Label(employee_details_frame, text="User Type",font=("Times New Roman", 15))
        employee_details_label.grid(row=4,column=2,padx=10,pady=10)
        employee_details_entry_combo=ttk.Combobox(employee_details_frame, values=("Admin","Employee"),font=("Times New Roman",15),width=18,state='readonly')
        employee_details_entry_combo.set("Search User Type")
        employee_details_entry_combo.grid(row=4,column=3,padx=10,pady=10)

        employee_details_label=Label(employee_details_frame, text="Salary",font=("Times New Roman", 15))
        employee_details_label.grid(row=3,column=4,padx=10,pady=10)
        employee_details_entry=Entry(employee_details_frame, font=("Times New Roman", 15),bg="light yellow")
        employee_details_entry.grid(row=3,column=5,padx=10,pady=10)

        employee_details_label=Label(employee_details_frame, text="Password",font=("Times New Roman", 15))
        employee_details_label.grid(row=4,column=4,padx=10,pady=10)
        employee_details_entry=Entry(employee_details_frame, font=("Times New Roman", 15),bg="light yellow")
        employee_details_entry.grid(row=4,column=5,padx=10,pady=10)

        add_button=Button(self.root,text="ADD",font=("Times New Roman", 15),bg="purple",activebackground="purple",fg="white",activeforeground="white",cursor = 'hand2',width=10,)
        add_button.place(x=200,y=600)
        
    
        update_button=Button(self.root,text="UPDATE",font=("Times New Roman", 15),bg="purple",activebackground= "#7B68EE",fg="white",cursor = 'hand2',width=10)
        update_button.place(x=350,y=600)

        delete_button=Button(self.root,text="DELETE",font=("Times New Roman", 15),bg="purple",activebackground= "#7B68EE",fg="white",cursor = 'hand2',width=10)
        delete_button.place(x=500,y=600)

        clear_button=Button(self.root,text="CLEAR",font=("Times New Roman", 15),bg="purple",activebackground= "#7B68EE",fg="white",cursor = 'hand2',width=10)
        clear_button.place(x=650,y=600)

if __name__=="__main__":
        root = Tk()
        obj = Employee(root)
        root.mainloop()