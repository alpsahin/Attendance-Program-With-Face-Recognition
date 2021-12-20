import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from tkinter import messagebox,PhotoImage
from tkcalendar import Calendar, DateEntry
from create_dataset import startCreate
from create_classifier import startTrainer
from Detector import startRecognize
import sqlite3
from tkinter import BOTH, END, LEFT

#from PIL import ImageTk, Image
#from gender_prediction import emotion,ageAndgender


def my_details(controller, lesson, course_date, rec_date, offset):
    controller.show_frame("PageFour")
    controller.update_frame("PageFour", lesson, course_date, rec_date, offset)


def on_createUser(id_var, name_var, age_var, gender_var):
    startCreate(str(id_var.get()),str(name_var.get()),str(age_var.get()) ,str(gender_var.get()))

def on_startTrainer():
    if messagebox.askokcancel("Trainer", "Dataset will be trained."):
        startTrainer()

def on_detector(lesson, lecture_date):
    startRecognize(lesson, lecture_date)

class MainUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=16, weight="bold")
        self.title("Student Attendance With Face Recognition")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None
        self.geometry("960x540")
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            self.show_frame("StartPage")

    def show_frame(self, page_name):
            frame = self.frames[page_name]
            frame.tkraise()

    def update_frame(self, page_name, lecture, course_date, rec_date, offset):
        frame = self.frames[page_name]
        frame.update_list(lecture, course_date, rec_date, offset)

    def on_closing(self):

        if messagebox.askokcancel("Quit", "Are you sure?"):
            self.destroy()
    


class StartPage(tk.Frame):

        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            #sload = Image.open("f.png")
            #load = load.resize((250, 250), Image.ANTIALIAS)
            render = PhotoImage(file='logoalp.png')
            img = tk.Label(self, image=render, borderwidth=0)
            img.image = render
            img.grid(row=0, column=8, rowspan=14, sticky="nsew")
            label = tk.Label(self, text="ATTENDANCE MANAGER", font='Helvetica 22 bold', fg="black", bg="#EDEDED")
            label2 = tk.Label(self, text="                      ", font='Helvetica 22 bold', fg="#122B3F", bg="#EDEDED")
            label.grid(row=12, column=8,padx=10, pady=10)
            label2.grid(row=12, column=1,padx=20, pady=10)

            button1 = tk.Button(self, text="    Add a Student    ", font='Helvetica 12 bold', fg="#000", bg="#FFC300", height=1, width=35, command=lambda: self.controller.show_frame("PageOne"))
            button2 = tk.Button(self, text="    Start Lecture    ", font='Helvetica 12 bold', fg="#000", bg="#FFC300", height=1, width=35, command=lambda: self.controller.show_frame("PageTwo"))
            button4 = tk.Button(self, text="   Attendance List   ", font='Helvetica 12 bold', fg="#000", bg="#FFC300", height=1, width=35, command=lambda: self.controller.show_frame("PageThree"))
            
            button1.grid(row=13, column=8,padx=10, pady=10, ipady=5)
            button2.grid(row=14, column=8,padx=10, pady=10, ipady=5)
            button4.grid(row=15, column=8,padx=10, pady=10, ipady=5)

            self.configure(bg= "#EDEDED", pady=1)


        def on_closing(self):
            if messagebox.askokcancel("Quit", "Are you sure?"):
                self.controller.destroy()




