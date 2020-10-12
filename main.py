from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from datetime import date

from views import CalendarView, AddEventView, EventListView
from calendar_db import create_connection


class ViewManager(ScreenManager):
    day, month, year, event = 0, 0, 0, None

    def __init__(self, conn):
        super(ViewManager, self).__init__()
        dt = date.today()
        self.conn = conn
        self.day = dt.day
        self.month = dt.month
        self.year = dt.year
        self.add_widget(CalendarView(day=self.day, month=self.month, year=self.year))
        self.add_widget(AddEventView(conn=self.conn))
        self.add_widget(EventListView(conn=self.conn))
        self.change_screen(name="calendar")
        del dt

    def change_screen(self, name, **kwargs):
        self.current = name


class CalendarApp(App):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn

    def build(self):
        return ViewManager(conn=self.conn)


if __name__ == "__main__":
    conn = create_connection("cal.db")
    if conn:
        CalendarApp(conn=conn).run()
    conn.close()
