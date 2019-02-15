import base64
import sys
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
                #print(chr(char))
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
            image = sys.argv[2]
            with open(image, "rb") as image_file:
                self.encoded_string = base64.b64encode(image_file.read())
            print(self.encoded_string)
        except:
            print("Conversion Failed")

if __name__ == "__main__":
    if(sys.argv[1] == "convert"):
        converted_img = ENCODE()
    elif(sys.argv[1] == "display"):
        converted_img = ENCODE()
    else:
        print("Problem with command line arguments")
        print(sys.argv[1])