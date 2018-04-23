# number checking algorithm
def check(num):
    count = 0
    
    # step 1
    for i in range(len(num)%2, len(num), 2):
        temp = str(int(num[i]) * 2)
        if int(temp) > 9:
            count += int(temp[0]) + int(temp[1])
        else:
            count += int(temp)
    
    # step 2
    for i in range(abs(len(num)%2 - 1), len(num), 2):
        count += int(num[i])
    
    # step 3
    if count % 10 == 0:
        return True
    return False

# get card number in (formatted)
print ("Number: ", end="")
while True:
    try:
        card_num = int(input())
    except ValueError:
        print ("Retry: ", end="")
    else:
        if card_num > 0:
            break
        print ("Retry: ", end="")

# check for correct card number length
card_num = str(card_num)
if len(card_num) < 15 or len(card_num) > 16:
    print ("Invalid number.")
    raise SystemExit
    
# check for correct card number starts
if card_num[0] == "3" and len(card_num) == 15:
    if card_num[1] == "4" or card_num[1] == "7":
        if check(card_num) == True:
            print ("AMEX")
            raise SystemExit
elif card_num[0] == "4" and len(card_num) == 16:
    if check(card_num) == True:
        print ("VISA")
        raise SystemExit
elif card_num[0] == "5" and len(card_num) == 16:
    for i in range(1,6):
        if card_num[1] == str(i):
            if check(card_num) == True:
                print ("Mastercard")
                raise SystemExit
print ("Invalid number.")
