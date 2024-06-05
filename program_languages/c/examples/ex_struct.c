#include <stdio.h>
#include <string.h>

struct friend {
    char name[50];
    int age;
};


struct student {
    char name[50];
    int roll;
    float marks;
    struct friend frd;
};


int main() {
    struct student s1 = {"John", 12, 98.5, {"Alice", 13}};

    struct student s2 = s1;
    strcpy(s2.name, "Jane");
    strcpy(s2.frd.name, "Bob");
    s2.frd.age = 14;


    printf("Student 1\n");
    printf("Name: %s\n", s1.name);
    printf("Roll: %d\n", s1.roll);
    printf("Marks: %.2f\n", s1.marks);
    printf("Friend: %s\n", s1.frd.name);
    printf("Friend's age: %d\n", s1.frd.age);

    printf("\nStudent 2\n");
    printf("Name: %s\n", s2.name);
    printf("Roll: %d\n", s2.roll);
    printf("Marks: %.2f\n", s2.marks);
    printf("Friend: %s\n", s2.frd.name);
    printf("Friend's age: %d\n", s2.frd.age);
    
    return 0;
}