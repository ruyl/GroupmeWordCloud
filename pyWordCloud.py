###
# Author: Nicholas Alvarez
# Version: 0.1
###
from groupy.client import Client
from wordcloud import WordCloud
import matplotlib
from sys import argv
import numpy as np
from PIL import Image

width_arg = False
length_arg = False
max_font_arg = False
mask_arg = False
filter_image = None

px_width = 1920
px_length = 1080
max_font = 1000

def print_usage():
    print("Usage: python3 pyWordCloud.py <output_path> <Groupme_api_token> [--width canvas_width --length canvas_length --max-font max_font_size --mask image_mask]")

if len(argv) < 3:
    print_usage()
    exit(1)

output_path = argv[1]
api_token = argv[2]

def is_positive_integer(x):
    return isinstance(x, int) and x > 0

if len(argv) > 3:
    for arg in sys.argv[2:]:
        if ((width_arg and (length_arg or mask_arg or max_font_arg)) or
            (length_arg and (width_arg or mask_arg or max_font_arg)) or
            (max_font_arg and (length_arg or mask_arg or width_arg)) or
            (mask_arg and (length_arg or width_arg or max_font_arg))):
                print_status()
                exit(1)
        if arg == "--width" or arg == "-w":
            width_arg = True
        if arg == "--length" or arg == "-l":
            length_arg = True
        if arg == "--max-font" or arg == "-s":
            max_font_arg = True
        if arg == "--mask" or arg == "-m":
            mask_arg = True
        if width_arg:
            if (not is_positive_integer(arg)):
                exit(1)
            px_width = int(arg)
            width_arg = False
        if length_arg:
            if (not is_positive_integer(arg)):
                exit(1)
            px_length = int(arg)
            length_arg = False
        if max_font_arg:
            if (not is_positive_integer(arg)):
                exit(1)
            max_font = int(arg)
            max_font_arg = False 
        if mask_arg:
            mask_path = arg
            mask_arg = False 
            filter_image = True
            
if mask_arg or width_arg or length_arg or max_font_arg or mask_arg:
    print_usage()
    exit(1)

#print("a")
myClient = Client.from_token(api_token)
client_list = []
print("Choose a group to word-cloud (input group ID):")
for group in myClient.groups.list_all():
    print(group.id, group.name)
    client_list.append(group)
chosen_group = input(">")

# Check if the input is a positive integer
if not is_positive_integer(int(chosen_group)):
    print("Please try again and enter a valid group ID.")
    exit(1)

pared_down_list = list(filter((lambda x : x.id==chosen_group), client_list))

if len(pared_down_list) == 0:
    print("Please try again and enter a valid group ID.")
    exit(1)

print("Choose member by ID:)")
for member in pared_down_list[0].members:
	print(member.user_id, member.name)
member_id = input(">")

# Check if the input is a positive integer

# Check if the input is a positive integer
if not is_positive_integer(int(member_id)):
    print("Please try again and enter a valid user ID.")
    exit(1)

all_words = ''
for message in filter(lambda x : x.user_id==member_id, pared_down_list[0].messages.list_all()):
    msg_text = message.text
    if msg_text != None:
        all_words += str(message.text)
        all_words += " "
        # print(message.name)

if filter_image == None:
    wordcloud = WordCloud(max_font_size=max_font, width=px_width, height=px_length).generate(all_words)
else:
    img_mask = np.array(Image.open(mask_img_name))
    wordcloud = WordCloud(max_font_size=max_font, width=px_width, height=px_length, mask=img_mask).generate(all_words)

image = wordcloud.to_file(output_path)
