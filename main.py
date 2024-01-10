import tkinter as tk
from tkinter import Text, Scrollbar
import os
import webbrowser
import json
import threading
import http.server
import socketserver

# Your imports from file_parser, command_generator, and models
from file_parser import read_path_from_file
from command_generator import generate_commands
from models import Point, LineSegment, Arc

PORT = 8000
server_thread = None
browser_opened = False

def start_server():
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Serving at port", PORT)
        httpd.serve_forever()

def regenerate_data():
    filename = "path_file.txt"
    path = read_path_from_file(filename)
    commands = generate_commands(path)

    data = {
        "path": [
            {"type": "line", "start": [segment.start.x, segment.start.y], "end": [segment.end.x, segment.end.y]} if isinstance(segment, LineSegment) else 
            {"type": "arc", "center": [segment.center.x, segment.center.y], "radius": segment.radius, "start_angle": segment.start_angle, "end_angle": segment.end_angle} for segment in path
        ],
        "commands": commands
    }

    with open('cnc_data.json', 'w') as f:
        json.dump(data, f, indent=4)

    print("Data regenerated.")

def open_simulation():
    global server_thread, browser_opened
    url = f'http://localhost:{PORT}/simulation.html'

    regenerate_data()  # Regenerate data before opening the simulation
    
    if server_thread is None or not server_thread.is_alive():
        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()
        print("Server started")
    else:
        print("Server already running")
    
    if not browser_opened:
        webbrowser.open(url)
        browser_opened = True
    else:
        webbrowser.open(url, new=0, autoraise=True)

def save_path_and_generate_commands(input_text):
    content = input_text.get("1.0", "end-1c")
    with open('path_file.txt', 'w') as file:
        file.write(content)

    filename = "path_file.txt"
    path = read_path_from_file(filename)
    commands = generate_commands(path)

    data = {
        "path": [
            {"type": "line", "start": [segment.start.x, segment.start.y], "end": [segment.end.x, segment.end.y]} if isinstance(segment, LineSegment) else 
            {"type": "arc", "center": [segment.center.x, segment.center.y], "radius": segment.radius, "start_angle": segment.start_angle, "end_angle": segment.end_angle} for segment in path
        ],
        "commands": commands
    }

    with open('cnc_data.json', 'w') as f:
        json.dump(data, f, indent=4)

    print("Path saved and commands generated.")

def load_last_text():
    try:
        with open('path_file.txt', 'r') as file:
            return file.read()
    except FileNotFoundError:
        return ""

def sync_scroll(input_txt, line_num_txt, *args):
    line_num_txt.yview(*args)
    input_txt.yview(*args)

def update_line_numbers(input_txt, line_num_txt):
    line_num_txt.configure(state='normal')
    line_num_txt.delete('1.0', 'end')
    number_of_lines = int(input_txt.index('end-1c').split('.')[0])
    line_number_string = "\n".join(str(i) for i in range(1, number_of_lines + 1))
    line_num_txt.insert('1.0', line_number_string)
    line_num_txt.configure(state='disabled')
    
    # Dynamically adjust the width of the line number column
    max_width = len(str(number_of_lines))
    line_num_txt.configure(width=max_width)

def setup_gui():
    root = tk.Tk()
    root.title("CNC Machine")

    # Create a scrollbar
    scrollbar = tk.Scrollbar(root)
    scrollbar.grid(row=0, column=2, sticky='ns')

    # Create the line number Text widget
    line_numbers = Text(root, width=5, padx=3, takefocus=0, border=0, background='lightgray', state='disabled', wrap='none')
    line_numbers.grid(row=0, column=0, sticky='nsew')

    # Create the main Text widget
    input_text = Text(root, height=10, yscrollcommand=scrollbar.set)
    input_text.grid(row=0, column=1, sticky="nsew")
    input_text.insert('1.0', load_last_text())
    input_text.bind("<KeyPress>", lambda e: update_line_numbers(input_text, line_numbers))
    input_text.bind("<KeyRelease>", lambda e: update_line_numbers(input_text, line_numbers))

    # Configure the scrollbar to scroll both Text widgets
    scrollbar.config(command=lambda *args: sync_scroll(input_text, line_numbers, *args))
    input_text.config(yscrollcommand=scrollbar.set)

    # Call update_line_numbers to ensure the line numbers are correct on program start
    update_line_numbers(input_text, line_numbers)

    # Configure column weights to ensure buttons have equal width
    root.grid_columnconfigure(0, weight=0)  # Line numbers
    root.grid_columnconfigure(1, weight=1)  # Main text widget
    root.grid_rowconfigure(0, weight=1)

    create_widgets(root, input_text, line_numbers)

    return root

def create_widgets(root, input_text, line_numbers):
    # Configure button row
    button_frame = tk.Frame(root)
    button_frame.grid(row=1, column=0, columnspan=3, sticky='ew')
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)

    # Create the buttons within the button frame
    save_btn = tk.Button(button_frame, text="Save Path", padx=10, pady=5, fg="white", bg="#263D42", command=lambda: save_path_and_generate_commands(input_text))
    save_btn.grid(row=0, column=0, sticky="ew")

    open_btn = tk.Button(button_frame, text="Open Simulation", padx=10, pady=5, fg="white", bg="#263D42", command=open_simulation)
    open_btn.grid(row=0, column=1, sticky="ew")

def main():
    root = setup_gui()
    root.mainloop()

if __name__ == "__main__":
    main()
