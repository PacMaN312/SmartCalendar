# calendar_gui.py (версія 2)
import tkinter as tk
from tkinter import messagebox, simpledialog
import calendar
import datetime
from models import User, CalendarModel, Event
from storage import load_events, save_events

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Календар")

        self.user = User(1, "User", "user@mail.com")
        self.calendar = CalendarModel(1, "Main Calendar")

        # Завантаження подій із JSON
        for ev in load_events():
            self.calendar.addEvent(ev)

        self.today = datetime.date.today()
        self.current_year = self.today.year
        self.current_month = self.today.month

        self.build_ui()
        self.draw_calendar()

    def build_ui(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

        self.prev_btn = tk.Button(top_frame, text="<", command=self.prev_month)
        self.prev_btn.grid(row=0, column=0)

        self.month_label = tk.Label(top_frame, font=("Arial", 16))
        self.month_label.grid(row=0, column=1, padx=20)

        self.next_btn = tk.Button(top_frame, text=">", command=self.next_month)
        self.next_btn.grid(row=0, column=2)

        self.calendar_frame = tk.Frame(self.root)
        self.calendar_frame.pack()

        self.details_frame = tk.LabelFrame(self.root, text="Деталі події", padx=10, pady=10)
        self.details_frame.pack(fill="both", expand=True, pady=10)

        self.details_text = tk.Label(self.details_frame, text="Оберіть день або подію.", justify="left", anchor="nw")
        self.details_text.pack(fill="both", expand=True)

    def draw_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        self.month_label.config(text=f"{calendar.month_name[self.current_month]} {self.current_year}")

        week_days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]
        for i, day in enumerate(week_days):
            tk.Label(self.calendar_frame, text=day, width=10).grid(row=0, column=i)

        month_days = calendar.monthcalendar(self.current_year, self.current_month)

        for row, week in enumerate(month_days, start=1):
            for col, day in enumerate(week):
                if day == 0:
                    continue

                date_str = f"{self.current_year}-{self.current_month:02}-{day:02}"
                events = self.calendar.getEventsByDate(date_str)

                btn_text = str(day)
                if events:
                    btn_text += " ●"

                btn = tk.Button(self.calendar_frame, text=btn_text, width=10, height=3,
                                command=lambda d=date_str: self.show_day_events(d))

                if (self.current_year, self.current_month, day) == (self.today.year, self.today.month, self.today.day):
                    btn.config(bg="#a2d2ff")  # підсвічування поточного дня

                btn.grid(row=row, column=col, padx=2, pady=2)

    def next_month(self):
        self.current_month += 1
        if self.current_month == 13:
            self.current_month = 1
            self.current_year += 1
        self.draw_calendar()

    def prev_month(self):
        self.current_month -= 1
        if self.current_month == 0:
            self.current_month = 12
            self.current_year -= 1
        self.draw_calendar()

    # --- Етап 4: додавання та перегляд подій ---
    def show_day_events(self, date):
        events = self.calendar.getEventsByDate(date)

        text = f"Дата: {date}\n\nПодії:\n"
        if not events:
            text += "— Немає подій —\n"
        else:
            for ev in events:
                text += f"[{ev.id}] {ev.title}\n"

        self.details_text.config(text=text)

        for widget in self.details_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()

        tk.Button(self.details_frame, text="Додати подію", command=lambda: self.add_event(date)).pack(pady=5)

        if events:
            for ev in events:
                tk.Button(self.details_frame, text=f"Відкрити: {ev.title}",
                          command=lambda e=ev: self.open_event(e)).pack(pady=3)

    def add_event(self, date):
        title = simpledialog.askstring("Назва", "Назва події:")
        if not title: return
        description = simpledialog.askstring("Опис", "Опис події:")

        new_id = len(self.calendar.listOfEvents) + 1
        ev = Event(new_id, title, description, date)
        self.calendar.addEvent(ev)
        save_events(self.calendar.listOfEvents)

        self.draw_calendar()
        self.show_day_events(date)

    def open_event(self, event):
        text = f"Подія #{event.id}\n\nНазва: {event.title}\n\nОпис:\n{event.description}"
        self.details_text.config(text=text)

# продовження CalendarApp з Етапу 4
    def open_event(self, event):
        text = f"Подія #{event.id}\n\nНазва: {event.title}\n\nОпис:\n{event.description}"
        self.details_text.config(text=text)

        for widget in self.details_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()

        tk.Button(self.details_frame, text="Редагувати", command=lambda: self.edit_event(event)).pack(pady=5)
        tk.Button(self.details_frame, text="Видалити", command=lambda: self.delete_event(event)).pack(pady=5)

    def edit_event(self, event):
        new_title = simpledialog.askstring("Нова назва", "Введіть:", initialvalue=event.title)
        if not new_title: return
        new_desc = simpledialog.askstring("Новий опис", "Введіть:", initialvalue=event.description)

        event.editEvent(new_title, new_desc)
        save_events(self.calendar.listOfEvents)

        self.open_event(event)
        self.draw_calendar()

    def delete_event(self, event):
        if not messagebox.askyesno("Підтвердження", "Видалити подію?"):
            return
        self.calendar.removeEvent(event)
        save_events(self.calendar.listOfEvents)

        self.draw_calendar()
        self.show_day_events(event.startDate)
