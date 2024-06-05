#include <iostream>
#include <memory>

class Shape
{
public:
    virtual void draw() const = 0; // pure virtual function
};

class Circle : public Shape
{
public:
    void draw() const override
    {
        std::cout << "Circle" << std::endl;
    }
};

class Square : public Shape
{
    public:
    void draw() const override
    {
        std::cout << "Square" << std::endl;
    }
};

std::unique_ptr<Shape> create_shape(const std::string &shape)
{
    if (shape == "circle")
    {
        return std::make_unique<Circle>();
    }
    else if (shape == "square")
    {
        return std::make_unique<Square>();
    }
    else
    {
        throw std::runtime_error("Unknown shape");
    }
}

int main(){
    Circle c;
    Square s;

    Shape *shapes[2] = {&c, &s};

    std::cout << "Drawing shapes using pointers" << std::endl;
    for (int i = 0; i < 2; i++)
    {
        shapes[i]->draw();
    }

    auto shape1_up = std::make_unique<Circle>();
    auto shape2_up = std::make_unique<Square>();
    
    std::unique_ptr<Shape> shapes_up[2] = {std::move(shape1_up), std::move(shape2_up)};

    std::cout << "Drawing shapes using unique pointers" << std::endl;
    for (int i = 0; i < 2; i++)
    {
        shapes_up[i]->draw();
    }

    // This will create a segmentation fault
    // shape1_up->draw();

    std::cout << "Drawing shapes using a function" << std::endl;
    for(auto &shape_name : {"circle", "square"}){
        create_shape(shape_name)->draw();
    }
    return 0;
}
