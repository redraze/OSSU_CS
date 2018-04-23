import sys

# encryption loop
def main(key, in_text):
    out_text = ""
    count = 0
    for i in range(0, len(in_text)):            
        # for lowercase letters
        if str.islower(in_text[i]) == True:
            out_text += chr((ord(in_text[i]) - 97 + key[count]) % 26 + 97)
            count += 1
        # for uppercase letters
        elif str.isupper(in_text[i]) == True:
            out_text += chr((ord(in_text[i]) - 65 + key[count]) % 26 + 65)
            count += 1
        # for non-alpha characters
        else:
            out_text += in_text[i]
        
        if count == len(key):
            count = 0

    # success
    return out_text


# ensure proper usage and format of argv[1]
if len(sys.argv) == 2:
    if str.isalpha(sys.argv[1]) == True:
        
        # format key
        key = []
        for i in range(0, len(sys.argv[1])):
            if str.isupper(sys.argv[1]) == True:
                key.append(ord(sys.argv[1][i]) - 65)
            else:
                key.append(ord(sys.argv[1][i]) - 97)
        
        # get plaintext
        print ("plaintext:  ", end="")
        in_text = input()
        
        # send key and plaintext to cipher function
        print ("ciphertext: {}".format(main(key, in_text)))
        raise SystemExit
print ("Usage: python vigenere.py k")
