# 🎵 Spotify Playlist Graph

This was a simple weekend project inspired by the graph view in **Obsidian**. The goal was to visualize a Spotify playlist as an interactive floating node graph using Python, `pygame`, and `networkx`.

While I typically lean towards working with CSV files, this project was a conscious effort to step out of my comfort zone and work with **JSON** for both data modeling and rendering.

## 🧠 Project Goals

| Goal                                                             |Progress Bar               |
|------------------------------------------------------------------|---------------------------|
| Mimic Obsidian’s interactive graph style with draggable nodes    | ████████████████████ 100% |
| Use `json` instead of CSV for structured data input              | ████████████████████ 100% |
| Add floating nodes using spring physics                          | ████████████████████ 100% |
| Enable node dragging and reanchoring                             | ████████████████████ 100% |
| Implement zooming and panning                                    | ████████████████████ 100% |


## 🛠️ Features

- Nodes represent **tracks**, **artists**, and **genres** in different colors.
- Nodes float naturally with spring physics and damping.
- Drag nodes to reposition them — they’ll continue floating around their new location.
- Zoom and pan using mouse scroll and drag.
- Edge lines between connected nodes.

## 🎧 How to Try This With Your Own Playlist
You can try this with your own Spotify playlist
1. Go to the Spotify Developer Dashboard and log in.
2. Create a new app and get a client ID and client secret.
3. Input it in to he .env
4. Run playlist.py
5. Run graphyify.py
