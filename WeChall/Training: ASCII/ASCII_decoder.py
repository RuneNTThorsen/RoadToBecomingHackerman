"""Script used to decode numbers into ASCII.\n\nSave the numbers in a file called <filename> with each number separated by a comma and a space and use as such: python ASCII_decoder.py <filename>"""


import sys


def decode_char_from_int(i):
    decoded_char = "" #string to put character into
    try:
        decoded_char += chr(i)
    except:
        raise Exception("Something went wrong when trying to decode " + i)
    return decoded_char


def main():
    """Main function used to do the decoding.

    Throws exceptions if wrong number of arguments are applied (should be 2 including the name of the script)."""
    print("Script used to decode numbers into ASCII.\n\nSave the numbers in a file called <filename> and use as such: python ASCII_decoder.py <filename>\n\n")
    if len(sys.argv) != 2:
        raise Exception("Wrong number of arguments!")
    
    filename = sys.argv[1]
    encoded_chars = "" #variable to hold the string of encoded characters

    #Read the file holding the encoded characters
    try:
        f = open(filename, "r")
        encoded_chars = f.read()
        f.close()
    except:
        print("Something went wrong when trying to read the file holding the numerical values of the ASCII characters")

    result = "" #string to append decoded characters to
    
    ecs = encoded_chars.split(", ")
    for ec in ecs:
        try:
            i = int(ec)
        except:
            raise Exception("Could not cast input " + ec + " to integer")
        else:
            result += decode_char_from_int(i)

    #Print decoded characters and return
    print("The resulting decoded string is:\n")
    print(result)
    return



if __name__ =="__main__":
    main()
