class SignalController:
    def __init__(self, max_capacity=20):
        """
        Initializes the Adaptive Signal Controller.
        max_capacity: The estimated maximum number of vehicles that can fit in the zone.
                      Used to calculate the Density Percentage.
        """
        self.max_capacity = max_capacity

    def compute_signal(self, current_vehicles):
        """
        Calculates density and returns the recommended signal timings.
        """
        # Calculate density percentage (capped at 100%)
        density = min((current_vehicles / self.max_capacity) * 100, 100)
        
        # Adaptive logic based on density thresholds
        if density < 20:
            status = "Low Traffic"
            green_time = 20  # seconds
        elif density < 60:
            status = "Moderate Traffic"
            green_time = 40  # seconds
        else:
            status = "Heavy Traffic"
            green_time = 60  # seconds
            
        return density, status, green_time
