#include <stdio.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // ensure proper usage
    if(argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }
    
    // ensure image_in can open
    FILE *image = fopen(argv[1], "rb");
    if(image == NULL)
    {
        fprintf(stderr, "Could not open image.\n");
        return 2;
    }
    
    FILE *pic = fopen("000.jpg", "wb");
    BYTE buffer[512];
    
    // find start of first jpg
    int start = 0;
    while(start == 0)
    {
        fread(&buffer[0], sizeof(BYTE), 1, image);
        if(buffer[0] == 0xff)
        {
            fread(&buffer[1], sizeof(BYTE), 1, image);
            if(buffer[1] == 0xd8)
            {
                fread(&buffer[2], sizeof(BYTE), 1, image);
                if(buffer[2] == 0xff)
                {
                    fread(&buffer[3], sizeof(BYTE), 1, image);
                    if(buffer[3] == 0xe0 || buffer[3] == 0xe1)
                    {
                        start = 1;
                    }
                }
            }
        }
    }
    
    // write in header of first jpg
    fwrite(&buffer, sizeof(BYTE), 4, pic);
    
    // write in rest of beginning block
    fread(&buffer, sizeof(BYTE), 508, image);
    fwrite(&buffer, sizeof(BYTE), 508, pic);
    
    // main jpg write loop
    int count = 0;
    char name[8];
    while(start == 1)
    {
        fread(&buffer, sizeof(BYTE), 512, image);
        // check for EOF
        if(feof(image))
        {
            break;
        }
        // check for jpg header
        if(buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] == 0xe0 || buffer[3] == 0xe1))
        {
            fclose(pic);
            count++;
            sprintf(name, "%03d.jpg", count);
            pic = fopen(name, "wb");
        }
        fwrite(&buffer, sizeof(BYTE), 512, pic);
    }    
    
    // success
    fclose(pic);
    fclose(image);
    return 0;
}
