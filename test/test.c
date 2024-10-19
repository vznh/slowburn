#include <stdio.h>

int main() {
    int a = 10;
    int b = 0;
    int result = a / b;  // Division by zero leads to undefined behavior
    printf("Result: %d\n", result);
    return 0;
}
