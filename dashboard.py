from tkinter import *
from PIL import Image,ImageTk
class IMS:
    def __init__(self, root):
        self.root=root
        self.root.geometry("1370x750")
        self.root.title("Inventory Management System")

        self.logo=PhotoImage(file="C:\\Users\\BilalQA\\Desktop\\inventory management system\\img logo2.png")
        lbl_title=Label(self.root,text="INVENTORY MANAGMENT SYSTEM",image=self.logo,compound=LEFT,padx=10,font=("Arial",40,"bold"),bg="purple",fg="white",anchor="w").place(x=0,y=0,relwidth=1,height=70)

        logout_btn=Button(self.root,text="LOGOUT",font=("Arial",15),bg="light yellow",fg="black",cursor="hand2").place(x=1240,y=20,height=25)
        lb12=Label(self.root,text="Welcome to Inventory Management System",font=("Arial",25),bg="light gray",fg="white",justify=CENTER).place(x=0,y=70,relwidth=1,height=40)


        self.img=Image.open("C:\\Users\\BilalQA\\Desktop\\inventory management system\\IMS img.jpeg")
        left_menu=Frame(self.root,bd=3,relief=GROOVE,image=self.img)
        left_menu.place(x=0,y=110,height=550,width=225)
root=Tk()
obj=IMS(root)
root.mainloop()