from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from pythonosc.udp_client import SimpleUDPClient

import time
import numpy as np

def main():
    BoardShim.enable_dev_board_logger()

    OSC_IP = "127.0.0.1"
    OSC_PORT = 7001

    client = SimpleUDPClient(OSC_IP, OSC_PORT)

    params = BrainFlowInputParams()
    board_id = BoardIds.SYNTHETIC_BOARD.value

    board = BoardShim(board_id, params)

    board.prepare_session()
    board.start_stream()

    print("🧠 Streaming to UE5 via OSC (Ctrl+C to stop)\n")

    try:
        while True:
            time.sleep(1)

            data = board.get_board_data()
            eeg_channels = BoardShim.get_eeg_channels(board_id)

            if len(eeg_channels) >= 2:

                alpha = np.mean(data[eeg_channels[0]])
                beta = np.mean(data[eeg_channels[1]])

                mind_state = float(
                    alpha / (alpha + beta + 1e-6)
                )

                client.send_message(
                    "/neuro/mindstate",
                    mind_state
                )

                print(
                    f"🧠 MindState: {mind_state:.5f}"
                )

    except KeyboardInterrupt:
        print("\n⛔ Stopping...")

    finally:
        board.stop_stream()
        board.release_session()
        print("✅ Clean exit")

if __name__ == "__main__":
    main()