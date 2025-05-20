import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
from matplotlib.text import Text


class GUI:

    def __init__(self):

        # Setup for interactive mode
        plt.ion()

        # Define block colors and shapes
        self.colors = ["red", "green", "blue"]
        self.shapes = ["square", "circle", "triangle"]

        # Setup block positions
        self.block_positions = [
            (x, y) for y in [2, 4, 6] for x in [2, 4, 6]
        ]  # 3x3 grid
        self.blocks = []

        # Store selected blocks
        self.your_blocks = []
        self.their_blocks = []

        # Store artists to update canvas
        self.block_artists = []
        self.your_block_artists = []
        self.their_block_artists = []

        # Logging text area
        self.log_text: Text = None

        # Create figure
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        plt.subplots_adjust(bottom=0.2)
        self.ax.set_xlim(0, 14)
        self.ax.set_ylim(0, 10)
        self.ax.set_aspect("equal")
        self.ax.axis("off")

    def draw_shape(self, color, shape, x, y):
        """Draw a black square with a colored shape inside, and return the shape artist"""
        # Draw black square border
        border = Rectangle(
            (x - 0.6, y - 0.6),
            1.2,
            1.2,
            edgecolor="black",
            facecolor="none",
            linewidth=2,
        )
        self.ax.add_patch(border)

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

        self.ax.add_patch(artist)
        return artist

    def log(self, message):
        """Update the text area with a message"""
        self.log_text.set_text(message)
        self.fig.canvas.draw_idle()

    def update_block_positions(self):
        """Redraw blocks in the new positions for 'your' and 'their' blocks"""
        # Clear old artists
        for artist in self.your_block_artists + self.their_block_artists:
            artist.remove()
        self.your_block_artists.clear()
        self.their_block_artists.clear()

        # Redraw your blocks on the left
        for i, block in enumerate(self.your_blocks):
            x, y = 0.6, 8 - (i * 1.2)
            artist = self.draw_shape(block["color"], block["shape"], x, y)
            self.your_block_artists.append(artist)

        # Redraw their blocks on the right
        for i, block in enumerate(self.their_blocks):
            x, y = 13.5, 8 - i
            artist = self.draw_shape(block["color"], block["shape"], x, y)
            self.their_block_artists.append(artist)

    def on_pick(self, event):
        """Handle mouse pick event"""
        artist = event.artist
        for i, block in enumerate(self.blocks):
            if block["artist"] == artist:
                # Move to your blocks if not already moved
                if block not in self.your_blocks and block not in self.their_blocks:
                    self.your_blocks.append(block)
                    self.log(f"You picked: {block['color']} {block['shape']}")
                    artist.set_visible(False)
                    self.update_block_positions()
                break

    def add_their_block(self, color, shape):
        """Externally add a block to 'their' blocks"""
        for block in self.blocks:
            if block["color"] == color and block["shape"] == shape:
                if block not in self.your_blocks and block not in self.their_blocks:
                    self.their_blocks.append(block)
                    self.log(f"They picked: {color} {shape}")
                    block["artist"].set_visible(False)
                    self.update_block_positions()
                return
        self.log(f"Block {color} {shape} not found or already chosen")

    def main(self, init_only=False):
        # Draw all 9 unique blocks
        for (color, shape), (x, y) in zip(
            [(c, s) for c in self.colors for s in self.shapes], self.block_positions
        ):
            artist = self.draw_shape(color, shape, x, y)
            self.blocks.append({"color": color, "shape": shape, "artist": artist})

        # Draw section labels
        self.ax.text(0.5, 9.5, "Your Blocks", fontsize=12, ha="center")
        self.ax.text(13.5, 9.5, "Their Blocks", fontsize=12, ha="center")

        # Add a text box at the bottom for logging
        self.log_text = self.ax.text(
            7, 0.5, "Click a block to select it.", ha="center", va="center", fontsize=12
        )

        # Connect event handler
        self.fig.canvas.mpl_connect("pick_event", self.on_pick)

        if not init_only:
            plt.show(block=True)


if __name__ == "__main__":
    gui = GUI()
    gui.main()
