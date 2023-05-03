import os
import zipfile
import shutil
import json
import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage, Canvas, ANCHOR, Text, Button, Menu



def rgb_to_hex(rgb):
    rgb = [int(x) for x in rgb[4:-1].split(',')]
    hex_code = ''.join([hex(x)[2:].zfill(2) for x in rgb])
    return '#' + hex_code


def create_tkinter():
    root.geometry('1125x1025')
    root.title('.pkpass Viewer - ' + file_path)
    menu = Menu(root)
    menu.add_command(label='Load', command=load)
    root.config(menu=menu)
    

def open_pkpass():
    # Extract zip file
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall()    
    
    # Bind images
    global logo, strip, qr_image, barcode_image
    logo = PhotoImage(file="logo@3x.png")
    strip = PhotoImage(file="strip@3x.png")
    qr_image = PhotoImage(file="qr_code.png")
    barcode_image = PhotoImage(file="barcode.png")

    # Bind values from json
    with open('pass.json', 'r') as f:
        data = json.load(f)
            
    global organization_name, background_color, foreground_color, label_color, logo_text, ticket_type, article_name, backfield_text, price, code_type, code, expiration_date
      
    organization_name = data['organizationName']
    background_color = data['backgroundColor']
    foreground_color = data['foregroundColor']
    label_color = data['labelColor']
    logo_text = data['logoText']
    ticket_type = data['eventTicket']['secondaryFields'][0]['label']                  ## PKBarcodeFormatQR = QR
    article_name = data['eventTicket']['secondaryFields'][0]['value']
    backfield_text = data['eventTicket']['backFields'][0]['value']
    price = data['eventTicket']['backFields'][1]['value']
    code_type = data['barcode']['format']
    code = data['barcode']['message']
    expiration_date = data['expirationDate']
    

def build_canvas():        
    # Build Canvas
    global canvas
    canvas = Canvas(root, width = 1125, height = 1025, bg=rgb_to_hex(background_color))

    canvas.create_image(0,0, anchor=tk.NW, image=logo)                                                          # Logo
    canvas.create_image(0,150, anchor=tk.NW, image=strip)                                                       # Strip Image
    canvas.create_text(330,60, anchor=tk.NW, text=logo_text, font=('Helvetica 32 bold'))                        # Logo Text
    if ticket_type == 'TICKET_LABEL':                                                                           # Text over Article Name
        canvas.create_text(15, 450, anchor=tk.NW, text='Ticket', fill=rgb_to_hex(label_color))
    else:
        canvas.create_text(15, 450, anchor=tk.NW, text='???')
    canvas.create_text(15, 475, anchor=tk.NW, text=article_name, font=('Helvetica 16'))                         # Article Name
    if code_type == 'PKBarcodeFormatQR':
        canvas.create_image(562,750, anchor=tk.CENTER, image=qr_image)                                          # QR-Code
    else:
        canvas.create_image(562,750, anchor=tk.CENTER, image=barcode_image)                                     # Barcode
    canvas.create_text(550, 965, anchor=tk.N, text=code)                                                        # Code Number
    canvas.pack()

    
def delete_on_closing():
    # Delete extracted files and zip file
    for filename in os.listdir():
        if filename != file_path and filename != "barcode.png" and filename != "qr_code.png" and filename != "run.py":
            try:
                shutil.rmtree(filename)
            except:
                os.remove(filename)
    root.destroy()


def load():
    canvas.pack_forget()
    for filename in os.listdir():
        if filename != file_path and filename != "barcode.png" and filename != "qr_code.png" and filename != "run.py":
            try:
                shutil.rmtree(filename)
            except:
                os.remove(filename)
    main()


def main():
    global file_path

    # Ask user to select a .pkpass file
    file_path = filedialog.askopenfilename(title="Select .pkpass file", filetypes=[("PKPASS Files", "*.pkpass")])

    if not file_path:
        messagebox.showwarning("Warning", "No file selected.")
    else:
        create_tkinter()
        open_pkpass()
        build_canvas()
        root.protocol("WM_DELETE_WINDOW", delete_on_closing)
        root.mainloop()

        
root = tk.Tk()
main()