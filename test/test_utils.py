import numpy as np
from flyt_deconfliction.utils import interpolate_path

def print_path(points):
    for pt, t in points:
        print(f"Point: {np.round(pt, 2)}, Time: {t}")

def test_interpolate_path():
    print("Test 1: Two waypoints, 0 to 10")
    waypoints = [[0, 0, 0], [10, 0, 0]]
    time_window = (0, 10)
    points = interpolate_path(waypoints, time_window)
    print_path(points)
    assert np.allclose(points[0][0], waypoints[0])
    assert np.allclose(points[-1][0], waypoints[-1])
    assert points[0][1] == time_window[0]
    assert points[-1][1] == time_window[1]
    print("Passed\n")

    print("Test 2: Three waypoints, 0 to 20")
    waypoints = [[0, 0, 0], [10, 10, 0], [20, 0, 0]]
    time_window = (0, 20)
    points = interpolate_path(waypoints, time_window)
    print_path(points)
    assert np.allclose(points[0][0], waypoints[0])
    assert np.allclose(points[-1][0], waypoints[-1])
    assert points[0][1] == time_window[0]
    assert points[-1][1] == time_window[1]
    print("Passed\n")

    print("Test 3: Single waypoint")
    waypoints = [[1, 2, 3]]
    time_window = (5, 5)
    points = interpolate_path(waypoints, time_window)
    print_path(points)
    assert len(points) == 1
    assert np.allclose(points[0][0], waypoints[0])
    assert points[0][1] == time_window[0]
    print("Passed\n")

if __name__ == "__main__":
    test_interpolate_path()
