# -*- coding: utf-8 -*-
# !/usr/bin/python3

import tkinter as tk
from tkinter import ttk
from tkinter import font as tk_font

from pathlib import Path
import csv


PIN_LENGTH = 4
PASSWORD_LENGTH = 6

CSV_FOLDER = Path("CSV")


# PIN_ADMIN = "0998"
PIN_ADMIN = "0000"

cur_user = None
node_num = -1
admin_node_num = -1
admin_power_line_num = -1


class Node:

    def __init__(self, num=0):
        self.__num = num
        self.__power_applied = False

    def get_num(self):
        return self.__num

    def get_power_applied(self):
        return self.__power_applied

    def set_power_applied(self, power):
        self.__power_applied = power


class User:
    
    def __init__(self, num=0):
        self.__num = num
        self.__pin = None
        self.__node_num = 0

    def get_num(self):
        return self.__num

    def get_pin(self):
        return self.__pin

    def set_pin(self, pin):
        self.__pin = str(pin).zfill(PIN_LENGTH)

    def get_node_num(self):
        return self.__node_num

    def set_node_num(self, node_number):
        self.__node_num = node_number

    def pin_ok(self, pin):
        if self.__pin is None:
            return False
        else:
            return self.__pin == pin


class Users:
    def __init__(self, path=CSV_FOLDER / "user_test.csv"):
        self.__users = self.__read_csv(path)

    def get_users(self):
        return self.__users

    def set_users(self, users_init):
        self.__users = users_init

    def get_user_by_pin(self, pin):
        for user in self.__users:
            if user.get_pin() == pin:
                return user
        return None

    @staticmethod
    def __read_csv(path):
        read_users = list()
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            row_count = 0
            for row in csv_reader:
                column_count = 0
                for column in row:
                    if row_count > 0:
                        if column_count == 0:
                            new_user = User(int(column))
                        elif column_count == 1:
                            new_user.set_pin(column)
                        elif column_count == 2:
                            new_user.set_node_num(int(column))
                        read_users.append(new_user)
                    column_count += 1
                row_count += 1
        return read_users


# noinspection PyUnusedLocal
def switch_to_full_screen(event):
    root.attributes("-fullscreen", True)


# noinspection PyUnusedLocal
def switch_from_full_screen(event):
    root.attributes("-fullscreen", False)


def time_event_gen():
    global frame_num
    if frame_num == 4:
        frame_4.event_generate('<<time_event>>', when='tail')


# noinspection PyUnusedLocal
def to_thirty_seven_admin(event):
    global frame_num
    frame_a_33.pack_forget()
    frame_num = 1037
    frame_a_37.pack(fill="both", expand=True)
    entry_a_37_10.focus_set()
    entry_a_37_10.select_range(0, tk.END)


# noinspection PyUnusedLocal
def to_thirty_three_admin(event):
    global frame_num
    if frame_num == 1031:
        frame_a_31.pack_forget()
    if frame_num == 1032:
        frame_a_32.pack_forget()
    frame_num = 1033
    frame_a_33.pack(fill="both", expand=True)
    frame_a_33.focus_set()


# noinspection PyUnusedLocal
def to_thirty_two_admin(event):
    global frame_num
    frame_a_31.pack_forget()
    frame_num = 1032
    frame_a_32.pack(fill="both", expand=True)
    name_admin_node_num.set('')
    entry_a_32.focus_set()


# noinspection PyUnusedLocal
def to_thirty_one_admin(event):
    global frame_num
    if frame_num == 103:
        frame_a_3.pack_forget()
    if frame_num == 1032:
        frame_a_32.pack_forget()
    if frame_num == 1033:
        frame_a_33.pack_forget()
    if frame_num == 1037:
        frame_a_37.pack_forget()
    frame_num = 1031
    frame_a_31.pack(fill="both", expand=True)
    name_admin_node_num.set('')
    entry_a_31.focus_set()


# noinspection PyUnusedLocal
def to_third_admin(event):
    global frame_num
    frame_a_2.pack_forget()
    frame_num = 103
    frame_a_3.pack(fill="both", expand=True)
    frame_a_3.focus_set()


# noinspection PyUnusedLocal
def to_second_admin(event):
    global frame_num
    if frame_num == 101:
        frame_a_1.pack_forget()
    elif frame_num == 103:
        frame_a_3.pack_forget()
    elif frame_num == 1031:
        frame_a_31.pack_forget()
    frame_num = 102
    frame_a_2.pack(fill="both", expand=True)
    frame_a_2.focus_set()


# noinspection PyUnusedLocal
def to_first_admin(event):
    global frame_num
    frame_1.pack_forget()
    frame_num = 101
    name_pass.set('')
    frame_a_1.pack(fill="both", expand=True)
    entry_a_1.focus_set()


# noinspection PyUnusedLocal
def to_fourth_screen(event):
    global frame_num
    frame_num = 4
    frame_3.pack_forget()
    frame_4.pack(fill="both", expand=True)
    frame_4.focus_set()
    frame_4.after(5000, time_event_gen)


