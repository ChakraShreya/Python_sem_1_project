from tkinter import *
from turtle import bgcolor, color
from PIL import ImageTk,Image
from tkinter import messagebox as mb

root=Tk()
root.title("Phone Book")
root.geometry("1000x700")
root.configure(bg="yellow")

# phonebook image displaying

root.iconbitmap("phone_ico.ico")
phoneBook_img=Image.open("phonebook_img.png")
resized_img=phoneBook_img.resize((100,100),Image.ANTIALIAS)
img=ImageTk.PhotoImage(resized_img)
ImageLabel=Label(image=img)
ImageLabel.pack()

# menu_frame

menu_frame=LabelFrame(root,text="MENU",padx=100,pady=80,bg="cyan",relief=SUNKEN)
menu_frame.pack()

# delete previous frames

def del_frames():
    for widget in menu_frame.winfo_children():
        widget.destroy()
    menu_frame.pack_forget()

#import all entries from file as dictionary
entries={}

def dict_entries():
    with open("phonebook.txt","r") as e:
        for line in e:
            global k
            global val_list
            k,val=line.strip().split(":")
            val_list=[]
            val_list.append(val.split(","))
            entries[k]=val_list

# all functions for buttons

def insert_entry():
    del_frames()
    menu_frame.pack_forget()
    insert_frame=LabelFrame(root,text="INSERT ENTRY",padx=100,pady=80,bg="cyan",relief=SUNKEN)
    insert_frame.pack()
    # namelabel
    name_label=Label(insert_frame,text="Name")
    name_label.grid(row=0,column=0)
    name=Entry(insert_frame,width=20,borderwidth=5)
    name.grid(row=1,column=0)
    # numberlabel
    number_label=Label(insert_frame,text="Number")
    number_label.grid(row=2,column=0)
    number=Entry(insert_frame,width=20,borderwidth=5)
    number.grid(row=3,column=0)

    def insert_click(nm,nn):
        #no empty entries
        if not(nm) or not(nn):
            if mb.askyesno("Empty Entry",'Would you like to fill the empty entries?'):
                pass
            else:
                root.destroy()
        #digits only no alphabets
        elif not(nn.isdigit()):
            if mb.askyesno("Invalid Phone Number",'Kindly enter numbers only. \nWould you like to re-enter a valid number?'):
                pass
            else:
                root.destroy()
        #10 digits only
        elif len(nn)!=10:
            if mb.askyesno("Invalid Phone Number",'Kindly enter a 10digit phone number only. \nWould you like to re-enter a valid number?'):
                pass
            else:
                root.destroy()

        else:
            dict_entries()
            nm=str(nm)
            nn=str(nn)
            if(nm in entries):
                entries[nm]+=[nn]
            else:
                entries.update({nm:[nn]})
            shove_dict_to_file()
            insert_message=Label(insert_frame,text="Your entry has been inserted").grid(row=5,column=0)

    insert_button=Button(insert_frame,text="Insert Entry",command=lambda: insert_click(name.get(),number.get())).grid(row=4,column=0)
    

def shove_dict_to_file():
    with open("phonebook.txt","w") as f:
        f.write("")
    v=""
    with open("phonebook.txt","a") as f:
        for key,value in entries.items():
            v=str(value)
            v=v.replace('[','')
            v=v.replace(']','')
            v=v.replace(" ","")
            v=v.replace("'","")
            result=key+":"+v+"\n"
            f.write(result)
#search
def search_no():
    dict_entries()
    no_search=entries.get(search_entry.get(),"not found")
    if no_search=='not found':
        if mb.askyesno("Contact unavailable",'Do you want to search for another number ?'):
            pass
        else:
            root.destroy()
            #tk.raise

    else:
        search_name_label=Label(search_frame,text=search_entry.get()+':')
        search_name_label.grid(row=2,column=0)
        for i in no_search[0]:
            searched_label=Label(search_frame,text=str(i)+'   ')
            searched_label.grid(row=3,column=1+no_search[0].index(i))

def search():
    global search_frame
    global search_entry
    dict_entries()
    del_frames()
    menu_frame.pack_forget()
    search_frame=LabelFrame(root,text="Search",padx=100,pady=80,bg="cyan",relief=SUNKEN)
    search_frame.pack()

    #user input for search
    search_label=Label(search_frame,text="Name: ")
    search_label.grid(row=0,column=0)
    search_entry=Entry(search_frame)
    search_entry.grid(row=0,column=1,columnspan=3)
    search_button=Button(search_frame,text='Enter',command=search_no)
    search_button.grid(row=1,column=4)


