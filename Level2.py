import pygame
from math import cos, sin, pi, atan2

RAY_AMOUNT = 100
SPRITE_BACKGROUND = (152, 0, 136, 255)

wallTextures = {
    '1': pygame.image.load('Sources/Level 2/a.jpg'),
    '2': pygame.image.load('Sources/Level 2/b.png'),
    '3': pygame.image.load('Sources/Level 2/c.jpg'),
    }

enemies = [{"x" : 100,
            "y" : 200,
            "sprite" : pygame.image.load('Sources/Level 2/1.png')},

           {"x" : 350,
            "y" : 150,
            "sprite" : pygame.image.load('Sources/Level 2/2.png')},

            {"x" : 300,
             "y" : 400,
             "sprite" : pygame.image.load('Sources/Level 2/3.png')}
    ]


class Raycaster(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        self.map = []
        self.zbuffer = [float('inf') for z in range(self.width)]

        self.blocksize = 50
        self.wallheight = 50

        self.maxdistance = 300

        self.stepSize = 5
        self.turnSize = 5

        # Primer Cambio
        self.change = {
            'x': -1,
            'y': -1,
            'fov': -1,
            'angle': -1
        }

        self.player = {
           'x' : 100,
           'y' : 100,
           'fov': 60,
           'angle': 0 }

        self.hitEnemy = False

    #Segundo cambio 
    def compareChanges(self):
        return self.player['x'] == self.change['x'] and \
            self.player['y'] == self.change['y'] and \
            self.player['fov'] == self.change['fov'] and \
            self.player['angle'] == self.change['angle']


    def load_map(self, filename):
        with open(filename) as file:
            for line in file.readlines():
                self.map.append( list(line.rstrip()) )

    def drawMinimap(self):
        minimapWidth = 100
        minimapHeight = 100


        minimapSurface = pygame.Surface( (500, 500 ) )
        minimapSurface.fill(pygame.Color("gray"))

        for x in range(0, 500, self.blocksize):
            for y in range(0, 500, self.blocksize):

                i = int(x/self.blocksize)
                j = int(y/self.blocksize)

                if j < len(self.map):
                    if i < len(self.map[j]):
                        if self.map[j][i] != ' ':
                            tex = wallTextures[self.map[j][i]]
                            tex = pygame.transform.scale(tex, (self.blocksize, self.blocksize) )
                            rect = tex.get_rect()
                            rect = rect.move((x,y))
                            minimapSurface.blit(tex, rect)

        rect = (int(self.player['x'] - 4), int(self.player['y']) - 4, 10,10)
        minimapSurface.fill(pygame.Color('black'), rect )

        for enemy in enemies:
            rect = (enemy['x'] - 4, enemy['y'] - 4, 10,10)
            minimapSurface.fill(pygame.Color('red'), rect )

        minimapSurface = pygame.transform.scale(minimapSurface, (minimapWidth,minimapHeight) )
        self.screen.blit(minimapSurface, (self.width - minimapWidth,self.height - minimapHeight))

    def drawSprite(self, obj, size):
        # Pitagoras
        spriteDist = ((self.player['x'] - obj['x']) ** 2 + (self.player['y'] - obj['y']) ** 2) ** 0.5

        # Angulo
        spriteAngle = atan2(obj['y'] - self.player['y'], obj['x'] - self.player['x']) * 180 / pi

        #Tamaño del sprite
        aspectRatio = obj['sprite'].get_width() / obj['sprite'].get_height()
        spriteHeight = (self.height / spriteDist) * size
        spriteWidth = spriteHeight * aspectRatio

        # Buscar el punto inicial para dibujar el sprite
        angleDif = (spriteAngle - self.player['angle']) % 360
        angleDif = (angleDif - 360) if angleDif > 180 else angleDif
        startX = angleDif * self.width / self.player['fov'] 
        startX += (self.width /  2) - (spriteWidth  / 2)
        startY = (self.height /  2) - (spriteHeight / 2)
        startX = int(startX)
        startY = int(startY)

        for x in range(startX, startX + int(spriteWidth)):
            if (0 < x < self.width) and self.zbuffer[x] >= spriteDist:
                for y in range(startY, startY + int(spriteHeight)):
                    tx = int((x - startX) * obj['sprite'].get_width() / spriteWidth )
                    ty = int((y - startY) * obj['sprite'].get_height() / spriteHeight )
                    texColor = obj['sprite'].get_at((tx, ty))
                    if texColor != SPRITE_BACKGROUND and texColor[3] > 128:
                        self.screen.set_at((x,y), texColor)

                        if y == self.height / 2:
                            self.zbuffer[x] = spriteDist
                            if x == self.width / 2:
                                self.hitEnemy = True
                            

    def castRay(self, angle):
        rads = angle * pi / 180
        dist = 0
        stepSize = 1
        stepX = stepSize * cos(rads)
        stepY = stepSize * sin(rads)

        playerPos = (self.player['x'],self.player['y'] )

        x = playerPos[0]
        y = playerPos[1]

        while True:
            dist += stepSize      

            x += stepX
            y += stepY

            i = int(x/self.blocksize)
            j = int(y/self.blocksize)

            if j < len(self.map):
                if i < len(self.map[j]):
                    if self.map[j][i] != ' ':

                        hitX = x - i*self.blocksize
                        hitY = y - j*self.blocksize

                        hit = 0

                        if 1 < hitX < self.blocksize-1:
                            if hitY < 1:
                                hit = self.blocksize - hitX
                            elif hitY >= self.blocksize-1:
                                hit = hitX
                        elif 1 < hitY < self.blocksize-1:
                            if hitX < 1:
                                hit = hitY
                            elif hitX >= self.blocksize-1:
                                hit = self.blocksize - hitY

                        tx = hit / self.blocksize

                        return dist, self.map[j][i], tx


    def render(self):
        halfHeight = int(self.height / 2)

        for column in range(RAY_AMOUNT):
            angle = self.player['angle'] - (self.player['fov'] / 2) + (self.player['fov'] * column / RAY_AMOUNT)
            dist, id, tx = self.castRay(angle)

            rayWidth = int(( 1 / RAY_AMOUNT) * self.width)

            for i in range(rayWidth):
                self.zbuffer[column * rayWidth + i] = dist

            startX = int(( (column / RAY_AMOUNT) * self.width))

            # perceivedHeight = screenHeight / (distance * cos( rayAngle - viewAngle)) * wallHeight
            h = self.height / (dist * cos( (angle - self.player["angle"]) * pi / 180)) * self.wallheight
            startY = int(halfHeight - h/2)
            endY = int(halfHeight + h/2)

            color_k = (1 - min(1, dist / self.maxdistance)) * 255

            tex = wallTextures[id]
            tex = pygame.transform.scale(tex, (tex.get_width() * rayWidth, int(h)))
            tx = int(tx * tex.get_width())
            self.screen.blit(tex, (startX, startY), (tx,0,rayWidth,tex.get_height()))


        self.hitEnemy = False
        for enemy in enemies:
            self.drawSprite(enemy, 50)

        sightRect = (int(self.width / 2 - 2), int(self.height / 2 - 2), 5,5 )
        self.screen.fill(pygame.Color('red') if self.hitEnemy else pygame.Color('white'), sightRect)

        self.drawMinimap()


width = 600
height = 600

class Game2(object):
    def __init__(self, screen, clock, width, height):
        super().__init__()

        self.screen = screen
        self.clock = clock
        self.width = width
        self.height = height

        self.screen = pygame.display.set_mode((width,height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
        self.screen.set_alpha(None)

        self.rCaster = Raycaster(screen)
        self.rCaster.load_map("map 2.txt")
        self.font = pygame.font.SysFont("Arial", 20)

        self.start()


    def updateFPS(self):
        fps = str(int(self.clock.get_fps()))
        fps = self.font.render(fps, 1, pygame.Color("white"))
        return fps

    def start(self):

        isRunning = True
        while isRunning:
            

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    isRunning = False

                elif ev.type == pygame.KEYDOWN:
                    newX = self.rCaster.player['x']
                    newY = self.rCaster.player['y']
                    forward = self.rCaster.player['angle'] * pi / 180
                    right = (self.rCaster.player['angle'] + 90) * pi / 180

                    if ev.key == pygame.K_ESCAPE:
                        isRunning = False
                    elif ev.key == pygame.K_w:
                        newX += cos(forward) * self.rCaster.stepSize
                        newY += sin(forward) * self.rCaster.stepSize
                    elif ev.key == pygame.K_s:
                        newX -= cos(forward) * self.rCaster.stepSize
                        newY -= sin(forward) * self.rCaster.stepSize
                    elif ev.key == pygame.K_a:
                        newX -= cos(right) * self.rCaster.stepSize
                        newY -= sin(right) * self.rCaster.stepSize
                    elif ev.key == pygame.K_d:
                        newX += cos(right) * self.rCaster.stepSize
                        newY += sin(right) * self.rCaster.stepSize
                    elif ev.key == pygame.K_q:
                        self.rCaster.player['angle'] -= self.rCaster.turnSize
                    elif ev.key == pygame.K_e:
                        self.rCaster.player['angle'] += self.rCaster.turnSize

                    i = int(newX/self.rCaster.blocksize)
                    j = int(newY/self.rCaster.blocksize)

                    if self.rCaster.map[j][i] == ' ':
                        self.rCaster.player['x'] = newX
                        self.rCaster.player['y'] = newY

            # Techo
            

            # Piso
            

            if not self.rCaster.compareChanges():
                #Techo
                self.screen.fill(pygame.Color("cyan3"), (0, 0,  width, int(height / 2)))
                #Piso
                self.screen.fill(pygame.Color("darkolivegreen3"), (0, int(height / 2),  width, int(height / 2)))
                self.rCaster.render()

            
            # FPS
            self.screen.fill(pygame.Color("black"), (0, 0, 40, 30))
            self.screen.blit(self.updateFPS(), (0, 0))

            pygame.display.update()
            self.clock.tick(60)