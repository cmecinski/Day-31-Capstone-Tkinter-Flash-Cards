from tkinter import *
import random
import pandas

# ---------------------------- CONSTANTS ------------------------------- #

BACKGROUND_COLOR = "#B1DDC6"
WHITE = "#FFFFFF"
to_learn = {}
current_card = {}

# ---------------------------- DATA ------------------------------- #
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


# print(word)
# print(word["French"].values)
# print(word["English"].values)

# ---------------------------- NEW WORD FUNCTION ------------------------------- #


def new_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(canvas_image, image=flash_front_img)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    flip_timer = window.after(3000, func=flip_card)


def is_known():
    # global current_card
    to_learn.remove(current_card)
    data_known = pandas.DataFrame(to_learn)
    data_known.to_csv("data/words_to_learn.csv", index=False)
    new_card()

# ---------------------------- FLIP CARD FUNCTION ------------------------------- #


def flip_card():
    canvas.itemconfig(canvas_image, image=flash_back_img)
    canvas.itemconfig(card_title, fill=WHITE)
    canvas.itemconfig(card_word, fill=WHITE)
    canvas.itemconfig(card_title, text="English")
    canvas.itemconfig(card_word, text=current_card["English"])


# ---------------------------- UI ------------------------------- #

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# Flash Card

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
flash_front_img = PhotoImage(file="images/card_front.png")
flash_back_img = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=flash_front_img)

card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

canvas.grid(column=0,row=0, columnspan=2)

# Buttons

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, command=new_card, highlightthickness=0, bg=BACKGROUND_COLOR)
wrong_button.grid(column=0, row=1)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, command=is_known, highlightthickness=0, bg=BACKGROUND_COLOR)
right_button.grid(column=1, row=1)


new_card()
window.mainloop()