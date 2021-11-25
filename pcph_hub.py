# -*- coding: utf-8 -*-
# !/usr/bin/python3

import tkinter as tk
from tkinter import ttk
from tkinter import font as tk_font

from pathlib import Path
from datetime import datetime
import csv

NODE_LENGTH = 2
PIN_LENGTH = 4
PASSWORD_LENGTH = 6

CSV_FOLDER = Path("CSV")

node_fields = "ID", "Charger Node Name", "Charger Node Type", \
              "Charger Node Status", "Power Line", "CAN Bus Address", "Active"
# node_access_types = "PRIVATE", "PUBLIC", "MIXED"
node_access_types = "PUBLIC", "PRIVATE", "MIXED"
# node_statuses = "ACTIVE", "OFF", "REPAIR"
node_statuses = "ONLINE", "OFFLINE", "REPAIR"

# PIN_ADMIN = "0998"
PIN_ADMIN = "0000"

cur_user = None
node_num = -1


# admin_node_num = -1
# admin_power_line_num = -1


class Node:

    def __init__(self, node_id=0):
        self.__id = node_id
        self.__name = ''
        self.__access = 0
        self.__status = 0
        self.__power_line_id = 0
        self.__power_line = None
        self.__can_bus_id = 0
        self.__active = False

    def get_id(self):
        return self.__id

    def set_id(self, new_id):
        self.__id = new_id

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_access(self):
        return self.__access

    def set_access(self, access):
        self.__access = access

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status

    def get_power_line_id(self):
        return self.__power_line_id

    def set_power_line_id(self, line_id):
        self.__power_line_id = line_id

    def get_can_bus_id(self):
        return self.__can_bus_id

    def set_can_bus_id(self, bus_id):
        self.__can_bus_id = bus_id

    def get_active(self):
        return self.__active

    def set_active(self, active):
        self.__active = active


class Nodes:
    def __init__(self, file_path_name=CSV_FOLDER / "node_test.csv"):
        self.__nodes = self.__read_csv(file_path_name)

    def get_nodes(self):
        return self.__nodes

    def set_nodes(self, all_nodes):
        self.__nodes = all_nodes

    def get_size(self):
        return self.__nodes.__sizeof__()

    def node_present(self, node_num_txt):
        for node in self.__nodes:
            if node.get_active() and node.get_name() == node_num_txt:
                return node
        return None

    @staticmethod
    def __read_csv(file_path_name):
        nodes_read = list()
        with open(file_path_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            row_count = 0
            for row in csv_reader:
                column_count = 0
                for column in row:
                    if row_count > 0:
                        if column_count == 0:
                            new_node = Node(int(column))
                        elif column_count == 1:
                            new_node.set_name(column)
                        elif column_count == 2:
                            node_type = column.upper()
                            if node_type == "PUBLIC":
                                new_node.set_access(1)
                            elif node_type == "PRIVATE":
                                new_node.set_access(2)
                            elif node_type == "MIXED":
                                new_node.set_access(3)
                            else:
                                new_node.set_access(0)
                        elif column_count == 3:
                            node_status = column.upper()
                            if node_status == "ONLINE":
                                new_node.set_status(1)
                            elif node_status == "OFFLINE":
                                new_node.set_status(2)
                            elif node_status == "REPAIR":
                                new_node.set_status(3)
                            else:
                                new_node.set_status(0)
                        elif column_count == 4:
                            new_node.set_power_line_id(column)
                        elif column_count == 5:
                            new_node.set_can_bus_id(column)
                        elif column_count == 6:
                            new_node.set_active(column == "ON")
                            nodes_read.append(new_node)
                    column_count += 1
                row_count += 1
        return nodes_read

    def save(self, file_path_name=CSV_FOLDER / "TEST\\node_test.csv"):
        self.write_csv(file_path_name)

    def save_backup(self):
        now = datetime.now()
        file_name = "Node_{}_{}_{}_{}_{}_{}.csv".format(
            now.year, now.month, now.day, now.hour, now.minute, now.second)
        self.save(CSV_FOLDER / "BACKUP" / file_name)

    def write_csv(self, file_path_name):
        with open(file_path_name, mode='w') as csv_write_file:
            csv_writer = csv.writer(csv_write_file, delimiter=',',
                                    lineterminator='\n')
            csv_writer.writerow(node_fields)
            for node in self.__nodes:
                if node.get_active():
                    node_active_txt = "ON"
                else:
                    node_active_txt = "OFF"
                csv_writer.writerow([str(node.get_id()), node.get_name(),
                                     node_access_types[node.get_access() - 1],
                                     node_statuses[node.get_status() - 1],
                                     str(node.get_power_line_id()),
                                     str(node.get_can_bus_id()),
                                     node_active_txt])

    def delete_by_name(self, name):
        for node in self.__nodes:
            if node.get_name() == name and node.get_active():
                self.save_backup()
                node.set_active(False)
                self.save(CSV_FOLDER / "node_test.csv")
                return True
        return False

    def add(self, node):
        self.save_backup()
        node.set_id(len(self.__nodes) + 1)
        self.__nodes.append(node)
        self.save(CSV_FOLDER / "node_test.csv")

    def modify(self, new_node):
        name = new_node.get_name()
        for node in self.__nodes:
            if node.get_name() == name and node.get_active():
                self.save_backup()
                node.set_power_line_id(new_node.get_power_line_id())
                node.set_access(new_node.get_access())
                node.set_status(new_node.get_status())
                self.save(CSV_FOLDER / "node_test.csv")
                return True
        return False


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
    # noinspection SpellCheckingInspection
    root.attributes("-fullscreen", True)


# noinspection PyUnusedLocal
def switch_from_full_screen(event):
    # noinspection SpellCheckingInspection
    root.attributes("-fullscreen", False)


def time_event_gen():
    global frame_num
    if frame_num == 4:
        frame_4.event_generate('<<time_event>>', when='tail')


def entry_node():
    node = Node()
    node.set_name(name_admin_node_num.get())
    node.set_power_line_id(int(name_admin_power_line_num.get()))
    node.set_access(int(name_admin_node_type.get()))
    node.set_status(int(name_admin_node_status.get()))
    node.set_active(True)
    return node


# noinspection PyUnusedLocal
def to_thirty_seven_admin(event):
    global frame_num
    frame_a_36.pack_forget()
    frame_num = 1037
    new_node = entry_node()
    if nodes.node_present(name_admin_node_num.get()) is None:
        nodes.add(new_node)
        label_a_37_12.configure(text="has been added")
    else:
        nodes.modify(new_node)
        label_a_37_12.configure(text="has been modified")
    frame_a_37.pack(fill="both", expand=True)
    frame_a_37.focus_set()


# noinspection PyUnusedLocal
def to_thirty_six_admin(event):
    global frame_num
    if frame_num == 1033:
        frame_a_33.pack_forget()
    if frame_num == 1034:
        frame_a_34.pack_forget()
    frame_num = 1036
    init_entries_a_36()
    frame_a_36.pack(fill="both", expand=True)
    entry_a_36_10.focus_set()
    entry_a_36_10.select_range(0, tk.END)


# noinspection PyUnusedLocal
def to_thirty_five_admin(event):
    global frame_num
    frame_a_33.pack_forget()
    frame_num = 1035
    frame_a_35.pack(fill="both", expand=True)
    frame_a_35.focus_set()


# noinspection PyUnusedLocal
def to_thirty_four_admin(event):
    global frame_num
    if frame_num == 1031:
        frame_a_31.pack_forget()
    if frame_num == 1032:
        frame_a_32.pack_forget()
    frame_num = 1034
    frame_a_34.pack(fill="both", expand=True)
    frame_a_34.focus_set()


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
    if frame_num == 1031:
        frame_a_31.pack_forget()
    if frame_num == 1033:
        frame_a_33.pack_forget()
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
    if frame_num == 1034:
        frame_a_34.pack_forget()
    if frame_num == 1035:
        frame_a_35.pack_forget()
    if frame_num == 1036:
        frame_a_36.pack_forget()
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
    elif frame_num == 1037:
        frame_a_37.pack_forget()
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
    elif frame_num == 1034:
        frame_a_34.pack_forget()
    elif frame_num == 1035:
        frame_a_35.place_forget()
    elif frame_num == 1036:
        frame_a_36.pack_forget()
    frame_num = 0
    name_pin.set('')
    frame_0.pack(fill="both", expand=True)
    frame_0.focus_set()


root = tk.Tk()

# noinspection SpellCheckingInspection
root.wm_title("PCPH  HUB")
# root.geometry("1024x600")
root.geometry("800x600")
root.minsize(800, 600)
root.configure(bg="#3838B8")
# noinspection SpellCheckingInspection
root.attributes("-fullscreen", True)

name_pin = tk.StringVar()
name_pass = tk.StringVar()

name_node_num = tk.StringVar(root, value=node_num)

name_admin_node_num = tk.StringVar()
name_admin_node_num_tmp = tk.StringVar()
name_admin_power_line_num = tk.StringVar()
name_admin_node_type = tk.StringVar()
name_admin_node_status = tk.StringVar()

color_front = "white"
color_back = "#3838B8"
color_entry_back = "#D8D8FC"
color_front_dialog = "black"
color_back_dialog = color_entry_back
color_border_dialog = color_back
thickness_border_dialog = 6

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
font_10_bold = tk_font.Font(family="Helvetica", size=28, weight="bold")

frame_0 = tk.Frame(root, bg=color_back)


# noinspection PyUnusedLocal
def key_press(event):
    if event.char == event.keysym or len(event.char) == 1:
        to_first_screen(event)


frame_0.bind("<Key>", key_press)
frame_0.pack(fill="both", expand=True)
frame_0.focus_set()

# noinspection SpellCheckingInspection
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
                         text="Enter Charger# to modify (1 - 99)",
                         font=font_6_bold,
                         bg="white")
