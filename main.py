from tkinter import *
from tkinter import ttk
import webbrowser
from pandas import DataFrame
import os
from scrape import amazon, flipkart, rd
from multiprocessing import Process,Queue
from threading import Thread

# Create the main window
root = Tk()
root.title("SHOP SMART")

# Maximize the window
screen_width = root.winfo_screenwidth() #1600
screen_height = root.winfo_screenheight()-900//12 #825
root.geometry(f"{screen_width}x{screen_height}")

# Define colors
color1 = '#040D12'
color2 = '#183D3D'
color3 = '#5C8374'
color4 = '#93B1A6'

# Background color
root.configure(bg = color1)

# Animation
animation_speed = 1
animation_frames = 150

# Function to define label
def create_label(label_text, label_bg, label_fg, label_font_name, label_font_size, label_font_style, label_relx, label_rely):
    label_name = Label(root, text = label_text, bg = label_bg, fg = label_fg, font = (label_font_name, label_font_size, label_font_style))
    label_name.place(relx = label_relx, rely = label_rely)
    return label_name

# Function to define frame
def create_frame(frame_bg, frame_width, frame_height, frame_relx, frame_rely):
    frame_name = Frame(root, bg = frame_bg, width = frame_width, height = frame_height)
    frame_name.place(relx = frame_relx, rely = frame_rely)
    return frame_name

# Function to define input
def create_input(input_bg, input_fg, input_insertbackground, input_width, input_font_name, input_font_size, input_font_style, input_relx, input_rely):
    input_name = Entry(root, bg = input_bg, fg = input_fg, insertbackground = input_insertbackground, width = input_width, font = (input_font_name, input_font_size, input_font_style))
    input_name.place(relx = input_relx, rely = input_rely)
    return input_name

# Function to define button
def create_button(button_text, button_bg, button_fg, button_width, button_height, button_font_name, button_font_size, button_font_style, button_command, button_relx, button_rely):

    def on_button_enter(e):
        button_name['background'] = button_fg
        button_name['foreground'] = button_bg

    def on_button_leave(e):
        button_name['background'] = button_bg
        button_name['foreground'] = button_fg

    button_name = Button(root, width = button_width, height = button_height, text = button_text, fg = button_fg, bg = button_bg, border = 0, activeforeground = button_bg, activebackground = button_fg, command = button_command, font = (button_font_name, button_font_size, button_font_style))

    button_name.bind("<Enter>", on_button_enter)
    button_name.bind("<Leave>", on_button_leave)

    button_name.place(relx = button_relx, rely = button_rely)
    return button_name

# Function to define combobox
def create_combobox(combobox_relx, combobox_rely):
    ttk.Style().configure("TCombobox", fieldbackground = color3)

    combobox_name = ttk.Combobox(root, values = ["Website: A-Z", "Website: Z-A", "Price: Low to High", "Price: High to Low", "Customer Rating: Low to High", "Customer Rating: High to Low", "Delivery Date: Ascending", "Delivery Date: Descending"], font = ("Arial", 18), width = 25)
    combobox_name.set("A-Z")

    combobox_name.place(relx = combobox_relx, rely = combobox_rely)
    return combobox_name

# Function to define URL button
def create_URL_button(button_text, button_bg, button_fg, button_width, button_height, button_font_name, button_font_size, button_font_style, button_url, button_relx, button_rely):

        def on_button_enter(e):
            button_name['background'] = button_fg
            button_name['foreground'] = button_bg
    
        def on_button_leave(e):
            button_name['background'] = button_bg
            button_name['foreground'] = button_fg
    
        button_name = Button(root, width = button_width, height = button_height, text = button_text, fg = button_fg, bg = button_bg, border = 0, activeforeground = button_bg, activebackground = button_fg, command = lambda: webbrowser.open(button_url), font = (button_font_name, button_font_size, button_font_style))
    
        button_name.bind("<Enter>", on_button_enter)
        button_name.bind("<Leave>", on_button_leave)
    
        button_name.place(relx = button_relx, rely = button_rely)
        return button_name

# Function to resize label
def resize_label(label_name, label_new_font_size):
    label_name.config(font = (label_name["font"].split()[0], int(label_new_font_size)))
    root.update()
    return label_name

