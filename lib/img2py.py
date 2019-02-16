import base64
import imghdr
import sys
import os
"""
written by Jake Pring from CircuitSpecialists.com
licensed as GPLv3
"""


class ENCODE:
    def __init__(self):
        try:
            # convert img to base64 code
            with open(sys.argv[2], "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())

            # write base64 code to python file
            filename = sys.argv[2].split('.')[0]
            python_img = open("%s.py" % filename, "w")
            python_img.write("class IMG:\n\tdef __init__(self):\n\t\tself.data = \"")
            count = 0
            for char in encoded_string:
                python_img.write("%s" % chr(char))
                count += 1
                if(count % 200 == 0):
                    python_img.write("\" \\\n\t\t\t\"")
            python_img.write("\"")
            python_img.close()

            print("\nFinished.\nConverted %s image to the python file %s.py" % (sys.argv[2], filename))
        except:
            print("Conversion Failed")

class DECODE:
    def __init__(self):
        try:
            # open python file, get img data and convert string
            try:
                python_img = open(sys.argv[2], "r")
            except:
                print("No file named %s exists" % sys.argv[2])
            encoded_str = python_img.read()
            encoded_str = encoded_str.replace("class IMG:\n\tdef __init__(self):\n\t\tself.data = \"", "")
            encoded_str = encoded_str.replace("\" \\\n\t\t\t\"", "")
            encoded_str = encoded_str.replace("\"", "")
            decoded_str = base64.b64decode(encoded_str)

            # Convert string to img file
            filename = sys.argv[2].split('.')[0]
            image_file = open("%s" % filename, "wb")
            image_file.write(decoded_str)
            image_file.close()

            # get image filetype, and name file
            image_format = imghdr.what(filename)
            try:
                os.rename(filename, "%s.%s" % (filename, image_format))
                print("\nFinished.\nConverted %s python file to %s image file" % (sys.argv[2], filename))
            except:
                print("\n%s.%s already exists" % (filename, image_format))
                os.remove(filename)
        except:
            print("Conversion Failed")

if __name__ == "__main__":
    if(sys.argv[1] == "-convert"):
        converted_img = ENCODE()
    elif(sys.argv[1] == "-decode"):
        converted_img = DECODE()
    elif(sys.argv[1] == "--help"):
        print("\nUsage:")
        print("\timg2py [options] <filename>")
        print("\nOptions: \n\t")
        print("\t-convert: Convert an image into a python script")
        print("\t-decode:  Decode a previously converted image file, back into its original image")
    else:
        print("Problem with command line arguments")
        print(sys.argv[1])