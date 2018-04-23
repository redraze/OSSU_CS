// Implements a dictionary's functionality.

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "dictionary.h"

// index for how may words have been loaded
unsigned int word_count = 0;

// define node structure type
typedef struct node{
    // booleans for each letter of the alphabet [0-25], the apostrophe character [26], and the end character [27]
    bool characters[28];
    // nodes for each letter of the alphabet [0-25] and the apostrophe character [26]
    struct node *next[27];
} node_t;
    
// create trie root pointer
node_t *root_ptr = NULL;

// prototype to assist in unload
void refree(node_t *pointer);

// Returns true if word is in dictionary else false.
bool check(const char *word)
{
    // create copy of word and reformat
    char temp[strlen(word) + 1];
    for (int i = 0; i < strlen(word); i++){
        if (isalpha(word[i]))
        {
            temp[i] = tolower(word[i]);
        }
        else
        {
            temp[i] = word[i];
        }
    }
    temp[strlen(word)] = '\0';
    
    // check word against loaded dictionary
    node_t *ptr = root_ptr;
    for (int i = 0; i < strlen(temp); i++)
    {
        // check for apostrophe
        if (temp[i] == '\'')
        {
            if (ptr->characters[26] == true)
            {
                ptr = ptr->next[26];
            }
            else
            {
                return false;
            }
        }
        else
        {
            if (ptr->characters[temp[i] - 97] == true)
            {
                ptr = ptr->next[temp[i] - 97];
            }
            else
            {
                return false;
            }
        }
    }
    
    // check for null character
    if (ptr->characters[27] == true)
    {
        return true;
    }
    return false;
}

// Loads dictionary into memory. Returns true if successful else false.
bool load(const char *dictionary)
{
    // check to make sure dictionary exists
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL){return false;}
    
    // create trie root
    node_t *root = malloc(sizeof(node_t));
    root_ptr = root;
        
    // temp word storage
    char buffer[LENGTH];
    for (int i = 0; i < LENGTH; i++){
        buffer[i] = '\0';
    }
    
    // iterate through each character of dictionary
    int index = 0;
    for (char c = fgetc(dict); c != EOF; c = fgetc(dict))
    {
        // check for end of word
        if (c == '\n')
        {
            node_t *ptr = root;
            index = 0;
            while (buffer[index] != '\0')
            {
                // check for apostrophe
                if (buffer[index] - 97 < 0)
                {
                    ptr->characters[26] = true;
                    // check for null pointer
                    if (ptr->next[26] == NULL)
                    {
                        // create new node
                        node_t *node = malloc(sizeof(node_t));
                        ptr->next[26] = node;
                        // follow new node
                        ptr = ptr->next[26];
                    }
                    else
                    {
                        ptr = ptr->next[26];
                    }
                }
                else
                {
                    ptr->characters[buffer[index] - 97] = true;
                    // check for null pointer
                    if (ptr->next[buffer[index] - 97] == NULL)
                    {
                        // create new node
                        node_t *node = malloc(sizeof(node_t));
                        ptr->next[buffer[index] - 97] = node;
                        // follow new node
                        ptr = ptr->next[buffer[index] - 97];
                    }
                    else
                    {
                        ptr = ptr->next[buffer[index] - 97];
                    }
                }
                index++;
            }
            // check null character
            ptr->characters[27] = true;
            
            // reset
            index = 0;
            for (int i = 0; i < LENGTH; i++){
                buffer[i] = '\0';
            }
            
            // track word count
            word_count++;
        }
        else
        {
        // store word from dictionary to temp storage
        buffer[index] = c;
        index++;
        }
    }

    // close and return
    fclose(dict);
    return true;
}

//Returns number of words in dictionary if loaded else 0 if not yet loaded.
unsigned int size(void)
{
    if(word_count)
    {
        return word_count;
    }
    return 0;
}

// Unloads dictionary from memory. Returns true if successful else false.
bool unload(void)
{
    // free branches
    refree(root_ptr);

    // free root
    free(root_ptr);

    return true;
}

void refree(node_t *pointer)
{
    for (int i = 0; i < 27; i++)
    {
        if (pointer->next[i] != NULL)
        {
            refree(pointer->next[i]);
            free(pointer->next[i]);
        }
    }
}