# noinspection PyUnusedLocal
def to_third_screen(event):
    global frame_num
    frame_num = 3
    frame_2.pack_forget()
    label_3_0.configure(text="Charger #" + str(node_num) + " selected")
    frame_3.pack(fill="both", expand=True)
    frame_3.focus_set()


# noinspection PyUnusedLocal
def to_second_screen(event):
    global frame_num
    if frame_num == 1:
        frame_1.pack_forget()
    if frame_num == 3:
        frame_3.pack_forget()
    frame_num = 2
    frame_2.pack(fill="both", expand=True)
    name_node_num.set(node_num)
    entry_2_1_2.focus_set()
    entry_2_1_2.select_range(0, tk.END)


# noinspection PyUnusedLocal
def to_first_screen(event):
    global frame_num
    frame_num = 1
    frame_0.pack_forget()
    frame_1.pack(fill="both", expand=True)
    entry_1.focus_set()


# noinspection PyUnusedLocal
def to_zero_screen(event):
    global frame_num
    if frame_num == 1:
        frame_1.pack_forget()
    elif frame_num == 2:
        frame_2.pack_forget()
    elif frame_num == 3:
        frame_3.pack_forget()
    elif frame_num == 4:
        frame_4.pack_forget()
    elif frame_num == 101:
        frame_a_1.pack_forget()
    elif frame_num == 102:
        frame_a_2.pack_forget()
    elif frame_num == 103:
        frame_a_3.pack_forget()
    elif frame_num == 1031:
        frame_a_31.pack_forget()
    elif frame_num == 1032:
        frame_a_32.pack_forget()
    elif frame_num == 1033:
        frame_a_33.pack_forget()
    elif frame_num == 1037:
        frame_a_37.pack_forget()
    frame_num = 0
    name_pin.set('')
    frame_0.pack(fill="both", expand=True)
    frame_0.focus_set()


root = tk.Tk()

root.wm_title("PCPH  HUB")
# root.geometry("1024x600")
root.geometry("800x600")
root.minsize(800, 600)
root.configure(bg="#3838B8")
root.attributes("-fullscreen", True)


name_pin = tk.StringVar()
name_pass = tk.StringVar()

name_node_num = tk.StringVar(root, value=node_num)

name_admin_node_num = tk.StringVar(root, value=node_num)
name_admin_power_line_num = tk.StringVar()
name_admin_node_type = tk.StringVar()
name_admin_node_status = tk.StringVar()


color_front = "white"
color_back = "#3838B8"
color_entry_back = "#B8B8F8"

font_1 = tk_font.Font(family="Helvetica", size=128)
font_2 = tk_font.Font(family="Helvetica", size=24)
font_2_bold = tk_font.Font(family="Helvetica", size=24, weight="bold")
font_2c_bold = tk_font.Font(family="Courier", size=24, weight="bold")
font_3 = tk_font.Font(family="Helvetica", size=32)
font_3_bold = tk_font.Font(family="Helvetica", size=32, weight="bold")
font_4 = tk_font.Font(family="Helvetica", size=48)
font_4_bold = tk_font.Font(family="Helvetica", size=48, weight="bold")
font_5 = tk_font.Font(family="Helvetica", size=64)
font_6 = tk_font.Font(family="Helvetica", size=20)
font_6_bold = tk_font.Font(family="Helvetica", size=20, weight="bold")
font_7_bold = tk_font.Font(family="Helvetica", size=40, weight="bold")
font_8_bold = tk_font.Font(family="Helvetica", size=18, weight="bold")
font_9_bold = tk_font.Font(family="Helvetica", size=36, weight="bold")

frame_0 = tk.Frame(root, bg=color_back)


# noinspection PyUnusedLocal
def key_press(event):
    if event.char == event.keysym or len(event.char) == 1:
        to_first_screen(event)


frame_0.bind("<Key>", key_press)
frame_0.pack(fill="both", expand=True)
frame_0.focus_set()

label_0_1 = tk.Label(frame_0,
                     text="----------- PCPH -----------",
                     font=font_1,
                     fg=color_front,
                     bg=color_back)
label_0_1.place(relx=0.5, rely=0.5, anchor='c')

label_0_2 = tk.Label(frame_0,
                     text="Press any key to activate",
                     font=font_2,
                     fg=color_front,
                     bg=color_back)
label_0_2.place(relx=0.5, rely=0.85, anchor='n')


frame_1 = tk.Frame(root, bg=color_back)

font_1_1 = tk_font.Font(family="Verdana", size=48)
font_1_2 = tk_font.Font(family="Arial", size=64, weight="bold")

label_1 = tk.Label(frame_1, text="Enter " + str(PIN_LENGTH) + "-digit PIN",
                   font=font_1_1,
                   fg=color_front,
                   bg=color_back)
label_1.place(relx=0.5, rely=0.3, anchor="c")


