import sys
import time
import os


class ConsoleManager:
    def clear(self) -> None:
        print("\x1B[2J\x1B[H", end="") # doesnt erase console history

    def exit(self) -> None:
        self.clear()
        print("exiting...")
        time.sleep(1)
        self.clear()
        sys.exit()

    def get_input(self, text) -> str:
        user_input = input(text)
        if user_input.strip() == "":
            print("you didn't write anything...")
            return ""
        return user_input



class DatabaseManager:
    def __del__(self) -> None:
        self._close_database()
    
    console = ConsoleManager()



    def _check_database(self, file) -> None:
        print() # specific line spacing
        if file.strip() == "":
            print("no input given, defaulting to \"database.txt\"")
            self.filename = "database.txt"
        else:
            self.filename = file

        print("checking...")
        time.sleep(1)

        try:
            database = open(self.filename, "x")
            print("database created!")
            database.close()
        except FileExistsError:
            print("database exists!")

    def _switch_database(self) -> None:
        self.console.clear()
        self._check_database(input("enter a new database name\n> "))


        
    def _open_database(self) -> None:
        self.database = open(self.filename, "a+t", buffering=1, encoding="utf-8")
        
    def _close_database(self) -> None:
        try:
            self.database.close()
        except AttributeError:
            pass
        
    def _refresh_database(self) -> None:
        self.database.flush()
        os.fsync(self.database)
        
    

    def initiate_database(self, file) -> None: # split from _check_database() so switching databases can be visually smoother
        self._check_database(file)
        time.sleep(1)
        self._open_database()
        self._open_menu()
        
    def _open_menu(self) -> None:
        while True:
            self.console.clear()
            choice = input(f"""currently accessing database "{self.filename}"
                        
select an operation:
            
1- add value
2- search value
3- update value
4- delete value
5- switch database
6- exit

> """)
            self.console.clear()
            match choice.strip():
                case "1": self._create_value()
                case "2": self._search_value()
                case "3": self._update_value()
                case "4": self._delete_value()
                case "5": self._switch_database()
                case "6":
                    self._close_database()
                    return
                case _: print("\nnot a valid option!")
            
            self._refresh_database()
            time.sleep(1)
            input("\npress enter to go back")
            self.console.clear()



    def _internal_get_value(self, value_to_search, indexes_to_skip) -> list[str, int]: # type: ignore
        print("checking database...")
        time.sleep(1)

        self.database.seek(0)
        for index, line in enumerate(self.database):
            if (value_to_search.strip() in line.strip()) and (index not in indexes_to_skip):
                print(f"\nentry found!\non line {index + 1}: {line.strip()}")
                return [line, index]
        print("no entries found...")
        return [None, None]



    def _create_value(self) -> None:
        input_value = self.console.get_input("add something to the database:\n> ")
        if input_value == "":
            return
        
        search_result = self._internal_get_value(input_value, [None])
        if search_result[1] != None:
            option = input("\nregister a duplicate anyway? y/n\n> ")
            if option.strip().lower() != "y":
                print("\noperation has been canceled" if option.strip().lower() == "n" else "\ninvalid option! finishing registration...")
                return
        
        print("\nregistering to database...")
        time.sleep(1)
        self.database.write(f"{input_value}\n")
        print("all registered!") # read like Elizabeth from Persona 3



    def _search_value(self) -> None:
        input_value = self.console.get_input("search for something in the database:\n> ")
        if input_value == "":
            return
        
        indexes_to_skip: list[int] = []
        while True:
            search_result = self._internal_get_value(input_value, indexes_to_skip)

            if search_result[1] == None:
                break
            
            option = input("\ncontinue searching? y/n\n> ")
            if option.strip().lower() != "y":
                print("\nsearch done!" if option.strip().lower() == "n" else "\ninvalid option! finishing search...")
                break
            else:
                self.console.clear()
                indexes_to_skip.append(search_result[1])



    def _update_value(self) -> None:
        input_value = self.console.get_input("search for something to update in the database:\n> ")
        if input_value == "":
            return

        search_result = self._internal_get_value(input_value, [])
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



    def _delete_value(self) -> None:
        input_value = self.console.get_input("search for something to delete in the database:\n> ")
        if input_value == "":
            return

        search_result = self._internal_get_value(input_value, [])
        if search_result[1] != None:
            option = input("\ndelete it? y/n\n> ")
            if option.strip().lower() != "y":
                print("\noperation has been canceled" if option.strip().lower() == "n" else "\ninvalid option! finishing operation...")

            else:
                print("\ndeleting...")
                time.sleep(1)

                self.database.seek(0)
                new_database = self.database.readlines()
                del new_database[search_result[1]]

                self.database.truncate(0)
                self.database.writelines(new_database)
                print("successful!")

    

db = DatabaseManager()
console = ConsoleManager()

while True:
    try:
        console.clear()
        match input("no database manager is open, access one? y/n\n> ").lower():
            case "y":
                console.clear()
                db.initiate_database(input("enter a database name\n> "))
            case "n":
                exit()
            case _:
                input("\ninvalid option! press enter to try again")
    except KeyboardInterrupt:
        console.exit()