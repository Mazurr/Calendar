import calendar as cl
import calendar_db as cl_db

if __name__ == '__main__':
    conn = cl_db.create_connection('cal.db')
    if conn:
        app = cl.Calendar()
        app.window.mainloop()
    cl_db.close_connection(conn)