label_a_31_21.place(relx=0.15, rely=0.15, anchor='w')


def entry_a_31_escape(event):
    if name_admin_node_num.get() == '':
        to_second_admin(event)
    else:
        name_admin_node_num.set('')


def entry_a_31_enter(event):
    # global admin_node_num
    charger_entry = name_admin_node_num.get()
    if len(charger_entry) > 2:
        name_admin_node_num.set('')
        return
    try:
        charger_num = int(charger_entry)
    except ValueError:
        name_admin_node_num.set('')
        return
    if charger_num < 0 or charger_num > 99:
        name_admin_node_num.set('')
        return
    if charger_num == 0:
        to_thirty_two_admin(event)
        return
    # admin_node_num = charger_num
    if nodes.node_present(name_admin_node_num.get()) is None:
        to_thirty_four_admin(event)
    else:
        to_thirty_three_admin(event)


# noinspection SpellCheckingInspection
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
                         text="Enter Charger# to add (1 - 99)",
                         font=font_6_bold,
                         bg="white")
label_a_32_21.place(relx=0.15, rely=0.15, anchor='w')


def entry_a_32_escape(event):
    if name_admin_node_num.get() == '':
        to_thirty_one_admin(event)
    else:
        name_admin_node_num.set('')


def entry_a_32_enter(event):
    # global admin_node_num
    charger_entry = name_admin_node_num.get()
    if len(charger_entry) > 2:
        name_admin_node_num.set('')
    try:
        charger_num = int(charger_entry)
    except ValueError:
        name_admin_node_num.set('')
        return
    if charger_num <= 0 or charger_num > 99:
        name_admin_node_num.set('')
        return
    if nodes.node_present(name_admin_node_num.get()) is None:
        to_thirty_four_admin(event)
    else:
        to_thirty_three_admin(event)


# noinspection SpellCheckingInspection
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


# noinspection PyUnusedLocal
def to_thirty_three_dialog(event):
    frame_d_33.place(relx=0.15, rely=0.3, relwidth=0.65, relheight=0.6)
    frame_d_33.focus_set()


frame_a_33 = tk.Frame(root, bg=color_back)
frame_a_33.bind("<Escape>", to_thirty_one_admin)
frame_a_33.bind("<Return>", to_thirty_six_admin)
frame_a_33.bind("1", to_thirty_three_dialog)
frame_a_33.bind("2", to_thirty_two_admin)

frame_a_33_1 = tk.Frame(frame_a_33, bg="white")
frame_a_33_1.place(relwidth=1, relheight=0.2)

label_a_33_11 = tk.Label(frame_a_33_1,
                         text="You selected",
                         font=font_10_bold,
                         bg='white')
label_a_33_11.place(relx=0.36, rely=0.5, anchor='e')

label_a_33_12 = tk.Label(frame_a_33_1,
                         text="EXISTING CHARGER",
                         font=font_3_bold,
                         fg='red',
                         bg='white')
label_a_33_12.place(relx=0.38, rely=0.48, anchor='w')

frame_a_33_2 = tk.Frame(frame_a_33, bg="white")
frame_a_33_2.place(rely=0.2, relwidth=1, relheight=0.65)

label_a_33_2 = tk.Label(frame_a_33_2,
                        text="Confirm and continue to MODIFY #",
                        font=font_10_bold,
                        bg="white")
label_a_33_2.place(relx=0.05, rely=0.15, anchor='w')

separator_a_33_22 = ttk.Separator(frame_a_33_2, orient='horizontal')
separator_a_33_22.place(relx=0.1, rely=0.35, relwidth=0.35, height=4)

separator_a_33_23 = ttk.Separator(frame_a_33_2, orient='horizontal')
separator_a_33_23.place(relx=0.55, rely=0.35, relwidth=0.35, height=4)

label_a_33_3 = tk.Label(frame_a_33_2,
                        text="OR",
                        font=font_7_bold,
                        fg=color_back,
                        bg="white")
label_a_33_3.place(relx=0.5, rely=0.35, anchor='c')

# noinspection SpellCheckingInspection
entry_a_33 = tk.Entry(frame_a_33_2,
                      takefocus=0,
                      state=tk.DISABLED,
                      textvariable=name_admin_node_num,
                      font=font_4,
                      width=2,
                      justify=tk.CENTER,
                      bd=4,
                      bg="lightgrey")
entry_a_33.place(relx=0.95, rely=0.15, anchor="e")

labels_a_3_3 = []
pl_x331 = [0.13]
pl_y331 = [0.55, 0.8]
pl_x332 = [0.15]
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
                                        font=font_2_bold,
                                        bg='white'))
        labels_a_3_3[0].place(relx=pl_x332[l_column],
                              rely=pl_y332[l_row],
                              anchor='w')

frame_a_33_3 = tk.Frame(frame_a_33, bg=color_back)
frame_a_33_3.place(rely=0.85, relwidth=1, relheight=0.15)

label_a_33_31 = tk.Label(frame_a_33_3,
                         text="Press Enter to confirm this selection",
                         font=font_6,
                         bg=color_back,
                         fg='white')
label_a_33_31.place(relx=0.5, rely=0.3, anchor='c')

label_a_33_32 = tk.Label(frame_a_33_3,
                         text="Press Cancel to cancel and return"
                              " to Charger's Setup",
                         font=font_6,
                         bg=color_back,
                         fg='white')
