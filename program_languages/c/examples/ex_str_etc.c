#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

void strupper_ex()
{
    char s[] = "Hello";
    char *s1 = s;
    // loop through the string. Ends when the null character is reached
    while (*s1)
    {
        *s1 = toupper(*s1); // ctype.h function to convert to upper case
        s1++;
    }
    printf("after strupper_ex: %s\n", s);
    if (*s1 == '\0')
    {
        printf("s1 is null\n");
    }
}

void ptr_bracket_ex()
{
    // s[i] is equivalent to *(s + i)
    char s[] = "Hello";
    // (int) casting is necessary to avoid warning
    for (int i = 0; i < (int)strlen(s); i++)
    {
        printf("s[%d]: %c\n", i, s[i]);
        printf("*(s + %d): %c\n", i, *(s + i));
    }
}

void stralloc_ex()
{
    char *s = (char *)calloc(6, sizeof(char));
    s[0] = 'H';
    s[1] = 'e';
    s[3] = 'l'; // this will not be printed as s[2] is null
    printf("stralloc_ex: %s\n", s);
    free(s); // this needs to be freed. Otherwise, memory leak.
}

void sizeof_ex()
{
    double d;
    // two ways to get the size of a variable
    // note: zu is the format specifier for unsigned long, which is the return type of sizeof
    printf("sizeof(d): %zu\n", sizeof(d));
    printf("sizeof(double): %zu\n", sizeof(double));
}

void str_empty_ex()
{
    char s[] = "Hello";
    // A string can be emptied by setting the first character to null
    *s = 0;
    printf("str_empty_ex: %s\n", s);

    // to check if a string is NOT empty,
    int is_not_empty = s && *s; // if s is not null and the first character is not null
    printf("is_not_empty: %d\n", is_not_empty);
}

void str_is_space_ex()
{
    char so[] = "  ";
    char *s = so;

    // check if a string is space
    char ch;
    while ((ch = *s++) != '\0')
    {
        if (!isspace(ch))
        {
            printf("Not a space\n");
            break;
        }
    }
    printf("Is a space\n");
}

void bool_ex()
{
    int x = 10;
    int y = !x;
    int z = !!x;

    printf("x: %d, y: %d, z: %d\n", x, y, z);
}

void str_repeat_ex()
{
    char s[] = "Hello";
    char *s1 = s;
    int size = strlen(s);
    char c;
    while (size--)
    {
        c = *s1++;
        printf("c: %c\n", c);
    }

    size = strlen(s);
    s1 = s;

    // the value of size is decremented after the statement is executed
    while (size--)
    {
        // size is decremented after the statement is executed
        printf("size: %d\n", size);

        *s1++ = 'a';
        // this will print the next character in the string
        printf("*s1: %c\n", *s1);
    }
    printf("s: %s\n", s);
}

void loop_ex()
{
    int loop = 3;
    // this makes the loop run 'loop' times
    while (loop--)
    {
        printf("loop: %d\n", loop);
    }

    int loop2 = 3;
    // this makes the loop run 'loop2' times
    for (int i = 0; i < loop2; i++)
    {
        printf("i: %d\n", i);
    }
}

void strncpy_ex()
{
    int num = 10;
    char *dest = malloc(num * sizeof(char));
    // this is NOT safe.
    strncpy(dest, "qwertyuiopfefefwfew", num + 5);
    printf("dest: %s\n", dest);

    char *src = "12345678901";
    strncpy(dest, src, num);
    printf("dest: %s\n", dest);
    for (int i = 0; i < num + 1; i++)
    {
        printf("dest[%d]: %c\n", i, dest[i]);
    }
    free(dest);

    char dest2[10] = "abcdefghi";
    char *src2 = "Hello";
    // This will add a null character at the end of the string
    char *p = strcpy(dest2, "X");
    printf("p: %s\n", p);
    printf("address dest2: %p, p: %p\n", dest2, p);
    printf("p\n");
    for (int i = 0; i < 10; i++)
    {
        printf("p[%d]: %c\n", i, p[i]);
    }

    // This will add a null character at the end of the string (why?)
    strncat(p, src2, strlen(src2));
    printf("dest2: %s\n", dest2);
    for (int i = 0; i < 10; i++)
    {
        printf("p[%d]: %c\n", i, p[i]);
    }
}

#define STRCPY_STRNCPY_EX_SIZE 10
void strcpy_strncpy_ex()
{
    char *src = "Hello";

    printf("*** strcpy\n");
    // strcpy: copies the string from src to dest and add a null at the end.
    // Hence, the size of dest should be at least strlen(src) + 1
    // Otherwise, it will cause a segmentation fault
    char dest[STRCPY_STRNCPY_EX_SIZE] = "1234567890";
    strcpy(dest, src);
    printf("dest: %s\n", dest);
    for (int i = 0; i < STRCPY_STRNCPY_EX_SIZE; i++)
    {
        printf("dest[%d]: %c\n", i, dest[i]);
    }

    printf("*** strncpy\n");
    // strncpy: copies always the number of characters specified in the third argument.
    // If the string is shorter than the number of characters, it copies the string 
    // and add null to the end.
    char dest2[STRCPY_STRNCPY_EX_SIZE] = "1234567890";
    strncpy(dest2, src, STRCPY_STRNCPY_EX_SIZE);
    printf("dest2: %s\n", dest);
    for (int i = 0; i < STRCPY_STRNCPY_EX_SIZE; i++)
    {
        printf("dest2[%d]: %c\n", i, dest2[i]);
    }

    // Let's copy less than the size of the source.
    // As it is less than the size of the source, it will NOT add a null at the end
    char dest3[STRCPY_STRNCPY_EX_SIZE] = "1234567890";
    strncpy(dest3, src, strlen(src) - 2);
    printf("dest3: %s\n", dest3);
    for (int i = 0; i < STRCPY_STRNCPY_EX_SIZE; i++)
    {
        printf("dest3[%d]: %c\n", i, dest3[i]);
    }
    
    // Let's copy more than the size of the source, but less than the size of the destination.
    char dest4[STRCPY_STRNCPY_EX_SIZE] = "1234567890";
    strncpy(dest4, src, strlen(src) + 2);
    printf("dest4: %s\n", dest4);
    for (int i = 0; i < STRCPY_STRNCPY_EX_SIZE; i++)
    {
        printf("dest4[%d]: %c\n", i, dest4[i]);
    }



}

