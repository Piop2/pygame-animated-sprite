# Pygame Animated Sprite
> Animated sprite package for pygame

## Install

```sh
pip install git+https://github.com/Piop2/pygame-animated-sprite.git@main
```

## Usage

```python
import pygame
from pygame_animated_sprite import AnimatedSprite

pygame.init()

window = pygame.display.set_mode((100, 500))
clock = pygame.time.Clock()

surfaces = [...]  # list of Surface objects for animation frames
durations = [...] # list of durations for each frame (ms)

sprite = AnimatedSprite.from_surfaces(
    surfaces,
    durations,
)

running = True
while running:
    # Handle events here
    ...

    time_delta = clock.tick(60)
    sprite.update(time_delta)
    ...
    
    sprite.draw(window, (0, 0))
    pygame.display.flip()
```
