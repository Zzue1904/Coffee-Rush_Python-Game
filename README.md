# Coffee Rush

Coffee Rush is a 2D café-management game made with Python and Pygame-ce.

The player takes the role of a barista and must serve customers before time runs out. Each customer has a different patience level, and the player must collect the correct item and deliver it quickly.

## Features

- Three playable levels with increasing difficulty.
- Three items: Coffee, Tea, and Cake.
- Different customers with unique names, appearances, and patience speeds.
- Three selectable baristas.
- Score system and time limit.
- Customer patience bar.
- Start menu, instructions screen, credits screen, level-complete screen, win screen, and game-over screen.
- Background café ambience and sound effects.

## Controls

| Key | Action |
| --- | --- |
| Arrow Keys / WASD | Move the barista |
| E | Pick up an item or deliver an order |
| 1 / 2 / 3 | Select a barista in the main menu |
| I | Open the instructions screen |
| C | Open the credits screen |
| ESC | Return to the main menu |
| SPACE | Start the game or continue to the next level |
| R | Return to the main menu after losing or winning |

## How to Play

1. Choose a barista from the main menu.
2. Press `SPACE` to start.
3. Check the customer's order at the top of the screen.
4. Move to the correct station and press `E` to pick up Coffee, Tea, or Cake.
5. Move to the customer and press `E` to deliver the order.
6. Complete each level before time runs out.
7. Do not let the customer's patience bar reach zero.

## Levels

| Level | Goal | Time Limit |
| --- | --- | --- |
| Level 1 | 50 points | 60 seconds |
| Level 2 | 70 points | 50 seconds |
| Level 3 | 90 points | 45 seconds |

## Technologies Used

- Python
- Pygame-ce
- PyInstaller

## Installation

Install Pygame-ce:

```bash
python -m pip install pygame-ce

Run the game:

python main.py

Project Structure:

CoffeeRush/
├── main.py
├── README.md
└── assets/
    └── sounds/
        ├── ambience.mp3
        ├── pickup-notification.mp3
        ├── success-notification.mp3
        ├── error-notification.mp3
        ├── win-notification.mp3
        └── game-over-notification.mp3
Credits
Created by: Megan Zurita Medina
Developed with Python and Pygame-ce.