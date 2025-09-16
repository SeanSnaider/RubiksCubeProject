from PIL import Image, ImageDraw
import random
import pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
BACKGROUND_COLOR = (0, 34, 51)
TEXT_COLOR = (255, 255, 255)
TEXT_BG_COLOR = (0, 0, 0, 180)  # RGBA with alpha for semi-transparency

class RubiksCube:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Rubik's Cube Simulator")
        self.clock = pygame.time.Clock()
        
        # Font initialization for text display
        self.font = pygame.font.SysFont('Arial', 16)
        self.big_font = pygame.font.SysFont('Arial', 20, bold=True)
        
        # self state variables
        self.text1 = ""
        self.stepsComp = 0
        self.stepHelp = 0
        self.display_text = []  # List to store text that will be displayed on screen
        self.bx = 250
        self.by = 50
        self.stepsPerSecond = 0
        self.boardleft = 125
        self.boardtop = 75
        self.cellWidth = 25
        self.cellHeight = 25
        self.rows = 3
        self.cols = 3
        self.cellborderwidth = 2
        self.cubeRows = 3
        self.cubeCols = 3
        self.colors = {
            'white': (255, 255, 255),
            'orange': (255, 165, 0),
            'green': (0, 255, 0),
            'red': (255, 0, 0),
            'blue': (0, 0, 255),
            'yellow': (255, 255, 0)
        }
        self.U = [[None for _ in range(self.cubeRows)] for _ in range(self.cubeCols)]
        self.L = [[None for _ in range(self.cubeRows)] for _ in range(self.cubeCols)]
        self.F = [[None for _ in range(self.cubeRows)] for _ in range(self.cubeCols)]
        self.R = [[None for _ in range(self.cubeRows)] for _ in range(self.cubeCols)]
        self.B = [[None for _ in range(self.cubeRows)] for _ in range(self.cubeCols)]
        self.D = [[None for _ in range(self.cubeRows)] for _ in range(self.cubeCols)]
        self.timePassed = -1
        self.resetCube()
        
    def resetCube(self):
        self.U = [['white'] * 3 for row in range(3)]
        self.L = [['orange'] * 3 for row in range(3)]
        self.F = [['green'] * 3 for row in range(3)]
        self.R = [['red'] * 3 for row in range(3)]
        self.B = [['blue'] * 3 for row in range(3)]
        self.D = [['yellow'] * 3 for row in range(3)]
        self.timePassed = 0
        
    def scrambleCube(self):
        text = ""
        for i in range(21):
            num = random.randrange(1, 13)
            if num == 1: 
                self.moveU()
                text += "U "
            elif num == 2: 
                self.moveUPrime()
                text += "U' "
            elif num == 3: 
                self.moveL()
                text += "L "
            elif num == 4: 
                self.moveLPrime()
                text += "L' "
            elif num == 5: 
                self.moveF()
                text += "F "
            elif num == 6: 
                self.moveFPrime()
                text += "F' "
            elif num == 7: 
                self.moveR()
                text += "R "
            elif num == 8: 
                self.moveRPrime()
                text += "R' "
            elif num == 9: 
                self.moveB()
                text += "B "
            elif num == 10: 
                self.moveBPrime()
                text += "B' "
            elif num == 11: 
                self.moveD()
                text += "D "
            elif num == 12: 
                self.moveDPrime()
                text += "D' "
        self.display_text.append(f"Scramble: {text}")
        
    def drawYellowFace(self, draw):
        # draw the yellow face (D)
        
        # Row 1
        draw.polygon([(74 + self.bx, 438 + self.by), (174 + self.bx, 438 + self.by), (170 + self.bx, 522 + self.by), (66 + self.bx, 522 + self.by)], fill = self.D[0][0])
        draw.polygon([(192 + self.bx, 438 + self.by), (294 + self.bx, 438 + self.by), (298 + self.bx, 522 + self.by), (188 + self.bx, 522 + self.by)], fill = self.D[0][1])
        draw.polygon([(310 + self.bx, 436 + self.by), (410 + self.bx, 436 + self.by), (414 + self.bx, 524 + self.by), (314 + self.bx, 524 + self.by)], fill = self.D[0][2])

        # Row 2
        draw.polygon([(84 + self.bx, 348 + self.by), (178 + self.bx, 348 + self.by), (174 + self.bx, 422 + self.by), (76 + self.bx, 422 + self.by)], fill = self.D[1][0])
        draw.polygon([(196 + self.bx, 348 + self.by), (288 + self.bx, 348 + self.by), (292 + self.bx, 424 + self.by), (192 + self.bx, 424 + self.by)], fill = self.D[1][1])
        draw.polygon([(306 + self.bx, 348 + self.by), (400 + self.bx, 348 + self.by), (404 + self.bx, 424 + self.by), (310 + self.bx, 424 + self.by)], fill = self.D[1][2])

        # Row 3
        draw.polygon([(94 + self.bx, 270 + self.by), (182 + self.bx, 270 + self.by), (178 + self.bx, 336 + self.by), (84 + self.bx, 336 + self.by)], fill = self.D[2][0])
        draw.polygon([(198 + self.bx, 270 + self.by), (286 + self.bx, 270 + self.by), (290 + self.bx, 336 + self.by), (194 + self.bx, 336 + self.by)], fill = self.D[2][1])
        draw.polygon([(302 + self.bx, 268 + self.by), (390 + self.bx, 268 + self.by), (398 + self.bx, 336 + self.by), (306 + self.bx, 336 + self.by)], fill = self.D[2][2])

    def drawBlueFace(self, draw):
        #draw the blue face (B)

        # Row 1
        draw.polygon([(414 + self.bx, 2 + self.by), (314 + self.bx, 2 + self.by), (310 + self.bx, 90 + self.by), (410 + self.bx, 90 + self.by)], fill = self.B[0][0])
        draw.polygon([(298 + self.bx, 4 + self.by), (188 + self.bx, 4 + self.by), (192 + self.bx, 88 + self.by), (292 + self.bx, 88 + self.by)], fill = self.B[0][1])
        draw.polygon([(170 + self.bx, 4 + self.by), (66 + self.bx, 4 + self.by), (74 + self.bx, 88 + self.by), (174 + self.bx, 88 + self.by)], fill = self.B[0][2])

        # Row 2
        draw.polygon([(404 + self.bx, 102 + self.by), (310 + self.bx, 102 + self.by), (306 + self.bx, 178 + self.by), (400 + self.bx, 178 + self.by)], fill = self.B[1][0])
        draw.polygon([(292 + self.bx, 102 + self.by), (192 + self.bx, 102 + self.by), (196 + self.bx, 178 + self.by), (288 + self.bx, 178 + self.by)], fill = self.B[1][1])
        draw.polygon([(174 + self.bx, 104 + self.by), (76 + self.bx, 104 + self.by), (84 + self.bx, 178 + self.by), (178 + self.bx, 178 + self.by)], fill = self.B[1][2])

        # Row 3
        draw.polygon([(398 + self.bx, 190 + self.by), (306 + self.bx, 190 + self.by), (302 + self.bx, 258 + self.by), (390 + self.bx, 258 + self.by)], fill = self.B[2][0])
        draw.polygon([(290 + self.bx, 190 + self.by), (194 + self.bx, 190 + self.by), (198 + self.bx, 256 + self.by), (286 + self.bx, 256 + self.by)], fill = self.B[2][1])
        draw.polygon([(178 + self.bx, 190 + self.by), (84 + self.bx, 190 + self.by), (94 + self.bx, 256 + self.by), (182 + self.bx, 256 + self.by)], fill = self.B[2][2])
    
    def drawOrangeFace(self, draw):
    # draw the orange face (L)
    
        # Row 1
        draw.polygon([(52 + self.bx, 158 + self.by), (38 + self.bx, 74 + self.by), (50 + self.bx, 12 + self.by), (62 + self.bx, 84 + self.by)], fill = self.L[0][0])
        draw.polygon([(20 + self.bx, 162 + self.by), (36 + self.bx, 86 + self.by), (48 + self.bx, 164 + self.by), (36 + self.bx, 246 + self.by)], fill = self.L[0][1])
        draw.polygon([(0 + self.bx, 264 + self.by), (18 + self.bx, 174 + self.by), (34 + self.bx, 264 + self.by), (18 + self.bx, 352 + self.by)], fill = self.L[0][2])
        # Row 2       
        draw.polygon([(66 + self.bx, 100 + self.by), (56 + self.bx, 166 + self.by), (64 + self.bx, 240 + self.by), (74 + self.bx, 164 + self.by)], fill = self.L[1][0])
        draw.polygon([(52 + self.bx, 352 + self.by), (62 + self.bx, 264 + self.by), (52 + self.bx, 180 + self.by), (38 + self.bx, 264 + self.by)], fill = self.L[1][1])
        draw.polygon([(22 + self.bx, 364 + self.by), (36 + self.bx, 440 + self.by), (48 + self.bx, 366 + self.by), (36 + self.bx, 282 + self.by)], fill = self.L[1][2])
        # Row 3
        draw.polygon([(80 + self.bx, 354 + self.by), (66 + self.bx, 264 + self.by), (76 + self.bx, 180 + self.by), (86 + self.bx, 264 + self.by)], fill = self.L[2][0])
        draw.polygon([(56 + self.bx, 362 + self.by), (66 + self.bx, 438 + self.by), (74 + self.bx, 360 + self.by), (64 + self.bx, 292 + self.by)], fill = self.L[2][1])
        draw.polygon([(40 + self.bx, 454 + self.by), (52 + self.bx, 370 + self.by), (62 + self.bx, 442 + self.by), (52 + self.bx, 514 + self.by)], fill = self.L[2][2])

    def drawRedFace(self, draw):
        # draw the red face (R)
        
        # Row 1
        draw.polygon([(484 + self.bx, 264 + self.by), (466 + self.bx, 174 + self.by), (450 + self.bx, 264 + self.by), (466 + self.bx, 352 + self.by)], fill = self.R[0][0])
        draw.polygon([(464 + self.bx, 162 + self.by), (448 + self.bx, 86 + self.by), (436 + self.bx, 164 + self.by), (448 + self.bx, 246 + self.by)], fill = self.R[0][1])
        draw.polygon([(432 + self.bx, 158 + self.by), (446 + self.bx, 74 + self.by), (434 + self.bx, 12 + self.by), (422 + self.bx, 84 + self.by)], fill = self.R[0][2])
        # Row 2
        draw.polygon([(462 + self.bx, 364 + self.by), (448 + self.bx, 440 + self.by), (436 + self.bx, 366 + self.by), (446 + self.bx, 282 + self.by)], fill = self.R[1][0])
        draw.polygon([(432 + self.bx, 352 + self.by), (422 + self.bx, 264 + self.by), (432 + self.bx, 180 + self.by), (446 + self.bx, 264 + self.by)], fill = self.R[1][1])
        draw.polygon([(418 + self.bx, 100 + self.by), (428 + self.bx, 166 + self.by), (420 + self.bx, 240 + self.by), (410 + self.bx, 164 + self.by)], fill = self.R[1][2])
        # Row 3
        draw.polygon([(444 + self.bx, 454 + self.by), (432 + self.bx, 370 + self.by), (422 + self.bx, 442 + self.by), (432 + self.bx, 514 + self.by)], fill = self.R[2][0])
        draw.polygon([(428 + self.bx, 362 + self.by), (418 + self.bx, 438 + self.by), (410 + self.bx, 360 + self.by), (420 + self.bx, 292 + self.by)], fill = self.R[2][1])
        draw.polygon([(404 + self.bx, 354 + self.by), (418 + self.bx, 264 + self.by), (408 + self.bx, 180 + self.by), (398 + self.bx, 264 + self.by)], fill = self.R[2][2])

    def drawGreenFace(self, draw):
        # draw the green face (F)
        
        # Row 1
        draw.polygon([(10 + self.bx, 272 + self.by), (148 + self.bx, 272 + self.by), (156 + self.bx, 362 + self.by), (28 + self.bx, 362 + self.by)], fill = self.F[0][0])
        draw.polygon([(172 + self.bx, 272 + self.by), (312 + self.bx, 272 + self.by), (306 + self.bx, 362 + self.by), (178 + self.bx, 362 + self.by)], fill = self.F[0][1])
        draw.polygon([(336 + self.bx, 272 + self.by), (474 + self.bx, 272 + self.by), (456 + self.bx, 362 + self.by), (328 + self.bx, 362 + self.by)], fill = self.F[0][2])
        # Row 2
        draw.polygon([(32 + self.bx, 376 + self.by), (158 + self.bx, 376 + self.by), (164 + self.bx, 450 + self.by), (46 + self.bx, 450 + self.by)], fill = self.F[1][0])
        draw.polygon([(180 + self.bx, 376 + self.by), (304 + self.bx, 376 + self.by), (300 + self.bx, 450 + self.by), (184 + self.bx, 450 + self.by)], fill = self.F[1][1])
        draw.polygon([(328 + self.bx, 376 + self.by), (452 + self.bx, 376 + self.by), (438 + self.bx, 450 + self.by), (320 + self.bx, 450 + self.by)], fill = self.F[1][2])
        # Row 3
        draw.polygon([(48 + self.bx, 464 + self.by), (164 + self.bx, 464 + self.by), (170 + self.bx, 526 + self.by), (62 + self.bx, 526 + self.by)], fill = self.F[2][0])
        draw.polygon([(186 + self.bx, 464 + self.by), (298 + self.bx, 464 + self.by), (296 + self.bx, 526 + self.by), (188 + self.bx, 526 + self.by)], fill = self.F[2][1])
        draw.polygon([(320 + self.bx, 462 + self.by), (436 + self.bx, 462 + self.by), (422 + self.bx, 526 + self.by), (314 + self.bx, 526 + self.by)], fill = self.F[2][2])

    def drawWhiteFace(self, draw):
        # draw the white face (U)
        
        # Row 1
        draw.polygon([(60 + self.bx, 0 + self.by), (168 + self.bx, 0 + self.by), (164 + self.bx, 64 + self.by), (48 + self.bx, 64 + self.by)], fill = self.U[0][0])
        draw.polygon([(188 + self.bx, 0 + self.by), (296 + self.bx, 0 + self.by), (300 + self.bx, 64 + self.by), (184 + self.bx, 64 + self.by)], fill = self.U[0][1])
        draw.polygon([(316 + self.bx, 0 + self.by), (424 + self.bx, 0 + self.by), (436 + self.bx, 64 + self.by), (320 + self.bx, 64 + self.by)], fill = self.U[0][2])
        # Row 2
        draw.polygon([(44 + self.bx, 76 + self.by), (162 + self.bx, 76 + self.by), (156 + self.bx, 152 + self.by), (30 + self.bx, 152 + self.by)], fill = self.U[1][0])
        draw.polygon([(184 + self.bx, 76 + self.by), (300 + self.bx, 76 + self.by), (304 + self.bx, 150 + self.by), (180 + self.bx, 150 + self.by)], fill = self.U[1][1])
        draw.polygon([(322 + self.bx, 76 + self.by), (440 + self.bx, 76 + self.by), (452 + self.bx, 152 + self.by), (328 + self.bx, 152 + self.by)], fill = self.U[1][2])
        # Row 3
        draw.polygon([(28 + self.bx, 166 + self.by), (156 + self.bx, 166 + self.by), (148 + self.bx, 256 + self.by), (10 + self.bx, 256 + self.by)], fill = self.U[2][0])
        draw.polygon([(178 + self.bx, 166 + self.by), (306 + self.bx, 166 + self.by), (310 + self.bx, 254 + self.by), (174 + self.bx, 254 + self.by)], fill = self.U[2][1])
        draw.polygon([(328 + self.bx, 166 + self.by), (456 + self.bx, 166 + self.by), (474 + self.bx, 254 + self.by), (336 + self.bx, 254 + self.by)], fill = self.U[2][2])

    def drawFlowerExample(self, draw):
        self.screen.fill(BACKGROUND_COLOR) 
        draw.polygon([(60 + self.bx, 0 + self.by), (168 + self.bx, 0 + self.by), (164 + self.bx, 64 + self.by), (48 + self.bx, 64 + self.by)], fill='orange')
        draw.polygon([(188 + self.bx, 0 + self.by), (296 + self.bx, 0 + self.by), (300 + self.bx, 64 + self.by), (184 + self.bx, 64 + self.by)], fill='white')
        draw.polygon([(316 + self.bx, 0 + self.by), (424 + self.bx, 0 + self.by), (436 + self.bx, 64 + self.by), (320 + self.bx, 64 + self.by)], fill='green')
        draw.polygon([(44 + self.bx, 76 + self.by), (162 + self.bx, 76 + self.by), (156 + self.bx, 152 + self.by), (30 + self.bx, 152 + self.by)], fill='white')
        draw.polygon([(184 + self.bx, 76 + self.by), (300 + self.bx, 76 + self.by), (304 + self.bx, 150 + self.by), (180 + self.bx, 150 + self.by)], fill='yellow')
        draw.polygon([(322 + self.bx, 76 + self.by), (440 + self.bx, 76 + self.by), (452 + self.bx, 152 + self.by), (328 + self.bx, 152 + self.by)], fill='white')
        draw.polygon([(28 + self.bx, 166 + self.by), (156 + self.bx, 166 + self.by), (148 + self.bx, 256 + self.by), (10 + self.bx, 256 + self.by)], fill='blue')
        draw.polygon([(178 + self.bx, 166 + self.by), (306 + self.bx, 166 + self.by), (310 + self.bx, 254 + self.by), (174 + self.bx, 254 + self.by)], fill='white')
        draw.polygon([(328 + self.bx, 166 + self.by), (456 + self.bx, 166 + self.by), (474 + self.bx, 254 + self.by), (336 + self.bx, 254 + self.by)], fill='green')

    def drawCornerExample1(self, draw):
        #white side (D)
        draw.polygon([(74 + self.bx, 438 + self.by), (174 + self.bx, 438 + self.by), (170 + self.bx, 522 + self.by), (66 + self.bx, 522 + self.by)], fill='orange')
        draw.polygon([(192 + self.bx, 438 + self.by), (294 + self.bx, 438 + self.by), (298 + self.bx, 522 + self.by), (188 + self.bx, 522 + self.by)], fill='white')
        draw.polygon([(310 + self.bx, 436 + self.by), (410 + self.bx, 436 + self.by), (414 + self.bx, 524 + self.by), (314 + self.bx, 524 + self.by)], fill='white')
        draw.polygon([(84 + self.bx, 348 + self.by), (178 + self.bx, 348 + self.by), (174 + self.bx, 422 + self.by), (76 + self.bx, 422 + self.by)], fill='white')
        draw.polygon([(196 + self.bx, 348 + self.by), (288 + self.bx, 348 + self.by), (292 + self.bx, 424 + self.by), (192 + self.bx, 424 + self.by)], fill='white')
        draw.polygon([(306 + self.bx, 348 + self.by), (400 + self.bx, 348 + self.by), (404 + self.bx, 424 + self.by), (310 + self.bx, 424 + self.by)], fill='white')
        draw.polygon([(94 + self.bx, 270 + self.by), (182 + self.bx, 270 + self.by), (178 + self.bx, 336 + self.by), (84 + self.bx, 336 + self.by)], fill='red')
        draw.polygon([(198 + self.bx, 270 + self.by), (286 + self.bx, 270 + self.by), (290 + self.bx, 336 + self.by), (194 + self.bx, 336 + self.by)], fill='white')
        draw.polygon([(302 + self.bx, 268 + self.by), (390 + self.bx, 268 + self.by), (398 + self.bx, 336 + self.by), (306 + self.bx, 336 + self.by)], fill='blue')
        #red side (B)
        draw.polygon([(414 + self.bx, 2 + self.by), (314 + self.bx, 2 + self.by), (310 + self.bx, 90 + self.by), (410 + self.bx, 90 + self.by)], fill='blue')
        draw.polygon([(298 + self.bx, 4 + self.by), (188 + self.bx, 4 + self.by), (192 + self.bx, 88 + self.by), (292 + self.bx, 88 + self.by)], fill='yellow')
        draw.polygon([(170 + self.bx, 4 + self.by), (66 + self.bx, 4 + self.by), (74 + self.bx, 88 + self.by), (174 + self.bx, 88 + self.by)], fill='white')
        draw.polygon([(404 + self.bx, 102 + self.by), (310 + self.bx, 102 + self.by), (306 + self.bx, 178 + self.by), (400 + self.bx, 178 + self.by)], fill='yellow')
        draw.polygon([(292 + self.bx, 102 + self.by), (192 + self.bx, 102 + self.by), (196 + self.bx, 178 + self.by), (288 + self.bx, 178 + self.by)], fill='red')
        draw.polygon([(174 + self.bx, 104 + self.by), (76 + self.bx, 104 + self.by), (84 + self.bx, 178 + self.by), (178 + self.bx, 178 + self.by)], fill='red')
        draw.polygon([(398 + self.bx, 190 + self.by), (306 + self.bx, 190 + self.by), (302 + self.bx, 258 + self.by), (390 + self.bx, 258 + self.by)], fill='red')
        draw.polygon([(290 + self.bx, 190 + self.by), (194 + self.bx, 190 + self.by), (198 + self.bx, 256 + self.by), (286 + self.bx, 256 + self.by)], fill='red')
        draw.polygon([(178 + self.bx, 190 + self.by), (84 + self.bx, 190 + self.by), (94 + self.bx, 256 + self.by), (182 + self.bx, 256 + self.by)], fill='yellow')
        #green side (L)
        draw.polygon([(52 + self.bx, 158 + self.by), (38 + self.bx, 74 + self.by), (50 + self.bx, 12 + self.by), (62 + self.bx, 84 + self.by)], fill='green')
        draw.polygon([(20 + self.bx, 162 + self.by), (36 + self.bx, 86 + self.by), (48 + self.bx, 164 + self.by), (36 + self.bx, 246 + self.by)], fill='green')
        draw.polygon([(0 + self.bx, 264 + self.by), (18 + self.bx, 174 + self.by), (34 + self.bx, 264 + self.by), (18 + self.bx, 352 + self.by)], fill='green')
        draw.polygon([(66 + self.bx, 100 + self.by), (56 + self.bx, 166 + self.by), (64 + self.bx, 240 + self.by), (74 + self.bx, 164 + self.by)], fill='yellow')
        draw.polygon([(52 + self.bx, 352 + self.by), (62 + self.bx, 264 + self.by), (52 + self.bx, 180 + self.by), (38 + self.bx, 264 + self.by)], fill='green')
        draw.polygon([(22 + self.bx, 364 + self.by), (36 + self.bx, 440 + self.by), (48 + self.bx, 366 + self.by), (36 + self.bx, 282 + self.by)], fill='red')
        draw.polygon([(80 + self.bx, 354 + self.by), (66 + self.bx, 264 + self.by), (76 + self.bx, 180 + self.by), (86 + self.bx, 264 + self.by)], fill='green')
        draw.polygon([(56 + self.bx, 362 + self.by), (66 + self.bx, 438 + self.by), (74 + self.bx, 360 + self.by), (64 + self.bx, 292 + self.by)], fill='green')
        draw.polygon([(40 + self.bx, 454 + self.by), (52 + self.bx, 370 + self.by), (62 + self.bx, 442 + self.by), (52 + self.bx, 514 + self.by)], fill='yellow')
        #blue side (R)
        draw.polygon([(484 + self.bx, 264 + self.by), (466 + self.bx, 174 + self.by), (450 + self.bx, 264 + self.by), (466 + self.bx, 352 + self.by)], fill='orange')
        draw.polygon([(464 + self.bx, 162 + self.by), (448 + self.bx, 86 + self.by), (436 + self.bx, 164 + self.by), (448 + self.bx, 246 + self.by)], fill='orange')
        draw.polygon([(432 + self.bx, 158 + self.by), (446 + self.bx, 74 + self.by), (434 + self.bx, 12 + self.by), (422 + self.bx, 84 + self.by)], fill='red')
        draw.polygon([(462 + self.bx, 364 + self.by), (448 + self.bx, 440 + self.by), (436 + self.bx, 366 + self.by), (446 + self.bx, 282 + self.by)], fill='blue')
        draw.polygon([(432 + self.bx, 352 + self.by), (422 + self.bx, 264 + self.by), (432 + self.bx, 180 + self.by), (446 + self.bx, 264 + self.by)], fill='blue')
        draw.polygon([(418 + self.bx, 100 + self.by), (428 + self.bx, 166 + self.by), (420 + self.bx, 240 + self.by), (410 + self.bx, 164 + self.by)], fill='blue')
        draw.polygon([(444 + self.bx, 454 + self.by), (432 + self.bx, 370 + self.by), (422 + self.bx, 442 + self.by), (432 + self.bx, 514 + self.by)], fill='blue')
        draw.polygon([(428 + self.bx, 362 + self.by), (418 + self.bx, 438 + self.by), (410 + self.bx, 360 + self.by), (420 + self.bx, 292 + self.by)], fill='blue')
        draw.polygon([(404 + self.bx, 354 + self.by), (418 + self.bx, 264 + self.by), (408 + self.bx, 180 + self.by), (398 + self.bx, 264 + self.by)], fill='yellow')
        #orange side (F)
        draw.polygon([(10 + self.bx, 272 + self.by), (148 + self.bx, 272 + self.by), (156 + self.bx, 362 + self.by), (28 + self.bx, 362 + self.by)], fill='white')
        draw.polygon([(172 + self.bx, 272 + self.by), (312 + self.bx, 272 + self.by), (306 + self.bx, 362 + self.by), (178 + self.bx, 362 + self.by)], fill='red')
        draw.polygon([(336 + self.bx, 272 + self.by), (474 + self.bx, 272 + self.by), (456 + self.bx, 362 + self.by), (328 + self.bx, 362 + self.by)], fill='green')
        draw.polygon([(32 + self.bx, 376 + self.by), (158 + self.bx, 376 + self.by), (164 + self.bx, 450 + self.by), (46 + self.bx, 450 + self.by)], fill='blue')
        draw.polygon([(180 + self.bx, 376 + self.by), (304 + self.bx, 376 + self.by), (300 + self.bx, 450 + self.by), (184 + self.bx, 450 + self.by)], fill='orange')
        draw.polygon([(328 + self.bx, 376 + self.by), (452 + self.bx, 376 + self.by), (438 + self.bx, 450 + self.by), (320 + self.bx, 450 + self.by)], fill='orange')
        draw.polygon([(48 + self.bx, 464 + self.by), (164 + self.bx, 464 + self.by), (170 + self.bx, 526 + self.by), (62 + self.bx, 526 + self.by)], fill='blue')
        draw.polygon([(186 + self.bx, 464 + self.by), (298 + self.bx, 464 + self.by), (296 + self.bx, 526 + self.by), (188 + self.bx, 526 + self.by)], fill='orange')
        draw.polygon([(320 + self.bx, 462 + self.by), (436 + self.bx, 462 + self.by), (422 + self.bx, 526 + self.by), (314 + self.bx, 526 + self.by)], fill='orange')
        #yellow side (U)
        draw.polygon([(60 + self.bx, 0 + self.by), (168 + self.bx, 0 + self.by), (164 + self.bx, 64 + self.by), (48 + self.bx, 64 + self.by)], fill='red')
        draw.polygon([(188 + self.bx, 0 + self.by), (296 + self.bx, 0 + self.by), (300 + self.bx, 64 + self.by), (184 + self.bx, 64 + self.by)], fill='green')
        draw.polygon([(316 + self.bx, 0 + self.by), (424 + self.bx, 0 + self.by), (436 + self.bx, 64 + self.by), (320 + self.bx, 64 + self.by)], fill='white')
        draw.polygon([(44 + self.bx, 76 + self.by), (162 + self.bx, 76 + self.by), (156 + self.bx, 152 + self.by), (30 + self.bx, 152 + self.by)], fill='orange')
        draw.polygon([(184 + self.bx, 76 + self.by), (300 + self.bx, 76 + self.by), (304 + self.bx, 150 + self.by), (180 + self.bx, 150 + self.by)], fill='yellow')
        draw.polygon([(322 + self.bx, 76 + self.by), (440 + self.bx, 76 + self.by), (452 + self.bx, 152 + self.by), (328 + self.bx, 152 + self.by)], fill='yellow')
        draw.polygon([(28 + self.bx, 166 + self.by), (156 + self.bx, 166 + self.by), (148 + self.bx, 256 + self.by), (10 + self.bx, 256 + self.by)], fill='orange')
        draw.polygon([(178 + self.bx, 166 + self.by), (306 + self.bx, 166 + self.by), (310 + self.bx, 254 + self.by), (174 + self.bx, 254 + self.by)], fill='green')
        draw.polygon([(328 + self.bx, 166 + self.by), (456 + self.bx, 166 + self.by), (474 + self.bx, 254 + self.by), (336 + self.bx, 254 + self.by)], fill='yellow')
    
    def drawCornerExample2(self, draw):
        # white side (D)
        draw.polygon([(74 + self.bx, 438 + self.by), (174 + self.bx, 438 + self.by), (170 + self.bx, 522 + self.by), (66 + self.bx, 522 + self.by)], fill='blue')
        draw.polygon([(192 + self.bx, 438 + self.by), (294 + self.bx, 438 + self.by), (298 + self.bx, 522 + self.by), (188 + self.bx, 522 + self.by)], fill='white')
        draw.polygon([(310 + self.bx, 436 + self.by), (410 + self.bx, 436 + self.by), (414 + self.bx, 524 + self.by), (314 + self.bx, 524 + self.by)], fill='red')
        draw.polygon([(84 + self.bx, 348 + self.by), (178 + self.bx, 348 + self.by), (174 + self.bx, 422 + self.by), (76 + self.bx, 422 + self.by)], fill='white')
        draw.polygon([(196 + self.bx, 348 + self.by), (288 + self.bx, 348 + self.by), (292 + self.bx, 424 + self.by), (192 + self.bx, 424 + self.by)], fill='white')
        draw.polygon([(306 + self.bx, 348 + self.by), (400 + self.bx, 348 + self.by), (404 + self.bx, 424 + self.by), (310 + self.bx, 424 + self.by)], fill='white')
        draw.polygon([(94 + self.bx, 270 + self.by), (182 + self.bx, 270 + self.by), (178 + self.bx, 336 + self.by), (84 + self.bx, 336 + self.by)], fill='white')
        draw.polygon([(198 + self.bx, 270 + self.by), (286 + self.bx, 270 + self.by), (290 + self.bx, 336 + self.by), (194 + self.bx, 336 + self.by)], fill='white')
        draw.polygon([(302 + self.bx, 268 + self.by), (390 + self.bx, 268 + self.by), (398 + self.bx, 336 + self.by), (306 + self.bx, 336 + self.by)], fill='orange')
        
        # red side (B)
        draw.polygon([(414 + self.bx, 2 + self.by), (314 + self.bx, 2 + self.by), (310 + self.bx, 90 + self.by), (410 + self.bx, 90 + self.by)], fill='white')
        draw.polygon([(298 + self.bx, 4 + self.by), (188 + self.bx, 4 + self.by), (192 + self.bx, 88 + self.by), (292 + self.bx, 88 + self.by)], fill='red')
        draw.polygon([(170 + self.bx, 4 + self.by), (66 + self.bx, 4 + self.by), (74 + self.bx, 88 + self.by), (174 + self.bx, 88 + self.by)], fill='green')
        draw.polygon([(404 + self.bx, 102 + self.by), (310 + self.bx, 102 + self.by), (306 + self.bx, 178 + self.by), (400 + self.bx, 178 + self.by)], fill='blue')
        draw.polygon([(292 + self.bx, 102 + self.by), (192 + self.bx, 102 + self.by), (196 + self.bx, 178 + self.by), (288 + self.bx, 178 + self.by)], fill='orange')
        draw.polygon([(174 + self.bx, 104 + self.by), (76 + self.bx, 104 + self.by), (84 + self.bx, 178 + self.by), (178 + self.bx, 178 + self.by)], fill='orange')
        draw.polygon([(398 + self.bx, 190 + self.by), (306 + self.bx, 190 + self.by), (302 + self.bx, 258 + self.by), (390 + self.bx, 258 + self.by)], fill='blue')
        draw.polygon([(290 + self.bx, 190 + self.by), (194 + self.bx, 190 + self.by), (198 + self.bx, 256 + self.by), (286 + self.bx, 256 + self.by)], fill='orange')
        draw.polygon([(178 + self.bx, 190 + self.by), (84 + self.bx, 190 + self.by), (94 + self.bx, 256 + self.by), (182 + self.bx, 256 + self.by)], fill='orange')
        
        # green side (L)
        draw.polygon([(52 + self.bx, 158 + self.by), (38 + self.bx, 74 + self.by), (50 + self.bx, 12 + self.by), (62 + self.bx, 84 + self.by)], fill='orange')
        draw.polygon([(20 + self.bx, 162 + self.by), (36 + self.bx, 86 + self.by), (48 + self.bx, 164 + self.by), (36 + self.bx, 246 + self.by)], fill='orange')
        draw.polygon([(0 + self.bx, 264 + self.by), (18 + self.bx, 174 + self.by), (34 + self.bx, 264 + self.by), (18 + self.bx, 352 + self.by)], fill='red')
        draw.polygon([(66 + self.bx, 100 + self.by), (56 + self.bx, 166 + self.by), (64 + self.bx, 240 + self.by), (74 + self.bx, 164 + self.by)], fill='blue')
        draw.polygon([(52 + self.bx, 352 + self.by), (62 + self.bx, 264 + self.by), (52 + self.bx, 180 + self.by), (38 + self.bx, 264 + self.by)], fill='blue')
        draw.polygon([(22 + self.bx, 364 + self.by), (36 + self.bx, 440 + self.by), (48 + self.bx, 366 + self.by), (36 + self.bx, 282 + self.by)], fill='blue')
        draw.polygon([(80 + self.bx, 354 + self.by), (66 + self.bx, 264 + self.by), (76 + self.bx, 180 + self.by), (86 + self.bx, 264 + self.by)], fill='blue')
        draw.polygon([(56 + self.bx, 362 + self.by), (66 + self.bx, 438 + self.by), (74 + self.bx, 360 + self.by), (64 + self.bx, 292 + self.by)], fill='blue')
        draw.polygon([(40 + self.bx, 454 + self.by), (52 + self.bx, 370 + self.by), (62 + self.bx, 442 + self.by), (52 + self.bx, 514 + self.by)], fill='yellow')
        
        # blue side (R)
        draw.polygon([(484 + self.bx, 264 + self.by), (466 + self.bx, 174 + self.by), (450 + self.bx, 264 + self.by), (466 + self.bx, 352 + self.by)], fill='green')
        draw.polygon([(464 + self.bx, 162 + self.by), (448 + self.bx, 86 + self.by), (436 + self.bx, 164 + self.by), (448 + self.bx, 246 + self.by)], fill='green')
        draw.polygon([(432 + self.bx, 158 + self.by), (446 + self.bx, 74 + self.by), (434 + self.bx, 12 + self.by), (422 + self.bx, 84 + self.by)], fill='green')
        draw.polygon([(462 + self.bx, 364 + self.by), (448 + self.bx, 440 + self.by), (436 + self.bx, 366 + self.by), (446 + self.bx, 282 + self.by)], fill='yellow')
        draw.polygon([(432 + self.bx, 352 + self.by), (422 + self.bx, 264 + self.by), (432 + self.bx, 180 + self.by), (446 + self.bx, 264 + self.by)], fill='green')
        draw.polygon([(418 + self.bx, 100 + self.by), (428 + self.bx, 166 + self.by), (420 + self.bx, 240 + self.by), (410 + self.bx, 164 + self.by)], fill='red')
        draw.polygon([(444 + self.bx, 454 + self.by), (432 + self.bx, 370 + self.by), (422 + self.bx, 442 + self.by), (432 + self.bx, 514 + self.by)], fill='green')
        draw.polygon([(428 + self.bx, 362 + self.by), (418 + self.bx, 438 + self.by), (410 + self.bx, 360 + self.by), (420 + self.bx, 292 + self.by)], fill='green')
        draw.polygon([(404 + self.bx, 354 + self.by), (418 + self.bx, 264 + self.by), (408 + self.bx, 180 + self.by), (398 + self.bx, 264 + self.by)], fill='yellow')
        
        # orange side (F)
        draw.polygon([(10 + self.bx, 272 + self.by), (148 + self.bx, 272 + self.by), (156 + self.bx, 362 + self.by), (28 + self.bx, 362 + self.by)], fill='blue')
        draw.polygon([(172 + self.bx, 272 + self.by), (312 + self.bx, 272 + self.by), (306 + self.bx, 362 + self.by), (178 + self.bx, 362 + self.by)], fill='yellow')
        draw.polygon([(336 + self.bx, 272 + self.by), (474 + self.bx, 272 + self.by), (456 + self.bx, 362 + self.by), (328 + self.bx, 362 + self.by)], fill='white')
        draw.polygon([(32 + self.bx, 376 + self.by), (158 + self.bx, 376 + self.by), (164 + self.bx, 450 + self.by), (46 + self.bx, 450 + self.by)], fill='yellow')
        draw.polygon([(180 + self.bx, 376 + self.by), (304 + self.bx, 376 + self.by), (300 + self.bx, 450 + self.by), (184 + self.bx, 450 + self.by)], fill='red')
        draw.polygon([(328 + self.bx, 376 + self.by), (452 + self.bx, 376 + self.by), (438 + self.bx, 450 + self.by), (320 + self.bx, 450 + self.by)], fill='red')
        draw.polygon([(48 + self.bx, 464 + self.by), (164 + self.bx, 464 + self.by), (170 + self.bx, 526 + self.by), (62 + self.bx, 526 + self.by)], fill='red')
        draw.polygon([(186 + self.bx, 464 + self.by), (298 + self.bx, 464 + self.by), (296 + self.bx, 526 + self.by), (188 + self.bx, 526 + self.by)], fill='red')
        draw.polygon([(320 + self.bx, 462 + self.by), (436 + self.bx, 462 + self.by), (422 + self.bx, 526 + self.by), (314 + self.bx, 526 + self.by)], fill='yellow')
        
        # yellow side (U)
        draw.polygon([(60 + self.bx, 0 + self.by), (168 + self.bx, 0 + self.by), (164 + self.bx, 64 + self.by), (48 + self.bx, 64 + self.by)], fill='yellow')
        draw.polygon([(188 + self.bx, 0 + self.by), (296 + self.bx, 0 + self.by), (300 + self.bx, 64 + self.by), (184 + self.bx, 64 + self.by)], fill='green')
        draw.polygon([(316 + self.bx, 0 + self.by), (424 + self.bx, 0 + self.by), (436 + self.bx, 64 + self.by), (320 + self.bx, 64 + self.by)], fill='orange')
        draw.polygon([(44 + self.bx, 76 + self.by), (162 + self.bx, 76 + self.by), (156 + self.bx, 152 + self.by), (30 + self.bx, 152 + self.by)], fill='yellow')
        draw.polygon([(184 + self.bx, 76 + self.by), (300 + self.bx, 76 + self.by), (304 + self.bx, 150 + self.by), (180 + self.bx, 150 + self.by)], fill='yellow')
        draw.polygon([(322 + self.bx, 76 + self.by), (440 + self.bx, 76 + self.by), (452 + self.bx, 152 + self.by), (328 + self.bx, 152 + self.by)], fill='orange')
        draw.polygon([(28 + self.bx, 166 + self.by), (156 + self.bx, 166 + self.by), (148 + self.bx, 256 + self.by), (10 + self.bx, 256 + self.by)], fill='white')
        draw.polygon([(178 + self.bx, 166 + self.by), (306 + self.bx, 166 + self.by), (310 + self.bx, 254 + self.by), (174 + self.bx, 254 + self.by)], fill='green')
        draw.polygon([(328 + self.bx, 166 + self.by), (456 + self.bx, 166 + self.by), (474 + self.bx, 254 + self.by), (336 + self.bx, 254 + self.by)], fill='red')
   
    def drawCornerExample3(self, draw):    
    # white side (D)
        draw.polygon([(74 + self.bx, 438 + self.by), (174 + self.bx, 438 + self.by), (170 + self.bx, 522 + self.by), (66 + self.bx, 522 + self.by)], fill='white')
        draw.polygon([(192 + self.bx, 438 + self.by), (294 + self.bx, 438 + self.by), (298 + self.bx, 522 + self.by), (188 + self.bx, 522 + self.by)], fill='white')
        draw.polygon([(310 + self.bx, 436 + self.by), (410 + self.bx, 436 + self.by), (414 + self.bx, 524 + self.by), (314 + self.bx, 524 + self.by)], fill='blue')
        draw.polygon([(84 + self.bx, 348 + self.by), (178 + self.bx, 348 + self.by), (174 + self.bx, 422 + self.by), (76 + self.bx, 422 + self.by)], fill='white')
        draw.polygon([(196 + self.bx, 348 + self.by), (288 + self.bx, 348 + self.by), (292 + self.bx, 424 + self.by), (192 + self.bx, 424 + self.by)], fill='white')
        draw.polygon([(306 + self.bx, 348 + self.by), (400 + self.bx, 348 + self.by), (404 + self.bx, 424 + self.by), (310 + self.bx, 424 + self.by)], fill='white')
        draw.polygon([(94 + self.bx, 270 + self.by), (182 + self.bx, 270 + self.by), (178 + self.bx, 336 + self.by), (84 + self.bx, 336 + self.by)], fill='orange')
        draw.polygon([(198 + self.bx, 270 + self.by), (286 + self.bx, 270 + self.by), (290 + self.bx, 336 + self.by), (194 + self.bx, 336 + self.by)], fill='white')
        draw.polygon([(302 + self.bx, 268 + self.by), (390 + self.bx, 268 + self.by), (398 + self.bx, 336 + self.by), (306 + self.bx, 336 + self.by)], fill='red')
        
        # red side (B)
        draw.polygon([(414 + self.bx, 2 + self.by), (314 + self.bx, 2 + self.by), (310 + self.bx, 90 + self.by), (410 + self.bx, 90 + self.by)], fill='green')
        draw.polygon([(298 + self.bx, 4 + self.by), (188 + self.bx, 4 + self.by), (192 + self.bx, 88 + self.by), (292 + self.bx, 88 + self.by)], fill='green')
        draw.polygon([(170 + self.bx, 4 + self.by), (66 + self.bx, 4 + self.by), (74 + self.bx, 88 + self.by), (174 + self.bx, 88 + self.by)], fill='green')
        draw.polygon([(404 + self.bx, 102 + self.by), (310 + self.bx, 102 + self.by), (306 + self.bx, 178 + self.by), (400 + self.bx, 178 + self.by)], fill='yellow')
        draw.polygon([(292 + self.bx, 102 + self.by), (192 + self.bx, 102 + self.by), (196 + self.bx, 178 + self.by), (288 + self.bx, 178 + self.by)], fill='green')
        draw.polygon([(174 + self.bx, 104 + self.by), (76 + self.bx, 104 + self.by), (84 + self.bx, 178 + self.by), (178 + self.bx, 178 + self.by)], fill='red')
        draw.polygon([(398 + self.bx, 190 + self.by), (306 + self.bx, 190 + self.by), (302 + self.bx, 258 + self.by), (390 + self.bx, 258 + self.by)], fill='green')
        draw.polygon([(290 + self.bx, 190 + self.by), (194 + self.bx, 190 + self.by), (198 + self.bx, 256 + self.by), (286 + self.bx, 256 + self.by)], fill='green')
        draw.polygon([(178 + self.bx, 190 + self.by), (84 + self.bx, 190 + self.by), (94 + self.bx, 256 + self.by), (182 + self.bx, 256 + self.by)], fill='yellow')
        
        # green side (L)
        draw.polygon([(52 + self.bx, 158 + self.by), (38 + self.bx, 74 + self.by), (50 + self.bx, 12 + self.by), (62 + self.bx, 84 + self.by)], fill='white')
        draw.polygon([(20 + self.bx, 162 + self.by), (36 + self.bx, 86 + self.by), (48 + self.bx, 164 + self.by), (36 + self.bx, 246 + self.by)], fill='red')
        draw.polygon([(0 + self.bx, 264 + self.by), (18 + self.bx, 174 + self.by), (34 + self.bx, 264 + self.by), (18 + self.bx, 352 + self.by)], fill='green')
        draw.polygon([(66 + self.bx, 100 + self.by), (56 + self.bx, 166 + self.by), (64 + self.bx, 240 + self.by), (74 + self.bx, 164 + self.by)], fill='blue')
        draw.polygon([(52 + self.bx, 352 + self.by), (62 + self.bx, 264 + self.by), (52 + self.bx, 180 + self.by), (38 + self.bx, 264 + self.by)], fill='orange')
        draw.polygon([(22 + self.bx, 364 + self.by), (36 + self.bx, 440 + self.by), (48 + self.bx, 366 + self.by), (36 + self.bx, 282 + self.by)], fill='orange')
        draw.polygon([(80 + self.bx, 354 + self.by), (66 + self.bx, 264 + self.by), (76 + self.bx, 180 + self.by), (86 + self.bx, 264 + self.by)], fill='blue')
        draw.polygon([(56 + self.bx, 362 + self.by), (66 + self.bx, 438 + self.by), (74 + self.bx, 360 + self.by), (64 + self.bx, 292 + self.by)], fill='orange')
        draw.polygon([(40 + self.bx, 454 + self.by), (52 + self.bx, 370 + self.by), (62 + self.bx, 442 + self.by), (52 + self.bx, 514 + self.by)], fill='orange')
        
        # blue side (R)
        draw.polygon([(484 + self.bx, 264 + self.by), (466 + self.bx, 174 + self.by), (450 + self.bx, 264 + self.by), (466 + self.bx, 352 + self.by)], fill='blue')
        draw.polygon([(464 + self.bx, 162 + self.by), (448 + self.bx, 86 + self.by), (436 + self.bx, 164 + self.by), (448 + self.bx, 246 + self.by)], fill='yellow')
        draw.polygon([(432 + self.bx, 158 + self.by), (446 + self.bx, 74 + self.by), (434 + self.bx, 12 + self.by), (422 + self.bx, 84 + self.by)], fill='white')
        draw.polygon([(462 + self.bx, 364 + self.by), (448 + self.bx, 440 + self.by), (436 + self.bx, 366 + self.by), (446 + self.bx, 282 + self.by)], fill='yellow')
        draw.polygon([(432 + self.bx, 352 + self.by), (422 + self.bx, 264 + self.by), (432 + self.bx, 180 + self.by), (446 + self.bx, 264 + self.by)], fill='red')
        draw.polygon([(418 + self.bx, 100 + self.by), (428 + self.bx, 166 + self.by), (420 + self.bx, 240 + self.by), (410 + self.bx, 164 + self.by)], fill='red')
        draw.polygon([(444 + self.bx, 454 + self.by), (432 + self.bx, 370 + self.by), (422 + self.bx, 442 + self.by), (432 + self.bx, 514 + self.by)], fill='red')
        draw.polygon([(428 + self.bx, 362 + self.by), (418 + self.bx, 438 + self.by), (410 + self.bx, 360 + self.by), (420 + self.bx, 292 + self.by)], fill='red')
        draw.polygon([(404 + self.bx, 354 + self.by), (418 + self.bx, 264 + self.by), (408 + self.bx, 180 + self.by), (398 + self.bx, 264 + self.by)], fill='yellow')
        
        # orange side (F)
        draw.polygon([(10 + self.bx, 272 + self.by), (148 + self.bx, 272 + self.by), (156 + self.bx, 362 + self.by), (28 + self.bx, 362 + self.by)], fill='orange')
        draw.polygon([(172 + self.bx, 272 + self.by), (312 + self.bx, 272 + self.by), (306 + self.bx, 362 + self.by), (178 + self.bx, 362 + self.by)], fill='orange')
        draw.polygon([(336 + self.bx, 272 + self.by), (474 + self.bx, 272 + self.by), (456 + self.bx, 362 + self.by), (328 + self.bx, 362 + self.by)], fill='red')
        draw.polygon([(32 + self.bx, 376 + self.by), (158 + self.bx, 376 + self.by), (164 + self.bx, 450 + self.by), (46 + self.bx, 450 + self.by)], fill='blue')
        draw.polygon([(180 + self.bx, 376 + self.by), (304 + self.bx, 376 + self.by), (300 + self.bx, 450 + self.by), (184 + self.bx, 450 + self.by)], fill='blue')
        draw.polygon([(328 + self.bx, 376 + self.by), (452 + self.bx, 376 + self.by), (438 + self.bx, 450 + self.by), (320 + self.bx, 450 + self.by)], fill='blue')
        draw.polygon([(48 + self.bx, 464 + self.by), (164 + self.bx, 464 + self.by), (170 + self.bx, 526 + self.by), (62 + self.bx, 526 + self.by)], fill='blue')
        draw.polygon([(186 + self.bx, 464 + self.by), (298 + self.bx, 464 + self.by), (296 + self.bx, 526 + self.by), (188 + self.bx, 526 + self.by)], fill='blue')
        draw.polygon([(320 + self.bx, 462 + self.by), (436 + self.bx, 462 + self.by), (422 + self.bx, 526 + self.by), (314 + self.bx, 526 + self.by)], fill='yellow')
        
        # yellow side (U)
        draw.polygon([(60 + self.bx, 0 + self.by), (168 + self.bx, 0 + self.by), (164 + self.bx, 64 + self.by), (48 + self.bx, 64 + self.by)], fill='orange')
        draw.polygon([(188 + self.bx, 0 + self.by), (296 + self.bx, 0 + self.by), (300 + self.bx, 64 + self.by), (184 + self.bx, 64 + self.by)], fill='orange')
        draw.polygon([(316 + self.bx, 0 + self.by), (424 + self.bx, 0 + self.by), (436 + self.bx, 64 + self.by), (320 + self.bx, 64 + self.by)], fill='red')
        draw.polygon([(44 + self.bx, 76 + self.by), (162 + self.bx, 76 + self.by), (156 + self.bx, 152 + self.by), (30 + self.bx, 152 + self.by)], fill='green')
        draw.polygon([(184 + self.bx, 76 + self.by), (300 + self.bx, 76 + self.by), (304 + self.bx, 150 + self.by), (180 + self.bx, 150 + self.by)], fill='yellow')
        draw.polygon([(322 + self.bx, 76 + self.by), (440 + self.bx, 76 + self.by), (452 + self.bx, 152 + self.by), (328 + self.bx, 152 + self.by)], fill='green')
        draw.polygon([(28 + self.bx, 166 + self.by), (156 + self.bx, 166 + self.by), (148 + self.bx, 256 + self.by), (10 + self.bx, 256 + self.by)], fill='yellow')
        draw.polygon([(178 + self.bx, 166 + self.by), (306 + self.bx, 166 + self.by), (310 + self.bx, 254 + self.by), (174 + self.bx, 254 + self.by)], fill='green')
        draw.polygon([(328 + self.bx, 166 + self.by), (456 + self.bx, 166 + self.by), (474 + self.bx, 254 + self.by), (336 + self.bx, 254 + self.by)], fill='white')
    
    def drawEdgesExample1(self, draw):
        # white side (D)
        draw.polygon([(74 + self.bx, 438 + self.by), (174 + self.bx, 438 + self.by), (170 + self.bx, 522 + self.by), (66 + self.bx, 522 + self.by)], fill='white')
        draw.polygon([(192 + self.bx, 438 + self.by), (294 + self.bx, 438 + self.by), (298 + self.bx, 522 + self.by), (188 + self.bx, 522 + self.by)], fill='white')
        draw.polygon([(310 + self.bx, 436 + self.by), (410 + self.bx, 436 + self.by), (414 + self.bx, 524 + self.by), (314 + self.bx, 524 + self.by)], fill='white')
        draw.polygon([(84 + self.bx, 348 + self.by), (178 + self.bx, 348 + self.by), (174 + self.bx, 422 + self.by), (76 + self.bx, 422 + self.by)], fill='white')
        draw.polygon([(196 + self.bx, 348 + self.by), (288 + self.bx, 348 + self.by), (292 + self.bx, 424 + self.by), (192 + self.bx, 424 + self.by)], fill='white')
        draw.polygon([(306 + self.bx, 348 + self.by), (400 + self.bx, 348 + self.by), (404 + self.bx, 424 + self.by), (310 + self.bx, 424 + self.by)], fill='white')
        draw.polygon([(94 + self.bx, 270 + self.by), (182 + self.bx, 270 + self.by), (178 + self.bx, 336 + self.by), (84 + self.bx, 336 + self.by)], fill='white')
        draw.polygon([(198 + self.bx, 270 + self.by), (286 + self.bx, 270 + self.by), (290 + self.bx, 336 + self.by), (194 + self.bx, 336 + self.by)], fill='white')
        draw.polygon([(302 + self.bx, 268 + self.by), (390 + self.bx, 268 + self.by), (398 + self.bx, 336 + self.by), (306 + self.bx, 336 + self.by)], fill='white')
        
        # red side (B)
        draw.polygon([(414 + self.bx, 2 + self.by), (314 + self.bx, 2 + self.by), (310 + self.bx, 90 + self.by), (410 + self.bx, 90 + self.by)], fill='yellow')
        draw.polygon([(298 + self.bx, 4 + self.by), (188 + self.bx, 4 + self.by), (192 + self.bx, 88 + self.by), (292 + self.bx, 88 + self.by)], fill='blue')
        draw.polygon([(170 + self.bx, 4 + self.by), (66 + self.bx, 4 + self.by), (74 + self.bx, 88 + self.by), (174 + self.bx, 88 + self.by)], fill='yellow')
        draw.polygon([(404 + self.bx, 102 + self.by), (310 + self.bx, 102 + self.by), (306 + self.bx, 178 + self.by), (400 + self.bx, 178 + self.by)], fill='yellow')
        draw.polygon([(292 + self.bx, 102 + self.by), (192 + self.bx, 102 + self.by), (196 + self.bx, 178 + self.by), (288 + self.bx, 178 + self.by)], fill='orange')
        draw.polygon([(174 + self.bx, 104 + self.by), (76 + self.bx, 104 + self.by), (84 + self.bx, 178 + self.by), (178 + self.bx, 178 + self.by)], fill='blue')
        draw.polygon([(398 + self.bx, 190 + self.by), (306 + self.bx, 190 + self.by), (302 + self.bx, 258 + self.by), (390 + self.bx, 258 + self.by)], fill='orange')
        draw.polygon([(290 + self.bx, 190 + self.by), (194 + self.bx, 190 + self.by), (198 + self.bx, 256 + self.by), (286 + self.bx, 256 + self.by)], fill='orange')
        draw.polygon([(178 + self.bx, 190 + self.by), (84 + self.bx, 190 + self.by), (94 + self.bx, 256 + self.by), (182 + self.bx, 256 + self.by)], fill='orange')
        
        # green side (L)
        draw.polygon([(52 + self.bx, 158 + self.by), (38 + self.bx, 74 + self.by), (50 + self.bx, 12 + self.by), (62 + self.bx, 84 + self.by)], fill='orange')
        draw.polygon([(20 + self.bx, 162 + self.by), (36 + self.bx, 86 + self.by), (48 + self.bx, 164 + self.by), (36 + self.bx, 246 + self.by)], fill='green')
        draw.polygon([(0 + self.bx, 264 + self.by), (18 + self.bx, 174 + self.by), (34 + self.bx, 264 + self.by), (18 + self.bx, 352 + self.by)], fill='orange')
        draw.polygon([(66 + self.bx, 100 + self.by), (56 + self.bx, 166 + self.by), (64 + self.bx, 240 + self.by), (74 + self.bx, 164 + self.by)], fill='yellow')
        draw.polygon([(52 + self.bx, 352 + self.by), (62 + self.bx, 264 + self.by), (52 + self.bx, 180 + self.by), (38 + self.bx, 264 + self.by)], fill='blue')
        draw.polygon([(22 + self.bx, 364 + self.by), (36 + self.bx, 440 + self.by), (48 + self.bx, 366 + self.by), (36 + self.bx, 282 + self.by)], fill='yellow')
        draw.polygon([(80 + self.bx, 354 + self.by), (66 + self.bx, 264 + self.by), (76 + self.bx, 180 + self.by), (86 + self.bx, 264 + self.by)], fill='blue')
        draw.polygon([(56 + self.bx, 362 + self.by), (66 + self.bx, 438 + self.by), (74 + self.bx, 360 + self.by), (64 + self.bx, 292 + self.by)], fill='blue')
        draw.polygon([(40 + self.bx, 454 + self.by), (52 + self.bx, 370 + self.by), (62 + self.bx, 442 + self.by), (52 + self.bx, 514 + self.by)], fill='blue')
        
        # blue side (R)
        draw.polygon([(484 + self.bx, 264 + self.by), (466 + self.bx, 174 + self.by), (450 + self.bx, 264 + self.by), (466 + self.bx, 352 + self.by)], fill='red')
        draw.polygon([(464 + self.bx, 162 + self.by), (448 + self.bx, 86 + self.by), (436 + self.bx, 164 + self.by), (448 + self.bx, 246 + self.by)], fill='blue')
        draw.polygon([(432 + self.bx, 158 + self.by), (446 + self.bx, 74 + self.by), (434 + self.bx, 12 + self.by), (422 + self.bx, 84 + self.by)], fill='red')
        draw.polygon([(462 + self.bx, 364 + self.by), (448 + self.bx, 440 + self.by), (436 + self.bx, 366 + self.by), (446 + self.bx, 282 + self.by)], fill='yellow')
        draw.polygon([(432 + self.bx, 352 + self.by), (422 + self.bx, 264 + self.by), (432 + self.bx, 180 + self.by), (446 + self.bx, 264 + self.by)], fill='green')
        draw.polygon([(418 + self.bx, 100 + self.by), (428 + self.bx, 166 + self.by), (420 + self.bx, 240 + self.by), (410 + self.bx, 164 + self.by)], fill='green')
        draw.polygon([(444 + self.bx, 454 + self.by), (432 + self.bx, 370 + self.by), (422 + self.bx, 442 + self.by), (432 + self.bx, 514 + self.by)], fill='green')
        draw.polygon([(428 + self.bx, 362 + self.by), (418 + self.bx, 438 + self.by), (410 + self.bx, 360 + self.by), (420 + self.bx, 292 + self.by)], fill='green')
        draw.polygon([(404 + self.bx, 354 + self.by), (418 + self.bx, 264 + self.by), (408 + self.bx, 180 + self.by), (398 + self.bx, 264 + self.by)], fill='green')
        
        # orange side (F)
        draw.polygon([(10 + self.bx, 272 + self.by), (148 + self.bx, 272 + self.by), (156 + self.bx, 362 + self.by), (28 + self.bx, 362 + self.by)], fill='yellow')
        draw.polygon([(172 + self.bx, 272 + self.by), (312 + self.bx, 272 + self.by), (306 + self.bx, 362 + self.by), (178 + self.bx, 362 + self.by)], fill='red')
        draw.polygon([(336 + self.bx, 272 + self.by), (474 + self.bx, 272 + self.by), (456 + self.bx, 362 + self.by), (328 + self.bx, 362 + self.by)], fill='yellow')
        draw.polygon([(32 + self.bx, 376 + self.by), (158 + self.bx, 376 + self.by), (164 + self.bx, 450 + self.by), (46 + self.bx, 450 + self.by)], fill='red')
        draw.polygon([(180 + self.bx, 376 + self.by), (304 + self.bx, 376 + self.by), (300 + self.bx, 450 + self.by), (184 + self.bx, 450 + self.by)], fill='red')
        draw.polygon([(328 + self.bx, 376 + self.by), (452 + self.bx, 376 + self.by), (438 + self.bx, 450 + self.by), (320 + self.bx, 450 + self.by)], fill='orange')
        draw.polygon([(48 + self.bx, 464 + self.by), (164 + self.bx, 464 + self.by), (170 + self.bx, 526 + self.by), (62 + self.bx, 526 + self.by)], fill='red')
        draw.polygon([(186 + self.bx, 464 + self.by), (298 + self.bx, 464 + self.by), (296 + self.bx, 526 + self.by), (188 + self.bx, 526 + self.by)], fill='red')
        draw.polygon([(320 + self.bx, 462 + self.by), (436 + self.bx, 462 + self.by), (422 + self.bx, 526 + self.by), (314 + self.bx, 526 + self.by)], fill='red')
        
        # yellow side (U)
        draw.polygon([(60 + self.bx, 0 + self.by), (168 + self.bx, 0 + self.by), (164 + self.bx, 64 + self.by), (48 + self.bx, 64 + self.by)], fill='blue')
        draw.polygon([(188 + self.bx, 0 + self.by), (296 + self.bx, 0 + self.by), (300 + self.bx, 64 + self.by), (184 + self.bx, 64 + self.by)], fill='orange')
        draw.polygon([(316 + self.bx, 0 + self.by), (424 + self.bx, 0 + self.by), (436 + self.bx, 64 + self.by), (320 + self.bx, 64 + self.by)], fill='blue')
        draw.polygon([(44 + self.bx, 76 + self.by), (162 + self.bx, 76 + self.by), (156 + self.bx, 152 + self.by), (30 + self.bx, 152 + self.by)], fill='orange')
        draw.polygon([(184 + self.bx, 76 + self.by), (300 + self.bx, 76 + self.by), (304 + self.bx, 150 + self.by), (180 + self.bx, 150 + self.by)], fill='yellow')
        draw.polygon([(322 + self.bx, 76 + self.by), (440 + self.bx, 76 + self.by), (452 + self.bx, 152 + self.by), (328 + self.bx, 152 + self.by)], fill='red')
        draw.polygon([(28 + self.bx, 166 + self.by), (156 + self.bx, 166 + self.by), (148 + self.bx, 256 + self.by), (10 + self.bx, 256 + self.by)], fill='green')
        draw.polygon([(178 + self.bx, 166 + self.by), (306 + self.bx, 166 + self.by), (310 + self.bx, 254 + self.by), (174 + self.bx, 254 + self.by)], fill='green')
        draw.polygon([(328 + self.bx, 166 + self.by), (456 + self.bx, 166 + self.by), (474 + self.bx, 254 + self.by), (336 + self.bx, 254 + self.by)], fill='green')

    def drawEdgesExample2(self, draw):
        # white side (D)
        draw.polygon([(74 + self.bx, 438 + self.by), (174 + self.bx, 438 + self.by), (170 + self.bx, 522 + self.by), (66 + self.bx, 522 + self.by)], fill='white')
        draw.polygon([(192 + self.bx, 438 + self.by), (294 + self.bx, 438 + self.by), (298 + self.bx, 522 + self.by), (188 + self.bx, 522 + self.by)], fill='white')
        draw.polygon([(310 + self.bx, 436 + self.by), (410 + self.bx, 436 + self.by), (414 + self.bx, 524 + self.by), (314 + self.bx, 524 + self.by)], fill='white')
        draw.polygon([(84 + self.bx, 348 + self.by), (178 + self.bx, 348 + self.by), (174 + self.bx, 422 + self.by), (76 + self.bx, 422 + self.by)], fill='white')
        draw.polygon([(196 + self.bx, 348 + self.by), (288 + self.bx, 348 + self.by), (292 + self.bx, 424 + self.by), (192 + self.bx, 424 + self.by)], fill='white')
        draw.polygon([(306 + self.bx, 348 + self.by), (400 + self.bx, 348 + self.by), (404 + self.bx, 424 + self.by), (310 + self.bx, 424 + self.by)], fill='white')
        draw.polygon([(94 + self.bx, 270 + self.by), (182 + self.bx, 270 + self.by), (178 + self.bx, 336 + self.by), (84 + self.bx, 336 + self.by)], fill='white')
        draw.polygon([(198 + self.bx, 270 + self.by), (286 + self.bx, 270 + self.by), (290 + self.bx, 336 + self.by), (194 + self.bx, 336 + self.by)], fill='white')
        draw.polygon([(302 + self.bx, 268 + self.by), (390 + self.bx, 268 + self.by), (398 + self.bx, 336 + self.by), (306 + self.bx, 336 + self.by)], fill='white')
        
        # red side (B)
        draw.polygon([(414 + self.bx, 2 + self.by), (314 + self.bx, 2 + self.by), (310 + self.bx, 90 + self.by), (410 + self.bx, 90 + self.by)], fill='yellow')
        draw.polygon([(298 + self.bx, 4 + self.by), (188 + self.bx, 4 + self.by), (192 + self.bx, 88 + self.by), (292 + self.bx, 88 + self.by)], fill='red')
        draw.polygon([(170 + self.bx, 4 + self.by), (66 + self.bx, 4 + self.by), (74 + self.bx, 88 + self.by), (174 + self.bx, 88 + self.by)], fill='yellow')
        draw.polygon([(404 + self.bx, 102 + self.by), (310 + self.bx, 102 + self.by), (306 + self.bx, 178 + self.by), (400 + self.bx, 178 + self.by)], fill='yellow')
        draw.polygon([(292 + self.bx, 102 + self.by), (192 + self.bx, 102 + self.by), (196 + self.bx, 178 + self.by), (288 + self.bx, 178 + self.by)], fill='green')
        draw.polygon([(174 + self.bx, 104 + self.by), (76 + self.bx, 104 + self.by), (84 + self.bx, 178 + self.by), (178 + self.bx, 178 + self.by)], fill='green')
        draw.polygon([(398 + self.bx, 190 + self.by), (306 + self.bx, 190 + self.by), (302 + self.bx, 258 + self.by), (390 + self.bx, 258 + self.by)], fill='green')
        draw.polygon([(290 + self.bx, 190 + self.by), (194 + self.bx, 190 + self.by), (198 + self.bx, 256 + self.by), (286 + self.bx, 256 + self.by)], fill='green')
        draw.polygon([(178 + self.bx, 190 + self.by), (84 + self.bx, 190 + self.by), (94 + self.bx, 256 + self.by), (182 + self.bx, 256 + self.by)], fill='green')
        
        # green side (L)
        draw.polygon([(52 + self.bx, 158 + self.by), (38 + self.bx, 74 + self.by), (50 + self.bx, 12 + self.by), (62 + self.bx, 84 + self.by)], fill='red')
        draw.polygon([(20 + self.bx, 162 + self.by), (36 + self.bx, 86 + self.by), (48 + self.bx, 164 + self.by), (36 + self.bx, 246 + self.by)], fill='blue')
        draw.polygon([(0 + self.bx, 264 + self.by), (18 + self.bx, 174 + self.by), (34 + self.bx, 264 + self.by), (18 + self.bx, 352 + self.by)], fill='red')
        draw.polygon([(66 + self.bx, 100 + self.by), (56 + self.bx, 166 + self.by), (64 + self.bx, 240 + self.by), (74 + self.bx, 164 + self.by)], fill='yellow')
        draw.polygon([(52 + self.bx, 352 + self.by), (62 + self.bx, 264 + self.by), (52 + self.bx, 180 + self.by), (38 + self.bx, 264 + self.by)], fill='orange')
        draw.polygon([(22 + self.bx, 364 + self.by), (36 + self.bx, 440 + self.by), (48 + self.bx, 366 + self.by), (36 + self.bx, 282 + self.by)], fill='blue')
        draw.polygon([(80 + self.bx, 354 + self.by), (66 + self.bx, 264 + self.by), (76 + self.bx, 180 + self.by), (86 + self.bx, 264 + self.by)], fill='orange')
        draw.polygon([(56 + self.bx, 362 + self.by), (66 + self.bx, 438 + self.by), (74 + self.bx, 360 + self.by), (64 + self.bx, 292 + self.by)], fill='orange')
        draw.polygon([(40 + self.bx, 454 + self.by), (52 + self.bx, 370 + self.by), (62 + self.bx, 442 + self.by), (52 + self.bx, 514 + self.by)], fill='orange')
        
        # blue side (R)
        draw.polygon([(484 + self.bx, 264 + self.by), (466 + self.bx, 174 + self.by), (450 + self.bx, 264 + self.by), (466 + self.bx, 352 + self.by)], fill='orange')
        draw.polygon([(464 + self.bx, 162 + self.by), (448 + self.bx, 86 + self.by), (436 + self.bx, 164 + self.by), (448 + self.bx, 246 + self.by)], fill='green')
        draw.polygon([(432 + self.bx, 158 + self.by), (446 + self.bx, 74 + self.by), (434 + self.bx, 12 + self.by), (422 + self.bx, 84 + self.by)], fill='orange')
        draw.polygon([(462 + self.bx, 364 + self.by), (448 + self.bx, 440 + self.by), (436 + self.bx, 366 + self.by), (446 + self.bx, 282 + self.by)], fill='red')
        draw.polygon([(432 + self.bx, 352 + self.by), (422 + self.bx, 264 + self.by), (432 + self.bx, 180 + self.by), (446 + self.bx, 264 + self.by)], fill='red')
        draw.polygon([(418 + self.bx, 100 + self.by), (428 + self.bx, 166 + self.by), (420 + self.bx, 240 + self.by), (410 + self.bx, 164 + self.by)], fill='orange')
        draw.polygon([(444 + self.bx, 454 + self.by), (432 + self.bx, 370 + self.by), (422 + self.bx, 442 + self.by), (432 + self.bx, 514 + self.by)], fill='red')
        draw.polygon([(428 + self.bx, 362 + self.by), (418 + self.bx, 438 + self.by), (410 + self.bx, 360 + self.by), (420 + self.bx, 292 + self.by)], fill='red')
        draw.polygon([(404 + self.bx, 354 + self.by), (418 + self.bx, 264 + self.by), (408 + self.bx, 180 + self.by), (398 + self.bx, 264 + self.by)], fill='red')
        
        # orange side (F)
        draw.polygon([(10 + self.bx, 272 + self.by), (148 + self.bx, 272 + self.by), (156 + self.bx, 362 + self.by), (28 + self.bx, 362 + self.by)], fill='yellow')
        draw.polygon([(172 + self.bx, 272 + self.by), (312 + self.bx, 272 + self.by), (306 + self.bx, 362 + self.by), (178 + self.bx, 362 + self.by)], fill='blue')
        draw.polygon([(336 + self.bx, 272 + self.by), (474 + self.bx, 272 + self.by), (456 + self.bx, 362 + self.by), (328 + self.bx, 362 + self.by)], fill='yellow')
        draw.polygon([(32 + self.bx, 376 + self.by), (158 + self.bx, 376 + self.by), (164 + self.bx, 450 + self.by), (46 + self.bx, 450 + self.by)], fill='yellow')
        draw.polygon([(180 + self.bx, 376 + self.by), (304 + self.bx, 376 + self.by), (300 + self.bx, 450 + self.by), (184 + self.bx, 450 + self.by)], fill='blue')
        draw.polygon([(328 + self.bx, 376 + self.by), (452 + self.bx, 376 + self.by), (438 + self.bx, 450 + self.by), (320 + self.bx, 450 + self.by)], fill='yellow')
        draw.polygon([(48 + self.bx, 464 + self.by), (164 + self.bx, 464 + self.by), (170 + self.bx, 526 + self.by), (62 + self.bx, 526 + self.by)], fill='blue')
        draw.polygon([(186 + self.bx, 464 + self.by), (298 + self.bx, 464 + self.by), (296 + self.bx, 526 + self.by), (188 + self.bx, 526 + self.by)], fill='blue')
        draw.polygon([(320 + self.bx, 462 + self.by), (436 + self.bx, 462 + self.by), (422 + self.bx, 526 + self.by), (314 + self.bx, 526 + self.by)], fill='blue')
        
        # yellow side (U)
        draw.polygon([(60 + self.bx, 0 + self.by), (168 + self.bx, 0 + self.by), (164 + self.bx, 64 + self.by), (48 + self.bx, 64 + self.by)], fill='green')
        draw.polygon([(188 + self.bx, 0 + self.by), (296 + self.bx, 0 + self.by), (300 + self.bx, 64 + self.by), (184 + self.bx, 64 + self.by)], fill='green')
        draw.polygon([(316 + self.bx, 0 + self.by), (424 + self.bx, 0 + self.by), (436 + self.bx, 64 + self.by), (320 + self.bx, 64 + self.by)], fill='green')
        draw.polygon([(44 + self.bx, 76 + self.by), (162 + self.bx, 76 + self.by), (156 + self.bx, 152 + self.by), (30 + self.bx, 152 + self.by)], fill='red')
        draw.polygon([(184 + self.bx, 76 + self.by), (300 + self.bx, 76 + self.by), (304 + self.bx, 150 + self.by), (180 + self.bx, 150 + self.by)], fill='yellow')
        draw.polygon([(322 + self.bx, 76 + self.by), (440 + self.bx, 76 + self.by), (452 + self.bx, 152 + self.by), (328 + self.bx, 152 + self.by)], fill='orange')
        draw.polygon([(28 + self.bx, 166 + self.by), (156 + self.bx, 166 + self.by), (148 + self.bx, 256 + self.by), (10 + self.bx, 256 + self.by)], fill='blue')
        draw.polygon([(178 + self.bx, 166 + self.by), (306 + self.bx, 166 + self.by), (310 + self.bx, 254 + self.by), (174 + self.bx, 254 + self.by)], fill='orange')
        draw.polygon([(328 + self.bx, 166 + self.by), (456 + self.bx, 166 + self.by), (474 + self.bx, 254 + self.by), (336 + self.bx, 254 + self.by)], fill='blue')
    
    def drawEOLL1(self, draw):
        # white side (D)
        draw.polygon([(74 + self.bx, 438 + self.by), (174 + self.bx, 438 + self.by), (170 + self.bx, 522 + self.by), (66 + self.bx, 522 + self.by)], fill='white')
        draw.polygon([(192 + self.bx, 438 + self.by), (294 + self.bx, 438 + self.by), (298 + self.bx, 522 + self.by), (188 + self.bx, 522 + self.by)], fill='white')
        draw.polygon([(310 + self.bx, 436 + self.by), (410 + self.bx, 436 + self.by), (414 + self.bx, 524 + self.by), (314 + self.bx, 524 + self.by)], fill='white')
        draw.polygon([(84 + self.bx, 348 + self.by), (178 + self.bx, 348 + self.by), (174 + self.bx, 422 + self.by), (76 + self.bx, 422 + self.by)], fill='white')
        draw.polygon([(196 + self.bx, 348 + self.by), (288 + self.bx, 348 + self.by), (292 + self.bx, 424 + self.by), (192 + self.bx, 424 + self.by)], fill='white')
        draw.polygon([(306 + self.bx, 348 + self.by), (400 + self.bx, 348 + self.by), (404 + self.bx, 424 + self.by), (310 + self.bx, 424 + self.by)], fill='white')
        draw.polygon([(94 + self.bx, 270 + self.by), (182 + self.bx, 270 + self.by), (178 + self.bx, 336 + self.by), (84 + self.bx, 336 + self.by)], fill='white')
        draw.polygon([(198 + self.bx, 270 + self.by), (286 + self.bx, 270 + self.by), (290 + self.bx, 336 + self.by), (194 + self.bx, 336 + self.by)], fill='white')
        draw.polygon([(302 + self.bx, 268 + self.by), (390 + self.bx, 268 + self.by), (398 + self.bx, 336 + self.by), (306 + self.bx, 336 + self.by)], fill='white')
        
        # red side (B)
        draw.polygon([(414 + self.bx, 2 + self.by), (314 + self.bx, 2 + self.by), (310 + self.bx, 90 + self.by), (410 + self.bx, 90 + self.by)], fill='yellow')
        draw.polygon([(298 + self.bx, 4 + self.by), (188 + self.bx, 4 + self.by), (192 + self.bx, 88 + self.by), (292 + self.bx, 88 + self.by)], fill='yellow')
        draw.polygon([(170 + self.bx, 4 + self.by), (66 + self.bx, 4 + self.by), (74 + self.bx, 88 + self.by), (174 + self.bx, 88 + self.by)], fill='orange')
        draw.polygon([(404 + self.bx, 102 + self.by), (310 + self.bx, 102 + self.by), (306 + self.bx, 178 + self.by), (400 + self.bx, 178 + self.by)], fill='green')
        draw.polygon([(292 + self.bx, 102 + self.by), (192 + self.bx, 102 + self.by), (196 + self.bx, 178 + self.by), (288 + self.bx, 178 + self.by)], fill='green')
        draw.polygon([(174 + self.bx, 104 + self.by), (76 + self.bx, 104 + self.by), (84 + self.bx, 178 + self.by), (178 + self.bx, 178 + self.by)], fill='green')
        draw.polygon([(398 + self.bx, 190 + self.by), (306 + self.bx, 190 + self.by), (302 + self.bx, 258 + self.by), (390 + self.bx, 258 + self.by)], fill='green')
        draw.polygon([(290 + self.bx, 190 + self.by), (194 + self.bx, 190 + self.by), (198 + self.bx, 256 + self.by), (286 + self.bx, 256 + self.by)], fill='green')
        draw.polygon([(178 + self.bx, 190 + self.by), (84 + self.bx, 190 + self.by), (94 + self.bx, 256 + self.by), (182 + self.bx, 256 + self.by)], fill='green')
        
        # green side (L)
        draw.polygon([(52 + self.bx, 158 + self.by), (38 + self.bx, 74 + self.by), (50 + self.bx, 12 + self.by), (62 + self.bx, 84 + self.by)], fill='red')
        draw.polygon([(20 + self.bx, 162 + self.by), (36 + self.bx, 86 + self.by), (48 + self.bx, 164 + self.by), (36 + self.bx, 246 + self.by)], fill='yellow')
        draw.polygon([(0 + self.bx, 264 + self.by), (18 + self.bx, 174 + self.by), (34 + self.bx, 264 + self.by), (18 + self.bx, 352 + self.by)], fill='green')
        draw.polygon([(66 + self.bx, 100 + self.by), (56 + self.bx, 166 + self.by), (64 + self.bx, 240 + self.by), (74 + self.bx, 164 + self.by)], fill='orange')
        draw.polygon([(52 + self.bx, 352 + self.by), (62 + self.bx, 264 + self.by), (52 + self.bx, 180 + self.by), (38 + self.bx, 264 + self.by)], fill='orange')
        draw.polygon([(22 + self.bx, 364 + self.by), (36 + self.bx, 440 + self.by), (48 + self.bx, 366 + self.by), (36 + self.bx, 282 + self.by)], fill='orange')
        draw.polygon([(80 + self.bx, 354 + self.by), (66 + self.bx, 264 + self.by), (76 + self.bx, 180 + self.by), (86 + self.bx, 264 + self.by)], fill='orange')
        draw.polygon([(56 + self.bx, 362 + self.by), (66 + self.bx, 438 + self.by), (74 + self.bx, 360 + self.by), (64 + self.bx, 292 + self.by)], fill='orange')
        draw.polygon([(40 + self.bx, 454 + self.by), (52 + self.bx, 370 + self.by), (62 + self.bx, 442 + self.by), (52 + self.bx, 514 + self.by)], fill='orange')
        
        # blue side (R)
        draw.polygon([(484 + self.bx, 264 + self.by), (466 + self.bx, 174 + self.by), (450 + self.bx, 264 + self.by), (466 + self.bx, 352 + self.by)], fill='red')
        draw.polygon([(464 + self.bx, 162 + self.by), (448 + self.bx, 86 + self.by), (436 + self.bx, 164 + self.by), (448 + self.bx, 246 + self.by)], fill='yellow')
        draw.polygon([(432 + self.bx, 158 + self.by), (446 + self.bx, 74 + self.by), (434 + self.bx, 12 + self.by), (422 + self.bx, 84 + self.by)], fill='blue')
        draw.polygon([(462 + self.bx, 364 + self.by), (448 + self.bx, 440 + self.by), (436 + self.bx, 366 + self.by), (446 + self.bx, 282 + self.by)], fill='red')
        draw.polygon([(432 + self.bx, 352 + self.by), (422 + self.bx, 264 + self.by), (432 + self.bx, 180 + self.by), (446 + self.bx, 264 + self.by)], fill='red')
        draw.polygon([(418 + self.bx, 100 + self.by), (428 + self.bx, 166 + self.by), (420 + self.bx, 240 + self.by), (410 + self.bx, 164 + self.by)], fill='red')
        draw.polygon([(444 + self.bx, 454 + self.by), (432 + self.bx, 370 + self.by), (422 + self.bx, 442 + self.by), (432 + self.bx, 514 + self.by)], fill='red')
        draw.polygon([(428 + self.bx, 362 + self.by), (418 + self.bx, 438 + self.by), (410 + self.bx, 360 + self.by), (420 + self.bx, 292 + self.by)], fill='red')
        draw.polygon([(404 + self.bx, 354 + self.by), (418 + self.bx, 264 + self.by), (408 + self.bx, 180 + self.by), (398 + self.bx, 264 + self.by)], fill='red')
        
        # orange side (F)
        draw.polygon([(10 + self.bx, 272 + self.by), (148 + self.bx, 272 + self.by), (156 + self.bx, 362 + self.by), (28 + self.bx, 362 + self.by)], fill='yellow')
        draw.polygon([(172 + self.bx, 272 + self.by), (312 + self.bx, 272 + self.by), (306 + self.bx, 362 + self.by), (178 + self.bx, 362 + self.by)], fill='yellow')
        draw.polygon([(336 + self.bx, 272 + self.by), (474 + self.bx, 272 + self.by), (456 + self.bx, 362 + self.by), (328 + self.bx, 362 + self.by)], fill='blue')
        draw.polygon([(32 + self.bx, 376 + self.by), (158 + self.bx, 376 + self.by), (164 + self.bx, 450 + self.by), (46 + self.bx, 450 + self.by)], fill='blue')
        draw.polygon([(180 + self.bx, 376 + self.by), (304 + self.bx, 376 + self.by), (300 + self.bx, 450 + self.by), (184 + self.bx, 450 + self.by)], fill='blue')
        draw.polygon([(328 + self.bx, 376 + self.by), (452 + self.bx, 376 + self.by), (438 + self.bx, 450 + self.by), (320 + self.bx, 450 + self.by)], fill='blue')
        draw.polygon([(48 + self.bx, 464 + self.by), (164 + self.bx, 464 + self.by), (170 + self.bx, 526 + self.by), (62 + self.bx, 526 + self.by)], fill='blue')
        draw.polygon([(186 + self.bx, 464 + self.by), (298 + self.bx, 464 + self.by), (296 + self.bx, 526 + self.by), (188 + self.bx, 526 + self.by)], fill='blue')
        draw.polygon([(320 + self.bx, 462 + self.by), (436 + self.bx, 462 + self.by), (422 + self.bx, 526 + self.by), (314 + self.bx, 526 + self.by)], fill='blue')
        
        # yellow side (U)
        draw.polygon([(60 + self.bx, 0 + self.by), (168 + self.bx, 0 + self.by), (164 + self.bx, 64 + self.by), (48 + self.bx, 64 + self.by)], fill='green')
        draw.polygon([(188 + self.bx, 0 + self.by), (296 + self.bx, 0 + self.by), (300 + self.bx, 64 + self.by), (184 + self.bx, 64 + self.by)], fill='green')
        draw.polygon([(316 + self.bx, 0 + self.by), (424 + self.bx, 0 + self.by), (436 + self.bx, 64 + self.by), (320 + self.bx, 64 + self.by)], fill='orange')
        draw.polygon([(44 + self.bx, 76 + self.by), (162 + self.bx, 76 + self.by), (156 + self.bx, 152 + self.by), (30 + self.bx, 152 + self.by)], fill='orange')
        draw.polygon([(184 + self.bx, 76 + self.by), (300 + self.bx, 76 + self.by), (304 + self.bx, 150 + self.by), (180 + self.bx, 150 + self.by)], fill='yellow')
        draw.polygon([(322 + self.bx, 76 + self.by), (440 + self.bx, 76 + self.by), (452 + self.bx, 152 + self.by), (328 + self.bx, 152 + self.by)], fill='blue')
        draw.polygon([(28 + self.bx, 166 + self.by), (156 + self.bx, 166 + self.by), (148 + self.bx, 256 + self.by), (10 + self.bx, 256 + self.by)], fill='red')
        draw.polygon([(178 + self.bx, 166 + self.by), (306 + self.bx, 166 + self.by), (310 + self.bx, 254 + self.by), (174 + self.bx, 254 + self.by)], fill='red')
        draw.polygon([(328 + self.bx, 166 + self.by), (456 + self.bx, 166 + self.by), (474 + self.bx, 254 + self.by), (336 + self.bx, 254 + self.by)], fill='yellow')

    def drawEOLL2(self, draw):
        # white side (D)
        draw.polygon([(74 + self.bx, 438 + self.by), (174 + self.bx, 438 + self.by), (170 + self.bx, 522 + self.by), (66 + self.bx, 522 + self.by)], fill='white')
        draw.polygon([(192 + self.bx, 438 + self.by), (294 + self.bx, 438 + self.by), (298 + self.bx, 522 + self.by), (188 + self.bx, 522 + self.by)], fill='white')
        draw.polygon([(310 + self.bx, 436 + self.by), (410 + self.bx, 436 + self.by), (414 + self.bx, 524 + self.by), (314 + self.bx, 524 + self.by)], fill='white')
        draw.polygon([(84 + self.bx, 348 + self.by), (178 + self.bx, 348 + self.by), (174 + self.bx, 422 + self.by), (76 + self.bx, 422 + self.by)], fill='white')
        draw.polygon([(196 + self.bx, 348 + self.by), (288 + self.bx, 348 + self.by), (292 + self.bx, 424 + self.by), (192 + self.bx, 424 + self.by)], fill='white')
        draw.polygon([(306 + self.bx, 348 + self.by), (400 + self.bx, 348 + self.by), (404 + self.bx, 424 + self.by), (310 + self.bx, 424 + self.by)], fill='white')
        draw.polygon([(94 + self.bx, 270 + self.by), (182 + self.bx, 270 + self.by), (178 + self.bx, 336 + self.by), (84 + self.bx, 336 + self.by)], fill='white')
        draw.polygon([(198 + self.bx, 270 + self.by), (286 + self.bx, 270 + self.by), (290 + self.bx, 336 + self.by), (194 + self.bx, 336 + self.by)], fill='white')
        draw.polygon([(302 + self.bx, 268 + self.by), (390 + self.bx, 268 + self.by), (398 + self.bx, 336 + self.by), (306 + self.bx, 336 + self.by)], fill='white')
        
        # red side (B)
        draw.polygon([(414 + self.bx, 2 + self.by), (314 + self.bx, 2 + self.by), (310 + self.bx, 90 + self.by), (410 + self.bx, 90 + self.by)], fill='red')
        draw.polygon([(298 + self.bx, 4 + self.by), (188 + self.bx, 4 + self.by), (192 + self.bx, 88 + self.by), (292 + self.bx, 88 + self.by)], fill='green')
        draw.polygon([(170 + self.bx, 4 + self.by), (66 + self.bx, 4 + self.by), (74 + self.bx, 88 + self.by), (174 + self.bx, 88 + self.by)], fill='yellow')
        draw.polygon([(404 + self.bx, 102 + self.by), (310 + self.bx, 102 + self.by), (306 + self.bx, 178 + self.by), (400 + self.bx, 178 + self.by)], fill='green')
        draw.polygon([(292 + self.bx, 102 + self.by), (192 + self.bx, 102 + self.by), (196 + self.bx, 178 + self.by), (288 + self.bx, 178 + self.by)], fill='green')
        draw.polygon([(174 + self.bx, 104 + self.by), (76 + self.bx, 104 + self.by), (84 + self.bx, 178 + self.by), (178 + self.bx, 178 + self.by)], fill='green')
        draw.polygon([(398 + self.bx, 190 + self.by), (306 + self.bx, 190 + self.by), (302 + self.bx, 258 + self.by), (390 + self.bx, 258 + self.by)], fill='green')
        draw.polygon([(290 + self.bx, 190 + self.by), (194 + self.bx, 190 + self.by), (198 + self.bx, 256 + self.by), (286 + self.bx, 256 + self.by)], fill='green')
        draw.polygon([(178 + self.bx, 190 + self.by), (84 + self.bx, 190 + self.by), (94 + self.bx, 256 + self.by), (182 + self.bx, 256 + self.by)], fill='green')
        
        # green side (L)
        draw.polygon([(52 + self.bx, 158 + self.by), (38 + self.bx, 74 + self.by), (50 + self.bx, 12 + self.by), (62 + self.bx, 84 + self.by)], fill='red')
        draw.polygon([(20 + self.bx, 162 + self.by), (36 + self.bx, 86 + self.by), (48 + self.bx, 164 + self.by), (36 + self.bx, 246 + self.by)], fill='red')
        draw.polygon([(0 + self.bx, 264 + self.by), (18 + self.bx, 174 + self.by), (34 + self.bx, 264 + self.by), (18 + self.bx, 352 + self.by)], fill='green')
        draw.polygon([(66 + self.bx, 100 + self.by), (56 + self.bx, 166 + self.by), (64 + self.bx, 240 + self.by), (74 + self.bx, 164 + self.by)], fill='orange')
        draw.polygon([(52 + self.bx, 352 + self.by), (62 + self.bx, 264 + self.by), (52 + self.bx, 180 + self.by), (38 + self.bx, 264 + self.by)], fill='orange')
        draw.polygon([(22 + self.bx, 364 + self.by), (36 + self.bx, 440 + self.by), (48 + self.bx, 366 + self.by), (36 + self.bx, 282 + self.by)], fill='orange')
        draw.polygon([(80 + self.bx, 354 + self.by), (66 + self.bx, 264 + self.by), (76 + self.bx, 180 + self.by), (86 + self.bx, 264 + self.by)], fill='orange')
        draw.polygon([(56 + self.bx, 362 + self.by), (66 + self.bx, 438 + self.by), (74 + self.bx, 360 + self.by), (64 + self.bx, 292 + self.by)], fill='orange')
        draw.polygon([(40 + self.bx, 454 + self.by), (52 + self.bx, 370 + self.by), (62 + self.bx, 442 + self.by), (52 + self.bx, 514 + self.by)], fill='orange')
        
        # blue side (R)
        draw.polygon([(484 + self.bx, 264 + self.by), (466 + self.bx, 174 + self.by), (450 + self.bx, 264 + self.by), (466 + self.bx, 352 + self.by)], fill='yellow')
        draw.polygon([(464 + self.bx, 162 + self.by), (448 + self.bx, 86 + self.by), (436 + self.bx, 164 + self.by), (448 + self.bx, 246 + self.by)], fill='yellow')
        draw.polygon([(432 + self.bx, 158 + self.by), (446 + self.bx, 74 + self.by), (434 + self.bx, 12 + self.by), (422 + self.bx, 84 + self.by)], fill='blue')
        draw.polygon([(462 + self.bx, 364 + self.by), (448 + self.bx, 440 + self.by), (436 + self.bx, 366 + self.by), (446 + self.bx, 282 + self.by)], fill='red')
        draw.polygon([(432 + self.bx, 352 + self.by), (422 + self.bx, 264 + self.by), (432 + self.bx, 180 + self.by), (446 + self.bx, 264 + self.by)], fill='red')
        draw.polygon([(418 + self.bx, 100 + self.by), (428 + self.bx, 166 + self.by), (420 + self.bx, 240 + self.by), (410 + self.bx, 164 + self.by)], fill='red')
        draw.polygon([(444 + self.bx, 454 + self.by), (432 + self.bx, 370 + self.by), (422 + self.bx, 442 + self.by), (432 + self.bx, 514 + self.by)], fill='red')
        draw.polygon([(428 + self.bx, 362 + self.by), (418 + self.bx, 438 + self.by), (410 + self.bx, 360 + self.by), (420 + self.bx, 292 + self.by)], fill='red')
        draw.polygon([(404 + self.bx, 354 + self.by), (418 + self.bx, 264 + self.by), (408 + self.bx, 180 + self.by), (398 + self.bx, 264 + self.by)], fill='red')
        
        # orange side (F)
        draw.polygon([(10 + self.bx, 272 + self.by), (148 + self.bx, 272 + self.by), (156 + self.bx, 362 + self.by), (28 + self.bx, 362 + self.by)], fill='orange')
        draw.polygon([(172 + self.bx, 272 + self.by), (312 + self.bx, 272 + self.by), (306 + self.bx, 362 + self.by), (178 + self.bx, 362 + self.by)], fill='yellow')
        draw.polygon([(336 + self.bx, 272 + self.by), (474 + self.bx, 272 + self.by), (456 + self.bx, 362 + self.by), (328 + self.bx, 362 + self.by)], fill='blue')
        draw.polygon([(32 + self.bx, 376 + self.by), (158 + self.bx, 376 + self.by), (164 + self.bx, 450 + self.by), (46 + self.bx, 450 + self.by)], fill='blue')
        draw.polygon([(180 + self.bx, 376 + self.by), (304 + self.bx, 376 + self.by), (300 + self.bx, 450 + self.by), (184 + self.bx, 450 + self.by)], fill='blue')
        draw.polygon([(328 + self.bx, 376 + self.by), (452 + self.bx, 376 + self.by), (438 + self.bx, 450 + self.by), (320 + self.bx, 450 + self.by)], fill='blue')
        draw.polygon([(48 + self.bx, 464 + self.by), (164 + self.bx, 464 + self.by), (170 + self.bx, 526 + self.by), (62 + self.bx, 526 + self.by)], fill='blue')
        draw.polygon([(186 + self.bx, 464 + self.by), (298 + self.bx, 464 + self.by), (296 + self.bx, 526 + self.by), (188 + self.bx, 526 + self.by)], fill='blue')
        draw.polygon([(320 + self.bx, 462 + self.by), (436 + self.bx, 462 + self.by), (422 + self.bx, 526 + self.by), (314 + self.bx, 526 + self.by)], fill='blue')
        
        # yellow side (U)
        draw.polygon([(60 + self.bx, 0 + self.by), (168 + self.bx, 0 + self.by), (164 + self.bx, 64 + self.by), (48 + self.bx, 64 + self.by)], fill='green')
        draw.polygon([(188 + self.bx, 0 + self.by), (296 + self.bx, 0 + self.by), (300 + self.bx, 64 + self.by), (184 + self.bx, 64 + self.by)], fill='yellow')
        draw.polygon([(316 + self.bx, 0 + self.by), (424 + self.bx, 0 + self.by), (436 + self.bx, 64 + self.by), (320 + self.bx, 64 + self.by)], fill='yellow')
        draw.polygon([(44 + self.bx, 76 + self.by), (162 + self.bx, 76 + self.by), (156 + self.bx, 152 + self.by), (30 + self.bx, 152 + self.by)], fill='yellow')
        draw.polygon([(184 + self.bx, 76 + self.by), (300 + self.bx, 76 + self.by), (304 + self.bx, 150 + self.by), (180 + self.bx, 150 + self.by)], fill='yellow')
        draw.polygon([(322 + self.bx, 76 + self.by), (440 + self.bx, 76 + self.by), (452 + self.bx, 152 + self.by), (328 + self.bx, 152 + self.by)], fill='orange')
        draw.polygon([(28 + self.bx, 166 + self.by), (156 + self.bx, 166 + self.by), (148 + self.bx, 256 + self.by), (10 + self.bx, 256 + self.by)], fill='yellow')
        draw.polygon([(178 + self.bx, 166 + self.by), (306 + self.bx, 166 + self.by), (310 + self.bx, 254 + self.by), (174 + self.bx, 254 + self.by)], fill='blue')
        draw.polygon([(328 + self.bx, 166 + self.by), (456 + self.bx, 166 + self.by), (474 + self.bx, 254 + self.by), (336 + self.bx, 254 + self.by)], fill='orange')
    
    def drawEOLL3(self, draw):
        # white side (D)
        draw.polygon([(74 + self.bx, 438 + self.by), (174 + self.bx, 438 + self.by), (170 + self.bx, 522 + self.by), (66 + self.bx, 522 + self.by)], fill='white')
        draw.polygon([(192 + self.bx, 438 + self.by), (294 + self.bx, 438 + self.by), (298 + self.bx, 522 + self.by), (188 + self.bx, 522 + self.by)], fill='white')
        draw.polygon([(310 + self.bx, 436 + self.by), (410 + self.bx, 436 + self.by), (414 + self.bx, 524 + self.by), (314 + self.bx, 524 + self.by)], fill='white')
        draw.polygon([(84 + self.bx, 348 + self.by), (178 + self.bx, 348 + self.by), (174 + self.bx, 422 + self.by), (76 + self.bx, 422 + self.by)], fill='white')
        draw.polygon([(196 + self.bx, 348 + self.by), (288 + self.bx, 348 + self.by), (292 + self.bx, 424 + self.by), (192 + self.bx, 424 + self.by)], fill='white')
        draw.polygon([(306 + self.bx, 348 + self.by), (400 + self.bx, 348 + self.by), (404 + self.bx, 424 + self.by), (310 + self.bx, 424 + self.by)], fill='white')
        draw.polygon([(94 + self.bx, 270 + self.by), (182 + self.bx, 270 + self.by), (178 + self.bx, 336 + self.by), (84 + self.bx, 336 + self.by)], fill='white')
        draw.polygon([(198 + self.bx, 270 + self.by), (286 + self.bx, 270 + self.by), (290 + self.bx, 336 + self.by), (194 + self.bx, 336 + self.by)], fill='white')
        draw.polygon([(302 + self.bx, 268 + self.by), (390 + self.bx, 268 + self.by), (398 + self.bx, 336 + self.by), (306 + self.bx, 336 + self.by)], fill='white')
        
        # red side (B)
        draw.polygon([(414 + self.bx, 2 + self.by), (314 + self.bx, 2 + self.by), (310 + self.bx, 90 + self.by), (410 + self.bx, 90 + self.by)], fill='orange')
        draw.polygon([(298 + self.bx, 4 + self.by), (188 + self.bx, 4 + self.by), (192 + self.bx, 88 + self.by), (292 + self.bx, 88 + self.by)], fill='yellow')
        draw.polygon([(170 + self.bx, 4 + self.by), (66 + self.bx, 4 + self.by), (74 + self.bx, 88 + self.by), (174 + self.bx, 88 + self.by)], fill='yellow')
        draw.polygon([(404 + self.bx, 102 + self.by), (310 + self.bx, 102 + self.by), (306 + self.bx, 178 + self.by), (400 + self.bx, 178 + self.by)], fill='green')
        draw.polygon([(292 + self.bx, 102 + self.by), (192 + self.bx, 102 + self.by), (196 + self.bx, 178 + self.by), (288 + self.bx, 178 + self.by)], fill='green')
        draw.polygon([(174 + self.bx, 104 + self.by), (76 + self.bx, 104 + self.by), (84 + self.bx, 178 + self.by), (178 + self.bx, 178 + self.by)], fill='green')
        draw.polygon([(398 + self.bx, 190 + self.by), (306 + self.bx, 190 + self.by), (302 + self.bx, 258 + self.by), (390 + self.bx, 258 + self.by)], fill='green')
        draw.polygon([(290 + self.bx, 190 + self.by), (194 + self.bx, 190 + self.by), (198 + self.bx, 256 + self.by), (286 + self.bx, 256 + self.by)], fill='green')
        draw.polygon([(178 + self.bx, 190 + self.by), (84 + self.bx, 190 + self.by), (94 + self.bx, 256 + self.by), (182 + self.bx, 256 + self.by)], fill='green')
        
        # green side (L)
        draw.polygon([(52 + self.bx, 158 + self.by), (38 + self.bx, 74 + self.by), (50 + self.bx, 12 + self.by), (62 + self.bx, 84 + self.by)], fill='red')
        draw.polygon([(20 + self.bx, 162 + self.by), (36 + self.bx, 86 + self.by), (48 + self.bx, 164 + self.by), (36 + self.bx, 246 + self.by)], fill='blue')
        draw.polygon([(0 + self.bx, 264 + self.by), (18 + self.bx, 174 + self.by), (34 + self.bx, 264 + self.by), (18 + self.bx, 352 + self.by)], fill='red')
        draw.polygon([(66 + self.bx, 100 + self.by), (56 + self.bx, 166 + self.by), (64 + self.bx, 240 + self.by), (74 + self.bx, 164 + self.by)], fill='orange')
        draw.polygon([(52 + self.bx, 352 + self.by), (62 + self.bx, 264 + self.by), (52 + self.bx, 180 + self.by), (38 + self.bx, 264 + self.by)], fill='orange')
        draw.polygon([(22 + self.bx, 364 + self.by), (36 + self.bx, 440 + self.by), (48 + self.bx, 366 + self.by), (36 + self.bx, 282 + self.by)], fill='orange')
        draw.polygon([(80 + self.bx, 354 + self.by), (66 + self.bx, 264 + self.by), (76 + self.bx, 180 + self.by), (86 + self.bx, 264 + self.by)], fill='orange')
        draw.polygon([(56 + self.bx, 362 + self.by), (66 + self.bx, 438 + self.by), (74 + self.bx, 360 + self.by), (64 + self.bx, 292 + self.by)], fill='orange')
        draw.polygon([(40 + self.bx, 454 + self.by), (52 + self.bx, 370 + self.by), (62 + self.bx, 442 + self.by), (52 + self.bx, 514 + self.by)], fill='orange')
        
        # blue side (R)
        draw.polygon([(484 + self.bx, 264 + self.by), (466 + self.bx, 174 + self.by), (450 + self.bx, 264 + self.by), (466 + self.bx, 352 + self.by)], fill='blue')
        draw.polygon([(464 + self.bx, 162 + self.by), (448 + self.bx, 86 + self.by), (436 + self.bx, 164 + self.by), (448 + self.bx, 246 + self.by)], fill='red')
        draw.polygon([(432 + self.bx, 158 + self.by), (446 + self.bx, 74 + self.by), (434 + self.bx, 12 + self.by), (422 + self.bx, 84 + self.by)], fill='green')
        draw.polygon([(462 + self.bx, 364 + self.by), (448 + self.bx, 440 + self.by), (436 + self.bx, 366 + self.by), (446 + self.bx, 282 + self.by)], fill='red')
        draw.polygon([(432 + self.bx, 352 + self.by), (422 + self.bx, 264 + self.by), (432 + self.bx, 180 + self.by), (446 + self.bx, 264 + self.by)], fill='red')
        draw.polygon([(418 + self.bx, 100 + self.by), (428 + self.bx, 166 + self.by), (420 + self.bx, 240 + self.by), (410 + self.bx, 164 + self.by)], fill='red')
        draw.polygon([(444 + self.bx, 454 + self.by), (432 + self.bx, 370 + self.by), (422 + self.bx, 442 + self.by), (432 + self.bx, 514 + self.by)], fill='red')
        draw.polygon([(428 + self.bx, 362 + self.by), (418 + self.bx, 438 + self.by), (410 + self.bx, 360 + self.by), (420 + self.bx, 292 + self.by)], fill='red')
        draw.polygon([(404 + self.bx, 354 + self.by), (418 + self.bx, 264 + self.by), (408 + self.bx, 180 + self.by), (398 + self.bx, 264 + self.by)], fill='red')
        
        # orange side (F)
        draw.polygon([(10 + self.bx, 272 + self.by), (148 + self.bx, 272 + self.by), (156 + self.bx, 362 + self.by), (28 + self.bx, 362 + self.by)], fill='yellow')
        draw.polygon([(172 + self.bx, 272 + self.by), (312 + self.bx, 272 + self.by), (306 + self.bx, 362 + self.by), (178 + self.bx, 362 + self.by)], fill='yellow')
        draw.polygon([(336 + self.bx, 272 + self.by), (474 + self.bx, 272 + self.by), (456 + self.bx, 362 + self.by), (328 + self.bx, 362 + self.by)], fill='orange')
        draw.polygon([(32 + self.bx, 376 + self.by), (158 + self.bx, 376 + self.by), (164 + self.bx, 450 + self.by), (46 + self.bx, 450 + self.by)], fill='blue')
        draw.polygon([(180 + self.bx, 376 + self.by), (304 + self.bx, 376 + self.by), (300 + self.bx, 450 + self.by), (184 + self.bx, 450 + self.by)], fill='blue')
        draw.polygon([(328 + self.bx, 376 + self.by), (452 + self.bx, 376 + self.by), (438 + self.bx, 450 + self.by), (320 + self.bx, 450 + self.by)], fill='blue')
        draw.polygon([(48 + self.bx, 464 + self.by), (164 + self.bx, 464 + self.by), (170 + self.bx, 526 + self.by), (62 + self.bx, 526 + self.by)], fill='blue')
        draw.polygon([(186 + self.bx, 464 + self.by), (298 + self.bx, 464 + self.by), (296 + self.bx, 526 + self.by), (188 + self.bx, 526 + self.by)], fill='blue')
        draw.polygon([(320 + self.bx, 462 + self.by), (436 + self.bx, 462 + self.by), (422 + self.bx, 526 + self.by), (314 + self.bx, 526 + self.by)], fill='blue')
        
        # yellow side (U)
        draw.polygon([(60 + self.bx, 0 + self.by), (168 + self.bx, 0 + self.by), (164 + self.bx, 64 + self.by), (48 + self.bx, 64 + self.by)], fill='green')
        draw.polygon([(188 + self.bx, 0 + self.by), (296 + self.bx, 0 + self.by), (300 + self.bx, 64 + self.by), (184 + self.bx, 64 + self.by)], fill='orange')
        draw.polygon([(316 + self.bx, 0 + self.by), (424 + self.bx, 0 + self.by), (436 + self.bx, 64 + self.by), (320 + self.bx, 64 + self.by)], fill='yellow')
        draw.polygon([(44 + self.bx, 76 + self.by), (162 + self.bx, 76 + self.by), (156 + self.bx, 152 + self.by), (30 + self.bx, 152 + self.by)], fill='yellow')
        draw.polygon([(184 + self.bx, 76 + self.by), (300 + self.bx, 76 + self.by), (304 + self.bx, 150 + self.by), (180 + self.bx, 150 + self.by)], fill='yellow')
        draw.polygon([(322 + self.bx, 76 + self.by), (440 + self.bx, 76 + self.by), (452 + self.bx, 152 + self.by), (328 + self.bx, 152 + self.by)], fill='yellow')
        draw.polygon([(28 + self.bx, 166 + self.by), (156 + self.bx, 166 + self.by), (148 + self.bx, 256 + self.by), (10 + self.bx, 256 + self.by)], fill='blue')
        draw.polygon([(178 + self.bx, 166 + self.by), (306 + self.bx, 166 + self.by), (310 + self.bx, 254 + self.by), (174 + self.bx, 254 + self.by)], fill='green')
        draw.polygon([(328 + self.bx, 166 + self.by), (456 + self.bx, 166 + self.by), (474 + self.bx, 254 + self.by), (336 + self.bx, 254 + self.by)], fill='yellow')
    
    def drawEOLL4(self, draw):
        # white side (D)
        draw.polygon([(74 + self.bx, 438 + self.by), (174 + self.bx, 438 + self.by), (170 + self.bx, 522 + self.by), (66 + self.bx, 522 + self.by)], fill='white')
        draw.polygon([(192 + self.bx, 438 + self.by), (294 + self.bx, 438 + self.by), (298 + self.bx, 522 + self.by), (188 + self.bx, 522 + self.by)], fill='white')
        draw.polygon([(310 + self.bx, 436 + self.by), (410 + self.bx, 436 + self.by), (414 + self.bx, 524 + self.by), (314 + self.bx, 524 + self.by)], fill='white')
        draw.polygon([(84 + self.bx, 348 + self.by), (178 + self.bx, 348 + self.by), (174 + self.bx, 422 + self.by), (76 + self.bx, 422 + self.by)], fill='white')
        draw.polygon([(196 + self.bx, 348 + self.by), (288 + self.bx, 348 + self.by), (292 + self.bx, 424 + self.by), (192 + self.bx, 424 + self.by)], fill='white')
        draw.polygon([(306 + self.bx, 348 + self.by), (400 + self.bx, 348 + self.by), (404 + self.bx, 424 + self.by), (310 + self.bx, 424 + self.by)], fill='white')
        draw.polygon([(94 + self.bx, 270 + self.by), (182 + self.bx, 270 + self.by), (178 + self.bx, 336 + self.by), (84 + self.bx, 336 + self.by)], fill='white')
        draw.polygon([(198 + self.bx, 270 + self.by), (286 + self.bx, 270 + self.by), (290 + self.bx, 336 + self.by), (194 + self.bx, 336 + self.by)], fill='white')
        draw.polygon([(302 + self.bx, 268 + self.by), (390 + self.bx, 268 + self.by), (398 + self.bx, 336 + self.by), (306 + self.bx, 336 + self.by)], fill='white')
        
        # red side (B)
        draw.polygon([(414 + self.bx, 2 + self.by), (314 + self.bx, 2 + self.by), (310 + self.bx, 90 + self.by), (410 + self.bx, 90 + self.by)], fill='yellow')
        draw.polygon([(298 + self.bx, 4 + self.by), (188 + self.bx, 4 + self.by), (192 + self.bx, 88 + self.by), (292 + self.bx, 88 + self.by)], fill='red')
        draw.polygon([(170 + self.bx, 4 + self.by), (66 + self.bx, 4 + self.by), (74 + self.bx, 88 + self.by), (174 + self.bx, 88 + self.by)], fill='green')
        draw.polygon([(404 + self.bx, 102 + self.by), (310 + self.bx, 102 + self.by), (306 + self.bx, 178 + self.by), (400 + self.bx, 178 + self.by)], fill='green')
        draw.polygon([(292 + self.bx, 102 + self.by), (192 + self.bx, 102 + self.by), (196 + self.bx, 178 + self.by), (288 + self.bx, 178 + self.by)], fill='green')
        draw.polygon([(174 + self.bx, 104 + self.by), (76 + self.bx, 104 + self.by), (84 + self.bx, 178 + self.by), (178 + self.bx, 178 + self.by)], fill='green')
        draw.polygon([(398 + self.bx, 190 + self.by), (306 + self.bx, 190 + self.by), (302 + self.bx, 258 + self.by), (390 + self.bx, 258 + self.by)], fill='green')
        draw.polygon([(290 + self.bx, 190 + self.by), (194 + self.bx, 190 + self.by), (198 + self.bx, 256 + self.by), (286 + self.bx, 256 + self.by)], fill='green')
        draw.polygon([(178 + self.bx, 190 + self.by), (84 + self.bx, 190 + self.by), (94 + self.bx, 256 + self.by), (182 + self.bx, 256 + self.by)], fill='green')
        
        # green side (L)
        draw.polygon([(52 + self.bx, 158 + self.by), (38 + self.bx, 74 + self.by), (50 + self.bx, 12 + self.by), (62 + self.bx, 84 + self.by)], fill='orange')
        draw.polygon([(20 + self.bx, 162 + self.by), (36 + self.bx, 86 + self.by), (48 + self.bx, 164 + self.by), (36 + self.bx, 246 + self.by)], fill='blue')
        draw.polygon([(0 + self.bx, 264 + self.by), (18 + self.bx, 174 + self.by), (34 + self.bx, 264 + self.by), (18 + self.bx, 352 + self.by)], fill='orange')
        draw.polygon([(66 + self.bx, 100 + self.by), (56 + self.bx, 166 + self.by), (64 + self.bx, 240 + self.by), (74 + self.bx, 164 + self.by)], fill='orange')
        draw.polygon([(52 + self.bx, 352 + self.by), (62 + self.bx, 264 + self.by), (52 + self.bx, 180 + self.by), (38 + self.bx, 264 + self.by)], fill='orange')
        draw.polygon([(22 + self.bx, 364 + self.by), (36 + self.bx, 440 + self.by), (48 + self.bx, 366 + self.by), (36 + self.bx, 282 + self.by)], fill='orange')
        draw.polygon([(80 + self.bx, 354 + self.by), (66 + self.bx, 264 + self.by), (76 + self.bx, 180 + self.by), (86 + self.bx, 264 + self.by)], fill='orange')
        draw.polygon([(56 + self.bx, 362 + self.by), (66 + self.bx, 438 + self.by), (74 + self.bx, 360 + self.by), (64 + self.bx, 292 + self.by)], fill='orange')
        draw.polygon([(40 + self.bx, 454 + self.by), (52 + self.bx, 370 + self.by), (62 + self.bx, 442 + self.by), (52 + self.bx, 514 + self.by)], fill='orange')
        
        # blue side (R)
        draw.polygon([(484 + self.bx, 264 + self.by), (466 + self.bx, 174 + self.by), (450 + self.bx, 264 + self.by), (466 + self.bx, 352 + self.by)], fill='blue')
        draw.polygon([(464 + self.bx, 162 + self.by), (448 + self.bx, 86 + self.by), (436 + self.bx, 164 + self.by), (448 + self.bx, 246 + self.by)], fill='green')
        draw.polygon([(432 + self.bx, 158 + self.by), (446 + self.bx, 74 + self.by), (434 + self.bx, 12 + self.by), (422 + self.bx, 84 + self.by)], fill='green')
        draw.polygon([(462 + self.bx, 364 + self.by), (448 + self.bx, 440 + self.by), (436 + self.bx, 366 + self.by), (446 + self.bx, 282 + self.by)], fill='red')
        draw.polygon([(432 + self.bx, 352 + self.by), (422 + self.bx, 264 + self.by), (432 + self.bx, 180 + self.by), (446 + self.bx, 264 + self.by)], fill='red')
        draw.polygon([(418 + self.bx, 100 + self.by), (428 + self.bx, 166 + self.by), (420 + self.bx, 240 + self.by), (410 + self.bx, 164 + self.by)], fill='red')
        draw.polygon([(444 + self.bx, 454 + self.by), (432 + self.bx, 370 + self.by), (422 + self.bx, 442 + self.by), (432 + self.bx, 514 + self.by)], fill='red')
        draw.polygon([(428 + self.bx, 362 + self.by), (418 + self.bx, 438 + self.by), (410 + self.bx, 360 + self.by), (420 + self.bx, 292 + self.by)], fill='red')
        draw.polygon([(404 + self.bx, 354 + self.by), (418 + self.bx, 264 + self.by), (408 + self.bx, 180 + self.by), (398 + self.bx, 264 + self.by)], fill='red')
        
        # orange side (F)
        draw.polygon([(10 + self.bx, 272 + self.by), (148 + self.bx, 272 + self.by), (156 + self.bx, 362 + self.by), (28 + self.bx, 362 + self.by)], fill='blue')
        draw.polygon([(172 + self.bx, 272 + self.by), (312 + self.bx, 272 + self.by), (306 + self.bx, 362 + self.by), (178 + self.bx, 362 + self.by)], fill='orange')
        draw.polygon([(336 + self.bx, 272 + self.by), (474 + self.bx, 272 + self.by), (456 + self.bx, 362 + self.by), (328 + self.bx, 362 + self.by)], fill='yellow')
        draw.polygon([(32 + self.bx, 376 + self.by), (158 + self.bx, 376 + self.by), (164 + self.bx, 450 + self.by), (46 + self.bx, 450 + self.by)], fill='blue')
        draw.polygon([(180 + self.bx, 376 + self.by), (304 + self.bx, 376 + self.by), (300 + self.bx, 450 + self.by), (184 + self.bx, 450 + self.by)], fill='blue')
        draw.polygon([(328 + self.bx, 376 + self.by), (452 + self.bx, 376 + self.by), (438 + self.bx, 450 + self.by), (320 + self.bx, 450 + self.by)], fill='blue')
        draw.polygon([(48 + self.bx, 464 + self.by), (164 + self.bx, 464 + self.by), (170 + self.bx, 526 + self.by), (62 + self.bx, 526 + self.by)], fill='blue')
        draw.polygon([(186 + self.bx, 464 + self.by), (298 + self.bx, 464 + self.by), (296 + self.bx, 526 + self.by), (188 + self.bx, 526 + self.by)], fill='blue')
        draw.polygon([(320 + self.bx, 462 + self.by), (436 + self.bx, 462 + self.by), (422 + self.bx, 526 + self.by), (314 + self.bx, 526 + self.by)], fill='blue')
        
        # yellow side (U)
        draw.polygon([(60 + self.bx, 0 + self.by), (168 + self.bx, 0 + self.by), (164 + self.bx, 64 + self.by), (48 + self.bx, 64 + self.by)], fill='yellow')
        draw.polygon([(188 + self.bx, 0 + self.by), (296 + self.bx, 0 + self.by), (300 + self.bx, 64 + self.by), (184 + self.bx, 64 + self.by)], fill='yellow')
        draw.polygon([(316 + self.bx, 0 + self.by), (424 + self.bx, 0 + self.by), (436 + self.bx, 64 + self.by), (320 + self.bx, 64 + self.by)], fill='red')
        draw.polygon([(44 + self.bx, 76 + self.by), (162 + self.bx, 76 + self.by), (156 + self.bx, 152 + self.by), (30 + self.bx, 152 + self.by)], fill='yellow')
        draw.polygon([(184 + self.bx, 76 + self.by), (300 + self.bx, 76 + self.by), (304 + self.bx, 150 + self.by), (180 + self.bx, 150 + self.by)], fill='yellow')
        draw.polygon([(322 + self.bx, 76 + self.by), (440 + self.bx, 76 + self.by), (452 + self.bx, 152 + self.by), (328 + self.bx, 152 + self.by)], fill='yellow')
        draw.polygon([(28 + self.bx, 166 + self.by), (156 + self.bx, 166 + self.by), (148 + self.bx, 256 + self.by), (10 + self.bx, 256 + self.by)], fill='yellow')
        draw.polygon([(178 + self.bx, 166 + self.by), (306 + self.bx, 166 + self.by), (310 + self.bx, 254 + self.by), (174 + self.bx, 254 + self.by)], fill='yellow')
        draw.polygon([(328 + self.bx, 166 + self.by), (456 + self.bx, 166 + self.by), (474 + self.bx, 254 + self.by), (336 + self.bx, 254 + self.by)], fill='red')
    
    def drawSune(self, draw):
        # white side (D)
        draw.polygon([(74 + self.bx, 438 + self.by), (174 + self.bx, 438 + self.by), (170 + self.bx, 522 + self.by), (66 + self.bx, 522 + self.by)], fill='white')
        draw.polygon([(192 + self.bx, 438 + self.by), (294 + self.bx, 438 + self.by), (298 + self.bx, 522 + self.by), (188 + self.bx, 522 + self.by)], fill='white')
        draw.polygon([(310 + self.bx, 436 + self.by), (410 + self.bx, 436 + self.by), (414 + self.bx, 524 + self.by), (314 + self.bx, 524 + self.by)], fill='white')
        draw.polygon([(84 + self.bx, 348 + self.by), (178 + self.bx, 348 + self.by), (174 + self.bx, 422 + self.by), (76 + self.bx, 422 + self.by)], fill='white')
        draw.polygon([(196 + self.bx, 348 + self.by), (288 + self.bx, 348 + self.by), (292 + self.bx, 424 + self.by), (192 + self.bx, 424 + self.by)], fill='white')
        draw.polygon([(306 + self.bx, 348 + self.by), (400 + self.bx, 348 + self.by), (404 + self.bx, 424 + self.by), (310 + self.bx, 424 + self.by)], fill='white')
        draw.polygon([(94 + self.bx, 270 + self.by), (182 + self.bx, 270 + self.by), (178 + self.bx, 336 + self.by), (84 + self.bx, 336 + self.by)], fill='white')
        draw.polygon([(198 + self.bx, 270 + self.by), (286 + self.bx, 270 + self.by), (290 + self.bx, 336 + self.by), (194 + self.bx, 336 + self.by)], fill='white')
        draw.polygon([(302 + self.bx, 268 + self.by), (390 + self.bx, 268 + self.by), (398 + self.bx, 336 + self.by), (306 + self.bx, 336 + self.by)], fill='white')
        
        # red side (B)
        draw.polygon([(414 + self.bx, 2 + self.by), (314 + self.bx, 2 + self.by), (310 + self.bx, 90 + self.by), (410 + self.bx, 90 + self.by)], fill='red')
        draw.polygon([(298 + self.bx, 4 + self.by), (188 + self.bx, 4 + self.by), (192 + self.bx, 88 + self.by), (292 + self.bx, 88 + self.by)], fill='red')
        draw.polygon([(170 + self.bx, 4 + self.by), (66 + self.bx, 4 + self.by), (74 + self.bx, 88 + self.by), (174 + self.bx, 88 + self.by)], fill='yellow')
        draw.polygon([(404 + self.bx, 102 + self.by), (310 + self.bx, 102 + self.by), (306 + self.bx, 178 + self.by), (400 + self.bx, 178 + self.by)], fill='green')
        draw.polygon([(292 + self.bx, 102 + self.by), (192 + self.bx, 102 + self.by), (196 + self.bx, 178 + self.by), (288 + self.bx, 178 + self.by)], fill='green')
        draw.polygon([(174 + self.bx, 104 + self.by), (76 + self.bx, 104 + self.by), (84 + self.bx, 178 + self.by), (178 + self.bx, 178 + self.by)], fill='green')
        draw.polygon([(398 + self.bx, 190 + self.by), (306 + self.bx, 190 + self.by), (302 + self.bx, 258 + self.by), (390 + self.bx, 258 + self.by)], fill='green')
        draw.polygon([(290 + self.bx, 190 + self.by), (194 + self.bx, 190 + self.by), (198 + self.bx, 256 + self.by), (286 + self.bx, 256 + self.by)], fill='green')
        draw.polygon([(178 + self.bx, 190 + self.by), (84 + self.bx, 190 + self.by), (94 + self.bx, 256 + self.by), (182 + self.bx, 256 + self.by)], fill='green')
        
        # green side (L)
        draw.polygon([(52 + self.bx, 158 + self.by), (38 + self.bx, 74 + self.by), (50 + self.bx, 12 + self.by), (62 + self.bx, 84 + self.by)], fill='green')
        draw.polygon([(20 + self.bx, 162 + self.by), (36 + self.bx, 86 + self.by), (48 + self.bx, 164 + self.by), (36 + self.bx, 246 + self.by)], fill='orange')
        draw.polygon([(0 + self.bx, 264 + self.by), (18 + self.bx, 174 + self.by), (34 + self.bx, 264 + self.by), (18 + self.bx, 352 + self.by)], fill='orange')
        draw.polygon([(66 + self.bx, 100 + self.by), (56 + self.bx, 166 + self.by), (64 + self.bx, 240 + self.by), (74 + self.bx, 164 + self.by)], fill='orange')
        draw.polygon([(52 + self.bx, 352 + self.by), (62 + self.bx, 264 + self.by), (52 + self.bx, 180 + self.by), (38 + self.bx, 264 + self.by)], fill='orange')
        draw.polygon([(22 + self.bx, 364 + self.by), (36 + self.bx, 440 + self.by), (48 + self.bx, 366 + self.by), (36 + self.bx, 282 + self.by)], fill='orange')
        draw.polygon([(80 + self.bx, 354 + self.by), (66 + self.bx, 264 + self.by), (76 + self.bx, 180 + self.by), (86 + self.bx, 264 + self.by)], fill='orange')
        draw.polygon([(56 + self.bx, 362 + self.by), (66 + self.bx, 438 + self.by), (74 + self.bx, 360 + self.by), (64 + self.bx, 292 + self.by)], fill='orange')
        draw.polygon([(40 + self.bx, 454 + self.by), (52 + self.bx, 370 + self.by), (62 + self.bx, 442 + self.by), (52 + self.bx, 514 + self.by)], fill='orange')
        
        # blue side (R)
        draw.polygon([(484 + self.bx, 264 + self.by), (466 + self.bx, 174 + self.by), (450 + self.bx, 264 + self.by), (466 + self.bx, 352 + self.by)], fill='blue')
        draw.polygon([(464 + self.bx, 162 + self.by), (448 + self.bx, 86 + self.by), (436 + self.bx, 164 + self.by), (448 + self.bx, 246 + self.by)], fill='blue')
        draw.polygon([(432 + self.bx, 158 + self.by), (446 + self.bx, 74 + self.by), (434 + self.bx, 12 + self.by), (422 + self.bx, 84 + self.by)], fill='yellow')
        draw.polygon([(462 + self.bx, 364 + self.by), (448 + self.bx, 440 + self.by), (436 + self.bx, 366 + self.by), (446 + self.bx, 282 + self.by)], fill='red')
        draw.polygon([(432 + self.bx, 352 + self.by), (422 + self.bx, 264 + self.by), (432 + self.bx, 180 + self.by), (446 + self.bx, 264 + self.by)], fill='red')
        draw.polygon([(418 + self.bx, 100 + self.by), (428 + self.bx, 166 + self.by), (420 + self.bx, 240 + self.by), (410 + self.bx, 164 + self.by)], fill='red')
        draw.polygon([(444 + self.bx, 454 + self.by), (432 + self.bx, 370 + self.by), (422 + self.bx, 442 + self.by), (432 + self.bx, 514 + self.by)], fill='red')
        draw.polygon([(428 + self.bx, 362 + self.by), (418 + self.bx, 438 + self.by), (410 + self.bx, 360 + self.by), (420 + self.bx, 292 + self.by)], fill='red')
        draw.polygon([(404 + self.bx, 354 + self.by), (418 + self.bx, 264 + self.by), (408 + self.bx, 180 + self.by), (398 + self.bx, 264 + self.by)], fill='red')
        
        # orange side (F)
        draw.polygon([(10 + self.bx, 272 + self.by), (148 + self.bx, 272 + self.by), (156 + self.bx, 362 + self.by), (28 + self.bx, 362 + self.by)], fill='blue')
        draw.polygon([(172 + self.bx, 272 + self.by), (312 + self.bx, 272 + self.by), (306 + self.bx, 362 + self.by), (178 + self.bx, 362 + self.by)], fill='green')
        draw.polygon([(336 + self.bx, 272 + self.by), (474 + self.bx, 272 + self.by), (456 + self.bx, 362 + self.by), (328 + self.bx, 362 + self.by)], fill='yellow')
        draw.polygon([(32 + self.bx, 376 + self.by), (158 + self.bx, 376 + self.by), (164 + self.bx, 450 + self.by), (46 + self.bx, 450 + self.by)], fill='blue')
        draw.polygon([(180 + self.bx, 376 + self.by), (304 + self.bx, 376 + self.by), (300 + self.bx, 450 + self.by), (184 + self.bx, 450 + self.by)], fill='blue')
        draw.polygon([(328 + self.bx, 376 + self.by), (452 + self.bx, 376 + self.by), (438 + self.bx, 450 + self.by), (320 + self.bx, 450 + self.by)], fill='blue')
        draw.polygon([(48 + self.bx, 464 + self.by), (164 + self.bx, 464 + self.by), (170 + self.bx, 526 + self.by), (62 + self.bx, 526 + self.by)], fill='blue')
        draw.polygon([(186 + self.bx, 464 + self.by), (298 + self.bx, 464 + self.by), (296 + self.bx, 526 + self.by), (188 + self.bx, 526 + self.by)], fill='blue')
        draw.polygon([(320 + self.bx, 462 + self.by), (436 + self.bx, 462 + self.by), (422 + self.bx, 526 + self.by), (314 + self.bx, 526 + self.by)], fill='blue')
        
        # yellow side (U)
        draw.polygon([(60 + self.bx, 0 + self.by), (168 + self.bx, 0 + self.by), (164 + self.bx, 64 + self.by), (48 + self.bx, 64 + self.by)], fill='orange')
        draw.polygon([(188 + self.bx, 0 + self.by), (296 + self.bx, 0 + self.by), (300 + self.bx, 64 + self.by), (184 + self.bx, 64 + self.by)], fill='yellow')
        draw.polygon([(316 + self.bx, 0 + self.by), (424 + self.bx, 0 + self.by), (436 + self.bx, 64 + self.by), (320 + self.bx, 64 + self.by)], fill='green')
        draw.polygon([(44 + self.bx, 76 + self.by), (162 + self.bx, 76 + self.by), (156 + self.bx, 152 + self.by), (30 + self.bx, 152 + self.by)], fill='yellow')
        draw.polygon([(184 + self.bx, 76 + self.by), (300 + self.bx, 76 + self.by), (304 + self.bx, 150 + self.by), (180 + self.bx, 150 + self.by)], fill='yellow')
        draw.polygon([(322 + self.bx, 76 + self.by), (440 + self.bx, 76 + self.by), (452 + self.bx, 152 + self.by), (328 + self.bx, 152 + self.by)], fill='yellow')
        draw.polygon([(28 + self.bx, 166 + self.by), (156 + self.bx, 166 + self.by), (148 + self.bx, 256 + self.by), (10 + self.bx, 256 + self.by)], fill='yellow')
        draw.polygon([(178 + self.bx, 166 + self.by), (306 + self.bx, 166 + self.by), (310 + self.bx, 254 + self.by), (174 + self.bx, 254 + self.by)], fill='yellow')
        draw.polygon([(328 + self.bx, 166 + self.by), (456 + self.bx, 166 + self.by), (474 + self.bx, 254 + self.by), (336 + self.bx, 254 + self.by)], fill='red')
    
    def drawAntiSune(self, draw):
        # white side (D)
        draw.polygon([(74 + self.bx, 438 + self.by), (174 + self.bx, 438 + self.by), (170 + self.bx, 522 + self.by), (66 + self.bx, 522 + self.by)], fill='white')
        draw.polygon([(192 + self.bx, 438 + self.by), (294 + self.bx, 438 + self.by), (298 + self.bx, 522 + self.by), (188 + self.bx, 522 + self.by)], fill='white')
        draw.polygon([(310 + self.bx, 436 + self.by), (410 + self.bx, 436 + self.by), (414 + self.bx, 524 + self.by), (314 + self.bx, 524 + self.by)], fill='white')
        draw.polygon([(84 + self.bx, 348 + self.by), (178 + self.bx, 348 + self.by), (174 + self.bx, 422 + self.by), (76 + self.bx, 422 + self.by)], fill='white')
        draw.polygon([(196 + self.bx, 348 + self.by), (288 + self.bx, 348 + self.by), (292 + self.bx, 424 + self.by), (192 + self.bx, 424 + self.by)], fill='white')
        draw.polygon([(306 + self.bx, 348 + self.by), (400 + self.bx, 348 + self.by), (404 + self.bx, 424 + self.by), (310 + self.bx, 424 + self.by)], fill='white')
        draw.polygon([(94 + self.bx, 270 + self.by), (182 + self.bx, 270 + self.by), (178 + self.bx, 336 + self.by), (84 + self.bx, 336 + self.by)], fill='white')
        draw.polygon([(198 + self.bx, 270 + self.by), (286 + self.bx, 270 + self.by), (290 + self.bx, 336 + self.by), (194 + self.bx, 336 + self.by)], fill='white')
        draw.polygon([(302 + self.bx, 268 + self.by), (390 + self.bx, 268 + self.by), (398 + self.bx, 336 + self.by), (306 + self.bx, 336 + self.by)], fill='white')
        
        # red side (B)
        draw.polygon([(414 + self.bx, 2 + self.by), (314 + self.bx, 2 + self.by), (310 + self.bx, 90 + self.by), (410 + self.bx, 90 + self.by)], fill='yellow')
        draw.polygon([(298 + self.bx, 4 + self.by), (188 + self.bx, 4 + self.by), (192 + self.bx, 88 + self.by), (292 + self.bx, 88 + self.by)], fill='red')
        draw.polygon([(170 + self.bx, 4 + self.by), (66 + self.bx, 4 + self.by), (74 + self.bx, 88 + self.by), (174 + self.bx, 88 + self.by)], fill='red')
        draw.polygon([(404 + self.bx, 102 + self.by), (310 + self.bx, 102 + self.by), (306 + self.bx, 178 + self.by), (400 + self.bx, 178 + self.by)], fill='green')
        draw.polygon([(292 + self.bx, 102 + self.by), (192 + self.bx, 102 + self.by), (196 + self.bx, 178 + self.by), (288 + self.bx, 178 + self.by)], fill='green')
        draw.polygon([(174 + self.bx, 104 + self.by), (76 + self.bx, 104 + self.by), (84 + self.bx, 178 + self.by), (178 + self.bx, 178 + self.by)], fill='green')
        draw.polygon([(398 + self.bx, 190 + self.by), (306 + self.bx, 190 + self.by), (302 + self.bx, 258 + self.by), (390 + self.bx, 258 + self.by)], fill='green')
        draw.polygon([(290 + self.bx, 190 + self.by), (194 + self.bx, 190 + self.by), (198 + self.bx, 256 + self.by), (286 + self.bx, 256 + self.by)], fill='green')
        draw.polygon([(178 + self.bx, 190 + self.by), (84 + self.bx, 190 + self.by), (94 + self.bx, 256 + self.by), (182 + self.bx, 256 + self.by)], fill='green')
        
        # green side (L)
        draw.polygon([(52 + self.bx, 158 + self.by), (38 + self.bx, 74 + self.by), (50 + self.bx, 12 + self.by), (62 + self.bx, 84 + self.by)], fill='yellow')
        draw.polygon([(20 + self.bx, 162 + self.by), (36 + self.bx, 86 + self.by), (48 + self.bx, 164 + self.by), (36 + self.bx, 246 + self.by)], fill='green')
        draw.polygon([(0 + self.bx, 264 + self.by), (18 + self.bx, 174 + self.by), (34 + self.bx, 264 + self.by), (18 + self.bx, 352 + self.by)], fill='green')
        draw.polygon([(66 + self.bx, 100 + self.by), (56 + self.bx, 166 + self.by), (64 + self.bx, 240 + self.by), (74 + self.bx, 164 + self.by)], fill='orange')
        draw.polygon([(52 + self.bx, 352 + self.by), (62 + self.bx, 264 + self.by), (52 + self.bx, 180 + self.by), (38 + self.bx, 264 + self.by)], fill='orange')
        draw.polygon([(22 + self.bx, 364 + self.by), (36 + self.bx, 440 + self.by), (48 + self.bx, 366 + self.by), (36 + self.bx, 282 + self.by)], fill='orange')
        draw.polygon([(80 + self.bx, 354 + self.by), (66 + self.bx, 264 + self.by), (76 + self.bx, 180 + self.by), (86 + self.bx, 264 + self.by)], fill='orange')
        draw.polygon([(56 + self.bx, 362 + self.by), (66 + self.bx, 438 + self.by), (74 + self.bx, 360 + self.by), (64 + self.bx, 292 + self.by)], fill='orange')
        draw.polygon([(40 + self.bx, 454 + self.by), (52 + self.bx, 370 + self.by), (62 + self.bx, 442 + self.by), (52 + self.bx, 514 + self.by)], fill='orange')
        
        # blue side (R)
        draw.polygon([(484 + self.bx, 264 + self.by), (466 + self.bx, 174 + self.by), (450 + self.bx, 264 + self.by), (466 + self.bx, 352 + self.by)], fill='orange')
        draw.polygon([(464 + self.bx, 162 + self.by), (448 + self.bx, 86 + self.by), (436 + self.bx, 164 + self.by), (448 + self.bx, 246 + self.by)], fill='orange')
        draw.polygon([(432 + self.bx, 158 + self.by), (446 + self.bx, 74 + self.by), (434 + self.bx, 12 + self.by), (422 + self.bx, 84 + self.by)], fill='blue')
        draw.polygon([(462 + self.bx, 364 + self.by), (448 + self.bx, 440 + self.by), (436 + self.bx, 366 + self.by), (446 + self.bx, 282 + self.by)], fill='red')
        draw.polygon([(432 + self.bx, 352 + self.by), (422 + self.bx, 264 + self.by), (432 + self.bx, 180 + self.by), (446 + self.bx, 264 + self.by)], fill='red')
        draw.polygon([(418 + self.bx, 100 + self.by), (428 + self.bx, 166 + self.by), (420 + self.bx, 240 + self.by), (410 + self.bx, 164 + self.by)], fill='red')
        draw.polygon([(444 + self.bx, 454 + self.by), (432 + self.bx, 370 + self.by), (422 + self.bx, 442 + self.by), (432 + self.bx, 514 + self.by)], fill='red')
        draw.polygon([(428 + self.bx, 362 + self.by), (418 + self.bx, 438 + self.by), (410 + self.bx, 360 + self.by), (420 + self.bx, 292 + self.by)], fill='red')
        draw.polygon([(404 + self.bx, 354 + self.by), (418 + self.bx, 264 + self.by), (408 + self.bx, 180 + self.by), (398 + self.bx, 264 + self.by)], fill='red')
        
        # orange side (F)
        draw.polygon([(10 + self.bx, 272 + self.by), (148 + self.bx, 272 + self.by), (156 + self.bx, 362 + self.by), (28 + self.bx, 362 + self.by)], fill='yellow')
        draw.polygon([(172 + self.bx, 272 + self.by), (312 + self.bx, 272 + self.by), (306 + self.bx, 362 + self.by), (178 + self.bx, 362 + self.by)], fill='blue')
        draw.polygon([(336 + self.bx, 272 + self.by), (474 + self.bx, 272 + self.by), (456 + self.bx, 362 + self.by), (328 + self.bx, 362 + self.by)], fill='green')
        draw.polygon([(32 + self.bx, 376 + self.by), (158 + self.bx, 376 + self.by), (164 + self.bx, 450 + self.by), (46 + self.bx, 450 + self.by)], fill='blue')
        draw.polygon([(180 + self.bx, 376 + self.by), (304 + self.bx, 376 + self.by), (300 + self.bx, 450 + self.by), (184 + self.bx, 450 + self.by)], fill='blue')
        draw.polygon([(328 + self.bx, 376 + self.by), (452 + self.bx, 376 + self.by), (438 + self.bx, 450 + self.by), (320 + self.bx, 450 + self.by)], fill='blue')
        draw.polygon([(48 + self.bx, 464 + self.by), (164 + self.bx, 464 + self.by), (170 + self.bx, 526 + self.by), (62 + self.bx, 526 + self.by)], fill='blue')
        draw.polygon([(186 + self.bx, 464 + self.by), (298 + self.bx, 464 + self.by), (296 + self.bx, 526 + self.by), (188 + self.bx, 526 + self.by)], fill='blue')
        draw.polygon([(320 + self.bx, 462 + self.by), (436 + self.bx, 462 + self.by), (422 + self.bx, 526 + self.by), (314 + self.bx, 526 + self.by)], fill='blue')
        
        # yellow side (U)
        draw.polygon([(60 + self.bx, 0 + self.by), (168 + self.bx, 0 + self.by), (164 + self.bx, 64 + self.by), (48 + self.bx, 64 + self.by)], fill='blue')
        draw.polygon([(188 + self.bx, 0 + self.by), (296 + self.bx, 0 + self.by), (300 + self.bx, 64 + self.by), (184 + self.bx, 64 + self.by)], fill='yellow')
        draw.polygon([(316 + self.bx, 0 + self.by), (424 + self.bx, 0 + self.by), (436 + self.bx, 64 + self.by), (320 + self.bx, 64 + self.by)], fill='orange')
        draw.polygon([(44 + self.bx, 76 + self.by), (162 + self.bx, 76 + self.by), (156 + self.bx, 152 + self.by), (30 + self.bx, 152 + self.by)], fill='yellow')
        draw.polygon([(184 + self.bx, 76 + self.by), (300 + self.bx, 76 + self.by), (304 + self.bx, 150 + self.by), (180 + self.bx, 150 + self.by)], fill='yellow')
        draw.polygon([(322 + self.bx, 76 + self.by), (440 + self.bx, 76 + self.by), (452 + self.bx, 152 + self.by), (328 + self.bx, 152 + self.by)], fill='yellow')
        draw.polygon([(28 + self.bx, 166 + self.by), (156 + self.bx, 166 + self.by), (148 + self.bx, 256 + self.by), (10 + self.bx, 256 + self.by)], fill='red')
        draw.polygon([(178 + self.bx, 166 + self.by), (306 + self.bx, 166 + self.by), (310 + self.bx, 254 + self.by), (174 + self.bx, 254 + self.by)], fill='yellow')
        draw.polygon([(328 + self.bx, 166 + self.by), (456 + self.bx, 166 + self.by), (474 + self.bx, 254 + self.by), (336 + self.bx, 254 + self.by)], fill='yellow')
    
    def drawAntiSune(self, draw):
        # white side (D)
        draw.polygon([(74 + self.bx, 438 + self.by), (174 + self.bx, 438 + self.by), (170 + self.bx, 522 + self.by), (66 + self.bx, 522 + self.by)], fill='white')
        draw.polygon([(192 + self.bx, 438 + self.by), (294 + self.bx, 438 + self.by), (298 + self.bx, 522 + self.by), (188 + self.bx, 522 + self.by)], fill='white')
        draw.polygon([(310 + self.bx, 436 + self.by), (410 + self.bx, 436 + self.by), (414 + self.bx, 524 + self.by), (314 + self.bx, 524 + self.by)], fill='white')
        draw.polygon([(84 + self.bx, 348 + self.by), (178 + self.bx, 348 + self.by), (174 + self.bx, 422 + self.by), (76 + self.bx, 422 + self.by)], fill='white')
        draw.polygon([(196 + self.bx, 348 + self.by), (288 + self.bx, 348 + self.by), (292 + self.bx, 424 + self.by), (192 + self.bx, 424 + self.by)], fill='white')
        draw.polygon([(306 + self.bx, 348 + self.by), (400 + self.bx, 348 + self.by), (404 + self.bx, 424 + self.by), (310 + self.bx, 424 + self.by)], fill='white')
        draw.polygon([(94 + self.bx, 270 + self.by), (182 + self.bx, 270 + self.by), (178 + self.bx, 336 + self.by), (84 + self.bx, 336 + self.by)], fill='white')
        draw.polygon([(198 + self.bx, 270 + self.by), (286 + self.bx, 270 + self.by), (290 + self.bx, 336 + self.by), (194 + self.bx, 336 + self.by)], fill='white')
        draw.polygon([(302 + self.bx, 268 + self.by), (390 + self.bx, 268 + self.by), (398 + self.bx, 336 + self.by), (306 + self.bx, 336 + self.by)], fill='white')
        
        # red side (B)
        draw.polygon([(414 + self.bx, 2 + self.by), (314 + self.bx, 2 + self.by), (310 + self.bx, 90 + self.by), (410 + self.bx, 90 + self.by)], fill='yellow')
        draw.polygon([(298 + self.bx, 4 + self.by), (188 + self.bx, 4 + self.by), (192 + self.bx, 88 + self.by), (292 + self.bx, 88 + self.by)], fill='red')
        draw.polygon([(170 + self.bx, 4 + self.by), (66 + self.bx, 4 + self.by), (74 + self.bx, 88 + self.by), (174 + self.bx, 88 + self.by)], fill='red')
        draw.polygon([(404 + self.bx, 102 + self.by), (310 + self.bx, 102 + self.by), (306 + self.bx, 178 + self.by), (400 + self.bx, 178 + self.by)], fill='green')
        draw.polygon([(292 + self.bx, 102 + self.by), (192 + self.bx, 102 + self.by), (196 + self.bx, 178 + self.by), (288 + self.bx, 178 + self.by)], fill='green')
        draw.polygon([(174 + self.bx, 104 + self.by), (76 + self.bx, 104 + self.by), (84 + self.bx, 178 + self.by), (178 + self.bx, 178 + self.by)], fill='green')
        draw.polygon([(398 + self.bx, 190 + self.by), (306 + self.bx, 190 + self.by), (302 + self.bx, 258 + self.by), (390 + self.bx, 258 + self.by)], fill='green')
        draw.polygon([(290 + self.bx, 190 + self.by), (194 + self.bx, 190 + self.by), (198 + self.bx, 256 + self.by), (286 + self.bx, 256 + self.by)], fill='green')
        draw.polygon([(178 + self.bx, 190 + self.by), (84 + self.bx, 190 + self.by), (94 + self.bx, 256 + self.by), (182 + self.bx, 256 + self.by)], fill='green')
        
        # green side (L)
        draw.polygon([(52 + self.bx, 158 + self.by), (38 + self.bx, 74 + self.by), (50 + self.bx, 12 + self.by), (62 + self.bx, 84 + self.by)], fill='yellow')
        draw.polygon([(20 + self.bx, 162 + self.by), (36 + self.bx, 86 + self.by), (48 + self.bx, 164 + self.by), (36 + self.bx, 246 + self.by)], fill='green')
        draw.polygon([(0 + self.bx, 264 + self.by), (18 + self.bx, 174 + self.by), (34 + self.bx, 264 + self.by), (18 + self.bx, 352 + self.by)], fill='green')
        draw.polygon([(66 + self.bx, 100 + self.by), (56 + self.bx, 166 + self.by), (64 + self.bx, 240 + self.by), (74 + self.bx, 164 + self.by)], fill='orange')
        draw.polygon([(52 + self.bx, 352 + self.by), (62 + self.bx, 264 + self.by), (52 + self.bx, 180 + self.by), (38 + self.bx, 264 + self.by)], fill='orange')
        draw.polygon([(22 + self.bx, 364 + self.by), (36 + self.bx, 440 + self.by), (48 + self.bx, 366 + self.by), (36 + self.bx, 282 + self.by)], fill='orange')
        draw.polygon([(80 + self.bx, 354 + self.by), (66 + self.bx, 264 + self.by), (76 + self.bx, 180 + self.by), (86 + self.bx, 264 + self.by)], fill='orange')
        draw.polygon([(56 + self.bx, 362 + self.by), (66 + self.bx, 438 + self.by), (74 + self.bx, 360 + self.by), (64 + self.bx, 292 + self.by)], fill='orange')
        draw.polygon([(40 + self.bx, 454 + self.by), (52 + self.bx, 370 + self.by), (62 + self.bx, 442 + self.by), (52 + self.bx, 514 + self.by)], fill='orange')
        
        # blue side (R)
        draw.polygon([(484 + self.bx, 264 + self.by), (466 + self.bx, 174 + self.by), (450 + self.bx, 264 + self.by), (466 + self.bx, 352 + self.by)], fill='orange')
        draw.polygon([(464 + self.bx, 162 + self.by), (448 + self.bx, 86 + self.by), (436 + self.bx, 164 + self.by), (448 + self.bx, 246 + self.by)], fill='orange')
        draw.polygon([(432 + self.bx, 158 + self.by), (446 + self.bx, 74 + self.by), (434 + self.bx, 12 + self.by), (422 + self.bx, 84 + self.by)], fill='blue')
        draw.polygon([(462 + self.bx, 364 + self.by), (448 + self.bx, 440 + self.by), (436 + self.bx, 366 + self.by), (446 + self.bx, 282 + self.by)], fill='red')
        draw.polygon([(432 + self.bx, 352 + self.by), (422 + self.bx, 264 + self.by), (432 + self.bx, 180 + self.by), (446 + self.bx, 264 + self.by)], fill='red')
        draw.polygon([(418 + self.bx, 100 + self.by), (428 + self.bx, 166 + self.by), (420 + self.bx, 240 + self.by), (410 + self.bx, 164 + self.by)], fill='red')
        draw.polygon([(444 + self.bx, 454 + self.by), (432 + self.bx, 370 + self.by), (422 + self.bx, 442 + self.by), (432 + self.bx, 514 + self.by)], fill='red')
        draw.polygon([(428 + self.bx, 362 + self.by), (418 + self.bx, 438 + self.by), (410 + self.bx, 360 + self.by), (420 + self.bx, 292 + self.by)], fill='red')
        draw.polygon([(404 + self.bx, 354 + self.by), (418 + self.bx, 264 + self.by), (408 + self.bx, 180 + self.by), (398 + self.bx, 264 + self.by)], fill='red')
        
        # orange side (F)
        draw.polygon([(10 + self.bx, 272 + self.by), (148 + self.bx, 272 + self.by), (156 + self.bx, 362 + self.by), (28 + self.bx, 362 + self.by)], fill='yellow')
        draw.polygon([(172 + self.bx, 272 + self.by), (312 + self.bx, 272 + self.by), (306 + self.bx, 362 + self.by), (178 + self.bx, 362 + self.by)], fill='blue')
        draw.polygon([(336 + self.bx, 272 + self.by), (474 + self.bx, 272 + self.by), (456 + self.bx, 362 + self.by), (328 + self.bx, 362 + self.by)], fill='green')
        draw.polygon([(32 + self.bx, 376 + self.by), (158 + self.bx, 376 + self.by), (164 + self.bx, 450 + self.by), (46 + self.bx, 450 + self.by)], fill='blue')
        draw.polygon([(180 + self.bx, 376 + self.by), (304 + self.bx, 376 + self.by), (300 + self.bx, 450 + self.by), (184 + self.bx, 450 + self.by)], fill='blue')
        draw.polygon([(328 + self.bx, 376 + self.by), (452 + self.bx, 376 + self.by), (438 + self.bx, 450 + self.by), (320 + self.bx, 450 + self.by)], fill='blue')
        draw.polygon([(48 + self.bx, 464 + self.by), (164 + self.bx, 464 + self.by), (170 + self.bx, 526 + self.by), (62 + self.bx, 526 + self.by)], fill='blue')
        draw.polygon([(186 + self.bx, 464 + self.by), (298 + self.bx, 464 + self.by), (296 + self.bx, 526 + self.by), (188 + self.bx, 526 + self.by)], fill='blue')
        draw.polygon([(320 + self.bx, 462 + self.by), (436 + self.bx, 462 + self.by), (422 + self.bx, 526 + self.by), (314 + self.bx, 526 + self.by)], fill='blue')
        
        # yellow side (U)
        draw.polygon([(60 + self.bx, 0 + self.by), (168 + self.bx, 0 + self.by), (164 + self.bx, 64 + self.by), (48 + self.bx, 64 + self.by)], fill='blue')
        draw.polygon([(188 + self.bx, 0 + self.by), (296 + self.bx, 0 + self.by), (300 + self.bx, 64 + self.by), (184 + self.bx, 64 + self.by)], fill='yellow')
        draw.polygon([(316 + self.bx, 0 + self.by), (424 + self.bx, 0 + self.by), (436 + self.bx, 64 + self.by), (320 + self.bx, 64 + self.by)], fill='orange')
        draw.polygon([(44 + self.bx, 76 + self.by), (162 + self.bx, 76 + self.by), (156 + self.bx, 152 + self.by), (30 + self.bx, 152 + self.by)], fill='yellow')
        draw.polygon([(184 + self.bx, 76 + self.by), (300 + self.bx, 76 + self.by), (304 + self.bx, 150 + self.by), (180 + self.bx, 150 + self.by)], fill='yellow')
        draw.polygon([(322 + self.bx, 76 + self.by), (440 + self.bx, 76 + self.by), (452 + self.bx, 152 + self.by), (328 + self.bx, 152 + self.by)], fill='yellow')
        draw.polygon([(28 + self.bx, 166 + self.by), (156 + self.bx, 166 + self.by), (148 + self.bx, 256 + self.by), (10 + self.bx, 256 + self.by)], fill='red')
        draw.polygon([(178 + self.bx, 166 + self.by), (306 + self.bx, 166 + self.by), (310 + self.bx, 254 + self.by), (174 + self.bx, 254 + self.by)], fill='yellow')
        draw.polygon([(328 + self.bx, 166 + self.by), (456 + self.bx, 166 + self.by), (474 + self.bx, 254 + self.by), (336 + self.bx, 254 + self.by)], fill='yellow')

    def drawYperm(self, draw):

        # white side (D)
        draw.polygon([(74 + self.bx, 438 + self.by), (174 + self.bx, 438 + self.by), (170 + self.bx, 522 + self.by), (66 + self.bx, 522 + self.by)], fill='white')
        draw.polygon([(192 + self.bx, 438 + self.by), (294 + self.bx, 438 + self.by), (298 + self.bx, 522 + self.by), (188 + self.bx, 522 + self.by)], fill='white')
        draw.polygon([(310 + self.bx, 436 + self.by), (410 + self.bx, 436 + self.by), (414 + self.bx, 524 + self.by), (314 + self.bx, 524 + self.by)], fill='white')
        draw.polygon([(84 + self.bx, 348 + self.by), (178 + self.bx, 348 + self.by), (174 + self.bx, 422 + self.by), (76 + self.bx, 422 + self.by)], fill='white')
        draw.polygon([(196 + self.bx, 348 + self.by), (288 + self.bx, 348 + self.by), (292 + self.bx, 424 + self.by), (192 + self.bx, 424 + self.by)], fill='white')
        draw.polygon([(306 + self.bx, 348 + self.by), (400 + self.bx, 348 + self.by), (404 + self.bx, 424 + self.by), (310 + self.bx, 424 + self.by)], fill='white')
        draw.polygon([(94 + self.bx, 270 + self.by), (182 + self.bx, 270 + self.by), (178 + self.bx, 336 + self.by), (84 + self.bx, 336 + self.by)], fill='white')
        draw.polygon([(198 + self.bx, 270 + self.by), (286 + self.bx, 270 + self.by), (290 + self.bx, 336 + self.by), (194 + self.bx, 336 + self.by)], fill='white')
        draw.polygon([(302 + self.bx, 268 + self.by), (390 + self.bx, 268 + self.by), (398 + self.bx, 336 + self.by), (306 + self.bx, 336 + self.by)], fill='white')
        
        # red side (B)
        draw.polygon([(414 + self.bx, 2 + self.by), (314 + self.bx, 2 + self.by), (310 + self.bx, 90 + self.by), (410 + self.bx, 90 + self.by)], fill='green')
        draw.polygon([(298 + self.bx, 4 + self.by), (188 + self.bx, 4 + self.by), (192 + self.bx, 88 + self.by), (292 + self.bx, 88 + self.by)], fill='orange')
        draw.polygon([(170 + self.bx, 4 + self.by), (66 + self.bx, 4 + self.by), (74 + self.bx, 88 + self.by), (174 + self.bx, 88 + self.by)], fill='blue')
        draw.polygon([(404 + self.bx, 102 + self.by), (310 + self.bx, 102 + self.by), (306 + self.bx, 178 + self.by), (400 + self.bx, 178 + self.by)], fill='green')
        draw.polygon([(292 + self.bx, 102 + self.by), (192 + self.bx, 102 + self.by), (196 + self.bx, 178 + self.by), (288 + self.bx, 178 + self.by)], fill='green')
        draw.polygon([(174 + self.bx, 104 + self.by), (76 + self.bx, 104 + self.by), (84 + self.bx, 178 + self.by), (178 + self.bx, 178 + self.by)], fill='green')
        draw.polygon([(398 + self.bx, 190 + self.by), (306 + self.bx, 190 + self.by), (302 + self.bx, 258 + self.by), (390 + self.bx, 258 + self.by)], fill='green')
        draw.polygon([(290 + self.bx, 190 + self.by), (194 + self.bx, 190 + self.by), (198 + self.bx, 256 + self.by), (286 + self.bx, 256 + self.by)], fill='green')
        draw.polygon([(178 + self.bx, 190 + self.by), (84 + self.bx, 190 + self.by), (94 + self.bx, 256 + self.by), (182 + self.bx, 256 + self.by)], fill='green')
        
        # green side (L)
        draw.polygon([(52 + self.bx, 158 + self.by), (38 + self.bx, 74 + self.by), (50 + self.bx, 12 + self.by), (62 + self.bx, 84 + self.by)], fill='red')
        draw.polygon([(20 + self.bx, 162 + self.by), (36 + self.bx, 86 + self.by), (48 + self.bx, 164 + self.by), (36 + self.bx, 246 + self.by)], fill='green')
        draw.polygon([(0 + self.bx, 264 + self.by), (18 + self.bx, 174 + self.by), (34 + self.bx, 264 + self.by), (18 + self.bx, 352 + self.by)], fill='orange')
        draw.polygon([(66 + self.bx, 100 + self.by), (56 + self.bx, 166 + self.by), (64 + self.bx, 240 + self.by), (74 + self.bx, 164 + self.by)], fill='orange')
        draw.polygon([(52 + self.bx, 352 + self.by), (62 + self.bx, 264 + self.by), (52 + self.bx, 180 + self.by), (38 + self.bx, 264 + self.by)], fill='orange')
        draw.polygon([(22 + self.bx, 364 + self.by), (36 + self.bx, 440 + self.by), (48 + self.bx, 366 + self.by), (36 + self.bx, 282 + self.by)], fill='orange')
        draw.polygon([(80 + self.bx, 354 + self.by), (66 + self.bx, 264 + self.by), (76 + self.bx, 180 + self.by), (86 + self.bx, 264 + self.by)], fill='orange')
        draw.polygon([(56 + self.bx, 362 + self.by), (66 + self.bx, 438 + self.by), (74 + self.bx, 360 + self.by), (64 + self.bx, 292 + self.by)], fill='orange')
        draw.polygon([(40 + self.bx, 454 + self.by), (52 + self.bx, 370 + self.by), (62 + self.bx, 442 + self.by), (52 + self.bx, 514 + self.by)], fill='orange')
        
        # blue side (R)
        draw.polygon([(484 + self.bx, 264 + self.by), (466 + self.bx, 174 + self.by), (450 + self.bx, 264 + self.by), (466 + self.bx, 352 + self.by)], fill='orange')
        draw.polygon([(464 + self.bx, 162 + self.by), (448 + self.bx, 86 + self.by), (436 + self.bx, 164 + self.by), (448 + self.bx, 246 + self.by)], fill='red')
        draw.polygon([(432 + self.bx, 158 + self.by), (446 + self.bx, 74 + self.by), (434 + self.bx, 12 + self.by), (422 + self.bx, 84 + self.by)], fill='red')
        draw.polygon([(462 + self.bx, 364 + self.by), (448 + self.bx, 440 + self.by), (436 + self.bx, 366 + self.by), (446 + self.bx, 282 + self.by)], fill='red')
        draw.polygon([(432 + self.bx, 352 + self.by), (422 + self.bx, 264 + self.by), (432 + self.bx, 180 + self.by), (446 + self.bx, 264 + self.by)], fill='red')
        draw.polygon([(418 + self.bx, 100 + self.by), (428 + self.bx, 166 + self.by), (420 + self.bx, 240 + self.by), (410 + self.bx, 164 + self.by)], fill='red')
        draw.polygon([(444 + self.bx, 454 + self.by), (432 + self.bx, 370 + self.by), (422 + self.bx, 442 + self.by), (432 + self.bx, 514 + self.by)], fill='red')
        draw.polygon([(428 + self.bx, 362 + self.by), (418 + self.bx, 438 + self.by), (410 + self.bx, 360 + self.by), (420 + self.bx, 292 + self.by)], fill='red')
        draw.polygon([(404 + self.bx, 354 + self.by), (418 + self.bx, 264 + self.by), (408 + self.bx, 180 + self.by), (398 + self.bx, 264 + self.by)], fill='red')
        
        # orange side (F)
        draw.polygon([(10 + self.bx, 272 + self.by), (148 + self.bx, 272 + self.by), (156 + self.bx, 362 + self.by), (28 + self.bx, 362 + self.by)], fill='blue')
        draw.polygon([(172 + self.bx, 272 + self.by), (312 + self.bx, 272 + self.by), (306 + self.bx, 362 + self.by), (178 + self.bx, 362 + self.by)], fill='blue')
        draw.polygon([(336 + self.bx, 272 + self.by), (474 + self.bx, 272 + self.by), (456 + self.bx, 362 + self.by), (328 + self.bx, 362 + self.by)], fill='green')
        draw.polygon([(32 + self.bx, 376 + self.by), (158 + self.bx, 376 + self.by), (164 + self.bx, 450 + self.by), (46 + self.bx, 450 + self.by)], fill='blue')
        draw.polygon([(180 + self.bx, 376 + self.by), (304 + self.bx, 376 + self.by), (300 + self.bx, 450 + self.by), (184 + self.bx, 450 + self.by)], fill='blue')
        draw.polygon([(328 + self.bx, 376 + self.by), (452 + self.bx, 376 + self.by), (438 + self.bx, 450 + self.by), (320 + self.bx, 450 + self.by)], fill='blue')
        draw.polygon([(48 + self.bx, 464 + self.by), (164 + self.bx, 464 + self.by), (170 + self.bx, 526 + self.by), (62 + self.bx, 526 + self.by)], fill='blue')
        draw.polygon([(186 + self.bx, 464 + self.by), (298 + self.bx, 464 + self.by), (296 + self.bx, 526 + self.by), (188 + self.bx, 526 + self.by)], fill='blue')
        draw.polygon([(320 + self.bx, 462 + self.by), (436 + self.bx, 462 + self.by), (422 + self.bx, 526 + self.by), (314 + self.bx, 526 + self.by)], fill='blue')
        
        # yellow side (U)
        draw.polygon([(60 + self.bx, 0 + self.by), (168 + self.bx, 0 + self.by), (164 + self.bx, 64 + self.by), (48 + self.bx, 64 + self.by)], fill='yellow')
        draw.polygon([(188 + self.bx, 0 + self.by), (296 + self.bx, 0 + self.by), (300 + self.bx, 64 + self.by), (184 + self.bx, 64 + self.by)], fill='yellow')
        draw.polygon([(316 + self.bx, 0 + self.by), (424 + self.bx, 0 + self.by), (436 + self.bx, 64 + self.by), (320 + self.bx, 64 + self.by)], fill='yellow')
        draw.polygon([(44 + self.bx, 76 + self.by), (162 + self.bx, 76 + self.by), (156 + self.bx, 152 + self.by), (30 + self.bx, 152 + self.by)], fill='yellow')
        draw.polygon([(184 + self.bx, 76 + self.by), (300 + self.bx, 76 + self.by), (304 + self.bx, 150 + self.by), (180 + self.bx, 150 + self.by)], fill='yellow')
        draw.polygon([(322 + self.bx, 76 + self.by), (440 + self.bx, 76 + self.by), (452 + self.bx, 152 + self.by), (328 + self.bx, 152 + self.by)], fill='yellow')
        draw.polygon([(28 + self.bx, 166 + self.by), (156 + self.bx, 166 + self.by), (148 + self.bx, 256 + self.by), (10 + self.bx, 256 + self.by)], fill='yellow')
        draw.polygon([(178 + self.bx, 166 + self.by), (306 + self.bx, 166 + self.by), (310 + self.bx, 254 + self.by), (174 + self.bx, 254 + self.by)], fill='yellow')
        draw.polygon([(328 + self.bx, 166 + self.by), (456 + self.bx, 166 + self.by), (474 + self.bx, 254 + self.by), (336 + self.bx, 254 + self.by)], fill='yellow')

    def drawUperm(self, draw):
        # white side (D)
        draw.polygon([(74 + self.bx, 438 + self.by), (174 + self.bx, 438 + self.by), (170 + self.bx, 522 + self.by), (66 + self.bx, 522 + self.by)], fill='white')
        draw.polygon([(192 + self.bx, 438 + self.by), (294 + self.bx, 438 + self.by), (298 + self.bx, 522 + self.by), (188 + self.bx, 522 + self.by)], fill='white')
        draw.polygon([(310 + self.bx, 436 + self.by), (410 + self.bx, 436 + self.by), (414 + self.bx, 524 + self.by), (314 + self.bx, 524 + self.by)], fill='white')
        draw.polygon([(84 + self.bx, 348 + self.by), (178 + self.bx, 348 + self.by), (174 + self.bx, 422 + self.by), (76 + self.bx, 422 + self.by)], fill='white')
        draw.polygon([(196 + self.bx, 348 + self.by), (288 + self.bx, 348 + self.by), (292 + self.bx, 424 + self.by), (192 + self.bx, 424 + self.by)], fill='white')
        draw.polygon([(306 + self.bx, 348 + self.by), (400 + self.bx, 348 + self.by), (404 + self.bx, 424 + self.by), (310 + self.bx, 424 + self.by)], fill='white')
        draw.polygon([(94 + self.bx, 270 + self.by), (182 + self.bx, 270 + self.by), (178 + self.bx, 336 + self.by), (84 + self.bx, 336 + self.by)], fill='white')
        draw.polygon([(198 + self.bx, 270 + self.by), (286 + self.bx, 270 + self.by), (290 + self.bx, 336 + self.by), (194 + self.bx, 336 + self.by)], fill='white')
        draw.polygon([(302 + self.bx, 268 + self.by), (390 + self.bx, 268 + self.by), (398 + self.bx, 336 + self.by), (306 + self.bx, 336 + self.by)], fill='white')
        
        # red side (B)
        draw.polygon([(414 + self.bx, 2 + self.by), (314 + self.bx, 2 + self.by), (310 + self.bx, 90 + self.by), (410 + self.bx, 90 + self.by)], fill='green')
        draw.polygon([(298 + self.bx, 4 + self.by), (188 + self.bx, 4 + self.by), (192 + self.bx, 88 + self.by), (292 + self.bx, 88 + self.by)], fill='red')
        draw.polygon([(170 + self.bx, 4 + self.by), (66 + self.bx, 4 + self.by), (74 + self.bx, 88 + self.by), (174 + self.bx, 88 + self.by)], fill='green')
        draw.polygon([(404 + self.bx, 102 + self.by), (310 + self.bx, 102 + self.by), (306 + self.bx, 178 + self.by), (400 + self.bx, 178 + self.by)], fill='green')
        draw.polygon([(292 + self.bx, 102 + self.by), (192 + self.bx, 102 + self.by), (196 + self.bx, 178 + self.by), (288 + self.bx, 178 + self.by)], fill='green')
        draw.polygon([(174 + self.bx, 104 + self.by), (76 + self.bx, 104 + self.by), (84 + self.bx, 178 + self.by), (178 + self.bx, 178 + self.by)], fill='green')
        draw.polygon([(398 + self.bx, 190 + self.by), (306 + self.bx, 190 + self.by), (302 + self.bx, 258 + self.by), (390 + self.bx, 258 + self.by)], fill='green')
        draw.polygon([(290 + self.bx, 190 + self.by), (194 + self.bx, 190 + self.by), (198 + self.bx, 256 + self.by), (286 + self.bx, 256 + self.by)], fill='green')
        draw.polygon([(178 + self.bx, 190 + self.by), (84 + self.bx, 190 + self.by), (94 + self.bx, 256 + self.by), (182 + self.bx, 256 + self.by)], fill='green')
        
        # green side (L)
        draw.polygon([(52 + self.bx, 158 + self.by), (38 + self.bx, 74 + self.by), (50 + self.bx, 12 + self.by), (62 + self.bx, 84 + self.by)], fill='orange')
        draw.polygon([(20 + self.bx, 162 + self.by), (36 + self.bx, 86 + self.by), (48 + self.bx, 164 + self.by), (36 + self.bx, 246 + self.by)], fill='green')
        draw.polygon([(0 + self.bx, 264 + self.by), (18 + self.bx, 174 + self.by), (34 + self.bx, 264 + self.by), (18 + self.bx, 352 + self.by)], fill='orange')
        draw.polygon([(66 + self.bx, 100 + self.by), (56 + self.bx, 166 + self.by), (64 + self.bx, 240 + self.by), (74 + self.bx, 164 + self.by)], fill='orange')
        draw.polygon([(52 + self.bx, 352 + self.by), (62 + self.bx, 264 + self.by), (52 + self.bx, 180 + self.by), (38 + self.bx, 264 + self.by)], fill='orange')
        draw.polygon([(22 + self.bx, 364 + self.by), (36 + self.bx, 440 + self.by), (48 + self.bx, 366 + self.by), (36 + self.bx, 282 + self.by)], fill='orange')
        draw.polygon([(80 + self.bx, 354 + self.by), (66 + self.bx, 264 + self.by), (76 + self.bx, 180 + self.by), (86 + self.bx, 264 + self.by)], fill='orange')
        draw.polygon([(56 + self.bx, 362 + self.by), (66 + self.bx, 438 + self.by), (74 + self.bx, 360 + self.by), (64 + self.bx, 292 + self.by)], fill='orange')
        draw.polygon([(40 + self.bx, 454 + self.by), (52 + self.bx, 370 + self.by), (62 + self.bx, 442 + self.by), (52 + self.bx, 514 + self.by)], fill='orange')
        
        # blue side (R)
        draw.polygon([(484 + self.bx, 264 + self.by), (466 + self.bx, 174 + self.by), (450 + self.bx, 264 + self.by), (466 + self.bx, 352 + self.by)], fill='red')
        draw.polygon([(464 + self.bx, 162 + self.by), (448 + self.bx, 86 + self.by), (436 + self.bx, 164 + self.by), (448 + self.bx, 246 + self.by)], fill='orange')
        draw.polygon([(432 + self.bx, 158 + self.by), (446 + self.bx, 74 + self.by), (434 + self.bx, 12 + self.by), (422 + self.bx, 84 + self.by)], fill='red')
        draw.polygon([(462 + self.bx, 364 + self.by), (448 + self.bx, 440 + self.by), (436 + self.bx, 366 + self.by), (446 + self.bx, 282 + self.by)], fill='red')
        draw.polygon([(432 + self.bx, 352 + self.by), (422 + self.bx, 264 + self.by), (432 + self.bx, 180 + self.by), (446 + self.bx, 264 + self.by)], fill='red')
        draw.polygon([(418 + self.bx, 100 + self.by), (428 + self.bx, 166 + self.by), (420 + self.bx, 240 + self.by), (410 + self.bx, 164 + self.by)], fill='red')
        draw.polygon([(444 + self.bx, 454 + self.by), (432 + self.bx, 370 + self.by), (422 + self.bx, 442 + self.by), (432 + self.bx, 514 + self.by)], fill='red')
        draw.polygon([(428 + self.bx, 362 + self.by), (418 + self.bx, 438 + self.by), (410 + self.bx, 360 + self.by), (420 + self.bx, 292 + self.by)], fill='red')
        draw.polygon([(404 + self.bx, 354 + self.by), (418 + self.bx, 264 + self.by), (408 + self.bx, 180 + self.by), (398 + self.bx, 264 + self.by)], fill='red')
        
        # orange side (F)
        draw.polygon([(10 + self.bx, 272 + self.by), (148 + self.bx, 272 + self.by), (156 + self.bx, 362 + self.by), (28 + self.bx, 362 + self.by)], fill='blue')
        draw.polygon([(172 + self.bx, 272 + self.by), (312 + self.bx, 272 + self.by), (306 + self.bx, 362 + self.by), (178 + self.bx, 362 + self.by)], fill='blue')
        draw.polygon([(336 + self.bx, 272 + self.by), (474 + self.bx, 272 + self.by), (456 + self.bx, 362 + self.by), (328 + self.bx, 362 + self.by)], fill='blue')
        draw.polygon([(32 + self.bx, 376 + self.by), (158 + self.bx, 376 + self.by), (164 + self.bx, 450 + self.by), (46 + self.bx, 450 + self.by)], fill='blue')
        draw.polygon([(180 + self.bx, 376 + self.by), (304 + self.bx, 376 + self.by), (300 + self.bx, 450 + self.by), (184 + self.bx, 450 + self.by)], fill='blue')
        draw.polygon([(328 + self.bx, 376 + self.by), (452 + self.bx, 376 + self.by), (438 + self.bx, 450 + self.by), (320 + self.bx, 450 + self.by)], fill='blue')
        draw.polygon([(48 + self.bx, 464 + self.by), (164 + self.bx, 464 + self.by), (170 + self.bx, 526 + self.by), (62 + self.bx, 526 + self.by)], fill='blue')
        draw.polygon([(186 + self.bx, 464 + self.by), (298 + self.bx, 464 + self.by), (296 + self.bx, 526 + self.by), (188 + self.bx, 526 + self.by)], fill='blue')
        draw.polygon([(320 + self.bx, 462 + self.by), (436 + self.bx, 462 + self.by), (422 + self.bx, 526 + self.by), (314 + self.bx, 526 + self.by)], fill='blue')
        
        # yellow side (U)
        draw.polygon([(60 + self.bx, 0 + self.by), (168 + self.bx, 0 + self.by), (164 + self.bx, 64 + self.by), (48 + self.bx, 64 + self.by)], fill='yellow')
        draw.polygon([(188 + self.bx, 0 + self.by), (296 + self.bx, 0 + self.by), (300 + self.bx, 64 + self.by), (184 + self.bx, 64 + self.by)], fill='yellow')
        draw.polygon([(316 + self.bx, 0 + self.by), (424 + self.bx, 0 + self.by), (436 + self.bx, 64 + self.by), (320 + self.bx, 64 + self.by)], fill='yellow')
        draw.polygon([(44 + self.bx, 76 + self.by), (162 + self.bx, 76 + self.by), (156 + self.bx, 152 + self.by), (30 + self.bx, 152 + self.by)], fill='yellow')
        draw.polygon([(184 + self.bx, 76 + self.by), (300 + self.bx, 76 + self.by), (304 + self.bx, 150 + self.by), (180 + self.bx, 150 + self.by)], fill='yellow')
        draw.polygon([(322 + self.bx, 76 + self.by), (440 + self.bx, 76 + self.by), (452 + self.bx, 152 + self.by), (328 + self.bx, 152 + self.by)], fill='yellow')
        draw.polygon([(28 + self.bx, 166 + self.by), (156 + self.bx, 166 + self.by), (148 + self.bx, 256 + self.by), (10 + self.bx, 256 + self.by)], fill='yellow')
        draw.polygon([(178 + self.bx, 166 + self.by), (306 + self.bx, 166 + self.by), (310 + self.bx, 254 + self.by), (174 + self.bx, 254 + self.by)], fill='yellow')
        draw.polygon([(328 + self.bx, 166 + self.by), (456 + self.bx, 166 + self.by), (474 + self.bx, 254 + self.by), (336 + self.bx, 254 + self.by)], fill='yellow')

    #draws all the amazing visuals for this function
    def draw(self):

        # Clear the screen with background color
        self.screen.fill(BACKGROUND_COLOR)
        
        # Create a PIL image for drawing
        img = Image.new('RGB', (SCREEN_WIDTH, SCREEN_HEIGHT), color=BACKGROUND_COLOR)
        draw = ImageDraw.Draw(img)

        # Draw all cube faces
        self.drawYellowFace(draw) 
        self.drawBlueFace(draw) 
        self.drawRedFace(draw) 
        self.drawOrangeFace(draw) 
        self.drawWhiteFace(draw) 
        self.drawGreenFace(draw) 

        #lots of conditionals to draw all of the states to give examples
        if self.stepsComp == 11:
            self.drawFlowerExample(draw)
        if self.stepsComp == 15:
            self.drawCornerExample1(draw)
        if self.stepsComp == 16:
            self.drawCornerExample2(draw)
        if self.stepsComp == 17:
            self.drawCornerExample3(draw)
        if self.stepsComp == 20:
           self.drawEdgesExample1(draw)
        if self.stepsComp == 21:
            self.drawEdgesExample2(draw)
        if self.stepsComp == 25:
            self.drawEOLL1(draw)
        if self.stepsComp == 26:
            self.drawEOLL2(draw)
        if self.stepsComp == 27:
            self.drawEOLL3(draw)
        if self.stepsComp == 28:
            self.drawEOLL4(draw)
        if self.stepsComp == 31:
            self.drawSune(draw)
        if self.stepsComp == 32:
            self.drawAntiSune(draw)
        if self.stepsComp == 36:
            self.drawTperm(draw)
        if self.stepsComp == 37:
            self.drawYperm(draw)
        if self.stepsComp == 39:
            self.drawUperm(draw)
        
        # Convert PIL image to pygame surface and display it
        mode = img.mode
        size = img.size
        data = img.tobytes()
        py_image = pygame.image.fromstring(data, size, mode)
        self.screen.blit(py_image, (0, 0))
        
        # Helper function to wrap text
        def wrap_text(text, font, max_width):
            words = text.split(' ')
            lines = []
            current_line = ""
            
            for word in words:
                test_line = current_line + (" " if current_line else "") + word
                if font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                        current_line = word
                    else:
                        lines.append(word)  # Word is too long but we have to show it
            
            if current_line:
                lines.append(current_line)
            
            return lines
        
        # Render the current move sequence text under the cube (around y=550-600)
        if self.text1:
            moves_text = f"Moves: {self.text1}"
            wrapped_moves = wrap_text(moves_text, self.big_font, SCREEN_WIDTH - 40)
            
            # Create background for moves text
            moves_height = len(wrapped_moves) * 28 + 20  # 28 pixels per line + padding
            moves_bg = pygame.Surface((SCREEN_WIDTH, moves_height), pygame.SRCALPHA)
            moves_bg.fill(TEXT_BG_COLOR)
            moves_y_start = 600  # Position under the cube
            self.screen.blit(moves_bg, (0, moves_y_start))
            
            # Render each line of moves
            y_offset = moves_y_start + 10
            for line in wrapped_moves:
                moves_surf = self.big_font.render(line, True, TEXT_COLOR)
                self.screen.blit(moves_surf, (20, y_offset))
                y_offset += 28
            
        # Create text display area at the bottom of the screen for tutorial text
        if self.display_text:
            # Calculate tutorial text area position (below moves)
            tutorial_y_start = 800 
            tutorial_height = SCREEN_HEIGHT - tutorial_y_start
            
            # Create semi-transparent background for tutorial text
            text_bg = pygame.Surface((SCREEN_WIDTH, tutorial_height), pygame.SRCALPHA)
            text_bg.fill(TEXT_BG_COLOR)
            self.screen.blit(text_bg, (0, tutorial_y_start))
            
            # Render each line of tutorial text with wrapping
            y_offset = tutorial_y_start + 10
            lines_shown = 0
            max_lines = (tutorial_height - 20) // 24  # Calculate how many lines fit
            
            for text_line in self.display_text[-max_lines:]:  # Show as many lines as fit
                wrapped_lines = wrap_text(text_line, self.font, SCREEN_WIDTH - 40)
                
                for wrapped_line in wrapped_lines:
                    if lines_shown >= max_lines:
                        break
                    text_surf = self.font.render(wrapped_line, True, TEXT_COLOR)
                    self.screen.blit(text_surf, (20, y_offset))
                    y_offset += 24  # Line spacing
                    lines_shown += 1
                
                if lines_shown >= max_lines:
                    break
        
        # Update the display
        pygame.display.flip()
    
    def handleKeyPress(self, key):
        if key == pygame.K_1: 
            self.moveSPrime()
            self.text1 += "S' "
        elif key == pygame.K_2: 
            self.moveE()
            self.text1 += "E "
        elif key == pygame.K_5: 
            self.moveM()
            self.text1 += "M "
        elif key == pygame.K_6: 
            self.moveM()
            self.text1 += "M "
        elif key == pygame.K_9:
            self.moveEPrime()
            self.text1 += "E' "
        elif key == pygame.K_0:
            self.moveS()
            self.text1 += "S "
        elif key == pygame.K_q: 
            self.rotateCubeZprime()
            self.text1 += "z' "
        elif key == pygame.K_w: 
            self.moveB()
            self.text1 += "B "
        elif key == pygame.K_e:
            self.moveLPrime()
            self.text1 += "L' "
        elif key == pygame.K_r:
            self.moveLwPrime()
            self.text1 += "Lw' "
        elif key == pygame.K_t: 
            self.rotateCubeX()
            self.text1 += "x "
        elif key == pygame.K_y: 
            self.rotateCubeX()
            self.text1 += "x "
        elif key == pygame.K_u: 
            self.moveRw()
            self.text1 += "Rw "
        elif key == pygame.K_i: 
            self.moveR()
            self.text1 += "R "
        elif key == pygame.K_o: 
            self.moveBPrime()
            self.text1 += "B' "
        elif key == pygame.K_p: 
            self.rotateCubeZ()
            self.text1 += 'z '
        elif key == pygame.K_a: 
            self.rotateCubeYprime()
            self.text1 += "y' "
        elif key == pygame.K_s:
            self.moveD()
            self.text1 += "D "
        elif key == pygame.K_d:
            self.moveL()
            self.text1 += "L "
        elif key == pygame.K_f: 
            self.moveUPrime()
            self.text1 += "U' "
        elif key == pygame.K_g: 
            self.moveFPrime()
            self.text1 += "F' "
        elif key == pygame.K_h: 
            self.moveF()
            self.text1 += "F "
        elif key == pygame.K_j:
            self.moveU()
            self.text1 += "U "
        elif key == pygame.K_k: 
            self.moveRPrime()
            self.text1 += "R' "
        elif key == pygame.K_l: 
            self.moveDPrime()
            self.text1 += "D' "
        elif key == pygame.K_SEMICOLON: 
            self.rotateCubeY()
            self.text1 += "y "
        elif key == pygame.K_z: 
            self.moveDw()
            self.text1 += "Dw "
        elif key == pygame.K_x:
            self.moveMPrime()
            self.text1 += "M' "
        elif key == pygame.K_c: 
            self.moveUwPrime()
            self.text1 += "Uw' "
        elif key == pygame.K_v:
            self.moveLw()
            self.text1 += "Lw "
        elif key == pygame.K_b:
            self.rotateCubeXprime()
            self.text1 += "x' "
        elif key == pygame.K_n:
            self.rotateCubeXprime()
            self.text1 += "x' "
        elif key == pygame.K_m:
            self.moveRwPrime()
            self.text1 += "Rw' "
        #elif key == pygame.K_BACKSLASH:
            #self.goToSolver()
            #self.text1 = ""
        elif key == pygame.K_COMMA:
            self.moveUw()
            self.text1 += "Uw "
        elif key == pygame.K_PERIOD: 
            self.moveMPrime()
            self.text1 += "M' "
        elif key == pygame.K_SLASH: 
            self.moveDwPrime()
            self.text1 += "Dw' "
        elif key == pygame.K_RIGHTBRACKET:
            self.resetCube()
            self.text1 = ""  # Fixed: was == instead of =
        elif key == pygame.K_LEFTBRACKET: 
            self.scrambleCube()
        elif key == pygame.K_EQUALS: 
            self.text1 = ""
        elif key == pygame.K_SPACE: 
            self.stepsComp += 1

        if ((self.stepsComp == 1) and (self.stepHelp != 1)):
            self.stepHelp = 1
            self.display_text = [
                "The first step to solving a Rubik's cube is to learn the notation that is used to show how the cube moves. The moves that I will teach",
                "you are the most basic ones, L, R, F, and U. In addition to these moves, I will teach you rotations such as x, y, z that will help you",
                "move the cube in the way that you want. Although this seems like a lot of information right now, I will go in depth into all of it",
                "click space to continue"
            ]
        if ((self.stepsComp == 2) and (self.stepHelp != 2)): 
            self.stepHelp = 2
            self.display_text = [
                "The first move I will teach you is R. R is a movement of the right layer upwards, to test a normal R move, click either 'i' on your keyboard.",
                "With all moves, there is a normal version as well as an inverse version. This inverse is a downwards movement of the right layer",
                "and is noted as a R', the same as R except with a apostrophe next to it. To do an R' move, click 'k' on your keyboard",
                "Once you are comfortable with these moves, click space to continue"
            ]
        if ((self.stepsComp == 3) and (self.stepHelp != 3)):
            self.stepHelp = 3
            self.display_text = [
                "The next move is L. L represents a downward movement of the left layer and you can do this move by clicking 'd' on your keyboard.",
                "The inverse of this move is denoted as L' and represents an upward movement of the left layer. To do this move, click 'e' on your keyboard",
                "Once you are comfortable with these moves, click space to continue"
            ]
        if ((self.stepsComp == 4) and (self.stepHelp != 4)):
            self.stepHelp = 4
            self.display_text = [
                "The next move, U, is going to be moving the top layer. A normal U move is a clockwise rotation of the U layer. To do this move, click 'j'",
                "The inverse is U', which will move the top layer counterclockwise. To move this layer, click 'f'.",
                "Once you are comfortable with these moves, click space to continue"
            ]
        if ((self.stepsComp == 5) and (self.stepHelp != 5)):
            self.stepHelp = 5
            self.display_text = [
                "The last move, F, is moving the front face of the cube. The normal F move will rotate the front face clockwise. To do this move, click 'h'",
                "As with the other moves, F' is the inverse of F, moving the front face counterclockwise. To do a F', press the 'g' key.",
                "Once you are comfortable with these moves, click space to continue"
            ]
        if ((self.stepsComp == 6) and (self.stepHelp != 6)):
            self.stepHelp = 6
            self.display_text = [
                "Now, we are going to move on to cube rotations. Cube rotations are exactly what they sound like, a rotation of the Rubiks Cube.",
                "With these moves, you can do three rotations, x rotations, y rotations, and z rotations.",
                "Similar to the moves we went over previously, these all have inverses.",
                "All of these rotations will be gone over in the next section, click space to continue"
            ]
        if ((self.stepsComp == 7) and (self.stepHelp != 7)):
            self.stepHelp = 7
            self.display_text = [
                "The first rotation we are going to go over is the x rotation. This rotation will move the front, top, back and bottom faces upwards. To do this, ",
                "click 't' or 'y'. Next is the inverse of this, an x' rotation will move the front, top, back and bottom faces downwards. To do this, click 'b' or 'n' ",
                "Once you feel comfortable with these rotations, click space to continue"
            ]
        if ((self.stepsComp == 8) and (self.stepHelp != 8)):
            self.stepHelp = 8
            self.display_text = [
                "The next rotation is the y rotation. A y rotation will move the front, left, back and right faces clockwise. To do a y rotation, click ';'",
                "After that is the inverse of a y rotation, the y' rotation. This will move the front, right, back, and left faces counterclockwise. To do this, click 'a'",
                "Once you feel comfortable with y rotations, click space to continue"
            ]
        if ((self.stepsComp == 9) and (self.stepHelp != 9)):
            self.stepHelp = 9
            self.display_text = [
                "After this is the final rotation, z rotations. These rotations move the top, right, bottom and left faces clockwise. To do a z rotation, click 'p'.",
                "The last rotation that you should know is z' rotations. These move the top, left, bottom, and right faces counter clockwise. To do a z' rotation, click 'q'",
                "Once you are comfortable with all these moves and rotations, we can start to learn to solve the Rubiks Cube!",
                "Click space to continue"
            ]
        #Flower
        if ((self.stepsComp == 10) and (self.stepHelp != 10)):
            self.stepHelp = 10
            self.scrambleCube()
            self.display_text = [
                "The first step is creating a 'flower'. This Flower is when you put four white edges (the pieces that have only two colors) around the yellow center.",
                "To give an idea as to what this looks like, click space again to see an image of what the flower looks like from the top down."
            ]
        if ((self.stepsComp == 11) and (self.stepHelp != 11)):
            self.stepHelp = 11
            self.display_text = [
                "As you can see in the image, there is a yellow piece in the center with four white edges surrounding it. This is the first step to solving a Rubiks cube.",
                "With this step, there is no algorithm that I can teach you to let you do this easily, this step is mostly just messing around with the cube and seeing if you",
                "can get all four white edges on the yellow side. This step will take some time, and some practice, so don't get discouraged. When doing this step the most",
                "important part is to try to keep the progress you have made.",
                "Once you understand how to make the flower, click space and try it for yourself!"
            ]
        if ((self.stepsComp == 12) and (self.stepHelp != 12)):
            self.stepHelp = 12
            self.display_text = [
                "Now try it yourself and click space once you finish!",
                "Tip: do a x2 rotation to put the yellow side ontop!",
            ]
        if ((self.stepsComp == 13) and (self.stepHelp != 13) and (not self.isFlowerComp())):
            self.stepsComp-=1
        if ((self.stepsComp == 13) and (self.stepHelp != 13) and (self.isFlowerComp())):
            self.stepHelp = 13
            self.display_text = [
                "Great Job! Now it is time to use the flower, to make the cross. To do this, look at the centers on the four surrounding sides, blue, green, red and orange.",
                "All four of the white edges that you have on the yellow side will have one of those colors on its other side. Move the top side until you see one of the colors match,",
                "then do two front moves to move it to the white side. This will solve an edge Repeat this step for the next 3 edges and click space once you are done"
            ]
        if ((self.stepsComp == 14) and (self.stepHelp != 14) and (not self.isCrossComp())):
            self.stepsComp-=1
        if ((self.stepsComp == 14) and (self.stepHelp != 14) and (self.isCrossComp())):
            self.stepHelp = 14
            self.display_text = [
                "Awesome! Now that the cross is done, you can move on to finishing the first layer. To do this, I will have to teach you an algorithm. An Algorithm is a set of moves that is done",
                "to accomplish a specific goal. In this case, I am going to teach you an algorithm, using the notation that I taught you earlier, to solve a corner into the first layer.",
                "First, rotate the cube so that the white side is on the bottom, this will make it easier to find the corners(the pieces that have 3 colors on them) and then put them into",
                "their proper position. Once you have done this, click space to continue"
            ]
        if ((self.stepsComp == 15) and (self.stepHelp != 15)):
            self.stepHelp = 15
            self.display_text = [
                "Now, I will teach you the first algorithm of three algorithms to solve a corner into its correct spot. The first thing I will teach you is how to orient the corner to solve this",
                "The first thing I want to state is that two of the three algorithms require you to make it so that the white side of the corner is facing you. Above is the first example of this",
                "as you can see, the white side of the top left corner is facing towards you. In this case, you need to put the corner into the slot with an algorithm. This algorithm is as follows:",
                " U L' U' L",
                "click space to see the next example"
            ]
        if ((self.stepsComp == 16) and (self.stepHelp != 16)):
            self.stepHelp = 16
            self.display_text = [
                "This next example shows the same thing, except the white sticker of the corner is facing you on the right side. This changes the algorithm you must do to solve this. From this angle, ",
                "Do the moves, U R U' R' to solve the corner into the slot.",
                "Click space to go to the next example"
            ]
        if ((self.stepsComp == 17) and (self.stepHelp != 17)):
            self.stepHelp = 17
            self.display_text = [
                "This last example is unique from the other two, this one has the white sticer facing upwards. To solve this one, place it above where it needs to be, as shown ",
                "in the example, and do the following algorithm: R U R' U' R U R' U' R U R' U'. This algorithm, although longer, is just the same set of moves repeated three times.",
                "if I write the algorithm like this, (R U R' U') (R U R' U') (R U R' U') It is much more evident how repetitive the algorithm is. Once you are comfortable, ",
                "click space to try this out yourself!"
            ]
        if ((self.stepsComp == 18) and (self.stepHelp != 18)):
            self.stepHelp = 18
            self.display_text = [
                "Tip: The three algorithms you need are: ",
                "For the sticker facing you on the right side, (U R U' R') ",
                "For the sticker facing you on the left side, (U L' U' L) ",
                "For the sticker facing you on the right side, (R U R' U') (R U R' U') (R U R' U') "
            ]
        if ((self.stepsComp == 19) and (self.stepHelp != 19) and (not self.is1stLayerComp())):
            self.stepsComp-=1
        if ((self.stepsComp == 19) and (self.stepHelp != 19) and (self.is1stLayerComp())):
            self.stepHelp = 19
            self.display_text = [
                "Great work! Now you have the the basics to solve the first layer of a Rubik's cube! The next step is to solve the second layer. To solve this, ",
                "there are two possible scenarios, the edge has to go into the right spot, or the edge has to go into the left slot. I will elaborate more when you see the ",
                "examples. Click space to continue"
            ]
        if ((self.stepsComp == 20) and (self.stepHelp != 20)):
            self.stepHelp = 20
            self.display_text = [
                "This first example has the edge placed in a manner where it matches the center piece. As you can see, the green on the edge corresponds to the green on the center of the",
                "green side. Then, if you look at the top face, you can see that the other color on the edge is orange. When looking at the cube, you can see that the right side is the orange side.",
                "This means that the orange and green edge has to go between these two sides (green and orange) To solve this edge, place it as shown in the example and do the following moves: ",
                "(U R U' R') (F R' F' R) . This algorithm will solve that given edge into the right slot. ",
                "Click space when you are ready to move to the next example"
            ]
        if ((self.stepsComp == 21) and (self.stepHelp != 21)):
            self.stepHelp = 21
            self.display_text = [
                "This example shows a similar scenario with a red edge aligned with the red center. When looking at the top of the edge, it can be seen that this edge is the red and blue edge.",
                "As the blue side is to the left, the correct position for this edge is the left slot. The left slot has a different algorithm from the right slot, although it has the same setup. ",
                "To solve an edge into the right slot, do the following algorithm: (U' L' U L) (F' L F L') ",
                "Once you feel comfortable, click space to do this yourself!"
            ]
        if ((self.stepsComp == 22) and (self.stepHelp != 22)):
            self.stepHelp = 22
            self.display_text = [
                "Tip: the two algorithms you need are",
                "Edge into left slot, (U' L' U L) (F' L F L') ",
                "Edge into right slot,(U R U' R') (F R' F' R) "
            ]
        if ((self.stepsComp == 23) and (self.stepHelp != 23) and (not self.is2ndLayerComp())):
            self.stepsComp-=1
        if ((self.stepsComp == 23) and (self.stepHelp != 23) and (self.is2ndLayerComp())):
            self.stepHelp = 23
            self.display_text = [
                "Amazing work! Now, we can move onto the last layer. This part of learning to solve a Rubik's Cube is very straight forward and is largely algorithmic. ",
                "This means that I will have to teach you a few algorithms to solve this layer. Click space to continue"
            ]
        if ((self.stepsComp == 24) and (self.stepHelp != 24)):
            self.stepHelp = 24
            self.display_text = [
                "The first step of the last layer is to make all of the edges on the top yellow. There are three possible cases you can get when looking at the edges. ",
                "You can have 0 yellow edges, 2 yellow edges making an 'L' shape and, lastly, 2 yellow edges making a line. To see these examples with the ",
                "algorithms to solve them, click space"
            ]
        if ((self.stepsComp == 25) and (self.stepHelp != 25)):
            self.stepHelp = 25
            self.display_text = [
                "This first example shows when none of the edges are yellow. As you can see, the edges, which are the pieces with only two colors, are not yellow. ",
                "The goal of this step is to make those edges all have the yellow on the top to make yellow cross. To solve this case, you can orient it in anyway ",
                "and do the following algorithm: F (U R U' R') F' U' F ( R U R' U') F' ", 
                "This algorithm, although long, is relatively easy to learn. Once you feel comfortable with this, click space to move on to the next example"
            ]
        if ((self.stepsComp == 26) and (self.stepHelp != 26)):
            self.stepHelp = 26
            self.display_text = [
                "This example has two yellow edges making an L shape. This L shape is selfarent from the two yellow edges being next to eachother. ", 
                "This case is much easier to solve, although it has to be oriented in a particular way. As you can see in the image, the orientation ",
                "has it so that the two yellow edges are on the back, and the left sides. This is how you have to orient it when doing this algorithm. ",
                "The algorithm is as follows: F ( U R U' R') F' if you remember the last algorithm, you will see that to solve the two edges, ",
                "you are merely doing the first part of it. When you feel comfortable with this algorithm, click space to continue"
            ]
        if ((self.stepsComp == 27) and (self.stepHelp != 27)):
            self.stepHelp = 27
            self.display_text = [
                "This example, similar to the last one, has two yellow edges. However, in this case, the two yellow edges make a line rather than an L.", 
                "This case requires the line to be oriented so that the yellow edges are on the left and right sides. To solve this case, do the ",
                "following algorithm: F ( R U R' U') F' the algorithm to solve this case, is merely the second half of the algorithm to solve the",
                "yellow cross when you have no edges solved when you are comfortable with this, click space to continue"
            ]
        if ((self.stepsComp == 28) and (self.stepHelp != 28)):
            self.stepHelp = 28
            self.display_text = [
                "Sometimes, you can skip this step entirely and get the cross to begin with. In this case, you got lucky and don't need to do anything! ",
                "click space to continue"
            ]
        if ((self.stepsComp == 29) and (self.stepHelp != 29)):
            self.display_text = [
                "Now, try it yourself and click space when you are done!",
                "Tip: to solve two edges in an L : F ( U R U' R') F' ",
                "     to solve two edges in a line : F ( R U R' U') F' ",
                "     to solve zero edges : F (U R U' R') F' U' F ( R U R' U') F' "
            ]
        if ((self.stepsComp == 30) and (self.stepHelp != 30) and (not self.isYellowCrossComp())):
            self.stepsComp-=1
        if ((self.stepsComp == 30) and (self.stepHelp != 30) and (self.isYellowCrossComp())):
            self.stepHelp = 30
            self.display_text = [
                "Great Job! Now, we can move on to orienting the yellow corners so that the entire top face is yellow. There are a lot of cases to solve this, ",
                "so instead of showing you every case and giving you a way to solve it, I am going to teach you how to complete this step with only two algorithms: ",
                "the 'Sune' and 'Anti-Sune'. Once you are ready, click space to continue"
            ]
        if ((self.stepsComp == 31) and (self.stepHelp != 31)):
            self.stepHelp = 31
            self.display_text = [
                "What you see infront of you is a 'Sune'. This case is fast and requires one algorithm. When doing a sune or an antisune, you want to make sure two ",
                "things are true when you are doing the algorithm, first, there is a solved corner either on your front right or front left. Second, the other corner ",
                "in the front slot MUST have the yellow side facing towards you. For this case, a sune, you have the front left corner solved and the front right corner has the ",
                "yellow side facing towards you. If you want to solve this case to orient the entire top layer, do the algorithm: R U R' U R U U R' ",
                "Once you feel comfortable with the sune, click space to learn about the antisune"
            ]
        if ((self.stepsComp == 32) and (self.stepHelp != 32)):
            self.stepHelp = 32
            self.display_text = [
                "Above is the anti-sune, a version of the sune algorithm that is a sort of 'lefty' version. To orient this case, you must have the cube in the same ",
                "position as above. This being the front right corner being oriented properly with yellow on top and the front left corner with the yellow side facing ",
                "towards you. To solve this case, do L' U' L U' L' U U L ",
                "In the next step, I will explain how you can use these two algorithms to orient the entire top layer, click space to continue"
            ]
        if ((self.stepsComp == 33) and (self.stepHelp != 33)):
            self.stepHelp = 33
            self.display_text = [
                "There are many different cases, some with the top layer having none of the four corners yellow, some having two, some having one, and some even where ",
                "the entire top side is already yellow. To get the entire top side to be yellow when given any case, you simply have to do a sune or anti-sune until you ",
                "have only one properly oriented edge. With this step, there is no real easy workaround to this, you simply have to mess around and eventually you will get to the step where you",
                "have a sune or anti-sune. Click space to try it on your own!"
            ]
        if ((self.stepsComp == 34) and (self.stepHelp != 34)):
            self.stepHelp = 34
            self.display_text = [
                "Tip",
                "Sune : R U R' U R U U R' ",
                "Anti-Sune : L' U' L U' L' U U L"
            ]
        if ((self.stepsComp == 35) and (self.stepHelp != 35) and (not self.OLLComp())):
            self.stepsComp -=1
        if ((self.stepsComp == 35) and (self.stepHelp != 35) and (self.OLLComp())):
            self.stepHelp = 35
            self.display_text = [
                "Great Job! There are now only 2 steps left to solve the Rubik's Cube! Now, we are going to move on to solving the corners so they are now in the correct positions.",
                "With the corners, there are two possible cases, both of which can use the same algorithm to solve. There can either be two edges that need to swselfed next to eachother, ",
                "or two edges that need to be swselfed diagonally from eachother. First I am going to show you the adjacent swap, click space to move on"
            ]
        if ((self.stepsComp == 36) and (self.stepHelp != 36)):
            self.stepHelp = 36
            self.display_text = [
                "This case above shows an adjacent swap, where the back right corner and front right corner need to be swselfed with each other. You can notice this case from two things, ",
                "either the fact the two edges next to each other need to be swselfed, or the 'headlights' which are two solved corners next to eachother. If you look at the left side of the ",
                "cube, you can see that these two corners are solved in relation to each other,  both having orange while on the orange side. When solving this case, place the 'headlights' ",
                "to your left and the two corners that need to be swselfed to your right as pictured above. Then, do this algorithm: (R U R' U') (R' F R R) U' (R' U' R U) (R' F')", 
                "When you are comfortable with this algorithm, click space to move on to the next step. "
            ]
        if ((self.stepsComp == 37) and (self.stepHelp != 37)):
            self.stepHelp = 37
            self.display_text = [
                "This case has a diagonal swap where the front right and back left corners need to be swselfed to solve the corners. Instead of learning a new algorithm, you can instead do the algorithm from",
                "the adjacent swap twice. To start, do the adjacent swap from any angle. Then, put the headlights that are created to the left and the two corners that need to be swselfed to the right and do ",
                "the same algorithm from the last step: (R U R' U') (R' F R R) U' (R' U' R U) (R' F') ",
                "Once you are comfortable with this, click space to continue and try this on your own!"
            ]
        if ((self.stepsComp == 38) and (self.stepHelp != 38)):
            self.stepHelp = 38
            self.display_text = [
                "Tip: ",
                "Corner Swap : (R U R' U') (R' F R R) U' (R' U' R U) (R' F') ",
            ]
        if ((self.stepsComp == 39) and (self.stepHelp != 39) and (not self.CPLLComp())):
            self.stepsComp -=1
        if ((self.stepsComp == 39) and (self.stepHelp != 39) and (self.CPLLComp())):
            self.stepHelp = 39
            self.display_text = [
                "Phenomenal Job! Now we can move on to the last step, solving the edges of the last layer. There is only 1 algorithm that you need to know to solve this step, however you may need to do",
                "it multiple times to solve any given case. For this step, I will only show you one example, the one that this algorithm solves and then explain what you have to do to get it to that state,",
                "and what orientation the cube must be in to solve it in this state. click space to continue"
            ]
        if ((self.stepsComp == 40) and (self.stepHelp != 40)):
            self.stepHelp = 40
            self.display_text = [
                "This case is where this algorithm will solve the cube in only one step. Let me now explain what this orientation is, with this, there is only one side with a solved edge with 3 edges swapped.",
                "What you want to do is find a solved edge and place it directly infront of you. If you can't find a solved edge, do the algorithm from any perspective. This will create a solved edge and then ",
                "you can place that solved edge infront of you and repeat the algorithm until the cube is solved. The algorithm is as follows : (R' U R' U') (R' U' R' U) (R U R R) ",
                "This is the last algorithm you need, now click space to finish solving the Rubik's Cube and try this for yourself!"
            ]
        if ((self.stepsComp == 41) and (self.stepHelp != 41)):
            self.stepHelp = 41
            self.display_text = [
                "Tip: "
                "Edge cycle : (R' U R' U') (R' U' R' U) (R U R R) "
            ]
        if ((self.stepsComp == 42) and (self.stepHelp != 42) and (not self.isCubeSolved())):
            self.stepsComp-=1
        if ((self.stepsComp == 42) and (self.stepHelp != 42) and (self.isCubeSolved())):
            self.stepHelp = 42
            self.display_text = [
                "CONGRATULATIONS! You have just solved a Rubik's Cube! Now you can impress your friends with this cool talent or mess around just for fun!",
                "Thank you for using my program and if you would like to do another solve, click space to restart"
            ]
        if (self.stepsComp == 43):
            self.stepsComp = 1
    

    def isFlowerComp(self):
        if(self.U[1][1] != "yellow"):
            return False
        if(self.U[0][1] != "white"):
            return False
        if(self.U[1][0] != "white"):
            return False
        if(self.U[1][2] != "white"):
            return False
        if(self.U[2][1] != "white"):
            return False
        return True
    
    def isCrossComp(self):
        if(self.D[1][1] != "white"):
            return False
        if(self.D[0][1] != "white"):
            return False
        if(self.D[1][0] != "white"):
            return False
        if(self.D[1][2] != "white"):
            return False
        if(self.D[2][1] != "white"):
            return False
        return True

    def is1stLayerComp(self):
        if ( not self.isCrossComp()):
            return False
        if (self.D[0][0] != 'white'):
            return False
        if (self.D[0][2] != 'white'):
            return False
        if (self.D[2][0] != 'white'):
            return False
        if (self.D[2][2] != 'white'):
            return False
        #front check
        if((self.F[1][1] != self.F[2][0]) or (self.F[1][1] != self.F[2][1]) or (self.F[1][1] != self.F[2][1])):
            return False
        #left check
        if((self.L[1][1] != self.L[2][0]) or (self.L[1][1] != self.L[2][1]) or (self.L[1][1] != self.L[2][1])):
            return False
        #right check
        if((self.R[1][1] != self.R[2][0]) or (self.R[1][1] != self.R[2][1]) or (self.R[1][1] != self.R[2][1])):
            return False
        #back check
        if((self.B[1][1] != self.B[2][0]) or (self.B[1][1] != self.B[2][1]) or (self.B[1][1] != self.B[2][1])):
            return False
        return True
        
    def is2ndLayerComp(self):
        if (not self.is1stLayerComp()):
            return False
        #front check
        if ((self.F[1][1] != self.F[1][0]) or (self.F[1][1] != self.F[1][2])):
            return False
        #left check
        if ((self.L[1][1] != self.L[1][0]) or (self.L[1][1] != self.L[1][2])):
            return False
        #right check
        if ((self.R[1][1] != self.R[1][0]) or (self.R[1][1] != self.R[1][2])):
            return False
        #back check
        if ((self.B[1][1] != self.B[1][0]) or (self.B[1][1] != self.B[1][2])):
            return False
        return True
        
    def isYellowCrossComp(self):
        if (not self.is2ndLayerComp()):
            return False
        if(self.U[1][1] != "yellow"):
            return False
        if(self.U[0][1] != "yellow"):
            return False
        if(self.U[1][0] != "yellow"):
            return False
        if(self.U[1][2] != "yellow"):
            return False
        if(self.U[2][1] != "yellow"):
            return False
        return True
        
    def OLLComp(self):
        if (not self.isYellowCrossComp()):
            return False
        if (self.U[0][0] != 'yellow'):
            return False
        if (self.U[0][2] != 'yellow'):
            return False
        if (self.U[2][0] != 'yellow'):
            return False
        if (self.U[2][2] != 'yellow'):
            return False
        return True
        
    def CPLLComp(self):
        if (not self.OLLComp()):
            return False
        #front check
        if (self.F[0][0] != self.F[0][2]):
            return False
        #right check
        if (self.R[0][0] != self.R[0][2]):
            return False
        #left check
        if (self.L[0][0] != self.L[0][2]):
            return False
        #back check
        if (self.B[0][0] != self.B[0][2]):
            return False
        return True    

    def isCubeSolved(self):
        if (not self.CPLLComp()):
            return False
        #front check    
        if ((self.F[1][1] != self.F[0][0]) or (self.F[1][1] != self.F[0][1]) or (self.F[1][1] != self.F[0][2])):
            return False
        #left check
        if ((self.L[1][1] != self.L[0][0]) or (self.L[1][1] != self.L[0][1]) or (self.L[1][1] != self.L[0][2])):
            return False
        #right check
        if ((self.R[1][1] != self.R[0][0]) or (self.R[1][1] != self.R[0][1]) or (self.R[1][1] != self.R[0][2])):
            return False
        #back check
        if ((self.B[1][1] != self.B[0][0]) or (self.B[1][1] != self.B[0][1]) or (self.B[1][1] != self.B[0][2])):
            return False
        return True
    
    def rotateCubeZ(self):
        moveS(self)
        moveF(self)
        moveBPrime(self)
        
    def rotateCubeZprime(self):
        self.moveSPrime()
        self.moveFPrime()
        self.moveB()

    def rotateCubeX(self):
        self.moveR()
        self.moveLPrime()
        self.moveMPrime()

    def rotateCubeXprime(self):
        self.moveRPrime()
        self.moveL()
        self.moveM()

    def rotateCubeY(self):
        self.moveU()
        self.moveDPrime()
        self.moveEPrime()

    def rotateCubeYprime(self):
        self.moveUPrime()
        self.moveD()
        self.moveE()

    def moveU(self):
        #corner swap
        self.U[0][0], self.U[0][2], self.U[2][2], self.U[2][0] = self.U[2][0], self.U[0][0], self.U[0][2], self.U[2][2]
        #edge swap
        self.U[0][1], self.U[1][2], self.U[2][1], self.U[1][0] = self.U[1][0], self.U[0][1], self.U[1][2], self.U[2][1]
        for i in range(3):
            self.B[0][i], self.R[0][i] , self.F[0][i] , self.L[0][i] = self.L[0][i], self.B[0][i], self.R[0][i] , self.F[0][i]
        
    def moveUPrime(self):
        for i in range(3):
            self.moveU()

    def moveR(self):
        #corner swap
        self.R[0][0], self.R[0][2], self.R[2][2], self.R[2][0] = self.R[2][0], self.R[0][0], self.R[0][2], self.R[2][2]
        #edge swap
        self.R[0][1], self.R[1][2], self.R[2][1], self.R[1][0] = self.R[1][0], self.R[0][1], self.R[1][2], self.R[2][1]
        for i in range(3):
            self.U[i][2], self.B[2-i][0] , self.D[i][2] , self.F[i][2] = self.F[i][2], self.U[i][2], self.B[2-i][0] , self.D[i][2]

    def moveRPrime(self):
        for i in range(3):
            self.moveR()

    def moveLPrime(self):
        #corner swap
        self.L[0][0], self.L[0][2], self.L[2][2], self.L[2][0] = self.L[0][2], self.L[2][2], self.L[2][0], self.L[0][0]
        #edge swap
        self.L[0][1], self.L[1][2], self.L[2][1], self.L[1][0] = self.L[1][2], self.L[2][1], self.L[1][0], self.L[0][1]
        for i in range(3):
            self.U[i][0], self.B[2-i][2] , self.D[i][0] , self.F[i][0] = self.F[i][0], self.U[i][0], self.B[2-i][2] , self.D[i][0]

    def moveL(self):
        for i in range(3):
            self.moveLPrime()

    def moveD(self):
        #corner swap
        self.D[0][0], self.D[0][2], self.D[2][2], self.D[2][0] = self.D[2][0], self.D[0][0], self.D[0][2], self.D[2][2]
        #edge swap
        self.D[0][1], self.D[1][2], self.D[2][1], self.D[1][0] = self.D[1][0], self.D[0][1], self.D[1][2], self.D[2][1]
        for i in range(3):
            self.F[2][i], self.R[2][i] , self.B[2][i] , self.L[2][i] = self.L[2][i], self.F[2][i], self.R[2][i] , self.B[2][i]

    def moveDPrime(self):
        for i in range(3):
            self.moveD()

    def moveB(self):
        #corner swap
        self.B[0][0], self.B[0][2], self.B[2][2], self.B[2][0] = self.B[2][0], self.B[0][0], self.B[0][2], self.B[2][2]
        #edge swap
        self.B[0][1], self.B[1][2], self.B[2][1], self.B[1][0] = self.B[1][0], self.B[0][1], self.B[1][2], self.B[2][1]
        for i in range(3):
            self.U[0][i], self.L[2-i][0] , self.D[2][2-i] , self.R[i][2] = self.R[i][2], self.U[0][i], self.L[2-i][0] , self.D[2][2-i]

    def moveBPrime(self):
        for i in range(3):
            self.moveB()

    def moveF(self):
        #corner swap
        self.F[0][0], self.F[0][2], self.F[2][2], self.F[2][0] = self.F[2][0], self.F[0][0], self.F[0][2], self.F[2][2]
        #edge swap
        self.F[0][1], self.F[1][2], self.F[2][1], self.F[1][0] = self.F[1][0], self.F[0][1], self.F[1][2], self.F[2][1]
        for i in range(3):
            self.U[2][i], self.R[i][0] , self.D[0][2-i] , self.L[2-i][2] = self.L[2-i][2], self.U[2][i], self.R[i][0] , self.D[0][2-i]
        
    def moveFPrime(self):
        for i in range(3):
            self.moveF()
            
    def moveMPrime(self):
        #all second column, rotate through the rows
        for i in range(3):
            self.F[i][1], self.U[i][1], self.B[2-i][1], self.D[i][1] = self.D[i][1], self.F[i][1], self.U[i][1], self.B[2-i][1]

    def moveM(self):
        for i in range(3):
            self.moveMPrime()

    def moveRw(self):
        self.moveMPrime()
        self.moveR()

    def moveRwPrime(self):
        self.moveM()
        self.moveRPrime()

    def moveLw(self):
        self.moveM()
        self.moveL()

    def moveLwPrime(self):
        self.moveMPrime()
        self.moveLPrime()
        
    def moveDw(self):
        self.moveD()
        self.moveE()
        
    def moveDwPrime(self):
        self.moveDPrime()
        self.moveEPrime()

    def moveUw(self):
        self.moveU()
        self.moveEPrime()

    def moveUwPrime(self):
        self.moveUPrime()
        self.moveE()

    def moveEPrime(self):
        for i in range(3):
            self.F[1][i], self.R[1][i], self.B[1][i], self.L[1][i] =  self.R[1][i], self.B[1][i], self.L[1][i], self.F[1][i]

    def moveE(self):
        for i in range(3):
            self.moveEPrime()

    def moveSPrime(self):
        for i in range(3):
            self.U[1][i], self.R[i][1], self.D[1][2-i], self.L[2-i][1] =  self.R[i][1], self.D[1][2-i], self.L[2-i][1], self.U[1][i]

    def moveS(self):
        for i in range(3):
            self.moveSPrime()
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.handleKeyPress(event.key)
            
            self.draw()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()

def main():
    cube = RubiksCube()
    cube.run()

if __name__ == "__main__":
    main()