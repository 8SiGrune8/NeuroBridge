from dataclasses import dataclass

import time
import numpy as np

from brainflow.board_shim import (
    BoardShim,
    BrainFlowInputParams,
    BoardIds,
)

from pythonosc.udp_client import SimpleUDPClient


# ==========================================================
# NeuroBridge Brain State
# ==========================================================

@dataclass
class BrainState:

    attention: float
    relaxation: float

    alpha: float
    beta: float
    theta: float
    delta: float
    gamma: float

    global_activity: float

    timestamp: float = 0.0


# ==========================================================
# Brain Bridge
# ==========================================================

class BrainBridge:

    OSC_IP = "127.0.0.1"
    OSC_PORT = 7001

    # ------------------------------------------------------

    def __init__(self):

        BoardShim.enable_dev_board_logger()

        self.client = SimpleUDPClient(
            self.OSC_IP,
            self.OSC_PORT
        )

        params = BrainFlowInputParams()

        self.board_id = BoardIds.SYNTHETIC_BOARD.value

        self.board = BoardShim(
            self.board_id,
            params
        )

    # ------------------------------------------------------

    def start(self):

        self.board.prepare_session()
        self.board.start_stream()

        print("===========================================")
        print(" NeuroBridge Brain Bridge")
        print("===========================================")
        print(f"OSC : {self.OSC_IP}:{self.OSC_PORT}")
        print("Board : Synthetic Board")
        print()

    # ------------------------------------------------------

    def stop(self):

        self.board.stop_stream()
        self.board.release_session()

        print("\nBrain Bridge stopped.")

    # ------------------------------------------------------
    # Compute Brain State
    # ------------------------------------------------------

    def compute_brain_state(self, data) -> BrainState:

        eeg_channels = BoardShim.get_eeg_channels(
            self.board_id
        )

        alpha = float(
            np.mean(np.abs(data[eeg_channels[0]]))
        )

        beta = float(
            np.mean(np.abs(data[eeg_channels[1]]))
        )

        theta = float(
            np.mean(np.abs(data[eeg_channels[2]]))
        ) if len(eeg_channels) > 2 else 0.0

        delta = float(
            np.mean(np.abs(data[eeg_channels[3]]))
        ) if len(eeg_channels) > 3 else 0.0

        gamma = float(
            np.mean(np.abs(data[eeg_channels[4]]))
        ) if len(eeg_channels) > 4 else 0.0

        attention = beta / (alpha + beta + 1e-6)

        relaxation = alpha / (alpha + beta + 1e-6)

        global_activity = (
            alpha +
            beta +
            theta +
            delta +
            gamma
        ) / 5.0

        return BrainState(

            attention=attention,
            relaxation=relaxation,

            alpha=alpha,
            beta=beta,
            theta=theta,
            delta=delta,
            gamma=gamma,

            global_activity=global_activity,

            timestamp=time.time()

        )

    # ------------------------------------------------------
    # Send Brain State
    # ------------------------------------------------------

    def send_brain_state(self, state: BrainState):

        self.client.send_message(
            "/neurobridge/attention",
            state.attention
        )

        self.client.send_message(
            "/neurobridge/relaxation",
            state.relaxation
        )

        self.client.send_message(
            "/neurobridge/alpha",
            state.alpha
        )

        self.client.send_message(
            "/neurobridge/beta",
            state.beta
        )

        self.client.send_message(
            "/neurobridge/theta",
            state.theta
        )

        self.client.send_message(
            "/neurobridge/delta",
            state.delta
        )

        self.client.send_message(
            "/neurobridge/gamma",
            state.gamma
        )

        self.client.send_message(
            "/neurobridge/global_activity",
            state.global_activity
        )

    # ------------------------------------------------------
    # Debug Output
    # ------------------------------------------------------

    def print_brain_state(self, state: BrainState):

        print("-------------------------------------------")

        print(
            f"Attention      : {state.attention:.3f}"
        )

        print(
            f"Relaxation     : {state.relaxation:.3f}"
        )

        print()

        print(
            f"Alpha          : {state.alpha:.3f}"
        )

        print(
            f"Beta           : {state.beta:.3f}"
        )

        print(
            f"Theta          : {state.theta:.3f}"
        )

        print(
            f"Delta          : {state.delta:.3f}"
        )

        print(
            f"Gamma          : {state.gamma:.3f}"
        )

        print()

        print(
            f"GlobalActivity : {state.global_activity:.3f}"
        )

        print("-------------------------------------------")

    # ------------------------------------------------------

    def run(self):

        self.start()

        try:

            while True:

                time.sleep(1)

                data = self.board.get_board_data()

                state = self.compute_brain_state(
                    data
                )

                self.send_brain_state(
                    state
                )

                self.print_brain_state(
                    state
                )

        except KeyboardInterrupt:

            print("\nStopping...")

        finally:

            self.stop()


# ==========================================================
# Entry Point
# ==========================================================

def main():

    bridge = BrainBridge()

    bridge.run()


if __name__ == "__main__":

    main()