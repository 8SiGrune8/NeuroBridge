############################################################
#
# NeuroBridge
#
# BrainBridge v2.0
#
# Streams complete BrainState from BrainFlow
# to Unreal Engine via OSC.
#
# Current Board:
#   BrainFlow Synthetic Board
#
# OSC Protocol:
#   /neurobridge/state
#
############################################################

from dataclasses import dataclass
import time

import numpy as np

from brainflow.board_shim import (
    BoardShim,
    BrainFlowInputParams,
    BoardIds
)

from pythonosc.udp_client import SimpleUDPClient


############################################################
# Configuration
############################################################

OSC_IP = "127.0.0.1"
OSC_PORT = 7001


############################################################
# BrainState
#
# Unified brain state transmitted to Unreal Engine.
############################################################

@dataclass
class BrainState:

    alpha: float

    beta: float

    theta: float

    gamma: float

    attention: float

    relaxation: float

    global_activity: float


############################################################
# BrainBridge
############################################################

class BrainBridge:

    def __init__(self):

        BoardShim.enable_dev_board_logger()

        self.client = SimpleUDPClient(
            OSC_IP,
            OSC_PORT
        )

        params = BrainFlowInputParams()

        self.board_id = BoardIds.SYNTHETIC_BOARD.value

        self.board = BoardShim(
            self.board_id,
            params
        )

    ########################################################

    def start(self):

        self.board.prepare_session()
        self.board.start_stream()

        print("🧠 BrainBridge v2 started\n")

    ########################################################

    def stop(self):

        self.board.stop_stream()
        self.board.release_session()

        print("\n✅ BrainBridge stopped")

    ########################################################
    # Read EEG channels
    ########################################################

    def compute_brain_state(self) -> BrainState:

        data = self.board.get_board_data()

        eeg = BoardShim.get_eeg_channels(
            self.board_id
        )

        ####################################################
        # Raw bands
        ####################################################

        alpha = float(np.mean(data[eeg[0]]))
        beta = float(np.mean(data[eeg[1]]))
        theta = float(np.mean(data[eeg[2]]))
        gamma = float(np.mean(data[eeg[3]]))

        ####################################################
        # Derived metrics
        ####################################################

        attention = beta / max(alpha, 1e-6)

        relaxation = alpha / max(beta, 1e-6)

        global_activity = (
            alpha +
            beta +
            theta +
            gamma
        ) / 4.0

        ####################################################

        return BrainState(

            alpha=alpha,

            beta=beta,

            theta=theta,

            gamma=gamma,

            attention=attention,

            relaxation=relaxation,

            global_activity=global_activity

        )

    ########################################################
    # Send complete BrainState
    ########################################################

    def send_brain_state(
        self,
        state: BrainState
    ):

        self.client.send_message(

            "/neurobridge/state",

            [

                state.alpha,

                state.beta,

                state.theta,

                state.gamma,

                state.attention,

                state.relaxation,

                state.global_activity

            ]

        )

    ########################################################
    # Console Output
    ########################################################

    def print_brain_state(
        self,
        state: BrainState
    ):

        print()

        print("========== BrainState ==========")

        print(f"Alpha            : {state.alpha:8.3f}")
        print(f"Beta             : {state.beta:8.3f}")
        print(f"Theta            : {state.theta:8.3f}")
        print(f"Gamma            : {state.gamma:8.3f}")

        print("--------------------------------")

        print(f"Attention        : {state.attention:8.3f}")
        print(f"Relaxation       : {state.relaxation:8.3f}")
        print(f"Global Activity  : {state.global_activity:8.3f}")

        print("================================")

    ########################################################

    def update(self):

        state = self.compute_brain_state()

        self.send_brain_state(state)

        self.print_brain_state(state)


############################################################
# Main
############################################################

def main():

    bridge = BrainBridge()

    bridge.start()

    try:

        while True:

            time.sleep(1)

            bridge.update()

    except KeyboardInterrupt:

        pass

    finally:

        bridge.stop()


############################################################

if __name__ == "__main__":

    main()