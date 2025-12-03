# 🏎️ Cardiff Autonomous Racing — TORCS AI Competition (2025)

This repository contains my submission for the **Cardiff University Autonomous Racing TORCS Competition (2025)**.  
It includes a custom autonomous racing agent built in Python, designed to navigate the challenging **3.6km Corkscrew** track for **three consecutive laps** inside the TORCS simulator.

---

## ✨ Key Features

### Autonomous Agent Logic
Custom control logic and a state-driven behaviour system (or RL algorithm such as DDPG/A2C depending on implementation).

### Environment Integration
Uses **gym_torcs** to communicate with the TORCS simulation, process sensor data, and apply control actions.

### Track-Optimised Behaviour
Specifically tuned for the **Corkscrew** track to balance high speed, stability, and safe cornering.

---

## ⚙️ Technology Stack

| Component | Description |
|----------|-------------|
| **TORCS (The Open Racing Car Simulator)** | Physics engine and racing simulation used for development and testing. |
| **gym_torcs** | Python wrapper for communication, state retrieval, and control signalling. |
| **Python 3.14.0** | Primary programming language for the agent logic and scripts. |

---

## 🚀 Getting Started

These instructions assume TORCS is already installed following the official competition setup.

### Prerequisites

- TORCS installed and configured  
  *(tested with the torcs_CAR package supplied in competition resources)*  
- Python **3.14.0** or newer  
- `gym_torcs` located at:  
