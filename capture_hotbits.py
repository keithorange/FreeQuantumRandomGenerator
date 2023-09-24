import argparse
import time
from hotbit_storage import HotBitStorage
from pixel_processor import PixelProcessor


from webcam_capture import WebcamCapture, WebcamError


def get_user_input():
    """
    Get user input from the command line.
    """
    parser = argparse.ArgumentParser(
        description='HotBits Generator from Webcam.')
    parser.add_argument('--interval', type=float, default=0.0001,
                        help='Interval between frame captures in seconds.')
    parser.add_argument('--storage', type=str, default='hotbits_storage',
                        help='Directory to store generated HotBits.')
    parser.add_argument('--verbose', action='store_true',
                        help='Enable verbose output.')
    parser.add_argument('--max_sets', type=int, default=1000,
                        help='Maximum number of sets (files) of hotbits will be generated. Can be run in background.')
    return parser.parse_args()


def main():
    """
    Main application logic to capture frames, process pixels, and store HotBits.
    """
    # Parse user input
    args = get_user_input()

    if args.verbose:
        print("Initializing HotBits generation...")

    # Initialize webcam, pixel processor, and storage with user-specified parameters
    webcam = WebcamCapture(verbose=args.verbose)
    webcam.initialize_capture()

    processor = PixelProcessor(verbose=args.verbose)
    storage = HotBitStorage(
        storage_directory=args.storage, verbose=args.verbose)

    # Capture the initial frame
    try:
        last_frame = webcam.capture_frame()
        if args.verbose:
            print("Successfully captured the initial frame.")
    except WebcamError as e:
        print(f"Error accessing webcam: {e}")
        return

    if args.verbose:
        print("Starting the HotBits generation loop...")

    while True:
        try:
            while storage.count_sets() >= args.max_sets:
                if args.verbose:
                    print(
                        f"Reached maximum cap of {args.max_sets}. Waiting for sets to be consumed...")
                time.sleep(10)  # Check every 10 seconds

            # Capture the current frame
            current_frame = webcam.capture_frame()

            if args.verbose:
                print(f"current_frame: {current_frame}")

            # Process pixels to generate bits
            processor.process_pixels(current_frame)

            if args.verbose:
                print(f"processed_frame: {processor.last_frame}")

            # If enough bits have been generated, convert to integers and save
            if len(processor.bits) >= 24 * 100:
                hotbits = processor.get_hotbits()
                storage.save_to_file(hotbits)
                if args.verbose:
                    print(
                        f"Stored {24 * 100} bits as a set of hotbits. Total bits processed: {processor.total_bits_processed}. Total stored sets: {storage.count_sets()}")

            # The current frame becomes the last frame for the next iteration
            last_frame = current_frame

            # Sleep for the user-specified interval before capturing the next frame
            time.sleep(args.interval)

        except WebcamError as e:
            print(f"Error accessing webcam: {e}")
            break
        except Exception as e:
            print(f"Unexpected error occurred: {e}")
            break

    if args.verbose:
        print("Exiting program.")


if __name__ == "__main__":
    main()
