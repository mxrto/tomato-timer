from tkinter import *
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None


# ----------------------------- DISABLE BUTTON ------------------------------- #
def disable_start_button():
    start_button["state"] = DISABLED


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global reps
    reps = 0

    window.after_cancel(timer)
    timer_label.config(text="Timer")
    check_label.config(text="")
    canvas.itemconfig(timer_text, text="00:00")

    start_button["state"] = NORMAL


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    reps += 1
    
    disable_start_button()

    if reps % 8 == 0:
        timer_label.config(text="Break", fg=RED)
        count_down(LONG_BREAK_MIN * 60)
    elif reps % 2 == 0:
        timer_label.config(text="Break", fg=PINK)
        count_down(SHORT_BREAK_MIN * 60)
    else:
        timer_label.config(text="Work", fg=GREEN)
        count_down(WORK_MIN * 60)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    # Count == seconds
    minutes = count // 60
    seconds = count % 60

    for n in range(0, 10):
        if seconds == n:
            seconds = f"0{n}"

    canvas.itemconfig(timer_text, text=f"{minutes}:{seconds}")
    if count > 0:
        # Loop
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        # add checkmarks for every successful session
        window.lift()
        window.attributes("-topmost", True)
        window.after_idle(window.attributes, "-topmost", False)

        start_timer()
        marks = ""
        for _ in range(reps//2):
            marks += "✓"
        check_label.config(text=marks)

        if reps % 2 == 0:
            # keep track of total sessions
            with open("total_sessions.txt") as file:
                total_session = file.read()

            total = int(total_session) + 1

            with open("total_sessions.txt", mode="w") as file:
                file.write(str(total))

            total_label.config(text=f"Completed tomatoes: {total}")


# ---------------------------- UI SETUP ------------------------------- #
# Window
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

# Canvas
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)

# Label
timer_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 35, "bold"))
timer_label.grid(row=0, column=1)

check_label = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 15, "bold"))
check_label.grid(row=3, column=1)

with open("total_sessions.txt") as file:
    total_sessions = file.read()

total_label = Label(text=f"Completed tomatoes: {total_sessions}", fg=PINK, bg=YELLOW, font=(FONT_NAME, 15, "bold"))
total_label.grid(row=4, column=1)

# Buttons
start_button = Button(text="Start", font=(FONT_NAME, 10, "bold"), bg=GREEN, highlightthickness=0, command=start_timer)
start_button.grid(row=2, column=0)

reset_button = Button(text="Reset", font=(FONT_NAME, 10, "bold"), bg=PINK, highlightthickness=0, command=reset_timer)
reset_button.grid(row=2, column=2)


window.mainloop()
