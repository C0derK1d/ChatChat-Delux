import pygame

pygame.init()

map_img = pygame.image.load("map.png")
map_chunks = {"house": pygame.Rect((320*2, 192*2), (320, 192))}
playspace = map_img.subsurface(map_chunks["house"]).copy() #(156, 96)
#playspace.fill((0,0,0))
d = pygame.display.set_mode((playspace.get_width()*2, playspace.get_height()*2), pygame.RESIZABLE)
pygame.display.set_caption("ChatChat // DELUX //")
sur = pygame.Surface((32,32))
sur.fill((0,255,0))
pygame.display.set_icon(sur)
playing = True
start_x = 0
tick = 0
#globalFont = pygame.font.Font("fixedsys.fon", 260)
globalFont = pygame.font.SysFont("Courier New", 12, bold=True, italic=False)

class MapComponent(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image = pygame.Surface((50,50)) #texture
        
        self.x = pos[0]
        self.y = pos[1]
        self.rect = self.image.get_rect()

    def show(self):
        self.rect = playspace.blit(self.image, (self.x + start_x, self.y))

class Wall(MapComponent):
    def __init__(self, pos):
        MapComponent.__init__(self, pos)

class Character(pygame.sprite.Sprite):
    def __init__(self, name : str):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image = pygame.Surface((16,16)) #texture
        self.image.fill((0, 0, 255))

        self.up = pygame.K_UP
        self.down = pygame.K_DOWN
        self.left = pygame.K_LEFT
        self.right = pygame.K_RIGHT

        self.rect = self.image.get_rect()
        
        self.x = 160
        self.prevX = 0
        self.nameX = self.rect.centerx - (len(self.name) * 5)
        self.y = 128
        self.prevY = 0

    def onUpdate(self):
        self.move()
        self.show()

    def action(self):
        pass

    def move(self):
        if tick % 3 == 0:
            keys = pygame.key.get_pressed()
            if not self.rect.collidepoint((self.rect.topleft[0], 0)):
                if keys[self.up]: self.y -= 16
            if not self.rect.collidepoint((self.rect.bottomleft[0], playspace.get_height()-16)):
                if keys[self.down]: self.y += 16
            if not self.rect.collidepoint((start_x, self.rect.topleft[1])):
                if keys[self.left]: self.x -= 16
            if not self.rect.collidepoint((start_x+playspace.get_width()-4, self.rect.topright[1])):
                if keys[self.right]: self.x += 16
        

    def show(self):
        self.rect = playspace.blit(self.image, (self.x + start_x, self.y))
        self.nameX = self.rect.centerx - (len(self.name) *3.5)
        playspace.blit(globalFont.render(self.name, True, (255,255,255)), (self.nameX, self.y-12))
    
class Dog(Character):
    def __init__(self,name : str):
        Character.__init__(self, name)
        self.image.fill((100, 0, 0))
        
class Cat(Character):
    def __init__(self,name : str):
        Character.__init__(self, name)
        self.image.fill((0, 255, 0))

        self.up = pygame.K_UP
        self.down = pygame.K_DOWN
        self.left = pygame.K_LEFT
        self.right = pygame.K_RIGHT

class Component(pygame.sprite.Sprite):
    def __init__(self, text : str, pos, size, color, fixed=True):
        pygame.sprite.Sprite.__init__(self)

        self.x = pos[0]
        self.y = pos[1]
        self.text = text
        self.isFixed = fixed
        self.image = pygame.Surface(size) #texture
        self.image.fill(color)
        self.hoverSurf = pygame.Surface(size)
        self.hoverSurf.fill((min(color[0] - 50, 255), min(color[1] - 50, 255), min(color[2] - 50,255)))
        self.hovering = False

        self.clicking = False
        self.rect = self.image.get_rect()

    def onUpdate(self):
        self.show()
        m = pygame.mouse.get_pos()
        size = self.image.get_size()
        if m[0] <= self.x+size[0] and m[0] >= self.x and m[1] <= self.y + size[1] and m[1] >= self.y:
            self.onHover()
            self.hovering = True
            if pygame.mouse.get_pressed()[0]:
                self.clicking = True
            if not pygame.mouse.get_pressed()[0] and self.clicking:
                self.clicking = False
                self.onClick()
        else: self.hovering = False

    def onHover(self):
        pass

    def onClick(self):
        pass

    def show(self):
        if self.hovering: self.rect = d.blit(self.hoverSurf, (self.x, self.y))
        else: self.rect = d.blit(self.image, (self.x, self.y))
        d.blit(globalFont.render(self.text, True, (0,0,0)), (self.x, self.y))

class Input(Component):

    def __init__(self, text : str, pos, size, color, fixed=True):
        Component.__init__(self, text, pos, size, color)

        self.typeing = False
        self.text = ""
        
    def onClick(self):
        self.typeing = not self.typeing
        if self.typeing: pygame.key.start_text_input()
        else: pygame.key.stop_text_input()
        print("I am clicked: "+str(self.typeing))

    def onUpdate(self):
        Component.onUpdate(self)

        for event in pygame.event.get(eventtype=pygame.TEXTINPUT): self.onTypeing(event.text)

    def onTypeing(self, key):
        if self.typeing: self.text += key

me = Cat("Csacsi")
#notme = Dog("Someone else")

chat_input = Input("Itt lesz majd a chat", (playspace.get_width()*2, playspace.get_height()*2), (1000,50), (255,255,255))

while playing:
    #playspace.fill((0,0,0))
    playspace = map_img.subsurface(map_chunks["house"]).copy()
    for event in pygame.event.get(eventtype=pygame.QUIT): playing = False
        #if event.type == pygame.VIDEORESIZE:
        #    size = pygame.display.get_surface().get_size()
        #    start_x = int(size[0]/2-360)
    me.onUpdate()
    #fov = playspace.subsurface(pygame.Rect((max(me.x-80, 0), max(me.y-48, 0)), (160, 96)))
    posx = min(max(me.rect.centerx-80, 8), 152)
    posy = min(max(me.rect.centery-48, 8), 88)
    fov_rect = pygame.Rect((posx, posy), (160, 96))
    print(fov_rect)
    fov = playspace.subsurface(fov_rect)
    #notme.onUpdate()
    chat_input.onUpdate()
    tick +=1
    pygame.display.update()
    pygame.time.Clock().tick(60)
    resized_playspace = pygame.transform.scale(fov, (320*2, 192*2))
    d.fill((0,0,100))
    d.blit(resized_playspace, (start_x,0))
    #d.blit(playspace, (start_x,0))

print("Bye!")