#!/usr/bin/env python
"""
Corkscrew Track Map with Waypoints and Braking Points
Based on track XML analysis - helps predict upcoming corners
"""

# Corkscrew track segments and their characteristics
# Format: (segment_name, type, distance_m, radius_m, arc_deg, brake_threshold)
# Used to brake BEFORE reaching each corner

CORKSCREW_SEGMENTS = [
    # Start/Finish straight
    ("s1", "lft", 32, 153.7, 12.0, 0.15),   # Gentle left turn
    ("s2", "str", 152, None, 0, 0.0),       # Straight
    ("s3", "lft", 38, 86.5, 25.0, 0.35),    # T1 - Medium left turn **BRAKE HERE**
    ("s5", "rgt", 78, 185.7, 15.0, 0.25),   # T2 - Medium right turn
    ("s6", "str", 27, None, 0, 0.0),        # Short straight
    ("s7", "lft", 45, 79.3, 32.0, 0.40),    # T3 - Sharp left turn **BRAKE HARD**
    ("s8", "str", 35, None, 0, 0.0),        # Straight
    ("s9", "rgt", 40, 119.7, 20.0, 0.30),   # T4 - Medium right turn
    ("s10", "str", 32, None, 0, 0.0),       # Straight
    ("s11", "lft", 125, 130.3, 54.0, 0.50), # T5 - Very sharp left (spiral) **BRAKE HARD**
    ("s14", "rgt", 80, 150.0, 30.0, 0.40),  # T6 - Sharp right turn **BRAKE**
    ("s16", "str", 94, None, 0, 0.0),       # Straight
    ("s17", "lft", 35, 95.2, 21.0, 0.30),   # T7 - Medium left turn
    ("s18", "str", 70, None, 0, 0.0),       # Straight
    ("s20", "rgt", 35, 120.0, 16.0, 0.25),  # T8 - Medium right turn
    ("s21", "lft", 117, 75.0, 89.0, 0.55),  # T9 - SHARP left spiral **BRAKE VERY HARD**
    ("s23", "str", 50, None, 0, 0.0),       # Straight
    ("s24", "rgt", 35, 100.0, 20.0, 0.30),  # T10 - Medium right turn
    ("s25", "str", 35, None, 0, 0.0),       # Straight
    ("s26", "lft", 32, 115.0, 16.0, 0.25),  # T11 - Medium left turn
    ("s27", "str", 160, None, 0, 0.0),      # Final straight back to start
]

# Cumulative distances to each segment start (approximate)
SEGMENT_DISTANCES = {
    "s1": 0,
    "s2": 32,
    "s3": 184,
    "s5": 222,
    "s6": 300,
    "s7": 327,
    "s8": 372,
    "s9": 407,
    "s10": 447,
    "s11": 479,
    "s14": 604,
    "s16": 684,
    "s17": 778,
    "s18": 813,
    "s20": 883,
    "s21": 918,
    "s23": 1035,
    "s24": 1085,
    "s25": 1120,
    "s26": 1155,
    "s27": 1187,
}

# Total track length (approximate)
TRACK_LENGTH = 1347  # meters

def get_upcoming_corner(distance_from_start, lookahead=100):
    """
    Detect upcoming corner based on current distance
    lookahead: meters ahead to look (default 100m)
    
    Returns: (corner_name, distance_to_corner, brake_threshold, turn_type)
    """
    target_distance = distance_from_start + lookahead
    
    for segment_name, seg_type, seg_length, radius, arc, brake_thresh in CORKSCREW_SEGMENTS:
        seg_dist = SEGMENT_DISTANCES.get(segment_name, 0)
        
        if distance_from_start < seg_dist < target_distance:
            distance_to_corner = seg_dist - distance_from_start
            return (segment_name, distance_to_corner, brake_thresh, seg_type)
    
    return (None, 0, 0.0, None)


def calculate_adaptive_brake(current_distance, speed, angle):
    """
    Calculate brake based on track knowledge and current state
    """
    upcoming_corner, dist_to_corner, brake_threshold, turn_type = get_upcoming_corner(current_distance)
    
    brake = 0.0
    
    # Current angle-based braking
    if angle > 0.5:
        brake = 0.8
    elif angle > 0.35:
        brake = 0.6
    elif angle > 0.25:
        brake = 0.4
    
    # Lookahead braking - brake BEFORE the corner
    if upcoming_corner and dist_to_corner < 50:
        # We're approaching a corner
        if dist_to_corner < 20:
            # Very close - brake hard
            brake = max(brake, brake_threshold + 0.1)
        else:
            # Starting to approach - light braking
            brake = max(brake, brake_threshold - 0.1)
    
    return max(0.0, min(1.0, brake))


def get_target_speed(current_distance, current_speed):
    """
    Get recommended speed based on track section
    """
    upcoming_corner, dist_to_corner, brake_threshold, turn_type = get_upcoming_corner(current_distance)
    
    base_speed = 110  # Target speed on straights
    
    if upcoming_corner:
        if brake_threshold > 0.50:
            # Very sharp corner coming
            return 60  if dist_to_corner < 100 else base_speed
        elif brake_threshold > 0.35:
            # Medium corner
            return 75 if dist_to_corner < 80 else base_speed
        elif brake_threshold > 0.25:
            # Light corner
            return 90 if dist_to_corner < 60 else base_speed
    
    return base_speed


if __name__ == "__main__":
    print("Corkscrew Track Map Loaded")
    print(f"Total track length: {TRACK_LENGTH}m")
    print(f"Number of segments: {len(CORKSCREW_SEGMENTS)}")
    
    # Test lookahead at various distances
    test_distances = [0, 100, 300, 500, 900, 1200]
    for dist in test_distances:
        corner, dist_to, brake_thresh, turn_type = get_upcoming_corner(dist)
        speed = get_target_speed(dist, 100)
        print(f"\nAt distance {dist}m: Next corner = {corner} ({dist_to}m away), brake at {brake_thresh}, target speed {speed} km/h")