# Function to resize frame
def resize_frame(frame_name, frame_new_width, frame_new_height):
    frame_name.config(width = frame_new_width, height = frame_new_height)
    root.update()
    return frame_name

# Function to resize input
def resize_input(input_name, input_new_width):
    input_name.config(width = input_new_width)
    root.update()
    return input_name

# Function to resize button
def resize_button(button_name, button_new_width, button_new_height):
    button_name.config(width = button_new_width, height = button_new_height)
    root.update()
    return button_name

# Function to move label
def move(name, start_relx, start_rely, end_relx, end_rely):

    # Calculate the change in relative position for each frame
    dx = (end_relx - start_relx) / animation_frames
    dy = (end_rely - start_rely) / animation_frames

    def animate(frame):
    
        if frame < animation_frames:

            nonlocal name, start_relx, start_rely

            start_relx += dx
            start_rely += dy

            name.place(relx = start_relx, rely = start_rely)
            root.after(animation_speed, animate, frame + 1)
    
    animate(0)

    return name

# Title Search for Anything
title_search = create_label("SEARCH", color1, color4, "Arial", screen_width//25, "bold", 0, 0) 
title_for = create_label("for", color1, color3, "Arial", screen_width//25, "italic", 0.14, 0.11)
title_anything = create_label("ANYTHING", color1, color4, "Arial", screen_width//25, "bold", 0.2, 0.2)

# Frame, title, search box
center_frame = create_frame(color2, 1150, 300, 0.15, 0.35)

title_product_name = create_label("Product name: ", color2, color4, "Arial", screen_width//60, "normal", 0.18, 0.4)
product_name_input = create_input(color1, color4, color2, screen_width//42, "Arial", screen_width//60, "bold", 0.36, 0.4)

title_pin_code = create_label("Pin code: ", color2, color4, "Arial", screen_width//60, "normal", 0.18, 0.5)
pin_code_input = create_input(color1, color4, color2, screen_width//42, "Arial", screen_width//60, "bold", 0.36, 0.5)

def throw():

    global title_website, title_price, title_rating, title_date, title_URL
    global result1_frame, result2_frame, result3_frame, result1_website_label, result2_website_label, result3_website_label, result1_price_label, result2_price_label, result3_price_label 
    global result1_rating_label, result2_rating_label, result3_rating_label, result1_date_label, result2_date_label, result3_date_label, result1_url_button, result2_url_button, result3_url_button 

    # Heading move
    title_website = move(title_website, 0.1, 0.39, -1, 0.42)
    title_price = move(title_price, 0.3, 0.39, -1, 0.42)
    title_rating = move(title_rating, 0.43, 0.39, -1, 0.42)
    title_date = move(title_date, 0.55, 0.39, -1, 0.42)
    title_URL = move(title_URL, 0.8, 0.39, -1, 0.42)
    
    # Result frames move
    result1_frame = move(result1_frame, 0.06, 0.45, -1, 0.48)
    result2_frame = move(result2_frame, 0.06, 0.6, -1, 0.63)
    result3_frame = move(result3_frame, 0.06, 0.75, -1, 0.78)

    # Website details move
    result1_website_label = move(result1_website_label, 0.1, 0.49, -1, 0.52)
    result2_website_label = move(result2_website_label, 0.1, 0.64, -1, 0.67)
    result3_website_label = move(result3_website_label, 0.1, 0.79, -1, 0.82)

    # Price details move
    result1_price_label = move(result1_price_label, 0.3, 0.49, -1, 0.52)
    result2_price_label = move(result2_price_label, 0.3, 0.64, -1, 0.67)
    result3_price_label = move(result3_price_label, 0.3, 0.79, -1, 0.82)

    # Rating details move
    result1_rating_label = move(result1_rating_label, 0.43, 0.49, -1, 0.52)
    result2_rating_label = move(result2_rating_label, 0.43, 0.64, -1, 0.67)
    result3_rating_label = move(result3_rating_label, 0.43, 0.79, -1, 0.82)

    # Date of delivery details move
    result1_date_label = move(result1_date_label, 0.55, 0.49, -1, 0.52)
    result2_date_label = move(result2_date_label, 0.55, 0.64, -1, 0.67)
    result3_date_label = move(result3_date_label, 0.55, 0.79, -1, 0.82)

    # URL details move
    result1_url_button = move(result1_url_button, 0.8, 0.49, -1, 0.52)
    result2_url_button = move(result2_url_button, 0.8, 0.64, -1, 0.67)
    result3_url_button = move(result3_url_button, 0.8, 0.79, -1, 0.82)


def pull():

    global title_website, title_price, title_rating, title_date, title_URL
    global result1_frame, result2_frame, result3_frame, result1_website_label, result2_website_label, result3_website_label, result1_price_label, result2_price_label, result3_price_label 
    global result1_rating_label, result2_rating_label, result3_rating_label, result1_date_label, result2_date_label, result3_date_label, result1_url_button, result2_url_button, result3_url_button 

    # Heading move
    title_website = move(title_website, 0.1, 2, 0.1, 0.42)
    title_price = move(title_price, 0.1, 2, 0.3, 0.42)
    title_rating = move(title_rating, 0.1, 2, 0.43, 0.42)
    title_date = move(title_date, 0.1, 2, 0.55, 0.42)
    title_URL = move(title_URL, 0.1, 2, 0.8, 0.42)
                
    # Result frames move
    result1_frame = move(result1_frame, 0.06, 2, 0.06, 0.48)
    result2_frame = move(result2_frame, 0.06, 2, 0.06, 0.63)
    result3_frame = move(result3_frame, 0.06, 2, 0.06, 0.78)
   
    # Website details move
    result1_website_label = move(result1_website_label, 0.1, 2, 0.1, 0.52)
    result2_website_label = move(result2_website_label, 0.1, 2, 0.1, 0.67)
    result3_website_label = move(result3_website_label, 0.1, 2, 0.1, 0.82)

    # Price details move
    result1_price_label = move(result1_price_label, 0.1, 2, 0.3, 0.52)
    result2_price_label = move(result2_price_label, 0.1, 2, 0.3, 0.67)
    result3_price_label = move(result3_price_label, 0.1, 2, 0.3, 0.82)

    # Rating details move
    result1_rating_label = move(result1_rating_label, 0.1, 2, 0.43, 0.52)
    result2_rating_label = move(result2_rating_label, 0.1, 2, 0.43, 0.67)
    result3_rating_label = move(result3_rating_label, 0.1, 2, 0.43, 0.82)

    # Date of delivery details move
    result1_date_label = move(result1_date_label, 0.1, 2, 0.55, 0.52)
    result2_date_label = move(result2_date_label, 0.1, 2, 0.55, 0.67)
    result3_date_label = move(result3_date_label, 0.1, 2, 0.55, 0.82)

    # URL details move
    result1_url_button = move(result1_url_button, 0.1, 2, 0.8, 0.52)
    result2_url_button = move(result2_url_button, 0.1, 2, 0.8, 0.67)
    result3_url_button = move(result3_url_button, 0.1, 2, 0.8, 0.82)

# Function to sort based on field
def sort(data, field):
    sorted_data = dict(sorted(data.items(), key=lambda item: item[1][field]))
    return sorted_data

# Sort combobox selection
def on_sort(event):

    global data
    selected_sort_name = sort_combobox.get()

    if selected_sort_name == "Website: Z-A": display_data = list(sort(data, "website").items())[::-1]
    elif selected_sort_name == "Price: Low to High": display_data = list(sort(data, "price").items())
    elif selected_sort_name == "Price: High to Low": display_data = list(sort(data, "price").items())[::-1]
    elif selected_sort_name == "Customer Rating: High to Low": display_data = list(sort(data, "rating").items())[::-1]
    elif selected_sort_name == "Customer Rating: Low to High": display_data = list(sort(data, "rating").items())
    elif selected_sort_name == "Delivery Date: Ascending": display_data = list(sort(data, "date-sort").items())
    elif selected_sort_name == "Delivery Date: Descending": display_data = list(sort(data, "date-sort").items())[::-1]
    else: display_data = list(sort(data, "website").items())

    # Change website name
    result1_website_label["text"] = display_data[0][1]["website"]
    result2_website_label["text"] = display_data[1][1]["website"]
    result3_website_label["text"] = display_data[2][1]["website"]

    # Change website name
    result1_price_label["text"] = display_data[0][1]["price"]
    result2_price_label["text"] = display_data[1][1]["price"]
    result3_price_label["text"] = display_data[2][1]["price"]

    # Change website name
    result1_rating_label["text"] = display_data[0][1]["rating"]
    result2_rating_label["text"] = display_data[1][1]["rating"]
    result3_rating_label["text"] = display_data[2][1]["rating"]

    # Change website name
    result1_date_label["text"] = display_data[0][1]["date"]
    result2_date_label["text"] = display_data[1][1]["date"]
    result3_date_label["text"] = display_data[2][1]["date"]
        
    # Change the website url
    result1_URL_button = command = lambda: webbrowser.open(display_data[0][1]["url"])
    result2_URL_button = command = lambda: webbrowser.open(display_data[1][1]["url"])
    result3_URL_button = command = lambda: webbrowser.open(display_data[2][1]["url"])
    
    pull()

# Share button
def on_share():
    global data
    product_name = product_name_input.get()
    df, excel_file = DataFrame(data).T, ""
    df = df[['website', 'price', 'rating', 'date', 'url']]
    for i in product_name.split(): excel_file += i + '_'
    excel_file += "results.xlsx"
    df.to_excel(excel_file, index=False)
    os.system('xdg-open ' + excel_file)

data, product_name = {}, ""

# Search button and function on search
def on_search():
    global data, pin_code_input, title_pin_code
    global search_button_already_pressed, title_search, title_for, title_anything, center_frame, title_product_name, product_name_input, search_button, sort_combobox, title_website, title_price, title_rating, title_date, title_URL, result1_frame, result2_frame, result3_frame
    global result1_website_label, result2_website_label, result3_website_label, result1_price_label, result2_price_label, result3_price_label, result1_rating_label, result2_rating_label, result3_rating_label, result1_date_label, result2_date_label, result3_date_label, result1_url_button, result2_url_button, result3_url_button

    product_name = product_name_input.get()
    pincode = pin_code_input.get()

    Q = Queue()

    # Get details
    if __name__ == "__main__":
        p1 = Process(target=amazon, args=(product_name, pincode, Q))
        p1.start()
        p2 = Process(target=flipkart, args=(product_name, pincode, Q))
        p2.start()
        p3 = Process(target=rd, args=(product_name, pincode, Q))
        p3.start()

        p1.join()
        p2.join()
        p3.join()

    website_data = [Q.get(), Q.get(), Q.get()]
    website_data.sort(key=lambda item: item[3])

    # Get details
    amazon_data = website_data[0]
    flipkart_data = website_data[1]
    relianceD_data = website_data[2]
    
    data = {
            "result1": {"website": "Amazon", "price": amazon_data[0], "rating": str(amazon_data[1]), "date": amazon_data[2], "url": amazon_data[3], "date-sort": amazon_data[4]},
            "result2": {"website": "Flipkart", "price": flipkart_data[0], "rating": str(flipkart_data[1]), "date": flipkart_data[2], "url": flipkart_data[3], "date-sort": flipkart_data[4]},
            "result3": {"website": "Reliance Digital", "price": relianceD_data[0], "rating": str(relianceD_data[1]), "date": relianceD_data[2], "url": relianceD_data[3], "date-sort": relianceD_data[4]}
    }

    if search_button_already_pressed == 0:

        search_button_already_pressed = 1

        # Resize elements
        title_search = resize_label(title_search, screen_width//35)
        title_for = resize_label(title_for, screen_width//35)
        title_anything = resize_label(title_anything, screen_width//35)

        center_frame = resize_frame(center_frame, 1400, 100)
        
        # move the elements to new position
        title_search = move(title_search, 0, 0, 0, 0)
        title_for = move(title_for, 0.14, 0.11, 0.165, 0)
        title_anything = move(title_anything, 0.2, 0.2, 0.215, 0)

        center_frame = move(center_frame, 0.18, 0.4, 0.06, 0.15)
        title_product_name = move(title_product_name, 0.18, 0.4, 0.07, 0.18)
        product_name_input = move(product_name_input, 0.36, 0.4, 0.24, 0.18)

        # move pincode entries
        title_pin_code = move(title_pin_code, 0.18, 0.5, -1, 0.5)
        pin_code_input = move(pin_code_input, 0.36, 0.5, 2, 0.5)

        search_button = move(search_button, 0.42, 0.5, 0.74, 0.18)

        # Sort combobox and title
        title_product_name = create_label("Search results: ", color1, color4, "Arial", screen_width//60, "bold", -1, 0.33)
        title_product_name = move(title_product_name, -1, 0.33, 0.07, 0.33)
        
        sort_combobox = create_combobox(2, 0.33)
        sort_combobox = move(sort_combobox, 2, 0.33, 0.7, 0.33)
        sort_combobox.bind("<<ComboboxSelected>>", on_sort)

        share_button = create_button("Share Results", color3, color1, screen_width//100, screen_height//450, "Arial", screen_width//100, "normal", on_share, 0, 0.7)
        share_button = move(share_button, 2, 0.025, 0.83, 0.025)
        

    else: # Throw the results already been showed

        throw()
    
        # Reset the value of combobox
        sort_combobox.set("A-Z")

    sorted_data = sort(data, "website")

    # Result frames create
    result1_frame = create_frame(color2, 1400, 100, 0.06, 2)
    result2_frame = create_frame(color2, 1400, 100, 0.06, 2)
    result3_frame = create_frame(color2, 1400, 100, 0.06, 2)

    # Heading for Website, price, rating, URL
    title_website = create_label("Website", color1, color4, "Arial", 20, "italic", 0.1, 0.42)
    title_price = create_label("Price", color1, color4, "Arial", 20, "italic", 0.3, 0.42)
    title_rating = create_label("Rating", color1, color4, "Arial", 20, "italic", 0.43, 0.42)
    title_date = create_label("Delivery date", color1, color4, "Arial", 20, "italic", 0.55, 0.42)
    title_URL = create_label("URL", color1, color4, "Arial", 20, "italic", 0.8, 0.42)

    # Website details
    result1_website_label = create_label(sorted_data["result1"]["website"], color2, color4, "Arial", 20, "normal", 0.1, 0.52)
    result2_website_label = create_label(sorted_data["result2"]["website"], color2, color4, "Arial", 20, "normal", 0.1, 0.67)
    result3_website_label = create_label(sorted_data["result3"]["website"], color2, color4, "Arial", 20, "normal", 0.1, 0.82)

    # Price details
    result1_price_label = create_label(sorted_data["result1"]["price"], color2, color4, "Arial", 20, "normal", 0.3, 0.52)
    result2_price_label = create_label(sorted_data["result2"]["price"], color2, color4, "Arial", 20, "normal", 0.3, 0.67)
    result3_price_label = create_label(sorted_data["result3"]["price"], color2, color4, "Arial", 20, "normal", 0.3, 0.82)

    # Rating details
    result1_rating_label = create_label(sorted_data["result1"]["rating"], color2, color4, "Arial", 20, "normal", 0.43, 0.52)
    result2_rating_label = create_label(sorted_data["result2"]["rating"], color2, color4, "Arial", 20, "normal", 0.43, 0.67)
    result3_rating_label = create_label(sorted_data["result3"]["rating"], color2, color4, "Arial", 20, "normal", 0.43, 0.82)

    # Date of delivery details
    result1_date_label = create_label(sorted_data["result1"]["date"], color2, color4, "Arial", 20, "normal", 0.55, 0.52)
    result2_date_label = create_label(sorted_data["result2"]["date"], color2, color4, "Arial", 20, "normal", 0.55, 0.67)
    result3_date_label = create_label(sorted_data["result3"]["date"], color2, color4, "Arial", 20, "normal", 0.55, 0.82)

    # URL details
    result1_url_button = create_URL_button("Visit", color4, color2, screen_width//200, screen_height//450, "Arial", screen_width//80, "normal", sorted_data["result1"]["url"], 0.8, 0.52)
    result2_url_button = create_URL_button("Visit", color4, color2, screen_width//200, screen_height//450, "Arial", screen_width//80, "normal", sorted_data["result2"]["url"], 0.8, 0.67)
    result3_url_button = create_URL_button("Visit", color4, color2, screen_width//200, screen_height//450, "Arial", screen_width//80, "normal", sorted_data["result3"]["url"], 0.8, 0.82)

    pull()
    
# Define a bit for search button already pressed
search_button_already_pressed = 0
search_button = create_button("Search", color4, color2, screen_width//100, screen_height//450, "Arial", screen_width//80, "normal", on_search, 0.42, 0.6)

# Bind enter key with search button
def enter_key(e): on_search()
root.bind("<Return>", enter_key)

# Tkinter mainloop
root.mainloop()
