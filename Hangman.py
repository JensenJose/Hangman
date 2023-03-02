import pygame
import math
import random
from words import word_list

#Initializes the pygame module
pygame.init()
WIDTH, HEIGHT = 800, 500
#Creates the game window with the given dimensions 
win = pygame.display.set_mode((WIDTH, HEIGHT))
#Sets the title for the game
pygame.display.set_caption("Hangman")

#BUTTON VARIABLES
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400
A = 65
for i in range(26):
    x = startx + GAP * 2 + (RADIUS * 2 + GAP) * (i % 13)
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

#FONTS
LETTER_FONT = pygame.font.SysFont('comicscan', 40)
WORD_FONT = pygame.font.SysFont('comicscan', 60)

#LOAD IMAGES
images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)

#GAME VARIABLES
hangman_status = 0
word = random.choice(word_list).upper()
guessed = []

#COLORS
WHITE = (255,255,255)
BLACK = (0, 0, 0)

#FUNCTION FOR DRAWING
def draw():
    win.fill(WHITE)
    #DRAW WORD
    display_word = ''
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 200))
        
    #Draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x-text.get_width()/2, y-text.get_height()/2))
    #Displayes the image on the given position
    win.blit(images[hangman_status], (150, 100)) 
    #Updates the display after setting the bg color to white for each frame
    pygame.display.update() 
    
#SETUP GAME LOOP
FPS = 60
#Creates a clock for mesuring the FPS
clock = pygame.time.Clock() 
run = True

def display_message(message):
    pygame.time.delay(1000)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

while run:
    #Ensures that the game runs only at the given FPS
    clock.tick(FPS) 
    draw()
    #A for looop is used to check each event present in the game and take an action accordingly
    for event in pygame.event.get():
        #In this if block it first check of the close button is clicked and closes the window if true
        if event.type == pygame.QUIT:
            run = False
        #This if block returns the position of the screen where the mouse was clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()
            for letter in letters:
                x, y, ltr, visible = letter
                if visible:    
                    dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                    if dis < RADIUS:
                        letter[3] = False
                        guessed.append(ltr)
                        if ltr not in word:
                            hangman_status += 1
    
    won = True
    for letter in word:
        if letter not in guessed:
            won  = False
            break
    if won:
        display_message("YOU WON!")
        break
    
    if hangman_status == 6:
        display_message("YOU LOST!")
        break
    
pygame.quit()