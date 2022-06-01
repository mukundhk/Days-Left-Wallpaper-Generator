import datetime
from PIL import Image, ImageFont, ImageDraw
import ctypes
import os
import json
import random

def remaining_days():
    with open("settings.json","r") as settings_file:
        settings = json.load(settings_file)
    final_date_elements = settings["date"].split("-")
    day,month,year = int(final_date_elements[0]),int(final_date_elements[1]),int(final_date_elements[2])
    
    today_epoch = datetime.datetime.now().timestamp()
    final_epoch = datetime.datetime(year,month,day).timestamp()

    difference = int(final_epoch - today_epoch)
    days = difference//86400 + 1
    weeks = days//7
    rem_days = days%7

    return (days,weeks,rem_days)

def days_to_text():
    today = datetime.datetime.now().strftime("%B %d, %Y")
    final = datetime.datetime(2022, 8, 1, 0, 0).strftime("%B %d, %Y")
    return (today,final)

def text(remaining_days,days_text):
    text = f"""{days_text[0]}
    
Just {remaining_days[0]} days left
{remaining_days[1]} weeks and {remaining_days[2]} days
for
{days_text[1]}
"""
    return text

def pick_colors():
    with open("settings.json","r") as settings_file:
        settings = json.load(settings_file)
    theme = settings["theme"]
    with open(r".\assets\colors.json","r") as colors_file:
        colors = json.load(colors_file)
    chosen_colors = random.choice(colors[theme])
    
    bg_color = tuple(chosen_colors["background"])
    text_color = tuple(chosen_colors["text"])

    return (bg_color,text_color)
    
def create_wallpaper(bg_color,text_color,text):
    width, height = 1920, 1080
    image = Image.new("RGBA",(width,height),color=bg_color)
    draw = ImageDraw.Draw(image)

    textfont = ImageFont.truetype("assets\\Nunito-VariableFont_wght.ttf", 50)
    draw.text((width/2,height/2), text, align="center", anchor="mm", font=textfont, fill=text_color)

    image.save(r".\assets\wallpaper.png", "PNG")

def set_wallpaper():
    absolute_path = os.path.abspath(r".\assets\wallpaper.png")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, absolute_path , 0)

if __name__ == "__main__":
    remaining_days = remaining_days()
    days_text = days_to_text()
    final_text = text(remaining_days, days_text)
    bg_color,text_color = pick_colors()
    create_wallpaper(bg_color,text_color,final_text)
    set_wallpaper()