def get_entry_1(event):
    global node_num
    global cur_user
    pin_entry = name_pin.get()
    if len(pin_entry) != PIN_LENGTH:
        name_pin.set('')
        return
    try:
        int(pin_entry)
    except ValueError:
        name_pin.set('')
        return
    cur_user = users.get_user_by_pin(pin_entry)
    if pin_entry == PIN_ADMIN:
        to_first_admin(event)
    if cur_user is None:
        name_pin.set('')
        return
    node_num = cur_user.get_node_num()
    to_second_screen(event)


entry_1 = tk.Entry(frame_1,
                   textvariable=name_pin,
                   font=font_1_2,
                   width=PIN_LENGTH,
                   bg=color_entry_back)
entry_1.bind("<Return>", get_entry_1)
entry_1.bind("<Escape>", to_zero_screen)
entry_1.place(relx=0.5, rely=0.5, anchor="c")
entry_1.focus_set()


label_2 = tk.Label(frame_1, text="Press Cancel to return",
                   font=font_2,
                   fg=color_front,
                   bg=color_back)
label_2.place(relx=0.5, rely=0.85, anchor="n")


frame_2 = tk.Frame(root, bg='white')


def clear_entry(event):
    if len(name_node_num.get()) == 0:
        to_zero_screen(event)
    else:
        entry_2_1_2.delete(0, tk.END)


frame_2_1 = tk.Frame(frame_2, bg='white')
frame_2_1.place(relwidth=1, relheight=0.8)

frame_2_2 = tk.Frame(frame_2, bg=color_back)
frame_2_2.place(rely=0.8, relwidth=1, relheight=0.2)

label_2_1_1 = tk.Label(frame_2_1,
                       text="Current rate per hour:",
                       font=font_3)
label_2_1_1.place(relx=0.35, rely=0.3, anchor='c')

label_2_1_2 = tk.Label(frame_2_1,
                       text="Please enter your \n charger number:",
                       font=font_3)
label_2_1_2.place(relx=0.35, rely=0.7, anchor='c')

button_2_1_1 = tk.Button(frame_2_1,
                         text="$0.183",
                         font=font_3)
button_2_1_1.place(relx=0.75, rely=0.3, anchor='c')


def get_entry(event):
    global node_num
    try:
        node_num = int(name_node_num.get())
        if node_num >= 0:
            to_third_screen(event)
        else:
            name_node_num.set('')
    except ValueError:
        name_node_num.set('')


entry_2_1_2 = tk.Entry(frame_2_1,
                       textvariable=name_node_num,
                       width=3,
                       font=font_3)
entry_2_1_2.bind('<Escape>', clear_entry)
entry_2_1_2.bind('<Return>', get_entry)
entry_2_1_2.place(relx=0.75, rely=0.7, anchor='c')

label_2_2 = tk.Label(frame_2_2,
                     text="Press Enter to select",
                     font=font_6_bold,
                     bg=color_back,
                     fg='white')
label_2_2.place(relx=0.5, rely=0.35, anchor='c')

label_2_3 = tk.Label(frame_2_2,
                     text="Press Cancel to cancel and exit",
                     font=font_6_bold,
                     bg=color_back,
                     fg='white')
label_2_3.place(relx=0.5, rely=0.65, anchor='c')


frame_3 = tk.Frame(root, bg=color_back)

frame_3.bind("<Escape>", to_second_screen)
frame_3.bind("<Return>", to_fourth_screen)
frame_3.focus_set()

label_3_0 = tk.Label(frame_3,
                     font=font_4,
                     fg=color_front,
                     bg=color_back)
label_3_0.place(relx=0.5, rely=0.4, anchor='n')

label_3_1 = tk.Label(frame_3, text="Press Enter to confirm and start charging",
                     font=font_6_bold,
                     fg=color_front,
                     bg=color_back)
label_3_1.place(relx=0.5, rely=0.84, anchor="n")

label_3_2 = tk.Label(frame_3, text="Press Cancel to cancel and exit",
                     font=font_6_bold,
                     fg=color_front,
                     bg=color_back)
label_3_2.place(relx=0.5, rely=0.9, anchor="n")

frame_4 = tk.Frame(root, bg=color_back)

frame_4.bind("<Escape>", to_zero_screen)
frame_4.bind("<<time_event>>", to_zero_screen)

label_4_1 = tk.Label(frame_4,
                     text="Charging Started",
                     font=font_5,
                     fg=color_front,
                     bg=color_back)
label_4_1.place(relx=0.5, rely=0.45, anchor='n')
                   
label_4_2 = tk.Label(frame_4, text="Press Cancel to return",
                     font=font_2,
                     fg=color_front,
                     bg=color_back)
label_4_2.place(relx=0.5, rely=0.85, anchor="n")


frame_a_1 = tk.Frame(root, bg=color_back)

font_a_1_1 = tk_font.Font(family="Verdana", size=48)
font_a_1_2 = tk_font.Font(family="Arial", size=64, weight="bold")

