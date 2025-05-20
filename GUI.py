import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
from matplotlib.text import Text

# Setup for interactive mode
plt.ion()

# Define block colors and shapes
colors = ["red", "green", "blue"]
shapes = ["square", "circle", "triangle"]

# Setup block positions
block_positions = [(x, y) for y in [2, 4, 6] for x in [2, 4, 6]]  # 3x3 grid
blocks = []

# Store selected blocks
your_blocks = []
their_blocks = []

# Store artists to update canvas
block_artists = []
your_block_artists = []
their_block_artists = []

# Logging text area
log_text: Text = None

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.2)
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.set_aspect("equal")
ax.axis("off")


def draw_shape(color, shape, x, y):
    """Draw a black square with a colored shape inside, and return the shape artist"""
    # Draw black square border
    border = Rectangle(
        (x - 0.6, y - 0.6), 1.2, 1.2, edgecolor="black", facecolor="none", linewidth=2
    )
    ax.add_patch(border)

    # Draw the actual shape
    if shape == "square":
        artist = Rectangle((x - 0.4, y - 0.4), 0.8, 0.8, color=color, picker=True)
    elif shape == "circle":
        artist = Circle((x, y), 0.4, color=color, picker=True)
    elif shape == "triangle":
        artist = Polygon(
            [[x, y + 0.45], [x - 0.4, y - 0.35], [x + 0.4, y - 0.35]],
            color=color,
            picker=True,
        )
    else:
        raise ValueError("Unknown shape")

    ax.add_patch(artist)
    return artist


def log(message):
    """Update the text area with a message"""
    log_text.set_text(message)
    fig.canvas.draw_idle()


def update_block_positions():
    """Redraw blocks in the new positions for 'your' and 'their' blocks"""
    # Clear old artists
    for artist in your_block_artists + their_block_artists:
        artist.remove()
    your_block_artists.clear()
    their_block_artists.clear()

    # Redraw your blocks on the left
    for i, block in enumerate(your_blocks):
        x, y = 0.6, 8 - (i * 1.2)
        artist = draw_shape(block["color"], block["shape"], x, y)
        your_block_artists.append(artist)

    # Redraw their blocks on the right
    for i, block in enumerate(their_blocks):
        x, y = 13.5, 8 - i
        artist = draw_shape(block["color"], block["shape"], x, y)
        their_block_artists.append(artist)


def on_pick(event):
    """Handle mouse pick event"""
    artist = event.artist
    for i, block in enumerate(blocks):
        if block["artist"] == artist:
            # Move to your blocks if not already moved
            if block not in your_blocks and block not in their_blocks:
                your_blocks.append(block)
                log(f"You picked: {block['color']} {block['shape']}")
                artist.set_visible(False)
                update_block_positions()
            break


def add_their_block(color, shape):
    """Externally add a block to 'their' blocks"""
    for block in blocks:
        if block["color"] == color and block["shape"] == shape:
            if block not in your_blocks and block not in their_blocks:
                their_blocks.append(block)
                log(f"They picked: {color} {shape}")
                block["artist"].set_visible(False)
                update_block_positions()
            return
    log(f"Block {color} {shape} not found or already chosen")


# Draw all 9 unique blocks
for (color, shape), (x, y) in zip(
    [(c, s) for c in colors for s in shapes], block_positions
):
    artist = draw_shape(color, shape, x, y)
    blocks.append({"color": color, "shape": shape, "artist": artist})

# Draw section labels
ax.text(0.5, 9.5, "Your Blocks", fontsize=12, ha="center")
ax.text(13.5, 9.5, "Their Blocks", fontsize=12, ha="center")

# Add a text box at the bottom for logging
log_text = ax.text(
    7, 0.5, "Click a block to select it.", ha="center", va="center", fontsize=12
)

# Connect event handler
fig.canvas.mpl_connect("pick_event", on_pick)

# Show plot
plt.show(block=True)
