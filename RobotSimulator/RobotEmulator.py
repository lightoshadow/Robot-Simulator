import pygame
import math
import re

pygame.init()

screen = pygame.display.set_mode((480,480))

RobotSprite = pygame.image.load('RobotSprite.png')
RobotSpriteX = 224
RobotSpriteY = 224
RobotSpriteRotation = 0

pygame.display.set_caption("Robot Emulator")
icon = RobotSprite
pygame.display.set_icon(icon)

global move_upwards_
move_upwards_ = pygame.USEREVENT + 1
global rotate_
rotate_ = pygame.USEREVENT + 2
global writecode_
writecode_ = pygame.USEREVENT + 3
global endwritingcode_
endwritingcode_ = pygame.USEREVENT + 4
global readcode_
readcode_ = pygame.USEREVENT + 5
global help_
help_ = pygame.USEREVENT + 6

global codelines
codelines = []

global expression
expression = '(.*)\((.*)\)$'
Compexpression = re.compile(expression)


class Robot(object):
    def __init__(self):
        self.img = RobotSprite
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.x = 224//2
        self.y = 224//2
        self.angle = 0
        self.rotatedSurf = pygame.transform.rotate(self.img,self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x,self.y)
        self.cosine = math.cos(math.radians(self.angle))
        self.sine = math.sin(math.radians(self.angle))

    def moveup(self, distance):    
        self.x += self.cosine * int(distance)
        self.y -= self.sine * int(distance)
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians (self.angle + 90))
        
    def turn(self, degrees):
        self.angle += (int(degrees) * -1)
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians (self.angle + 90))

    def draw(self, screen):
        screen.blit(self.rotatedSurf,self.rotatedRect) 

def writecode(data):
    codelines.append(data)

def endwritingcode(file):
    with open(file, "w") as f:
        for line in codelines:
            f.write(line+"\n")
    f.close()

def readcode(file):
    f = open(file,"r")
    lines = f.readlines()
    for line in lines:
        group=Compexpression.search(line)
        global value
        (instruction,value)=(group[1],group[2])        
        if instruction == 'move':
            print("move")
            #pygame.event.post(pygame.event.Event(move_upwards))
            robot.moveup(value)
        if instruction == 'rotate':
            print("rotate")
            #pygame.event.post(pygame.event.Event(rotate_))
            robot.turn(value)
        
        print(":{}, :{}".format(instruction,value))
    f.close()
    #robot.moveup(1)


def newinputhandler():
    inputcommand = input('>>>>')
    try:
        group=Compexpression.search(inputcommand)
        global value
        (instruction,value)=(group[1],group[2])
        if instruction == 'quit' and value=="":
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        else:
            if instruction == 'move':
                if writeCode == True:
                    writecode(inputcommand)
                pygame.event.post(pygame.event.Event(move_upwards_))
            if instruction == 'rotate':
                if writeCode == True:
                    writecode(inputcommand)
                pygame.event.post(pygame.event.Event(rotate_))
            if instruction == 'startwriting' and value == '':
                pygame.event.post(pygame.event.Event(writecode_))
            if instruction == 'endwriting':
                pygame.event.post(pygame.event.Event(endwritingcode_))
            if instruction == 'read':
                pygame.event.post(pygame.event.Event(readcode_))
            if (instruction == "help"):
                help()
    except:
        print("Syntax Error")

def help():
    print("""Commands you can use:
    move(distance) - it makes robot move forwards/backwards
    rotate(degrees) - it makes robot rotate clockwise/counterclockwise
    startwriting() - remembers commands you enter from now on
    endwriting(file) - writes commands remembred
    read(file) - reads commands written in a file""")

robot = Robot()
running = True
writeCode = False
robot.moveup(1)
print("type help() for help")
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False    
        if event.type == move_upwards_:
            if RobotSpriteX > 0:
                robot.moveup(value)
        if event.type == rotate_:
            robot.turn(value)
        if event.type == writecode_:
            writeCode = True
        if event.type == endwritingcode_:
            writeCode = False
            endwritingcode(str(value))
        if event.type == readcode_:
            readcode(value)
        if event.type == help_:
            help()

    screen.fill((255,255,255))

    robot.draw(screen)

    pygame.display.update()

    newinputhandler()  