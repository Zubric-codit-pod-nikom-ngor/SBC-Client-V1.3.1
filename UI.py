#!/usr/bin/env python
# -*- coding: utf8 -*-

# Мы живём в жестоком мире...

import asyncio
import json
import os
import pickle
import random
import socket
import subprocess
import sys
import threading
import time
import PIL.Image
import io
import sbc
from tkvideo import tkvideo
from moviepy import VideoFileClip
import customtkinter as ctk
import googletrans
from sbc_bootstrapping import *
from functools import lru_cache
from tkinter import filedialog

poo_poo_on_a_stick = "\\"
filepath1 = fr'{__file__[::-1][__file__[::-1].find(poo_poo_on_a_stick):][::-1]}_internal'
if os.access(filepath1, os.R_OK) == True:
    if os.access(filepath1, os.W_OK) == True:
        if os.access(filepath1, os.F_OK) == True:
            pass
        else:
            exit()
    else: exit()
is_valid = True
n = sbc.BlockChain()
local_ip = n.get_local_ip()
external_ip = n.external_ip
if external_ip != None:
    is_valid = True
else:
    is_valid = False
lcb = sbc.BlockChain()
if lcb.external_ip != None:
    is_valid = True
print(external_ip,type(external_ip))

dummy = sbc.Block()
dummy.data = 'None'
dummy.sender = 'No sender'
dummy.creation_time = 'None'

bf1 = None
block_frame = []

block_chosing = 0

manual_adress = ''
data_box_path = None
notif_data = []
notif_running = False
notifs_queue = []
assigned = {}

curr_paths = {}

anim_id = 1
anim_id1 = 2
anim_id2 = 3
current_width = 35.5
current_width1 = 35.5
current_width2 = 35.5
chosen_blocks = {}
created_blc_data_ = []

hvexp = None
slider = None

def ext():
    lcb.joined = False
    lcb.running = False
    try:
        wd.destroy()
    except:
        pass
    # time.sleep(1.5)
    rewrite_settings('assigned', {})
    rewrite_settings('automatic', 0)
    for el in sbc.for_del:
        1
    exit()

@lru_cache()
def clamp(x):
  return max(0, min(x, 255))

def thread_deco(func):
    threading.Thread(target=func,daemon=True).start()

