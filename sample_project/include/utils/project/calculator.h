#ifndef CALCULATOR_H
#define CALCULATOR_H

namespace MyOrg { // Example potential anonymization target

/**
 * @brief A simple calculator class.
 * Provided by MyOrg Tech Solutions.
 */
class Calculator {
public:
    /**
     * @brief Adds two integers.
     * @param a The first integer.
     * @param b The second integer.
     * @return The sum of a and b.
     */
    int add(int a, int b);

    /**
     * @brief Subtracts two integers.
     * @param a The first integer.
     * @param b The second integer.
     * @return The result of a - b.
     */
    int subtract(int a, int b);
};

} // namespace MyOrg

#endif // CALCULATOR_H