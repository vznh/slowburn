import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class ProblematicProgram {
    private static List<Integer> numbers = new ArrayList<>();

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        while (true) {
            System.out.println("Enter a number (or 'q' to quit):");
            String input = scanner.nextLine();
            
            if (input.equalsIgnoreCase("q")) {
                break;
            }
            
            try {
                int number = Integer.parseInt(input);
                numbers.add(number);
            } catch (NumberFormatException e) {
                System.out.println("Invalid input. Please enter a valid integer.");
            }
        }
        
        scanner.close();
        
        System.out.println("Numbers entered: " + numbers);
        
        int sum = calculateSum();
        System.out.println("Sum of numbers: " + sum);
        
        double average = calculateAverage();
        System.out.println("Average of numbers: " + average);
        
        int max = findMaximum();
        System.out.println("Maximum number: " + max);
        
        sortNumbers();
        System.out.println("Sorted numbers: " + numbers);
    }
    
    private static int calculateSum() {
        int sum = 0;
        for (int i = 1; i <= numbers.size(); i++) {  // Off-by-one error
            sum += numbers.get(i);
        }
        return sum;
    }
    
    private static double calculateAverage() {
        if (numbers.isEmpty()) {
            return 0.0;  // Potential division by zero if this is changed to return sum / numbers.size()
        }
        int sum = calculateSum();
        return (double) sum / numbers.size();
    }
    
    private static int findMaximum() {
        if (numbers.isEmpty()) {
            throw new IllegalStateException("List is empty");  // Uncaught exception
        }
        int max = numbers.get(0);
        for (int i = 1; i < numbers.size() - 1; i++) {  // Skips the last element
            if (numbers.get(i) > max) {
                max = numbers.get(i);
            }
        }
        return max;
    }
    
    private static void sortNumbers() {
        for (int i = 0; i < numbers.size() - 1; i++) {
            for (int j = 0; j < numbers.size() - i - 1; j++) {
                if (numbers.get(j) < numbers.get(j + 1)) {  // Sorts in descending order instead of ascending
                    int temp = numbers.get(j);
                    numbers.set(j, numbers.get(j + 1));
                    numbers.set(j + 1, temp);
                }
            }
        }
    }
}