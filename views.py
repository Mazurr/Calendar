from datetime import date, datetime
from tkinter import Button, Label, Frame, Entry, Text

class CalendarView(Frame):
    l_mouth = range(1,32)
    s_mouth = range(1,31)
    calendar ={ '1':('January',l_mouth), '2':['February',range(1,30)], '3':('March',l_mouth), '4':('April',s_mouth), '5':('May',l_mouth), 
                '6':('June',s_mouth), '7':('July',l_mouth), '8':('August',l_mouth), '9':('September',s_mouth), '10':('October',l_mouth),
                '11':('November',s_mouth), '12':('December',l_mouth)}
    week = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')

    def __init__(self, window, **kwargs):
        Frame.__init__(self, window)
        self.window = window
        self.dt = date.today()
        self.month_n = kwargs['month']
        self.months = self.calendar[str(self.month_n)]
        self.yr = kwargs['year']
        self.m_day_frame = Frame(self)
        self.m_day_frame.grid(row=3, column=0, columnspan=7)

        self.year = Label(self, text=self.yr, height=2, justify='center')
        self.year.grid(row = 0, column=1, columnspan=5)

        self.y_button_left = Button(self, text="<", command=lambda: self.change_year(-1))
        self.y_button_left.grid(row=0, column=0)
        self.y_button_right = Button(self, text=">", command=lambda: self.change_year(1))
        self.y_button_right.grid(row=0, column=6)

        self.l_month = Label(self, text=self.months[0], height=2, justify='center')
        self.l_month.grid(row = 1, column=1, columnspan=5)
        self.m_button_left = Button(self, text="<", command=lambda: self.change_month(-1))
        self.m_button_left.grid(row=1, column=0)
        self.m_button_right = Button(self, text=">", command=lambda: self.change_month(1))
        self.m_button_right.grid(row=1, column=6)

        i=0
        for w_day in self.week:
            week_e = Label(self, text=w_day, width=15, height=2, justify='center')
            week_e.grid(row=2, column=i)
            i += 1
        self.leap_year
        self.render_days()

    def leap_year(self):
        if (self.yr % 4) == 0:
           if (self.yr % 100) == 0:
               if (self.yr % 400) == 0:
                    (self.calendar['2'])[1] = range(1,30)
               else:
                   (self.calendar['2'])[1] = range(1,29)
           else:
               (self.calendar['2'])[1] = range(1,30)
        else:
           (self.calendar['2'])[1] = range(1,29)

    def change_year(self, k):
        self.yr += k
        self.year.config(text=self.yr)
        self.leap_year()
        self.render_days()

    def change_month(self, k):
        self.month_n += k
        if self.month_n < 1:
            self.month_n = 12
        elif self.month_n > 12:
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
        if self.month_n == 1:
            days = 31
        else:
            days = ((self.calendar[str(self.month_n-1)])[1])[-1]
        if (c > 0):
            for n in range(c,0,-1):
                prev_month = Label(self.m_day_frame, text=days-n+1, width=15, height=5, justify='center')
                prev_month.grid(row=r, column=c-n)
        for m_day in self.months[1]:
            month_b = Button(self.m_day_frame, text=m_day, command=lambda d=m_day: self.window.show_view("events_list_view", year=self.yr, month=self.month_n, day=d), 
                            width=15, height=5, justify='center', bg=(today if m_day == self.dt.day else None ))
            month_b.grid(row=r, column=c)
            c += 1
            if(c == 7):
                r+=1
                c=0
        if (c < 7 and c != 0):
            for n in range(c,7,1):
                next_month = Label(self.m_day_frame, text=n-c+1, width=15, height=5, justify='center')
                next_month.grid(row=r, column=n)

    def get_first_day(self):
        return self.dt.replace(self.yr, month=self.month_n, day=1).weekday()

class AddEventsView(Frame):
    def __init__(self, window, **kwargs):
        Frame.__init__(self, window)
        self.window = window
        self.conn = kwargs['conn']
        self.day = kwargs['day']
        self.month = kwargs['month']
        self.year = kwargs['year']

        year_l = Label(self, text=self.year, height=2, width=50, justify='center')
        year_l.grid(row = 0, column=0)
        #self.month_l = Label(self, text=self.year, height=2, width=15, justify='center')
        #self.month_l.grid(row = 0, column=0)
        title_l = Label(self, text="Title", height=2, width=50,  justify='left')
        title_l.grid(row = 1, column=0)
        self.title = Entry(self, width=50)
        self.title.grid(row = 2, column=0)

        descript_l = Label(self, text="Description", height=2, width=15)
        descript_l.grid(row = 3, column=0)
        self.descript = Text(self, height=25, width=50)
        self.descript.grid(row = 4, column=0)

        save = Button(self, text="Save", command=self.save_event, width=50, height=2, justify='center')
        save.grid(row=5, column=0)

        cancel = Button(self, text="Cancel", command=lambda: window.show_view("events_list_view", year=self.year, month=self.month, day=self.day), width=50, height=2, justify='center')
        cancel.grid(row=6, column=0)

    def save_event(self):
        title = self.title.get()
        descript = self.descript.get("1.0",'end-1c')
        query = ''' INSERT INTO Events(title, descript, date)
              VALUES('{}', '{}', {:02}-{:02}-{:02}) '''.format(title, descript, self.day, self.month, self.year)
        print(query)
        c = self.conn.cursor()
        c.execute(query)
        self.conn.commit()
        self.window.show_view("events_list_view", year=self.year, month=self.month, day=self.day)

class EventsListView(Frame):
    def __init__(self, window, **kwargs):
        Frame.__init__(self, window)
        self.conn = kwargs['conn']
        self.day = kwargs['day']
        self.month = kwargs['month']
        self.year = kwargs['year']
        self.window = window
        
        year_l = Label(self, text=self.year, height=2, width=50, justify='center')
        year_l.grid(row=0, column=0, columnspan=2)

        rows = self.list_events()
        r = 1
        for row in rows:
            event_t = Text(self, state='disabled', width=50)
            event_t.insert("1.0", row)
            event_t.grid(row=r, column=0, columnspan=2)
            r += 1
            del_ev = Button(self, text="Delete", command=lambda id=row[0]: self.delete_event(id=id))
            del_ev.grid(row=r, column=0)
            edit_ev = Button(self, text = "Edit")
            edit_ev.grid(row=r, column=1)
            r+=1
        add = Button(self, text="Add new event", command=lambda: window.show_view("add_event_view", year=self.year, month=self.month, day=self.day), width=50, height=2, justify='center')
        add.grid(row=r+1, column=0, columnspan=2)

        back = Button(self, text="Back", command=lambda: window.show_view("calendar_view", year=self.year, month=self.month, day=self.day), width=50, height=2, justify='center')
        back.grid(row=r+2, column=0, columnspan=2)

    def list_events(self):
        c = self.conn.cursor()
        query = "SELECT * FROM Events WHERE Events.date == {:02}-{:02}-{:02} ORDER BY 'date'".format(self.day, self.month, self.year)
        c.execute(query)
        rows = c.fetchall()
        return rows

    def delete_event(self, id):
        c = self.conn.cursor()
        query = "DELETE FROM Events WHERE Events.id == {} ".format(id)
        print(query)
        c.execute(query)
        self.conn.commit()
        self.window.show_view("events_list_view", year=self.year, month=self.month, day=self.day)