package open_door_and_window

# Priority is determined by the order of the rules
allow {
    smoke_detected
}

allow {
    owner_at_home
}

smoke_detected {
    input.smoke_detector.smoke_detected
}

owner_at_home {
    input.owner_location.at_home
}

# The policy is to lock the doors and windows when the owner is away