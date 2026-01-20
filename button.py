import pygame

class Button:
    def __init__(self, x, y, w, h, text, color, image_path=None):
        self.base_rect = pygame.Rect(x, y, w, h)
        self.rect = self.base_rect.copy()
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, 40)
        self.pressed = False

        self.image = None
        self.hover_image = None
        if image_path:
            try:
                self.image = pygame.image.load(image_path).convert_alpha()
                self.image = pygame.transform.scale(self.image, (w, h))
                self.hover_image = self.image.copy()
                self.hover_image.fill((40, 40, 40, 0), special_flags=pygame.BLEND_RGBA_ADD)
            except:
                self.image = None

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse_pos)

        if self.image:
            screen.blit(self.hover_image if is_hover else self.image, self.rect.topleft)
        else:
            draw_color = self.color
            if is_hover:
                draw_color = tuple(min(c + 40, 255) for c in self.color)
            pygame.draw.rect(screen, draw_color, self.rect, border_radius=20)

        if self.text:
            text_surf = self.font.render(self.text, True, (255, 255, 255))
            screen.blit(text_surf, text_surf.get_rect(center=self.rect.center))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.rect = self.base_rect.inflate(-10, -10)
                self.pressed = True
        if event.type == pygame.MOUSEBUTTONUP and self.pressed:
            self.rect = self.base_rect.copy()
            self.pressed = False
            if self.rect.collidepoint(event.pos):
                return True
        return False
