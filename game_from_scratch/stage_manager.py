from tkinter import *
import json
import tkinter

def change_selected_item():

    def change_time():
        time = time_entry.get()
        if time.isnumeric():
            time = int(time)

            with open('stage1_test.json', 'r+') as f:
                data = json.load(f)
                data['enemy'][0]['time'] = time
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()

                change_object.clipboard_clear()
                change_object.clipboard_append()
                change_object.update()
            
        change_object.destroy()

    change_object = Tk()
    change_object.geometry('600x400')
    
    selected_list = Listbox(change_object, height=len(list_box.curselection()), width=95)

    selected_counter = 0
    for index in list_box.curselection():
        selected_counter += 1
        selected_list.insert(selected_counter,list_box.get(index))

    time_entry = Entry(change_object)

    change_button = tkinter.Button(change_object, text='change time', command=change_time)

    selected_list.pack()
    time_entry.pack()
    change_button.pack()

    change_object.mainloop()

json_stage = json.load(open('stage1_test.json', 'r+'))
base_json = json_stage['enemy']

gui = Tk()
gui.geometry('600x400')

list_box = Listbox(gui,height=23, width=95, selectmode=EXTENDED)

json_counter = 0
for item in base_json:
    json_counter += 1
    list_box.insert(json_counter,item)

enter_button = tkinter.Button(gui, text='select objects', command=change_selected_item)

list_box.pack()
enter_button.pack()

gui.mainloop()