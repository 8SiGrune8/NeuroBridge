from pythonosc.udp_client import SimpleUDPClient
import time

client = SimpleUDPClient("127.0.0.1", 7001)

value = 0.0
direction = 1

try:
    while True:
        client.send_message("/neuro/mindstate", value)

        print(f"Sent MindState: {value:.2f}")

        value += 0.1 * direction

        if value >= 1.0:
            value = 1.0
            direction = -1

        if value <= 0.0:
            value = 0.0
            direction = 1

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nSender stopped.")
    print("=== NeuroBridge OSC Test Sender ===")
    print("Sending /neuro/mindstate to 127.0.0.1:7001")
    print("Press Ctrl+C to stop.\n")