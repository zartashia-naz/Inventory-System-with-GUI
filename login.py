from tkinter import *
root=Tk()
root.title("Login Page")
root.geometry("400x500")
root.resizable(FALSE,FALSE)

lbl=Label(root,text="USER LOGIN PAGE",font=("times new roman",25,"bold"),fg="RED").place(x=20,y=10)
lbl_1=Label(root,text="Username:",font=("times new roman",15),fg="Black").place(x=30,y=50)
text_entry=Entry(root,font=("times new roman",15),fg="Black",).place(x=120,y=50)
lbl_2=Label(root,text="Email:",font=("times new roman",15),fg="Black").place(x=30,y=80)
text_entry2=Entry(root,font=("times new roman",15),fg="Black",).place(x=120,y=80)
# text_entry=Entry(root,font=("times new roman",40,"bold"),bg="lightyellow",fg="black").place(x=20,y=300)
root.mainloop()