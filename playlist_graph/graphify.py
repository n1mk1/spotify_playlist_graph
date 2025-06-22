import pygame
import json
import networkx as nx
import random

# WINDOW
WIDTH, HEIGHT = 1400, 900
NODE_RADIUS = 12
FONT_SIZE = 14

# Load Graph Data
with open("spotify_playlist_graph.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Setup pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spotify Graph")
font = pygame.font.SysFont(None, FONT_SIZE)
clock = pygame.time.Clock()

# Build graph
G = nx.Graph()
for node in data["nodes"]:
    G.add_node(node["id"], label=node["label"], type=node["type"])
for edge in data["edges"]:
    G.add_edge(edge["source"], edge["target"])

# Layout
layout = nx.spring_layout(G, seed=42, scale=800)
positions = {node_id: [int(x + WIDTH/2), int(y + HEIGHT/2)] for node_id, (x, y) in layout.items()}
original_positions = {node_id: pos[:] for node_id, pos in positions.items()}
velocities = {node_id: [random.uniform(-1, 1), random.uniform(-1, 1)] for node_id in G.nodes}

# Interaction state
dragging_node = None
mouse_drag_offset = (0, 0)
pan_offset = [0, 0]
last_mouse_pos = None
zoom = 1.0

def draw_graph():
    screen.fill((0, 0, 0))  # Spotify black

    # Draw edges
    for edge in G.edges:
        a, b = edge
        ax, ay = transformed_pos(positions[a])
        bx, by = transformed_pos(positions[b])
        pygame.draw.line(screen, (40, 40, 40), (ax, ay), (bx, by), 1)  # gray edges between nodes

    # Draw nodes
    for node_id in G.nodes:
        x, y = transformed_pos(positions[node_id])
        node_type = G.nodes[node_id]["type"]
        
        # Spotify themed node colors
        color = {
            "track": (29, 185, 84),        # Spotify green
            "artist": (179, 179, 179),     # light gray
            "genre": (30, 215, 96),        # lighter green
        }.get(node_type, (255, 255, 255))  # default white

        pygame.draw.circle(screen, color, (int(x), int(y)), NODE_RADIUS)
        
        # label
        label = G.nodes[node_id]["label"]
        text = font.render(label[:20], True, (255, 255, 255))  # white text
        screen.blit(text, (x + 10, y))


def transformed_pos(pos):
    x = pos[0] * zoom + pan_offset[0]
    y = pos[1] * zoom + pan_offset[1]
    return [x, y]

def inverse_transform(x, y):
    gx = (x - pan_offset[0]) / zoom
    gy = (y - pan_offset[1]) / zoom
    return gx, gy

def get_node_under_mouse(mx, my):
    for node_id, (x, y) in positions.items():
        tx, ty = transformed_pos((x, y))
        dist = ((mx - tx)**2 + (my - ty)**2)**0.5
        if dist <= NODE_RADIUS:
            return node_id
    return None

def update_node_positions():
    damping = 0.98
    spring_strength = 0.01
    max_speed = 2.0

    for node_id in G.nodes:
        if node_id == dragging_node:
            continue

        pos = positions[node_id]
        orig = original_positions[node_id]
        vel = velocities[node_id]

        # Spring force
        force_x = (orig[0] - pos[0]) * spring_strength
        force_y = (orig[1] - pos[1]) * spring_strength

        # Apply force
        vel[0] += force_x
        vel[1] += force_y

        # Damping
        vel[0] *= damping
        vel[1] *= damping

        # Clamp velocity
        vel[0] = max(-max_speed, min(max_speed, vel[0]))
        vel[1] = max(-max_speed, min(max_speed, vel[1]))

        # Update position
        pos[0] += vel[0]
        pos[1] += vel[1]

# Main 
running = True
while running:
    screen.fill((0, 0, 0))
    update_node_positions()
    draw_graph()
    pygame.display.flip()
    clock.tick(165)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Zoom
        if event.type == pygame.MOUSEWHEEL:
            zoom += event.y * 0.1
            zoom = max(0.2, min(zoom, 5))

        # Start drag
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                node = get_node_under_mouse(*event.pos)
                if node:
                    dragging_node = node
                    mouse_drag_offset = inverse_transform(*event.pos)
                else:
                    last_mouse_pos = event.pos

        # End drag
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if dragging_node:
                    # Set the new rest position to where the node was dropped
                    original_positions[dragging_node] = positions[dragging_node][:]
                dragging_node = None
                last_mouse_pos = None


        # Dragging funcion
        if event.type == pygame.MOUSEMOTION:
            if dragging_node:
                gx, gy = inverse_transform(*event.pos)
                dx = gx - mouse_drag_offset[0]
                dy = gy - mouse_drag_offset[1]
                positions[dragging_node][0] += dx
                positions[dragging_node][1] += dy
                mouse_drag_offset = (gx, gy)
            elif last_mouse_pos:
                dx = event.pos[0] - last_mouse_pos[0]
                dy = event.pos[1] - last_mouse_pos[1]
                pan_offset[0] += dx
                pan_offset[1] += dy
                last_mouse_pos = event.pos

pygame.quit()