class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        id_var=tk.StringVar()
        name_var=tk.StringVar()
        age_var=tk.StringVar()
        gender_var=tk.StringVar()

        tk.Frame.__init__(self, parent)
        self.controller = controller

        label2 = tk.Label(self, text="                      ", font='Helvetica 22 bold', fg="#122B3F", bg="#EDEDED")
        label2.grid(row=3, column=1,padx=20, pady=10)

        label = tk.Label(self, text="Personal Information", font='Helvetica 22 ', fg="black", bg="#EDEDED")
        label.grid(row=1,  column=3,padx=0)


        tk.Label(self, text="Student Name", bg="#EDEDED", fg="#000", font='Helvetica 12 bold').grid(row=8, column=2, pady=10, padx=1,)
        self.user_name = tk.Entry(self, textvariable = name_var, borderwidth=3, bg="lightgrey", font='Helvetica 11 bold')
        self.user_name.grid(row=8,  column=3,padx=0)

        tk.Label(self, text="Student Id", bg="#EDEDED", fg="#000", font='Helvetica 12 bold').grid(row=9, column=2, pady=10, padx=0,)
        self.user_id = tk.Entry(self, textvariable = id_var, borderwidth=3, bg="lightgrey", font='Helvetica 11 bold')
        self.user_id.grid(row=9, column=3,padx=0)

        tk.Label(self, text="Student Age", bg="#EDEDED", fg="#000", font='Helvetica 12 bold').grid(row=10, column=2, pady=10, padx=0,)
        self.user_age = tk.Entry(self, textvariable = age_var, borderwidth=3, bg="lightgrey", font='Helvetica 11 bold')
        self.user_age.grid(row=10, column=3,padx=0)

        tk.Label(self, text="Student Gender", bg="#EDEDED", fg="#000", font='Helvetica 12 bold').grid(row=11, column=2, pady=10, padx=0,)
        self.user_gender = tk.Entry(self, textvariable = gender_var, borderwidth=3, bg="lightgrey", font='Helvetica 11 bold')
        self.user_gender.grid(row=11,  column=3,padx=0)

        self.buttoncanc = tk.Button(self, text="Back", bg="#FFC300", fg="#000", width=20, command=lambda: controller.show_frame("StartPage"))
        self.buttoncanc.grid(row=12,  column=10,padx=25, ipadx=10, ipady=4, pady=10)

        self.buttonadd = tk.Button(self, text ="Add User", bg="#FFC300", fg="#000", width=20, command=lambda: on_createUser(id_var, name_var, age_var, gender_var))
        self.buttonadd.grid(row=12, column=1, pady=10, padx=5, ipadx=5, ipady=4)

        button3 = tk.Button(self, text="Train Dataset", font='Helvetica 12', fg="#000", bg="#CCFF00", height=1, width=25, command=lambda: on_startTrainer())
        button3.grid(row=12, column=3,padx=75, pady=10)


        self.configure(bg="#EDEDED")


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        coursename_var = tk.StringVar()

        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text=" ", font='Helvetica 22 ', fg="black", bg="#EDEDED")
        label.grid(row=2,  column=2,ipadx=5, pady=40)


        tk.Label(self, text="Course Name", bg="#EDEDED", fg="#000", font='Helvetica 12 bold').grid(row=8, column=2, pady=40, padx=16)
        tk.Label(self, text="Course Date", bg="#EDEDED", fg="black", font='Helvetica 12 bold').grid(row=6, column=2, pady=10, padx=25)


        self.buttoncanc = tk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"), bg="#FFC300", fg="#000", width=20)
        self.menuvar = tk.StringVar(self)
        self.buttonext = tk.Button(self, text="Next", command=lambda: on_detector(self.cb.get(), self.lesson_date.get_date()), fg="#000", bg="#FFC300", width=20)
        self.buttoncanc.grid(row=10,  column=5,padx=30, pady=10, ipadx=10, ipady=7)
        self.buttonext.grid(row=10, column=1, pady=10, padx=70,ipadx=10, ipady=7)

        self.cb = ttk.Combobox(self, state="readonly")
        self.cb['values'] = self.combo_input()
        self.cb.grid(row=8,ipadx=5, ipady=4, column=3, pady=10, padx=5)

        #date
        self.lesson_date = DateEntry(self, state="readonly", locale='tr_TR', date_pattern='yyyy-mm-dd')
        self.lesson_date.grid(row=6, ipadx=5, ipady=4, column=3, pady=10, padx=5)        

        self.configure(bg="#EDEDED")

    def combo_input(self):
        db = sqlite3.connect('FaceBase.db')
        cursor = db.cursor()
        cursor.execute('SELECT NAME FROM LESSON')
        data = []

        for row in cursor.fetchall():
            data.append(row[0])

        db.close()
        return data




