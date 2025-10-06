import pyautogui
import time
import numpy as np
import pyperclip
from pynput import keyboard as pynput_keyboard
import threading
import csv
import random


webIcon = r"/Users/nirav/IGFinderBot/IGIconWeb.png"  # Path for IG icon
mapIcon = r"/Users/nirav/IGFinderBot/IGIconMap.png"
csv_path = "/Users/nirav/IGFinderBot/IG Finder - Main.csv"  # Path to your local CSV file
time.sleep(5)

stop_program = False  # Used to stop the script on ESC key press

# Function to listen for ESC keyTint World Tennessee

def on_press(key):
    global stop_program
    if key == pynput_keyboard.Key.esc:
        print("\nESC key pressed. Exiting gracefully...")
        stop_program = True
        return False  # Stop the listener

# Start the listener in a separate thread
listener_thread = threading.Thread(target=lambda: pynput_keyboard.Listener(on_press=on_press).run(), daemon=True)
listener_thread.start()

def get_random_tween():
    tweens = [
        pyautogui.easeInOutQuad,
        pyautogui.easeInOutSine,
        pyautogui.easeInOutCubic,
    ]
    return random.choice(tweens)

def bezier_interp(p0, p1, p2, p3, t):
    return (
        (1 - t)**3 * p0 +
        3 * (1 - t)**2 * t * p1 +
        3 * (1 - t) * t**2 * p2 +
        t**3 * p3
    )

def offset_point(x, y, max_offset=50):
    return (
        x + random.randint(-max_offset, max_offset),
        y + random.randint(-max_offset, max_offset)
    )

def human_move_to(x, y, duration=0.4, steps=25, overshoot_px=random.randint(20, 35), target_jitter=5):
    final_x = x + random.randint(-target_jitter, target_jitter)
    final_y = y + random.randint(-target_jitter, target_jitter)

    start_x, start_y = pyautogui.position()
    ctrl1 = offset_point(start_x, start_y, max_offset=60)
    ctrl2 = offset_point(final_x, final_y, max_offset=60)

    tween = get_random_tween()

    overshoot_x = x + random.randint(-overshoot_px, overshoot_px)
    overshoot_y = y + random.randint(-overshoot_px, overshoot_px)

    delay = duration / steps  # time between steps

    # Step 1: Curve to overshoot target
    for step in range(steps):
        t = tween(step / steps)
        cur_x = bezier_interp(start_x, ctrl1[0], ctrl2[0], overshoot_x, t)
        cur_y = bezier_interp(start_y, ctrl1[1], ctrl2[1], overshoot_y, t)
        pyautogui.moveTo(cur_x, cur_y, _pause=False)
        time.sleep(delay)

    # Step 2: Small pause before adjusting
    time.sleep(random.uniform(0.02, 0.05))

    # Step 3: Quick micro-adjust to final target
    pyautogui.moveTo(x, y, duration=random.uniform(0.03, 0.07), tween=pyautogui.easeOutQuad)

    # Step 4: Micro-pause to simulate human "settling"
    time.sleep(random.uniform(0.02, 0.05))

def random_idle_mouse_move():
    if random.random() < 0.8:
        # Small nearby movement
        current_x, current_y = pyautogui.position()
        move_x = current_x + random.randint(-100, 100)
        move_y = current_y + random.randint(-100, 100)
    else:
        # Occasional full-screen drift
        move_x = random.randint(0, 1920)
        move_y = random.randint(0, 1080)

    human_move_to(move_x, move_y)

# Load data from CSV
with open(csv_path, newline='') as f:
    reader = list(csv.reader(f))

# Ensure at least header + one data row
if len(reader) < 2:
    print("CSV is empty or has no data rows.")
    exit()

# This function extracts Instagram URL and returns result if found
def mapSearchFunction():
    human_move_to(708, 5)
    time.sleep(random.uniform(1, 2))
    human_move_to(407, 111)  # Search bar
    time.sleep(random.uniform(0.5, 1))
    pyautogui.leftClick()
    time.sleep(random.uniform(0.5, 1))
    pyautogui.hotkey('command', 'v')

    time.sleep(random.uniform(0.5, 1))
    pyautogui.press('enter')

    random_idle_mouse_move()
    time.sleep(1)
    human_move_to(1611, 640)  # Scrollbar
    time.sleep(1)

    map_screenshot_region = (0, 789, 2880, 1886)
    map_last_screenshot = pyautogui.screenshot(region=map_screenshot_region)

    while not stop_program:
        try:
            iconLocation = pyautogui.locateOnScreen(mapIcon, confidence=0.9)
            x = iconLocation.left/1.94127303
            y = iconLocation.top/1.94127303  # Move the mouse to the center of the image
            human_move_to(x, y)  # Right-click after moving the mouse
            time.sleep(random.uniform(0.5, 1))
            pyautogui.rightClick()

            time.sleep(random.uniform(0.5, 1))
            for _ in range(5):
                pyautogui.press('down')
            pyautogui.press('enter')
            time.sleep(random.uniform(0.5, 1))
            random_idle_mouse_move()
            time.sleep(5)
            return pyperclip.paste()

        except:
            print("Image not found", end="\r")
            pyautogui.scroll(-10)
            map_new_screenshot = pyautogui.screenshot(region=map_screenshot_region)
            if np.array_equal(np.array(map_last_screenshot), np.array(map_new_screenshot)):
                print("Reached the end of the scrollable area once.")
                return webSearchFunction()
            else:
                map_last_screenshot = map_new_screenshot

def webSearchFunction():
    pyautogui.scroll(1000)
    web_screenshot_region = (0, 789, 2880, 1886)
    web_last_screenshot = pyautogui.screenshot(region=web_screenshot_region)

    while not stop_program:
        try:
            iconLocation = pyautogui.locateOnScreen(webIcon, confidence=0.8)
            x = iconLocation.left/1.82127303
            y = iconLocation.top/1.94127303  # Move the mouse to the center of the image
            human_move_to(x, y)  # Right-click after moving the mouse
            time.sleep(random.uniform(0.5, 1))
            pyautogui.rightClick()

            time.sleep(random.uniform(0.5, 1))
            for _ in range(5):
                pyautogui.press('down')
            pyautogui.press('enter')
            time.sleep(random.uniform(0.5, 1))
            random_idle_mouse_move()
            time.sleep(5)
            return pyperclip.paste()

        except:
            print("Image not found", end="\r")
            pyautogui.scroll(-10)
            web_new_screenshot = pyautogui.screenshot(region=web_screenshot_region)
            if np.array_equal(np.array(web_last_screenshot), np.array(web_new_screenshot)):
                print("Reached the end of the scrollable area once.")
                return None
            else:
                web_last_screenshot = web_new_screenshot

# Process each row
for idx in range(1, len(reader)):
    if stop_program:
        break

    cell = reader[idx][2] if len(reader[idx]) >= 3 else ''
    if not cell.strip():
        print("Empty cell encountered. Stopping.")
        break

    pyperclip.copy(cell)
    result = mapSearchFunction()

    # If result is found, write to the 4th column
    if result:
        while len(reader[idx]) < 4:
            reader[idx].append('')  # Ensure 4th column exists
        reader[idx][3] = result
        print("Result found and written to CSV")
    else:
        # If result is not found, mark the 4th column as "failed"
        while len(reader[idx]) < 4:
            reader[idx].append('')  # Ensure 4th column exists
        reader[idx][3] = "failed"

# Write back updated data
with open(csv_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(reader)

print("Done processing CSV.")
