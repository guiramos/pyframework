import base64
import io
import json
import re
import textwrap

import regex

import os
import pytz
import datetime

from PIL import Image

from IPython.display import Markdown

UNAUTHORIZED_MESSAGE = "Unauthorized: Invalid client token."
BAD_REQUEST_MESSAGE = "Bad Request: 'ticker' and 'operation' must be present in the request body."


def convert_time_to_datetime(time_in_milliseconds, timezone_str):
    # Convert time from milliseconds to seconds and create a datetime object
    datetime_obj = datetime.datetime.fromtimestamp(time_in_milliseconds / 1000)

    # Create a timezone object
    timezone = pytz.timezone(timezone_str)

    # Convert the datetime object to the desired timezone
    datetime_obj_in_timezone = datetime_obj.astimezone(timezone)

    return datetime_obj_in_timezone


def convert_utcstr_to_tz(utc_time, target_tz='US/Eastern'):
    utc_timestamp = datetime.datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%SZ")
    utc_timestamp = pytz.timezone('UTC').localize(utc_timestamp)

    return utc_timestamp.astimezone(pytz.timezone(target_tz))


def convert_utc_to_tz(utc_timestamp, target_tz='US/Eastern'):
    return utc_timestamp.astimezone(pytz.timezone(target_tz))


def get_today_date():
    tz = pytz.timezone(os.environ.get('TZ'))
    return datetime.datetime.now(tz)


def get_date_formatted(date=None):
    if date is None:
        date = get_today_date()
    return date.strftime('%Y-%m-%d')


def current_datetime_tz():
    return datetime.datetime.now(pytz.timezone(os.environ.get('TZ')))


def date_time_formatted(date_time=None):
    if date_time is None:
        date_time = current_datetime_tz()
    return date_time.strftime('%Y-%m-%dT%H:%M:%S')


def concatenate_contents_from_context(list_of_objects, start_index):
    return " ".join([item["content"] for item in list_of_objects[start_index:]])


def remove_enclosed_expression(text: str) -> str:
    return re.sub(r'<.*?>', '', text)


def remove_special_chars(input_string: str) -> str:
    cleaned_string = ''.join(c for c in input_string if c.isalnum() or c == ' ')
    return cleaned_string


def split_on_case(text: str) -> list:
    return re.findall(r'[A-Z]?[a-z]*|[A-Z]+', text)


def extract_json_payload(text):
    json_regex = r'(\{(?:[^{}]|(?R))*\}|\[(?:[^[\]]|(?R))*\])'
    match = regex.search(json_regex, text)

    if match:
        return match.group(0)

    return None


def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


def remove_markdowns(text):
    # Remove blockquotes, unordered lists, and ordered lists
    text = re.sub(r'^[>|\-|\d\.]+\s', '', text, flags=re.MULTILINE)

    # Remove headings
    text = re.sub(r'^#+\s', '', text, flags=re.MULTILINE)

    # Remove inline code blocks
    text = re.sub(r'`[^`]*`', '', text)

    # Remove code blocks
    text = re.sub(r'```[^```]*```', '', text, flags=re.MULTILINE)

    # Remove bold, italic, and strikethrough
    text = re.sub(r'(\*{1,2}|~~)([^*~]+)(\*{1,2}|~~)', r'\2', text)

    # Remove links
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)

    # Remove images
    text = re.sub(r'!\[[^\]]*\]\([^\)]+\)', '', text)

    # Remove HTML tags
    text = re.sub(r'<[^>]*>', '', text)

    return text


def calculate_percentage_change(old_value, new_value):
    if old_value == 0:
        raise ValueError("The old value cannot be zero for percentage calculation.")
    return ((new_value - old_value) / old_value) * 100


def percentage_of(value, total, proportion=True):
    if value == 0:
        return 0
    percentage = (value / total) * 100
    if proportion:
        if percentage < 100:
            percentage -= 100
        else:
            percentage = 100 - percentage
    return percentage


def is_time_between(self, begin_time, end_time, check_time):
    if begin_time < end_time:
        return begin_time <= check_time <= end_time
    else:  # crosses midnight
        return check_time >= begin_time or check_time <= end_time


def encode_image_to_base64(image_path):
    try:
        with Image.open(image_path) as img:

            # Resize image if it's too large
            max_size = (1024, 1024)
            img.thumbnail(max_size, Image.DEFAULT_STRATEGY)

            # Convert image to RGB if it's not
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG')
            return base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
    except Exception as e:
        return f"Error encoding image: {str(e)}"