label_a_33_32.place(relx=0.5, rely=0.7, anchor='c')


# noinspection PyUnusedLocal
def frame_d_33_escape(event):
    frame_d_33.place_forget()
    frame_a_33.focus_set()


# noinspection PyUnusedLocal
def frame_d_33_enter(event):
    nodes.delete_by_name((name_admin_node_num.get()))
    frame_d_33.place_forget()
    to_thirty_five_admin(event)


frame_d_33 = tk.Frame(frame_a_33,
                      bg=color_back_dialog,
                      highlightcolor=color_border_dialog,
                      highlightthickness=thickness_border_dialog)
frame_d_33.bind("<Escape>", frame_d_33_escape)
frame_d_33.bind("<Return>", frame_d_33_enter)

label_d_33_1 = tk.Label(frame_d_33,
                        text="DELETE",
                        font=font_3_bold,
                        fg="red",
                        bg=color_back_dialog)
label_d_33_1.place(relx=0.5, rely=0.15, anchor='c')

label_d_33_2 = tk.Label(frame_d_33,
                        text="Charger # ",
                        font=font_10_bold,
                        fg=color_front_dialog,
                        bg=color_back_dialog)
label_d_33_2.place(relx=0.35, rely=0.35, anchor='c')

# noinspection SpellCheckingInspection
entry_d_33 = tk.Entry(frame_d_33,
                      takefocus=0,
                      state=tk.DISABLED,
                      textvariable=name_admin_node_num,
                      font=font_4,
                      width=2,
                      justify=tk.CENTER,
                      bd=4,
                      bg="lightgrey")
entry_d_33.place(relx=0.8, rely=0.35, anchor="c")

label_d_33_31 = tk.Label(frame_d_33,
                         text="Press ",
                         font=font_6_bold,
                         fg=color_front_dialog,
                         bg=color_back_dialog)
label_d_33_31.place(relx=0.05, rely=0.715, anchor='w')

label_d_33_32 = tk.Label(frame_d_33,
                         text="Enter ",
                         font=font_3_bold,
                         fg=color_back,
                         bg=color_back_dialog)
label_d_33_32.place(relx=0.21, rely=0.7, anchor='w')

label_d_33_33 = tk.Label(frame_d_33,
                         text="--->",
                         font=font_2c_bold,
                         fg=color_front_dialog,
                         bg=color_back_dialog)
label_d_33_33.place(relx=0.46, rely=0.713, anchor='w')

label_d_33_34 = tk.Label(frame_d_33,
                         text="to CONFIRM",
                         font=font_6_bold,
                         fg=color_front_dialog,
                         bg=color_back_dialog)
label_d_33_34.place(relx=0.64, rely=0.715, anchor='w')

label_d_33_41 = tk.Label(frame_d_33,
                         text="Press ",
                         font=font_6_bold,
                         fg=color_front_dialog,
                         bg=color_back_dialog)
label_d_33_41.place(relx=0.04, rely=0.865, anchor='w')

label_d_33_42 = tk.Label(frame_d_33,
                         text="Cancel ",
                         font=font_3_bold,
                         fg=color_back,
                         bg=color_back_dialog)
label_d_33_42.place(relx=0.2, rely=0.85, anchor='w')

label_d_33_43 = tk.Label(frame_d_33,
                         text="--->",
                         font=font_2c_bold,
                         fg=color_front_dialog,
                         bg=color_back_dialog)
label_d_33_43.place(relx=0.49, rely=0.863, anchor='w')

label_d_33_44 = tk.Label(frame_d_33,
                         text="to CANCEL",
                         font=font_6_bold,
                         fg=color_front_dialog,
                         bg=color_back_dialog)
label_d_33_44.place(relx=0.67, rely=0.865, anchor='w')

frame_a_34 = tk.Frame(root, bg=color_back)
frame_a_34.bind("<Escape>", to_thirty_one_admin)
frame_a_34.bind("<Return>", to_thirty_six_admin)
frame_a_34.bind("1", to_thirty_one_admin)

frame_a_34_1 = tk.Frame(frame_a_34, bg="white")
frame_a_34_1.place(relwidth=1, relheight=0.2)

label_a_34_11 = tk.Label(frame_a_34_1,
                         text="You selected",
                         font=font_10_bold,
                         bg='white')
label_a_34_11.place(relx=0.41, rely=0.5, anchor='e')

label_a_34_12 = tk.Label(frame_a_34_1,
                         text="NEW CHARGER",
                         font=font_3_bold,
                         fg='red',
                         bg='white')
label_a_34_12.place(relx=0.43, rely=0.48, anchor='w')

frame_a_34_2 = tk.Frame(frame_a_34, bg="white")
frame_a_34_2.place(rely=0.2, relwidth=1, relheight=0.65)

label_a_34_22 = tk.Label(frame_a_34_2,
                         text="Confirm and continue to ADD #",
                         font=font_10_bold,
                         bg="white")
label_a_34_22.place(relx=0.07, rely=0.15, anchor='w')

separator_a_34_22 = ttk.Separator(frame_a_34_2, orient='horizontal')
separator_a_34_22.place(relx=0.1, rely=0.35, relwidth=0.35, height=4)

separator_a_34_23 = ttk.Separator(frame_a_34_2, orient='horizontal')
separator_a_34_23.place(relx=0.55, rely=0.35, relwidth=0.35, height=4)

label_a_34_23 = tk.Label(frame_a_34_2,
                         text="OR",
                         font=font_7_bold,
                         fg=color_back,
                         bg="white")
label_a_34_23.place(relx=0.5, rely=0.35, anchor='c')

# noinspection SpellCheckingInspection
entry_a_34 = tk.Entry(frame_a_34_2,
                      takefocus=0,
                      state=tk.DISABLED,
                      textvariable=name_admin_node_num,
                      font=font_4,
                      width=2,
                      justify=tk.CENTER,
                      bd=4,
                      bg="lightgrey")
entry_a_34.place(relx=0.92, rely=0.15, anchor="e")

label_a34_24 = tk.Label(frame_a_34_2,
                        text=" 1 ",
                        font=font_2,
                        bg=color_back,
                        fg=color_front)
label_a34_24.place(relx=0.08, rely=0.6, anchor='e')

label_a34_25 = tk.Label(frame_a_34_2,
                        text="Modify existing Charger (another # to select)",
                        font=font_2_bold,
                        bg="white")
label_a34_25.place(relx=0.1, rely=0.6, anchor='w')

frame_a_34_3 = tk.Frame(frame_a_34, bg=color_back)
frame_a_34_3.place(rely=0.85, relwidth=1, relheight=0.15)

label_a_34_31 = tk.Label(frame_a_34_3,
                         text="Press Enter to confirm this selection",
                         font=font_6,
                         bg=color_back,
                         fg='white')
label_a_34_31.place(relx=0.5, rely=0.3, anchor='c')

label_a_34_32 = tk.Label(frame_a_34_3,
                         text="Press Cancel to cancel and return to Charger's"
                              "Setup",
                         font=font_6,
                         bg=color_back,
                         fg='white')
label_a_34_32.place(relx=0.5, rely=0.7, anchor='c')


def key_a_35(event):
    if event.char == event.keysym or len(event.char) == 1:
        to_thirty_one_admin(event)


frame_a_35 = tk.Frame(root, bg=color_back)
frame_a_35.bind("<Key>", key_a_35)

frame_a_35_1 = tk.Frame(frame_a_35, bg='white')
frame_a_35_1.place(relwidth=1, relheight=0.85)

