# Importing necessary libraries

# For file I/O operations
import json
# For OS-level operations such as checking existence of directories and listing files
import os
# For obtaining the current time to timestamp files
import time


class HotBitStorage:
    """
    This class handles the storage and management of HotBits.
    HotBits are random data, and this class offers methods to save them to disk 
    and count how many sets of them have been stored.
    """

    def __init__(self, storage_directory="hotbits_storage", verbose=False):
        """
        Constructor to initialize storage properties.

        :param storage_directory: The directory where HotBits will be stored.
                                  Default is a directory named "hotbits_storage".
        :param verbose: If set to True, the class will print out additional 
                        debug information.
        """
        # Directory where HotBits will be saved
        self.storage_directory = storage_directory
        # Control print statements
        self.verbose = verbose

        # Check if the storage directory exists. If not, create it.
        if not os.path.exists(self.storage_directory):
            os.makedirs(self.storage_directory)

    def save_to_file(self, hotbits):
        """
        Save the generated HotBits to a JSON file.

        :param hotbits: The list of HotBits to be saved.
        """
        # Generate a unique filename using the current timestamp
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(self.storage_directory,
                                f"hotbits_{timestamp}.json")

        # Write the HotBits to the file in JSON format
        with open(filename, 'w') as file:
            json.dump({"integerList": hotbits}, file)

        # If verbose mode is enabled, print the location where HotBits were saved
        if self.verbose:
            print(f"Saved HotBits to: {filename}")

    def count_sets(self):
        """
        Count the number of sets (json files) in the storage directory.

        :return: The number of json files (sets of HotBits) stored.
        """
        # List all .json files in the storage directory and return their count
        return len([name for name in os.listdir(self.storage_directory) if name.endswith('.json')])
