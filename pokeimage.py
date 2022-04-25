from tkinter import *
from tkinter import ttk
from PokeAPI import get_poke_list, get_pokemon_image_url
import os
import sys
import ctypes
import requests

def main():
    
    #variables defining paths for the script and the images folder the downloaded image will be saved. Create images folder if it doesn't already exist
    script_dir = sys.path[0]
    images_dir = os.path.join(script_dir, 'images')
    if not os.path.isdir(images_dir):
        os.makedirs(images_dir)

    #create the main window itself, including icons
    root=Tk()
    root.title('Pokemon Image Viewer')
    app_id = 'COMP593.PokeImageViewer'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    root.iconbitmap(os.path.join(script_dir, 'Poke-Ball.ico'))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.geometry('600x600')

    #create the frames and determine their locations
    frm = ttk.Frame(root)
    frm.grid(sticky=(N,S,E,W))
    frm.columnconfigure(0, weight=1)
    frm.rowconfigure(0, weight=80)
    frm.rowconfigure(1, weight=10)
    frm.rowconfigure(2, weight=10)

    #where the image of the pokemon is displayed
    poke_img = PhotoImage(file=os.path.join(script_dir,'pokeball.png'))
    lbl_img = Label(frm, image=poke_img)
    lbl_img.grid(row=0, column=0)

    #drop-down box with the list of pokemon the user can choose from
    poke_list = get_poke_list(limit=1000) 
    poke_list.sort()
    cbo_poke_sel = ttk.Combobox(frm, values=poke_list, state='readonly')
    cbo_poke_sel.set('Select a Pokemon')
    cbo_poke_sel.grid(row=1, column=0)

    #set image of pokemon as image in GUI, download if it has not already been downloaded, enable the 'set as desktop' button
    def handle_cbo_poke_sel(event):
        """
        sets the image of the pokemon as the image shown in the GUI. The image will be downloaded if it is not already in the 'images' folder. The 'Set as Desktop' will then be enabled.
        :param: event; user selects the desired pokemon from the dropdown list
        :return: None
        """
        poke_name = cbo_poke_sel.get()
        image_url = get_pokemon_image_url(poke_name)
        image_path = os.path.join(images_dir, poke_name + '.png')
        if download_image_from_url(image_url, image_path):
            poke_img['file'] = image_path
            btn_set_dtop.state(['!disabled'])

    #set the image as desktop background
    cbo_poke_sel.bind('<<ComboboxSelected>>', handle_cbo_poke_sel) 

    def btn_set_dtop_click():
        """
        Upon clicking the 'set as desktop' button, the image will be set as the desktop background. (Calls the function that changes the background)
        :return: None
        """
        poke_name = cbo_poke_sel.get()
        image_path = os.path.join(images_dir, poke_name + '.png')
        set_dtop_bkgrnd_img(image_path)

    btn_set_dtop = ttk.Button(frm, text='Set as Desktop Image', command=btn_set_dtop_click)
    btn_set_dtop.state(['disabled'])
    btn_set_dtop.grid(row=2, column=0, padx=10, pady=10)


    root.mainloop()

#function that sets the desktop background, called within main loop
def set_dtop_bkgrnd_img(path):
    """
    This function is the process of setting the desktop background. Uses the path of the desired image. Called when the 'set as desktop' button is clicked.
    :param: path: the path of the image of the desired pokemon- contained in the 'images folder
    :returns: None
    """
    try:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
    except:
        print('Error setting Desktop Background')
        
#function that downloads the image from the URL, called within main loop
def download_image_from_url(url, path):
    """
    Downloads the image from the URL. 
    :param: url: contained within the dictionary from the PokeAPI
    :param: path: the path to where the image will be saved within the 'images' folder
    :returns: message containing image data
    """
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