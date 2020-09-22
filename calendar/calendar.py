from datetime import date, datetime
from tkinter import *

class Calendar():
    
    def __init__(self):
        l_mouth = range(1,32)
        s_mouth = range(1,31)
        self.calendar ={'1':('Styczeń',l_mouth), '2':('Luty',range(1,29)), '3':('Marzec',l_mouth), '4':('Kwiecień',s_mouth), '5':('Maj',l_mouth), 
                        '6':('Czerwiec',s_mouth), '7':('Lipiec',l_mouth), '8':('Sierpień',l_mouth), '9':('Wrzesień',s_mouth), '10':('Pażdziernik',l_mouth),
                        '11':('Listopad',s_mouth), '12':('Grudzień',l_mouth)}
        self.week = ('Pon', 'Wt', 'Śr', 'Czw', 'Pi', 'Sob', 'Niedz')

        self.window = Tk()
        self.dt = date.today()
        self.months = self.calendar[str(self.dt.month)]
        self.month_n = self.dt.month
        self.yr = self.dt.year
        self.m_day_frame = Frame(self.window)
        self.m_day_frame.grid(row=3, column=0, columnspan=7)

        self.year = Label(self.window, text=self.yr, height=2, justify='center')
        self.year.grid(row = 0, column=1, columnspan=5)

        self.y_button_left = Button(self.window, text="<", command=lambda: self.change_year(-1))
        self.y_button_left.grid(row=0, column=0)
        self.y_button_right = Button(self.window, text=">", command=lambda: self.change_year(1))
        self.y_button_right.grid(row=0, column=6)

        self.l_month = Label(self.window, text=self.months[0], height=2, justify='center')
        self.l_month.grid(row = 1, column=1, columnspan=5)
        self.m_button_left = Button(self.window, text="<", command=lambda: self.change_month(-1))
        self.m_button_left.grid(row=1, column=0)
        self.m_button_right = Button(self.window, text=">", command=lambda: self.change_month(1))
        self.m_button_right.grid(row=1, column=6)

        i=0
        for w_day in self.week:
            week_e = Label(self.window, text=w_day, width=15, height=2, justify='center')
            week_e.grid(row=2, column=i)
            i += 1

        self.render_days()


    def change_year(self, k):
        self.yr += k
        self.year.config(text=self.yr)
        self.render_days()

    def change_month(self, k):
        self.month_n += k
        if self.month_n < 1:
            self.month_n = 12
        if self.month_n > 12:
            self.month_n = 1
        self.months = self.calendar[str(self.month_n)]
        self.l_month.config(text=self.months[0])
        self.render_days()

    def render_days(self):
        for widget in self.m_day_frame.winfo_children():
            widget.destroy()
        c = self.get_first_day()
        r = 2
        if self.yr == self.dt.year and self.month_n == self.dt.month:
            today = "#a4ff48"
        else:
            today = None
        for m_day in self.months[1]:

            month_e = Button(self.m_day_frame, text=m_day, command=self.add_event, width=15, height=5, justify='center', bg=(today if m_day == self.dt.day else None ))
            month_e.grid(row=r, column=c)
            c += 1
            if(c == 7):
                r+=1
                c=0
    
    def get_first_day(self):
        return self.dt.replace(self.yr, month=self.month_n, day=1).weekday()
    
    def add_event(self):
        pass

