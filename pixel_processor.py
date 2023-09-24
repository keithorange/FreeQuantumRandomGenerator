import numpy as np
import random as python_random
from matplotlib import pyplot as plt


class PixelProcessor:
    """
    This class processes webcam frames to generate random bits.
    """

    def __init__(self, verbose=False, sampling_ratio=0.2):
        """
        Constructor to initialize pixel processing properties.
        :param verbose: Control print statements for debugging.
        :param sampling_ratio: Fraction of pixels to sample from each frame.
        """
        self.bits = ""  # Holds the generated bits
        self.total_bits_processed = 0  # Count of total bits processed
        self.verbose = verbose  # Control print statements
        self.last_frame = None  # Holds the last processed frame
        self.sampling_ratio = sampling_ratio  # Fraction of pixels to sample

    def process_pixels(self, current_frame):
        """
        Process pixels from a frame to generate random bits.
        :param current_frame: A frame from the webcam.
        """
        if self.last_frame is None:
            self.last_frame = current_frame
            return

        if current_frame.shape != self.last_frame.shape:
            raise ValueError(
                "Frames have different shapes. Ensure consistent frame captures.")

        rows, cols, channels = current_frame.shape
        num_samples = int(rows * cols * self.sampling_ratio)

        # Randomly sample pixels across the frame
        sample_pixels = python_random.sample(
            [(i, j) for i in range(rows) for j in range(cols)], num_samples)

        for (i, j) in sample_pixels:
            for c in range(channels):  # Iterate over RGB channels
                # Extract the least significant bit
                bit = current_frame[i, j, c] & 1
                self.bits += str(bit)

        self.total_bits_processed += num_samples * channels
        self.last_frame = np.copy(current_frame)  # Update the last frame

    def get_hotbits(self, chunk_size=24):
        """
        Convert the generated bits to integers.
        :param chunk_size: Number of bits per integer.
        :return: List of generated integers.
        """
        integers = []
        while len(self.bits) >= chunk_size:
            chunk = self.bits[:chunk_size]
            integer = int(chunk, 2)
            if integer != 0:
                integers.append(integer)
            self.bits = self.bits[chunk_size:]

        if self.verbose:
            print(f"Converted {len(integers)} integers from bits.")

        return integers