label_a_1 = tk.Label(frame_a_1,
                     text="Enter " + str(PASSWORD_LENGTH) + "-digit Password",
                     font=font_a_1_1,
                     fg=color_front,
                     bg=color_back)
label_a_1.place(relx=0.5, rely=0.3, anchor="c")


def get_entry_a_1(event):
    pin_entry = name_pass.get()
    if len(pin_entry) != PASSWORD_LENGTH:
        name_pass.set('')
        return
    try:
        int(pin_entry)
    except ValueError:
        name_pass.set('')
        return
    to_second_admin(event)


entry_a_1 = tk.Entry(frame_a_1,
                     textvariable=name_pass,
                     font=font_a_1_2,
                     width=PASSWORD_LENGTH,
                     bg=color_entry_back)
entry_a_1.bind("<Return>", get_entry_a_1)
entry_a_1.bind("<Escape>", to_zero_screen)
entry_a_1.place(relx=0.5, rely=0.5, anchor="c")
entry_a_1.focus_set()


frame_a_2 = tk.Frame(root, bg=color_back)


def key_press_a_2(event):
    if event.keysym == '1':
        to_third_admin(event)
    elif event.keysym == '2':
        to_third_admin(event)
    elif event.keysym == '3':
        to_third_admin(event)
    elif event.keysym == '4':
        to_third_admin(event)


frame_a_2.bind("<Escape>", to_zero_screen)
frame_a_2.bind("<Key>", key_press_a_2)

frame_a_2_1 = tk.Frame(frame_a_2, bg='white')
frame_a_2_1.place(relwidth=1, relheight=0.2)

label_a_2_1 = tk.Label(frame_a_2_1,
                       text="Administration and Setup Menu",
                       font=font_9_bold,
                       bg='white')
label_a_2_1.place(relx=0.5, rely=0.5, anchor='c')

frame_a_2_2 = tk.Frame(frame_a_2, bg='white')
frame_a_2_2.place(rely=0.2, relwidth=1, relheight=0.65)

labels_a_2_2 = []
pl_x1 = [0.18, 0.58]
pl_y1 = [0.3, 0.65]
pl_x2 = [0.2, 0.6]
pl_y2 = [0.3, 0.65]
tl = ["Infrastructure\nsetup",
      "Check setup",
      "Error log",
      "Ping Charger#"]
      
for l_column in range(2):
    for l_row in range(2):
        n = 2 * l_column + l_row
        labels_a_2_2.insert(0, tk.Label(frame_a_2_2,
                                        text=' ' + str(n + 1) + ' ',
                                        font=font_2,
                                        bg=color_back,
                                        fg=color_front))
        labels_a_2_2[0].place(relx=pl_x1[l_column],
                              rely=pl_y1[l_row],
                              anchor='e')
        labels_a_2_2.insert(0, tk.Label(frame_a_2_2,
                                        text=tl[n],
                                        font=font_2,
                                        bg='white'))
        labels_a_2_2[0].place(relx=pl_x2[l_column],
                              rely=pl_y2[l_row],
                              anchor='w')

frame_a_2_3 = tk.Frame(frame_a_2, bg=color_back)
frame_a_2_3.place(rely=0.85, relwidth=1, relheight=0.15)

label_a_2_3 = tk.Label(frame_a_2_3,
                       text="Press Cancel to cancel and logout",
                       font=font_2,
                       bg=color_back,
                       fg='white')
label_a_2_3.place(relx=0.5, rely=0.5, anchor='c')


frame_a_3 = tk.Frame(root, bg=color_back)


def key_press_a_3(event):
    if event.keysym == '1':
        to_thirty_one_admin(event)
    elif event.keysym == '2':
        to_thirty_one_admin(event)
    elif event.keysym == '3':
        to_thirty_one_admin(event)


frame_a_3.bind("<Escape>", to_second_admin)
frame_a_3.bind("<Key>", key_press_a_3)

frame_a_3_1 = tk.Frame(frame_a_3, bg='white')
frame_a_3_1.place(relwidth=1, relheight=0.2)

label_a_3_1 = tk.Label(frame_a_3_1,
                       text="Select action by\npressing action number",
                       font=font_3_bold,
                       bg='white')
label_a_3_1.place(relx=0.5, rely=0.5, anchor='c')

frame_a_3_2 = tk.Frame(frame_a_3, bg='white')
frame_a_3_2.place(rely=0.2, relwidth=1, relheight=0.65)

labels_a_3_2 = []
pl_x321 = [0.33]
pl_y321 = [0.2, 0.45, 0.7]
pl_x322 = [0.35]
pl_y322 = [0.2, 0.45, 0.7]
t32l = ["Power Line(s) Setup",
        "Charger(s) Setup",
        "CAN Bus Setup"]
      
