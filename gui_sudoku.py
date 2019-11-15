import pygame
from sudoku_solve import isvalid,solve
import time

pygame.font.init()

class grid:
    problem = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    def __init__(self,rows,cols,width,height):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.cubes = [[cube(self.problem[r][c],r,c,width,height)for c in range(cols)]for r in range(rows)]
        self.selected = None
        self.model = None

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def is_done(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True
    
    def update_model(self):
        self.model = [[self.cubes[r][c].value for c in range(self.cols)]for r in range(self.rows)]
    
    def place_it(self,val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_value(val)
            self.update_model()

            if isvalid(self.model,val,(row,col)) and solve(self.model):
                return True
            else:
                self.cubes[row][col].set_value(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def click(self,pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return(int(y),int(x))
        else:
            return None

    def select(self,row,col):
        ### reset all selections
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False
        
        self.cubes[row][col].selected = True
        self.selected = (row,col)

    def rend(self,val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self,win):
        gap = self.width / 9
        for i in range(self.rows+1):
            if i%3 == 0 and i!=0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win,(0,0,0),(0,i*gap),(self.width,i*gap),thick)
            pygame.draw.line(win,(0,0,0),(i*gap,0),(i*gap,self.height),thick)
        ##cubes render
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

class cube:
    rows = 9
    cols = 9

    def __init__(self,value,row,col,width,height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
        self.temp = 0

    def set_temp(self,val):
        self.temp = val
    def set_value(self,val):
        self.value = val

    def draw(self,win):
        fnt = pygame.font.SysFont("comicsans",40)
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp!=0 and self.value == 0:
            tex = fnt.render(str(self.temp),1,(128,128,128))
            win.blit(tex,(x+5,y+5))
        elif not(self.value==0):
            tex = fnt.render(str(self.value),1,(0,0,0))
            win.blit(tex,(x + (gap/2 - tex.get_width()/2), y + (gap/2 - tex.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win,(255,0,0),(x,y,gap,gap),3)

def redraw_window(win, board, time, strikes):
    win.fill((255,255,255))
    ## render time
    fon = pygame.font.SysFont("comicsans",20)
    tex = fon.render("Elapsed time: "+form_time(time), 1, (0,0,0))
    win.blit(tex,((540-180),560))
    ## render strikes
    tex = fon.render("X "*strikes,1,(255,0,0))
    win.blit(tex,(20,560))
    board.draw(win)

def form_time(secs):
    sec = secs%60
    min = secs//60
    hr = min//60

    t = " "+str(min)+" : "+str(sec)
    return t

def main():
    window = pygame.display.set_mode((540,600))
    pygame.display.set_caption("sudoku game")

    board = grid(9,9,540,540)

    key = None

    run = True

    start = time.time()

    strikes = 0

    while run:
        elapsed_time = round(time.time()-start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i,j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place_it(board.cubes[i][j].temp):
                            print("done")
                        else:
                            print("failure")
                            strikes = strikes + 1
                        key = None
                        
                        if board.is_done():
                            print("Game Finished")
                            run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0],clicked[1])
                    key = None

        if board.selected and key != None:
            board.rend(key)
        
        redraw_window(window,board,elapsed_time,strikes)
        pygame.display.update()

main()
pygame.quit()