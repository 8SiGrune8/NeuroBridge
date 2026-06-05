from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
import time
import numpy as np

def main():
    BoardShim.enable_dev_board_logger()

    params = BrainFlowInputParams()
    board_id = BoardIds.SYNTHETIC_BOARD.value

    board = BoardShim(board_id, params)

    board.prepare_session()
    board.start_stream()

    print("🧠 Live EEG stream started (Ctrl+C to stop)\n")

    try:
        while True:
            time.sleep(1)

            data = board.get_board_data()

            eeg_channels = BoardShim.get_eeg_channels(board_id)

            if len(eeg_channels) >= 2:
                alpha = np.mean(data[eeg_channels[0]])
                beta = np.mean(data[eeg_channels[1]])

                mind_state = alpha / (alpha + beta + 1e-6)

                print(f"🧠 MindState: {mind_state:.5f}")

            else:
                print("⚠️ Not enough EEG channels")

    except KeyboardInterrupt:
        print("\n⛔ Stopping stream...")

    finally:
        board.stop_stream()
        board.release_session()
        print("✅ Session closed cleanly")

if __name__ == "__main__":
    main()