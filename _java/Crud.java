package _java;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;



class ConsoleManager
{
    public void clear()
    {
        System.out.print("\033[H\033[2J"); // doesnt erase console history
    }

    public void sleep()
    {
        try
        {
            Thread.sleep(1000);
        }
        catch (InterruptedException e)
        {
            Thread.currentThread().interrupt();
        }
    }

    public void exitConsole()
    {
        clear();
        System.out.println("exiting...");
        sleep();
        clear();
        System.exit(0);
    }

    public String getInput(String message)
    {
        try (Scanner scan = new Scanner(System.in))
        {
            System.out.print(message);
            String userInput = scan.nextLine().strip();

            if (userInput.equals(""))
            {
                System.out.println("you didn't write anything...");
                return "";
            }
            return userInput;
        }
    }
}


// TODO: complete DatabaseManager class
class DatabaseManager
{
    private ConsoleManager console = new ConsoleManager();
    private String filename;
    private File database;
    private FileWriter databaseWriter;



    private void checkDatabase(String file)
    {
        System.out.println(); // specific line spacing
        if (file.strip() == "")
        {
            System.out.println("no input given, defaulting to \"database.txt\"");
            filename = "database.txt";
        }
        else
            filename = file;

        System.out.println("checking...");
        console.sleep();

        try
        {
            database = new File(filename);
            if (database.createNewFile())
                System.out.println("database created!");
            else
                System.out.println("database exists!");
        }
        catch (IOException e)
        {
            System.out.println("something went wrong...");
            // TODO: manage exceptions properly
        }
    }

    private void updateDatabase(String action)
    {
        try
        {
            switch (action)
            {
                case "open": databaseWriter = new FileWriter(database);
                case "close": databaseWriter.close();
                case "flush": databaseWriter.flush();
            }
        }
        catch (IOException e)
        {
            System.out.println("something went wrong...");
            // TODO: manage exceptions properly
        }
    }

    public void setupManager(Boolean... fromMenu)
    {
        console.clear();
        updateDatabase("close");
        try (Scanner scan = new Scanner(System.in))
        {
            System.out.print("enter a database name\n> ");
            String userInput = scan.nextLine().strip();
            checkDatabase(userInput);
        }
        updateDatabase("open");
        console.sleep();
        if (!fromMenu[0])
            openMenu();
    }



    private void openMenu()
    {
        while (true)
        {
            console.clear();
            try (Scanner scan = new Scanner(System.in))
            {
                System.out.println(String.format("currently accessing database %s", filename));
                System.out.print("""
select an operation:

1- add value
2- search value
3- update value
4- delete value
5- switch database
6- exit

> """);
                String choice = scan.nextLine().strip();
                console.clear();
                switch (choice)
                {
                    case "1": // createValue();
                    case "2": // searchValue();
                    case "3": // updateValue();
                    case "4": // deleteValue();
                    case "5": setupManager(true);
                    case "6":
                        updateDatabase("close");
                        return;
                    default:
                        System.out.println("\nnot a valid option!");
                }
                updateDatabase("flush");
                if (choice != "5")
                {
                    console.sleep();
                    System.out.println("\npress enter to go back");
                }
                scan.nextLine();
                console.clear();
            }
        }
    }
}



public class Crud
{
    public static void main(String[] args)
    {
        // TODO: complete main()
    }
}