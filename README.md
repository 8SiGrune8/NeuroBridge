\# NeuroBridge



\## Overview



NeuroBridge is an experimental middleware layer that connects neurophysiological signals to interactive digital experiences.



The project is being developed as part of the Unreal Odyssey ecosystem and serves as a bridge between brain-computer interface technologies and real-time virtual environments.



The initial implementation focuses on EEG devices such as Muse 2 and Muse S, using BrainFlow as the signal acquisition layer and Unreal Engine 5 as the visualization layer.



The long-term goal is not to read thoughts or perform medical analysis, but to create meaningful interactions between a person's internal state and a digital world.



\---



\## Vision



NeuroBridge explores a simple idea:



> The state of consciousness can become a form of interaction.



Traditional interfaces rely on physical actions:



\* keyboard

\* mouse

\* controller

\* touch screen



NeuroBridge investigates a different approach:



\* attention

\* calmness

\* engagement

\* cognitive state



as inputs for digital experiences.



The project aims to transform invisible internal processes into visible changes inside a virtual world.



\---



\## Project Goals



\### Short-Term Goal



Build a working MVP that demonstrates:



EEG Signal → Interpretation → Unreal Engine Response



\### Mid-Term Goal



Create a reusable middleware layer that can:



\* receive EEG signals from supported devices

\* process and interpret brain activity

\* expose high-level cognitive metrics

\* communicate with external applications



\### Long-Term Goal



Provide a foundation for adaptive interactive experiences where virtual environments respond to the user's mental state in real time.



\---



\## Current Technology Stack



\### EEG Acquisition



\* Muse 2

\* Muse S



\### Signal Layer



\* BrainFlow



\### Processing Layer



\* Python



\### Communication Layer



\* UDP (initial MVP)



\### Visualization Layer



\* Unreal Engine 5



\---



\## System Architecture



Muse 2 / Muse S

↓

BrainFlow

↓

NeuroBridge

↓

MindState Interpretation

↓

UDP Communication

↓

Unreal Engine 5

↓

Dynamic World Response



\---



\## MVP Scope



The first MVP focuses on a single real-time metric:



MindState



The goal is to transform EEG-derived values into a normalized parameter that can drive visual changes inside Unreal Engine.



Examples:



\* Light intensity

\* Atmospheric effects

\* Fog density

\* Material parameters

\* Audio ambience



The purpose of the MVP is to demonstrate a clear relationship between a user's mental state and the virtual environment.



\---



\## Development Stages



\### Stage 1



BrainFlow integration



Status: Complete



\* Python environment configured

\* BrainFlow installed

\* Synthetic Board operational

\* Real-time data stream verified



\### Stage 2



MindState prototype



Status: In Progress



\* Continuous signal acquisition

\* Basic state estimation

\* Real-time updates



\### Stage 3



UE5 Integration



Status: Planned



\* UDP communication

\* Unreal Engine receiver

\* Real-time visual feedback



\### Stage 4



Muse Integration



Status: Planned



\* Muse S / Muse 2 connectivity

\* Live EEG acquisition

\* Real-world testing



\---



\## Non-Goals



NeuroBridge is not intended to:



\* perform medical diagnostics

\* replace clinical EEG systems

\* interpret thoughts

\* provide healthcare recommendations



The project focuses exclusively on interactive and experiential applications.



\---



\## Project Status



Current Status:



Prototype Development



The project has successfully established the first working data pipeline using BrainFlow Synthetic Board streams and is progressing toward real-time Unreal Engine integration.



\---



\## License



TBD



## Important OSC Configuration (UE 5.7+)
When creating the OSC Server in Unreal Engine, set:
Receive IP Address = 0.0.0.0
Using 127.0.0.1 may prevent the Blueprint OSC receiver from receiving messages, even though the sender is transmitting correctly.
OSC sender can still transmit to:
127.0.0.1:7001
while the UE server listens on:
0.0.0.0:7001

---

# NeuroBridge Development Milestones

## Milestone M0 — Project Foundation

* [x] Python environment installed
* [x] Git repository initialized
* [x] BrainFlow installed
* [x] Project structure created

---

## Milestone M1 — Unreal Communication Pipeline

* [x] OSC Sender implemented in Python
* [x] OSC Receiver implemented in Unreal Engine
* [x] Real-time float transmission verified
* [x] Successfully controlled an Unreal Engine actor from external OSC data (Sphere scale)

## Milestone M2 — BrainFlow Integration

* [ ] Connected BrainFlow Synthetic Board
* [ ] Implemented a prototype MindState metric
* [ ] Streamed BrainFlow data via OSC
* [ ] Successfully controlled Unreal Engine visualization using BrainFlow data

## Milestone M3 — BrainView Prototype

The first functional prototype of **BrainView** has been developed — a research-oriented visualization module for representing brain activity inside Unreal Engine 5.

Unlike a static 3D brain model, BrainView is designed as a scalable visualization framework capable of receiving data from both real EEG devices (e.g. Muse) and software simulators such as the BrainFlow Synthetic Board.

Completed features:

- [x] Automatic generation of neural nodes
- [x] BrainNode data structure implemented
- [x] Automatic assignment of anatomical brain regions
- [x] GPU data transfer using **Per Instance Custom Data**
- [x] Procedural neuron material created
- [x] First visualization control pipeline implemented
- [x] Global neural activity can be controlled through a single parameter, allowing the entire brain visualization to change its flickering behaviour in real time

BrainView will serve as the primary visualization subsystem of NeuroBridge.

---

## Milestone M4 — NeuroBridge Live Pipeline

The first complete real-time data pipeline between BrainFlow and Unreal Engine has been successfully demonstrated.

Completed features:

- [x] BrainFlow Synthetic Board connected
- [x] Real-time MindState calculation
- [x] OSC transmission implemented
- [x] Unreal Engine 5.7 receives OSC messages successfully
- [x] BrainFlow data directly controls objects inside Unreal Engine

### Architecture

```
BrainFlow Synthetic Board
          ↓
      MindState
          ↓
      Python OSC
          ↓
      Unreal Engine 5.7
          ↓
 Blueprint Visualization
```

### Important OSC Configuration (UE 5.7+)

When creating an OSC Server in Unreal Engine 5.7, use:

```
Receive IP Address = 0.0.0.0
```

instead of

```
127.0.0.1
```

The OSC sender may still transmit to:

```
127.0.0.1:7001
```

while the Unreal Engine server listens on

```
0.0.0.0:7001
```

Using `127.0.0.1` as the **Receive IP Address** prevented OSC messages from being received during testing, while `0.0.0.0` resolved the issue completely.

This configuration has been verified with Unreal Engine **5.7**.

---



## Not released


## Milestone M3 — Muse Integration

* [ ] Connect Muse 2 / Muse S
* [ ] Receive live EEG stream
* [ ] Compute MindState metric
* [ ] Stream MindState to Unreal Engine

## Milestone M4 — Neurofeedback Prototype

* [ ] Create visual feedback scene
* [ ] Smooth incoming values
* [ ] User-controlled visual response
* [ ] End-to-end NeuroBridge MVP demonstration


---


## Development Log

### 2026-06-30
- BrainFlow Synthetic Board successfully connected to Unreal Engine.
- Real-time OSC communication verified.
- First live visualization driven by BrainFlow data.
- Unreal Engine 5.7 OSC receiver configuration issue resolved (`Receive IP Address = 0.0.0.0`).

### 2026-06-XX
- BrainView prototype completed.
- Procedural neuron rendering implemented.

