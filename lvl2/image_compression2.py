from PIL import Image
import numpy as np
from matplotlib import cm
from struct import *
import os.path

def get_shape(arr): # Function that gets the shape of an image.

    height, width = arr.shape
    return height, width

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
        decompressed_image = np.frombuffer(decompressed_data, dtype=np.uint8).reshape(get_shape(pil_to_np(im)))
        
        return decompressed_image

def save_image(arr): # Function that saves the compressed image.
    compressed_image = Image.fromarray(arr).save("lvl2/result.png")
    return compressed_image

def pil_to_np(img):
    return np.array(img)

def gray(img):
    return img.convert('L')

def save_compressed_data(arr): # Function that saves the compressed file bite-wise.
    output_file = open("lvl2/compressed"+".bin","wb")
    for data in arr:
        output_file.write(pack('>H',int(data)))
    return output_file

def ratio(path_1, path_2):

    ratio = os.path.getsize(path_1)/os.path.getsize(path_2)
    return ratio

def get_size(path):

    return str(os.path.getsize(path))

def lvl2():

    im = Image.open("lvl2/squares.png")
    compressed = compressor(pil_to_np(gray(im)).flatten())
    save_compressed_data(compressed)
    decompressed = decompressor(compressed, im)
    save_image(decompressed)
  
