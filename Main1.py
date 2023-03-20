import time
import turtle
from abc import ABC, abstractmethod
import pygame
import concurrent.futures


pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)
pygame.init

game_end = False
screen = pygame.display.set_mode((480, 480))
pygame.display.set_caption('board')

def main(white_first:bool):
    
    board_make()
    print("board made")
    board_set()
    print("board set")
    piece_update()
    time.sleep(.1)
    while not(game_end):
        board_update()
        time.sleep(2)
        test= move_reader(white_first)
        board_update()
        print("move Made")
        if test:
            white_first = not(white_first)
def legal_check(move_input,color):
    return (columns[move_input%10][int(move_input/10)]).in_square.color != color       
class potential_moves:
    def __init__(self,moves:list,attacks:list) -> None:
        self.moves = moves
        self.attacks = attacks
class piece(ABC):         #defines basic movement for all pieces, NEED TO ADD COLLUSION DETECTION AND ATTACKING
        def __init__(self,space,color:bool, life:bool,allowed_moves:potential_moves):
            self.space = space
            self.color = color
            self.life = life  
            self.allowed_moves  =  potential_moves([],[])
        @abstractmethod
        def pos_update(self,X,Y):
            pass
        @abstractmethod
        def get_spot(self):
            pass
        def move_checker(self,move_to):
            pass
        def move_list (self)->potential_moves:
            pass   
class knight(piece): #cant move or attack
        def move(self,move_to):
            return(move_to - self.space)%11 ==0 or (move_to - self.space)%9 ==0
        def pos_update(self,X,Y):
            if self.color:
                screen.blit(pygame.image.load("Chess_nlt60.png"),(X,Y))
            else:
                screen.blit(pygame.image.load("Chess_ndt60.png"),(X,Y))
        def get_spot(self):
            return self.space
        def move_list(self) -> potential_moves:
            output = list()
            return output
class bishop(piece): #cant move or attack          
        def pos_update(self,X,Y):
            if self.color:
                screen.blit(pygame.image.load("Chess_blt60.png"),(X,Y))
            else:
                screen.blit(pygame.image.load("Chess_bdt60.png"),(X,Y))
        def get_spot(self):
            return self.space
        def move_list(self) -> potential_moves:
            output = []
            attack = []
            #going up and right
            collision_check =  False
            x=1
            while not(collision_check):
                print(self.space)
                space_mod = self.space + x*11
                hibitch = input(columns[(int)(space_mod/10)][space_mod%10].in_square == empty)
                if space_mod >77 or space_mod<0: 
                    break 
                if columns[(int)(space_mod/10)][space_mod%10].in_square == empty:
                    output.append(space_mod)
                else: 
                    if columns[(int)(space_mod/10)][space_mod%10].in_square.color == self.color:
                        collision_check =True
                    else:
                        attack.append(space_mod)
                        collision_check = True
                x=x+1
                
            #going up and left
            collision_check =  False
            x=1
            while not(collision_check):
                space_mod = self.space + x* 9
                print("wat" + space_mod)
                if space_mod >77 or space_mod<0:
                    break
                if columns[(int)(space_mod/10)][space_mod%10].in_square == empty:
                    output.append(space_mod) 
                else: 
                    if columns[(int)(space_mod/10)][space_mod%10].in_square.color == self.color:
                        collision_check =True
                    else:
                        attack.append(space_mod)
                        collision_check = True
                x=x+1
                
            #going down and right
            collision_check =  False
            x=1
            while not(collision_check):
                space_mod = self.space -x*11
                if space_mod >77 or space_mod<0: 
                    break
                if columns[(int)(space_mod/10)][space_mod%10].in_square == empty:
                    output.append(space_mod)
                else: 
                    if columns[(int)(space_mod/10)][space_mod%10].in_square.color == self.color:
                        collision_check =True
                    else:
                        attack.append(space_mod)
                        collision_check = True
                x=x+1
                
            #going down and left
            collision_check =  False
            x=1
            while not(collision_check):
                space_mod = self.space - x*9
                if space_mod >77 or space_mod<0: 
                    break
                if columns[(int)(space_mod/10)][space_mod%10].in_square == empty:
                    output.append(space_mod)
                else: 
                    if columns[(int)(space_mod/10)][space_mod%10].in_square.color == self.color:
                        collision_check =True
                    else:
                        attack.append(space_mod)
                        collision_check = True
                x=x+1
            self.allowed_moves.moves = output
            self.allowed_moves.attacks = attack
            return output      
