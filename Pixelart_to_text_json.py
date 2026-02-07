from PIL import Image
import json
import os

from numpy.ma.extras import row_stack
from orca.colornames import rgb_string_to_color_name

# Path to your folder
folder_path = "assets"

# List all files
files = os.listdir(folder_path)

# Filter only images (example: .png and .jpg)
image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

print(image_files)
def image_to_code(true_RGB = False):
    img_list = {}
    for i in image_files:
        img = Image.open(f'assets/{i}')
        print(img)
        width, height = img.size
        color_list = []
        for y in range(height):
            row = []
            for x in range(width):
                color = img.getpixel((x,y))
                #print(color)
                if true_RGB:
                    if len(color) != 4:
                        color = (color[0], color[1], color[2], 255)
                else:
                    if len(color) == 4:
                        color = rgb_to_256(color[0],color[1],color[2],color[3])
                    else:
                        color = rgb_to_256(color[0], color[1], color[2])

                #print(f'\033[48;5;{color}m{color}\033[0m')
                row.append(color)
            color_list.append(row)
        img_list[i] = color_list_to_art(color_list,true_RGB)




def color_list_to_art(colors,true_RGB = False):
    img = []
    for y in range(len(colors)//2):
        row = ''
        for x in range(len(colors[0])):
            y_1 = y * 2
            y_2 = y_1 + 1
            color_1 = colors[y_1][x]
            color_2 = colors[y_2][x]
            if true_RGB:
                #print(color_1)
                r_1, g_1, b_1, a_1 = color_1
                r_2, g_2, b_2, a_2 = color_2
                if color_1[3] < 128 and color_2[3] < 128:
                    row += ' '
                elif color_1[3] < 128:
                    row += f'\033[38;2;{r_2};{g_2};{b_2}m▄\033[0m'
                elif color_2[3] < 128:
                    row += f'\033[38;2;{r_1};{g_1};{b_1}m▀\033[0m'
                elif (r_1,g_1,b_1) == (0,0,0) and (r_2,g_2,b_2) == (0,0,0):
                    row += f'\033[38;5;16m█\033[0m'
                elif color_1 == (0,0,0,255):
                    row += f'\033[48;2;{r_2};{g_2};{b_2};38;2;{r_1};{g_1};{b_1}m▀\033[0m'
                else:
                    row += f'\033[48;2;{r_1};{g_1};{b_1};38;2;{r_2};{g_2};{b_2}m▄\033[0m'
            else:
                if color_1 == 16 and color_2 == 16:
                    row += f'\033[38;5;16m█\033[0m'
                elif color_1 == 256 and color_2 == 256:
                    row += ' '
                elif color_1 == 256:
                    row += f'\033[38;5;{color_2}m▄\033[0m'
                elif color_2 == 256:
                    row += f'\033[38;5;{color_1}m▀\033[0m'
                elif color_1 == 16:
                    row += f'\033[48;5;{color_2};38;5;{color_1}m▀\033[0m'
                else:
                    row += f'\033[48;5;{color_1};38;5;{color_2}m▄\033[0m'
        print(row)
        img.append(row)
    return img





def rgb_to_256(r, g, b, a=None):
    if a != None:
        if a < 128:
            return 256
    # 6×6×6-Farbwürfel
    cube_levels = [0, 95, 135, 175, 215, 255]
    best_index = 0
    min_dist = float('inf')

    # Würfelfarben
    for i, rc in enumerate(cube_levels):
        for j, gc in enumerate(cube_levels):
            for k, bc in enumerate(cube_levels):
                index = 16 + 36*i + 6*j + k
                dist = ((r-rc)*0.299)**2 + ((g-gc)*0.587)**2 + ((b-bc)*0.114)**2
                if dist < min_dist:
                    min_dist = dist
                    best_index = index

    # Graustufen prüfen
    for i in range(24):
        gray = 8 + i*10
        dist = (r-gray)**2 + (g-gray)**2 + (b-gray)**2
        if dist < min_dist:
            min_dist = dist
            best_index = 232 + i

    return best_index

#image_to_code(True)
out = image_to_code()

