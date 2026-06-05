from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
import time
import numpy as np
import socket
import json

def main():
    BoardShim.enable_dev_board_logger()

    # UDP НАСТРОЙКА
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5005
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    params = BrainFlowInputParams()
    board_id = BoardIds.SYNTHETIC_BOARD.value

    board = BoardShim(board_id, params)

    board.prepare_session()
    board.start_stream()

    print("🧠 Streaming to UE5 via UDP (Ctrl+C to stop)\n")

    try:
        while True:
            time.sleep(1)

            data = board.get_board_data()
            eeg_channels = BoardShim.get_eeg_channels(board_id)

            if len(eeg_channels) >= 2:
                alpha = np.mean(data[eeg_channels[0]])
                beta = np.mean(data[eeg_channels[1]])

                mind_state = float(alpha / (alpha + beta + 1e-6))

                msg = {
                    "mind_state": mind_state
                }

                sock.sendto(json.dumps(msg).encode(), (UDP_IP, UDP_PORT))

                print(f"🧠 MindState: {mind_state:.5f}")

    except KeyboardInterrupt:
        print("\n⛔ Stopping...")

    finally:
        board.stop_stream()
        board.release_session()
        sock.close()
        print("✅ Clean exit")

if __name__ == "__main__":
    main()