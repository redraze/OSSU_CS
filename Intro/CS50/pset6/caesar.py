import sys

# check for proper usage
if len(sys.argv) != 2:
    print ("Usage: python caesar.py k")
    raise SystemExit

# get text in
print("plaintext:  ", end="")
in_word = input()
out_word = ""
k = int(sys.argv[1])
for i in range(0, len(in_word)):
    # for uppercase letters
    if str.isupper(in_word[i]) == True:
        out_word += chr((ord(in_word[i]) - 65 + k) % 26 + 65)
    # for lowercase letters
    elif str.islower(in_word[i]) == True:
        out_word += chr((ord(in_word[i]) - 97 + k) % 26 + 97)
    # for non-alpha characters
    else:
        out_word += in_word[i]
print("ciphertext: {}".format(out_word))
