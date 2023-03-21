from PIL import Image
import numpy as np
from matplotlib import cm
from struct import *
import os.path


def get_shape(arr):

    height, width = arr.shape

    return height, width

def compressor(data):
    code = 256
    dictionary_size = 256
    current_string = ""
    compressed = []
    dictionary = {chr(i): i for i in range(dictionary_size)}
    
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

def decompressor(compressed,im):
        
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
        decompressed_image = np.frombuffer(decompressed_data, dtype=np.uint8).reshape(get_shape(pil_to_np(im)))
        
        return decompressed_image

def save_image(arr):
    compressed_image = Image.fromarray(arr).save("lvl3/result.png")
    return compressed_image

def pil_to_np(img):
    return np.array(img)

def gray(img):
    return img.convert('L')

def difference_image(arr):

    # Intermediate difference image
    inter_diff = np.diff(arr, axis=1)
    inter_diff = np.insert(inter_diff, 0, arr[:, 0], axis=1)

    # Difference image
    pivot = inter_diff[0,0]
    inter_diff[:,0] = inter_diff[:,0] - pivot

    return inter_diff

def save_compressed_data(arr): # Function that saves the compressed file bite-wise.
    output_file = open("lvl3/compressed"+".bin","wb")
    for data in arr:
        output_file.write(pack('>H',int(data)))
    return output_file

def get_pivot(arr):
    return arr[0,0]

def reverse_difference(inter_diff, im):

    # Get pivot value
    pivot = get_pivot(pil_to_np(im))
    # Add pivot to first column of inter_diff
    inter_diff[:, 0] += pivot

    # Reverse the modification of inter_diff
    for i in range(1, inter_diff.shape[1]):
        inter_diff[:, i] += inter_diff[:, i-1]

    return inter_diff

def ratio(path_1, path_2):

    ratio = os.path.getsize(path_1)/os.path.getsize(path_2)
    return ratio

def get_size(path):

    return str(os.path.getsize(path))

def lvl3():
    im = Image.open("lvl3/squares.png")
    img_array = pil_to_np(gray(im))
    diff_image = difference_image(img_array)
    compressed = compressor(diff_image.flatten())
    save_compressed_data(compressed)
    decompressed = decompressor(compressed, im)
    reverse_diff_image = reverse_difference(diff_image, im)
    save_image(reverse_diff_image)