label_a_35_11 = tk.Label(frame_a_35_1,
                         text="Charger # ",
                         font=font_4_bold,
                         bg="white")
label_a_35_11.place(relx=0.63, rely=0.25, anchor='e')

# noinspection SpellCheckingInspection
entry_a_35 = tk.Entry(frame_a_35_1,
                      takefocus=0,
                      state=tk.DISABLED,
                      textvariable=name_admin_node_num,
                      font=font_5,
                      width=2,
                      justify=tk.CENTER,
                      bd=4,
                      bg="lightgrey")
entry_a_35.place(relx=0.72, rely=0.25, anchor="c")

label_a_35_12 = tk.Label(frame_a_35_1,
                         text="has been deleted",
                         font=font_4_bold,
                         bg="white")
label_a_35_12.place(relx=0.5, rely=0.55, anchor='c')

frame_a_35_2 = tk.Frame(frame_a_35, bg=color_back)
frame_a_35_2.place(rely=0.85, relwidth=1, relheight=0.15)

label_a_35_2 = tk.Label(frame_a_35_2,
                        text="Press any key to continue",
                        font=font_3,
                        bg=color_back,
                        fg='white')
label_a_35_2.place(relx=0.5, rely=0.5, anchor='c')


def init_entries_a_36():
    name = name_admin_node_num.get()
    name_admin_node_num_tmp.set(name)
    node = nodes.node_present(name)
    if node is None:
        name_admin_power_line_num.set('')
        name_admin_node_type.set('')
        name_admin_node_status.set('')
    else:
        name_admin_power_line_num.set(node.get_power_line_id())
        name_admin_node_type.set(node.get_access())
        name_admin_node_status.set(node.get_status())


frame_a_36 = tk.Frame(root, bg=color_back)
frame_a_36.bind("<Escape>", to_thirty_one_admin)


frame_a_36_1 = tk.Frame(frame_a_36, bg='white')
frame_a_36_1.place(relwidth=1, relheight=0.85)

label_a_36_00 = tk.Label(frame_a_36_1,
                         text="Selected Charger #",
                         font=font_3_bold,
                         bg="white")
label_a_36_00.place(relx=0.4, rely=0.1, anchor='c')

# noinspection SpellCheckingInspection
entry_a_36_00 = tk.Entry(frame_a_36_1,
                         takefocus=0,
                         state=tk.DISABLED,
                         textvariable=name_admin_node_num,
                         font=font_4,
                         width=2,
                         justify=tk.CENTER,
                         bd=4,
                         bg="lightgrey")
entry_a_36_00.place(relx=0.7, rely=0.1, anchor="w")

label_a_36_10 = tk.Label(frame_a_36_1,
                         text="Charger number",
                         font=font_6_bold,
                         bg="white")
label_a_36_10.place(relx=0.1, rely=0.3, anchor='w')


# noinspection PyUnusedLocal
def to_entry_a_36_10_dialog(event):
    frame_d_36_10.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.6)
    frame_d_36_10.focus_set()


# noinspection PyUnusedLocal
def frame_d_36_10_escape(event):
    frame_d_36_10.place_forget()
    entry_a_36_10.focus_set()
    entry_a_36_10.select_range(0, tk.END)


frame_d_36_10 = tk.Frame(frame_a_36,
                         bg=color_back_dialog,
                         highlightcolor=color_border_dialog,
                         highlightthickness=thickness_border_dialog)
frame_d_36_10.bind("<Escape>", frame_d_36_10_escape)
frame_d_36_10.bind("<FocusOut>", frame_d_36_10_escape)

label_d_36_10_11 = tk.Label(frame_d_36_10,
                            text="For the field Charger #\n"
                                 "Enter any number in a range",
                            font=font_2_bold,
                            bg=color_back_dialog)
label_d_36_10_11.place(relx=0.5, rely=0.3, anchor='s')

label_d_36_10_12 = tk.Label(frame_d_36_10,
                            text="1  -  99",
                            font=font_3_bold,
                            fg="red",
                            bg=color_back_dialog)
label_d_36_10_12.place(relx=0.5, rely=0.375, anchor='c')

label_d_36_10_13 = tk.Label(frame_d_36_10,
                            text="(one or two symbols - no extra '0' or spaces)",
                            font=font_6_bold,
                            bg=color_back_dialog)
label_d_36_10_13.place(relx=0.5, rely=0.45, anchor='n')

label_d_36_10_21 = tk.Label(frame_d_36_10,
                            text="Press ",
                            font=font_6,
                            fg=color_front_dialog,
                            bg=color_back_dialog)
label_d_36_10_21.place(relx=0.05, rely=0.825, anchor='w')

label_d_36_10_22 = tk.Label(frame_d_36_10,
                            text="CANCEL",
                            font=font_3_bold,
                            fg=color_back,
                            bg=color_back_dialog)
label_d_36_10_22.place(relx=0.19, rely=0.8175, anchor='w')

label_d_36_10_23 = tk.Label(frame_d_36_10,
                            text="--->",
                            font=font_2c_bold,
                            fg=color_front_dialog,
                            bg=color_back_dialog)
label_d_36_10_23.place(relx=0.49, rely=0.825, anchor='w')

label_d_36_10_24 = tk.Label(frame_d_36_10,
                            text="to CONTINUE",
                            font=font_6_bold,
                            fg=color_front_dialog,
                            bg=color_back_dialog)
label_d_36_10_24.place(relx=0.64, rely=0.825, anchor='w')


def entry_a_36_10_escape(event):
    if name_admin_node_num_tmp.get() == '':
        to_thirty_six_dialog_cancel(event)
        # to_thirty_one_admin(event)
    else:
        name_admin_node_num_tmp.set('')


# noinspection PyUnusedLocal
def entry_a_36_10_enter(event):
    charger_txt = name_admin_node_num_tmp.get()
    if len(charger_txt) > 2:
        to_entry_a_36_10_dialog(event)
        return
    try:
        charger_num = int(charger_txt)
    except ValueError:
        to_entry_a_36_10_dialog(event)
        return
    if charger_num <= 0 or charger_num > 99:
        to_entry_a_36_10_dialog(event)
        return
    if name_admin_node_num.get() != charger_txt:
        name_admin_node_num.set(charger_txt)
        init_entries_a_36()
    entry_a_36_20.focus_set()
    entry_a_36_20.select_range(0, tk.END)


# noinspection PyUnusedLocal
def entry_a_36_10_focus_out(event):
    selected = root.focus_get()
    on_second = selected == entry_a_36_20
    on_other_entry =\
        on_second or selected == entry_a_36_30 or selected == entry_a_36_40
    if on_other_entry:
        charger_txt = name_admin_node_num_tmp.get()
        if len(charger_txt) > 2:
            to_entry_a_36_10_dialog(event)
            return
        try:
            charger_num = int(charger_txt)
        except ValueError:
            to_entry_a_36_10_dialog(event)
            return
        if charger_num <= 0 or charger_num > 99:
            to_entry_a_36_10_dialog(event)
            return
        # name_admin_node_num.set(charger_txt)
        # init_entries_a_36()
        if on_second:
            entry_a_36_20.select_range(0, tk.END)


entry_a_36_10 = tk.Entry(frame_a_36_1,
                         textvariable=name_admin_node_num_tmp,
                         font=font_2,
                         width=3,
                         justify=tk.CENTER,
                         bd=4,
                         bg="white")

entry_a_36_10.bind("<Escape>", entry_a_36_10_escape)
entry_a_36_10.bind("<Return>", entry_a_36_10_enter)
entry_a_36_10.bind("<FocusOut>", entry_a_36_10_focus_out)
entry_a_36_10.place(relx=0.8, rely=0.35, anchor="sw")

