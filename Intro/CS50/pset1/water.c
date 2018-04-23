#include <stdio.h>
#include <cs50.h>

int main(void){
    int bottles;
    int minutes;
    do{
        printf("\nMinutes spent in shower:");
        minutes = GetInt();
        if (minutes < 0){
            printf("\t\t\t\t\t***Please enter a positive integer.***\n");
        };
    }while(minutes < 0);
    bottles = 12 * minutes;
    printf("Bottles of water used: %i\n", bottles);
}
