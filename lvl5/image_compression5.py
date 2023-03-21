from PIL import Image
import numpy as np
from matplotlib import cm
from struct import *
import os.path

def get_shape(arr): # Function that gets the shape of an image.

    size = arr.shape
    height = size[0]
    width = size[1]
    depth = size[2]
    return height, width, depth

def compressor(data): # Function that compresses the given image array with lzw algorithm.

    # Building the dictionary
    code = 256
    dictionary_size = 256
    current_string = ""
    compressed = []
    dictionary = {chr(i): i for i in range(dictionary_size)}
    
    # LZW Compression algorithm
    for element in data:
        new_string = current_string + chr(element)

        if new_string in dictionary:
            current_string = new_string

        else:
            compressed.append(dictionary[current_string])
            dictionary[new_string] = code
            code += 1
            current_string = chr(element)    

    if current_string in dictionary:
        compressed.append(dictionary[current_string])

    return compressed 

def decompressor(compressed,im): # Function that decompresses the given array with lzw algorithm.
        
        # Building the dictionary
        dictionary = {i: bytes([i]) for i in range(256)}
        w = bytes([compressed.pop(0)])
        result = [w]
        # LZW Decompression algorithm
        for k in compressed:
            if k in dictionary:
                entry = dictionary[k]
            elif k == len(dictionary):
                entry = w + bytes([w[0]])
            else:
                raise ValueError("Bad compressed k: %s" % k)
            result.append(entry)
            
            dictionary[len(dictionary)] = w + bytes([entry[0]])
            w = entry

        # Convert the list of bytes to a numpy array
        decompressed_data = b"".join(result)
        decompressed_image = np.frombuffer(decompressed_data, dtype=np.uint8).reshape(get_shape(pil_to_np(red(im))))
        
        return decompressed_image

def save_image(arr): # Function that saves the compressed image.

    compressed_image = Image.fromarray(arr).save("lvl5/result.png")
    return compressed_image

def get_pivot(arr):
    return arr[0,0]

def difference_image(arr):

    # Intermediate difference image
    inter_diff = np.diff(arr, axis=1)
    inter_diff = np.insert(inter_diff, 0, arr[:, 0], axis=1)

    # Difference image
    pivot = inter_diff[0,0]
    inter_diff[:,0] = inter_diff[:,0] - pivot

    return inter_diff

def reverse_difference(inter_diff, im):

    # Get pivot value
    pivot = get_pivot(pil_to_np(im))
    # Add pivot to first column of inter_diff
    inter_diff[:, 0] += pivot

    # Reverse the modification of inter_diff
    for i in range(1, inter_diff.shape[1]):
        inter_diff[:, i] += inter_diff[:, i-1]

    return inter_diff

def save_compressed_data(arr): # Function that saves the compressed file bite-wise.
    output_file = open("lvl5/compressed"+".bin","wb")
    for data in arr:
        output_file.write(pack('>H',int(data)))
    return output_file

def red(img):
    RGB = img.split()
    R = RGB[0]
    G = RGB[1]
    B = RGB[2]

    R = R.point(lambda i: i*1)
    G = G.point(lambda i: i*0)
    B = B.point(lambda i: i*0)

    return Image.merge("RGB", (R,G,B))

def blue(img):
    RGB = img.split()
    R = RGB[0]
    G = RGB[1]
    B = RGB[2]

    R = R.point(lambda i: i*0)
    G = G.point(lambda i: i*0)
    B = B.point(lambda i: i*1)

    return Image.merge("RGB", (R,G,B))

def green(img):
    RGB = img.split()
    R = RGB[0]
    G = RGB[1]
    B = RGB[2]

    R= R.point(lambda i: i*0)
    G= G.point(lambda i: i*1)
    B= B.point(lambda i: i*0)

    return Image.merge("RGB", (R,G,B))

def pil_to_np(img):
    return np.array(img)

def process_red():
    im = Image.open("lvl5/template.png")
    img_array = pil_to_np(red(im))
    diff_image = difference_image(img_array)
    compressed = compressor(diff_image.flatten())
    save_compressed_data(compressed)
    decompressed = decompressor(compressed, im)
    reverse_diff_image = reverse_difference(diff_image, im)
    save_image(reverse_diff_image)

def process_green():
    im = Image.open("lvl5/template.png")
    img_array = pil_to_np(green(im))
    diff_image = difference_image(img_array)
    compressed = compressor(diff_image.flatten())
    save_compressed_data(compressed)
    decompressed = decompressor(compressed, im)
    reverse_diff_image = reverse_difference(diff_image, im)
    save_image(reverse_diff_image)

def process_blue():
    im = Image.open("lvl5/template.png")
    img_array = pil_to_np(blue(im))
    diff_image = difference_image(img_array)
    compressed = compressor(diff_image.flatten())
    save_compressed_data(compressed)
    decompressed = decompressor(compressed, im)
    reverse_diff_image = reverse_difference(diff_image, im)
    save_image(reverse_diff_image)   

def ratio(path_1, path_2):

    ratio = os.path.getsize(path_1)/os.path.getsize(path_2)
    return ratio

def get_size(path):

    return str(os.path.getsize(path))