class rook(piece):#cant move or attack
        # def __init__(self,space,color, life):
        #     self.space = space
        #     self.color = color
        #     self.life = life
        def move(self,move_to):
            return(move_to%10 == self.space%10) or int(move_to/10) == int(self.space/10)
        def pos_update(self,X,Y):
            if self.color:
                screen.blit(pygame.image.load("Chess_rlt60.png"),(X,Y))
            else:
                screen.blit(pygame.image.load("Chess_rdt60.png"),(X,Y))
        def get_spot(self):
            return self.space
        def move_list(self) -> potential_moves:
            output = list()
            return output
class queen(piece):#cant move or attack
      
        def move(self,move_to):
            return((self.space%10-(int(self.space/10)))==((move_to%10-(int(move_to/10))))) or ((self.space%10+(int(self.space/10)))==((move_to%10+(int(move_to/10))))) or (move_to%10 == self.space%10) or int(move_to/10) == int(self.space/10)
        def pos_update(self,X,Y):
            if self.color:
                screen.blit(pygame.image.load("Chess_qlt60.png"),(X,Y))
            else:
                screen.blit(pygame.image.load("Chess_qdt60.png"),(X,Y))
        def get_spot(self):
            return self.space
        def move_list(self) -> potential_moves:
            output = list()
            return output
class king(piece):#cant move or attack
       
        def move(self,move_to):
            return abs(move_to-self.space) == 11 or abs(move_to-self.space) == 10 or abs(move_to-self.space) == 9 or abs(move_to-self.space) == 1
        def pos_update(self,X,Y):
            if self.color:
                screen.blit(pygame.image.load("Chess_klt60.png"),(X,Y))
            else:
                screen.blit(pygame.image.load("Chess_kdt60.png"),(X,Y))
        def get_spot(self):
            return self.space
        def move_list(self) -> potential_moves:
            output = list()
            return output
class pawn(piece): #cant attack
    def pos_update(self,X,Y):
        if self.color:
            screen.blit(pygame.image.load("Chess_plt60.png"),(X,Y))
        else:
            screen.blit(pygame.image.load("Chess_pdt60.png"),(X,Y))
    def get_spot(self):
        return self.space
    def move_list(self) -> potential_moves:
        output = []
        attack =[]
        moved:bool = self.color and (self.space%10) == 1 or not(self.color) and (self.space%10)==6
        if self.color:
            if columns[(int(self.space/10))][(self.space%10)+1].in_square == empty: output.append(self.space+1)
            if columns[(int(self.space/10))-1][(self.space%10)+1].in_square != empty and columns[(int(self.space/10))-1][(self.space%10)-1].in_space_color != self.color: attack.append(self.space+9)
            if columns[(int(self.space/10))+1][(self.space%10)+1].in_square != empty and columns[(int(self.space/10))+1][(self.space%10)+1].in_space_color != self.color: attack.append(self.space+11)
            if moved:
                if columns[(int(self.space/10))][(self.space%10)+2].in_square == empty: output.append(self.space+2)
        else:
            if columns[(int(self.space/10))][(self.space%10)-1].in_square == empty: output.append(self.space-1)
            if columns[(int(self.space/10))-1][(self.space%10)-1].in_square != empty and columns[(int(self.space/10))-1][(self.space%10)-1].in_space_color != self.color: attack.append(self.space-9)
            if columns[(int(self.space/10))+1][(self.space%10)-1].in_square != empty and columns[(int(self.space/10))+1][(self.space%10)-1].in_space_color != self.color: attack.append(self.space-11)
            if moved:
                if columns[(int(self.space/10))][(self.space%10)-2].in_square == empty: output.append(self.space-2)
        self.allowed_moves.attacks = attack
        self.allowed_moves.moves = output
        return self.allowed_moves   
class NA(piece):
    def move(self,move_to):
        return
    def pos_update(self,X,Y):
        return
    def get_spot(self):
            print("nah fam")
    def move_list(self) -> potential_moves:
        output = list()
        return output
class space:
    def __init__(self, in_square:piece ,color):
        self.in_square = in_square
        self.color = color #False =  dark True = light 
empty = NA(00,False,False,potential_moves([],[]))
blank = space(empty,False)
column1 = [blank,blank,blank,blank,blank,blank,blank,blank]
column2 = [blank,blank,blank,blank,blank,blank,blank,blank]
column3 = [blank,blank,blank,blank,blank,blank,blank,blank]
column4 = [blank,blank,blank,blank,blank,blank,blank,blank]
column5 = [blank,blank,blank,blank,blank,blank,blank,blank]
column6 = [blank,blank,blank,blank,blank,blank,blank,blank]
column7 = [blank,blank,blank,blank,blank,blank,blank,blank]
column8 = [blank,blank,blank,blank,blank,blank,blank,blank]
columns = [column1,column2,column3,column4,column5,column6,column7,column8] # mod will get sec digit int div will get first
def board_make():
    print("making")
    color_count = 1
    for y in range (8):
        for x in range (8):
            if color_count%2 == 0:
                pygame.draw.rect(screen, "brown", (x*60, y*60 , 60, 60))
            else:
                pygame.draw.rect(screen, "white", (x*60, y*60 , 60, 60))
            color_count = color_count+1
        color_count = color_count+1
    print("done making")
    return   
