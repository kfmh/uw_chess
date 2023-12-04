import time
import requests

class Loading_status:
    def __init__(self):
        self.timeout = 300  # timeout in seconds
        self.check_interval = 10  # time to wait between checks in seconds
        self.start_time = time.time()

    def is_model_ready(self):
        # Replace with actual API call or status check
        response1 = requests.get("https://api-inference.huggingface.co/models/openai/whisper-large-v2")
        response2 = requests.get("https://api-inference.huggingface.co/models/facebook/fastspeech2-en-ljspeech")
        print(response1)
        print(response2)
        if response1.status_code == 200 and response2.status_code == 200:
            return True
        return False

    def status_check(self):
        while True:
            if self.is_model_ready():
                print("Model is ready!")
                break
            elif time.time() - self.start_time > self.timeout:
                print("Timeout reached, model is still not ready.")
                break
            else:
                print("Model is still loading... waiting.")
                time.sleep(self.check_interval)
