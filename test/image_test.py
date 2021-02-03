from sense_hat import SenseHat

sense = SenseHat()

# Define some colours
r = (255, 0, 0) # Red
g = (0, 255, 0) # Green
bu = (0, 0, 255) # Blue
b = (0, 0, 0) # Black

# Set up where each colour will display
creeper_pixels = [
    g, g, g, g, g, g, g, g,
    g, g, g, g, g, g, g, g,
    g, b, b, g, g, b, b, g,
    g, b, b, g, g, b, b, g,
    g, g, g, b, b, g, g, g,
    g, g, b, b, b, b, g, g,
    g, g, b, b, b, b, g, g,
    g, g, b, g, g, b, g, g
]

# Display these colours on the LED matrix
sense.set_pixels(creeper_pixels)
