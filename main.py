from datetime import date
from views import CalendarView, AddEventsView, EventsListView
from tkinter import Tk, Frame
import calendar_db as cl_db

class Views(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, *kwargs)
        self.current_view = None
        day = date.today().day
        month = date.today().month
        year = date.today().year
        self.conn = kwargs['conn']
        self.view = {}
        self.view["calendar_view"] = CalendarView
        self.view["add_event_view"] = AddEventsView
        self.view["events_list_view"] = EventsListView
        
        self.show_view("calendar_view", day=day, month=month, year=year)
        del day, month, year

    def show_view(self, page_name, **kwargs):
        '''Show a view for the given view name'''
        new_view = self.view[page_name](self, day=kwargs['day'], month=kwargs['month'], year=kwargs['year'], conn=self.conn)
        
        if self.current_view is not None:
            self.current_view.destroy()

        self.current_view = new_view
        self.current_view.pack()

if __name__ == '__main__':
    conn = cl_db.create_connection('cal.db')
    if conn:
        app = Views(conn=conn)
        app.mainloop()
    conn.close()