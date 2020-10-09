from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput

from datetime import date

from views import CalendarView
from calendar_db import create_connection

class CalendarApp(App):
    def build(self):
        dt = date.today()
        day = dt.day
        month = dt.month
        year = dt.year
        calendar = CalendarView(day=day, month=month, year=year)
        del day, year, month
        return calendar

if __name__ == "__main__":
    conn = create_connection("cal.db")
    if conn:
        CalendarApp().run()
    conn.close()