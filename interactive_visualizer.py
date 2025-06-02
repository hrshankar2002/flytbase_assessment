import plotly.graph_objects as go
from utils import interpolate_path

def visualize_4d_conflicts(primary, others, conflicts, title="4D Conflict Visualization"):
    fig = go.Figure()

    def add_trace(path, label, color):
        xs, ys, zs, ts = zip(*[(p[0], p[1], p[2], t) for p, t in path])
        fig.add_trace(go.Scatter3d(
            x=xs, y=ys, z=zs, mode='lines+markers',
            marker=dict(size=4),
            line=dict(width=3),
            name=label,
            text=[f"t={t}" for t in ts],
            hoverinfo='text'
        ))

    primary_interp = interpolate_path(primary["waypoints"], primary["time_window"])
    add_trace(primary_interp, "Primary Drone", "blue")

    for drone in others:
        drone_interp = interpolate_path(drone["waypoints"], drone["time_window"])
        add_trace(drone_interp, f"Drone {drone['id']}", "gray")

    for conflict in conflicts:
        x, y, z = conflict["location"]
        fig.add_trace(go.Scatter3d(
            x=[x], y=[y], z=[z],
            mode='markers+text',
            marker=dict(size=6, color='red'),
            text=[f"Conflict@{conflict['time']}s"],
            name='Conflict'
        ))

    fig.update_layout(
        scene=dict(
            xaxis_title='X', yaxis_title='Y', zaxis_title='Z',
            aspectmode='cube'
        ),
        title=title,
        margin=dict(l=0, r=0, b=0, t=40)
    )
    fig.show()
