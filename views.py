from datetime import date, datetime

from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivy.uix.gridlayout import GridLayout

calendar = {
    "1": ("January", range(1, 32)),
    "2": ("February", range(1, 30), range(1, 29)),
    "3": ("March", range(1, 32)),
    "4": ("April", range(1, 31)),
    "5": ("May", range(1, 32)),
    "6": ("June", range(1, 31)),
    "7": ("July", range(1, 32)),
    "8": ("August", range(1, 32)),
    "9": ("September", range(1, 31)),
    "10": ("October", range(1, 32)),
    "11": ("November", range(1, 31)),
    "12": ("December", range(1, 32)),
}
week = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")


class CalendarView(Screen):
    def __init__(self, **kwargs):
        super(CalendarView, self).__init__()
        self.dt = date.today()
        self.month_n = kwargs["month"]
        self.month = calendar[str(self.month_n)]
        self.month_label.text = self.month[0]
        self.year = kwargs["year"]
        self.year_label.text = str(self.year)
        for w_day in week:
            self.week_grid.add_widget(Label(text=w_day))
        self.render_days()

    def render_days(self):
        self.days_grid.clear_widgets()
        if self.month_n == 2:
            l = self.leap_year()
        else:
            l = 1
        if self.month_n == 1:
            days = 31
        else:
            days = ((calendar[str(self.month_n - 1)])[1])[-1]

        c = self.get_first_day()
        if c > 0:
            for n in range(c, 0, -1):
                self.days_grid.add_widget(Label(text=str(days - n + 1)))

        if self.year == self.dt.year and self.month_n == self.dt.month:
            today = [0.51, 0.89, 0.25, 0.65]
        else:
            today = [1, 1, 1, 1]
        for m_day in self.month[l]:
            self.days_grid.add_widget(
                Button(
                    text=str(m_day),
                    background_color=(today if m_day == self.dt.day else [1, 1, 1, 1]),
                    on_press=self.add_event,
                )
            )
            c += 1
            if c >= 7:
                c = 0

        if c < 7 and c != 0:
            for n in range(c, 7, 1):
                self.days_grid.add_widget(Label(text=str(n - c + 1)))

    def get_first_day(self):
        return self.dt.replace(self.year, month=self.month_n, day=1).weekday()

    def change_year(self, k):
        self.year += k
        self.year_label.text = str(self.year)
        self.leap_year()
        self.render_days()

    def change_month(self, k):
        self.month_n += k
        if self.month_n < 1:
            self.month_n = 12
        elif self.month_n > 12:
            self.month_n = 1
        self.month = calendar[str(self.month_n)]
        self.month_label.text = self.month[0]
        self.render_days()

    def leap_year(self):
        if (self.year % 4) == 0:
            if (self.year % 100) == 0:
                if (self.year % 400) == 0:
                    return 1
                else:
                    return 2
            else:
                return 1
        else:
            return 2

    def add_event(self, day):
        self.parent.year = self.year
        self.parent.month = self.month_n
        self.parent.day = int(day.text)
        self.parent.change_screen("event_list")


class EventListView(Screen):
    id_e, popup = None, None
    def __init__(self, conn, **kwargs):
        super(EventListView, self).__init__()
        self.conn = conn
        self.year = 2019
        self.month = 20
        self.day = 2
        self.button_list = {}

    def on_pre_enter(self):
        self.year = self.parent.year
        self.month = self.parent.month
        self.day = self.parent.day
        self.year_label.text = str(self.year)
        self.month_label.text = (calendar[str(self.month)])[0]
        self.list_event()

    def add_event(self):
        self.parent.change_screen("add_event")

    def go_back(self):
        self.parent.change_screen("calendar")

    def list_event(self):
        self.event_list_grid.clear_widgets()
        self.button_list = {}
        data = self.events_query()
        for row in data:
            self.event_list_grid.add_widget(Label(text=str(row)))
            child_grid = GridLayout(
                cols=2,
                size_hint_y=None,
                height=30,
                row_default_height=30,
                row_force_default=True,
            )
            temp = Button(text="Edit", on_press=self.edit_event)
            self.button_list[temp] = row[0]
            child_grid.add_widget(temp)
            temp = Button(text="Delete", on_release=self.delete_confirm)
            self.button_list[temp] = (row[0], row[1])
            child_grid.add_widget(temp)
            self.event_list_grid.add_widget(child_grid)
    
    def delete_confirm(self, btn):
        event = self.button_list[btn]
        self.id_e = event[0]
        box = GridLayout(cols=1, padding = (10))
        box.add_widget(Label(text = 'Delete event '+event[1]+"?"))
        btn1 = Button(text = "DELETE", on_release = self.delete_event)
        btn2 = Button(text = "CANCEL")
        box.add_widget(btn1)
        box.add_widget(btn2)
        popup = Popup(
            title="Confirm Delete!",
            content=box,
            size_hint=(None, None), 
            size=(400, 400,),
            auto_dismiss = True
        )
        self.popup = popup
        btn2.bind(on_press = popup.dismiss)
        popup.open()


    def delete_event(self, *args):
        for a in args:
            print(args)
        self.popup.dismiss()
        c = self.conn.cursor()
        query = "DELETE FROM Events WHERE Events.id == {} ".format(self.id_e)
        self.id_e = None
        c.execute(query)
        self.conn.commit()
        self.on_pre_enter()

    def events_query(self):
        c = self.conn.cursor()
        query = "SELECT * FROM Events WHERE Events.date == {:02}-{:02}-{:02} ORDER BY 'date'".format(
            self.day, self.month, self.year
        )
        c.execute(query)
        rows = c.fetchall()
        return rows
    
    def edit_event(self, btn):
        self.parent.event = self.button_list[btn]
        self.parent.change_screen("add_event")

class AddEventView(Screen):
    def __init__(self, conn, **kwargs):
        super(AddEventView, self).__init__()
        self.conn = conn
        self.year = 2019
        self.month = 20
        self.day = 2
        self.event = None

    def on_pre_enter(self):
        self.year = self.parent.year
        self.month = self.parent.month
        self.day = self.parent.day
        self.year_label.text = str(self.year)
        self.month_label.text = (calendar[str(self.month)])[0]
        self.title.text = ""
        self.description.text = ""
        self.event = self.parent.event
        if self.event is not None:
            self.load_event()


    def go_back(self):
        self.parent.change_screen("event_list")

    def save_event(self):
        title = self.title.text
        descript = self.description.text
        if self.event is None:
            query = """ INSERT INTO Events(title, descript, date)
                  VALUES('{}', '{}', {:02}-{:02}-{:02}) """.format(
                title, descript, self.day, self.month, self.year
            )
        else:
            query = """UPDATE Events
                    SET title = '{}', descript = '{}'
                    WHERE Events.id == {}""".format(title, descript, self.event)
            self.parent.event = None
        c = self.conn.cursor()
        c.execute(query)
        self.conn.commit()
        self.go_back()

    def load_event(self):
        c = self.conn.cursor()
        query = "SELECT * FROM Events WHERE Events.id == {} ".format(self.event)
        c.execute(query)
        rows = c.fetchall()
        self.title.text = rows[0][1]
        self.description.text = rows[0][2]

class Mybutton(ButtonBehavior):
    pass