package _java;
import java.io.*;
import java.util.*;



class ConsoleManager
{
    private ConsoleManager()
    {
        throw new IllegalStateException("utility class");
    }

    static Scanner scan = new Scanner(System.in);

    public static void clear()
    {
        System.out.print("\033[H\033[2J"); // doesnt erase console history
    }

    public static void sleep()
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

    public static void exit()
    {
        clear();
        System.out.println("exiting...");
        sleep();
        clear();
        System.exit(0);
    }

    public static String input(String message)
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



class DatabaseManager
{
    private String filename;
    private File database;



    private void checkDatabase(String file)
    {
        System.out.println(); // specific line spacing
        if (file.strip().equals(""))
        {
            System.out.println("no input given, defaulting to \"database.txt\"\n");
            ConsoleManager.sleep();
            filename = "database.txt";
        }
        else filename = file;

        System.out.println("checking...\n");
        ConsoleManager.sleep();

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
            System.out.println(String.format("something went wrong...%n'%s'", e));
        }
    }

    public void setupDatabase(Boolean openMenu)
    {
        ConsoleManager.clear();
        System.out.print("enter a database name\n> ");
        checkDatabase(ConsoleManager.scan.nextLine().strip());
        ConsoleManager.sleep();
        if (Boolean.TRUE.equals(openMenu))
            openMenu();
    }



    private void openMenu()
    {
        while (true)
        {
            ConsoleManager.clear();

            System.out.println(String.format("currently accessing '%s'%n", filename));
            System.out.println("""
select an operation:

1- add value
2- search value
3- update value
4- delete value
5- switch database
6- exit""");
            System.out.print("\n> ");

            String choice = ConsoleManager.scan.nextLine().strip();   
            ConsoleManager.clear();
            switch (choice)
            {
                case "1":
                    createEntry();
                    break;
                case "2":
                    // TODO: search function
                    break;
                case "3":
                    // TODO: update function
                    break;
                case "4":
                    // TODO: delete function
                    break;
                case "5":
                    setupDatabase(false);
                    break;
                case "6":
                    return;
                default:
                    System.out.println("\nnot a valid option!");
            }
            if (!choice.equals("5"))
            {
                ConsoleManager.sleep();
                System.out.println("\npress enter to go back");
                ConsoleManager.scan.nextLine();
            }
            ConsoleManager.clear();
        }
    }



    private Map<Integer, String> internalGetInfo(String valueToSearch, Set<Integer> indexesToSkip)
    {
        System.out.println("\nchecking database...");
        ConsoleManager.sleep();

        if (indexesToSkip == null) indexesToSkip = new HashSet<>();

        try (Scanner scan = new Scanner(database))
        {
            for (int i = 0; scan.hasNextLine(); i++)
            {
                String line = scan.nextLine();
                if (line.contains(valueToSearch.strip()) && !indexesToSkip.contains(i))
                {
                    System.out.println(String.format("match found!%n%non line %s: %s", i, line));
                    Map<Integer, String> result = new HashMap<>();
                    result.put(i, line);
                    return result;
                }
            }

            System.out.println("no entries found...");
        }
        catch (FileNotFoundException e)
        {
            System.out.println("file not found...");
        }
        
        return Collections.emptyMap();
    }



    private void createEntry()
    {
        String inputValue = ConsoleManager.input("add something to the database:\n> ");
        if (inputValue.equals("")) return;

        Map<Integer, String> searchResult = internalGetInfo(inputValue, null);
        if (searchResult.get(1) != null)
        {
            System.out.print("\nregister a duplicate anyway? y/n\n> ");
            String option = ConsoleManager.scan.nextLine().strip().toLowerCase();
            if (!option.equals("y"))
            {
                System.out.println(option.equals("n") ?
                "\noperation has been canceled" :
                "\ninvalid option! finishing registration...");
                return;
            }
        }

        System.out.println("\nregistering to database...");
        ConsoleManager.sleep();

        try (FileWriter writer = new FileWriter(database, true))
        {
            writer.write(String.format("%s%n", inputValue));
            System.out.println("all registered!"); // read like Elizabeth from Persona 3
        }
        catch (IOException e)
        {
            System.out.println(String.format("failed to register!%n'%s'", e));
        }
    }
}



public class Crud
{
    public static void main(String[] args)
    {
        DatabaseManager db = new DatabaseManager();

        try
        {
            loop: while (true)
            {
                ConsoleManager.clear();
                System.out.print("no database manager is open, access one? y/n\n> ");
                switch (ConsoleManager.scan.nextLine().strip().toLowerCase())
                {
                    case "y":
                        db.setupDatabase(true);
                        break;
                    case "n":
                        ConsoleManager.exit();
                        break loop;
                    default:
                        System.out.println("\ninvalid option! press enter to try again");
                        ConsoleManager.scan.nextLine();
                }
            }
        }
        catch (NoSuchElementException e)
        {
            ConsoleManager.exit();
        }
    }
}