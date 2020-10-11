from datetime import date, datetime

from kivy.uix.button import Button
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
                    on_press=lambda d=m_day: self.add_event(d),
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
    def __init__(self, conn, **kwargs):
        super(EventListView, self).__init__()
        self.conn = conn
        self.year = 2019
        self.month = 20
        self.day = 2

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
            child_grid.add_widget(Button(text="Edit"))
            child_grid.add_widget(
                Button(text="Delete", on_press=lambda id=row[0]: self.delete_event(id))
            )
            self.event_list_grid.add_widget(child_grid)

    def delete_event(self, id):
        c = self.conn.cursor()
        print(id.on_press)
        """
        query = "DELETE FROM Events WHERE Events.id == {} ".format(id)
        c.execute(query)
        self.conn.commit()
        """
        self.parent.change_screen("event_list")

    def events_query(self):
        c = self.conn.cursor()
        query = "SELECT * FROM Events WHERE Events.date == {:02}-{:02}-{:02} ORDER BY 'date'".format(
            self.day, self.month, self.year
        )
        c.execute(query)
        rows = c.fetchall()
        return rows


class AddEventView(Screen):
    def __init__(self, conn, **kwargs):
        super(AddEventView, self).__init__()
        self.conn = conn
        self.year = 2019
        self.month = 20
        self.day = 2

    def on_pre_enter(self):
        self.year = self.parent.year
        self.month = self.parent.month
        self.day = self.parent.day
        self.year_label.text = str(self.year)
        self.month_label.text = (calendar[str(self.month)])[0]

    def go_back(self):
        self.parent.change_screen("event_list")

    def save_event(self):
        title = self.title.text
        descript = self.description.text
        query = """ INSERT INTO Events(title, descript, date)
              VALUES('{}', '{}', {:02}-{:02}-{:02}) """.format(
            title, descript, self.day, self.month, self.year
        )
        print(query)
        c = self.conn.cursor()
        c.execute(query)
        self.conn.commit()
        self.go_back()
