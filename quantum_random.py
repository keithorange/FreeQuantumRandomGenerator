# Importing necessary libraries
import json
import os
# Standard Python random library for certain operations
import random as python_random


class QuantumRandom:
    """
    This class mimics the Python random library but uses quantum-generated bits.
    It provides methods that are analogous to the standard Python random library,
    but the source of randomness is from pre-generated quantum random bits
    stored in JSON files.
    """

    def __init__(self, storage_directory="hotbits_storage"):
        """
        Constructor to initialize quantum random properties.

        :param storage_directory: Directory where HotBits (quantum random bits) are stored.
        """
        self.storage_directory = storage_directory
        self.current_bits = ""  # Holds the current quantum bits as a string
        self.load_next_file()  # Load the first file on instantiation

    def load_next_file(self):
        """
        Load the next available HotBits file from the specified directory.
        If no files are available, an error is raised.
        """
        # List all JSON files in the directory
        files = [f for f in os.listdir(
            self.storage_directory) if f.endswith('.json')]
        if not files:
            raise ValueError(
                "No HotBits available. Generate more quantum random bits.")

        # Randomly choose one of the available files
        self.current_file = os.path.join(
            self.storage_directory, python_random.choice(files))
        # Load the chosen file and append its bits to `current_bits`
        with open(self.current_file, 'r') as file:
            integers = json.load(file)["integerList"]
            for integer in integers:
                self.current_bits += format(integer, '024b')

        # Remove the loaded file to avoid using the same randomness again
        os.remove(self.current_file)
        # Logging statement
        print(
            f"Loaded file: {self.current_file}, Current bits length: {len(self.current_bits)}")

    # The following methods mimic the Python random library using quantum-generated bits:

    def getrandbits(self, k):
        """
        Returns a number representing the random bits.

        :param k: The number of random bits required.
        :return: Integer representation of the k random bits.
        """
        # Ensure there are enough bits available
        while len(self.current_bits) < k:
            self.load_next_file()

        # Extract the required k bits and update the remaining bits
        result_bits = self.current_bits[:k]
        self.current_bits = self.current_bits[k:]
        return int(result_bits, 2)

    def randrange(self, start, stop=None, step=1):
        """
        Returns a random number between the given range.

        :param start: Start of the range.
        :param stop: End of the range.
        :param step: Step size between numbers in the range.
        :return: Random number from the specified range.
        """
        if stop is None:
            start, stop = 0, start

        # Total numbers in the range
        range_size = (stop - start) // step

        while True:
            # Generate a random number up to the closest power of 2
            rand_num = self.getrandbits((range_size - 1).bit_length())
            if rand_num < range_size:
                return start + rand_num * step

    def randint(self, a, b):
        """
        Returns a random number between the given range, inclusive.

        :param a: Start of the range.
        :param b: End of the range.
        :return: Random integer between a and b, inclusive.
        """
        range_size = b - a + 1
        max_power_of_two = 2 ** (range_size.bit_length() - 1)

        while True:
            # Generate a random number in the power-of-two range
            rand_num = self.getrandbits(max_power_of_two.bit_length())
            if a <= rand_num <= b:
                return rand_num

    def choice(self, seq):
        """
        Returns a random element from the given sequence.

        :param seq: A sequence (list, tuple, etc.).
        :return: A random element from the sequence.
        """
        return seq[self.randint(0, len(seq) - 1)]

    def choices(self, seq, k=1):
        """
        Returns a list with a random selection from the given sequence.

        :param seq: A sequence (list, tuple, etc.).
        :param k: Number of elements to select.
        :return: A list of k random elements from the sequence.
        """
        return [self.choice(seq) for _ in range(k)]

    def shuffle(self, seq):
        """
        Shuffles the sequence in-place using quantum randomness.

        :param seq: A sequence (typically a list) to shuffle.
        """
        for i in reversed(range(1, len(seq))):
            j = self.randint(0, i)
            seq[i], seq[j] = seq[j], seq[i]

    def sample(self, seq, k):
        """
        Returns a k length list of unique elements chosen from the sequence.

        :param seq: A sequence (list, tuple, etc.).
        :param k: Number of unique elements to select.
        :return: A list of k unique elements from the sequence.
        """
        return [seq[i] for i in sorted(self.choices(range(len(seq)), k))]

    def random(self):
        """
        Returns a random float number between 0 and 1.

        :return: Random float between 0 and 1.
        """
        return self.getrandbits(53) / 9007199254740992  # 2**53

    def uniform(self, a, b):
        """
        Returns a random float number between two given parameters.

        :param a: Start of the range.
        :param b: End of the range.
        :return: Random float between a and b.
        """
        return a + (b - a) * self.random()
