# PyWeek 36 - Dark Gravity

Topic: **Dark Matter**

Idea: In a 3D space (for 3D pygame, I used my own repo [pygame3D](https://github.com/Hakkush-07/pygame-3D)) full of planets, the player travels with a spaceship. There exists unpredictable gravity due to dark matter! Can you reach your destination in time?

## Run the Game

Install `pygame` and run

```sh
python run_game.py
```

![image](ss.png)

## Objective

You have an objective planet. You need to go near it and press `X` to detect it. Due to dark matter, there exists random gravity so it is not easy to freely move around. After you are done with one planet, another is assigned. You can see the distance to it and height difference. In the middle of the screen, you can see the timer and direction you need to go.

## Controls

- **ESC** -> quits
- **U** -> toggles free/game mode

### In Game Mode
- **WASD** -> applies force
- **TG** -> applies force up or down
- **NM** -> rotates left or right
- **X** -> detects the target planet in front of the player

### In Free Mode
- **WASD** -> changes position
- **TG** -> changes position up or down
- **MOUSE** -> rotates
- **O** -> resets camera rotation in case it is messed up
