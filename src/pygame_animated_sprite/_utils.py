from pygame import Surface, Rect


def clip_surface(surface: Surface, x: int, y: int, x_size: int, y_size: int) -> Surface:
    handle_surface: Surface = surface.copy()
    clip_rect = Rect(x, y, x_size, y_size)
    handle_surface.set_clip(clip_rect)
    image: Surface = surface.subsurface(handle_surface.get_clip())
    return image.copy()
