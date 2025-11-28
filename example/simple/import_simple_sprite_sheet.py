import pygame
from pygame_animated_sprite import AnimatedSprite
from pygame_animated_sprite.loader import SimpleSpriteSheetLoader


pygame.init()

window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("import simple sprite sheet")
clock = pygame.Clock()


encoder = SimpleSpriteSheetLoader(
    columns=1, rows=3, size=(32, 32), position=(1, 13), padding=(1, 0)
)
parappa_animation = AnimatedSprite.load(path="parappa_sheet.png", loader=encoder)

running = True
while running:
    time_delta = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update
    parappa_animation.update(time_delta)

    # render
    window.fill((147, 199, 255))
    window.blit(pygame.transform.scale_by(parappa_animation.render(), 10), (10, 10))

    pygame.display.flip()

pygame.quit()