for l_column in range(1):
    for l_row in range(3):
        n = 2 * l_column + l_row
        labels_a_3_2.insert(0, tk.Label(frame_a_3_2,
                                        text=' ' + str(n + 1) + ' ',
                                        font=font_2,
                                        bg=color_back,
                                        fg=color_front))
        labels_a_3_2[0].place(relx=pl_x321[l_column],
                              rely=pl_y321[l_row],
                              anchor='e')
        labels_a_3_2.insert(0, tk.Label(frame_a_3_2,
                                        text=t32l[n],
                                        font=font_2,
                                        bg='white'))
        labels_a_3_2[0].place(relx=pl_x322[l_column],
                              rely=pl_y322[l_row],
                              anchor='w')

frame_a_3_3 = tk.Frame(frame_a_3, bg=color_back)
frame_a_3_3.place(rely=0.85, relwidth=1, relheight=0.15)

label_a_3_3 = tk.Label(frame_a_3_3,
                       text="Press Cancel to return to Administration and "
                            "Setup Menu",
                       font=font_6,
                       bg=color_back,
                       fg='white')
label_a_3_3.place(relx=0.5, rely=0.5, anchor='c')


frame_a_31 = tk.Frame(root, bg=color_back)

style_a_31 = ttk.Style(frame_a_31)
style_a_31.configure("TSeparator", background=color_back)

frame_a_31_1 = tk.Frame(frame_a_31, bg='white')
frame_a_31_1.place(relwidth=1, relheight=0.2)

label_a_31_1 = tk.Label(frame_a_31_1,
                        text="Charger(s) Setup",
                        font=font_3_bold,
                        bg='white')
label_a_31_1.place(relx=0.5, rely=0.5, anchor='c')

frame_a_31_2 = tk.Frame(frame_a_31, bg='white')
frame_a_31_2.place(rely=0.2, relwidth=1, relheight=0.65)

label_a_31_21 = tk.Label(frame_a_31_2,
                         text="Enter Charger# to modify",
                         font=font_6_bold,
                         bg="white")
label_a_31_21.place(relx=0.15, rely=0.15, anchor='w')


def entry_a_31_escape(event):
    if name_admin_node_num.get() == '':
        to_second_admin(event)
    else:
        name_admin_node_num.set('')


def entry_a_31_enter(event):
    global admin_node_num
    charger_entry = name_admin_node_num.get()
    try:
        charger_num = int(charger_entry)
    except ValueError:
        name_admin_node_num.set('')
        return
    if charger_num < 0:
        name_admin_node_num.set('')
        return
    if charger_num == 0:
        to_thirty_two_admin(event)
        return
    admin_node_num = charger_num
    to_thirty_three_admin(event)


entry_a_31 = tk.Entry(frame_a_31_2,
                      textvariable=name_admin_node_num,
                      font=font_4,
                      width=2,
                      justify=tk.CENTER,
                      bd=4,
                      bg="lightgrey")
entry_a_31.bind("<Return>", entry_a_31_enter)
entry_a_31.bind("<Escape>", entry_a_31_escape)
entry_a_31.place(relx=0.83, rely=0.15, anchor="e")

separator_a_31_21 = ttk.Separator(frame_a_31_2, orient='horizontal')
separator_a_31_21.place(relx=0.1, rely=0.3, relwidth=0.8, height=4)

label_a_31_221 = tk.Label(frame_a_31_2,
                          text="--->",
                          font=font_2c_bold,
                          bg="white")
label_a_31_221.place(relx=0.15, rely=0.46, anchor='w')

label_a_31_222 = tk.Label(frame_a_31_2,
                          text="then press",
                          font=font_6,
                          bg="white")
label_a_31_222.place(relx=0.3, rely=0.45, anchor='w')

label_a_31_223 = tk.Label(frame_a_31_2,
                          text="Enter",
                          font=font_3_bold,
                          fg=color_back,
                          bg="white")
label_a_31_223.place(relx=0.85, rely=0.45, anchor='e')

separator_a_31_22 = ttk.Separator(frame_a_31_2, orient='horizontal')
separator_a_31_22.place(relx=0.1, rely=0.6, relwidth=0.8, height=4)

label_a_31_231 = tk.Label(frame_a_31_2,
                          text="--->",
                          font=font_2c_bold,
                          bg="white")
label_a_31_231.place(relx=0.15, rely=0.76, anchor='w')

label_a_31_232 = tk.Label(frame_a_31_2,
                          text="or enter",
                          font=font_6,
                          bg="white")
label_a_31_232.place(relx=0.3, rely=0.75, anchor='w')

label_a_31_233 = tk.Label(frame_a_31_2,
                          text="0",
                          font=font_7_bold,
                          fg=color_back,
                          bg="white")
label_a_31_233.place(relx=0.48, rely=0.74, anchor='c')

label_a_31_234 = tk.Label(frame_a_31_2,
                          text="to add a new charger",
                          font=font_6,
                          bg="white")
label_a_31_234.place(relx=0.85, rely=0.75, anchor='e')

frame_a_31_3 = tk.Frame(frame_a_31, bg=color_back)
frame_a_31_3.place(rely=0.85, relwidth=1, relheight=0.15)

