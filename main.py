import tkinter.messagebox
from tkinter import *
from tkinter import ttk
import pandas
import random
import os
import time
from data_manager import DataManager

#Try to open the local data if no file found then fetch the data from Sheety
# Access the categories sheets and load the name of the other sheets
# Assign the name of all sheets to the tuple TOPIC
TOPIC = ()
data_manager = DataManager()

try:
    data_read_from_file = pandas.read_csv("data/sheet-name.csv")
except FileNotFoundError:
    sheets_name_from_sheety = data_manager.get_sheets_data()
    for row in sheets_name_from_sheety:
        TOPIC = TOPIC + (row["categoriesName"],)
    data_frame = pandas.DataFrame(sheets_name_from_sheety)
    data_frame.to_csv("data/sheet-name.csv", index=False)
else:
    for index, row in data_read_from_file.iterrows():
        TOPIC = TOPIC + (row["categoriesName"],)

# Access the detail data of each sheet and save the data to csv file
for name in TOPIC:
    temp_sheet_name = name
    temp_sheet_name = temp_sheet_name[0].lower() + temp_sheet_name[1:]

    # check if file already esisted!
    file_to_check = f"data/{temp_sheet_name}.csv"
    if os.path.exists(file_to_check):
        pass
    else:
        sheet_detail_data = data_manager.get_detail_data(temp_sheet_name)
        df = pandas.DataFrame(sheet_detail_data)
        df.to_csv(f"data/{temp_sheet_name}.csv", index=False)
print(TOPIC)

current_card = {}
to_learn = {}

def load_data(file_name):
    global to_learn
    file_to_load = f"data/{file_name}.csv"
    loaded_data = pandas.read_csv(file_to_load)
    to_learn = loaded_data.to_dict(orient="records")
def next_card():
    global current_card
    global to_learn
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_word, text=current_card["wörter"], fill="black")

    canvas.itemconfig(card_word_des, text=current_card["english"])
    canvas.itemconfig(card_background, image=card_front_img)
    canvas.itemconfig(card_word_note, text=f"{len(to_learn)}")

def btn_callback_f(text):

    if text == current_card["artikel"]:
        print(text)
        print(current_card["wörter"])
        print(f"{len(to_learn)} need to learn")

        if len(to_learn) > 1:
            to_learn.remove(current_card)
            data = pandas.DataFrame(to_learn)
            data.to_csv("data/words_to_learn.csv")
            next_card()
        else:
            done_then_reload()
    else:
        canvas.itemconfig(card_word, fill="red")
        canvas.itemconfig(card_background, image= card_back_img)

def done_then_reload():
    if tkinter.messagebox.askokcancel(title="Congratulation!",
                                      message="Welldone! You learn all words,\n Press OK to learn it again!"):
        os.remove("data/words_to_learn.csv")
        print("Deleteted learnt file")
        load_data(random.choice(TOPIC))
        next_card()
    else:
        canvas.itemconfig(card_word, text="CONGRATULATION!", fill="green")

def cate_changed(event):
    load_data(selected_category.get())
    next_card()
    #print(selected_category.get())


##VIEWCONTROLLER
BACKGROUND_COLOR = "#B1DDC6"
window = Tk()
window.title("DER-DIE-DAS")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)

card_word = canvas.create_text(400, 263, text="Word", font=("Ariel", 80, "bold"))
card_word_des = canvas.create_text(400, 310, text="Word", font=("Ariel", 28, "italic"), fill="#FF3FA4")
card_word_note = canvas.create_text(700, 20, text="Word", font=("Ariel", 18, "italic"), fill="#FF3FA4")
canvas.config(background=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=1, column=0, columnspan=3)

der_button = Button(text="der", font=("Ariel", 40, "italic"), command=lambda: btn_callback_f("der"))
der_button.grid(row=2, column=0)

die_button = Button(text="die", bg="green", font=("Ariel", 40, "italic"), command=lambda: btn_callback_f("die"))
die_button.grid(row=2, column=1)

das_button = Button(text="das", bg="blue", font=("Ariel", 40, "italic"), command=lambda: btn_callback_f("das"))
das_button.grid(row=2, column=2)

#
# To craete combo box
selected_category = StringVar()
cb_category = ttk.Combobox(window, textvariable=selected_category)
cb_category.grid(row=0, column=0, columnspan=1)

style = ttk.Style()
style.theme_use('clam')
style.configure("TCombobox", fieldbackground="grey", padding=10)
# style.map('TCombobox', arrowcolor=[
#     ('disabled', 'gray'),
#     ('pressed !disabled', 'blue'),
#     ('focus !disabled', 'green'),
#     ('hover !disabled', 'yellow')])

cb_category['values'] = TOPIC
cb_category.bind('<<ComboboxSelected>>', cate_changed)

random_cate = random.choice(TOPIC)
load_data(random_cate)
next_card()

window.mainloop()
