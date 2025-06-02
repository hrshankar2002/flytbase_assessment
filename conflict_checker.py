from utils import distance_3d, interpolate_path, temporal_overlap
from scipy.spatial import KDTree

# m = number of interpolated points for the primary drone
# n = number of other drones
# k = average number of interpolated points per other drone
# N = n * k = total number of points in the KD-Tree
# r = average number of spatial neighbors found per query
# w = number of waypoints in the primary drone
# c = number of conflicts

### CONFLICT CHECKER
## O(m*n*k) time complexity (conflict check without spatial indexing)
# def check_conflicts(primary, others, safety_distance):
#     conflicts = []
#     status = "clear"
#     primary_interp = interpolate_path(primary["waypoints"], primary["time_window"])

#     for drone in others:
#         drone_interp = interpolate_path(drone["waypoints"], drone["time_window"])
#         for (pt1, t1) in primary_interp:
#             for (pt2, t2) in drone_interp:
#                 if temporal_overlap(t1, t2) and distance_3d(pt1, pt2) < safety_distance:
#                     status = "conflict detected"
#                     conflicts.append({
#                         "time": t1,
#                         "location": pt1,
#                         "conflict_with": drone["id"],
#                         "distance": distance_3d(pt1, pt2)
#                     })
#                     break
#     return status, conflicts

## O(m*(log(n*k)+r)) time complexity (conflict check with spatial indexing)
def check_conflicts(primary, others, safety_distance):
    conflicts = []  # O(1)
    status = "clear"  # O(1)
    primary_interp = interpolate_path(primary["waypoints"], primary["time_window"])  # O(m)

    # Gather all other drones' points, times, and IDs
    other_points = []  # O(1)
    other_times = []   # O(1)
    other_ids = []     # O(1)
    for drone in others:  # O(n)
        drone_interp = interpolate_path(drone["waypoints"], drone["time_window"])  # O(k) per drone
        for (pt, t) in drone_interp:  # O(k) per drone
            other_points.append(pt)  # O(1)
            other_times.append(t)    # O(1)
            other_ids.append(drone["id"])  # O(1)
    # Total for above: O(n * k)

    tree = KDTree(other_points)  # O(N * log N), N = n * k

    for (pt1, t1) in primary_interp:  # O(m)
        idxs = tree.query_ball_point(pt1, safety_distance)  # O(log N + r) per query
        for idx in idxs:  # O(r) per primary point
            t2 = other_times[idx]  # O(1)
            if temporal_overlap(t1, t2):  # O(1)
                status = "conflict detected"  # O(1)
                conflicts.append({           # O(1)
                    "time": t1,
                    "location": pt1,
                    "conflict_with": other_ids[idx],
                    "distance": distance_3d(pt1, other_points[idx])
                })
                break  # O(1)
    # Total: O(m * (log N + r))
    return status, conflicts  # O(1)

### SUGGEST RESOLUTION
## O(w*c) time complexity (suggest resolution)
# def suggest_resolution(primary, conflicts, z_offset=10):
#     adjusted = primary.copy()
#     adjusted["waypoints"] = []
#     for wp in primary["waypoints"]:
#         in_conflict = any(distance_3d(wp, c["location"]) < 5 for c in conflicts)
#         if in_conflict:
#             new_wp = [wp[0], wp[1], wp[2] + z_offset]
#         else:
#             new_wp = wp
#         adjusted["waypoints"].append(new_wp)
#     return adjusted

## O(w*(log(c)+r)) time complexity (suggest resolution)
def suggest_resolution(primary, conflicts, buffer_zone=5, z_offset=10):
    adjusted = primary.copy()  # O(1)
    adjusted["waypoints"] = []  # O(1)
    if conflicts:
        conflict_points = [c["location"] for c in conflicts]  # O(c)
        tree = KDTree(conflict_points)  # O(c * log c)
        for wp in primary["waypoints"]:  # O(w)
            idxs = tree.query_ball_point(wp, buffer_zone)  # O(log c + r') per query, r' = spatial neighbors per wp
            in_conflict = len(idxs) > 0  # O(1)
            if in_conflict:
                new_wp = [wp[0], wp[1], wp[2] + z_offset]  # O(1)
            else:
                new_wp = wp  # O(1)
            adjusted["waypoints"].append(new_wp)  # O(1)
        # Total: O(w * (log c + r'))
    else:
        adjusted["waypoints"] = primary["waypoints"][:]  # O(w)
    return adjusted  # O(1)
