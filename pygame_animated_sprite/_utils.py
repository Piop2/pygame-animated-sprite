from pygame import Surface


def clip_surface(
    surface: Surface, dest: tuple[int, int], size: tuple[int, int]
) -> Surface:
    handle_surface: Surface = surface.copy()
    handle_surface.set_clip((dest, size))

    return surface.subsurface(handle_surface.get_clip()).copy()
