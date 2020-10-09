from datetime import date, datetime

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.properties import StringProperty

class CalendarView(Widget):
    l_mouth = range(1, 32)
    s_mouth = range(1, 31)
    calendar = {
        "1": ("January", l_mouth),
        "2": ["February", range(1, 30)],
        "3": ("March", l_mouth),
        "4": ("April", s_mouth),
        "5": ("May", l_mouth),
        "6": ("June", s_mouth),
        "7": ("July", l_mouth),
        "8": ("August", l_mouth),
        "9": ("September", s_mouth),
        "10": ("October", l_mouth),
        "11": ("November", s_mouth),
        "12": ("December", l_mouth),
    }
    week = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
    year_l = StringProperty()
    month_l = StringProperty()
    def __init__(self, **kwargs):
        super(CalendarView, self).__init__()
        self.dt = date.today()
        self.month_n = kwargs["month"]
        self.month = self.calendar[str(self.month_n)]
        self.month_l = self.month[0]
        self.year = kwargs["year"]
        self.year_l = str(kwargs["year"])
        for w_day in self.week:
            self.week_grid.add_widget(Label(text=w_day))
        self.leap_year
        self.render_days()

    def render_days(self):
        self.days_grid.clear_widgets()
        if self.month_n == 1:
            days = 31
        else:
            days = ((self.calendar[str(self.month_n - 1)])[1])[-1]
        c = self.get_first_day()
        if c > 0:
            for n in range(c, 0, -1):
                self.days_grid.add_widget(Label(text=str(days-n+1)))
        if self.year == self.dt.year and self.month_n == self.dt.month:
            today = [0.51, 0.89, 0.25, 0.65]
        else:
            today = [1,1,1,1]
        for m_day in self.month[1]:
            self.days_grid.add_widget(Button(text=str(m_day), background_color=( today if m_day == self.dt.day else [1,1,1,1])))
            c += 1
            if c >= 7:
                c = 0
        if c < 7 and c != 0:
            for n in range(c, 7, 1):
                self.days_grid.add_widget(Label(text=str(n - c + 1)))
                
    def get_first_day(self):
        return self.dt.replace(self.year, month=self.month_n, day=1).weekday()
    
    def change_year(self, k):
        if k == "<":
            self.year -= 1
        else:
            self.year += 1
        self.year_label.text = str(self.year)
        self.leap_year()
        self.render_days()

    def change_month(self, k):
        if k == "<":
            self.month_n -= 1
        else:
            self.month_n += 1
        if self.month_n < 1:
            self.month_n = 12
        elif self.month_n > 12:
            self.month_n = 1
        self.month = self.calendar[str(self.month_n)]
        self.month_label.text = self.month[0]
        self.render_days()
    
    def leap_year(self):
        if (self.year % 4) == 0:
            if (self.year % 100) == 0:
                if (self.year % 400) == 0:
                    (self.calendar["2"])[1] = range(1, 30)
                else:
                    (self.calendar["2"])[1] = range(1, 29)
            else:
                (self.calendar["2"])[1] = range(1, 30)
        else:
            (self.calendar["2"])[1] = range(1, 29)