label_a_31_3 = tk.Label(frame_a_31_3,
                        text="Press Cancel to return to Administration and "
                             "Setup Menu",
                        font=font_6,
                        bg=color_back,
                        fg='white')
label_a_31_3.place(relx=0.5, rely=0.5, anchor='c')

frame_a_32 = tk.Frame(root, bg=color_back)

frame_a_32_1 = tk.Frame(frame_a_32, bg='white')
frame_a_32_1.place(relwidth=1, relheight=0.2)

label_a_32_1 = tk.Label(frame_a_32_1,
                        text="Add a new Charger",
                        font=font_3_bold,
                        bg='white')
label_a_32_1.place(relx=0.5, rely=0.5, anchor='c')

frame_a_32_2 = tk.Frame(frame_a_32, bg="white")
frame_a_32_2.place(rely=0.2, relwidth=1, relheight=0.65)

label_a_32_21 = tk.Label(frame_a_32_2,
                         text="Enter Charger# to add",
                         font=font_6_bold,
                         bg="white")
label_a_32_21.place(relx=0.15, rely=0.15, anchor='w')


def entry_a_32_escape(event):
    if name_admin_node_num.get() == '':
        to_thirty_one_admin(event)
    else:
        name_admin_node_num.set('')


def entry_a_32_enter(event):
    global admin_node_num
    charger_entry = name_admin_node_num.get()
    try:
        charger_num = int(charger_entry)
    except ValueError:
        name_admin_node_num.set('')
        return
    if charger_num <= 0:
        name_admin_node_num.set('')
        return
    admin_node_num = charger_num
    to_thirty_three_admin(event)


entry_a_32 = tk.Entry(frame_a_32_2,
                      textvariable=name_admin_node_num,
                      font=font_4,
                      width=2,
                      justify=tk.CENTER,
                      bd=4,
                      bg="lightgrey")
entry_a_32.bind("<Return>", entry_a_32_enter)
entry_a_32.bind("<Escape>", entry_a_32_escape)
entry_a_32.place(relx=0.83, rely=0.15, anchor="e")

separator_a_32_21 = ttk.Separator(frame_a_32_2, orient='horizontal')
separator_a_32_21.place(relx=0.1, rely=0.3, relwidth=0.8, height=4)

label_a_32_221 = tk.Label(frame_a_32_2,
                          text="--->",
                          font=font_2c_bold,
                          bg="white")
label_a_32_221.place(relx=0.15, rely=0.46, anchor='w')

label_a_32_222 = tk.Label(frame_a_32_2,
                          text="then press",
                          font=font_6,
                          bg="white")
label_a_32_222.place(relx=0.3, rely=0.45, anchor='w')

label_a_32_223 = tk.Label(frame_a_32_2,
                          text="Enter",
                          font=font_3_bold,
                          fg=color_back,
                          bg="white")
label_a_32_223.place(relx=0.85, rely=0.45, anchor='e')

frame_a_32_3 = tk.Frame(frame_a_32, bg=color_back)
frame_a_32_3.place(rely=0.85, relwidth=1, relheight=0.15)

label_a_32_3 = tk.Label(frame_a_32_3,
                        text="Press Cancel to return to Charger(s) Setup",
                        font=font_2,
                        bg=color_back,
                        fg='white')
label_a_32_3.place(relx=0.5, rely=0.5, anchor='c')


frame_a_33 = tk.Frame(root, bg=color_back)
frame_a_33.bind("<Escape>", to_thirty_one_admin)
frame_a_33.bind("<Return>", to_thirty_seven_admin)

frame_a_33_1 = tk.Frame(frame_a_33, bg="white")
frame_a_33_1.place(relwidth=1, relheight=0.2)

label_a_33_1 = tk.Label(frame_a_33_1,
                        text="Continue with existing Charger",
                        font=font_3_bold,
                        bg='white')
label_a_33_1.place(relx=0.5, rely=0.5, anchor='c')

frame_a_33_2 = tk.Frame(frame_a_33, bg="white")
frame_a_33_2.place(rely=0.2, relwidth=1, relheight=0.65)

label_a_33_2 = tk.Label(frame_a_33_2,
                        text="Confirm Charger# selected to modify",
                        font=font_6_bold,
                        bg="white")
label_a_33_2.place(relx=0.1, rely=0.15, anchor='w')

separator_a_32_22 = ttk.Separator(frame_a_33_2, orient='horizontal')
separator_a_32_22.place(relx=0.1, rely=0.35, relwidth=0.35, height=4)

separator_a_32_23 = ttk.Separator(frame_a_33_2, orient='horizontal')
separator_a_32_23.place(relx=0.55, rely=0.35, relwidth=0.35, height=4)

label_a_33_3 = tk.Label(frame_a_33_2,
                        text="OR",
                        font=font_7_bold,
                        fg=color_back,
                        bg="white")
label_a_33_3.place(relx=0.5, rely=0.35, anchor='c')

entry_a_33 = tk.Entry(frame_a_33_2,
                      takefocus=0,
                      state=tk.DISABLED,
                      textvariable=name_admin_node_num,
                      font=font_4,
                      width=2,
                      justify=tk.CENTER,
                      bd=4,
                      bg="lightgrey")
