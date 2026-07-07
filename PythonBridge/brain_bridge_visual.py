"""
===========================================================
 NeuroBridge Visual Simulation Module
-----------------------------------------------------------

 Generates physiologically plausible synthetic cognitive
 states for BrainView, HUD and presentation purposes.

 This module is NOT intended to replace real EEG.

 Real EEG:
     brain_bridge_v2.py

 Visual Simulation:
     brain_bridge_visual.py

 Unreal Engine OSC Protocol:
     /neurobridge/state

 NeuroBridge Prototype v0.1
===========================================================
"""

from dataclasses import dataclass
from enum import Enum
from pythonosc.udp_client import SimpleUDPClient

import math
import random
import time


# =========================================================
# OSC
# =========================================================

OSC_IP = "127.0.0.1"
OSC_PORT = 7001

client = SimpleUDPClient(OSC_IP, OSC_PORT)


# =========================================================
# Brain State
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
# Scenarios
# =========================================================

class VisualScenario(Enum):

    RELAXED = 0
    FOCUSED = 1
    FLOW = 2
    INSIGHT = 3


# ---------------------------------------------------------
# Change scenario here
# ---------------------------------------------------------

SCENARIO = VisualScenario.FLOW


# =========================================================
# Generator
# =========================================================

class VisualStateGenerator:

    def __init__(self):

        self.start_time = time.time()

    # -----------------------------------------------------

    def generate(self):

        t = time.time() - self.start_time

        if SCENARIO == VisualScenario.RELAXED:
            return self.relaxed(t)

        if SCENARIO == VisualScenario.FOCUSED:
            return self.focused(t)

        if SCENARIO == VisualScenario.INSIGHT:
            return self.insight(t)

        return self.flow(t)

    # =====================================================
    # FLOW
    # =====================================================

    def flow(self, t):

        alpha = 0.65 + 0.15 * math.sin(t * 0.30)

        beta = 0.55 + 0.20 * math.sin(t * 0.90)

        theta = 0.40 + 0.12 * math.sin(t * 0.18)

        gamma = 0.15 + 0.03 * math.sin(t * 4.00)

        attention = 0.70 + 0.20 * math.sin(t * 0.70)

        relaxation = 1.0 - attention

        activity = (
            alpha
            + beta
            + theta
            + gamma
        ) / 4.0

        return BrainState(
            alpha,
            beta,
            theta,
            gamma,
            attention,
            relaxation,
            activity
        )

    # =====================================================
    # RELAXED
    # =====================================================

    def relaxed(self, t):

        alpha = 0.85 + 0.08 * math.sin(t * 0.20)

        beta = 0.25 + 0.05 * math.sin(t * 0.70)

        theta = 0.70 + 0.05 * math.sin(t * 0.15)

        gamma = 0.10

        attention = 0.25 + 0.05 * math.sin(t * 0.30)

        relaxation = 0.90

        activity = (
            alpha
            + beta
            + theta
            + gamma
        ) / 4.0

        return BrainState(
            alpha,
            beta,
            theta,
            gamma,
            attention,
            relaxation,
            activity
        )

    # =====================================================
    # FOCUSED
    # =====================================================

    def focused(self, t):

        alpha = 0.30

        beta = 0.90 + 0.05 * math.sin(t * 1.20)

        theta = 0.20

        gamma = 0.30 + 0.05 * math.sin(t * 3.50)

        attention = 0.92

        relaxation = 0.12

        activity = (
            alpha
            + beta
            + theta
            + gamma
        ) / 4.0

        return BrainState(
            alpha,
            beta,
            theta,
            gamma,
            attention,
            relaxation,
            activity
        )

    # =====================================================
    # INSIGHT
    # =====================================================

    def insight(self, t):

        alpha = 0.45

        beta = 0.60

        theta = 0.35

        gamma = 0.15

        if int(t) % 7 == 0:
            gamma += 0.60

        attention = 0.75

        relaxation = 0.25

        activity = (
            alpha
            + beta
            + theta
            + gamma
        ) / 4.0

        return BrainState(
            alpha,
            beta,
            theta,
            gamma,
            attention,
            relaxation,
            activity
        )


# =========================================================
# Sender
# =========================================================

def send_brain_state(state: BrainState):

    client.send_message(
        "/neurobridge/state",
        [
            state.alpha,
            state.beta,
            state.theta,
            state.gamma,
            state.attention,
            state.relaxation,
            state.global_activity,
        ],
    )


# =========================================================
# Main
# =========================================================

def main():

    generator = VisualStateGenerator()

    print("\n========================================")
    print(" NeuroBridge Visual Simulation")
    print("========================================")

    print(f"Scenario : {SCENARIO.name}")

    print("----------------------------------------")

    try:

        while True:

            state = generator.generate()

            send_brain_state(state)

            print(
                f"A:{state.alpha:.2f} "
                f"B:{state.beta:.2f} "
                f"T:{state.theta:.2f} "
                f"G:{state.gamma:.2f} "
                f"Att:{state.attention:.2f} "
                f"Rel:{state.relaxation:.2f} "
                f"Act:{state.global_activity:.2f}"
            )

            time.sleep(0.05)

    except KeyboardInterrupt:

        print("\nStopped.")


# =========================================================

if __name__ == "__main__":
    main()