void str_repeat_ex2()
{
    char so[] = "Hello";
    char *s = so;
    char ch = 'x';
    int size = 3;

    while (size--)
        *s++ = ch; // Replace *s with ch and increment s
    *s = '\0';     // Null terminate the string
    printf("s: %s\n", so);
}

void free_str_pointer(char **ps)
{
    // free if the pointer is not null
    if (*ps)
    {
        free(*ps);  // free this pointer
        *ps = NULL; // and set it to null. This is necessary to avoid dangling pointer
    }
}

void free_ex()
{
    char *s = (char *)malloc(10 * sizeof(char));
    printf("s: %p\n", s);
    free(s);
    printf("s: %p\n", s);
    s = NULL; // this is necessary to avoid dangling pointer
    printf("s: %p\n", s);

    char *s2 = (char *)malloc(10 * sizeof(char));
    printf("s2: %p\n", s2);
    free_str_pointer(&s2);
    printf("s2: %p\n", s2);
}

void const_car_ex()
{
    char s[] = "Hello";
    char *result = s;
    printf("result: %s\n", result);
    printf("result p: %p\n", result);
    result = "";
    printf("result: %s\n", result);
    printf("result p: %p\n", result);
}

const char *strvalgetn(char** d)
{
    const char *result = *d;
    if (!result) result = "";
    return result;
}

void ptr_to_str_ex()
{
    char *s = "Hello";
    s[0] = 'a'; // this will cause a segmentation fault
    printf("s: %s\n", s);
}

const char* getGreeting(){
    return "Hello";
}

void const_char_ex(){
    const char *s = getGreeting();
    // s[0] = 'h'; // this creates a compilation error
    printf("s: %s\n", s);
    // s[0] = 'a'; // this will cause a segmentation fault

    const char s2[] = "Hello";
    //s2[0] = 'a'; // this creates a compilation error
    char* s3 = s2;
    s3[0] = 'a'; // this is allowed
}

void str_funs_ex(){
    char *s = "Hello";
    char *s2 = strdup(s);
    printf("s2: %s\n", s2);
    free(s2);

}

void sprintf_ex1(){

    // sprintf: this can create a buffer overflow if the buffer is not big enough
    int age = 30;
    char name[] = "John Doe";
    char result_sprintf[100];

    sprintf(result_sprintf, "Name: %s, Age: %d", name, age);
    printf("result_sprintf: %s\n", result_sprintf);

    // snprintf: control with the size of the buffer
    // In this example, only the first 9 characters are copied to the buffer 
    // and the 10th character is null
    char result2_snprintf[10];
    snprintf(result2_snprintf, 10, "Name: %s, Age: %d", name, age);
    printf("result2: %s\n", result2_snprintf);
    for (int i = 0; i < 10; i++)
    {
        printf("result2_snprintf[%d]: %c\n", i, result2_snprintf[i]);
    }
}

void printPointer(void* ptr) {
    printf("Pointer address: %p\n", ptr);
}

void void_pointer_ex() {
    int x = 10;
    double y = 20.0;

    printPointer(&x);
    printPointer(&y);

}

void sscanf_ex(){
    char s[] = "AB232C ss10:XYZ:20";
    char name[10];
    int res = sscanf(s, "%s", name);
    printf("name: %s\n", name);
    printf("s: %s\n", s);
    printf("res: %d\n", res);

    char s2[] = " A234BCD";
    int res2 = sscanf(s2, "%s", name);
    printf("name: %s\n", name);
    printf("s2: %s\n", s2);
    printf("res2: %d\n", res2);
}

void str_array_len_ex(){
    char s[] = "Hello";
    printf("size of \"Hello\": %d\n", (int)(sizeof(s)/sizeof(s[0])));
}

void strstr_ex()
{
    char s[] = "Hello";
    char *s1 = strstr(s, "ll");
    printf("s1: %s\n", s1);

    char *s2 = strstr(s, "oo");
    printf("s2: %s\n", s2);
}

int main()
{

    // strupper_ex();
    // ptr_bracket_ex();
    // stralloc_ex();
    // sizeof_ex();
    // str_empty_ex();
    // bool_ex();
    // str_repeat_ex();
    // loop_ex();
    // strncpy_ex();
    // strcpy_strncpy_ex();
    // str_repeat_ex2();
    // free_ex();
    // const_car_ex();
    // ptr_to_str_ex();
    // const_char_ex();
    // strdup_ex();
    // sprintf_ex1();
    // void_pointer_ex();
    sscanf_ex();
    // str_array_len_ex();
    //strstr_ex();
    return 0;
}