entry_a_33.place(relx=0.83, rely=0.15, anchor="e")

labels_a_3_3 = []
pl_x331 = [0.18]
pl_y331 = [0.55, 0.8]
pl_x332 = [0.2]
pl_y332 = [0.55, 0.8]
t33l = ["Delete this Charger",
        "Add new Charger (another # to select)"]
      
for l_column in range(1):
    for l_row in range(2):
        n = 2 * l_column + l_row
        labels_a_3_3.insert(0, tk.Label(frame_a_33_2,
                                        text=' ' + str(n + 1) + ' ',
                                        font=font_2,
                                        bg=color_back,
                                        fg=color_front))
        labels_a_3_3[0].place(relx=pl_x331[l_column],
                              rely=pl_y331[l_row],
                              anchor='e')
        labels_a_3_3.insert(0, tk.Label(frame_a_33_2,
                                        text=t33l[n],
                                        font=font_6_bold,
                                        bg='white'))
        labels_a_3_3[0].place(relx=pl_x332[l_column],
                              rely=pl_y332[l_row],
                              anchor='w')

frame_a_33_3 = tk.Frame(frame_a_33, bg=color_back)
frame_a_33_3.place(rely=0.85, relwidth=1, relheight=0.15)

label_a_33_31 = tk.Label(frame_a_33_3,
                         text="Press Enter to confirm",
                         font=font_6_bold,
                         bg=color_back,
                         fg='white')
label_a_33_31.place(relx=0.5, rely=0.3, anchor='c')

label_a_33_32 = tk.Label(frame_a_33_3,
                         text="Press Cancel to cancel",
                         font=font_6_bold,
                         bg=color_back,
                         fg='white')
label_a_33_32.place(relx=0.5, rely=0.7, anchor='c')

frame_a_37 = tk.Frame(root, bg=color_back)
frame_a_37.bind("<Escape>", to_thirty_one_admin)

frame_a_37_1 = tk.Frame(frame_a_37, bg='white')
frame_a_37_1.place(relwidth=1, relheight=0.85)

label_a_37_00 = tk.Label(frame_a_37_1,
                         text="Selected Charger #",
                         font=font_3_bold,
                         bg="white")
label_a_37_00.place(relx=0.4, rely=0.1, anchor='c')

entry_a_37_00 = tk.Entry(frame_a_37_1,
                         takefocus=0,
                         state=tk.DISABLED,
                         textvariable=name_admin_node_num,
                         font=font_4,
                         width=2,
                         justify=tk.CENTER,
                         bd=4,
                         bg="lightgrey")
entry_a_37_00.place(relx=0.7, rely=0.1, anchor="w")

label_a_37_10 = tk.Label(frame_a_37_1,
                         text="Charger number",
                         font=font_6_bold,
                         bg="white")
label_a_37_10.place(relx=0.1, rely=0.3, anchor='w')


def entry_a_37_10_escape(event):
    if name_admin_node_num.get() == '':
        to_thirty_one_admin(event)
    else:
        name_admin_node_num.set('')


# noinspection PyUnusedLocal
def entry_a_37_10_enter(event):
    global admin_node_num
    charger_entry = name_admin_node_num.get()
    try:
        charger_num = int(charger_entry)
    except ValueError:
        name_admin_node_num.set('')
        return
    if charger_num <= 0:
        name_admin_node_num.set('')
        return
    admin_node_num = charger_num
    entry_a_37_20.focus_set()
    entry_a_37_20.select_range(0, tk.END)


entry_a_37_10 = tk.Entry(frame_a_37_1,
                         textvariable=name_admin_node_num,
                         font=font_2,
                         width=3,
                         justify=tk.CENTER,
                         bd=4,
                         bg="white")

entry_a_37_10.bind("<Return>", entry_a_37_10_enter)
entry_a_37_10.bind("<Escape>", entry_a_37_10_escape)
entry_a_37_10.place(relx=0.8, rely=0.35, anchor="sw")

separator_a_37_10 = ttk.Separator(frame_a_37_1, orient='horizontal')
separator_a_37_10.place(relx=0.1, rely=0.35, relwidth=0.65, height=4)

label_a_37_20 = tk.Label(frame_a_37_1,
                         text="Power Line number",
                         font=font_6_bold,
                         bg="white")
label_a_37_20.place(relx=0.1, rely=0.45, anchor='w')


def entry_a_37_20_escape(event):
    if name_admin_power_line_num.get() == '':
        to_thirty_one_admin(event)
    else:
        name_admin_power_line_num.set('')


# noinspection PyUnusedLocal
def entry_a_37_20_enter(event):
    global admin_power_line_num
    charger_entry = name_admin_power_line_num.get()
    try:
        charger_num = int(charger_entry)
    except ValueError:
        name_admin_node_num.set('')
        return
    if charger_num <= 0:
        name_admin_node_num.set('')
        return
    admin_power_line_num = charger_num
    entry_a_37_30.focus_set()
    entry_a_37_30.select_range(0, tk.END)


