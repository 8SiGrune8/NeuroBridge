"""
===========================================================
 NeuroBridge Visual Runtime
-----------------------------------------------------------

Version : 2.0

Milestone : M7

Official NeuroBridge Runtime

-----------------------------------------------------------

Python ---> Unreal Engine

    /neurobridge/state

    Port 7001

-----------------------------------------------------------

Unreal Engine ---> Python

    /neurobridge/command

    Port 7002

===========================================================
"""

from dataclasses import dataclass
from enum import Enum

from pythonosc.udp_client import SimpleUDPClient

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer

import threading

import math
import random
import time



# =========================================================
# OSC CONFIGURATION
# =========================================================

UE_IP = "127.0.0.1"

UE_PORT = 7001

COMMAND_PORT = 7002



# =========================================================
# OSC CLIENT
# =========================================================

osc_client = SimpleUDPClient(

    UE_IP,

    UE_PORT

)



# =========================================================
# BRAIN STATE
# =========================================================

@dataclass
class BrainState:

    alpha: float

    beta: float

    theta: float

    gamma: float

    attention: float

    relaxation: float

    global_activity: float



# =========================================================
# VISUAL SCENARIOS
# =========================================================

class VisualScenario(Enum):

    RELAXED = "Relaxed"

    FOCUSED = "Focused"

    FLOW = "Flow"

    INSIGHT = "Insight"



# =========================================================
# VISUAL GENERATOR
# =========================================================

class VisualStateGenerator:

    def __init__(self):

        self.start_time = time.time()

        self.current_scenario = VisualScenario.FLOW

        print()

        print("========================================")
        print(" NeuroBridge Runtime")
        print("========================================")

        print()

        print(
            f"Current Scenario : {self.current_scenario.value}"
        )

        print()



    # -----------------------------------------------------
    # Scenario Control
    # -----------------------------------------------------

    def set_scenario(

        self,

        scenario: VisualScenario

    ):

        if scenario == self.current_scenario:

            return

        self.current_scenario = scenario

        print()

        print("========================================")
        print(" Scenario Changed")
        print("----------------------------------------")

        print(
            self.current_scenario.value
        )

        print("========================================")

        print()



    # -----------------------------------------------------
    # Generate
    # -----------------------------------------------------

    def generate(self) -> BrainState:

        t = time.time() - self.start_time

        if self.current_scenario == VisualScenario.RELAXED:

            return self.generate_relaxed(t)

        if self.current_scenario == VisualScenario.FOCUSED:

            return self.generate_focused(t)

        if self.current_scenario == VisualScenario.INSIGHT:

            return self.generate_insight(t)

        return self.generate_flow(t)




    def generate_relaxed(self, t) -> BrainState:

        alpha = 0.82 + 0.05 * math.sin(t * 0.25)

        beta = 0.22 + 0.03 * math.sin(t * 0.55)

        theta = 0.68 + 0.04 * math.sin(t * 0.18)

        gamma = 0.08 + 0.01 * math.sin(t * 1.20)

        attention = 0.25 + 0.05 * math.sin(t * 0.40)

        relaxation = 0.92 + 0.03 * math.sin(t * 0.18)

        global_activity = 0.42 + 0.03 * math.sin(t * 0.30)

        return BrainState(

            alpha,

            beta,

            theta,

            gamma,

            attention,

            relaxation,

            global_activity

        )


    # -----------------------------------------------------
    # Focused
    # -----------------------------------------------------

    def generate_focused(self, t) -> BrainState:

        alpha = 0.42 + 0.03 * math.sin(t * 0.70)

        beta = 0.88 + 0.05 * math.sin(t * 0.45)

        theta = 0.18 + 0.02 * math.sin(t * 0.35)

        gamma = 0.34 + 0.04 * math.sin(t * 1.10)

        attention = 0.93 + 0.03 * math.sin(t * 0.60)

        relaxation = 0.22 + 0.03 * math.sin(t * 0.50)

        global_activity = 0.82 + 0.04 * math.sin(t * 0.55)

        return BrainState(

            alpha,

            beta,

            theta,

            gamma,

            attention,

            relaxation,

            global_activity

        )


    # -----------------------------------------------------
    # Flow
    # -----------------------------------------------------

    def generate_flow(self, t) -> BrainState:

        alpha = 0.68 + 0.08 * math.sin(t * 0.70)

        beta = 0.72 + 0.07 * math.sin(t * 0.90)

        theta = 0.42 + 0.05 * math.sin(t * 0.50)

        gamma = 0.55 + 0.05 * math.sin(t * 1.50)

        attention = 0.78 + 0.08 * math.sin(t * 0.65)

        relaxation = 0.72 + 0.08 * math.sin(t * 0.40)

        global_activity = 0.86 + 0.05 * math.sin(t * 0.45)

        return BrainState(

            alpha,

            beta,

            theta,

            gamma,

            attention,

            relaxation,

            global_activity

        )


    # -----------------------------------------------------
    # Insight
    # -----------------------------------------------------

    def generate_insight(self, t) -> BrainState:

        gamma_burst = 0.18 * max(

            0.0,

            math.sin(t * 2.60)

        )

        alpha = 0.58 + 0.04 * math.sin(t * 0.45)

        beta = 0.74 + 0.06 * math.sin(t * 0.75)

        theta = 0.32 + 0.05 * math.sin(t * 0.28)

        gamma = 0.62 + gamma_burst

        attention = 0.88 + 0.05 * math.sin(t * 0.55)

        relaxation = 0.54 + 0.06 * math.sin(t * 0.30)

        global_activity = 0.94 + gamma_burst * 0.30

        return BrainState(

            alpha,

            beta,

            theta,

            gamma,

            attention,

            relaxation,

            global_activity

        )




