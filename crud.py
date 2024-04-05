import sys
import time
import os



def clear() -> None:
    print('\x1B[2J\x1B[H', end='')

def exit() -> None:
    clear()
    print("exiting...")
    time.sleep(1)
    clear()
    sys.exit()

def get_input(text) -> str:
    user_input = input(text)
    if user_input.strip() == "":
        print("you didn't write anything...")
        return ""
    return user_input



class DatabaseManager:

    def __init__(self) -> None:
        clear()
        print("checking for database...\n")
        time.sleep(1)

        try:
            database = open("database.txt", "x")
            print("database created!")
            database.close()
        except FileExistsError:
            print("database exists!")
            
        time.sleep(1)
        clear()
        self.open_database()

    def __del__(self) -> None:
        self.close_database()
        
        
        
    def open_database(self) -> None:
        self.database = open("database.txt", "a+t", buffering=1, encoding="utf-8")
        
    def close_database(self) -> None:
        self.database.close()
        
    def refresh_database(self) -> None:
        self.database.flush()
        os.fsync(self.database)



    def internal_get_value(self, value_to_search, indexes_to_skip) -> list[str, int]:
        clear()
        print("checking database...")
        time.sleep(1)

        self.database.seek(0)
        for index, line in enumerate(self.database):
            if (value_to_search.strip() in line.strip()) and (index not in indexes_to_skip):
                print(f"\nentry found!\non line {index + 1}: {line.strip()}")
                return [line, index]
        print("no entries found...")
        return [None, None]



    def create_value(self) -> None:
        input_value = get_input("add something to the database:\n> ")
        if input_value == "":
            return
        
        search_result = self.internal_get_value(input_value, [None])
        if search_result[1] != None:
            option = input("\nregister a duplicate anyway? y/n\n> ")
            if option.strip() != "y":
                print("\noperation has been canceled" if option.strip() == "n" else "\ninvalid option! finishing registration...")
                return
        
        print("\nregistering to database...")
        time.sleep(1)
        self.database.write(f"{input_value}\n")
        print("all registered!")



    def search_value(self) -> None:
        input_value = get_input("search for something in the database:\n> ")
        if input_value == "":
            return
        
        indexes_to_skip: list[int] = []
        while True:
            search_result = self.internal_get_value(input_value, indexes_to_skip)
            if search_result[1] != None:
                option = input("\ncontinue searching? y/n\n> ")
                if option.strip() != "y":
                    print("\nsearch done!" if option.strip() == "n" else "\ninvalid option! finishing search...")
                    break
                else:
                    indexes_to_skip.append(search_result[1])
            else:
                break



    def delete_value(self) -> None:
        input_value = get_input("search for something to delete in the database:\n> ")
        if input_value == "":
            return

        search_result = self.internal_get_value(input_value, [])
        if search_result[1] != None:
            option = input("\ndelete it? y/n\n> ")
            if option.strip() != "y":
                print("\noperation has been canceled" if option.strip() == "n" else "\ninvalid option! finishing operation...")
            else:
                print("\ndeleting...")
                time.sleep(1)

                self.database.seek(0)
                new_database = self.database.readlines()
                del new_database[search_result[1]]

                self.database.truncate(0)
                self.database.writelines(new_database)
                print("successful!")



    def update_value(self) -> None:
        input_value = get_input("search for something to update in the database:\n> ")
        if input_value == "":
            return

        search_result = self.internal_get_value(input_value, [])
        if search_result[1] != None:
            option = input("\nregister something new:\n> ")
            print("\nupdating...")
            time.sleep(1)
            
            self.database.seek(0)
            new_database = self.database.readlines()
            new_database[search_result[1]] = f"{option}\n"

            self.database.truncate(0)
            self.database.writelines(new_database)
            print("successful!")
    



try:
    db = DatabaseManager()
    while True:
        option = input("""select an operation:
        
1- add value
2- search value
3- update value
4- delete value
5- exit

> """)

        clear()
        match option.strip():
            case "1": db.create_value()
            case "2": db.search_value()
            case "3": db.update_value()
            case "4": db.delete_value()
            case "5": exit()
            case _: print("not a valid option!")
        
        db.refresh_database()
        time.sleep(1)
        print("\npress enter to go back")
        input()
        clear()

except KeyboardInterrupt:
    exit()
