#!/usr/bin/env python
"""
Simple Corkscrew AI Driver - Based on proven torcs_jm_par logic
Tuned specifically for the Corkscrew track tight corners.
"""

import math

# ==================== CONFIGURATION ====================
class DrivingConfig:
    """Configuration for the AI driver"""
    
    # Speed Management
    TARGET_SPEED = 180  # Allow full speed on straights
    MAX_SPEED = 180
    MIN_SPEED = 5
    
    # Steering Control
    STEER_GAIN = 70     # Increased for Corkscrew's tight turns
    CENTERING_GAIN = 0.60  # Keep original value
    STEER_SMOOTHING = 0.95
    
    # Braking Strategy
    BRAKE_THRESHOLD_TIGHT = 0.25  # Even earlier braking for Corkscrew
    
    # Acceleration Control
    ACCEL_GAIN = 0.20  # Slow acceleration to maintain stability
    ACCEL_DECAY = 0.35  # Quick braking/speed reduction
    ACCEL_MIN_THRESHOLD = 10  # Speed below which we boost acceleration
    
    # Traction Control
    ENABLE_TRACTION_CONTROL = True
    TRACTION_THRESHOLD = 2.2  # Wheel spin threshold
    TRACTION_REDUCTION = 0.15  # How much to reduce accel on wheel spin
    
    # Anti-Spin Prevention
    ENABLE_SPIN_PREVENTION = True
    SPIN_THRESHOLD = 0.3  # Angle threshold for spin detection (lower = earlier)
    SPIN_BRAKE = 0.7  # Apply brake if spinning (stronger braking)
    
    # Downshift Prevention
    ENABLE_DOWNFORCE = True
    DOWNFORCE_SPEED = 100  # Speed to start using downforce strategies
    
    # Gear Shifting
    GEAR_SPEEDS = [0, 35, 65, 100, 140, 180]  # Lower thresholds for upshifting, allow 6th gear
    GEAR_UPSHIFT_BUFFER = 5  # RPM buffer for upshifting
    GEAR_DOWNSHIFT_BUFFER = 10  # RPM buffer for downshifting
    
    # Recovery
    STUCK_THRESHOLD = 300  # Time before considered stuck
    STUCK_RECOVERY_TIME = 20  # How long to apply recovery
    
    # Track-specific (Corkscrew)
    CORKSCREW_CORRECTION = 0.8  # Reduced steering for Corkscrew's unique geometry


