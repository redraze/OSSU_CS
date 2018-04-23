#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void){
    float money;
    printf("O hai! How much change is owed?\n...$");
    do{
        money = GetFloat();
        if(money < 0){
            printf("Please enter a positive number.\n");
        };
    }while(money < 0);
    money = (int)round(money*100);
    int quarters = 0;
    int dimes = 0;
    int nickels = 0;
    while(money > 24){
        quarters++;
        money -= 25;
    };
    while(money > 9){
        dimes++;
        money -= 10;
    };
    while(money > 4){
        nickels++;
        money -= 5;
    };
    //Print for check50:
    int total_change = quarters + dimes + nickels + money;
    printf("%.0d\n", total_change);
}
