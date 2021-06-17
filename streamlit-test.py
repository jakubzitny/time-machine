import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st
import datetime
import pytz
from streamlit_drawable_canvas import st_canvas
import pickle as pkl
import pytesseract

st.title("Time Machine")
zone = st.selectbox('Time zone',list(pytz.all_timezones))

@st.cache
def draw_canvas():

    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 1)",
        stroke_width=10,
        stroke_color="rgba(0, 0, 0, 1)",
        background_color="rgba(255, 255, 255, 1)",
        update_streamlit=True,
        height=280,
        width=680,
        drawing_mode="freedraw",
        key="canvas",
    )


def convert_to_datetime(numbers: str):
    """
    This takes the for number like "0455", which is the output from the previous "modeling" part.
    It is considered to be UTC time in 24 hour format.
    """
    print(numbers)
    hour = int(numbers[0:2])
    minute = int(numbers[2:4])
    now = datetime.utcnow()
    return now.replace(hour = hour, minute = minute)
    

def convert_from_utc(utc_time: datetime, target_timezone: str = 'America/New_York'):
    """
    Takes a datetime in the UTC timezone and converts it into a desired timezone
    """
    target = timezone(target_timezone)
    return utc_time.astimezone(target)

def convert_time(digits: str, target_timezone: str):
    parsed_datetime = convert_to_datetime(digits)
    output = convert_from_utc(convert_to_datetime(digits), target_timezone)
    output_format = "%H:%M"
    if output.day != parsed_datetime.day:
        output_format += " %x"
    
    output_formatted = output.strftime(output_format)
    
    return f"{digits} in UTC is {output_formatted} in {target_timezone}"

draw_canvas()

# if canvas_result.image_data is not None:
if st.button('Press to process image'):

    # Pass image into tesseract
    # we get e.g., 12 15
    image_to_number = pytesseract.image_to_string(canvas_result.image_data)

    # pass digits to time zone conversion
    str_to_datetime = convert_time(image_to_number,zone)

    # streamlit code to output the converted time
    st.write("Converting time to the time zone " + str(zone))
    st.write(str_to_datetime)
    st.write("With ❤️ from the Deepnote community")
