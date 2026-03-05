from sys import implementation
from PIL import Image
import json
import os
import random
import numpy as np
from skimage.filters import gaussian

from numpy.ma.extras import row_stack
from orca.colornames import rgb_string_to_color_name

# Path to your folder
folder_path = "assets"

# List all files
files = os.listdir(folder_path)

# Filter only images (example: .png and .jpg)
image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

print(image_files)
def image_to_code(true_RGB = False,dither=False):
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
                elif dither:
                    #color = color_dither(color[0], color[1], color[2],x,y)
                    color = bw_dither(color[0], color[1], color[2],x,y)
                    #color = rgb_to_256(color[0],color[1],color[2],color[3])
                    #print(color)
                else:
                    if len(color) == 4:
                        color = rgb_to_256(color[0],color[1],color[2],color[3])
                    else:
                        color = rgb_to_256(color[0], color[1], color[2])

                #print(f'\033[48;5;{color}m{color}\033[0m')
                row.append(color)
            color_list.append(row)
        img_list[i] = color_list_to_art(color_list,true_RGB,dither)




def color_list_to_art(colors,true_RGB = False, dither=False):
    img = []
    for y in range(len(colors)//2):
        row = ''
        for x in range(len(colors[0])):
            y_1 = y * 2
            y_2 = y_1 + 1
            color_1 = colors[y_1][x]
            color_2 = colors[y_2][x]
            if true_RGB or dither:
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
    #for i in range(24):
    #    gray = 8 + i*10
    #    dist = (r-gray)**2 + (g-gray)**2 + (b-gray)**2
    #    if dist < min_dist:
    #        min_dist = dist
    #        best_index = 232 + i

    return best_index


dither_patern_2 = [
    [1,13,4,16],
    [9,5,12,8],
    [3,15,2,14],
    [11,7,10,6]
]




dither_patern_1 = [
    [1,4],
    [3,2]
]

fdither_patern_1 = [
    [4,2],
    [3,1]
]

def get_patern(num):
    if num <= 1:
        return dither_patern_1
    else:
        patern_temp = get_patern(num-1)
        temp = 2 ** num
        other_num = (2 ** (num-1))**2
        out_temp = []
        for y in range(temp):
            out_tt = []
            for x in range(temp):
                if dither_patern_1[y % 2][x % 2 ] == 1 :
                    out_tt.append(patern_temp[y//2][x//2])
                elif dither_patern_1[y % 2][x % 2 ] == 4:
                    out_tt.append(patern_temp[y//2][x//2]+other_num*3)
                elif dither_patern_1[y % 2][x % 2 ] == 3:
                    out_tt.append(patern_temp[y//2][x//2]+other_num*2)
                elif dither_patern_1[y % 2][x % 2 ] == 2:
                    out_tt.append(patern_temp[y//2][x//2]+other_num)
            out_temp.append(out_tt)
        for i in out_temp:
            print(i)
        return out_temp
        
        
def make_blue_noise(size,cmax):
    out = []
    for y in range(size):
        row = []
        for x in range(size):
            temp = random.randint(0,cmax)
            row.append(temp)
        print(row)
        out.append(row)
    return out
        



def blueNoise(size, sigma=0.5, initial_ratio=0.9,cmax=255):
    # Init: Place some initial pixels based off thresholded white noise
    shape = (size, size)
    ranks = np.zeros(shape)
    initial_white_noise = np.random.rand(size, size)
    placed_pixels = initial_white_noise >= (1-initial_ratio)
  
    count_placed = np.sum(placed_pixels)
    count_remaining = placed_pixels.size - count_placed
    prev_swap = None
    while True:
        blurred = gaussian(placed_pixels, sigma, mode='wrap')
        densest = (blurred * placed_pixels).argmax()
        voidest = (blurred + placed_pixels).argmin()
        densest_coord = np.unravel_index(densest, shape)
        voidest_coord = np.unravel_index(voidest, shape)
        if prev_swap == (voidest, densest):
            break
        if densest == voidest:
            break
        placed_pixels[densest_coord] = False
        placed_pixels[voidest_coord] = True
        prev_swap = (densest, voidest)
        
    not_ranked = placed_pixels.copy()
    for rank in range(count_placed, 0, -1):
        blurred = gaussian(not_ranked, sigma, mode='wrap')
        densest = (blurred * not_ranked).argmax()
        densest_coord = np.unravel_index(densest, shape)
    
        not_ranked[densest_coord] = False
        ranks[densest_coord] = rank
        
    for rank in range(count_remaining):
        blurred = gaussian(placed_pixels, sigma, mode='wrap')
        voidest = (blurred + placed_pixels).argmin()
        voidest_coord = np.unravel_index(voidest, shape)
    
        placed_pixels[voidest_coord] = True
        ranks[voidest_coord] = count_placed + rank
    
    #print(ranks)
    out = []
    for i in ranks:
        row = []
        for j in i:
            row.append(int(j/((size**2)/cmax))+1)
        out.append(row)
        print(row)
    return out
                

def b_or_w(color,px,py,cmax,patern):
    dl = len(patern)
    num = patern[py%dl][px%dl]
    num = (num / dith_max) / cmax
    pmax = 1 / cmax

    out = 0
    for i in range(cmax):
        num_t = num + pmax*i
        if color >= num_t:
           out += 1
    if out == 0:
        return 0
    else:
        return pmax * out

        




def bw_dither(r,g,b,px,py):        
    gray = ((r*0.299)+(g*0.587)+(b*0.114))
    gray = abs(gray / 256)
    out = b_or_w(gray,px,py,7,dither_patern)
    #out1 = b_or_w(gray,px,py,1,dither_patern_lol)
    out1 = 1
    #print(out)
    return (int(255*out*out1),int(255*out*out1),int(255*out*out1),255)
    
    
def color_dither(r,g,b,px,py):
    gray = ((r*0.299)+(g*0.587)+(b*0.114))
    gray = abs(gray / 256)
    r = r / 255
    g = g / 255
    b = b / 255
        
    out =1# b_or_w(gray,px,py,4,dither_patern_lol)
    out1 = b_or_w(r,px,py,16,dither_patern_r)# * b_or_w(r,px,py,16,dither_patern_lol)
    out3 = b_or_w(b,px,py,16,dither_patern_b)# * b_or_w(b,px,py,16,dither_patern_lol)
    out2 = b_or_w(g,px,py,16,dither_patern_g)# * b_or_w(g,px,py,16,dither_patern_lol)
    #print(out1,out2,out3)
    return (int(255*out1*out)%256,int(255*out2*out)%256,int(255*out3*out)%256,255)
        
        
def dither_test():
    color_list = []
    for y in range(20):
        row = []
        row2 = ""
        for x in range(30):
            dl = len(dither_patern)
            num = dither_patern[x%dl][y%dl]
            num = num / dith_max
            temp = int(255 * num)
            temp2 = 255 - temp
            color = (temp,temp,temp,255)
            temp3 = str(temp)
            while len(temp3) <=2:
                temp3 += " "
            out = f"\033[48;2;{temp};{temp};{temp};38;2;{temp2};{temp2};{temp2}m{temp3}\033[0m"
            row.append(color)
            row2 += out
        color_list.append(row)
        print(row2)
    #color_list_to_art(color_list,False,True)


def lukas_dither(bysize,blsize):
    real_size = 2 ** bysize
    max_di = real_size ** 2
    rr_size = real_size * blsize
    by_pet = get_patern(bysize)
    blue_pet = blueNoise(rr_size,cmax=max_di)
    new_pet = []
    for y in range(rr_size):
        row = []
        row_temp = ''
        for x in range(rr_size):
            tile_by = by_pet[y%real_size][x%real_size]
            tile_blue = blue_pet[y][x]
            tile_blue += 1 if tile_blue == 0 else 0 
            #print(tile_by,tile_blue)
            row_temp += f"[{tile_by},{tile_blue}]"
            #tile = tile_by if ((y * rr_size) + (x)) % 2 == 0 else tile_blue
            #tile = tile_by if x % 2 == 0 else tile_blue
            #tile = tile_by if ((y * rr_size) + (x)// 2) % 2 == 0 else tile_blue
            tile = tile_by if ((y//2) + (x//2)) % 2 == 0 else tile_blue
            #tile = tile_by if (y + x) % 2 == 0 else tile_blue
            #tile = tile_by if ((y//blsize) + (x//blsize)) % 2 == 0 else tile_blue
            #tile = tile_by if ((y//real_size) + (x//real_size)) % 2 == 0 else tile_blue
            #tile = tile_by if ((x//real_size) + (y//blsize)) % 2 == 0 else tile_blue
            #t1 = 1 if real_size%blsize == 0 else real_size%blsize
            #t2 = 1 if blsize%real_size == 0 else blsize%real_size
            #tile = tile_by if ((x//t1) + (y//t2)) % 2 == 0 else tile_blue
            #tile = tile_by if ((x//real_size) + (y//blsize) + (y//real_size) + (x//blsize)) % 2 == 0 else tile_blue
            #tile = tile_blue
            #tile = random.choice((tile_blue,tile_by))
            row.append(tile)
        print(row_temp)
        print(row)
        new_pet.append(row)
    return new_pet, max_di, real_size * blsize
    

#image_to_code(True)
#dither_patern = get_patern(4)
#dither_patern_lol = dither_patern
#dith_len = len(dither_patern)
dith_len = 2 ** 3
dith_max = dith_len ** 2
#dither_patern = blueNoise(dith_len*4,cmax=dith_max)
#dither_patern_r = blueNoise(dith_len*4,cmax=dith_max)
#dither_patern_g = blueNoise(dith_len*4,cmax=dith_max)
#dither_patern_b = blueNoise(dith_len*4,cmax=dith_max)
#dith_len *= 4
#dither_patern = make_blue_noise(dith_len*4,cmax=dith_max)
#dith_max,dith_len = 16**2,16
# 
#dither_patern = blueNoise(dith_len*5,cmax=dith_max)
#dith_len = dith_len*5
#dither_patern = get_patern(3)
dither_patern, dith_max, dith_lenh = lukas_dither(2,3)
#dither_patern_lol, dith_max, dith_lenh = lukas_dither(3,3)
#dither_patern_r, dith_max, dith_lenh = lukas_dither(3,3)
#dither_patern_g, dith_max, dith_lenh = lukas_dither(3,3)
#dither_patern_b, dith_max, dith_lenh = lukas_dither(3,3)

#dither_patern_lol = dither_patern
#dither_patern_r = dither_patern
#dither_patern_g = dither_patern
#dither_patern_b = dither_patern

dither_test()
out = image_to_code(dither=True)
#out = image_to_code(true_RGB=True)

