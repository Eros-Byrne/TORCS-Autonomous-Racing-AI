🏎️ TORCS Autonomous Racing AI Competition

🏆 Cardiff University Autonomous Racing Competition Submission:

This repository contains the source code for an autonomous racing agent developed in Python for the Cardiff University Autonomous Racing TORCS Competition (2025).

The project's objective was to develop a robust control or learning algorithm to successfully navigate the high-complexity, 3.6km "Corkscrew" track for three consecutive laps in the Open Source Racing Car Simulator (TORCS).

✨ Key Features:

Agent Core: Custom control logic and state machine (or a specific RL algorithm like DDPG/A2C if applicable) implemented in Python.

Environment Interaction: Utilizes the gym_torcs interface to connect the Python agent to the TORCS simulation environment.

Track Focus: Optimized specifically for high-speed, safe traversal of the demanding Corkscrew track.

⚙️ Technology Stack:

+ TORCS (The Open Racing Car Simulator)

+ Provides the physics and environment.

+ gym_torcs

+ Python wrapper for communication and state management.

+ Language = Python 3.14.0 this was Primary language for the agent and training scripts.

🚀 Getting Started:

These instructions assume you have the TORCS environment already set up as per the competition guidelines. This section focuses on running the Python agent client.

Prerequisites:

+ TORCS installed and configured (Tested with the torcs_CAR package provided).

+ Python 3.14.0 or newer.

+ Running the Agent

+ Start TORCS Server - Navigate to your TORCS installation (C:\torcs\torcs) and launch wtorcs.exe. Configure a Quick Race for this ai code the track Corkscrew used and that laps are set to 3 while using driver Ensure scr_server 1.

Launch Python Agent:
Open your terminal (PowerShell, Command Prompt, or Bash) and navigate to the agent directory (C:\torcs\gym_torcs).

# This command starts the client and connects to the TORCS server
python torcs_jm_par_enhanced.py 

Monitor Performance:
The agent will take control of the car. Check the terminal output for real-time sensor readings and control decisions.

📊 Competition Results:

Competition Rank: 1st Place

Best Lap Time: 01:45.321
