from PIL import Image, ImageDraw
import random
import pygame
import kociemba
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
        self.cellborderwidth = 2
        self.cubeRows = 3
        self.cubeCols = 3
        
        self.colors = {
            'U': (255, 255, 255),
            'L': (255, 165, 0),
            'F': (0, 255, 0),
            'R': (255, 0, 0),
            'B': (0, 0, 255),
            'D': (255, 255, 0)
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
        self.U = [['U'] * 3 for row in range(3)]
        self.L = [['L'] * 3 for row in range(3)]
        self.F = [['F'] * 3 for row in range(3)]
        self.R = [['R'] * 3 for row in range(3)]
        self.B = [['B'] * 3 for row in range(3)]
        self.D = [['D'] * 3 for row in range(3)]
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
        draw.polygon([(74 + self.bx, 438 + self.by), (174 + self.bx, 438 + self.by), (170 + self.bx, 522 + self.by), (66 + self.bx, 522 + self.by)], fill = self.colors[self.D[0][0]])
        draw.polygon([(192 + self.bx, 438 + self.by), (294 + self.bx, 438 + self.by), (298 + self.bx, 522 + self.by), (188 + self.bx, 522 + self.by)], fill = self.colors[self.D[0][1]])
        draw.polygon([(310 + self.bx, 436 + self.by), (410 + self.bx, 436 + self.by), (414 + self.bx, 524 + self.by), (314 + self.bx, 524 + self.by)], fill = self.colors[self.D[0][2]])

        # Row 2
        draw.polygon([(84 + self.bx, 348 + self.by), (178 + self.bx, 348 + self.by), (174 + self.bx, 422 + self.by), (76 + self.bx, 422 + self.by)], fill = self.colors[self.D[1][0]])
        draw.polygon([(196 + self.bx, 348 + self.by), (288 + self.bx, 348 + self.by), (292 + self.bx, 424 + self.by), (192 + self.bx, 424 + self.by)], fill = self.colors[self.D[1][1]])
        draw.polygon([(306 + self.bx, 348 + self.by), (400 + self.bx, 348 + self.by), (404 + self.bx, 424 + self.by), (310 + self.bx, 424 + self.by)], fill = self.colors[self.D[1][2]])

        # Row 3
        draw.polygon([(94 + self.bx, 270 + self.by), (182 + self.bx, 270 + self.by), (178 + self.bx, 336 + self.by), (84 + self.bx, 336 + self.by)], fill = self.colors[self.D[2][0]])
        draw.polygon([(198 + self.bx, 270 + self.by), (286 + self.bx, 270 + self.by), (290 + self.bx, 336 + self.by), (194 + self.bx, 336 + self.by)], fill = self.colors[self.D[2][1]])
        draw.polygon([(302 + self.bx, 268 + self.by), (390 + self.bx, 268 + self.by), (398 + self.bx, 336 + self.by), (306 + self.bx, 336 + self.by)], fill = self.colors[self.D[2][2]])

    def drawBlueFace(self, draw):
        #draw the blue face (B)

        # Row 1
        draw.polygon([(414 + self.bx, 2 + self.by), (314 + self.bx, 2 + self.by), (310 + self.bx, 90 + self.by), (410 + self.bx, 90 + self.by)], fill = self.colors[self.B[0][0]])
        draw.polygon([(298 + self.bx, 4 + self.by), (188 + self.bx, 4 + self.by), (192 + self.bx, 88 + self.by), (292 + self.bx, 88 + self.by)], fill = self.colors[self.B[0][1]])
        draw.polygon([(170 + self.bx, 4 + self.by), (66 + self.bx, 4 + self.by), (74 + self.bx, 88 + self.by), (174 + self.bx, 88 + self.by)], fill = self.colors[self.B[0][2]])

        # Row 2
        draw.polygon([(404 + self.bx, 102 + self.by), (310 + self.bx, 102 + self.by), (306 + self.bx, 178 + self.by), (400 + self.bx, 178 + self.by)], fill = self.colors[self.B[1][0]])
        draw.polygon([(292 + self.bx, 102 + self.by), (192 + self.bx, 102 + self.by), (196 + self.bx, 178 + self.by), (288 + self.bx, 178 + self.by)], fill = self.colors[self.B[1][1]])
        draw.polygon([(174 + self.bx, 104 + self.by), (76 + self.bx, 104 + self.by), (84 + self.bx, 178 + self.by), (178 + self.bx, 178 + self.by)], fill = self.colors[self.B[1][2]])

        # Row 3
        draw.polygon([(398 + self.bx, 190 + self.by), (306 + self.bx, 190 + self.by), (302 + self.bx, 258 + self.by), (390 + self.bx, 258 + self.by)], fill = self.colors[self.B[2][0]])
        draw.polygon([(290 + self.bx, 190 + self.by), (194 + self.bx, 190 + self.by), (198 + self.bx, 256 + self.by), (286 + self.bx, 256 + self.by)], fill = self.colors[self.B[2][1]])
        draw.polygon([(178 + self.bx, 190 + self.by), (84 + self.bx, 190 + self.by), (94 + self.bx, 256 + self.by), (182 + self.bx, 256 + self.by)], fill = self.colors[self.B[2][2]])
    
    def drawOrangeFace(self, draw):
        # draw the orange face (L)
    
        # Row 1
        draw.polygon([(52 + self.bx, 158 + self.by), (38 + self.bx, 74 + self.by), (50 + self.bx, 12 + self.by), (62 + self.bx, 84 + self.by)], fill = self.colors[self.L[0][0]])
        draw.polygon([(20 + self.bx, 162 + self.by), (36 + self.bx, 86 + self.by), (48 + self.bx, 164 + self.by), (36 + self.bx, 246 + self.by)], fill = self.colors[self.L[0][1]])
        draw.polygon([(0 + self.bx, 264 + self.by), (18 + self.bx, 174 + self.by), (34 + self.bx, 264 + self.by), (18 + self.bx, 352 + self.by)], fill = self.colors[self.L[0][2]])
        # Row 2
        draw.polygon([(66 + self.bx, 100 + self.by), (56 + self.bx, 166 + self.by), (64 + self.bx, 240 + self.by), (74 + self.bx, 164 + self.by)], fill = self.colors[self.L[1][0]])
        draw.polygon([(52 + self.bx, 352 + self.by), (62 + self.bx, 264 + self.by), (52 + self.bx, 180 + self.by), (38 + self.bx, 264 + self.by)], fill = self.colors[self.L[1][1]])
        draw.polygon([(22 + self.bx, 364 + self.by), (36 + self.bx, 440 + self.by), (48 + self.bx, 366 + self.by), (36 + self.bx, 282 + self.by)], fill = self.colors[self.L[1][2]])
        # Row 3
        draw.polygon([(80 + self.bx, 354 + self.by), (66 + self.bx, 264 + self.by), (76 + self.bx, 180 + self.by), (86 + self.bx, 264 + self.by)], fill = self.colors[self.L[2][0]])
        draw.polygon([(56 + self.bx, 362 + self.by), (66 + self.bx, 438 + self.by), (74 + self.bx, 360 + self.by), (64 + self.bx, 292 + self.by)], fill = self.colors[self.L[2][1]])
        draw.polygon([(40 + self.bx, 454 + self.by), (52 + self.bx, 370 + self.by), (62 + self.bx, 442 + self.by), (52 + self.bx, 514 + self.by)], fill = self.colors[self.L[2][2]])

    def drawRedFace(self, draw):
        # draw the red face (R)
        
        # Row 1
        draw.polygon([(484 + self.bx, 264 + self.by), (466 + self.bx, 174 + self.by), (450 + self.bx, 264 + self.by), (466 + self.bx, 352 + self.by)], fill = self.colors[self.R[0][0]])
        draw.polygon([(464 + self.bx, 162 + self.by), (448 + self.bx, 86 + self.by), (436 + self.bx, 164 + self.by), (448 + self.bx, 246 + self.by)], fill = self.colors[self.R[0][1]])
        draw.polygon([(432 + self.bx, 158 + self.by), (446 + self.bx, 74 + self.by), (434 + self.bx, 12 + self.by), (422 + self.bx, 84 + self.by)], fill = self.colors[self.R[0][2]])
        # Row 2
        draw.polygon([(462 + self.bx, 364 + self.by), (448 + self.bx, 440 + self.by), (436 + self.bx, 366 + self.by), (446 + self.bx, 282 + self.by)], fill = self.colors[self.R[1][0]])
        draw.polygon([(432 + self.bx, 352 + self.by), (422 + self.bx, 264 + self.by), (432 + self.bx, 180 + self.by), (446 + self.bx, 264 + self.by)], fill = self.colors[self.R[1][1]])
        draw.polygon([(418 + self.bx, 100 + self.by), (428 + self.bx, 166 + self.by), (420 + self.bx, 240 + self.by), (410 + self.bx, 164 + self.by)], fill = self.colors[self.R[1][2]])
        # Row 3
        draw.polygon([(444 + self.bx, 454 + self.by), (432 + self.bx, 370 + self.by), (422 + self.bx, 442 + self.by), (432 + self.bx, 514 + self.by)], fill = self.colors[self.R[2][0]])
        draw.polygon([(428 + self.bx, 362 + self.by), (418 + self.bx, 438 + self.by), (410 + self.bx, 360 + self.by), (420 + self.bx, 292 + self.by)], fill = self.colors[self.R[2][1]])
        draw.polygon([(404 + self.bx, 354 + self.by), (418 + self.bx, 264 + self.by), (408 + self.bx, 180 + self.by), (398 + self.bx, 264 + self.by)], fill = self.colors[self.R[2][2]])

    def drawGreenFace(self, draw):
        # draw the green face (F)
        
        # Row 1
        draw.polygon([(10 + self.bx, 272 + self.by), (148 + self.bx, 272 + self.by), (156 + self.bx, 362 + self.by), (28 + self.bx, 362 + self.by)], fill = self.colors[self.F[0][0]])
        draw.polygon([(172 + self.bx, 272 + self.by), (312 + self.bx, 272 + self.by), (306 + self.bx, 362 + self.by), (178 + self.bx, 362 + self.by)], fill = self.colors[self.F[0][1]])
        draw.polygon([(336 + self.bx, 272 + self.by), (474 + self.bx, 272 + self.by), (456 + self.bx, 362 + self.by), (328 + self.bx, 362 + self.by)], fill = self.colors[self.F[0][2]])
        # Row 2
        draw.polygon([(32 + self.bx, 376 + self.by), (158 + self.bx, 376 + self.by), (164 + self.bx, 450 + self.by), (46 + self.bx, 450 + self.by)], fill = self.colors[self.F[1][0]])
        draw.polygon([(180 + self.bx, 376 + self.by), (304 + self.bx, 376 + self.by), (300 + self.bx, 450 + self.by), (184 + self.bx, 450 + self.by)], fill = self.colors[self.F[1][1]])
        draw.polygon([(328 + self.bx, 376 + self.by), (452 + self.bx, 376 + self.by), (438 + self.bx, 450 + self.by), (320 + self.bx, 450 + self.by)], fill = self.colors[self.F[1][2]])
        # Row 3
        draw.polygon([(48 + self.bx, 464 + self.by), (164 + self.bx, 464 + self.by), (170 + self.bx, 526 + self.by), (62 + self.bx, 526 + self.by)], fill = self.colors[self.F[2][0]])
        draw.polygon([(186 + self.bx, 464 + self.by), (298 + self.bx, 464 + self.by), (296 + self.bx, 526 + self.by), (188 + self.bx, 526 + self.by)], fill = self.colors[self.F[2][1]])
        draw.polygon([(320 + self.bx, 462 + self.by), (436 + self.bx, 462 + self.by), (422 + self.bx, 526 + self.by), (314 + self.bx, 526 + self.by)], fill = self.colors[self.F[2][2]])

    def drawWhiteFace(self, draw):
        # draw the white face (U)
        
        # Row 1
        draw.polygon([(60 + self.bx, 0 + self.by), (168 + self.bx, 0 + self.by), (164 + self.bx, 64 + self.by), (48 + self.bx, 64 + self.by)], fill = self.colors[self.U[0][0]])
        draw.polygon([(188 + self.bx, 0 + self.by), (296 + self.bx, 0 + self.by), (300 + self.bx, 64 + self.by), (184 + self.bx, 64 + self.by)], fill = self.colors[self.U[0][1]])
        draw.polygon([(316 + self.bx, 0 + self.by), (424 + self.bx, 0 + self.by), (436 + self.bx, 64 + self.by), (320 + self.bx, 64 + self.by)], fill = self.colors[self.U[0][2]])
        # Row 2
        draw.polygon([(44 + self.bx, 76 + self.by), (162 + self.bx, 76 + self.by), (156 + self.bx, 152 + self.by), (30 + self.bx, 152 + self.by)], fill = self.colors[self.U[1][0]])
        draw.polygon([(184 + self.bx, 76 + self.by), (300 + self.bx, 76 + self.by), (304 + self.bx, 150 + self.by), (180 + self.bx, 150 + self.by)], fill = self.colors[self.U[1][1]])
        draw.polygon([(322 + self.bx, 76 + self.by), (440 + self.bx, 76 + self.by), (452 + self.bx, 152 + self.by), (328 + self.bx, 152 + self.by)], fill = self.colors[self.U[1][2]])
        # Row 3
        draw.polygon([(28 + self.bx, 166 + self.by), (156 + self.bx, 166 + self.by), (148 + self.bx, 256 + self.by), (10 + self.bx, 256 + self.by)], fill = self.colors[self.U[2][0]])
        draw.polygon([(178 + self.bx, 166 + self.by), (306 + self.bx, 166 + self.by), (310 + self.bx, 254 + self.by), (174 + self.bx, 254 + self.by)], fill = self.colors[self.U[2][1]])
        draw.polygon([(328 + self.bx, 166 + self.by), (456 + self.bx, 166 + self.by), (474 + self.bx, 254 + self.by), (336 + self.bx, 254 + self.by)], fill = self.colors[self.U[2][2]])

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
        elif key == pygame.K_BACKSLASH:
            self.text1 += " Solution: " + self.goToSolver()
            self.resetCube
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

    # will get the current state as a readable form for kociemba
    def goToSolver(self):
        cube_string = self.getCubeAsString()
        solution = kociemba.solve(cube_string)
        return solution
    
    def getCubeAsString(self):
        # order of the way we should make this as a string is U R F D L B
        array = self.getFacesOrder()

        # do the necessary rotations to have the cube read properly
        rotations = ""
        rotations += self.rotateWhiteToTop(array) # will also add the rotation to the solution
        rotations += self.rotateGreenToFront(array) # will also add the rotation to the solution

        # Now build the cube state string
        result = ""
        result += self.getFaceAsReadable(self.U)
        result += self.getFaceAsReadable(self.R)
        result += self.getFaceAsReadable(self.F)
        result += self.getFaceAsReadable(self.D)
        result += self.getFaceAsReadable(self.L)
        result += self.getFaceAsReadable(self.B)
        return result
    
    def rotateWhiteToTop(self, array):
        result = "" # where we will store the rotation necessary to move white to the top
        # we have to check all locations and then depending on the index it is in, make the relevant move

        # already in the top
        if (array[0] == self.U):
            return result
        
        # on the right index, requires a z'
        if (array[1] == self.U):
            self.rotateCubeZprime()
            result += "z' "
            return result

        # in front, requires a x
        if (array[2] == self.U):
            self.rotateCubeX()
            result += "x "
            return result
        
        # on the bottom, requiest any "2" rotation, doing x2 here
        if (array[3] == self.U):
            # less lines to just make the move twice than actively loop through it and such
            self.rotateCubeX()
            self.rotateCubeX()
            result += "x2 "
            return result
        
        # on the left, requres a z
        if (array[4] == self.U):
            self.rotateCubeZ()
            result += "z "
            return result

        # on the back, requires a x'
        if (array[5] == self.U):
            self.rotateCubeXPrime()
            result += "x' "
            return result

        # Fallback if no condition matched
        return result

    def rotateGreenToFront(self, array):
        # we only have to check four things this time! 
        # we check, F (index 2), R (index 1), L (index 4), B (index 5)

        result = ""
        # on the front, we do nothing
        if (array[2] == self.F):
            return result
        
        # on the right, we need to do a y rotation
        if (array[1] == self.F):
            self.rotateCubeY()
            result += "y "
            return result
        
        # on the left, we need a y' rotation
        if (array[4] == self.F):
            self.rotateCubeYprime()
            result += "y' "
            return result
        
        # on the back, we need a y2 rotation
        if (array[5] == self.F):
            self.rotateCubeYprime()
            self.rotateCubeYprime()
            result += "y2 "
            return result

        # Fallback if no condition matched
        return result

    def getFacesOrder(self):
        '''basically check at index [1][1] if the thing is "U", that is our white face. 
        Then we add the red face as face 2, then green as 3, yellow as 4, orange as 5, blue as 6'''
        # we also need to rotate the cube to be in the proper order, that is what we are going to do here so that everything works properly
        # we are basically going to fetch the white face, orient that to the top, then orient the green face to the front
        result = []
        result.append(self.getFace('U'))
        result.append(self.getFace('R'))
        result.append(self.getFace('F'))
        result.append(self.getFace('D'))
        result.append(self.getFace('L'))
        result.append(self.getFace('B'))
        return result

    def getFace(self, face):
        # will get the white face    

        # u face
        if self.U[1][1] == face:
            return self.U
        
        # R face
        if self.R[1][1] == face:
            return self.R

        # F face
        if self.F[1][1] == face:
            return self.F

        # L face
        if self.L[1][1] == face:
            return self.L
        
        # B face
        if self.B[1][1] == face:
            return self.B
        
        # D face
        if self.D[1][1] == face:
            return self.D

    def getFaceAsReadable(self, face):
        result = ""
        for i in range(self.cubeRows):
            for j in range(self.cubeCols):
                result += face[i][j]
        return result
    
    def rotateCubeZ(self):
        self.moveS()
        self.moveF()
        self.moveBPrime()
        
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
        # Swap edge pieces between faces (each swap happens once per piece)
        self.B[0][0], self.R[0][0] , self.F[0][0] , self.L[0][0] = self.L[0][0], self.B[0][0], self.R[0][0] , self.F[0][0]
        self.B[0][1], self.R[0][1] , self.F[0][1] , self.L[0][1] = self.L[0][1], self.B[0][1], self.R[0][1] , self.F[0][1]
        self.B[0][2], self.R[0][2] , self.F[0][2] , self.L[0][2] = self.L[0][2], self.B[0][2], self.R[0][2] , self.F[0][2]
        
    def moveUPrime(self):
        for i in range(3):
            self.moveU()

    def moveR(self):
        #corner swap
        self.R[0][0], self.R[0][2], self.R[2][2], self.R[2][0] = self.R[2][0], self.R[0][0], self.R[0][2], self.R[2][2]
        #edge swap
        self.R[0][1], self.R[1][2], self.R[2][1], self.R[1][0] = self.R[1][0], self.R[0][1], self.R[1][2], self.R[2][1]
        # Swap edge pieces between faces (each swap happens once per piece)
        self.U[0][2], self.B[2][0] , self.D[0][2] , self.F[0][2] = self.F[0][2], self.U[0][2], self.B[2][0] , self.D[0][2]
        self.U[1][2], self.B[1][0] , self.D[1][2] , self.F[1][2] = self.F[1][2], self.U[1][2], self.B[1][0] , self.D[1][2]
        self.U[2][2], self.B[0][0] , self.D[2][2] , self.F[2][2] = self.F[2][2], self.U[2][2], self.B[0][0] , self.D[2][2]

    def moveRPrime(self):
        for i in range(3):
            self.moveR()

    def moveLPrime(self):
        #corner swap
        self.L[0][0], self.L[0][2], self.L[2][2], self.L[2][0] = self.L[0][2], self.L[2][2], self.L[2][0], self.L[0][0]
        #edge swap
        self.L[0][1], self.L[1][2], self.L[2][1], self.L[1][0] = self.L[1][2], self.L[2][1], self.L[1][0], self.L[0][1]
        # Swap edge pieces between faces (each swap happens once per piece)
        self.U[0][0], self.B[2][2] , self.D[0][0] , self.F[0][0] = self.F[0][0], self.U[0][0], self.B[2][2] , self.D[0][0]
        self.U[1][0], self.B[1][2] , self.D[1][0] , self.F[1][0] = self.F[1][0], self.U[1][0], self.B[1][2] , self.D[1][0]
        self.U[2][0], self.B[0][2] , self.D[2][0] , self.F[2][0] = self.F[2][0], self.U[2][0], self.B[0][2] , self.D[2][0]

    def moveL(self):
        for i in range(3):
            self.moveLPrime()

    def moveD(self):
        #corner swap
        self.D[0][0], self.D[0][2], self.D[2][2], self.D[2][0] = self.D[2][0], self.D[0][0], self.D[0][2], self.D[2][2]
        #edge swap
        self.D[0][1], self.D[1][2], self.D[2][1], self.D[1][0] = self.D[1][0], self.D[0][1], self.D[1][2], self.D[2][1]
        # Swap edge pieces between faces (each swap happens once per piece)
        self.F[2][0], self.R[2][0] , self.B[2][0] , self.L[2][0] = self.L[2][0], self.F[2][0], self.R[2][0] , self.B[2][0]
        self.F[2][1], self.R[2][1] , self.B[2][1] , self.L[2][1] = self.L[2][1], self.F[2][1], self.R[2][1] , self.B[2][1]
        self.F[2][2], self.R[2][2] , self.B[2][2] , self.L[2][2] = self.L[2][2], self.F[2][2], self.R[2][2] , self.B[2][2]

    def moveDPrime(self):
        for i in range(3):
            self.moveD()

    def moveB(self):
        #corner swap
        self.B[0][0], self.B[0][2], self.B[2][2], self.B[2][0] = self.B[2][0], self.B[0][0], self.B[0][2], self.B[2][2]
        #edge swap
        self.B[0][1], self.B[1][2], self.B[2][1], self.B[1][0] = self.B[1][0], self.B[0][1], self.B[1][2], self.B[2][1]
        # Swap edge pieces between faces (each swap happens once per piece)
        self.U[0][0], self.L[2][0] , self.D[2][2] , self.R[0][2] = self.R[0][2], self.U[0][0], self.L[2][0] , self.D[2][2]
        self.U[0][1], self.L[1][0] , self.D[2][1] , self.R[1][2] = self.R[1][2], self.U[0][1], self.L[1][0] , self.D[2][1]
        self.U[0][2], self.L[0][0] , self.D[2][0] , self.R[2][2] = self.R[2][2], self.U[0][2], self.L[0][0] , self.D[2][0]

    def moveBPrime(self):
        for i in range(3):
            self.moveB()

    def moveF(self):
        #corner swap
        self.F[0][0], self.F[0][2], self.F[2][2], self.F[2][0] = self.F[2][0], self.F[0][0], self.F[0][2], self.F[2][2]
        #edge swap
        self.F[0][1], self.F[1][2], self.F[2][1], self.F[1][0] = self.F[1][0], self.F[0][1], self.F[1][2], self.F[2][1]
        # Swap edge pieces between faces (each swap happens once per piece)
        self.U[2][0], self.R[0][0] , self.D[0][2] , self.L[2][2] = self.L[2][2], self.U[2][0], self.R[0][0] , self.D[0][2]
        self.U[2][1], self.R[1][0] , self.D[0][1] , self.L[1][2] = self.L[1][2], self.U[2][1], self.R[1][0] , self.D[0][1]
        self.U[2][2], self.R[2][0] , self.D[0][0] , self.L[0][2] = self.L[0][2], self.U[2][2], self.R[2][0] , self.D[0][0]
        
    def moveFPrime(self):
        for i in range(3):
            self.moveF()
            
    def moveMPrime(self):
        #all second column, rotate through the rows
        self.F[0][1], self.U[0][1], self.B[2][1], self.D[0][1] = self.D[0][1], self.F[0][1], self.U[0][1], self.B[2][1]
        self.F[1][1], self.U[1][1], self.B[1][1], self.D[1][1] = self.D[1][1], self.F[1][1], self.U[1][1], self.B[1][1]
        self.F[2][1], self.U[2][1], self.B[0][1], self.D[2][1] = self.D[2][1], self.F[2][1], self.U[2][1], self.B[0][1]

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
        self.F[1][0], self.R[1][0], self.B[1][0], self.L[1][0] =  self.R[1][0], self.B[1][0], self.L[1][0], self.F[1][0]
        self.F[1][1], self.R[1][1], self.B[1][1], self.L[1][1] =  self.R[1][1], self.B[1][1], self.L[1][1], self.F[1][1]
        self.F[1][2], self.R[1][2], self.B[1][2], self.L[1][2] =  self.R[1][2], self.B[1][2], self.L[1][2], self.F[1][2]

    def moveE(self):
        for i in range(3):
            self.moveEPrime()

    def moveSPrime(self):
        self.U[1][0], self.R[0][1], self.D[1][2], self.L[2][1] =  self.R[0][1], self.D[1][2], self.L[2][1], self.U[1][0]
        self.U[1][1], self.R[1][1], self.D[1][1], self.L[1][1] =  self.R[1][1], self.D[1][1], self.L[1][1], self.U[1][1]
        self.U[1][2], self.R[2][1], self.D[1][0], self.L[0][1] =  self.R[2][1], self.D[1][0], self.L[0][1], self.U[1][2]

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