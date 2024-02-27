import random
import pygame
import time
actions = ["rock", "paper", "scissors"]
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("music.mp3")
RESCOL=(255,255,255)
WIDTH, HEIGHT = 1000, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ROCK PAPER SCISSORS")
BG = pygame.image.load("bg3.png")
font = pygame.font.SysFont("Red", 30)
resfont= pygame.font.SysFont("Red", 60)
TEXTCOL = (255, 255,255)
BCOLOR = (140, 180, 210)
BWIDTH, BHEIGHT = 150, 50
BDISTANCE = 100
rock = pygame.transform.scale(pygame.image.load("r1.png"), (50, 50))
paper = pygame.transform.scale(pygame.image.load("b1.png"), (50, 50))
scissors = pygame.transform.scale(pygame.image.load("s1.png"), (50, 50))
state = "menu"
playerscore = 0
aiscore = 0
mode = 1
MODEPOS = (WIDTH // 2 - BWIDTH // 2, HEIGHT // 4 + 4 * BHEIGHT // 2 + 25)
SETTINGSPOS = (WIDTH // 2 - BWIDTH // 2, HEIGHT // 4 + 1.75 * BDISTANCE + BHEIGHT // 2)
LEADERBOARDPOS = (WIDTH // 2 - BWIDTH // 2, HEIGHT // 4 + 2.75 * BDISTANCE + BHEIGHT // 2 - 25)
PLAYPOS = (WIDTH // 2 - BWIDTH // 2, HEIGHT // 4 + 2 * BHEIGHT // 2)
QUITPOS = (WIDTH // 2 - BWIDTH // 2, HEIGHT // 4 + 4 * BDISTANCE + BHEIGHT // 2 - 75)
ROCKPOS = (WIDTH // 2 - BWIDTH - 150, HEIGHT // 2)
PAPERPOS = (WIDTH // 2 - BWIDTH // 2, HEIGHT // 2)
SCISSORSPOS = (WIDTH // 2 + 150, HEIGHT // 2)

level1completed = False
level2completed = False

class Bot:
    def __init__(self, level):
        self.level = level

    def choose_action(self):
        return random.choice(actions)

def playmusic(playing):
    global music_playing
    if playing:
        pygame.mixer.music.play(-1)
        music_playing = True
    else:
        pygame.mixer.music.stop()
        music_playing = False

def stopmusic():
    pygame.mixer.music.stop()

def animate(bot1, bot2=None):
    global achoice1, achoice2
    achoiceframes = 60
    for frame in range(achoiceframes):
        achoice1 = bot1.choose_action()
        if bot2:
            achoice2 = bot2.choose_action()
        draw()
        pygame.display.update()
        pygame.time.delay(25)

def ttext(text, font, color, x, y):
    img = font.render(text, True, color)
    WIN.blit(img, (x, y))

def button(color, pos, text):
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(pos[0], pos[1], BWIDTH, BHEIGHT)
    border_radius = 10
    if button_rect.collidepoint(mouse_pos):
        new_color = tuple(max(0, c - 50) for c in color)
        pygame.draw.rect(WIN, new_color, button_rect, border_radius=border_radius)
    else:
        pygame.draw.rect(WIN, color, button_rect, border_radius=border_radius)
    text_width, text_height = font.size(text)
    text_x = pos[0] + (BWIDTH - text_width) // 2
    text_y = pos[1] + (BHEIGHT - text_height) // 2
    ttext(text, font, TEXTCOL, text_x, text_y)

def click(pos, buttonpos):
    return (
            buttonpos[0] <= pos[0] <= buttonpos[0] + BWIDTH and
            buttonpos[1] <= pos[1] <= buttonpos[1] + BHEIGHT
    )

def scores():
    if WIDTH == 1000:
        ttext(f"Player: {playerscore}   AI: {aiscore}", font, TEXTCOL, WIDTH // 2 - 100, 10)
    else:
        ttext(f"Player: {playerscore}   AI: {aiscore}", font, TEXTCOL, WIDTH // 2 - 100, 50)


def dresult(result):
    ttext(result, resfont, RESCOL, WIDTH // 2 - 50, HEIGHT // 2 - 150)
    pygame.display.update()
    time.sleep(0.5)

def choices(pchoice, achoice1, achoice2=None):
    if WIDTH==1000:
        ttext("Player choice:", font, TEXTCOL, WIDTH // 4 - 120, HEIGHT // 2 - 150)
        ttext("AI choice:", font, TEXTCOL, 3 * WIDTH // 4 - 100, HEIGHT // 2 - 150)
    else:
        ttext("Player choice:", font, TEXTCOL, WIDTH // 4 - 120, HEIGHT // 2 - 200)
        ttext("AI choice:", font, TEXTCOL, 3 * WIDTH // 4 - 100, HEIGHT // 2 - 200)
    if pchoice:
        if pchoice == "rock":
            WIN.blit(rock, (WIDTH // 4 + 25, HEIGHT // 2 - 125))
        elif pchoice == "paper":
            WIN.blit(paper, (WIDTH // 4 + 25, HEIGHT // 2 - 125))
        elif pchoice == "scissors":
            WIN.blit(scissors, (WIDTH // 4 + 25, HEIGHT // 2 - 125))
    if achoice1:
        if achoice1 == "rock":
            WIN.blit(rock, (3 * WIDTH // 4, HEIGHT // 2 - 125))
        elif achoice1 == "paper":
            WIN.blit(paper, (3 * WIDTH // 4, HEIGHT // 2 - 125))
        elif achoice1 == "scissors":
            WIN.blit(scissors, (3 * WIDTH // 4, HEIGHT // 2 - 125))
    if achoice2:
        if achoice2 == "rock":
            WIN.blit(rock, (3 * WIDTH // 4 , HEIGHT // 2 - 200))
        elif achoice2 == "paper":
            WIN.blit(paper, (3 * WIDTH // 4 , HEIGHT // 2 - 200))
        elif achoice2 == "scissors":
            WIN.blit(scissors, (3 * WIDTH // 4 , HEIGHT // 2 - 200))

def modebutton(mouse_pos=None):
    global mode, level1completed, level2completed, mode_text, state
    if mouse_pos:
        if MODEPOS[0] <= mouse_pos[0] <= MODEPOS[0] + BWIDTH and \
           MODEPOS[1] <= mouse_pos[1] <= MODEPOS[1] + BHEIGHT:
            if level1completed and level2completed:
                if mode == 3:
                    mode = 1
                    mode_text= "Mode: 1 level"
                elif mode == 1:
                    mode = 2
                    mode_text= "Mode: 2 level"
                elif mode == 2:
                    mode = 3
                    mode_text="Mode: Endless"
            elif level1completed:
                if mode == 1:
                    mode = 2
                    mode_text = "Mode: 2 level"
                else:
                    mode = 1
                    mode_text = "Mode: 1 level"
            elif level2completed:
                mode = 3
            else:
                mode = 1
    if mode == 1:
        mode_text = "Mode: 1 level"
    elif mode == 2:
        mode_text = "Mode: 2 level"
    elif mode == 3:
        mode_text = "Endless"
    button(BCOLOR, MODEPOS, mode_text)

def modeclick():
    global mode, level1completed, level2completed, mode_text, state
    if level1completed and level2completed:
        if mode == 3:
            mode = 1
        elif mode == 1:
            mode = 2
        elif mode == 2:
            mode = 3
    elif level1completed:
         if mode==2:
             mode=1
         elif mode==1:
             mode=2
    elif level2completed:
        mode = 3
    else:
        mode = 1
    if mode == 1:
        mode_text = "Mode: 1 level"
    elif mode == 2:
        mode_text = "Mode: 2 level"
    elif mode == 3:
        mode_text = "Endless"
    button(BCOLOR, MODEPOS, mode_text)

def drawsettingsb():
    button(BCOLOR, SETTINGSPOS, "Settings")


def drawleaderboard():
    button(BCOLOR, LEADERBOARDPOS, "Leaderboard")


def drawplay():
    button(BCOLOR, PLAYPOS, "Play")


def drawquit():
    button(BCOLOR, QUITPOS, "Quit")


def drawback():
    button(BCOLOR, (20, 20), "Back")

def draw():
    WIN.blit(BG, (0, 0))
    if state == "menu":
        scores()
        drawplay()
        drawsettingsb()
        drawleaderboard()
        drawquit()
        modebutton()
    elif state == "play":
        scores()
        button((140, 180, 210), ROCKPOS, "Rock")
        button((140, 180, 210), PAPERPOS, "Paper")
        button((140, 180, 210), SCISSORSPOS, "Scissors")
        choices(pchoice, achoice1, achoice2)
        drawback()

def settingsclick():
    global WIDTH, HEIGHT, BG, ROCKPOS, PAPERPOS, SCISSORSPOS, MODEPOS, SETTINGSPOS, LEADERBOARDPOS, WIN, PLAYPOS, QUITPOS, level1completed, level2completed, mode
    if WIDTH == 1000:
        WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        WIDTH, HEIGHT = pygame.display.get_surface().get_size()
        QUITPOS = (WIDTH // 2 - BWIDTH // 2, HEIGHT // 2 + 200)
        PLAYPOS = (WIDTH // 2 - BWIDTH // 2, HEIGHT // 2 - 100)
        ROCKPOS = (WIDTH // 2 - BWIDTH - 150, HEIGHT // 2)
        PAPERPOS = (WIDTH // 2 - BWIDTH // 2, HEIGHT // 2)
        SCISSORSPOS = (WIDTH // 2 + 150, HEIGHT // 2)
        MODEPOS = ((WIDTH - BWIDTH) // 2, HEIGHT // 2 - 25)
        SETTINGSPOS = ((WIDTH - BWIDTH) // 2, HEIGHT // 2 + 50)
        LEADERBOARDPOS = ((WIDTH - BWIDTH) // 2, HEIGHT // 2 + 125)
    else:
        WIDTH, HEIGHT = 1000, 600
        WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        MODEPOS = (WIDTH // 2 - BWIDTH // 2, HEIGHT // 4 + 4 * BHEIGHT // 2 + 25)
        SETTINGSPOS = (
            WIDTH // 2 - BWIDTH // 2, HEIGHT // 4 + 1.75 * BDISTANCE + BHEIGHT // 2)
        LEADERBOARDPOS = (
            WIDTH // 2 - BWIDTH // 2, HEIGHT // 4 + 2.75 * BDISTANCE + BHEIGHT // 2 - 25)
        PLAYPOS = (WIDTH // 2 - BWIDTH // 2, HEIGHT // 4 + 2 * BHEIGHT // 2)
        QUITPOS = (
            WIDTH // 2 - BWIDTH // 2, HEIGHT // 4 + 4 * BDISTANCE + BHEIGHT // 2 - 75)
        ROCKPOS = (WIDTH // 2 - BWIDTH - 150, HEIGHT // 2)
        PAPERPOS = (WIDTH // 2 - BWIDTH // 2, HEIGHT // 2)
        SCISSORSPOS = (WIDTH // 2 + 150, HEIGHT // 2)
        LEADERBOARDPOS = ((WIDTH - BWIDTH) // 2, HEIGHT // 2 + 125)
    BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))
    pygame.display.update()


class Leaderboard:
    def __init__(self):
        self.scores = []
        self.background = pygame.image.load("bg3.png")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

    def update(self, playerscore, aiscore):
        self.scores.append((playerscore, aiscore))

    def display(self):
        sorted_scores = sorted(self.scores, key=lambda x: (x[0], x[1]), reverse=True)
        if WIDTH == 1000:
            win = pygame.display.set_mode((WIDTH, HEIGHT))
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
            win.blit(self.background, (0, 0))
        else:
            win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
            win.blit(self.background, (0, 0))
        ttext("Leaderboard", font, TEXTCOL, WIDTH // 2 - 75, 20)
        y = 50
        i = 1
        for player, ai in sorted_scores:
            text = f"{i}. Player {player} - AI {ai}"
            ttext(text, font, TEXTCOL, WIDTH // 2 - 100, y)
            y += 40
            i += 1
        pygame.display.update()



leaderboard = Leaderboard()


def displayleaderboard():
    leaderboard.display()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            elif event.type == pygame.QUIT:
                pygame.quit()
                return

def backclick():
    global playerscore, aiscore
    playerscore = 0
    aiscore = 0

def game1result(pchoice, achoice1):
    if pchoice == achoice1:
        return "Tie!"
    elif (pchoice == "rock" and achoice1 == "scissors") or \
            (pchoice == "paper" and achoice1 == "rock") or \
            (pchoice == "scissors" and achoice1 == "paper"):
        return "Win!"
    else:
        return "Lose!"

def gameresult(pchoice, achoice1, achoice2):
    if pchoice == achoice1 and pchoice == achoice2:
        return "Tie!"
    elif (pchoice == "rock" and achoice1 == "scissors" and achoice2 == "scissors") or \
            (pchoice == "paper" and achoice1 == "rock" and achoice2 == "rock") or \
            (pchoice == "scissors" and achoice1 == "paper" and achoice2 == "paper"):
        return "You Win!"
    elif (pchoice == "rock" and achoice1 == "paper" and achoice2 == "paper") or \
            (pchoice == "paper" and achoice1 == "scissors" and achoice2 == "scissors") or \
            (pchoice == "scissors" and achoice1 == "rock" and achoice2 == "rock"):
        return "You Lose!"
    else:
        return "Tie!"

def main():
    global state, playerscore, aiscore, pchoice, achoice, result, mode, lчeaderboard, achoice1, achoice2, level1completed, level2completed
    run = True
    music_playing = True
    state = "menu"
    while run:
        result = ""
        pchoice = ""
        achoice = ""
        achoice1 = ""
        achoice2 = ""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    music_playing = not music_playing
                    if music_playing:
                        playmusic(True)
                    else:
                        stopmusic()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if state == "instructions":
                    handle_instructions_click(event)
                elif state == "menu":
                    if click(mouse_pos, PLAYPOS):
                        state = "play"
                        playerscore = 0
                        aiscore = 0
                    elif click(mouse_pos, MODEPOS):
                        modeclick()
                    elif click(mouse_pos, SETTINGSPOS):
                        settingsclick()
                    elif click(mouse_pos, LEADERBOARDPOS):
                        displayleaderboard()
                    elif click(mouse_pos, QUITPOS):
                        run = False
                elif state == "play":
                    if click(mouse_pos, ROCKPOS):
                        pchoice = "rock"
                    elif click(mouse_pos, PAPERPOS):
                        pchoice = "paper"
                    elif click(mouse_pos, SCISSORSPOS):
                        pchoice = "scissors"
                    elif click(mouse_pos, (20, 20)):
                        state = "menu"
                        backclick()
                    else:
                        continue
                    if pchoice:
                        if mode == 1:
                            bot = Bot(1)
                            draw()
                            animate(bot)
                            achoice = bot.choose_action()
                            achoice1 = achoice
                            result = game1result(pchoice, achoice1)
                        elif mode == 2:
                            bot1 = Bot(2)
                            bot2 = Bot(2)
                            draw()
                            choices(pchoice, bot1.choose_action(), bot2.choose_action())
                            animate(bot1, bot2)
                            achoice1, achoice2 = bot1.choose_action(), bot2.choose_action()
                            result = gameresult(pchoice, achoice1, achoice2)
                        elif mode == 3:
                            bot = Bot(1)
                            draw()
                            animate(bot)
                            achoice = bot.choose_action()
                            achoice1 = achoice
                            result = game1result(pchoice, achoice1)
                        if "Win" in result:
                            playerscore += 1
                            leaderboard.update(playerscore, aiscore)
                        elif "Lose" in result:
                            aiscore += 1
                            leaderboard.update(playerscore, aiscore)
                        if mode == 1 and playerscore >= 3:
                            result = "PLAYER WINS!"
                            level1completed = True
                            state = "menu"
                            backclick()
                            modebutton()
                        elif mode == 2 and playerscore >= 6:
                            result = "PLAYER WINS!"
                            state = "menu"
                            level2completed = True
                            mode = 3
                            backclick()
                            modebutton()
                        elif mode == 2 and aiscore >= 6:
                            result = "AI WINS!"
                            state = "menu"
                            level2completed = False
                            backclick()
                        elif mode == 1 and aiscore >= 3:
                            result = "AI WINS!"
                            level1completed = False
                            state = "menu"
                            backclick()
                        elif mode == 3 and playerscore >= 100:
                            result = "PLAYER WINS!"
                            state = "menu"
                            backclick()
        draw()
        dresult(result)
        pygame.display.update()
    stopmusic()
    pygame.quit()
if __name__ == "__main__":
    main()