entry_a_37_20 = tk.Entry(frame_a_37_1,
                         textvariable=name_admin_power_line_num,
                         font=font_2,
                         width=3,
                         justify=tk.CENTER,
                         bd=4,
                         bg="white")
entry_a_37_20.bind("<Return>", entry_a_37_20_enter)
entry_a_37_20.bind("<Escape>", entry_a_37_20_escape)
entry_a_37_20.place(relx=0.8, rely=0.5, anchor="sw")

separator_a_37_20 = ttk.Separator(frame_a_37_1, orient='horizontal')
separator_a_37_20.place(relx=0.1, rely=0.5, relwidth=0.65, height=4)

label_a_37_30 = tk.Label(frame_a_37_1,
                         text="Type",
                         font=font_6_bold,
                         bg="white")
label_a_37_30.place(relx=0.1, rely=0.6, anchor='w')

label_a_37_31 = tk.Label(frame_a_37_1,
                         text="1 Public",
                         font=font_8_bold,
                         fg=color_back,
                         bg="white")
label_a_37_31.place(relx=0.25, rely=0.6, anchor='w')

label_a_37_32 = tk.Label(frame_a_37_1,
                         text="2 Private",
                         font=font_8_bold,
                         fg=color_back,
                         bg="white")

label_a_37_32.place(relx=0.425, rely=0.6, anchor='w')

entry_a_37_30 = tk.Entry(frame_a_37_1,
                         textvariable=name_admin_node_type,
                         font=font_2,
                         width=3,
                         justify=tk.CENTER,
                         bd=4,
                         bg="white")
entry_a_37_30.place(relx=0.8, rely=0.65, anchor="sw")

separator_a_37_30 = ttk.Separator(frame_a_37_1, orient='horizontal')
separator_a_37_30.place(relx=0.1, rely=0.65, relwidth=0.65, height=4)

separator_a_37_31 = ttk.Separator(frame_a_37_1, orient='vertical')
separator_a_37_31.place(relx=0.4, rely=0.57, relheight=0.06, width=4)

label_a_37_40 = tk.Label(frame_a_37_1,
                         text="Status",
                         font=font_6_bold,
                         bg="white")
label_a_37_40.place(relx=0.1, rely=0.75, anchor='w')

label_a_37_41 = tk.Label(frame_a_37_1,
                         text="1 Online",
                         font=font_8_bold,
                         fg=color_back,
                         bg="white")
label_a_37_41.place(relx=0.25, rely=0.75, anchor='w')

label_a_37_42 = tk.Label(frame_a_37_1,
                         text="2 Offline",
                         font=font_8_bold,
                         fg=color_back,
                         bg="white")

label_a_37_42.place(relx=0.425, rely=0.75, anchor='w')

label_a_37_43 = tk.Label(frame_a_37_1,
                         text="3 Disable",
                         font=font_8_bold,
                         fg=color_back,
                         bg="white")
label_a_37_43.place(relx=0.6, rely=0.75, anchor='w')

entry_a_37_40 = tk.Entry(frame_a_37_1,
                         textvariable=name_admin_node_status,
                         font=font_2,
                         width=3,
                         justify=tk.CENTER,
                         bd=4,
                         bg="white")
entry_a_37_40.place(relx=0.8, rely=0.8, anchor="sw")

separator_a_37_40 = ttk.Separator(frame_a_37_1, orient='horizontal')
separator_a_37_40.place(relx=0.1, rely=0.8, relwidth=0.65, height=4)

separator_a_37_41 = ttk.Separator(frame_a_37_1, orient='vertical')
separator_a_37_41.place(relx=0.4, rely=0.72, relheight=0.06, width=4)

separator_a_37_42 = ttk.Separator(frame_a_37_1, orient='vertical')
separator_a_37_42.place(relx=0.575, rely=0.72, relheight=0.06, width=4)

frame_a_37_2 = tk.Frame(frame_a_37, bg=color_back)
frame_a_37_2.place(rely=0.85, relwidth=1, relheight=0.15)

label_a_37_21 = tk.Label(frame_a_37_2,
                         text="Press Enter to save and return to the "
                              "Charger(s) Setup screen",
                         font=font_8_bold,
                         bg=color_back,
                         fg='white')
label_a_37_21.place(relx=0.05, rely=0.3, anchor='w')

label_a_37_22 = tk.Label(frame_a_37_2,
                         text="Press Cancel to return to the Charger(s) "
                              "Setup screen",
                         font=font_8_bold,
                         bg=color_back,
                         fg='white')
label_a_37_22.place(relx=0.05, rely=0.7, anchor='w')


root.bind("<Shift-Up>", switch_to_full_screen)
root.bind("<Shift-Down>", switch_from_full_screen)
root.bind("<Shift-Escape>", to_zero_screen)


frame_num = 0
users = Users()

root.mainloop()
