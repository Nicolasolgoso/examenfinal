import math
import matplotlib.pyplot as plt
import numpy as np

def projectile_motion(initial_speed, launch_angle):
    # Constants
    g = 9.8  # acceleration due to gravity (m/s^2)

    # Convert launch angle to radians
    launch_angle_rad = math.radians(launch_angle)

    # Initial velocity components
    vx0 = initial_speed * math.cos(launch_angle_rad)
    vy0 = initial_speed * math.sin(launch_angle_rad)

    # Time of flight
    flight_time = (2 * vy0) / g

    # Time intervals for position calculation
    time_intervals = np.linspace(0, flight_time, num=1000)

    # Calculate projectile position at regular time intervals
    x_positions = vx0 * time_intervals
    y_positions = vy0 * time_intervals - 0.5 * g * time_intervals**2

    # Combine time and position data into a list
    projectile_data = np.array(list(zip(time_intervals, x_positions, y_positions)))

    # Visualize the trajectory
    plt.plot(x_positions, y_positions, label=f'Speed: {initial_speed} m/s, Angle: {launch_angle} degrees')
    plt.title('Projectile Motion')
    plt.xlabel('Horizontal Distance (m)')
    plt.ylabel('Vertical Distance (m)')
    plt.grid(True)
    plt.legend()
    plt.show()

    return {"speed": initial_speed, "angle": launch_angle, "max_distance": max(x_positions),
            "max_height": max(y_positions), "flight_time": flight_time, "position_data": projectile_data}

def save_to_file(data, filename):
    with open(filename, 'w') as file:
        file.write("Time (s)\tHorizontal Distance (m)\tVertical Distance (m)\n")
        for entry in data:
            file.write("\t".join(map(str, entry)) + "\n")

def analyze_projectiles(projectiles, time_limit):
    # Find the launch with the maximum distance
    max_distance_launch = max(projectiles, key=lambda p: p["max_distance"])

    # Find the launch with the highest altitude
    max_height_launch = max(projectiles, key=lambda p: p["max_height"])

    # Find launches exceeding the time limit
    exceeding_time_limit = [p for p in projectiles if p["flight_time"] > time_limit]

    # Output analysis
    print("Maximum Distance Reached: {:.2f} meters".format(max_distance_launch["max_distance"]))
    print("Launch with Highest Altitude:")
    print("Speed: {} m/s, Angle: {} degrees, Max Height: {:.2f} meters".format(
        max_height_launch["speed"], max_height_launch["angle"], max_height_launch["max_height"]))
    print("Launches Exceeding Time Limit of {} seconds:".format(time_limit))
    for p in exceeding_time_limit:
        print("Speed: {} m/s, Angle: {} degrees, Flight Time: {:.2f} seconds".format(
            p["speed"], p["angle"], p["flight_time"]))

    # Save projectile data to a text file for the launch with the highest altitude
    save_to_file(max_height_launch["position_data"], 'projectile_highest_altitude.txt')

    # Plot individual trajectories for each projectile
    for p in projectiles:
        plt.plot(p["position_data"][:, 1], p["position_data"][:, 2],
                 label=f'Speed: {p["speed"]} m/s, Angle: {p["angle"]} degrees')

    plt.title('Projectile Motion - Individual Trajectories')
    plt.xlabel('Horizontal Distance (m)')
    plt.ylabel('Vertical Distance (m)')
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # Read data from file
    with open('projectile_data.txt', 'r') as file:
        next(file)  # Skip header line
        projectiles_data = [list(map(float, line.strip().split())) for line in file]

    # Launch projectiles and collect data
    projectiles = [projectile_motion(speed, angle) for speed, angle in projectiles_data]

    # Analyze projectiles
    time_limit = 4
    analyze_projectiles(projectiles, time_limit)



