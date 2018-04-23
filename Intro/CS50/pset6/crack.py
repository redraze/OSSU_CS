import crypt
import sys

# ensure proper usage
if len(sys.argv) != 2:
    print ("Usage: python crack.py hash")
    raise SystemExit


# get hashed password and salt
hashed = sys.argv[1]
salt = hashed[0] + hashed[1]

# letter scheme a through z and A through Z
letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

# try all single character password combinations
for i in range(0, len(letters)):
    if crypt.crypt(letters[i], salt) == hashed:
        print (letters[i])
        raise SystemExit

# try all two character password combinations
for i in range(0, len(letters)):
    for j in range(0, len(letters)):
        if crypt.crypt(letters[i] + letters[j], salt) == hashed:
            print (letters[i] + letters[j])
            raise SystemExit

# try all three character password combinations
for i in range(0, len(letters)):
    for j in range(0, len(letters)):
        for k in range(0, len(letters)):
            if crypt.crypt(letters[i] + letters[j] + letters[k], salt) == hashed:
                print (letters[i] + letters[j] + letters[k])
                raise SystemExit

# try all four character password combinations
for i in range(0, len(letters)):
    for j in range(0, len(letters)):
        for k in range(0, len(letters)):
            for l in range(0, len(letters)):
                if crypt.crypt(letters[i] + letters[j] + letters[k] + letters[l], salt) == hashed:
                    print (letters[i] + letters[j] + letters[k] + letters[l])
                    raise SystemExit
# failure
print ("Could not crack password.")
