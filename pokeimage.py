from tkinter import *
from tkinter import ttk
from PokeAPI import get_poke_list, get_pokemon_image_url
import os
import sys
import ctypes
import requests

def main():
    
    script_dir = sys.path[0]
    images_dir = os.path.join(script_dir, 'images')
    if not os.path.isdir(images_dir):
        os.makedirs(images_dir)

    root=Tk()
    root.title('Pokemon Image Viewer')
    app_id = 'COMP593.PokeImageViewer'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    root.iconbitmap(os.path.join(script_dir, 'Poke-Ball.ico'))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.geometry('600x600')

    frm = ttk.Frame(root)
    frm.grid(sticky=(N,S,E,W))
    frm.columnconfigure(0, weight=1)
    frm.rowconfigure(0, weight=80)
    frm.rowconfigure(1, weight=10)
    frm.rowconfigure(2, weight=10)

    #spot for the image of the pokemon
    poke_img = PhotoImage(file=os.path.join(script_dir,'pokeball.png'))
    lbl_img = Label(frm, image=poke_img)
    lbl_img.grid(row=0, column=0)

    poke_list = get_poke_list(limit=1000) 
    poke_list.sort()
    cbo_poke_sel = ttk.Combobox(frm, values=poke_list, state='readonly')
    cbo_poke_sel.set('Select a Pokemon')
    cbo_poke_sel.grid(row=1, column=0)

#set image of pokemon as image in GUI
    def handle_cbo_poke_sel(event):
        poke_name = cbo_poke_sel.get()
        image_url = get_pokemon_image_url(poke_name)
        image_path = os.path.join(images_dir, poke_name + '.png')
        if download_image_from_url(image_url, image_path):
            poke_img['file'] = image_path
            btn_set_dtop.state(['!disabled'])

    cbo_poke_sel.bind('<<ComboboxSelected>>', handle_cbo_poke_sel) #fix

    def btn_set_dtop_click():
        poke_name = cbo_poke_sel.get()
        image_path = os.path.join(images_dir, poke_name + '.png')
        set_dtop_bkgrnd_img(image_path)

    btn_set_dtop = ttk.Button(frm, text='Set as Desktop Image')
    btn_set_dtop.state(['disabled'])
    btn_set_dtop.grid(row=2, column=0, padx=10, pady=10)


    root.mainloop()

def set_dtop_bkgrnd_img(path):
    try:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
    except:
        print('Error setting Desktop Background')

def download_image_from_url(url, path):
    
    if os.path.isfile(path):
        return path
    
    resp_msg = requests.get(url)
    if resp_msg.status_code == 200:
        try:
            img_data = resp_msg.content
            with open(path, 'wb') as fp:
                fp.write(img_data)
            return path
        except:
            return
    else:
        print('Failed to download image.')
        print('Response code:', resp_msg.status_code)
        print(resp_msg.text)

main()