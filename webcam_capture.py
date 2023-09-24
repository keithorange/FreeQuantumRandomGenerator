# Importing necessary libraries

# OpenCV for webcam capture and image processing
import cv2
# Efficient array operations
import numpy as np
# For file I/O operations
import json
# For obtaining detailed traceback during exceptions
import traceback
# For introducing delays and timing operations
import time


class WebcamError(Exception):
    """
    Custom exception to handle webcam specific errors.
    """

    def __init__(self, message="Webcam error occurred"):
        """
        Constructor for the WebcamError exception.

        :param message: The error message to be displayed.
        """
        # Extract the current traceback and append it to the error message
        current_traceback = "".join(
            traceback.format_list(traceback.extract_stack()))
        self.message = message + "\n" + current_traceback
        super().__init__(self.message)


class WebcamCapture:
    """
    This class captures video frames from the webcam and provides utilities for processing.
    """

    def __init__(self, verbose=False):
        """
        Constructor to initialize webcam capture properties.

        :param verbose: If set to True, the class will print out additional debug information.
        """
        # Placeholder for the webcam capture object
        self.capture = None
        # Placeholder for the last captured frame
        self.last_frame = None
        self.verbose = verbose

    def initialize_capture(self, cam_index=0):
        """
        Set up the webcam for capturing.

        :param cam_index: Index of the camera to use. Default is 0 (the default webcam).
        """
        # List all available camera devices
        available_cams = []
        for i in range(10):  # checking the first 10 indexes
            cap = cv2.VideoCapture(i)
            if cap.read()[0]:
                available_cams.append(i)
                cap.release()

        if self.verbose:
            print(f"Available cameras at indexes: {available_cams}")

        # cam_index denotes the selected webcam
        self.capture = cv2.VideoCapture(cam_index)
        # Introduce a delay of 1 second to allow the camera to warm up
        time.sleep(1)

        # Display detailed information about the camera being used
        width = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fps = self.capture.get(cv2.CAP_PROP_FPS)

        if self.verbose:
            print(
                f"Initialized webcam at index {cam_index} with resolution {width}x{height} and {fps} FPS")

        # Check if the webcam is opened successfully
        if not self.capture.isOpened():
            raise WebcamError(
                f"Error initializing webcam at index {cam_index}. Please ensure a webcam is connected and accessible.")

    def capture_frame(self):
        """
        Capture a single frame from the webcam and return it.
        """
        ret, frame = self.capture.read()  # Read a frame
        if not ret:
            # Display possible reasons for failure to capture a frame
            backend_name = self.capture.getBackendName()
            backend_version = self.capture.get(cv2.CAP_PROP_BACKEND_VERSION)
            print(f"Used backend: {backend_name} v{backend_version}")
            raise WebcamError(
                "Error capturing frame. Possible reasons include:\n"
                "1. Webcam is being used by another application.\n"
                "2. Webcam was unplugged.\n"
                "3. Hardware or driver malfunction.\n"
                "Please ensure the webcam is functioning properly.")

        return frame  # Return the original RGB frame

    def release_capture(self):
        """
        Properly release the webcam resources.
        """
        if self.capture:
            self.capture.release()
            cv2.destroyAllWindows()  # Close any OpenCV windows
