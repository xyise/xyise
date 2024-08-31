#include <stdio.h>
#include <string.h>

struct person {char name[10]; };

struct person a = {"A"}, b = {"B"}, c = {"C"}, d = {"D"}, e = {"E"}, z = {"Z"}, *ptr;

void make_z1(struct person *p)
{
    strcpy(p->name, z.name);
}

void make_z2(struct person *p)
{
    *p = z;
}

void make_z3(struct person *p)
{
    p = (struct person *)malloc(sizeof(struct person));
    memcpy(p, &z, (sizeof(struct person)));
}

void make_z4(struct person *p)
{
    p = &z;
}

struct person *make_z5()
{
    return &z;
}

void make_z6(struct person * const p)
{
    *p = z;
}

void print(struct person *p)
{
    printf("%s\n", p->name);
}

int main()
{
    make_z1(&a); print(&a);
    make_z2(&b); print(&b);
    make_z3(&c); print(&c);
    make_z4(&d); print(&d);
    ptr = make_z5(); print(ptr);
    make_z6(&e); print(&e);
    return 0;
}