separator_a_36_10 = ttk.Separator(frame_a_36_1, orient='horizontal')
separator_a_36_10.place(relx=0.1, rely=0.35, relwidth=0.65, height=4)

label_a_36_20 = tk.Label(frame_a_36_1,
                         text="Power Line number",
                         font=font_6_bold,
                         bg="white")
label_a_36_20.place(relx=0.1, rely=0.45, anchor='w')


# noinspection PyUnusedLocal
def to_entry_a_36_20_dialog(event):
    frame_d_36_20.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.6)
    frame_d_36_20.focus_set()


# noinspection PyUnusedLocal
def frame_d_36_20_escape(event):
    frame_d_36_20.place_forget()
    entry_a_36_20.focus_set()
    entry_a_36_20.select_range(0, tk.END)


frame_d_36_20 = tk.Frame(frame_a_36,
                         bg=color_back_dialog,
                         highlightcolor=color_border_dialog,
                         highlightthickness=thickness_border_dialog)
frame_d_36_20.bind("<Escape>", frame_d_36_20_escape)
frame_d_36_20.bind("<FocusOut>", frame_d_36_20_escape)

label_d_36_20_11 = tk.Label(frame_d_36_20,
                            text="For the field Power Line #\n"
                                 "Enter any number in a range",
                            font=font_2_bold,
                            bg=color_back_dialog)
label_d_36_20_11.place(relx=0.5, rely=0.3, anchor='s')

label_d_36_20_12 = tk.Label(frame_d_36_20,
                            text="1  -  99",
                            font=font_3_bold,
                            fg="red",
                            bg=color_back_dialog)
label_d_36_20_12.place(relx=0.5, rely=0.375, anchor='c')

label_d_36_20_13 = tk.Label(frame_d_36_20,
                            text="(one or two symbols - no extra '0' or spaces)",
                            font=font_6_bold,
                            bg=color_back_dialog)
label_d_36_20_13.place(relx=0.5, rely=0.45, anchor='n')

label_d_36_20_21 = tk.Label(frame_d_36_20,
                            text="Press ",
                            font=font_6_bold,
                            fg=color_front_dialog,
                            bg=color_back_dialog)
label_d_36_20_21.place(relx=0.05, rely=0.825, anchor='w')

label_d_36_20_22 = tk.Label(frame_d_36_20,
                            text="CANCEL",
                            font=font_3_bold,
                            fg=color_back,
                            bg=color_back_dialog)
label_d_36_20_22.place(relx=0.19, rely=0.8175, anchor='w')

label_d_36_20_23 = tk.Label(frame_d_36_20,
                            text="--->",
                            font=font_2c_bold,
                            fg=color_front_dialog,
                            bg=color_back_dialog)
label_d_36_20_23.place(relx=0.49, rely=0.825, anchor='w')

label_d_36_20_24 = tk.Label(frame_d_36_20,
                            text="to CONTINUE",
                            font=font_6_bold,
                            fg=color_front_dialog,
                            bg=color_back_dialog)
label_d_36_20_24.place(relx=0.64, rely=0.825, anchor='w')


def entry_a_36_20_escape(event):
    if name_admin_power_line_num.get() == '':
        to_thirty_six_dialog_cancel(event)
        # to_thirty_one_admin(event)
    else:
        name_admin_power_line_num.set('')


# noinspection PyUnusedLocal
def entry_a_36_20_enter(event):
    entry_a_36_30.focus_set()
    entry_a_36_30.select_range(0, tk.END)


# noinspection PyUnusedLocal
def entry_a_36_20_focus_out(event):
    selected = root.focus_get()
    on_third = selected == entry_a_36_30
    on_other_entry =\
        on_third or selected == entry_a_36_10 or selected == entry_a_36_40
    if on_other_entry:
        charger_txt = name_admin_power_line_num.get()
        if len(charger_txt) > 2:
            to_entry_a_36_20_dialog(event)
            return
        try:
            charger_num = int(charger_txt)
        except ValueError:
            to_entry_a_36_20_dialog(event)
            return
        if charger_num <= 0 or charger_num > 99:
            to_entry_a_36_20_dialog(event)
            return
        if on_third:
            entry_a_36_30.select_range(0, tk.END)


entry_a_36_20 = tk.Entry(frame_a_36_1,
                         textvariable=name_admin_power_line_num,
                         font=font_2,
                         width=3,
                         justify=tk.CENTER,
                         bd=4,
                         bg="white")
entry_a_36_20.bind("<Escape>", entry_a_36_20_escape)
entry_a_36_20.bind("<Return>", entry_a_36_20_enter)
entry_a_36_20.bind("<FocusOut>", entry_a_36_20_focus_out)
entry_a_36_20.place(relx=0.8, rely=0.5, anchor="sw")

separator_a_36_20 = ttk.Separator(frame_a_36_1, orient='horizontal')
separator_a_36_20.place(relx=0.1, rely=0.5, relwidth=0.65, height=4)

label_a_36_30 = tk.Label(frame_a_36_1,
                         text="Type",
                         font=font_6_bold,
                         bg="white")
label_a_36_30.place(relx=0.1, rely=0.6, anchor='w')

label_a_36_31 = tk.Label(frame_a_36_1,
                         text="1 Public",
                         font=font_8_bold,
                         fg=color_back,
                         bg="white")
label_a_36_31.place(relx=0.25, rely=0.6, anchor='w')

label_a_36_32 = tk.Label(frame_a_36_1,
                         text="2 Private",
                         font=font_8_bold,
                         fg=color_back,
                         bg="white")

label_a_36_32.place(relx=0.425, rely=0.6, anchor='w')


# noinspection PyUnusedLocal
def to_entry_a_36_30_dialog(event):
    frame_d_36_30.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.6)
    frame_d_36_30.focus_set()


# noinspection PyUnusedLocal
def frame_d_36_30_escape(event):
    frame_d_36_30.place_forget()
    entry_a_36_30.focus_set()
    entry_a_36_30.select_range(0, tk.END)


frame_d_36_30 = tk.Frame(frame_a_36,
                         bg=color_back_dialog,
                         highlightcolor=color_border_dialog,
                         highlightthickness=thickness_border_dialog)
frame_d_36_30.bind("<Escape>", frame_d_36_30_escape)
frame_d_36_30.bind("<FocusOut>", frame_d_36_30_escape)

label_d_36_30_11 = tk.Label(frame_d_36_30,
                            text="For the field Type\n"
                                 "Enter any number in a range",
                            font=font_2_bold,
                            bg=color_back_dialog)
label_d_36_30_11.place(relx=0.5, rely=0.3, anchor='s')

label_d_36_30_12 = tk.Label(frame_d_36_30,
                            text="1  -  2",
                            font=font_3_bold,
                            fg="red",
                            bg=color_back_dialog)
label_d_36_30_12.place(relx=0.5, rely=0.375, anchor='c')

label_d_36_30_13 = tk.Label(frame_d_36_20,
                            text="(one or two symbols - "
                                 "no extra '0' or spaces)",
                            font=font_6_bold,
                            bg=color_back_dialog)
label_d_36_30_13.place(relx=0.5, rely=0.45, anchor='n')

label_d_36_30_21 = tk.Label(frame_d_36_30,
                            text="Press ",
                            font=font_6_bold,
                            fg=color_front_dialog,
                            bg=color_back_dialog)
label_d_36_30_21.place(relx=0.05, rely=0.825, anchor='w')

