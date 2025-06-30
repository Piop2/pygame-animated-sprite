from pygame import Surface, Rect


def clip_surface(surface: Surface, x: int, y: int, x_size: int, y_size: int) -> Surface:
    handle_surface: Surface = surface.copy()
    handle_surface.set_clip(((x, y), (x_size, y_size)))

    return surface.subsurface(handle_surface.get_clip()).copy()
