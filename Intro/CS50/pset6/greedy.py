# get change in (formatted)
print ("O hai! How much change is owed?")
while True:
    try:
        change = float(input())
    except ValueError:
        print ("How much change is owed?")
    else:
        if change > 0:
            break
        print("How much change is owed?")
        
change = int(change * 100)

# get quarters out
quarters = (change - (change % 25))/25
change = change - (quarters * 25)

# get dimes out
dimes = (change - (change % 10))/10
change = change - (dimes * 10)

# get nickels out
nickels = (change - (change % 5))/5
change = change - (nickels * 5)

# pennies out is whatever's left of change

# long format print
#print ("Quarters out : {}\nDimes out: {}\nNickels out: {}\nPennies out: {}"
#       .format(int(quarters), int(dimes), int(nickels), int(change)))

# short format print
print ("Total change out: {}".format(int(quarters + dimes + nickels + change)))