def sort():
    dict_entries()
    del_frames()
    menu_frame.pack_forget()
    sort_frame=LabelFrame(root,text="ALL CONTACTS",padx=100,pady=80,bg="cyan",relief=SUNKEN)
    sort_frame.pack(side="top",fill="both",expand=True)
    
    #sorting

    scroll_frame=Frame(root)
    scroll_frame.pack(fill=BOTH,expand=1)
    my_canvas=Canvas(scroll_frame,bg="grey")
    my_canvas.pack(side=LEFT,fill=BOTH,expand=1)
    my_scrollbar=Scrollbar(scroll_frame,orient=VERTICAL,command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT,fill=Y)
    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e:my_canvas.configure(scrollregion=my_canvas.bbox("all")))
    another_frame=Frame(my_canvas,bg="grey")
    my_canvas.create_window((0,0),window=another_frame,anchor="nw")

    key_list=list(entries.keys())
    key_list.sort()
    for i in key_list:
        name_label=Label(another_frame,text=i, borderwidth=1, relief="solid",fg='purple')
        posx,posy=key_list.index(i),0
        name_label.grid(row=posx,column=posy)
        for j in entries[i]:
            for k in j:
                no_label=Label(another_frame,text=k+'\n', borderwidth=1, relief="solid",width=15,fg="blue")
                posy=j.index(k)+2
                no_label.grid(row=posx,column=posy)

#DELETE AN ENTRY
def delete():
    del_frames()
    menu_frame.pack_forget()
    delete_frame=LabelFrame(root,text="Delete an entry",padx=100,pady=80,bg="grey",relief=SUNKEN)
    delete_frame.pack()



    name_label=Label(delete_frame,text="Name")
    name_label.grid(row=0,column=0)
    name=Entry(delete_frame,width=20,borderwidth=5)
    name.grid(row=1,column=0)
    
    
    def del_a_no(n_to_be_del,nd_list,name):
        dict_entries()
        for element in nd_list:
            if n_to_be_del==element:
                 nd_list.remove(element)

        del entries[name]
        entries[name]=nd_list
                         
        insert_message=Label(delete_frame,text="Your entry has been deleted").grid(row=3,column=0) 
        shove_dict_to_file()
    
    def temp(s,nd_list,name):
        del_a_no(s,nd_list,name)

    
    global delete
    def delete_click():
        del_frames()
        dict_entries()
        delete=str(name.get())
        if delete in entries.keys():
            if mb.askyesno("DELETE","Do you want to delete entire entry?"):

                 del entries[name.get()]
                 shove_dict_to_file()
                 insert_message=Label(delete_frame,text="Your entry has been deleted").grid(row=3,column=0) 
                 pass
                 
            else:
                def delete_no():
                    dict_entries()
                    nd=entries[name.get()]
                    nd=str(nd)
                    nd=nd.replace('[','')
                    nd=nd.replace(']','')
                    nd=nd.replace(" ","")
                    nd=nd.replace("'","")
                    nd_list=[]
                    nd_list=nd.split(",")

                    for i in nd_list:                  
                       delete_bt=Button(delete_frame,text=str(i)+'   ',command=lambda k=str(i): temp(k,nd_list,name.get()))
                       delete_bt.grid(row=3,column=1+nd_list.index(i))
                delete_no()
                     




    delete_button=Button(delete_frame,text="Delete Entry",command=lambda:delete_click()).grid(row=4,column=0)
    

# all function buttons

button_insert=Button(menu_frame,text="Add a new entry",font="Times 15",padx=50,pady=20,fg="blue",bg='orange',command=insert_entry)
button_search=Button(menu_frame,text="Search an entry",font="Times 15",padx=50,pady=20,fg="blue",bg='orange',command=search)
button_sorted=Button(menu_frame,text="Display entries in sorted order",font="Times 15",padx=50,pady=20,fg="blue",bg='orange',command=sort)
button_del=Button(menu_frame,text="Delete an entry",font="Times 15",padx=50,pady=20,fg="blue",bg='orange',command=delete)

button_insert.pack()
button_search.pack()
button_sorted.pack()
button_del.pack()




button_quit=Button(root,text="Exit",padx=10,pady=10,fg="white",bg='red',font="Times 15",command=root.quit)
button_quit.pack()




root.mainloop()
