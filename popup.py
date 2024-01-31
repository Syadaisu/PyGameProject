import pygame

class Popup:
    def __init__(self, width, height, message, font_size=32):
        self.width = width
        self.height = height
        self.message = message
        self.font_size = font_size
        self.surface = pygame.Surface((width, height))
        self.font = pygame.font.Font(None, font_size)

    def render(self):
        self.surface.fill((255, 255, 255))  # Fill the surface with white

        # Split the text into words
        words = self.message.split(' ')
        lines = ['']
        line_index = 0

        # Add the words to the lines
        for word in words:
            # Add a space before the word if the line is not empty
            temp_line = lines[line_index] + (' ' if lines[line_index] else '') + word
            temp_surface = self.font.render(temp_line, True, (0, 0, 0))
            if temp_surface.get_width() > self.surface.get_width() - 20:  # Leave a 10 pixel margin on both sides
                lines.append(word)
                line_index += 1
            else:
                lines[line_index] = temp_line

        # Render the lines onto the popup surface
        for i, line in enumerate(lines):
            text_surface = self.font.render(line, True, (0, 0, 0))
            self.surface.blit(text_surface, (10, 10 + i * self.font_size))  # Adjust the y position for each line

        return self.surface