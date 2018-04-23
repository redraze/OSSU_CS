#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main(void){
    string name = get_string();
    char initials[10];
    int initials_count = 0;
    if(isalpha(name[0])){
        initials[0] = name[0];
        initials_count++;
    };
    int activation = 0;
    for(int i = 0; i < strlen(name); i++){
        if(isspace(name[i])){
            activation = 1;
        };
        if(isalpha(name[i]) && activation == 1){
            initials[initials_count] = name[i];
            initials_count++;
            activation = 0;
        };
    };
    initials_count = 0;
    while(isalpha(initials[initials_count])){
        if(islower(initials[initials_count])){
            initials[initials_count] = (toupper(initials[initials_count]));
        };
        printf("%c", initials[initials_count]);
        initials_count++;
    };
    printf("\n");
    return 0;
}