label_d_36_30_22 = tk.Label(frame_d_36_30,
                            text="CANCEL",
                            font=font_3_bold,
                            fg=color_back,
                            bg=color_back_dialog)
label_d_36_30_22.place(relx=0.19, rely=0.8175, anchor='w')

label_d_36_30_23 = tk.Label(frame_d_36_30,
                            text="--->",
                            font=font_2c_bold,
                            fg=color_front_dialog,
                            bg=color_back_dialog)
label_d_36_30_23.place(relx=0.49, rely=0.825, anchor='w')

label_d_36_30_24 = tk.Label(frame_d_36_30,
                            text="to CONTINUE",
                            font=font_6_bold,
                            fg=color_front_dialog,
                            bg=color_back_dialog)
label_d_36_30_24.place(relx=0.64, rely=0.825, anchor='w')


def entry_a_36_30_escape(event):
    if name_admin_node_type.get() == '':
        to_thirty_six_dialog_cancel(event)
        # to_thirty_one_admin(event)
    else:
        name_admin_node_type.set('')


# noinspection PyUnusedLocal
def entry_a_36_30_enter(event):
    entry_a_36_40.focus_set()
    entry_a_36_40.select_range(0, tk.END)


# noinspection PyUnusedLocal
def entry_a_36_30_focus_out(event):
    selected = root.focus_get()
    on_fourth = selected == entry_a_36_40
    on_other_entry =\
        on_fourth or selected == entry_a_36_10 or selected == entry_a_36_20
    if on_other_entry:
        charger_txt = name_admin_node_type.get()
        if len(charger_txt) > 1:
            to_entry_a_36_30_dialog(event)
            return
        try:
            charger_num = int(charger_txt)
        except ValueError:
            to_entry_a_36_30_dialog(event)
            return
        if charger_num <= 0 or charger_num > 2:
            to_entry_a_36_30_dialog(event)
            return
        if on_fourth:
            entry_a_36_40.select_range(0, tk.END)


entry_a_36_30 = tk.Entry(frame_a_36_1,
                         textvariable=name_admin_node_type,
                         font=font_2,
                         width=3,
                         justify=tk.CENTER,
                         bd=4,
                         bg="white")
entry_a_36_30.place(relx=0.8, rely=0.65, anchor="sw")
entry_a_36_30.bind("<Escape>", entry_a_36_30_escape)
entry_a_36_30.bind("<Return>", entry_a_36_30_enter)
entry_a_36_30.bind("<FocusOut>", entry_a_36_30_focus_out)

separator_a_36_30 = ttk.Separator(frame_a_36_1, orient='horizontal')
separator_a_36_30.place(relx=0.1, rely=0.65, relwidth=0.65, height=4)

separator_a_36_31 = ttk.Separator(frame_a_36_1, orient='vertical')
separator_a_36_31.place(relx=0.4, rely=0.57, relheight=0.06, width=4)

label_a_36_40 = tk.Label(frame_a_36_1,
                         text="Status",
                         font=font_6_bold,
                         bg="white")
label_a_36_40.place(relx=0.1, rely=0.75, anchor='w')

label_a_36_41 = tk.Label(frame_a_36_1,
                         text="1 Online",
                         font=font_8_bold,
                         fg=color_back,
                         bg="white")
label_a_36_41.place(relx=0.25, rely=0.75, anchor='w')

label_a_36_42 = tk.Label(frame_a_36_1,
                         text="2 Offline",
                         font=font_8_bold,
                         fg=color_back,
                         bg="white")

label_a_36_42.place(relx=0.425, rely=0.75, anchor='w')

label_a_36_43 = tk.Label(frame_a_36_1,
                         text="3 Repair",
                         font=font_8_bold,
                         fg=color_back,
                         bg="white")
label_a_36_43.place(relx=0.6, rely=0.75, anchor='w')


# noinspection PyUnusedLocal
def to_entry_a_36_40_dialog(event):
    frame_d_36_40.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.6)
    frame_d_36_40.focus_set()


# noinspection PyUnusedLocal
def frame_d_36_40_escape(event):
    frame_d_36_40.place_forget()
    entry_a_36_40.focus_set()
    entry_a_36_40.select_range(0, tk.END)


frame_d_36_40 = tk.Frame(frame_a_36,
                         bg=color_back_dialog,
                         highlightcolor=color_border_dialog,
                         highlightthickness=thickness_border_dialog)
frame_d_36_40.bind("<Escape>", frame_d_36_40_escape)
frame_d_36_40.bind("<FocusOut>", frame_d_36_40_escape)

label_d_36_40_11 = tk.Label(frame_d_36_40,
                            text="For the field Status\n"
                                 "Enter any number in a range",
                            font=font_2_bold,
                            bg=color_back_dialog)
label_d_36_40_11.place(relx=0.5, rely=0.3, anchor='s')

label_d_36_40_12 = tk.Label(frame_d_36_40,
                            text="1  -  3",
                            font=font_3_bold,
                            fg="red",
                            bg=color_back_dialog)
label_d_36_40_12.place(relx=0.5, rely=0.375, anchor='c')

label_d_36_40_13 = tk.Label(frame_d_36_40,
                            text="(one or two symbols - "
                                 "no extra '0' or spaces)",
                            font=font_6_bold,
                            bg=color_back_dialog)
label_d_36_40_13.place(relx=0.5, rely=0.45, anchor='n')

label_d_36_40_21 = tk.Label(frame_d_36_40,
                            text="Press ",
                            font=font_6_bold,
                            fg=color_front_dialog,
                            bg=color_back_dialog)
label_d_36_40_21.place(relx=0.05, rely=0.825, anchor='w')

label_d_36_40_22 = tk.Label(frame_d_36_40,
                            text="CANCEL",
                            font=font_3_bold,
                            fg=color_back,
                            bg=color_back_dialog)
label_d_36_40_22.place(relx=0.19, rely=0.8175, anchor='w')

label_d_36_40_23 = tk.Label(frame_d_36_40,
                            text="--->",
                            font=font_2c_bold,
                            fg=color_front_dialog,
                            bg=color_back_dialog)
label_d_36_40_23.place(relx=0.49, rely=0.825, anchor='w')

label_d_36_40_24 = tk.Label(frame_d_36_40,
                            text="to CONTINUE",
                            font=font_6_bold,
                            fg=color_front_dialog,
                            bg=color_back_dialog)
label_d_36_40_24.place(relx=0.64, rely=0.825, anchor='w')


def entry_a_36_40_escape(event):
    if name_admin_node_status.get() == '':
        to_thirty_six_dialog_cancel(event)
        # to_thirty_one_admin(event)
    else:
        name_admin_node_status.set('')


# noinspection PyUnusedLocal
def entry_a_36_40_enter(event):
    entry_a_36_10.focus_set()
    entry_a_36_10.select_range(0, tk.END)


def entry_a_36_40_focus_out(event):
    selected = root.focus_get()
    on_first = selected == entry_a_36_10
    on_other_entry =\
        on_first or selected == entry_a_36_20 or selected == entry_a_36_30
    if on_other_entry:
        charger_txt = name_admin_node_status.get()
        if len(charger_txt) > 1:
            to_entry_a_36_40_dialog(event)
            return
        try:
            charger_num = int(charger_txt)
        except ValueError:
            to_entry_a_36_40_dialog(event)
            return
        if charger_num <= 0 or charger_num > 3:
            to_entry_a_36_40_dialog(event)
            return
        if on_first:
            entry_a_36_10.select_range(0, tk.END)
            if name_admin_power_line_num.get() == ''\
                    or name_admin_node_type.get() == '':
                to_thirty_six_dialog_no_fields(event)
            else:
                to_thirty_six_dialog_confirm(event)


