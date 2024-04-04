import sys
import time
import os



clear = lambda: os.system('cls')

def exit(clearScreen: bool) -> None:
    if clearScreen:
        clear()
    print("exiting...")
    time.sleep(1)
    clear()
    sys.exit()



def WriteToDatabase() -> None:
    string = input("add something to the database:\n")

    if string == "":
        print("you didn't write anything...")
        return
    
    clear()
    print("checking database...")
    time.sleep(1)

    f = open("database.txt", "r")
    for idx, x in enumerate(f):
        if string == x.strip():
            print(f"\nduplicate found!\non line {idx}: {x.strip()}")

            option = input("\nregister anyway? y/n\n")
            if option.strip() == "y":
                print("")
                f.close()
                break
            else:
                print("\noperation has been canceled" if option == "n" else "\ninvalid option! finishing registration...")
                f.close()
                return
    
    print("registering to database...")
    time.sleep(1)

    f = open("database.txt", "a")
    f.write(f"\n{string}")
    f.close()
    print("all registered!")



def SearchDatabase() -> None:
    string = input("search for something in the database:\n")

    if string == "":
        print("you didn't search anything...")
        return
    
    clear()
    print("searching the database...")
    time.sleep(1)

    f = open("database.txt", "r")
    for idx, x in enumerate(f):
        if string in x:
            print(f"match found!\non line {idx}: {x.strip()}")

            option = input("\ncontinue searching? y/n\n")
            if option.strip() == "y":
                clear()
                print("searching the database...")
                time.sleep(1)
            else:
                print("\nsearch done!" if option == "n" else "\ninvalid option! finishing search...")
                f.close()
                return

    f.close()
    print("no results found...")



def DeleteInDatabase() -> None:
    string = input("search for something to delete in the database:\n")

    if string == "":
        print("you didn't search anything...")
        return
    
    clear()
    print("checking database...")
    time.sleep(1)

    f = open("database.txt", "r")
    data = f.readlines()
    f.close()

    f = open("database.txt", "r")
    for idx, x in enumerate(f):
        if string == x.strip():
            print(f"\nmatch found!\non line {idx}: {x.strip()}")

            option = input("\ndelete it? y/n\n")
            if option.strip() == "y":
                print("\ndeleting...")
                time.sleep(1)
                
                del data[idx]
                f.close()

                f = open("database.txt", "w")
                f.writelines(data)
                print("successful!")
                f.close()
                return
            else:
                print("\noperation has been canceled" if option == "n" else "\ninvalid option! finishing operation...")
                f.close()
                return
    
    f.close()
    print("no results found...")



def UpdateDatabase() -> None:
    string = input("search for something to update in the database:\n")

    if string == "":
        print("you didn't search anything...")
        return
    
    clear()
    print("checking database...")
    time.sleep(1)

    f = open("database.txt", "r")
    data = f.readlines()
    f.close()

    f = open("database.txt", "r")
    for idx, x in enumerate(f):
        if string == x.strip():
            print(f"\nmatch found!\non line {idx}: {x.strip()}")

            option = input("\nregister something new:\n")
            print("\nupdating...")
            time.sleep(1)
            
            data[idx] = f"{option}\n"
            f.close()
            
            f = open("database.txt", "w")
            f.writelines(data)
            print("successful!")
            f.close()
            return
    
    f.close()
    print("no results found...")



try:
    clear()
    print("checking for database...\n")
    time.sleep(1)

    try:
        f = open("database.txt", "x")
        print("database created!")
    except FileExistsError:
        print("database exists!")
    time.sleep(1)
    clear()



    while True:
        option = input("""select an operation:
        
        1- add value
        2- search value
        3- update value
        4- delete value
        5- exit
        
        > """)
        print("")

        match option.strip():
            case "1":
                clear()
                WriteToDatabase()
                time.sleep(1)
                print("\npress enter to go back")
                input()
                clear()

            case "2":
                clear()
                SearchDatabase()
                time.sleep(1)
                print("\npress enter to go back")
                input()
                clear()

            case "3":
                clear()
                UpdateDatabase()
                time.sleep(1)
                print("\npress enter to go back")
                input()
                clear()

            case "4":
                clear()
                DeleteInDatabase()
                time.sleep(1)
                print("\npress enter to go back")
                input()
                clear()

            case "5":
                exit(False)

            case _:
                print("not a valid option!")
                time.sleep(1)
                clear()



except KeyboardInterrupt:
    exit(True)