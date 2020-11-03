import pygame
class Button():
    def __init__(self, x, y, width,height,real_color=(0,0,0),color=(0,0,0),
                hover_color=(0,0,0), press_color=(0,0,0),text=''):
        self.real_color = real_color
        self.color = color #The color that will be drawed
        self.hover_color = hover_color
        self.press_color = press_color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)

        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def is_over(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

    def clicked(self, event, pos):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.is_over(pos):
                return True

    def hovered_over(self, event, pos):
        if event.type == pygame.MOUSEMOTION:
            if self.is_over(pos):
                self.color = self.hover_color
            else:
                self.color = self.real_color

    def change_color(self, event, pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_over(pos):
                self.color = self.hover_color
            else:
                self.color = self.real_color

    def main_loop(self, event, pos):
        self.hovered_over(event, pos)
        self.change_color(event, pos)
        if self.clicked(event, pos):
            return True