def board_set():
    color_count = 0
    for i in range (8): #create empty board
        for k in range (8):
            dspace = space(empty,False)
            lspace = space(empty,True)
            if color_count%2 ==0:
                columns[i][k] = dspace
            else:
                columns[i][k] = lspace
            color_count = color_count+1
        color_count = color_count+1
            
    for i in range (8): #places pawns
        columns[i][1].in_square = pawn(((10*i)+1),True,True,potential_moves([],[]))
        columns[i][6].in_square = pawn(((10*i)+6),False,True,potential_moves([],[]))
    
    #placing bishops
    columns[2][0].in_square = bishop(20,True,True,potential_moves([],[]))
    columns[5][0].in_square = bishop(50,True,True,potential_moves([],[]))
    columns[2][7].in_square = bishop(27,False,True,potential_moves([],[]))
    columns[5][7].in_square = bishop(57,False,True,potential_moves([],[]))
    
    #placing rooks
    columns[0][0].in_square = rook(00,True,True,potential_moves([],[]))
    columns[0][7].in_square = rook(7,False,True,potential_moves([],[]))
    columns[7][0].in_square = rook(70,True,True,potential_moves([],[]))
    columns[7][7].in_square = rook(77,False,True,potential_moves([],[]))
    
    #placing knights
    columns[1][0].in_square = knight(10,True,True,potential_moves([],[]))
    columns[6][0].in_square = knight(60,True,True,potential_moves([],[]))
    columns[1][7].in_square = knight(17,False,True,potential_moves([],[]))
    columns[6][7].in_square = knight(67,False,True,potential_moves([],[]))

    #placing kings and queens
    columns[3][0].in_square = queen(30,True,True,potential_moves([],[]))
    columns[3][7].in_square = queen(37,False,True,potential_moves([],[]))
    columns[4][0].in_square = king(40,True,True,potential_moves([],[]))
    columns[4][7].in_square = king(47,False,True,potential_moves([],[]))

    return  
def piece_update():       
    
    for i in range (8):
        for k in range (8):
            columns[i][k].in_square.pos_update(i*60,420-k*60)
    pygame.display.update()
    pygame.display.flip()
    return    
def move_lister(spot:space):
    
    for x in range (8):
        for y in range (8):
            if spot.in_square.move((y*10)+x):
                screen.blit(pygame.image.load("good move marker.png"),(x*60,420-y*60))
                pygame.display.update()
                
    pygame.display.flip()
def board_update():
    print("UPDATE?")
    screen.fill((0,0,0))
    pygame.display.flip()
    pygame.display.update()    
    color_count = 1
    for y in range (8):
        for x in range (8):
            if color_count%2 == 0:
                pygame.draw.rect(screen, "brown", (x*60, y*60 , 60, 60))
            else:
                pygame.draw.rect(screen, "white", (x*60, y*60 , 60, 60))
            color_count = color_count+1
        color_count = color_count+1
    piece_update()
    print("done making")
    pygame.display.flip()
    pygame.display.update()
    return      
def move_reader(white_check:bool): #fix for new coodinate system
    action = pool.submit(input("What do you want to do? "))
    print(action)
    pool.shutdown(wait=True)
    if action == "move":
        piece_input = pool.submit(input("What piece"))
        move_input= pool.submit(input("where to? "))
        pool.shutdown(wait=True)
        current_spot = (columns[int(piece_input[0:1])][int(piece_input[1:2])])
        future_spot = (columns[int(move_input[0:1])][int(move_input[1:2])])
        
        current_piece = current_spot.in_square
        good_moves =  current_piece.move_list().moves
        good_attacks = current_piece.move_list().attacks
        output= False
        attack_check = False
        print(piece_input)
        print(good_moves)
        print(good_attacks)
        print(move_input)
        for x in range (len(good_moves)):
            if good_moves[x] == int(move_input):
                output= True
        for x in range (len(good_attacks)):
            if good_attacks[x] == int(move_input):
                output= True
                attack_check = True
        if attack_check:
            confirm_attack = pool.submit(input("This will attack a peice, Press 'Y' if you want to commit"))
            if confirm_attack != "Y":
                output = False
        if output:
            current_piece.space = move_input
            future_spot.in_square = current_piece
            current_spot.in_square = empty
            return True
        else:
            print("NAH BRO")
            return False
    if action == "list":
        piece_input = pool.submit(input("What piece"))
        pool.shutdown(wait=True)
        current_spot = (columns[int(piece_input[0:1])][int(piece_input[1:2])])
        print(current_spot.in_square.move_list())
            

