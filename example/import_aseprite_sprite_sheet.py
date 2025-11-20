import pygame
from pygame_animated_sprite import AnimatedSprite
from pygame_animated_sprite.loader.aseprite import AsepriteBaseSpriteSheetEncoder


pygame.init()

window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("import aseprite sprite sheet")
clock = pygame.Clock()


encoder = AsepriteBaseSpriteSheetEncoder(json_format="hash")
mario_animation = AnimatedSprite.load(path="./mario.json", loader=encoder)

running = True
while running:
    time_delta = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update
    mario_animation.update(time_delta)

    # render
    window.fill("black")
    window.blit(pygame.transform.scale_by(mario_animation.render(), 10), (10, 10))

    pygame.display.flip()

pygame.quit()