# =========================================================
# OSC SENDER
# =========================================================

class BrainBridgeSender:

    def __init__(self):

        self.client = osc_client


    # -----------------------------------------------------
    # Send Brain State
    # -----------------------------------------------------

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


# =========================================================
# COMMAND SERVER
# =========================================================

class NeuroBridgeCommandServer:

    def __init__(

        self,

        generator: VisualStateGenerator

    ):

        self.generator = generator

        self.dispatcher = Dispatcher()

        self.dispatcher.map(

            "/neurobridge/command",

            self.on_command

        )

        self.server = ThreadingOSCUDPServer(

            (

                "127.0.0.1",

                COMMAND_PORT

            ),

            self.dispatcher

        )


    # -----------------------------------------------------
    # Start
    # -----------------------------------------------------

    def start(self):

        print()

        print("========================================")
        print(" NeuroBridge Command Server")
        print("========================================")

        print(

            f"Listening : 127.0.0.1:{COMMAND_PORT}"

        )

        print()

        threading.Thread(

            target=self.server.serve_forever,

            daemon=True

        ).start()


    # -----------------------------------------------------
    # Command Handler
    # -----------------------------------------------------

    def on_command(

        self,

        address,

        *args

    ):

        if len(args) == 0:

            return

        command = str(args[0]).lower()

        print()

        print("========================================")
        print(" NeuroBridge Command")
        print("----------------------------------------")

        print(f"Address : {address}")

        print(f"Command : {command}")

        print("========================================")

        print()


        if command == "relaxed":

            self.generator.set_scenario(

                VisualScenario.RELAXED

            )

            return


        if command == "focused":

            self.generator.set_scenario(

                VisualScenario.FOCUSED

            )

            return


        if command == "flow":

            self.generator.set_scenario(

                VisualScenario.FLOW

            )

            return


        if command == "insight":

            self.generator.set_scenario(

                VisualScenario.INSIGHT

            )

            return


        print(

            f"Unknown command : {command}"

        )




# =========================================================
# RUNTIME
# =========================================================

class BrainBridgeRuntime:

    def __init__(self):

        self.generator = VisualStateGenerator()

        self.sender = BrainBridgeSender()

        self.command_server = NeuroBridgeCommandServer(

            self.generator

        )


    # -----------------------------------------------------
    # Startup
    # -----------------------------------------------------

    def start(self):

        print()

        print("========================================")
        print(" NeuroBridge Runtime")
        print("========================================")

        print("Initializing...")

        print()

        self.command_server.start()

        print("Brain Generator      ✓")

        print("OSC Sender           ✓")

        print("OSC Command Server   ✓")

        print()

        print("----------------------------------------")

        print(f"UE Output Port : {UE_PORT}")

        print(f"Python Port    : {COMMAND_PORT}")

        print()

        print("Runtime Started")

        print("----------------------------------------")

        print()

        print("Press Ctrl+C to stop.")

        print()


    # -----------------------------------------------------
    # Update
    # -----------------------------------------------------

    def tick(self):

        state = self.generator.generate()

        self.sender.send_brain_state(

            state

        )

        self.print_state(state)


    # -----------------------------------------------------
    # Debug
    # -----------------------------------------------------

    def print_state(

        self,

        state: BrainState

    ):

        print(

            f"A:{state.alpha:.3f}   "

            f"B:{state.beta:.3f}   "

            f"T:{state.theta:.3f}   "

            f"G:{state.gamma:.3f}   "

            f"Att:{state.attention:.3f}   "

            f"Rel:{state.relaxation:.3f}   "

            f"GA:{state.global_activity:.3f}"

        )


    # -----------------------------------------------------
    # Main Loop
    # -----------------------------------------------------

    def run(self):

        self.start()

        try:

            while True:

                self.tick()

                time.sleep(0.10)

        except KeyboardInterrupt:

            print()

            print("----------------------------------------")

            print("Stopping NeuroBridge Runtime...")

            print("----------------------------------------")

            print()

        finally:

            print("Runtime stopped.")

            print()





# =========================================================
# ENTRY POINT
# =========================================================

def main():

    runtime = BrainBridgeRuntime()

    runtime.run()


if __name__ == "__main__":

    main()