class AdvancedDriver:
    """Advanced driving AI with memory and adaptive behavior"""
    
    def __init__(self):
        self.config = DrivingConfig()
        self.prev_steer = 0
        self.prev_accel = 0.2
        self.prev_angle = 0
        self.stuck_counter = 0
        self.lap_count = 0
        self.last_dist_from_start = 0
        self.crash_recovery_time = 0
        
    def update_lap_counter(self, dist_from_start):
        """Track lap count based on distance reset"""
        if dist_from_start < self.last_dist_from_start and self.last_dist_from_start > 100:
            self.lap_count += 1
            print(f"Lap {self.lap_count} started!")
        self.last_dist_from_start = dist_from_start
    
    def detect_stuck(self, S):
        """Detect if the car is stuck"""
        if 'stucktimer' in S and S['stucktimer'] > self.config.STUCK_THRESHOLD:
            self.stuck_counter += 1
            return True
        else:
            self.stuck_counter = 0
            return False
    
    def calculate_speed_target(self, S):
        """Calculate dynamic target speed based on track conditions"""
        angle = abs(S['angle'])
        
        # Adjust target speed based on track curvature
        if angle > self.config.BRAKE_THRESHOLD_TIGHT:
            return self.config.TARGET_SPEED * 0.6  # Tight corners - slow down
        elif angle > self.config.BRAKE_THRESHOLD_MEDIUM:
            return self.config.TARGET_SPEED * 0.8  # Medium corners
        else:
            return self.config.TARGET_SPEED  # Straights - go fast
    
    def calculate_steering(self, S):
        """Steering using track sensors for robust cornering"""
        angle = S.get('angle', 0)
        track_pos = S.get('trackPos', 0)
        track = S.get('track', [200]*19)
        # Find where the track is most open ahead (max sensor value)
        max_idx = max(range(len(track)), key=lambda i: track[i])
        center_idx = 9
        # Calculate desired direction: negative = left, positive = right
        direction = (max_idx - center_idx) / 9.0  # -1 (far left) to +1 (far right)
        # Combine: follow open track, correct angle, and center car
        steer = direction * 0.7 + (angle * self.config.STEER_GAIN / math.pi) - (track_pos * self.config.CENTERING_GAIN)
        return max(-1, min(1, steer))
    
    def detect_upcoming_turn(self, S):
        """Look ahead in track sensors to detect sharp upcoming turns"""
        track = S.get('track', [200] * 19)
        
        # Check far ahead sensors (indices 5-13, looking 2-3 car lengths ahead)
        left_far = min(track[5:9])    # Left side far ahead
        center_far = min(track[10:14])  # Center far ahead
        right_far = min(track[15:18])   # Right side far ahead
        
        # Detect if there's a sharp turn ahead (narrow passage)
        sharpness = 0
        if left_far < 15 or right_far < 15:  # Very narrow corridor
            sharpness = 2  # Sharp turn coming
        elif left_far < 25 or right_far < 25:  # Moderately narrow
            sharpness = 1  # Medium turn coming
        
        return sharpness
    
    def calculate_brake(self, S, steer):
        """Brake based on upcoming track curvature using sensors"""
        track = S.get('track', [200]*19)
        speed = S.get('speedX', 0)
        center = track[9]
        min_ahead = min(track[7:12])
        angle = abs(S.get('angle', 0))
        # Only brake if car is turning (not on straight) and a real corner is coming
        if angle > 0.1:
            if min_ahead < 35 and speed > 80:
                return 0.4  # Brake for tight corner
            elif min_ahead < 60 and speed > 100:
                return 0.18  # Brake for medium corner
            elif min_ahead < 90 and speed > 130:
                return 0.07  # Light brake for gentle curve
        return 0.0
    
    def calculate_throttle(self, S, brake):
        """Throttle: full on straights, reduce for corners/braking"""
        speed = S.get('speedX', 0)
        track = S.get('track', [200]*19)
        min_ahead = min(track[7:12])
        # Lower target speed only for tight/medium corners, otherwise use full TARGET_SPEED
        if min_ahead < 40:
            target = 70
        elif min_ahead < 70:
            target = 100
        else:
            target = self.config.TARGET_SPEED
        # If braking, no throttle
        if brake > 0.1:
            accel = 0.0
        elif speed < target - 5:
            accel = 1.0
        elif speed < target:
            accel = 0.5
        else:
            accel = 0.2
        # Boost from standstill
        if speed < 5:
            accel = 1.0
        return max(0.0, min(1.0, accel))
    
    def apply_traction_control(self, S, accel):
        """Prevent wheel spin"""
        if not self.config.ENABLE_TRACTION_CONTROL:
            return accel
        
        # Calculate wheel spin
        wheel_spin = ((S['wheelSpinVel'][2] + S['wheelSpinVel'][3]) -
                      (S['wheelSpinVel'][0] + S['wheelSpinVel'][1]))
        
        if wheel_spin > self.config.TRACTION_THRESHOLD:
            accel -= self.config.TRACTION_REDUCTION
        
        return max(0.0, min(1.0, accel))
    
    def apply_spin_prevention(self, S, accel, brake):
        """Prevent spinouts"""
        if not self.config.ENABLE_SPIN_PREVENTION:
            return accel, brake
        
        angle = abs(S['angle'])
        
        if angle > self.config.SPIN_THRESHOLD and S['speedX'] > 30:
            accel = 0.0
            brake = self.config.SPIN_BRAKE
        
        return accel, brake
    
    def shift_gear(self, S):
        """Intelligent gear shifting"""
        speed = S.get('speedX', 0)
        
        # Determine gear based on speed thresholds
        # Always start at gear 1 (forward)
        gear = 1
        for i, threshold in enumerate(self.config.GEAR_SPEEDS):
            if speed > threshold:
                gear = i + 1
        
        # Clamp gear to valid range (1-6, no neutral or reverse)
        gear = max(1, min(6, gear))
        
        return gear
    
    def drive(self, server_state, driver_action):
        """Main driving logic - EXACT like original torcs_jm_par"""
        S = server_state.d
        R = driver_action.d
        
        # Update internal state
        self.update_lap_counter(S.get('distFromStart', 0))
        
        # Calculate controls
        R['steer'] = self.calculate_steering(S)
        self.prev_steer = R['steer']  # Track for throttle calculation
        R['accel'] = self.calculate_throttle(S, R['brake'])
        R['brake'] = self.calculate_brake(S, R['steer'])
        R['accel'] = self.apply_traction_control(S, R['accel'])
        R['gear'] = self.shift_gear(S)
        R['clutch'] = 0.0
    
    def _debug_print(self, S, R):
        """Optional debug output"""
        # Uncomment to enable debug output
        # print(f"Lap: {self.lap_count} | Speed: {S['speedX']:.1f} | Angle: {S['angle']:.2f} | Steer: {R['steer']:.2f}")
        pass


# ==================== MAIN ====================
if __name__ == "__main__":
    # This is an example of how to use the AdvancedDriver class
    # Import your TORCS client library and use it like this:
    #
    # from torcs_jm_par import Client
    # 
    # driver = AdvancedDriver()
    # client = Client(p=3001)
    # 
    # for step in range(client.maxSteps, 0, -1):
    #     client.get_servers_input()
    #     driver.drive(client.S, client.R)
    #     client.respond_to_server()
    # 
    # client.shutdown()
    
    print("Corkscrew AI Driver Loaded Successfully!")
    print("Import this module and use AdvancedDriver class in your TORCS client.")
