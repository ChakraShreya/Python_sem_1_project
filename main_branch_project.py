from tkinter import *
from PIL import ImageTk,Image

root=Tk()
root.title("Phone Book")
root.geometry("800x600")
root.configure(bg="yellow")

# phonebook image displaying

root.iconbitmap("phone_ico.ico")
phoneBook_img=Image.open("phonebook_img.png")
resized_img=phoneBook_img.resize((100,100),Image.ANTIALIAS)
img=ImageTk.PhotoImage(resized_img)
ImageLabel=Label(image=img)
ImageLabel.pack()

# menu_frame

menu_frame=LabelFrame(root,text="MENU",padx=100,pady=80,bg="grey",relief=SUNKEN)
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
    insert_frame=LabelFrame(root,text="INSERT ENTRY",padx=100,pady=80,bg="grey",relief=SUNKEN)
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
    no_search=entries.get(search_entry.get(),"This contact is not available")
    search_name_label=Label(search_frame,text=search_entry.get()+':')
    search_name_label.grid(row=2,column=0)
    for i in no_search:
        searched_label=Label(search_frame,text=i)
        searched_label.grid(row=3,column=1+no_search.index(i))

def search():
    global search_frame
    global search_entry
    dict_entries()
    del_frames()
    menu_frame.pack_forget()
    search_frame=LabelFrame(root,text="Search",padx=100,pady=80,bg="grey",relief=SUNKEN)
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
    sort_frame=LabelFrame(root,text="ALL CONTACTS",padx=100,pady=80,bg="grey",relief=SUNKEN)
    sort_frame.pack()
    
    #sorting
    key_list=list(entries.keys())
    key_list.sort()
    for i in key_list:
        name_label=Label(sort_frame,text=i, borderwidth=1, relief="solid",bg='black',fg='white')
        posx,posy=key_list.index(i),0
        name_label.grid(row=posx,column=posy)
        for j in entries[i]:
            for k in j:
                no_label=Label(sort_frame,text=k+'\n', borderwidth=1, relief="solid",width=15)
                posy=j.index(k)+2
                no_label.grid(row=posx,column=posy)

    #slider
    '''vertical=Scale(sort_frame,from_=0,to=100)
    vertical.grid(row=0,column=10,command=slide)'''
    
            

# all function buttons

button_insert=Button(menu_frame,text="Add a new entry",padx=50,pady=10,fg="blue",command=insert_entry)
button_search=Button(menu_frame,text="Search an entry",padx=50,pady=10,fg="blue",command=search)
button_sorted=Button(menu_frame,text="Display entries in sorted order",padx=50,pady=10,fg="blue",command=sort)
button_del=Button(menu_frame,text="Delete an entry",padx=50,pady=10,fg="blue")

button_insert.pack()
button_search.pack()
button_sorted.pack()
button_del.pack()




button_quit=Button(root,text="Exit",padx=10,pady=10,fg="red",command=root.quit)
button_quit.pack()




root.mainloop()