class PageThree(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        course_var=tk.StringVar()
        section_var=tk.StringVar()

        self.controller = controller

        #header label
        label = tk.Label(self, text="        Attendance List", font='Helvetica 22 ', fg="black", bg="#EDEDED")
        label.grid(row=2,  column=2,ipadx=5, pady=40)

        #name label
        tk.Label(self, text="Course Name", bg="#EDEDED", fg="black", font='Helvetica 12 bold').grid(row=5, column=2, pady=10, padx=25)  
        
        #date label
        tk.Label(self, text="Course Date", bg="#EDEDED", fg="black", font='Helvetica 12 bold').grid(row=6, column=2, pady=10, padx=25)

        #back button
        self.buttoncanc = tk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"), bg="#FFC300", fg="#000", width=20)
        self.buttoncanc.grid(row=7, column=4, ipadx=5, ipady=4,pady=10, padx=5)
        
        #show attendance button
        self.attendance_list = tk.Button(self, text="Attendance List", command=lambda: [my_details(controller, self.cb.get(), self.lesson_date.get_date(), 0, 0)], bg="#FFC300", fg="#000", width=20)
        self.attendance_list.grid(row=7, column=1, ipadx=5, ipady=4, pady=10, padx=65)

        #lesson
        self.cb = ttk.Combobox(self, state="readonly")
        self.cb['values'] = self.combo_input()
        self.cb.grid(row=5, ipadx=5, ipady=4, column=3, pady=10, padx=25)

        #date
        self.lesson_date = DateEntry(self, state="readonly", locale='tr_TR', date_pattern='yyyy-mm-dd')
        self.lesson_date.grid(row=6, ipadx=5, ipady=4, column=3, pady=10, padx=5)

        self.configure(bg="#EDEDED")

    def combo_input(self):
        db = sqlite3.connect('FaceBase.db')
        cursor = db.cursor()
        cursor.execute('SELECT NAME FROM LESSON')
        data = []

        for row in cursor.fetchall():
            data.append(row[0])

        db.close()
        return data

    

class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

    def update_list(self, lesson, course_date, rec_date, offset):
        my_c = sqlite3.connect("FaceBase.db")
        my_c = my_c.cursor()
        r_set=my_c.execute("SELECT count(*) FROM ATTENDANCE WHERE LESSON='"+lesson+"' AND ATTENDANCE_DATE>='"+str(course_date)+" 00:00:00' AND ATTENDANCE_DATE<'"+str(course_date)+" 23:59:59'")
        data_row=r_set.fetchone()
        nu_rec=data_row[0] # Total number of rows in table
        limit = 8; # No of records to be shown per page.
        print(str(nu_rec) + "-" + str(course_date))

        self.buttoncanc = tk.Button(self, text="Back", command=lambda: [self.controller.show_frame("PageThree")], bg="#555956", fg="#fff", width=20)
        self.buttoncanc.grid(row=13, column=1, ipadx=5, ipady=4,pady=10, padx=5)

        if(nu_rec > 0):
            try:
                try:
                    q = "SELECT STUDENT_ID, STUDENT_NAME, STRFTIME('%d/%m/%Y - %H:%M', ATTENDANCE_DATE) AS ATTENDANCE_DATE FROM ATTENDANCE  WHERE LESSON='"+lesson+"' AND ATTENDANCE_DATE>='"+str(course_date)+" 00:00:00' AND ATTENDANCE_DATE<'"+str(course_date)+" 23:59:59' LIMIT " + str(offset) + "," +str(limit)
                    r_set=my_c.execute(q)
                    i=1 # row value inside the loop
                    label = tk.Label(self, text=lesson, font='Helvetica 22 ', fg="black", bg='white')
                    label.grid(row=0, column=0,ipadx=5, pady=5)


                    for student in r_set: 
                        for j in range(len(student)):
                            self.e = tk.Entry(self, width=20, fg='black', bg='white', font = "Helvetica 18 bold") 
                            self.e.grid(row=i, column=j, ipadx=28, ipady=10) 
                            self.e.insert(END, student[j])
                        i=i+1
                    while (i<=limit):
                        for j in range(len(student)):
                            self.e = tk.Entry(self, width=20, fg='black', bg='white', font = "Helvetica 18 bold") 
                            self.e.grid(row=i, column=j, ipadx=28, ipady=10) 
                            self.e.insert(END, "")
                        i=i+1

                    back = offset - limit
                    next = offset + limit
                    
                    b1 = tk.Button(self, text='Next >', command=lambda: self.update_list(lesson, course_date, rec_date, next))
                    b1.grid(row=13,column=2, ipadx= 10, ipady=5, pady=5)
                    b2 = tk.Button(self, text='< Prev', command=lambda: self.update_list(lesson, course_date, rec_date, back))
                    b2.grid(row=13,column=0, ipadx= 10, ipady=5, pady=5)

                    if(nu_rec <= next): 
                        b1["state"]="disabled"
                    else:
                        b1["state"]="active"
                        
                    if(back >= 0):
                        b2["state"]="active"
                    else:
                        b2["state"]="disabled"
                except:
                    print("db error")
            except:
                print("db error")
        else:
            self.controller.show_frame("PageThree")
        my_c.close()
        self.configure(bg='white')
        

        
app = MainUI()
app.iconphoto(False, tk.PhotoImage(file='ikon.png'))
app.mainloop()