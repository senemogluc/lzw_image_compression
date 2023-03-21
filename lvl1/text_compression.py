from struct import *
import os.path

def compressor(data): # Function that compresses the given file with lzw algorithm.

    # Building the dictionary
    dictionary_size = 256                   
    dictionary = {chr(i): i for i in range(dictionary_size)}    
    string = ""             
    compressed_data = []    

    # LZW Compression algorithm.
    for symbol in data:                     
        string_plus_symbol = string + symbol 
        if string_plus_symbol in dictionary: 
            string = string_plus_symbol
        else:
            compressed_data.append(dictionary[string])
            dictionary[string_plus_symbol] = dictionary_size
            dictionary_size += 1
            string = symbol

    if string in dictionary:
        compressed_data.append(dictionary[string])
    return compressed_data    

def decompressor(compressed_data): # Function that decompresses the given array with lzw algorithm.

    # Building the dictionary
    next_code = 256
    decompressed_data = ""
    string = ""
    dictionary_size = 256
    dictionary = dict([(x, chr(x)) for x in range(dictionary_size)])

    # LZW Decompression algorithm
    for code in compressed_data:
        if not (code in dictionary):
            dictionary[code] = string + (string[0])
        decompressed_data += dictionary[code]
        if not(len(string) == 0):
            dictionary[next_code] = string + (dictionary[code][0])
            next_code += 1
        string = dictionary[code]

    return decompressed_data

def save_compressed_data(arr): # Function that saves the compressed file bite-wise.
    output_file = open("lvl1/compressed"+".bin","wb")
    for data in arr:
        output_file.write(pack('>H',int(data)))
    return output_file

def save_decompressed_data(str): # Function that saves the decompressed file.
    output_file = open("lvl1/decompressed" + ".txt", "w")
    for data in str:
        output_file.write(data)
    return output_file    

def ratio(path_1, path_2):

    ratio = os.path.getsize(path_1)/os.path.getsize(path_2)
    return ratio

def lvl1():
    file = open("lvl1/input.txt")
    data = file.read()
    print("\nThe input data is: ", data, "\n")
    compressed = compressor(data)
    print("The compressed data is; ", compressed, "\n")
    save_compressed_data(compressed) 
    decompressed = decompressor(compressed)
    print("The decompressed data is: ", decompressed, "\n")
    save_decompressed_data(decompressed)

    print("The size of 'input.txt' is :", os.path.getsize("lvl1/input.txt"), "bytes\n")
    print("The size of 'compressed.bin' is :", os.path.getsize("lvl1/compressed.bin"), "bytes\n")
    print("The compress ratio is: ",ratio("lvl1/compressed.bin","lvl1/decompressed.txt" )) 

lvl1()
