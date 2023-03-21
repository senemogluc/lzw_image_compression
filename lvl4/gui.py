import  tkinter             as      tk
from    tkinter             import  ttk
from    tkinter             import  filedialog, messagebox
from    PIL                 import  Image, ImageTk
import  os
from    image_compression4  import process_red, process_green, process_blue, get_size

current_directory = os.path.dirname(os.path.realpath(__file__)) # Image Compression via LZW\lvl2
original_image_file_path = current_directory + '/template.png'
temp_image_file_path = current_directory + '/result.png'
compressed_path = current_directory + '/compressed.bin'

def start():
   
    if os.path.exists("lvl4/compressed.bin"):
       os.remove("lvl4/compressed.bin")
    open("lvl4/compressed.bin", "x")

    compressed_size = get_size(compressed_path)

    root = tk.Tk()
    root.title('LZW')
    root['bg'] = 'darkslateblue'  

    frame = tk.Frame(root)
    frame.grid(row = 0, column = 0, padx = 15, pady = 15)
    frame['bg'] = 'slateblue'

    # Original image title
    oimg_title_label = ttk.Label(frame, text="Original Image" )
    oimg_title_label.grid(row = 1, column=1, columnspan=2)

    # Decompressed image title
    pimg_title_label = ttk.Label(frame, text="Decompressed Image")
    pimg_title_label.grid(row = 1, column=6, columnspan=3)

    # Original image
    oimg = ImageTk.PhotoImage(file = original_image_file_path)
    oimg_panel = tk.Label(frame, image = oimg)
    oimg_panel.grid(row = 2, column = 0, columnspan = 5, padx = 10, pady = 10)

    # Temporary image
    pimg = ImageTk.PhotoImage(file = original_image_file_path)
    pimg_panel = tk.Label(frame, image = pimg)
    pimg_panel.grid(row = 2, column = 5, columnspan = 5, padx = 10, pady = 10)

    # Original image size
    oimg_size_label = ttk.Label(frame, text="Size of an image is " + get_size(original_image_file_path) + " bytes")
    oimg_size_label.grid(row = 3, column=1, columnspan=2)

    # Temporary image size
    pimg_size_label = ttk.Label(frame, text="Size of 'compressed.bin' file is " + compressed_size + " bytes")
    pimg_size_label.grid(row = 3, column=6, columnspan=1)

    # Open Image button
    btn1 = tk.Button(frame, text = 'Open Image', width = 10)
    btn1['command'] = lambda:open_image(oimg_panel)
    btn1.grid(row = 4, column = 0) 

    # Red Scale button
    btn2 = tk.Button(frame, text = 'Red Scale', bg = 'red', width = 10)
    btn2.grid(row = 4, column = 1)
    btn2['command'] = lambda:[process_red(), modify_image(pimg_panel),modify_size(pimg_size_label)]

    # Green Scale button
    btn2 = tk.Button(frame, text = 'Green Scale', bg = 'green', width = 10)
    btn2.grid(row = 4, column = 2)
    btn2['command'] = lambda:[process_green(), modify_image(pimg_panel),modify_size(pimg_size_label)]

    # Blue Scale button
    btn2 = tk.Button(frame, text = 'Blue Scale', bg = 'blue', width = 10)
    btn2.grid(row = 4, column = 3)
    btn2['command'] = lambda:[process_blue(), modify_image(pimg_panel),modify_size(pimg_size_label)]
    root.mainloop()

def open_image(image_panel):
   global image_file_path   # to modify the global variable image_file_path
   # get the path of the image file selected by the user
   file_path = filedialog.askopenfilename(initialdir = current_directory, 
                                          title = 'Select an image file', 
                                          filetypes = [('png files', '*.png'), 
                                                       ('bmp files', '*.bmp')])
   # display an warning message when the user does not select an image file
   if file_path == '':
      messagebox.showinfo('Warning', 'No image file is selected/opened.')
   # otherwise modify the global variable image_file_path and the displayed image
   else:
      image_file_path = file_path
      img = ImageTk.PhotoImage(file = image_file_path) 
      image_panel.config(image = img) 
      image_panel.photo_ref = img

def modify_image(image_panel):
   
   temp_img = Image.open(temp_image_file_path)
   img = ImageTk.PhotoImage(image = temp_img) 
   image_panel.config(image=img)
   image_panel.photo_ref = (img)

def modify_size(image_size):
   global compressed_size
   updated_size = get_size(compressed_path)
   compressed_size = updated_size
   image_size.config(text="Size of 'compressed.bin' is " + updated_size + " bytes")

if __name__== '__main__':
   start()    