@lru_cache()
def get_hex(color):
    rgb = tuple((c // 256 for c in wd.winfo_rgb(color)))
    rgb = [*rgb]
    for el in range(len(rgb)):
        rgb[el] = rgb[el]-10
    rgb = (clamp(rgb[0]),
           clamp(rgb[1]),
           clamp(rgb[2]))
    return "#{0:02x}{1:02x}{2:02x}".format(*rgb)

def is_ip(ip):
    items = ip.split('.')
    if len(items) != 4:
        notify(translated_data[29], False, True)
        return False
    for el in items:
        if 0 <= int(el) and int(el) <= 255:
            pass
        else:
            notify(translated_data[29], False, True)
            return False
    notify(translated_data[28], True, True, delay=1500)
    return True

def button(root, sizex, sizey, pos, func=None,color='gray', **kwargs) -> ctk.CTkButton:

    pos = [*pos]
    if kwargs == {}:
        btn = ctk.CTkButton(root,
                            sizex, sizey,
                            fg_color=color,
                            hover_color=get_hex(color),
                            command=func)
    else:
        btn = ctk.CTkButton(root,
                            sizex, sizey,
                            fg_color=color,
                            hover_color=get_hex(color),
                            command=func,
                            **kwargs)

    btn.place(x=pos[0], y=pos[1])
    return btn

async def translate_text(lang):
    global translated_data
    translated_data = []
    translation = googletrans.Translator()
    translations = await translation.translate(lang_data,lang)
    for el in translations:
        translated_data.append(el.text)
    for el in range(len(buttons)):
        buttons[el].configure(True,
            text=translated_data[el])

def request_to(command: str):
    request = os.popen(command)
    result = request.read()
    request.close()
    return result

def kill(item):
    item: ctk.CTkOptionMenu
    item.destroy()

def kill_all(items):
    for el in items:
        kill(el)

def rewrite_settings(item, value):
    with open('settings.stng','w') as file:
        settings[item] = value
        json.dump(settings,file)

def translation_tab():
    if states[0] == 0:
        states[0] = states[0]+1
    else:
        states[0] = states[0]-1
    time.sleep(0.15)
    if states[0] == 1:
        global tab_data
        curr_lang = 'en'
        frame1 = ctk.CTkFrame(wd, 550, 240, 0,
                              fg_color='grey14')
        frame1.place(x=0,y=30)
        frame = ctk.CTkFrame(wd,400,223.5,13,
                             fg_color='grey20')
        frame.place(x=75, y=37.5)
        list = ctk.CTkScrollableFrame(wd,364.5,190,0)
        list.place(x=85,y=49.5)
        langs = ['russian',
                 'english',
                 'chinese',
                 'arabic',
                 'japanese',]
        codes = ['ru',
                 'en',
                 'zh',
                 'ar',
                 'ja',]
        tab_data[0].append(frame)
        tab_data[0].append(frame1)
        tab_data[0].append(list)
        for el in range(len(langs)):
            tab_data[0].append(ctk.CTkButton(list,text=langs[el],
                                             command=lambda s=codes[el]: [print(s),
                                                                          asyncio.run(translate_text(s)),
                                                                          translation_tab(),
                                                                          kill_all(tab_data[0]),
                                                                          list.place(x=-500,y=0),
                                                                          rewrite_settings('language',s)],
                                             font=('roboto',16),
                                             fg_color='grey',
                                             hover_color=get_hex('grey'),
                                             corner_radius=0,
                                             width=300))
            tab_data[0][-1].pack(pady=3)
    else:
        kill_all(tab_data[0])

def remodel_list(list_widget, frame):
    def update_ui(items, list_widget, dummy1, label):
        dummy1.destroy()
        label.destroy()
        # if list_widget.winfo_exists():  # Проверяем существование виджета
        #     list_widget.destroy()
        list1 = ctk.CTkScrollableFrame(frame, width=200, height=175, corner_radius=0,
                                       label_text=translated_data[6])
        list1.place(x=175, y=10)
        list1._scrollbar.configure(height=10)
        global current_list_widget
        current_list_widget = list1
        print(f'list got created, items count: {len(items)}')
        print(f'items: {items}')
        if len(items) == 0:
            print('added placeholder')
            label = ctk.CTkLabel(list1, width=160, height=28, fg_color='grey',
                                 text=translated_data[7], corner_radius=6)
            label.pack(pady=5)
        else:
            for el in items:
                label = ctk.CTkLabel(list1, width=160, height=28, fg_color='grey',
                                     text=el, corner_radius=6)
                label.pack(pady=5)
                print(f'added: {el}')
        list1.update()
        frame.update()
    framel = ctk.CTkFrame(wd, 400, 223.5, 13,
                         fg_color='grey20')
    framel.place(x=75, y=37.5)
    dummy1 = ctk.CTkFrame(framel, width=1200, height=223.5, corner_radius=13,
                          fg_color='grey15')
    dummy1.place(x=100, y=67)
    label = ctk.CTkLabel(dummy1, 200, 50, text=translated_data[27], font=('Roboto', 16))
    label.pack(pady=20)
    # progress = ctk.CTkProgressBar(dummy1, width=300)
    # progress.pack(pady=10)
    # progress.set(0)
    # progress.start()
    def fetch_data():
        items = get_open_blockchain()
        print('items:', items)
        wd.after(0, lambda: update_ui(items, list_widget, dummy1, label))
        framel.destroy()

    threading.Thread(target=fetch_data, daemon=True).start()

def remodel_block_ui(block: sbc.Block):
    global block_frame, bf1, block_chosing
    if len(lcb.chain.blocks) == 0:
        pass
    elif [dummy,*lcb.chain.blocks].index(block) == block_chosing:
        pass
    elif [dummy,*lcb.chain.blocks].index(block) > block_chosing:
        block_chosing+=1
    elif [dummy,*lcb.chain.blocks].index(block) < block_chosing:
        block_chosing-=1
    kill_all(block_frame[1:])
    data = str(block.data).lower().capitalize()
    block_frame = [block_frame[0]]
    while '\n' in data:
        data = data.replace('\n', '\-n-')
    block_frame.append(ctk.CTkLabel(block_frame[0], 90, 40, fg_color='grey18',
                                    text=f'{translated_data[18]}: \n{str(block.sender)[:24]}  ', corner_radius=6))
    block_frame[1].place(x=5, y=5)
    try:
        block_frame.append(
            ctk.CTkLabel(block_frame[0], 90, 40, fg_color='grey18', text=f'{translated_data[19]}: \n"{data.split(sbc.BlockChainProtocol.DIVIDER)[1]}" "{data.split(sbc.BlockChainProtocol.DIVIDER)[2][::-1][:data.split(sbc.BlockChainProtocol.DIVIDER)[2][::-1].find("/")][::-1]}"',
                         corner_radius=6))
        block_frame[2].place(x=5, y=50, relwidth=1 - 0.024 * 2.5)
    except:
        block_frame.append(
            ctk.CTkLabel(block_frame[0], 90, 40, fg_color='grey18',
                         text=f'{translated_data[19]}: \n"None" "Non existent file"',
                         corner_radius=6))
        block_frame[2].place(x=5, y=50, relwidth=1 - 0.024 * 2.5)
    block_frame.append(ctk.CTkLabel(block_frame[0], 90, 40, fg_color='grey18',
                                    text=f'{translated_data[20]}: \n{str(block.creation_time)[:24]}  ', corner_radius=6))
    block_frame[3].place(x=5, y=95, relwidth=1 - 0.024 * 2.5)
    block_frame.append(button(block_frame[0], 40, 57.5, (5, 140 + .5), text='<'))
    block_frame.append(button(block_frame[0], 40, 57.5, (198.5 - 40 * 1.5 - 2.5, 140 + .5), text='>'))
    block_frame.append(
        ctk.CTkSwitch(block_frame[0], 81, 57.5, fg_color='grey18', text=translated_data[21], font=(None, 10)))
    block_frame[-1].place(x=50, y=140 + .5, relwidth=0.4)
    try:
        if chosen_blocks[block_chosing] == 1:
            block_frame[-1].toggle()
        else:
            pass
    except Exception as err: print(1,err)
    block_frame[-2].configure(command=lambda: [
        remodel_block_ui([dummy,*lcb.chain.blocks][min(len(lcb.chain.blocks),block_chosing+1)]),
        print(chosen_blocks)])
    block_frame[-3].configure(command=lambda: [
        remodel_block_ui([dummy,*lcb.chain.blocks][max(0,block_chosing-1)]),
        print(chosen_blocks)
    ])

def get_switch_options():
    while True:
        try:
            chosen_blocks[block_chosing] = block_frame[-1].get()
        except: pass
        time.sleep(0.2)

def exp_sequence():
    periods = []
    streak = 0
    for el in chosen_blocks:
        if el != 0:
            if streak == 0 and chosen_blocks[el] == 1:
                periods.append([el-1])
                streak+=1
            elif streak != 0 and chosen_blocks[el] == 1:
                periods[-1].append(el-1)
            elif streak != 0 and chosen_blocks[el] == 0:
                streak = 0
    individuals = []
    while True:
        lns = list(map(lambda item:len(item),periods))
        if lns.count(1) == 0:
            break
        else:
            periods.pop(lns.index(1))
            individuals.append(lns.index(1))

    if periods != []:
        print(f'exporting periods: {periods}')
        for period in periods:
            contents = lcb.chain.fetch_period(period[0],period[-1])
            def ask_directory():
                filename = filedialog.asksaveasfilename(
                    title='Choose directory',
                    filetypes=[("Text files", "*.txt")],
                    defaultextension=".txt"
                )
                return filename
            item = ask_directory()
            while item == None or item == '/':
                item = ask_directory()
            with open(item, 'w') as file:
                file.write('\n'.join(
                    [
                        'connected: ' + str(contents['connected']), 'merged: ' + str(contents['merged']), 'raw data:',
                        *list(map(lambda item: str(item), lcb.chain.blocks))
                    ]
                ))
    if individuals != []:
        print(f'exporting individuals: {individuals}')
        for ind in individuals:
            contents = lcb.chain.fetch_period(ind,ind)
            def ask_directory():
                filename = filedialog.asksaveasfilename(
                    title='Choose directory',
                    filetypes=[("Text files", "*.txt")],
                    defaultextension=".txt"
                )
                return filename
            item = ask_directory()
            while item == None or item == '/':
                item = ask_directory()
            with open(item, 'w') as file:
                file.write('\n'.join(
                    [
                        'connected: ' + str(contents['connected']), 'merged: ' + str(contents['merged']), 'raw data:',
                        *list(map(lambda item: str(item), lcb.chain.blocks))
                    ]
                ))
    elif periods == []:
        print('exporting all')
        contents = lcb.chain.fetch_current()

        def ask_directory():
            filename = filedialog.asksaveasfilename(
                title='Choose directory',
                filetypes=[("Text files", "*.txt")],
                defaultextension=".txt"
            )
            return filename

        item = ask_directory()
        while item == None or item == '/':
            item = ask_directory()
        with open(item, 'w') as file:
            file.write('\n'.join(
                [
                    'connected: ' + str(contents['connected']), 'merged: ' + str(contents['merged']), 'raw data:',
                    *list(map(lambda item: str(item), lcb.chain.blocks))
                ]
            ))

def ui_in_connection():
    if states[5] == 0:
        states[5] = states[5] + 1
    else:
        states[5] = states[5] - 1
    if states[5] == 1:
        global tab_data, block_frame, block_chosing, lcb,bf1,vid_running,manual_adress,data_box_path
        global hvexp

        def path(item):
            global manual_adress
            manual_adress = item
            print(manual_adress)

        def create_block(data):
            ddt = f'0{sbc.BlockChainProtocol.DIVIDER}{data}{sbc.BlockChainProtocol.DIVIDER}{manual_adress}'
            creator = lcb.external_ip
            blc = sbc.Block()
            blc.data = ddt
            blc.sender = creator
            lnmem = len(lcb.chain.blocks)
            if '' in blc.data.split(sbc.BlockChainProtocol.DIVIDER):
                pass
            else:
                lcb.block_buffer.append(blc)

            def count_u(lnmem):
                time.sleep(5)
                print(lnmem,len(lcb.chain.blocks))
                if len(lcb.chain.blocks) != lnmem:
                    notify(translated_data[51], True, True)
                else:
                    notify(translated_data[52], False, True)
            threading.Thread(target=count_u,args=(lnmem,),daemon=True).start()

        def recreate_values():
            def cpt(path):
                pathl = path[::-1][path[::-1].find('/'):][::-1][:-1]
                filename = path[::-1][:path[::-1].find('/')][::-1]
                pathn = pathl[::-1][:pathl[::-1].find('/')][::-1]
                text = pathn + '/' + filename
                return text
            global data_box_path
            while True:
                items = lcb.pres_f
                items = set(map(lambda item: cpt(item),items))
                data_box_path.configure(values=[translated_data[25],*items])
                time.sleep(5)
                # print([translated_data[25],*list(sbc.filenames.values())])

        frame1 = ctk.CTkFrame(wd, 550, 240, 0,
                              fg_color='grey14')
        frame1.place(x=0, y=30)
        bf1 = ctk.CTkFrame(wd, 400, 223.5, 13,
                             fg_color='grey20')
        bf1.place(x=75, y=37.5)
        frfr = ctk.CTkFrame(bf1, 143 + 40, 198.5 + 5, 8,
                     fg_color='grey30')
        frfr.place(x=207, y=10)
        tab_data[5].append(bf1)
        tab_data[5].append(frame1)
        tab_data[5].append(frfr)
        vid_running = False
        block_frame = [
            ctk.CTkFrame(bf1, 143 + 40, 198.5 + 5, 8,
                         fg_color='grey30')]
        block_frame[0].place(x=207, y=10)
        try: test_block = lcb.chain.blocks[0]
        except: test_block = dummy
        remodel_block_ui(test_block)

        scnd_frame = ctk.CTkFrame(bf1, 198.5 + 5 - 50, 143 + 13, 8,
                     fg_color='grey30')
        scnd_frame.place(y=10, x=10)
        creator_lbl = ctk.CTkLabel(scnd_frame, 1, 32.5, fg_color='grey', text=f'{translated_data[18]}:\n{lcb.external_ip}',
                     corner_radius=5)
        creator_lbl.place(x=5, y=5, relwidth=1 - 0.03*2.5)
        data_box_info = ctk.CTkEntry(scnd_frame, 1, 32.5, 5,
                             placeholder_text=translated_data[24])
        data_box_info.place(x=5, y=42.5, relwidth=1 - 0.03*2.5)
        help_lbl = ctk.CTkLabel(scnd_frame, 1, 32.5, fg_color='grey',
                                   text=f'{translated_data[26]}',
                                   corner_radius=5)
        help_lbl.place(x=5, y=80, relwidth=1 - 0.03 * 2.5)
        data_box_path = ctk.CTkOptionMenu(
            scnd_frame,
            values=[translated_data[25], *lcb.pres_f],
            command=path,
            width=1,
            height=32.5,
            fg_color='grey20',
            button_color='grey18',
        )
        data_box_path.set(translated_data[25])
        data_box_path.place(x=5, y=117.5, relwidth=1 - 0.03*2.5)

        threading.Thread(target=recreate_values, daemon=True).start()
        threading.Thread(target=get_switch_options, daemon=True).start()

        submition = button(bf1, 198.5 - 45, 42, (10, 143+28), text=translated_data[22],
                           func=lambda: [create_block(data_box_info.get())])

        #blockchain exporting related things here!

        exp_button = ctk.CTkButton(bf1,35.5,35.5,7,
        fg_color='gray', hover_color=get_hex('gray'),text='📤',command=lambda: exp_sequence())
        def smooth_animate(expand):
            global current_width, anim_id
            if expand:
                target = 150
            else:
                target = 35.5
            diff = target - current_width
            if abs(diff) > 0.5:
                step = diff * 0.7
                current_width += step
                if expand:
                    current_width = min(current_width, 150)
                else:
                    current_width = max(current_width, 35.5)
                # Убираем configure(width=...) и используем только relwidth
                exp_button.place_configure(x=166.5, y=10, relwidth=current_width / 400)
                wd.update_idletasks()
                anim_id = wd.after(12, lambda: smooth_animate(expand))
            else:
                current_width = target
                exp_button.place_configure(x=166.5, y=10, relwidth=current_width / 400)
                wd.update_idletasks()
        def on_enter(event):
            global anim_id
            if anim_id:
                wd.after_cancel(anim_id)
            exp_button.configure(text=translated_data[43])
            smooth_animate(True)
        def on_leave(event):
            global anim_id
            if anim_id:
                wd.after_cancel(anim_id)
            exp_button.configure(text='📤')
            smooth_animate(False)
        exp_button.place(x=166.5,y=10)
        exp_button.bind('<Enter>',lambda e: on_enter(e))
        exp_button.bind('<Leave>', lambda e: on_leave(e))


        range_button = ctk.CTkButton(bf1, 35.5, 35.5, 7,
        fg_color='gray', hover_color=get_hex('gray'),text='[...]')
        def smooth_animate1(expand):
            global current_width1, anim_id1
            if expand:
                target = 150
            else:
                target = 35.5
            diff = target - current_width1
            if abs(diff) > 0.5:
                step = diff * 0.7
                current_width1 += step
                if expand:
                    current_width1 = min(current_width1, 150)
                else:
                    current_width1 = max(current_width1, 35.5)
                # range_button.configure(width=current_width1)  # ← ИСПРАВЛЕНО: было current_width
                range_button.place(x=166.5, y=49.5, relwidth=current_width1 / 400)
                wd.update_idletasks()  # ← ДОБАВЬТЕ ЭТУ СТРОКУ
                anim_id1 = wd.after(12, lambda: smooth_animate1(expand))
            else:
                # Финальная установка точного значения
                current_width1 = target
                # range_button.configure(width=current_width1)
                range_button.place(x=166.5, y=49.5, relwidth=current_width1 / 400)
                wd.update_idletasks()  # ← ДОБАВЬТЕ ЭТУ СТРОКУ
        def on_enter1(event):
            global anim_id1
            if anim_id1:
                wd.after_cancel(anim_id1)
            range_button.configure(text=translated_data[46])
            smooth_animate1(True)
        def on_leave1(event):
            global anim_id1
            if anim_id1:
                wd.after_cancel(anim_id1)
            range_button.configure(text='[...]')
            smooth_animate1(False)
        range_button.place(x=166.5, y=49.5)
        range_button.bind('<Enter>', lambda e: on_enter1(e))
        range_button.bind('<Leave>', lambda e: on_leave1(e))
        def chrng():
            vals = []
            global chosen_blocks
            for el in chosen_blocks:
                if chosen_blocks[el] == 1:
                    vals.append(el)
            if len(vals) != 2:
                notify(f'chosen {len(vals)} blocks instead of 2',False,True,delay=2250)
            else:
                notify(translated_data[45],True,True,delay=2250)
                print(vals)
                for el in range(vals[0],vals[1]+1):
                    chosen_blocks[el] = 1
        range_button.configure(command=chrng)


        def deselect_all():
            global chosen_blocks
            for el in chosen_blocks:
                chosen_blocks[el] = 0
            if chosen_blocks[block_chosing] == 1:
                block_frame[-1].toggle()
        des_button = ctk.CTkButton(bf1, 35.5, 35.5, 7,
        fg_color='gray', hover_color=get_hex('gray'), text='<...>',
        command=lambda: deselect_all())
        def smooth_animate2(expand):
            global current_width2, anim_id2
            if expand:
                target = 150
            else:
                target = 35.5
            diff = target - current_width2
            if abs(diff) > 0.5:
                step = diff * 0.7
                current_width2 += step
                if expand:
                    current_width2 = min(current_width2, 150)
                else:
                    current_width2 = max(current_width2, 35.5)
                # des_button.configure(width=current_width2)
                des_button.place(x=166.5, y=89, relwidth=current_width2 / 400)
                wd.update_idletasks()  # ← ДОБАВЬТЕ ЭТУ СТРОКУ
                anim_id2 = wd.after(12, lambda: smooth_animate2(expand))
            else:
                # Финальная установка точного значения
                current_width2 = target
                # des_button.configure(width=current_width2)
                des_button.place(x=166.5, y=89, relwidth=current_width2 / 400)
                wd.update_idletasks()
        def on_enter2(event):
            global anim_id2
            if anim_id2:
                wd.after_cancel(anim_id2)
            des_button.configure(text=translated_data[53])
            smooth_animate2(True)
        def on_leave2(event):
            global anim_id2
            if anim_id2:
                wd.after_cancel(anim_id2)
            des_button.configure(text='<...>')
            smooth_animate2(False)
        des_button.place(x=166.5, y=89)
        des_button.bind('<Enter>', lambda e: on_enter2(e))
        des_button.bind('<Leave>', lambda e: on_leave2(e))


        def submit_auto_creation():
            while True:
                rewrite_settings('automatic',slider.get())
                time.sleep(5)
        global slider
        slider = ctk.CTkSwitch(bottom_frame, 81, 57.5, bg_color="transparent", text=translated_data[44])
        slider.place(x=7.5, y=-12.5)
        threading.Thread(target=submit_auto_creation,daemon=True).start()
    else:
        kill_all(tab_data[5])

def link_directory(count):
    global curr_paths,assigned,created_files
    def ask_directory():
        filename = filedialog.askdirectory(
            title='Choose directory',
            initialdir=settings['strt_pnt']
        )
        return filename
    filename = ask_directory()
    curr_paths[count] = filename
    rewrite_settings('strt_pnt', filename)

    assigned = {}
    for i,el in enumerate(curr_paths.values()):
        assigned[list(sbc.filenames.values())[i]] = el

    created_files = []
    for el in list(assigned.values()):
        created_files.append(el)
    print(assigned,created_files)

def start_joining(ip):
    if is_ip(ip) == True:
        joining_thrd = threading.Thread(target=lcb.join, args=(ip,),daemon=True)
        joining_thrd.start()
        framel = ctk.CTkFrame(wd, 400, 223.5, 13,
                              fg_color='grey20')
        framel.place(x=75, y=37.5)
        dummy1 = ctk.CTkFrame(framel, width=1200, height=223.5, corner_radius=13,
                              fg_color='grey15')
        dummy1.place(x=100, y=67)
        label = ctk.CTkLabel(dummy1, 200, 50, text=translated_data[47], font=('Roboto', 16))
        label.pack(pady=20)
        wd.update()
        time.sleep(1.3)
        if joining_thrd.is_alive() == False:
            notify(translated_data[48], False, True, delay=2500)
            kill_all([framel, dummy1, label])
            return None
        print(ip)
        label.configure(text=translated_data[31])
        while 'genstart' not in lcb.instructions:
            if 'datapack' in lcb.instructions:
                label.configure(True, text=translated_data[32])
            if 'create' in lcb.instructions:
                label.configure(True, text=translated_data[33])
            wd.update()
        label.configure(True, text=translated_data[34])
        wd.update()
        time.sleep(1)
        kill(label)
        kill(dummy1)
        kill(framel)

        for i,data in enumerate(list(lcb.prev_file_data.keys())[::-1]):
            framel = ctk.CTkFrame(wd, 400, 223.5, 13,
                                  fg_color='grey20')
            framel.place(x=75, y=37.5)
            dummy1 = ctk.CTkFrame(framel, width=150, height=193.5, corner_radius=13,
                                  fg_color='grey15')
            dummy1.place(x=126, y=15)
            label = ctk.CTkLabel(dummy1, 130, 30, text=f'{translated_data[35]}\n{data[::-1][:data[::-1].find("/")][::-1]}', font=('Roboto', 16))
            label.place(x=10,y=10)
            wd.update()

            dir_choose = button(dummy1,130, 35,[10,103.5],lambda item=[i].copy()[0]: link_directory(item),'gray', text=translated_data[36])
            dir_submit = button(dummy1, 130, 35, [10, 148.5],
                                lambda items=[label, dummy1, framel].copy(): [kill_all(items),
                                                                              rewrite_settings("assigned",assigned)] if None not in list(
                                    curr_paths.keys()) else False, 'gray', text=translated_data[37])
            if data == list(lcb.prev_file_data.keys())[-1]:
                dir_submit.configure(False, command=lambda items=[label, dummy1, framel].copy(): [kill_all(items),
                                                                              rewrite_settings("assigned",assigned),
                                                                              ui_in_connection()] if None not in list(
                                    curr_paths.keys()) else False)

def connection_tab():
    if states[1] == 0:
        states[1] = states[1]+1
    else:
        states[1] = states[1]-1
    if states[1] == 1:
        global tab_data
        frame1 = ctk.CTkFrame(wd, 550, 240, 0,
                              fg_color='grey14')
        frame1.place(x=0,y=30)
        frame = ctk.CTkFrame(wd,400,223.5,13,
                             fg_color='grey20')
        frame.place(x=75, y=37.5)
        tab_data[1].append(frame)
        tab_data[1].append(frame1)
        btn = button(frame,160, 45, (82.5-75, 115-30),
                     text=translated_data[4])
        tab_data[1].append(btn)
        list = ctk.CTkScrollableFrame(frame, 200, 175, 0,
                                      label_text=translated_data[6])
        list.place(x=175,y=10)
        list._scrollbar.configure(height=10)
        tab_data[1].append(btn)

        entry = ctk.CTkEntry(frame,160, 30, 5,
                             placeholder_text=translated_data[23])
        entry.place(x=7.5,y=50)
        btn.configure(False,command=lambda: start_joining(entry.get()))
        tab_data[1].append(entry)
        closing_btn = button(frame, 72.5, 25, (122.5 - 75, 50 - 30),
                            text=translated_data[8],
                            func=connection_tab)
        tab_data[1].append(closing_btn)

        remodel_list(list, frame)

        search_btn = button(frame, 100, 50, (112.5 - 75, 170 - 30),
                            text=translated_data[5],
                            func=lambda: remodel_list(list, frame))
        tab_data[1].append(search_btn)
    else:
        kill_all(tab_data[1])

def creation_tab():
    if states[2] == 0:
        states[2] = states[2]+1
    else:
        states[2] = states[2]-1
    if states[2] == 1:
        global tab_data
        frame1 = ctk.CTkFrame(wd, 550, 240, 0,
                              fg_color='grey14')
        frame1.place(x=0,y=30)
        frame = ctk.CTkFrame(wd,300,100,13,
                             fg_color='grey20')
        frame.place(x=130, y=37.5+45)
        labl = ctk.CTkLabel(frame, text=translated_data[9],
                            font=('Barlow Condensed Medium',18))
        labl.place(x=60,y=5)
        sure = button(frame,120,40,(15,55),
                      text=translated_data[10],
                      font=('Barlow Condensed Medium',14))
        quit_tab = button(frame,120,40,(165,55),
                          text=translated_data[11],
                          font=('Barlow Condensed Medium',14))
        tab_data[2].append(sure)
        tab_data[2].append(quit_tab)
        tab_data[2].append(frame)
        tab_data[2].append(frame1)
        tab_data[2].append(labl)
        quit_tab.configure(False, command=lambda: creation_tab())
        sure.configure(False, command=lambda: [choose_files_tab()])
    else:
        kill_all(tab_data[2])

def set_running():
    global lcb
    lcb.running = False

def confirmed_tab():
    if states[3] == 0:
        states[3] = states[3]+1
    else:
        states[3] = states[3]-1
    if states[3] == 1:
        global tab_data, lcb
        frame1 = ctk.CTkFrame(wd, 550, 240, 0,
                              fg_color='grey14')
        frame1.place(x=0, y=30)
        frame = ctk.CTkFrame(wd, 400, 223.5, 13,
                             fg_color='grey20')
        frame.place(x=75, y=37.5)
        tab_data[3].append(frame)
        tab_data[3].append(frame1)
        threading.Thread(target=lcb.create,daemon=True).start()
        list = ctk.CTkScrollableFrame(frame, 235, 175, 0,
                                      label_text=translated_data[12])
        list.place(x=140, y=10)
        list._scrollbar.configure(height=10)
        print('blockchain created')
        threading.Thread(target=push_request,daemon=True,args=(1,)).start()
        rmt = threading.Thread(target=remodeling_cycle,args=(list,frame,),daemon=True)
        rmt.start()
        bt1 = button(frame,115,96.75,[10,10],
                     lambda: set_running(),text=translated_data[49],
                     font=('Roboto',12))
        bt1.place(x=10,y=10, relwidth=0.2875)
        bt2 = button(frame, 115, 96.75, [10, 10+96.75+10],
                     lambda: [set_running(),ext()], text=translated_data[50],
                     font=('Roboto',12))
        bt2.place(x=10,y=10+96.75+10,relwidth=0.2875)
    else:
        kill_all(tab_data[3])

def choose_files_tab():
    if states[6] == 0:
        states[6] = states[6]+1
    else:
        states[6] = states[6]-1
    if states[6] == 1:

        def ask_file():
            filename = filedialog.askopenfilename(
                title='Choose file',
                initialdir=settings['strt_pnt'],
                filetypes=[("All files", "*")]
            )
            return filename

        global tab_data
        frame1 = ctk.CTkFrame(wd, 550, 240, 0,
                              fg_color='grey14')
        frame1.place(x=0,y=30)
        tab_data[6].append(frame1)
        list = ctk.CTkScrollableFrame(frame1, 230, 180, 6,
                                      label_text=translated_data[38])
        list.place(x=150,y=10,relheight=0.5833)
        list._scrollbar.configure(True, height=10)
        add = button(frame1,250,30,[150,160],color='grey',text=translated_data[39], font=("Roboto",14))
        confirm = button(frame1, 250, 30, [150, 200], color='grey', text=translated_data[37], font=("Roboto", 14))
        lcb.sharing_files = []
        def add_file():
            path = ask_file()
            if path != '/':
                pathl = path[::-1][path[::-1].find('/'):][::-1][:-1]
                filename = path[::-1][:path[::-1].find('/')][::-1]
                pathn = pathl[::-1][:pathl[::-1].find('/')][::-1]
                text = pathn+'/'+filename
                rewrite_settings('strt_pnt',pathl)
                if text not in lcb.sharing_files:
                    btn = ctk.CTkButton(list, 210, 30, fg_color='gray',
                                        hover_color=get_hex('gray'),text=text,
                                        command=lambda txt = f'{path}': [btn.destroy(),
                                        lcb.sharing_files.remove(txt)])
                    btn.place(relwidth=0.9131)
                    btn.pack(pady=3)
                    lcb.sharing_files.append(path)
            else:
                notify(translated_data[40],True,False,delay=2000)

        add.configure(command=lambda: add_file())
        confirm.configure(command=lambda: [confirmed_tab(),choose_files_tab(),creation_tab()] if lcb.sharing_files != [] else notify(translated_data[41],False,True,delay=2000))

    else:
        kill_all(tab_data[6])

def get_LAN_servers():
    requested = request_to('arp -a')
    processed = requested.split('\n')
    while '' in processed:
        processed.remove('')
    data = []
    for el in processed[2:]:
        splited = el.split(' ')
        while '' in splited:
            splited.remove('')
        data.append(splited)
    print(data)
    dynamic_tag = data[0][2]
    tagged = []
    for el in data:
        if el[2] == dynamic_tag:
            tagged.append(el)
    ips = map(lambda data: data[0], tagged)
    ips = list(ips)
    ips.append(local_ip)

    book = {'successful': []}
    for ip in ips:
        temp_sock = socket.socket(socket.AF_INET,
                                  socket.SOCK_DGRAM)
        temp_sock.settimeout(0.1)
        try:
            res = temp_sock.connect_ex((ip,15009))
            temp_sock.close()
        except:
            res = 10035
        book[ip] = res
    for el in book:
        if book[el] == 0:
            book['successful'].append(el)
    print(book)
    left = []
    for ip in book['successful']:
        request = subprocess.run(["powershell", "-Command", 'function Test-Port {param([String[]]$ComputerName,[Int]$Port=5985,[Int]$Timeout=350)$result=@();foreach($c in $ComputerName){$r=$c.Split(":");if($r.count-eq1){$h=$c;$p=$Port}elseif($r.count-eq2){$h=$r[0];$p=$r[1]}else{Write-Error "Unknown format: $c";return};$t=New-Object System.Net.Sockets.TcpClient;$o=$t.ConnectAsync($h,$p).Wait($Timeout);$result+=[PSCustomObject]@{RemoteHostname=$h;RemotePort=$p;PortOpened=$o;Timeout=$Timeout;SourceHost=$env:COMPUTERNAME;OriginalName=$c}};return $result}; Test-Port'+f' {ip} 15009 | findstr "PortOpened"'], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)  # Добавляем таймаут для subprocess
        if 'True\n' in request.stdout:
            left.append(ip)
        print(request.stdout)
    return left

def get_open_blockchain():
    # nearby = []
    try:
        artif_ = pull_request()['open_blockchain']
    except:
        artif_ = []
    nearby = get_LAN_servers()
    combined = [*artif_,*nearby]
    return [*set(combined)]

def main_vid():
    frame = ctk.CTkFrame(wd, 205, 205, 5,
                             fg_color='grey17')
    frame.place(x=320, y=50)

    pic_des = ctk.CTkImage(PIL.Image.open('.\\static2.jpg'), size=(196,196))
    static = ctk.CTkLabel(frame, image=pic_des, height=196, width=196, text='')
    static.place(x=5, y=4)

    lbl = ctk.CTkLabel(frame, text='')
    lbl.place(x=5, y=5)
    clip = VideoFileClip('.\\vid_res.mp4')
    clip.with_speed_scaled(0.5)
    while True:
        try:
            player = tkvideo.TkVideo(clip, lbl._label, loop=0, size=(195, 195), hz=60)
            player.play()
            time.sleep(12.42)
            clip = VideoFileClip('.\\vid_res.mp4')
            clip.with_speed_scaled(0.5)
        except: pass

def remodeling_cycle(list,frame):
    global lcb
    while True:
        try:
            list = remodel_information(list,
                                       lcb,
                                       frame)
            time.sleep(5)
        except:
            ext()

def notify(what, good=True, success_mentioned=False, docum_=None, delay=3000):
    global notif_data, notif_running, notifs_queue

    def anim_out(func, x, wdt):
        global notif_data, notif_running, notifs_queue
        a = 0.15
        v = 0
        while x > 0 - (10 + 70 + 10 + 100):
            v += a
            x -= v
            notif_data[0].place(x=x, y=10)
            if func != None:
                notif_data[1].place(x=x + wdt + 10, y=10)
            time.sleep(0.01)
            wd.update()
        kill_all(notif_data)
        notif_data = []
        notif_running = False
        if len(notifs_queue) != 0:
            notify(notifs_queue[0][0],
                   notifs_queue[0][1],
                   notifs_queue[0][2],
                   notifs_queue[0][3],
                   notifs_queue[0][4])
            notifs_queue.pop(0)

    def anim_in(func, x, wdt):
        global notif_data
        a = 0.15
        v = 0
        while x < 10:
            v += a
            x += v
            notif_data[0].place(x=x, y=10)
            if func != None:
                notif_data[1].place(x=x + wdt + 10, y=10)
            time.sleep(0.01)
        wd.after(delay, lambda: anim_out(func, x, wdt))

    def create(what, success, good, func):
        global notif_data,notif_running
        notif_running = True
        wdt = 70
        wdt1 = 100
        x1 = 10
        x = 0-(x1+wdt+10+wdt1)
        if func != None:
            notif_data.append(ctk.CTkButton(wd, wdt, 30, 5,text=translated_data[30],fg_color='gray30', hover_color=get_hex('gray30'),command=func,font=('Roboto', 9)))
            notif_data[-1].place(x=x,y=10, relwidth = 0.132)
            notif_data.append(ctk.CTkLabel(wd, wdt1, 30, 5, fg_color='gray25', text=what, font=('Roboto', 12)))
            if success != False:
                if good == True:
                    notif_data[-1].configure(text_color='green')
                else:
                    notif_data[-1].configure(text_color='red')
            notif_data[-1].place(x=x+wdt+10,y=10)
        else:
            notif_data.append(ctk.CTkLabel(wd, wdt1, 30, 5, fg_color='gray25', text=what, font=('Roboto', 12)))
            if success != False:
                if good == True:
                    notif_data[-1].configure(text_color='green')
                else:
                    notif_data[-1].configure(text_color='red')
            notif_data[-1].place(x=x, y=10)
        wd.after(10, anim_in(func, x, wdt))

    if notif_running == False:
        notif_data = []
        threading.Thread(target=create, daemon=True, args=(what,success_mentioned,good,docum_,)).start()
    else:
        notifs_queue.append([what, good, success_mentioned, docum_, delay])

def remodel_information(list, blc: sbc.BlockChain, frame):
    try:
        global created_blc_data_
        if not frame.winfo_exists():
            ext()
            return None

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            LAN_ip = s.getsockname()[0]
        EXTERNAL_ip = blc.external_ip
        active = blc.running
        requested_current_text = [f'LAN IP: {LAN_ip}',
                                  f'{translated_data[14]}: {EXTERNAL_ip}',
                                  f'{translated_data[15]}: {len(blc.nodes)}',
                                  f'{translated_data[17]}: {active}']
        reqired_to_remodel = False
        for el in created_blc_data_:
            el: ctk.CTkLabel
            if el._text not in requested_current_text:
                reqired_to_remodel = True
                print(el._text)
                break
        if created_blc_data_ == [] or reqired_to_remodel == True:
            list1 = ctk.CTkScrollableFrame(frame, 235, 175, 0, label_text=translated_data[12])
            list1.place(x=140, y=10)
            list1._scrollbar.configure(False,height=5)
            i1 = ctk.CTkLabel(list1, 160, 28, fg_color='grey', text=f'LAN IP: {LAN_ip}', corner_radius=6)
            i1.pack(pady=3)
            i2 = ctk.CTkLabel(list1, 160, 28, fg_color='grey', text=f'{translated_data[14]}: {EXTERNAL_ip}',corner_radius=6)
            i2.pack(pady=3)
            i3 = ctk.CTkLabel(list1, 160, 28, fg_color='grey', text=f'{translated_data[15]}: {len(blc.nodes)}',corner_radius=6)
            i3.pack(pady=3)
            i4 = ctk.CTkLabel(list1, 160, 28, fg_color='grey', text=f'{translated_data[17]}: {active}', corner_radius=6)
            i4.pack(pady=3)
            i5 = ctk.CTkLabel(list1, 160, 28, fg_color='grey', text=f'{translated_data[42]}:',corner_radius=6)
            i5.pack(pady=3)
            for el in lcb.sharing_files:
                ctk.CTkLabel(list1, 160, 28, fg_color='grey', text=f'{el}',
                             corner_radius=6).pack(pady=3)
            created_blc_data_ = [i1, i2, i3, i4]
            return list1
        return list

    except Exception as e:
        print(f"Ошибка в remodel_information: {e}")
        ext()

ctk.set_appearance_mode('dark')

wd = ctk.CTk()
wd.geometry('550x300')
wd.resizable(False,False)
wd.title('SBC services v1.3.1')
wd.wm_iconbitmap('icon.ico')

with open('settings.stng','r') as stngs:
    settings = json.loads(stngs.read())
print(settings)

lang_data = [
    'Connect to\nblockchain',
    'Create blockchain',
    'Help/\nInfo',
    'Change\nlanguage',
    'Connect',
    'Search',
    'Open blockchain',
    'No open connections\nwere found',
    'Back',
    'Are you sure, you want\nto open blockchain?',
    "Yes, i'm sure\n(continue)",
    "No, i'm not sure\n(go to the menu)",
    "Information",
    "IP LAN",
    "IP EXTERNAL",
    "Members",
    "Blocks",
    "Active",
    "Creator",
    "Data",
    "Creation Date",
    "Pick\n\nBlock",
    "submit manually",
    "enter ip...",
    "enter data...",
    "assign file...",
    "/\ Data | file \/",
    "Loading servers...",
    "IP valid!",
    "IP not valid",
    "see more...",
    "Processing commands...",
    "Changing settings",
    "Opening server for\ndistribution",
    "Success!",
    "Requesting\ndirectory\nfor file",
    "choose path",
    "confirm",
    "chosen files",
    "add file",
    "file already chosen!",
    "no files chosen!",
    "sharing files",
    "export data",
    "enable automatic block creation",
    "success!",
    "choose range",
    "attempting connection",
    "Connection Failed!",
    "Close server",
    "Exit",
    "Successful!",
    "Block was rejected!",
    "Deselect all"
]
translated_data = []
buttons = []
states = [0,0,0,0,0,0,0]
tab_data = [[],[],[],[],[],[],[]]

asyncio.run(translate_text(settings['language']))

connect_btn = button(wd,275,60,[17,50],
                     corner_radius=13, color='grey20',
                     text=translated_data[0],
                     font=('Barlow Condensed Medium',18),
                     text_color='grey60',
                     func=lambda: connection_tab())

create_btn = button(wd,275,60,[17,120],
                    corner_radius=13, color='grey20',
                    text=translated_data[1],
                    font=('Barlow Condensed Medium',18),
                    text_color='grey60',
                    func=lambda: creation_tab())

# help_btn = button(wd,132.5,60,[17,190],
#                   corner_radius=13, color='grey20',
#                   text=translated_data[2],
#                   font=('Barlow Condensed Medium',18),
#                   text_color='grey60')

lang_btn = button(wd,275,60,[17,190],
                  func=lambda: translation_tab(),
                  corner_radius=13, color='grey20',
                  text=translated_data[3],
                  font=('Barlow Condensed Medium',18),
                  text_color='grey60')

vid_running = True
vid_thread = threading.Thread(target=main_vid,
                              daemon=True)
vid_thread.start()

buttons.append(connect_btn)
buttons.append(create_btn)
buttons.append(button(wd,1,1,[-100,-100]))
buttons.append(lang_btn)

top_frame = ctk.CTkFrame(wd, 550, 30, 0)
top_frame.place(x=0,y=0)
bottom_frame = ctk.CTkFrame(wd, 550, 30, 0)
bottom_frame.place(x=0,y=270)

def wait_assignment():
    time.sleep(1)
    wd.bind("<Unmap>", lambda event: [wd.update_idletasks(),wd.attributes('-disabled', 1)])
    wd.bind("<Map>", lambda event: [wd.update_idletasks(),wd.attributes('-disabled', 0)])
threading.Thread(target=wait_assignment,daemon=True).start()

if is_valid == False:
    os.system('error.vbs')
    exit()

wd.protocol('WM_DELETE_WINDOW',ext)
wd.mainloop()