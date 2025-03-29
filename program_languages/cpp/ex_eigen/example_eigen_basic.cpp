#include <iostream>
#include <Eigen/Dense>

void ex_basic()
{
    Eigen::Matrix2d mat;
    mat(0, 0) = 3;
    mat(1, 0) = 2.5;
    mat(0, 1) = -1;
    mat(1, 1) = mat(1, 0) + mat(0, 1);

    std::cout << "Here is the matrix mat:\n" << mat << std::endl;

    Eigen::Vector2d vec(1, 2);
    std::cout << "Here is the vector vec:\n" << vec << std::endl;

    Eigen::Vector2d result = mat * vec;
    std::cout << "The result of mat * vec is:\n" << result << std::endl;

    Eigen::MatrixXd mat10x10 = Eigen::MatrixXd::Identity(10, 5);
    std::cout << "Here is a 10x10 matrix filled with random values:\n" << mat10x10 << std::endl;

}

void random_const_ex()
{
    Eigen::MatrixXd mat = Eigen::MatrixXd::Random(3, 3);
    mat = (mat + Eigen::MatrixXd::Constant(3, 3, 1.2)) * 50;
    std::cout << "mat = " << mat << std::endl;
    Eigen::VectorXd v(3);
    v << 1, 2, 3;
    std::cout << "v = " << v << std::endl;
    std::cout << "Doing mat * v" << std::endl;
    std::cout << mat * v << std::endl;
}

void assignment_ex()
{
    Eigen::MatrixXd mat(5, 2);
    mat(0) = 1.0;
    mat(2,0) = 3.0;
    mat(8|) = 6.0;

    std::cout << "mat = \n" << mat << std::endl;
}

int main() {

    ex_basic();
    random_const_ex();
    assignment_ex();

    return 0;
}