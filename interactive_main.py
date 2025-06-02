from mission_loader import load_primary_mission, load_simulated_missions
from conflict_checker import check_conflicts, suggest_resolution
from interactive_visualizer import visualize_4d_conflicts

if __name__ == "__main__":
    primary = load_primary_mission("sample_data/near_miss_but_clear/near_miss_but_clear_primary.json")
    others = load_simulated_missions("sample_data/near_miss_but_clear/near_miss_but_clear_others.json")

    status, conflicts = check_conflicts(primary, others, safety_distance=10)

    print(f"\nMission Status: {status}")
    if conflicts:
        for c in conflicts:
            print(c)

        new_primary = suggest_resolution(primary, conflicts)
        print("\nSuggested Resolution (adjusted path):")
        for wp in new_primary['waypoints']:
            print(wp)
        visualize_4d_conflicts(new_primary, others, conflicts, title="Adjusted Mission with Conflicts")
    else:
        visualize_4d_conflicts(primary, others, [], title="Original Mission (No Conflicts)")
