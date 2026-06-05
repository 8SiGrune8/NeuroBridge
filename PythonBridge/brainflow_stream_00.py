from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
import time
import numpy as np

def main():
    # включаем логирование (полезно для отладки)
    BoardShim.enable_dev_board_logger()

    params = BrainFlowInputParams()

    # ВАЖНО: это виртуальная EEG плата (без Muse)
    board_id = BoardIds.SYNTHETIC_BOARD.value

    board = BoardShim(board_id, params)

    board.prepare_session()
    board.start_stream()

    print("🧠 EEG stream started...")

    time.sleep(5)

    # забираем данные
    data = board.get_board_data()

    board.stop_stream()
    board.release_session()

    print("📊 Data shape:", data.shape)

    # покажем первые значения
    print("\nFirst 5 columns:")
    print(data[:, :5])

    # берем EEG каналы
    eeg_channels = BoardShim.get_eeg_channels(board_id)

    if len(eeg_channels) >= 2:
    	alpha = np.mean(data[eeg_channels[0]])
    	beta = np.mean(data[eeg_channels[1]])

    	mind_state = alpha / (alpha + beta + 1e-6)

    	print("\n🧠 MindState:", mind_state)

if __name__ == "__main__":
    main()