entry_a_36_40 = tk.Entry(frame_a_36_1,
                         textvariable=name_admin_node_status,
                         font=font_2,
                         width=3,
                         justify=tk.CENTER,
                         bd=4,
                         bg="white")
entry_a_36_40.place(relx=0.8, rely=0.8, anchor="sw")
entry_a_36_40.bind("<Escape>", entry_a_36_40_escape)
entry_a_36_40.bind("<Return>", entry_a_36_40_enter)
entry_a_36_40.bind("<FocusOut>", entry_a_36_40_focus_out)

separator_a_36_40 = ttk.Separator(frame_a_36_1, orient='horizontal')
separator_a_36_40.place(relx=0.1, rely=0.8, relwidth=0.65, height=4)

separator_a_36_41 = ttk.Separator(frame_a_36_1, orient='vertical')
separator_a_36_41.place(relx=0.4, rely=0.72, relheight=0.06, width=4)

separator_a_36_42 = ttk.Separator(frame_a_36_1, orient='vertical')
separator_a_36_42.place(relx=0.575, rely=0.72, relheight=0.06, width=4)

frame_a_36_2 = tk.Frame(frame_a_36, bg=color_back)
frame_a_36_2.place(rely=0.85, relwidth=1, relheight=0.15)

label_a_36_21 = tk.Label(frame_a_36_2,
                         text="Press Enter to confirm and continue",
                         font=font_6,
                         bg=color_back,
                         fg='white')
label_a_36_21.place(relx=0.5, rely=0.3, anchor='c')

label_a_36_22 = tk.Label(frame_a_36_2,
                         text="Press Cancel to cancel",
                         font=font_6,
                         bg=color_back,
                         fg='white')
label_a_36_22.place(relx=0.5, rely=0.7, anchor='c')


# noinspection PyUnusedLocal
def to_thirty_six_dialog_cancel(event):
    frame_d_36_escape.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.6)
    frame_d_36_escape.focus_set()


# noinspection PyUnusedLocal
def to_thirty_six_dialog_confirm(event):
    frame_d_36_confirm.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.6)
    frame_d_36_confirm.focus_set()


# noinspection PyUnusedLocal
def to_thirty_six_dialog_no_fields(event):
    empty_fields = ''
    if name_admin_power_line_num.get() == '':
        empty_fields += 'Power Line number\n'
    if name_admin_node_type.get() == '':
        empty_fields += 'Type'
    frame_d_36_no_fields.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.6)
    frame_d_36_no_fields.focus_set()
    label_d_36_no_fields_12.configure(text=empty_fields)


# noinspection PyUnusedLocal
def frame_d_36_no_fields_escape(event):
    frame_d_36_no_fields.place_forget()
    if name_admin_power_line_num.get() == '':
        entry_a_36_20.focus_set()
        entry_a_36_20.select_range(0, tk.END)
    elif name_admin_node_type.get() == '':
        entry_a_36_30.focus_set()
        entry_a_36_30.select_range(0, tk.END)


frame_d_36_no_fields = tk.Frame(frame_a_36,
                                bg=color_back_dialog,
                                highlightcolor=color_border_dialog,
                                highlightthickness=thickness_border_dialog)
frame_d_36_no_fields.bind("<Escape>", frame_d_36_no_fields_escape)
frame_d_36_no_fields.bind("<FocusOut>", frame_d_36_no_fields_escape)


label_d_36_no_fields_11 = tk.Label(frame_d_36_no_fields,
                                   text="Some fields are empty\n"
                                        "To continue Enter the data into",
                                   font=font_2_bold,
                                   bg=color_back_dialog)
label_d_36_no_fields_11.place(relx=0.5, rely=0.3, anchor='s')

label_d_36_no_fields_12 = tk.Label(frame_d_36_no_fields,
                                   text='',
                                   font=font_3_bold,
                                   fg="red",
                                   bg=color_back_dialog)
label_d_36_no_fields_12.place(relx=0.5, rely=0.31, anchor='n')

label_d_36_no_fields_21 = tk.Label(frame_d_36_no_fields,
                                   text="Press ",
                                   font=font_6_bold,
                                   fg=color_front_dialog,
                                   bg=color_back_dialog)
label_d_36_no_fields_21.place(relx=0.05, rely=0.825, anchor='w')

label_d_36_no_fields_22 = tk.Label(frame_d_36_no_fields,
                                   text="CANCEL",
                                   font=font_3_bold,
                                   fg=color_back,
                                   bg=color_back_dialog)
label_d_36_no_fields_22.place(relx=0.19, rely=0.8175, anchor='w')

label_d_36_no_fields_23 = tk.Label(frame_d_36_no_fields,
                                   text="--->",
                                   font=font_2c_bold,
                                   fg=color_front_dialog,
                                   bg=color_back_dialog)
label_d_36_no_fields_23.place(relx=0.49, rely=0.825, anchor='w')

label_d_36_no_fields_24 = tk.Label(frame_d_36_no_fields,
                                   text="to CONTINUE",
                                   font=font_6_bold,
                                   fg=color_front_dialog,
                                   bg=color_back_dialog)
label_d_36_no_fields_24.place(relx=0.64, rely=0.825, anchor='w')


def frame_d_36_cancel(event):
    frame_d_36_escape.place_forget()
    to_thirty_one_admin(event)


# noinspection PyUnusedLocal
def frame_d_36_enter(event):
    frame_d_36_escape.place_forget()
    if name_admin_node_num.get() == '':
        entry_a_36_10.focus_set()
        entry_a_36_10.select_range(0, tk.END)
    elif name_admin_power_line_num.get() == '':
        entry_a_36_20.focus_set()
        entry_a_36_20.select_range(0, tk.END)
    elif name_admin_node_type.get() == '':
        entry_a_36_30.focus_set()
        entry_a_36_30.select_range(0, tk.END)
    elif name_admin_node_status.get() == '':
        entry_a_36_40.focus_set()
        entry_a_36_40.select_range(0, tk.END)
    else:
        entry_a_36_10.focus_set()
        entry_a_36_10.select_range(0, tk.END)


frame_d_36_escape = tk.Frame(frame_a_36,
                             bg=color_back_dialog,
                             highlightcolor=color_border_dialog,
                             highlightthickness=thickness_border_dialog)
frame_d_36_escape.bind("<Return>", frame_d_36_enter)
frame_d_36_escape.bind("<Escape>", frame_d_36_cancel)
# frame_d_36_escape.bind("<FocusOut>", frame_d_36_cancel)

label_d_36_escape_11 = tk.Label(frame_d_36_escape,
                                text="CANCEL",
                                fg="red",
                                font=font_3_bold,
                                bg=color_back_dialog)
label_d_36_escape_11.place(relx=0.5, rely=0.2, anchor='s')

label_d_36_escape_12 = tk.Label(frame_d_36_escape,
                                text="Selected Charger configuration\n"
                                     "(all data entered will be lost)",
                                font=font_2_bold,
                                bg=color_back_dialog)
label_d_36_escape_12.place(relx=0.5, rely=0.2, anchor='n')

label_d_36_escape_21 = tk.Label(frame_d_36_escape,
                                text="Press ",
                                font=font_6_bold,
                                fg=color_front_dialog,
                                bg=color_back_dialog)
label_d_36_escape_21.place(relx=0.02, rely=0.615, anchor='w')

label_d_36_escape_22 = tk.Label(frame_d_36_escape,
                                text="Enter ",
                                font=font_3_bold,
                                fg=color_back,
                                bg=color_back_dialog)
