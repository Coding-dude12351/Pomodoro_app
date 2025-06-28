import tkinter as tk
from  tkinter import messagebox
import time 
import winsound

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate pomodoro Timer")
        self.root.geometry("400x450")
        self.root.resizable(False,False)
        
        # STATE
        self.is_running = False
        self.is_break = False
        self.time_left = 0
        self.sessions_completed = 0
        self.is_dark_mode =False
        self.WORK_MIN = 25
        self.BREAK_MIN= 5
        self.history_file = "pomodoro_history.txt"
        self.quotes = ["keep going, you got this!", 
                       "stay focused, stay sharp.",
                       "Greatness takes time.", 
                       "One pomodoro at a time!",
                       ]
        # TASK ENTRY
        self.task_label = tk.Label(root, text = "Enter your task:")
        self.task_label.pack(pady=3)
        self.task_entry = tk.Entry(root, width=30)
        self.task_entry.pack()
        
        # CUSTOM SESSION DURATIONS
        self.work_time_label = tk.Label(root, text= "work (mins):")
        self.work_time_label.pack()
        self.work_time_entry = tk.Entry(root)
        self.work_time_entry.insert(0, "25")
        self.work_time_entry.pack()
        
        self.break_time_label = tk.Label(root, text="Break (mins)")
        self.break_time_label.pack()
        self.break_time_entry = tk.Entry(root)
        self.break_time_entry.insert(0, "5")
        self.break_time_entry.pack()
        
        # DISPLAY
        
        self.status_label = tk.Label(root, text = "Ready", font=("Helvetica", 16))
        self.status_label.pack(pady = 10)
        self.timer_display = tk.Label(root, text = "00:00", font = ("Helvetica", 36))
        self.timer_display.pack()
        
        self.session_counter = tk.Label(root, text ="sessions completed; 0")
        self.session_counter.pack()
        
        # BUTTONS
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady = 10)
        
        self.start_button = tk.Button(btn_frame,text="start", command=self.start_timer)
        self.start_button.grid(row=0,column=0,padx=10)
        self.reset_button = tk.Button(btn_frame, text="Reset",command=self.reset_timer)
        self.reset_button.grid(row=0,column=1,padx=10)
        self.theme_button = tk.Button(root, text="Toggle Theme",command=self.toggle_theme)
        self.theme_button.pack()
        
        self.update_timer()
        self.apply_theme()

    def start_timer(self):
        if not self.is_running:
            if not self.task_entry.get():
                messagebox.showinfo("Task Required", "Please enter a task to work on.")
                return
            try:
                self.WORK_MIN = int(self.work_time_entry.get())
                self.BREAK_MIN = int(self.break_time_entry.get())
                self.time_left = self.WORK_MIN * 60
            except ValueError:
                messagebox.showerror("Invalid Input", "Enter valid numbers for time.")
                return

            import random
            quote = random.choice(self.quotes)
            self.status_label.config(text=f"{quote}\nWork: {self.task_entry.get()}")
            self.is_running = True
            self.update_timer()

    def reset_timer(self):
        self.is_running = False
        self.is_break = False
        self.time_left = 0
        self.status_label.config(text="Ready")
        self.timer_display.config(text="00:00")
        self.session_counter.config(text="sessions completed: 0")

    def update_timer(self):
        mins, secs = divmod(self.time_left, 60)
        self.timer_display.config(text=f"{mins:02d}:{secs:02d}")

        if self.is_running:
            if self.time_left > 0:
                self.time_left -= 1
                self.root.after(1000, self.update_timer)
            else:
                winsound.Beep(1000, 500)  # Replace with playsound for other platforms
                if self.is_break:
                    self.sessions_completed += 1
                    self.session_counter.config(text=f"sessions completed: {self.sessions_completed}")
                    self.save_session_to_file()
                self.is_break = not self.is_break
                self.time_left = (self.BREAK_MIN if self.is_break else self.WORK_MIN) * 60
                status = "Break Time!" if self.is_break else f"Work: {self.task_entry.get()}"
                self.status_label.config(text=status)
                self.update_timer()

    def save_session_to_file(self):
        task = self.task_entry.get()
        with open(self.history_file, "a") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - completed: {task}\n")

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()

    def apply_theme(self):
        bg = "#222" if self.is_dark_mode else "#fff"
        fg = "#0f0" if self.is_dark_mode else "#000"
        self.root.configure(bg=bg)
        for widget in self.root.winfo_children():
            if isinstance(widget, (tk.Label, tk.Button, tk.Entry)):
                widget.configure(bg=bg, fg=fg)
                if isinstance(widget, tk.Entry):
                    widget.configure(insertbackground=fg)
            elif isinstance(widget, tk.Frame):
                widget.configure(bg=bg)


# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()




















