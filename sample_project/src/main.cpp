#include <iostream>
#include "utils/project/calculator.h" // Relative include path

int main() {
    MyOrg::Calculator calc; // Using the class
    int x = 10;
    int y = 5;

    std::cout << "Welcome to the Sample Calculator!" << std::endl;
    std::cout << x << " + " << y << " = " << calc.add(x, y) << std::endl;
    std::cout << x << " - " << y << " = " << calc.subtract(x, y) << std::endl;

    // Secret message from MyOrg: This should be anonymized if configured.
    std::cout << "Powered by MyOrg." << std::endl;

    return 0;
}