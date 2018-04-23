#include <stdio.h>
#include <cs50.h>

//my first attempt
int main()
{
   //card number aquisition
   long long num;
   printf("Enter a credit card number : ");
   num = get_long_long();
   
   //card number length check (too short)
   if (num < 340000000000000){
      printf("INVALID\n");
      return 0;
   };
   
   //for AMEX
   if (((num < 380000000000000) && (num > 370000000000000)) || ((num > 340000000000000) && (num < 350000000000000))){
      int two; int three; int four; int five; int six; int seven; int eight; int nine; 
      int ten; int eleven; int twelve; int thirteen; int fourteen; int fifteen;
      fifteen =   (num % 10); 
      fourteen =  (num % 100 -               (num % 10))/               10;
      thirteen =  (num % 1000 -              (num % 100))/              100;
      twelve =    (num % 10000 -             (num % 1000))/             1000; 
      eleven =    (num % 100000 -            (num % 10000))/            10000;
      ten =       (num % 1000000 -           (num % 100000))/           100000; 
      nine =      (num % 10000000 -          (num % 1000000))/          1000000;
      eight =     (num % 100000000 -         (num % 10000000))/         10000000; 
      seven =     (num % 1000000000 -        (num % 100000000))/        100000000;
      six =       (num % 10000000000 -       (num % 1000000000))/       1000000000; 
      five =      (num % 100000000000 -      (num % 10000000000))/      10000000000;
      four =      (num % 1000000000000 -     (num % 100000000000))/     100000000000; 
      three =     (num % 10000000000000 -    (num % 1000000000000))/    1000000000000;
      two =       (num % 100000000000000 -   (num % 10000000000000))/   10000000000000;
      int step_0 = 0; int step_1; int step_2;
      fourteen *= 2; twelve *= 2; ten *= 2; eight *= 2; six *= 2; four *= 2; two *= 2; 
      //add the digits of each digit product together
      if (two < 10)     {step_0 += two;}     else{step_0 += two % 10;      step_0 += (two - (two % 10))/10;};
      if (four < 10)    {step_0 += four;}    else{step_0 += four % 10;     step_0 += (four - (four % 10))/10;};
      if (six < 10)     {step_0 += six;}     else{step_0 += six % 10;      step_0 += (six - (six % 10))/10;};
      if (eight < 10)   {step_0 += eight;}   else{step_0 += eight % 10;    step_0 += (eight - (eight % 10))/10;};
      if (ten < 10)     {step_0 += ten;}     else{step_0 += ten % 10;      step_0 += (ten - (ten % 10))/10;};
      if (twelve < 10)  {step_0 += twelve;}  else{step_0 += twelve % 10;   step_0 += (twelve - (twelve % 10))/10;};
      if (fourteen < 10){step_0 += fourteen;}else{step_0 += fourteen % 10; step_0 += (fourteen - (fourteen % 10))/10;}
      step_1 = fifteen + thirteen + eleven + nine + seven + five + three + 3;
      step_2 = (step_0 + step_1) % 10;
      if (step_2 == 0){
         printf("AMEX\n");
         return 0;
      };
      printf("INVALID\n");
      return 0;
   };
   
   //for MasterCard
   if ((num > 5100000000000000) && (num < 5600000000000000)){
      int two; int three; int four; int five; int six; int seven; int eight; int nine; 
      int ten; int eleven; int twelve; int thirteen; int fourteen; int fifteen; int sixteen;
      sixteen =   (num % 10); 
      fifteen =   (num % 100 -                  (num % 10))/                  10; 
      fourteen =  (num % 1000 -                 (num % 100))/                 100;
      thirteen =  (num % 10000 -                (num % 1000))/                1000; 
      twelve =    (num % 100000 -               (num % 10000))/               10000;
      eleven =    (num % 1000000 -              (num % 100000))/              100000; 
      ten =       (num % 10000000 -             (num % 1000000))/             1000000;
      nine =      (num % 100000000 -            (num % 10000000))/            10000000; 
      eight =     (num % 1000000000 -           (num % 100000000))/           100000000; 
      seven =     (num % 10000000000 -          (num % 1000000000))/          1000000000;
      six =       (num % 100000000000 -         (num % 10000000000))/         10000000000; 
      five =      (num % 1000000000000 -        (num % 100000000000))/        100000000000;
      four =      (num % 10000000000000 -       (num % 1000000000000))/       1000000000000; 
      three =     (num % 100000000000000 -      (num % 10000000000000))/      10000000000000;
      two =       (num % 1000000000000000 -     (num % 100000000000000))/     100000000000000;
      int step_0 = 1; int step_1; int step_2;        //step_0 == 1 because 2*(the first number of mastercard will always be 5)%10
      fifteen *= 2; thirteen *= 2; eleven *= 2; nine *= 2; seven *= 2; five *= 2; three *= 2;
      if (three < 10)      {step_0 += three;}      else{step_0 += three % 10;       step_0 += (three - (three % 10))/10;};
      if (five < 10)       {step_0 += five;}       else{step_0 += five % 10;        step_0 += (five - (five % 10))/10;};
      if (seven < 10)      {step_0 += seven;}      else{step_0 += seven % 10;       step_0 += (seven - (seven % 10))/10;};
      if (nine < 10)       {step_0 += nine;}       else{step_0 += nine % 10;        step_0 += (nine - (nine % 10))/10;};
      if (eleven < 10)     {step_0 += eleven;}     else{step_0 += eleven % 10;      step_0 += (eleven - (eleven % 10))/10;};
      if (thirteen < 10)   {step_0 += thirteen;}   else{step_0 += thirteen % 10;    step_0 += (thirteen - (thirteen % 10))/10;};
      if (fifteen < 10)    {step_0 += fifteen;}    else{step_0 += fifteen % 10;     step_0 += (fifteen - (fifteen % 10))/10;};
      step_1 = sixteen + fourteen + twelve + ten + eight + six + four + two;
      step_2 = (step_0 + step_1) % 10;
      if (step_2 == 0){
         printf("MASTERCARD\n");
         return 0;
      };
      printf("INVALID\n");
      return 0;
   };
   
   //for VISA
   if ((num > 4000000000000000) && (num < 5000000000000000)){
      int two; int three; int four; int five; int six; int seven; int eight; int nine; 
      int ten; int eleven; int twelve; int thirteen; int fourteen; int fifteen; int sixteen;
      sixteen =   (num % 10); 
      fifteen =   (num % 100 -                  (num % 10))/                  10; 
      fourteen =  (num % 1000 -                 (num % 100))/                 100;
      thirteen =  (num % 10000 -                (num % 1000))/                1000; 
      twelve =    (num % 100000 -               (num % 10000))/               10000;
      eleven =    (num % 1000000 -              (num % 100000))/              100000; 
      ten =       (num % 10000000 -             (num % 1000000))/             1000000;
      nine =      (num % 100000000 -            (num % 10000000))/            10000000; 
      eight =     (num % 1000000000 -           (num % 100000000))/           100000000;
      seven =     (num % 10000000000 -          (num % 1000000000))/          1000000000;
      six =       (num % 100000000000 -         (num % 10000000000))/         10000000000; 
      five =      (num % 1000000000000 -        (num % 100000000000))/        100000000000;
      four =      (num % 10000000000000 -       (num % 1000000000000))/       1000000000000; 
      three =     (num % 100000000000000 -      (num % 10000000000000))/      10000000000000;
      two =       (num % 1000000000000000 -     (num % 100000000000000))/     100000000000000;
      int step_0 = 8; int step_1; int step_2;         //step_0 == 8 because 2*(the first number of a VISA will always be 4)%10
      fifteen *= 2; thirteen *= 2; eleven *= 2; nine *= 2; seven *= 2; five *= 2; three *= 2;
      if (three < 10)      {step_0 += three;}      else{step_0 += three % 10;       step_0 += (three - (three % 10))/10;};
      if (five < 10)       {step_0 += five;}       else{step_0 += five % 10;        step_0 += (five - (five % 10))/10;};
      if (seven < 10)      {step_0 += seven;}      else{step_0 += seven % 10;       step_0 += (seven - (seven % 10))/10;};
      if (nine < 10)       {step_0 += nine;}       else{step_0 += nine % 10;        step_0 += (nine - (nine % 10))/10;};
      if (eleven < 10)     {step_0 += eleven;}     else{step_0 += eleven % 10;      step_0 += (eleven - (eleven % 10))/10;};
      if (thirteen < 10)   {step_0 += thirteen;}   else{step_0 += thirteen % 10;    step_0 += (thirteen - (thirteen % 10))/10;};
      if (fifteen < 10)    {step_0 += fifteen;}    else{step_0 += fifteen % 10;     step_0 += (fifteen - (fifteen % 10))/10;};
      step_1 = sixteen + fourteen + twelve + ten + eight + six + four + two;
      step_2 = (step_0 + step_1) % 10;
      if (step_2 == 0){
         printf("VISA\n");
         return 0;
      };
      printf("INVALID\n");
      return 0;
   };
   
   //else number too long (INVLAID)
   printf("INVALID\n");
   return 0;
}

