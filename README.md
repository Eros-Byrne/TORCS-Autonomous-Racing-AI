🚗 TORCS-Autonomous-Racing-AI

Cardiff University Autonomous Racing Competition Submission

This repository contains the source code for an autonomous racing agent developed in Python for the Cardiff University Autonomous Racing TORCS Competition (2025).

The goal of the project was to develop a robust control or learning algorithm to successfully navigate the high-complexity, 3.6km "Corkscrew" track for three consecutive laps in the Open Source Racing Car Simulator (TORCS) environment.

✨ Features

Agent Core: Custom control logic and state machine (or a specific RL algorithm like DDPG/A2C if applicable) implemented in Python.

Environment Interaction: Utilizes the gym_torcs interface to connect the Python agent to the TORCS simulation environment.

Track Focus: Optimized specifically for high-speed, safe traversal of the Corkscrew track.

⚙️ Technology Stack

Component

Technology

Role

Simulation

TORCS (The Open Racing Car Simulator)

Provides the physics and environment.

Interface

gym_torcs

Python wrapper for communication and state management.

Language

Python 3.14.0+

Primary language for the agent and training scripts.

Framework

(Placeholder: e.g., PyTorch, TensorFlow, or PID Control)

The specific AI/Control framework used for the driving logic.

🚀 Getting Started

These instructions assume you have the TORCS environment already set up as per the competition guidelines. This section focuses on running the Python agent.

Prerequisites

TORCS installed and configured (Tested with the torcs_CAR package provided).

Python 3.14.0 or newer.

Running the Agent

Start TORCS Server:
Navigate to your TORCS installation (C:\torcs\torcs) and launch wtorcs.exe. Configure a Quick Race:

Track: Corkscrew

Laps: 3

Driver: Ensure scr_server 1 is selected.

Launch Python Agent:
Open your terminal or PowerShell and navigate to the agent directory (C:\torcs\gym_torcs).

# This command starts the client and connects to the TORCS server
python torcs_jm_par.py 




Monitor Performance:
The agent will take control of the car. Check the terminal output for real-time sensor readings and control decisions.

💡 Agent Design and Methodology

(This is where you would describe your specific solution. Choose one of the two options below, or write your own.)

Option 1: Using Traditional Control Systems (e.g., PID)

The driving logic is primarily managed by a series of cascaded PID (Proportional-Integral-Derivative) controllers.

Lateral Control (Steering): A PID controller is used to minimize the angular difference between the car's current heading and the desired path (determined by the track center and track edge sensors).

Longitudinal Control (Throttle/Brake): A separate PID controller targets an optimal velocity for different track segments (e.g., slower target speed in sharp corners, higher on straights). This controller adjusts the throttle and brake inputs to maintain the target speed.

Option 2: Using Reinforcement Learning (e.g., DDPG)

The agent was trained using a Deep Deterministic Policy Gradient (DDPG) algorithm.

State Space: The state vector included 29 variables, such as track-edge distances, speed, RPM, and angle to track axis.

Action Space: Continuous actions for steering (

$$-1, 1$$

), acceleration (

$$0, 1$$

), and braking (

$$0, 1$$

).

Reward Function: The reward was shaped to prioritize high velocity while heavily penalizing off-track excursions, resulting in a focus on safety and sustained pace. Training was performed over 100,000 steps of environment interaction.

🎓 Competition Video and Results

Competition Video: Cardiff Autonomous Racing TORCS Demonstration (Hosted on Google Drive)

Competition Rank: 1st Place Won

Best Lap Time: (e.g., 01:45.321)
