"""This script is used for decrypting text by bruteforcing the Caesar cipher.\nThe script is intended to be used as such:\npython caesar.py <character string>\n\nThe character string can be any character string (remember to put it in quoation marks)\nIf the script is not used as intended, an exception will be raised."""


import sys


#Alphabets for the Caesar cipher. Note that numbers are not encrypted!
small_alphabet = "abcdefghijklmnopqrstuvwxyz"
large_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#Find the length of the alphabet
alphabet_length = len(small_alphabet)


def gen_enc_dec_letter(alphabet, alphabet_index, letter):
    """Is used to decryct a single letter.
    
    alphabet_index is the index of the letter that is to be returned,
    letter is the letter that is to be encrypted/decrypted."""
    #Store global variables locally, to increase performance
    smalph = small_alphabet
    lalph = large_alphabet
    #Start by testing for the edge case, that the letter is not in the alphabet. If
    #it is, then proceed as normal.
    if letter not in smalph and letter not in lalph:
        return letter
    return alphabet[alphabet_index]


def decrypt(key, ciphertext):
    """Decryption function, that decrypts a message using the Caesar cipher.

    key is the key to be used for decryption and
    ciphertext is the ciphertext to be decrypted."""
    #Store global variables locally, to increase performance
    smalph = small_alphabet
    lalph = large_alphabet
    length = alphabet_length
    #Make string to store the result in
    result = ""

    #Iteratively find the alphabet index from the key and add the resulting letter
    #to the result
    for letter in ciphertext:
        if letter in smalph:
            alphabet_index = (smalph.find(letter) - key) % length
            result = result + gen_enc_dec_letter(smalph, alphabet_index, letter)
        else:
            alphabet_index = (lalph.find(letter) - key) % length
            result = result + gen_enc_dec_letter(lalph, alphabet_index, letter)

    #Return the result
    return result


def main():
    """Main function used to decrypt text by brute force.

    Throws exceptions if wrong number of arguments are applied (should be 2 including the name of the script)."""
    #Start off by testing if the number of required arguments are as should be
    if len(sys.argv) != 2:
        raise Exception("Wrong number of arguments!\nThe correct number of arguments is 2!\n\nThe script is intended to be used as such:\npython caesar_bruteforcer.py <character string>\n\nThe character string can be any character string (remember to put it in quoation marks).")

    #Store global variables locally, to increase performance
    length = alphabet_length
    ciphertext = sys.argv[1]

    #Filename to be saved to
    filename = "possible plaintexts"

    #Start finding plaintexts and adding them together
    print("\nTrying to bruteforce encryption and saving to file " + filename)
    results = "" #string to append possible results to
    results += "Encrypted ciphertext: " + ciphertext + "\n\n"
    for key in range(1, length+1):
        #Try all possible lengths (not trying if the text is not encrypted (key = 0))
        results += "A possible decryption could be: "
        results += decrypt(key, ciphertext)
        results += "\n\n"


    #Save to file
    try:
        f = open(filename, "w")
        f.write(results)
        f.close()
    except:
        print("Something went wrong when trying to save the file holding the possible plaintexts. Here is the result printed to the terminal instead:\n\n")
        print(results)
    else:
        print("\nDone! Look in file " + filename + " to see the different possible plaintexts.")

    return

if __name__ == "__main__":
    main()
