"""This script is used for encrypting/decrypting text using the Caesar cipher.\nThe script is intended to be used as such:\npython caesar.py <character string> <key> <mode>\n\nThe character string can be any character string (remember to put it in quoation marks), the key has to be a positive integer either 0 or above and the mode must be either \"e\" (for encryption mode) or \"d\" (for decryption mode).\nIf any of the abovementioned is not followed, an exception will be raised."""


import sys


#Alphabets for the Caesar cipher. Note that numbers are not encrypted!
small_alphabet = "abcdefghijklmnopqrstuvwxyz"
large_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#Find the length of the alphabet
alphabet_length = len(small_alphabet)


def gen_enc_dec_letter(alphabet, alphabet_index, letter):
    """Is used to encrypt or decryct a single letter.
    
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


def encrypt(key, message):
    """Encryption function, that encrypts a message using the Caesar cipher.

    key is the key to be used for encryption and
    message is the message to be encrypted."""
    #Store global variables locally, to increase performance
    smalph = small_alphabet
    lalph = large_alphabet
    length = alphabet_length
    #Make string to store the result in
    result = ""

    #Iteratively find the alphabet index from the key and add the resulting letter
    #to the result
    for letter in message:
        if letter in smalph:
            alphabet_index = (smalph.find(letter) + key) % length
            result = result + gen_enc_dec_letter(smalph, alphabet_index, letter)
        else:
            alphabet_index = (lalph.find(letter) + key) % length
            result = result + gen_enc_dec_letter(lalph, alphabet_index, letter)

    #Return the result
    return result


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
    """Main function used to encrypt/decrypt text.

    Throws exceptions if wrong number of arguments are applied (should be 4 including the name of the script), if key is not an integer and if the mode selected is not either \"e\" (for encryption) or \"d\" (for decryption)."""
    #Start off by testing if the number of required arguments are as should be
    if len(sys.argv) != 4:
        print("Wrong number of arguments!\nThe correct number of arguments is 4!\n\nThe script is intended to be used as such:\npython caesar.py <character string> <key> <mode>\n\nThe character string can be any character string (remember to put it in quoation marks), the key has to be a positive integer either 0 or above and the mode must be either \"e\" (for encryption mode) or \"d\" (for decryption mode)")
    #Test if the mode is selected correctly
    if not ((sys.argv[3] == "e") or (sys.argv[3] == "d")):
        raise Exception("The mode must be either \"e\" (for encryption mode) or \"d\" (for decryption mode).")

    #Store global variable locally, to increase performance
    length = alphabet_length
    #The key might be big, so to save computation it is once and for all computed
    #here. Also automatically tests if the key is an integer
    key = int(sys.argv[2]) % length

    #Select what to do based on the input to the program
    if sys.argv[3] == "e":
        print("\nEncryption mode. Your encrypted text is:")
        result = encrypt(key, sys.argv[1])
    else:
        print("\nDecryption mode. Your decrypted text is:")
        result = decrypt(key, sys.argv[1])

    print(result)
    return

if __name__ == "__main__":
    main()
