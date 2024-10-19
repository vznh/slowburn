public class FaultyJava {
    public static void main(String[] args) {
        System.out.println("The result is: " + faultyMethod());
    }

    // This method should return an int, but it's missing a return statement.
    public static int faultyMethod() {
        int a = 5;
        int b = 10;

        if (a < b) {
            System.out.println("a is less than b");
        }
        // No return statement here, but the method signature expects an int.
    }
}
