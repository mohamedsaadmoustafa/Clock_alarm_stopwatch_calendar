from tkinter import *
from tkinter import ttk
import datetime, time
from tkcalendar import Calendar
import winsound
from threading import *

class App(Tk): # self represent TK
    def __init__(self):
        super().__init__()
        # root window
        self.title("Digital Clock")
        self.geometry("400x400")
        self.resizable(False, False)
        self.style = ttk.Style(self)
        self.style.theme_create(
            "dummy",
            parent = "alt",
            settings = {
                "TNotebook":
                    {
                        "configure": {
                            "tabmargins": [2, 5, 2, 0]
                        }
                    },
                "TNotebook.Tab": {
                    "configure": {
                        "padding": [5, 1],
                        "background": "#DCF0F2"
                    },
                    "map": {
                        "background": [("selected", "#F2C84B")],
                        "expand": [("selected", [1, 1, 1, 0])]
                    }
                }
            }
        )
        self.style.theme_use("dummy") # clam
        # alarm sounf name
        self.alarm_name: str = "rooster-crowing-in-the-morning.wav"
        # create tabs
        self.tabControl = ttk.Notebook(self)
        self.clock_tab = Frame(self.tabControl)
        self.alarm_tab = Frame(self.tabControl)
        self.stopwatch_tab = Frame(self.tabControl)
        self.calender_tab = Frame(self.tabControl)

        # Backgrount for every tab
        self.clock_tab.config(
            bg = clock_tab_bg,
            #fg = "#ff0",
        )
        self.alarm_tab.config(
            bg = alarm_tab_bg,
            #fg="#ff0",
        )
        self.stopwatch_tab.config(
            bg = stopwatch_tab_bg,
            #fg="#ff0",
        )
        self.calender_tab.config(
            bg = calender_tab_bg,
            #fg="#ff0",
        )
        #
        self.tabControl.add(self.clock_tab, text="Clock")
        self.tabControl.add(self.alarm_tab, text="Alarm")
        self.tabControl.add(self.stopwatch_tab, text="StopWatch")
        self.tabControl.add(self.calender_tab, text="Calender")
        self.tabControl.pack(expand=1, fill="both")

        self.showClock()
        self.showAlarm()
        self.showStopWatch()
        self.showCalender()

    """  Tab 1: Clock  """
    def showClock(self):
        """  Diasplay digital clock and date  """
        current_time: str = datetime.datetime.now().strftime("%H:%M:%S")
        current_date: str = datetime.date.today().strftime("%d, %b %Y")
        # Run in GUI
        clock_label1 = Label(self.clock_tab, text=current_time)
        clock_label1.after(1000, self.showClock)
        clock_label2 = Label(self.clock_tab, text = current_date)

        clock_label1.place(x=50, y=80)
        clock_label2.place(x=40, y=200)

        clock_label1.config(
            bg = clock_tab_bg,
            fg = '#fff',
            font=("Helvetica", 55),
        )
        clock_label2.config(
            bg = clock_tab_bg,
            fg = '#fff',
            font=("Helvetica", 45),
        )

    """  Tab 2: Alarm  """
    def AlarmThreading(self):
        t1 = Thread(target=self.Alarm)
        t1.start()

    def runAlarmSound(self):
        winsound.PlaySound(self.alarm_name, winsound.SND_ASYNC)

    def Alarm(self):
        wait_alarm = True
        while wait_alarm:  # wait_alarm:
            time.sleep(1)  # check every 20 second
            time_now = datetime.datetime.now()
            if time_now.hour == hourVar.get() and time_now.minute == minVar.get():
                self.runAlarmSound()
                wait_alarm = False

    def showAlarm(self):
        """ Set an alarm """
        hourLabel = Label(self.alarm_tab, text="Hours: ")
        hourLabel.place(x=20, y=20)
        minLabel = Label(self.alarm_tab, text="Minutes: ")
        minLabel.place(x=20, y=100)

        global hourVar, minVar
        hourVar, minVar = IntVar(), IntVar()
        hourTime = Scale( self.alarm_tab, variable=hourVar, from_=0, to=23, orient=HORIZONTAL, sliderlength=30, length=200)
        hourTime.place(x=170, y=20)
        minTime = Scale(self.alarm_tab, variable=minVar, from_=0, to=59, orient=HORIZONTAL, sliderlength=30, length=200)
        minTime.place(x=170, y=100)
        submit = Button(self.alarm_tab, text="Set Alarm", command=self.AlarmThreading )
        submit.place(x=150, y=200)

        hourLabel.config(
            bg = alarm_tab_bg,
            fg = '#fff',
            font=("Helvetica", 25),
        )
        minLabel.config(
            bg = alarm_tab_bg,
            fg = '#fff',
            font=("Helvetica", 25),
        )
        hourTime.config(
            bg = "#32CD32",
            fg = '#fff',
            font=("Helvetica", 15),
            troughcolor='#fff'
        )
        minTime.config(
            bg = "#32CD32",
            fg = '#fff',
            font=("Helvetica", 15),
            troughcolor='#fff'
        )
        submit.config(
            bg = "#9ACD32",
            fg = '#fff',
            font=("Helvetica", 15),
        )

    """  Tab 3: StopWatch  """
    def devideSeconds(self, seconds):
        """  Convert Seeconds to hours, minutes and seconds  """
        # count start with zero so add an additional selcond
        minutes = seconds // 60
        seconds %= 60
        hours = minutes // 60
        minutes %= 60
        return f"{int(hours)} : {int(minutes)} : {seconds}"

    def showStopWatch(self):
        """ """
        global stopwatch_counter, still_running
        stopwatch_counter, still_running = 0, False

        def counter_label(counterLabel):
            def count():
                if still_running:
                    global stopwatch_counter
                    if not stopwatch_counter: display = "0 : 0 : 0"
                    else: display = self.devideSeconds(stopwatch_counter)  # convert seconds to h:m:s format
                    # update counter Label
                    counterLabel["text"] = display
                    counterLabel.after(1000, count)
                    # increase counter by 1 every second
                    stopwatch_counter += 1
            count()

        def StartTimer(counterLabel):
            global still_running
            still_running = True
            counter_label(counterLabel)
            start_btn["state"], stop_btn["state"], reset_btn["state"] = ("disabled", "normal", "normal")

        def StopTimer():
            global still_running
            still_running = False
            start_btn["state"], stop_btn["state"], reset_btn["state"] = ("normal", "disabled", "normal")

        def ResetTimer(counterLabel):
            global stopwatch_counter
            stopwatch_counter = 0
            if not still_running:
                reset_btn["state"], counterLabel["text"] = "disabled", "0 : 0 : 0"

        # add label  to show timer 0 : 0 : 0
        counterLabel = Label(self.stopwatch_tab, text="0 : 0 : 0")
        start_btn = Button(self.stopwatch_tab, text="Start", command=lambda: StartTimer(counterLabel))
        stop_btn = Button(self.stopwatch_tab, text="Stop", state="disabled", command=StopTimer)
        reset_btn = Button(self.stopwatch_tab, text="Reset", state="disabled", command=lambda: ResetTimer(counterLabel))
        # gui componnents place
        counterLabel.place(x=200, y=100, anchor="center")
        start_btn.place(x=100, y=200, anchor="center")
        stop_btn.place(x=200, y=200, anchor="center")
        reset_btn.place(x=300, y=200, anchor="center")
        #
        counterLabel.config(
            bg = stopwatch_tab_bg,
            fg = '#fff',
            font = ("Helvetica", 40),
        )
        start_btn.config(
            bg = "#FFDF00",
            fg = '#fff',
            font=("Helvetica", 15),
        )
        stop_btn.config(
            bg = "#FFDF00",
            fg = '#fff',
            font=("Helvetica", 15),
        )
        reset_btn.config(
            bg = "#D4AF37",
            fg = '#fff',
            font=("Helvetica", 15),
        )
    """  Tab 4: Calender  """
    def showCalender(self):
        """ """
        current_date = datetime.date.today()
        current_date_str: str = datetime.date.today().strftime("%d, %b %Y")
        # creating a calender object
        calendar_value = StringVar(self.calender_tab, current_date_str)
        cal = Calendar(
            self.calender_tab,
            selectmode = "day",
            font = "Helvetica 15",
            year = current_date.year,
            month = current_date.month,
            date = current_date.day,
            firstweekday = "sunday",
            date_pattern = "dd-mm-yyyy",
            textvariable = calendar_value,
        )
        cal.grid(sticky='nsew', pady=20, padx=15)
        cal.configure(
            background = calender_tab_bg,
            foreground = '#fff',
            bordercolor = calender_tab_bg,
            headersbackground = calender_tab_bg,
            headersforeground = '#fff',
            selectbackground = '#fff',
            selectforeground = calender_tab_bg,
            normalbackground = calender_tab_bg,
            normalforeground = "#fff",
            weekendbackground = "#C33085",
            weekendforeground = "#fff",
            othermonthbackground = "#edbad8",
            othermonthforeground = "#fff",
            othermonthwebackground = "#edbad8",
            othermonthweforeground = "#fff",
        )

        dynamic_label = Label(self.calender_tab, textvariable = calendar_value)
        dynamic_label.grid(sticky='nsew', pady=10, padx=0)
        dynamic_label.config(
            text = f"{current_date_str}",
            #bg = "#F2C84B",
            bg = calender_tab_bg,
            fg = "#fff",
            font = ("Helvetica", 18),
        )

if __name__ == "__main__":
    clock_tab_bg = "#088F8F"  # "#7393B3"
    alarm_tab_bg = "#90EE90"
    stopwatch_tab_bg = "#E6BE8A"
    calender_tab_bg = "#822058"


    app = App()
    app.mainloop()
