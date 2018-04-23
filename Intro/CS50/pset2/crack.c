#define _XOPEN_SOURCE

#include <unistd.h>
#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, string argv[]){
    if(argc != 2){
        printf("Usage: ./crack hash\n");
        return 1;
    }
    char salt[3];
    memset(salt, '\0', 3);
    strncpy(salt, argv[1], 2);
    char pass[20] = "";
    string char_list = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    
    //single character password decryption
    printf("\nTrying single character passwords...\n");
    for(int i = 0; i < strlen(char_list); i++){
        pass[0] = char_list[i];
        if(strcmp(argv[1], crypt(pass, salt)) == 0){
            printf("\nDecrypted password: %s\n\n", pass);
            return 0;
        };
    };
    
    //two character password decryption
    printf("\nPassword is not a single character.\nTrying two charcter passwords...\n");
    for(int i = 0; i < strlen(char_list); i++){
        pass[0] = char_list[i];
        for(int j = 0; j < strlen(char_list); j++){
            pass[1] = char_list[j];
            if(strcmp(argv[1], crypt(pass, salt)) == 0){
                printf("\nDecrypted password: %s\n\n", pass);
                return 0;
            };
        };
    };
    
    //three character password decryption
    printf("\nPassword is not two characters.\nTrying three character passwords...\n");
    for(int i = 0; i < strlen(char_list); i++){
        pass[0] = char_list[i];
        for(int j = 0; j < strlen(char_list); j++){
            pass[1] = char_list[j];
            for(int k = 0; k < strlen(char_list); k++){
                pass[2] = char_list[k];
                if(strcmp(argv[1], crypt(pass, salt)) == 0){
                    printf("\nDecrypted password: %s\n\n", pass);
                    return 0;
                };
            };
        };
    };
    
    //four character password decryption
    printf("\nPassword is not three characters.\nTrying four character passwords...\n");
    for(int i = 0; i < strlen(char_list); i++){
        pass[0] = char_list[i];
        for(int j = 0; j < strlen(char_list); j++){
            pass[1] = char_list[j];
            for(int k = 0; k < strlen(char_list); k++){
                pass[2] = char_list[k];
                for(int l = 0; l < strlen(char_list); l++){
                    pass[3] = char_list[l];
                    if(strcmp(argv[1], crypt(pass, salt)) == 0){
                        printf("\nDecrypted password: %s\n\n", pass);
                        return 0;
                    };
                };
            };
        };
    };
    printf("\nDecryption failed.\n\n");
    return 0;
};
