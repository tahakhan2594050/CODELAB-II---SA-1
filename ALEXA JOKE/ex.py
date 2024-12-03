import tkinter as tk
from tkinter import messagebox
import random

# A list of jokes with setups and punchlines
jokes = [
    "Why did the chicken cross the road?To get to the other side.",
    "What happens if you boil a clown?You get a laughing stock.",
    "Why did the car get a flat tire?Because there was a fork in the road!",
    "How did the hipster burn his mouth?He ate his pizza before it was cool.",
    "What did the janitor say when he jumped out of the closet?SUPPLIES!!!!",
    "Why shouldn't you tell secrets in a cornfield?Too many ears.",
    "What do you call a bear with no teeth?A gummy bear!",
    "Why don't scientists trust Atoms?They make up everything.",
    "Why did the developer go broke?Because he used up all his cache.",
]

def get_random_joke():
    """Pick a random joke and split it into setup and punchline."""
    joke = random.choice(jokes)
    setup, punchline = joke.split("?")
    return setup + "?", punchline

def reveal_punchline():
    """Display the punchline one character at a time for a typewriter effect."""
    punchline_label.config(text="")  # Clear any previous punchline
    for i in range(len(current_punchline) + 1):
        root.after(i * 50, lambda text=current_punchline[:i]: punchline_label.config(text=text))

def display_new_joke():
    """Load a new joke onto the screen."""
    global current_punchline
    setup, punchline = get_random_joke()
    joke_label.config(text=setup)  # Show the setup
    punchline_label.config(text="")  # Clear the punchline
    current_punchline = punchline  # Save punchline for later reveal

def confirm_and_quit():
    """Ask the user to confirm before closing the app."""
    if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
        root.destroy()

# Set up the main application window
root = tk.Tk()
root.title("Tell Me a Joke")
root.geometry("600x500")
root.configure(bg="#FFFF99")  # Light yellow background for a cheerful vibe

# Fonts and colors for the UI
setup_font = ("Helvetica Neue", 20, "bold")
punchline_font = ("Helvetica Neue", 18, "italic")
button_font = ("Helvetica Neue", 16)
text_color = "#000000"
button_color = "#CC0000"
hover_color = "#990033"

# Joke setup label
joke_label = tk.Label(
    root, text="", font=setup_font, fg=text_color, bg="#FFFF99", wraplength=550, justify="center"
)
joke_label.pack(pady=20)

# Punchline label
punchline_label = tk.Label(
    root, text="", font=punchline_font, fg=text_color, bg="#FFFF99", wraplength=550, justify="center"
)
punchline_label.pack(pady=20)

# Hover effect for buttons
def on_hover(event):
    event.widget.config(bg=hover_color)

def off_hover(event):
    event.widget.config(bg=button_color)

# Button to reveal the punchline
reveal_button = tk.Button(
    root, text="Reveal Punchline", font=button_font, bg=button_color, fg="white", width=20, command=reveal_punchline
)
reveal_button.pack(pady=10)
reveal_button.bind("<Enter>", on_hover)
reveal_button.bind("<Leave>", off_hover)

# Button to get a new joke
new_joke_button = tk.Button(
    root, text="New Joke", font=button_font, bg=button_color, fg="white", width=20, command=display_new_joke
)
new_joke_button.pack(pady=10)
new_joke_button.bind("<Enter>", on_hover)
new_joke_button.bind("<Leave>", off_hover)

# Button to quit the application
quit_button = tk.Button(
    root, text="Quit", font=button_font, bg=button_color, fg="white", width=20, command=confirm_and_quit
)
quit_button.pack(pady=10)
quit_button.bind("<Enter>", on_hover)
quit_button.bind("<Leave>", off_hover)

# Load the first joke
display_new_joke()

# Start the application loop
root.mainloop()
