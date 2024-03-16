import os  # Import module for interacting with the operating system
import time  # Import module for working with time
from datetime import datetime  # Import datetime class for working with dates and times
from smartcard.System import readers  # Import module for working with NFC readers
from smartcard.util import toHexString  # Import function for converting data to hexadecimal format
from smartcard.Exceptions import NoCardException, CardConnectionException  # Import exceptions for NFC cards

UID_FILE_PREFIX = "scanned_uid_"  # Prefix for UID file names

def get_uid(connection):
    GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]  # Command to get UID from card
    data, sw1, sw2 = connection.transmit(GET_UID)  # Send command and get response
    if sw1 == 144:  # Check if response is successful
        return toHexString(data).replace(" ", "") + '000000000000'  # Return UID in hexadecimal format
    return None  # If getting UID fails, return None

def check_uid_in_file(uid, file_path):
    with open(file_path, 'a+') as file:  # Open file for reading and writing
        file.seek(0)  # Move cursor to the beginning of the file
        return uid in file.read()  # Check if UID is present in the file

def create_uid_file(today_date):
    return f"{UID_FILE_PREFIX}{today_date}.txt"  # Create file name based on current date

def main():
    uid_count = 0  # UID counter
    r = readers()  # Initialize NFC readers
    if not r:  # Check if readers are found
        print("NFC readers not found.")  # Print message about absence of readers
        print("Program finished. Goodbye.")  # Print message about program completion
        time.sleep(3)  # Delay before exiting the program
        return

    print("Connected readers:", r)  # Print information about connected readers
    print("Number of scanned UID's:", uid_count)  # Print initial value of UID counter
    print("Place a card to get UID...")  # Prompt the user to place a card for scanning
    
    card_present = False  # Variable to track card presence
    today_date = datetime.now().strftime("%d%m%Y")  # Get current date
    uid_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), create_uid_file(today_date))  # Form path to UID file

    try:
        while True:
            for reader in r:  # Iterate through each reader
                with reader.createConnection() as connection:  # Establish connection with each reader
                    try:
                        connection.connect()  # Connect to the card
                        uid = get_uid(connection)  # Get UID from the card
                        if uid:  # If UID is obtained
                            if not card_present:  # If the card is detected for the first time
                                if check_uid_in_file(uid, uid_file_path):  # Check if this UID is already recorded in the file
                                    print("\033[2J\033[H")  # Clear the screen
                                    print("Number of scanned UID's:", uid_count)  # Print current number of scanned UID's
                                    print("This UID is already recorded")  # Notify that UID has already been recorded earlier                                
                                else:
                                    uid_count += 1  # Increment UID counter
                                    print("\033[2J\033[H")  # Clear the screen
                                    print("Number of scanned UID's:", uid_count)  # Print current number of scanned UID's
                                    with open(uid_file_path, 'a') as file:  # Open file for appending
                                        file.write(uid + '\n')  # Write UID to the file
                                    print("UID:", uid)  # Print obtained UID
                                card_present = True  # Set flag indicating card is present
                    except NoCardException:  # Handle exception when card is not found
                        if card_present:  # If card was present
                            print("Place another card to get UID...")  # Prompt to place another card for scanning
                            card_present = False  # Set flag indicating card is absent
                    except CardConnectionException as e:  # Handle exception when connection error with card occurs
                        print("Card connection error:", e)  # Print message about connection error
                        print("\033[2J\033[H")  # Clear the screen
                        print("Number of scanned UID's:", uid_count)  # Print current number of scanned UID's
                        print("UID:", uid)  # Print obtained UID
                        print("Place another card to get UID...")  # Prompt to place another card for scanning
                        card_present = False  # Set flag indicating card is absent
    except KeyboardInterrupt:  # Handle exception when user presses Ctrl+C
        print("\033[2J\033[H")  # Clear the screen
        print("Number of scanned UID's:", uid_count)  # Print number of scanned UID's
        print("The program is finished. Goodbye")  # Print message about program termination
        time.sleep(2)  # Delay before exiting the program

if __name__ == "__main__":
    main()  # Call the main function if the script is run directly