/*

//    my second attempt
#include <stdio.h>
#include <math.h>
#include <cs50.h>

int main(void){
   
   //card number aquisition
   long long num;
   printf("Enter a credit card number : ");
   num = get_long_long();
   
   //card number length check (too short)
   if(num < 34e+13){
      printf("INVALID\n");
      return 0;
   };
   
   //for AMEX
   if(((num < 38e+13) && (num > 37e+13)) || ((num > 34e+13) && (num < 35e+13))){
      long long num_list[15];
      for(int i = 15; i > 0; i--){
         long long mod_1 = pow(10, i);
         long long mod_2 = pow(10, i-1);
         if (num % mod_1 == num % mod_2){
            num_list[i-1] = 0;
         }else{
            num_list[i-1] = (num % mod_1 - num % mod_2)/mod_2;
         };
      };
      for(int i = 13; i >= 0; i -= 2){
         num_list[i] *= 2;
      };
      int sum = 0;
      for(int i = 0; i < 15; i++){
         if(num_list[i] > 9){
            sum += num_list[i] % 10;
            sum += (num_list[i] - num_list[i] % 10)/10;
         }else{
         sum += num_list[i];   
         };
      };
      if(sum % 10 == 0){
         printf("AMEX\n");
      }else{
         printf("INVALID\n");
      }
      return 0;
   };
   
   //for MasterCard
   if ((num > 51e+14) && (num < 56e+14)){
      long long num_list[16];
      for(int i = 16; i > 0; i--){
         long long mod_1 = pow(10, i);
         long long mod_2 = pow(10, i-1);
         if(num % mod_1 == num % mod_2){
            num_list[i-1] = 0;
         }else{
            num_list[i-1] = (num % mod_1 - num % mod_2)/mod_2;
         };
      };
      for(int i = 15; i >= 0; i -= 2){
         num_list[i] *= 2;
      };
      int sum = 0;
      for(int i = 0; i < 16; i++){
         if(num_list[i] > 9){
            sum += num_list[i] % 10;
            sum += (num_list[i] - num_list[i] % 10)/10;
         }else{
         sum += num_list[i];   
         };
      };
      if(sum % 10 == 0){
         printf("MASTERCARD\n");
      }else{
         printf("INVALID\n");
      }
      return 0;
   };
   
   //for VISA
   if ((num > 4e+15) && (num < 5e+15)){
      long long num_list[16];
      for(int i = 16; i > 0; i--){
         long long mod_1 = pow(10, i);
         long long mod_2 = pow(10, i-1);
         if(num % mod_1 == num % mod_2){
            num_list[i-1] = 0;
         }else{
            num_list[i-1] = (num % mod_1 - num % mod_2)/mod_2;
         };
      };
      for(int i = 15; i >= 0; i -= 2){
         num_list[i] *= 2;
      };
      int sum = 0;
      for(int i = 0; i < 16; i++){
         if(num_list[i] > 9){
            sum += num_list[i] % 10;
            sum += (num_list[i] - num_list[i] % 10)/10;
         }else{
         sum += num_list[i];   
         };
      };
      if(sum % 10 == 0){
         printf("VISA\n");
      }else{
         printf("INVALID\n");
      }
      return 0;
   };
   
   //else number too long (INVLAID)
   printf("INVALID\n");
   return 0;
}                                         */