label_d_36_escape_22.place(relx=0.18, rely=0.6, anchor='w')

label_d_36_escape_23 = tk.Label(frame_d_36_escape,
                                text="--->",
                                font=font_2c_bold,
                                fg=color_front_dialog,
                                bg=color_back_dialog)
label_d_36_escape_23.place(relx=0.38, rely=0.613, anchor='w')

label_d_36_escape_24 = tk.Label(frame_d_36_escape,
                                text="to CONTINUE with\nSelected Charger #",
                                font=font_6_bold,
                                fg=color_front_dialog,
                                bg=color_back_dialog)
label_d_36_escape_24.place(relx=0.55, rely=0.615, anchor='w')

label_d_36_escape_31 = tk.Label(frame_d_36_escape,
                                text="Press",
                                font=font_6_bold,
                                fg=color_front_dialog,
                                bg=color_back_dialog)
label_d_36_escape_31.place(relx=0.01, rely=0.865, anchor='w')

label_d_36_escape_32 = tk.Label(frame_d_36_escape,
                                text="Cancel",
                                font=font_3_bold,
                                fg=color_back,
                                bg=color_back_dialog)
label_d_36_escape_32.place(relx=0.15, rely=0.85, anchor='w')

label_d_36_escape_33 = tk.Label(frame_d_36_escape,
                                text="--->",
                                font=font_2c_bold,
                                fg=color_front_dialog,
                                bg=color_back_dialog)
label_d_36_escape_33.place(relx=0.38, rely=0.863, anchor='w')

label_d_36_escape_34 = tk.Label(frame_d_36_escape,
                                text="to CANCEL and\nrestart Charger's setup",
                                font=font_6_bold,
                                fg=color_front_dialog,
                                bg=color_back_dialog)
label_d_36_escape_34.place(relx=0.51, rely=0.865, anchor='w')


# noinspection PyUnusedLocal
def frame_d_36_confirm_cancel(event):
    frame_d_36_confirm.place_forget()
    entry_a_36_10.focus_set()
    entry_a_36_10.select_range(0, tk.END)


frame_d_36_confirm = tk.Frame(frame_a_36,
                              bg=color_back_dialog,
                              highlightcolor=color_border_dialog,
                              highlightthickness=thickness_border_dialog)
frame_d_36_confirm.bind("<Return>", to_thirty_seven_admin)
frame_d_36_confirm.bind("<Escape>", frame_d_36_confirm_cancel)
frame_d_36_confirm.bind("<FocusOut>", frame_d_36_confirm_cancel)


label_d_36_confirm_11 = tk.Label(frame_d_36_confirm,
                                 text="CONFIRM",
                                 fg="red",
                                 font=font_3_bold,
                                 bg=color_back_dialog)
label_d_36_confirm_11.place(relx=0.5, rely=0.2, anchor='s')

label_d_36_confirm_12 = tk.Label(frame_d_36_confirm,
                                 text="Selected Charger configuration",
                                 font=font_2_bold,
                                 bg=color_back_dialog)
label_d_36_confirm_12.place(relx=0.5, rely=0.2, anchor='n')

label_d_36_confirm_21 = tk.Label(frame_d_36_confirm,
                                 text="Press ",
                                 font=font_6_bold,
                                 fg=color_front_dialog,
                                 bg=color_back_dialog)
label_d_36_confirm_21.place(relx=0.03, rely=0.615, anchor='w')

label_d_36_confirm_22 = tk.Label(frame_d_36_confirm,
                                 text="Enter ",
                                 font=font_3_bold,
                                 fg=color_back,
                                 bg=color_back_dialog)
label_d_36_confirm_22.place(relx=0.18, rely=0.6, anchor='w')

label_d_36_confirm_23 = tk.Label(frame_d_36_confirm,
                                 text="--->",
                                 font=font_2c_bold,
                                 fg=color_front_dialog,
                                 bg=color_back_dialog)
label_d_36_confirm_23.place(relx=0.38, rely=0.613, anchor='w')

label_d_36_confirm_24 = tk.Label(frame_d_36_confirm,
                                 text="to CONFIRM and\nSave configuration",
                                 font=font_6_bold,
                                 fg=color_front_dialog,
                                 bg=color_back_dialog)
label_d_36_confirm_24.place(relx=0.54, rely=0.615, anchor='w')

label_d_36_confirm_31 = tk.Label(frame_d_36_confirm,
                                 text="Press",
                                 font=font_6_bold,
                                 fg=color_front_dialog,
                                 bg=color_back_dialog)
label_d_36_confirm_31.place(relx=0.01, rely=0.865, anchor='w')

label_d_36_confirm_32 = tk.Label(frame_d_36_confirm,
                                 text="Cancel",
                                 font=font_3_bold,
                                 fg=color_back,
                                 bg=color_back_dialog)
label_d_36_confirm_32.place(relx=0.15, rely=0.85, anchor='w')

label_d_36_confirm_33 = tk.Label(frame_d_36_confirm,
                                 text="--->",
                                 font=font_2c_bold,
                                 fg=color_front_dialog,
                                 bg=color_back_dialog)
label_d_36_confirm_33.place(relx=0.38, rely=0.863, anchor='w')

label_d_36_confirm_34 = tk.Label(frame_d_36_confirm,
                                 text="to CANCEL and return\nto Selected Charger #",
                                 font=font_6_bold,
                                 fg=color_front_dialog,
                                 bg=color_back_dialog)
label_d_36_confirm_34.place(relx=0.51, rely=0.865, anchor='w')


frame_a_37 = tk.Frame(root, bg=color_back)
frame_a_37.bind("<Escape>", to_second_admin)
frame_a_37.bind("<Return>", to_thirty_one_admin)

frame_a_37_1 = tk.Frame(frame_a_37, bg='white')
frame_a_37_1.place(relwidth=1, relheight=0.85)

label_a_37_11 = tk.Label(frame_a_37_1,
                         text="Charger # ",
                         font=font_4_bold,
                         bg="white")
label_a_37_11.place(relx=0.63, rely=0.25, anchor='e')

# noinspection SpellCheckingInspection
entry_a_37 = tk.Entry(frame_a_37_1,
                      takefocus=0,
                      state=tk.DISABLED,
                      textvariable=name_admin_node_num,
                      font=font_5,
                      width=2,
                      justify=tk.CENTER,
                      bd=4,
                      bg="lightgrey")
entry_a_37.place(relx=0.72, rely=0.25, anchor="c")

label_a_37_12 = tk.Label(frame_a_37_1,
                         text='',
                         font=font_4_bold,
                         bg="white")
label_a_37_12.place(relx=0.5, rely=0.55, anchor='c')

frame_a_37_2 = tk.Frame(frame_a_37, bg=color_back)
frame_a_37_2.place(rely=0.85, relwidth=1, relheight=0.15)

label_a_37_21 = tk.Label(frame_a_37_2,
                         text="Press Enter for next Charger(s) Setup",
                         font=font_6,
                         bg=color_back,
                         fg='white')
label_a_37_21.place(relx=0.5, rely=0.3, anchor='c')

label_a_37_22 = tk.Label(frame_a_37_2,
                         text="Press Cancel for Admin Menu",
                         font=font_6,
                         bg=color_back,
                         fg='white')
label_a_37_22.place(relx=0.5, rely=0.7, anchor='c')


root.bind("<Shift-Up>", switch_to_full_screen)
root.bind("<Shift-Down>", switch_from_full_screen)
root.bind("<Shift-Escape>", to_zero_screen)

frame_num = 0
nodes = Nodes()
users = Users()

root.mainloop()
