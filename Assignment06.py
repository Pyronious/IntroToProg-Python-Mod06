# ------------------------------------------------------------------------------------------ #
# Title: Assignment06
# Desc: This assignment demonstrates using functions, classes, and separations of concern
# Change Log:
#   Patrick Moynihan: 2024-04-10 Created script
#   Patrick Moynihan: 2024-04-08 Added ability to save data to CSV file
#   Patrick Moynihan: 2024-04-25 Added menu functionality
#   Patrick Moynihan: 2024-05-02 Added ability to read data from CSV file
#   Patrick Moynihan: 2024-05-10 Refactored to use dictionaries and JSON file format
#   Patrick Moynihan: 2024-05-18 Refactored to use functions and classes
# ------------------------------------------------------------------------------------------ #
import json
from typing import IO

# Define the Data Constants

MENU: str = '''
------ Course Registration Program ------
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"
KEYS: list = ["FirstName", "LastName", "CourseName"]

# Define the Data Variables
menu_choice: str = ''  # Hold the choice made by the user.
students: list = []  # List of data for all students
saved: bool = True  # Tracks whether newly added data has been saved


# Define the classes

class FileProcessor:
    """
    Functions for reading and writing JSON files.

    ChangeLog:
        Patrick Moynihan, 2024-05-18: Created class
    """

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list) -> None:
        """
        Reads the specified JSON file and stores it in a list.

        ChangeLog:
        Patrick Moynihan, 2024-05-18: Created method

        :param file_name: string representing the name of the JSON file
        :param student_data: list to which student data will be stored
        """
        file: IO  # Holds a reference to an opened file.
        file_data: list  # Holds the file read from the JSON file

        print(f">>> Loading data from {file_name}")
        try:
            file = open(file_name, "r")
            file_data = json.load(file)
            student_data.extend(file_data)  # add the data we just loaded to the passed-in list
            file.close()
            print(f">>> Loaded {len(student_data)} records.")

            for i, item in enumerate(student_data, start=1):
                # Check to see if the keys we are expecting exist in the data
                if not all(key in item for key in KEYS):
                    raise Exception(
                        f">>> Missing an expected key ({KEYS}) in record {i}. Please check {file_name} for errors.")

        # Let the user know we couldn't find the file
        except FileNotFoundError:
            IO.output_error_messages(f">>> {file_name} not found. A new file will be created.")
            file = open(file_name, "w")
            file.close()

        # Let the user know some other problem occurred when loading the file
        except Exception as e:
            IO.output_error_messages(
                f">>> There was an error loading the data from {file_name}. Please check {file_name} and try again.")
            IO.output_error_messages(e, e.__doc__)
            exit()

        # If the file is still open for some reason, close it
        finally:
            if not file.closed:
                print(">>> Closing file.")
                file.close()

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list) -> bool:
        """
                Writes the specified JSON file and stores it in a list.

                ChangeLog:
                Patrick Moynihan, 2024-05-18: Created method

                :param file_name: string representing the name of the JSON file
                :param student_data: list from which student data will be saved
                :return: bool representing whether or not the data was saved
                """
        file: IO = None
        json_data: str = ''  # Holds combined string data separated by a comma.

        try:
            # Save JSON to file
            file = open(file_name, 'w')
            json.dump(student_data, file, indent=4)
            file.close()
            print(f">>> Wrote registration data to filename {file_name}\n")

            # Print JSON data to terminal
            json_data = json.dumps(students, indent=4)
            print(json_data)
            return True

        except Exception as e:
            IO.output_error_messages(">>> There was an error writing the registration data. Is the file read-only?")
            IO.output_error_messages(f">>> {e}", e.__doc__)
        finally:
            # Does file have a value other than None? If so, is the file open? If so, close the file.
            if file and not file.closed:
                file.close()


class IO:
    """
        Functions for handling user input and output.

        ChangeLog:
            Patrick Moynihan, 2024-05-18: Created class
        """

    @staticmethod
    def output_menu(menu: str) -> None:
        """
        Displays the menu options

        ChangeLog:
            Patrick Moynihan, 2024-05-18: Created method

        :param menu: string to be printed as the menu
        """
        print(menu)

    @staticmethod
    def input_menu_choice() -> str:
        """
        Retrieves user input from the menu

        ChangeLog:
            Patrick Moynihan, 2024-05-18: Created method

        :return: string representing the user input
        """
        choice = input("Enter your choice: ")
        return choice

    @staticmethod
    def output_student_courses(student_data: list) -> None:
        """
        Prints out the student registration data in human-readable format.

        ChangeLog:
            Patrick Moynihan, 2024-05-18: Created method

        :param student_data: list from which student data will be presented
        """
        print(">>> The current data is:\n")
        print("First Name          Last Name           Course Name         ")
        print("------------------------------------------------------------")
        for item in student_data:
            # Print each row of the table inside 20 character wide columns
            print(f"{item['FirstName'][:20]:<20}{item['LastName'][:20]:<20}{item['CourseName'][:20]:<20}")
        print("------------------------------------------------------------")

    @staticmethod
    def input_student_data(student_data: list) -> None:
        """
        Reads the student registration data from the user and appends it to a list

        ChangeLog:
                Patrick Moynihan, 2024-05-18: Created method

        :param student_data: list to which student data will be appended
        """
        student_first_name: str = ''  # Holds the first name of a student entered by the user.
        student_last_name: str = ''  # Holds the last name of a student entered by the user.
        course_name: str = ''  # Holds the name of a course entered by the user.

        # Input user data, allow only alpha characters
        while True:
            try:
                student_first_name = input("Enter student's first name: ")
                if not student_first_name.isalpha():
                    raise ValueError(f">>> Please use only letters. Try again.\n")
                else:
                    break
            except ValueError as e:
                IO.output_error_messages(e)

        while True:
            try:
                student_last_name = input("Enter student's last name: ")
                if not student_last_name.isalpha():
                    raise ValueError(">>> Please use only letters. Try again.\n")
                else:
                    break
            except ValueError as e:
                IO.output_error_messages(e)

        course_name = input("Enter the course name: ")

        # Create dictionary using captured data
        data = {"FirstName": student_first_name, "LastName": student_last_name, "CourseName": course_name}

        # Append the entered data to the passed-in list
        student_data.append(data)
        print(f">>> Registered {student_first_name} {student_last_name} for {course_name}.\n")

    @staticmethod
    def output_error_messages(message: str, error: Exception = None) -> None:
        """
        Presents custom error message to user, along with Python's technical error.

        ChangeLog:
                Patrick Moynihan, 2024-05-18: Created method

        :param message: The custom error message to present to the user
        :param error: The technical error message from Python
        """
        # if we get two arguments, print the custom error and the Python technical error
        if error:
            print(f"{message}")
            print(f">>> Python technical error: {error}")
        # otherwise just print the custom error message
        else:
            print(f"{message}")


# Load data from enrollment JSON file into students
FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Main program loop

while True:
    # Present the menu of choices
    IO.output_menu(MENU)
    menu_choice = IO.input_menu_choice()

    if menu_choice == '1':
        # Ingest student registration data from user
        IO.input_student_data(student_data=students)
        saved = False  # Set the saved flag to false, so we can remind user to save
        continue

    elif menu_choice == '2':
        # Display the data in a human-friendly format
        IO.output_student_courses(students)
        continue

    elif menu_choice == '3':
        # Save the data to a file and set saved flag to True if save was successful
        if FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students) == True:
            saved = True
        continue

    elif menu_choice == '4':
        # Exit if data has already been saved or was unmodified (i.e. saved = undefined)
        if saved is False:
            save_confirm = input(">>> New registration data not saved. Save it now? (Y/N): ")
            if save_confirm.capitalize() == 'Y':
                if FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students) == True:
                    print(">>> Have a nice day!\n")
                    exit()
                else:
                    continue # File was not successfully saved, so return to main menu
            elif save_confirm.capitalize() == 'N':
                print(">>> Newly entered data not saved.")
                print(">>> Have a nice day!\n")
                exit()
        else:
            print(">>> Have a nice day!\n")
            exit()

    else:
        print("Please only choose option 1, 2, 3, or 4.")
