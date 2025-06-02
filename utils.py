import numpy as np

def distance_3d(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def temporal_overlap(t1, t2, threshold=1.0):
    return abs(t1 - t2) <= threshold

## list based version of interpolate_path
# def interpolate_path(waypoints, time_window):
#     points = []
#     total_time = time_window[1] - time_window[0]
#     steps = len(waypoints) - 1
#     if steps == 0:
#         return [(waypoints[0], time_window[0])]

#     time_step = total_time / steps
#     for i in range(steps):
#         start, end = np.array(waypoints[i]), np.array(waypoints[i+1])
#         for j in range(10):
#             alpha = j / 10
#             pt = (1 - alpha) * start + alpha * end
#             t = time_window[0] + (i + alpha) * time_step
#             points.append((pt.tolist(), round(t, 2)))
    
#     points.append((waypoints[-1], time_window[1])) # include the last waypoint with the end time
#     return points

## numpy version of interpolate_path (faster)
def interpolate_path(waypoints, time_window, steps_per_segment=10):
    waypoints = np.array(waypoints)
    total_time = time_window[1] - time_window[0]
    num_segments = len(waypoints) - 1

    if num_segments == 0:
        return [(waypoints[0].tolist(), time_window[0])]

    time_step = total_time / num_segments
    interpolated = []

    for i in range(num_segments):
        start, end = waypoints[i], waypoints[i + 1]
        alphas = np.linspace(0, 1, steps_per_segment, endpoint=False)
        for alpha in alphas:
            pt = (1 - alpha) * start + alpha * end
            t = time_window[0] + (i + alpha) * time_step
            interpolated.append((pt.tolist(), round(t, 2)))

    return interpolated



