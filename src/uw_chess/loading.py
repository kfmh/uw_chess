# ============================================================================
# loading.py
# In case of using models via api-inference like huggingFace transformers 
# game start after api is tested
# ============================================================================

import time
import requests

class Loading_status:
    """
    A class to check the loading status of a model hosted on an API.

    Attributes:
        timeout (int): Maximum time to wait for the model to be ready in seconds.
        check_interval (int): Time interval between successive status checks in seconds.
        start_time (float): Time when the status check was initiated.
    """

    def __init__(self):
        """
        Initializes the Loading_status class with default values for timeout and check interval.
        """
        self.timeout = 300  # Timeout set to 300 seconds (5 minutes)
        self.check_interval = 10  # Interval between status checks set to 10 seconds
        self.start_time = time.time()  # Record the start time of the process

    def is_model_ready(self):
        """
        Checks if the model is ready by making a request to the model's API.

        Returns:
            bool: True if the model is ready, False otherwise.
        """
        # Replace the URL with the actual API endpoint for your model
        response = requests.get("https://api-inference.huggingface.co/models/facebook/fastspeech2-en-ljspeech")

        if response.status_code == 200:
            return True  # Model is ready
        return False  # Model is not ready

    def status_check(self):
        """
        Continuously checks the model's status at regular intervals until it's ready or a timeout is reached.
        """
        while True:
            if self.is_model_ready():
                print("Model is ready!")
                break  # Exit loop if model is ready
            elif time.time() - self.start_time > self.timeout:
                print("Timeout reached, model is still not ready.")
                break  # Exit loop if timeout is reached
            else:
                print("Model is still loading... waiting.")
                time.sleep(self.check_interval)  # Wait for the defined check interval before checking again
