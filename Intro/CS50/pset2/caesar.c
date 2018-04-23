#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int main(int argc, string argv[]){
    if(argc != 2){
        printf("Usage: ./caesar k\n");
        return 1;
    };
    int k = atoi(argv[1]);
    if(k < 0){
        printf("Usage: ./caesar k\n");
        return 0;
    };
    printf("plaintext:\t");
    string str = get_string();
    k %= 26;
    int p = 0;
    for(int i = 0; i < strlen(str); i++){
        if(isalpha(str[i])){
            if(isupper(str[i])){
                p = str[i] + k;
                if(p > 90){
                    p -= 26;
                };
                str[i] = p;
            }else{
                p = str[i] + k;
                if(p > 122){
                    p -= 26;
                };
                str[i] = p;
            };
        };
    };
    printf("ciphertext:\t%s\n", str);
    return 0;
}
