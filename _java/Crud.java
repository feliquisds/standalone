package _java;
import java.util.Scanner;



class ConsoleManager {
    void clear() {
        System.out.print("\033[H\033[2J"); // doesnt erase console history
    }

    void sleep() {
        try {
            Thread.sleep(1000);
        }
        catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    void exitConsole() {
        clear();
        System.out.println("exiting...");
        sleep();
        clear();
        System.exit(0);
    }

    String getInput(String message) {
        try (Scanner scan = new Scanner(System.in)) {
            System.out.print(message);
            String userInput = scan.nextLine().strip();

            if (userInput.equals("")) {
                System.out.println("you didn't write anything...");
                return "";
            }
            return userInput;
        }
    }
}



class DatabaseManager {
    // TODO: complete DatabaseManager class
}



public class Crud {

    public static void main(String[] args) {
        // TODO: complete main()
    }
}