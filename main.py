import decimal
import random

import pygame

import Menu
import Spritesheet

pygame.init()

# SCREEN SETUP
screen_width = 1100
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))

purple = (30, 30, 65)
grey = (40, 40, 40)
black = (0, 0, 0)
white = (255, 255, 255)
brown = (60, 50, 50)
red = (150, 48, 53)
exit_cell_col = (130, 28, 33)

# FONTS
Font_size = 46
Title_Font_size = 146
Font = pygame.font.SysFont('arial.ttf', Font_size)
Title_Font = pygame.font.SysFont('arial.ttf', Title_Font_size)

# IMAGE SETUP
player_spritesheet = pygame.image.load('character_spritesheet.png')
player_sprite_sheet = Spritesheet.SpriteSheet(player_spritesheet)

enemy_spritesheet = pygame.image.load('enemy_spritesheet.png')
enemy_sprite_sheet = Spritesheet.SpriteSheet(enemy_spritesheet)

Bomb_png = pygame.image.load('Bomb.png')
Bomb_Sprite = Spritesheet.SpriteSheet(Bomb_png)

Bombblast_png = pygame.image.load('Bomb_Blast.png')
Blast_sprite = Spritesheet.SpriteSheet(Bombblast_png)

# MAZE SETUP
Tile_Size = 100
columns = (screen_width // Tile_Size) - (200 // Tile_Size)
rows = (screen_height // Tile_Size) - (100 // Tile_Size)
cell_grid = []

clock = pygame.time.Clock()

Next_Level_Initialise = False

# METHOD FOR FINDING THE INDEX OF AN ITEM IN A LIST GIVEN ITS POSITION IN AN ARRAY
Index_Of = lambda r, c: r + c * columns

Wall_Gen = False
Wall_list = []


# PLAYER CLASS
class Player:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.Lvel = 5
        self.Uvel = 5
        self.Rvel = 5
        self.Dvel = 5
        self.scale_factor = (decimal.Decimal(Tile_Size) / decimal.Decimal(32))
        self.UpFrames = []
        self.RightFrames = []
        self.DownFrames = []
        self.LeftFrames = []
        self.FrameList = self.DownFrames
        self.Sprite_Row = 0
        self.Animation_index = 0
        self.Bomb_Count = 0
        self.wall_list_gen = True
        self.Ani_time = pygame.time.get_ticks()
        self.Death_Screen = False
        self.maze_x = 0
        self.maze_y = 0
        self.player_node = 3
        self.Pathfinding_time = pygame.time.get_ticks()
        self.Pathfinding = True
        self.Victory_Screen = False
        self.Pause_Screen = False
        self.Exit_check = True

    # GETTING INDIVIDUAL CHARACTER SPRITES FORM A SPRITE SHEET
    def Player_Frames(self):
        # UP
        for i in range(7):
            self.Sprite_Row = 0
            frame = player_sprite_sheet.get_image(self.Sprite_Row, i, 32, 32, self.scale_factor, black)
            self.UpFrames.append(frame)

        # RIGHT
        for i in range(7):
            self.Sprite_Row = 1
            frame = player_sprite_sheet.get_image(self.Sprite_Row, i, 32, 32, self.scale_factor, black)
            self.RightFrames.append(frame)

        # DOWN
        for i in range(7):
            self.Sprite_Row = 2
            frame = player_sprite_sheet.get_image(self.Sprite_Row, i, 32, 32, self.scale_factor, black)
            self.DownFrames.append(frame)

        # LEFT
        for i in range(7):
            self.Sprite_Row = 3
            frame = player_sprite_sheet.get_image(self.Sprite_Row, i, 32, 32, self.scale_factor, black)
            self.LeftFrames.append(frame)

    def Player_draw(self):
        screen.blit(self.FrameList[self.Animation_index], (self.x, self.y))

    def Player_move_animation(self, maze, PHB):
        animation_cooldown = 50
        key = pygame.key.get_pressed()

        collided_left = False
        collided_top = False
        collided_right = False
        collided_bottom = False

        # CREATING A LIST OF THE MAZES WALLS TO BE USED FOR COLLISION TESTING

        if self.wall_list_gen:
            for wall in Wall_list:
                Wall_list.remove(wall)

            for node in cell_grid:
                if node.Borders['N']:
                    Wall_list.append(node.N_Border)

                if node.Borders['E']:
                    Wall_list.append(node.E_Border)

                if node.Borders['S']:
                    Wall_list.append(node.S_Border)

                if node.Borders['W']:
                    Wall_list.append(node.W_Border)

        self.wall_list_gen = False

        # PLAYER COLLISION WITH MAZE WALLS
        for wall in Wall_list:

            # CHECKS FOR GENERAL COLLISION
            if (PHB.x + PHB.w >= wall.x and PHB.x <= wall.x + wall.w) and (
                    PHB.y + PHB.h >= wall.y and PHB.y <= wall.y + wall.h):

                # CHECKS FOR COLLISION WITH LEFT-SIDE OF A WALL
                if (PHB.x + PHB.w == wall.x) and (PHB.y != wall.y + wall.h and PHB.y + PHB.h != wall.y):
                    collided_left = True

                # CHECKS FOR COLLISION WITH RIGHT-SIDE OF A WALL
                if ((PHB.x == wall.x) or (PHB.x == wall.x + wall.w)) and (
                        PHB.y != wall.y + wall.h and PHB.y + PHB.h != wall.y):
                    collided_right = True

                # CHECKS FOR COLLISION WITH TOP-SIDE OF A WALL
                if (PHB.y + PHB.h == wall.y) and (PHB.x != wall.x + wall.w and PHB.x + PHB.w != wall.x):
                    collided_top = True

                # CHECKS FOR COLLISION WITH BOTTOM-SIDE OF A WALL
                if ((PHB.y == wall.y) or (PHB.y == wall.y + wall.h)) and (
                        PHB.x != wall.x + wall.w and PHB.x + PHB.w != wall.x):
                    collided_bottom = True

                if (collided_top == True) and (collided_left == True):
                    self.Rvel = 0
                    self.Dvel = 0

                if (collided_bottom == True) and (collided_left == True):
                    self.Uvel = 0
                    self.Rvel = 0

                if (collided_top == True) and (collided_right == True):
                    self.Dvel = 0
                    self.Lvel = 0

                if (collided_bottom == True) and (collided_right == True):
                    self.Lvel = 0
                    self.Uvel = 0

            if collided_left:
                self.Rvel = 0

            if collided_top:
                self.Dvel = 0

            if collided_right:
                self.Lvel = 0

            if collided_bottom:
                self.Uvel = 0

        # PLAYERS MOVEMENT ANIMATION
        if key[pygame.K_UP]:
            if pygame.time.get_ticks() - self.Ani_time > animation_cooldown:
                self.Animation_index += 1
                self.Ani_time = pygame.time.get_ticks()
                self.FrameList = self.UpFrames
                self.y -= self.Uvel

        if key[pygame.K_RIGHT]:
            if pygame.time.get_ticks() - self.Ani_time > animation_cooldown:
                self.Animation_index += 1
                self.Ani_time = pygame.time.get_ticks()
                self.FrameList = self.RightFrames
                self.x += self.Rvel

        if key[pygame.K_LEFT]:
            if pygame.time.get_ticks() - self.Ani_time > animation_cooldown:
                self.Animation_index += 1
                self.Ani_time = pygame.time.get_ticks()
                self.FrameList = self.LeftFrames
                self.x -= self.Lvel

        if key[pygame.K_DOWN]:
            if pygame.time.get_ticks() - self.Ani_time > animation_cooldown:
                self.Animation_index += 1
                self.Ani_time = pygame.time.get_ticks()
                self.FrameList = self.DownFrames
                self.y += self.Dvel

        if not collided_left:
            self.Rvel = 5

        if not collided_top:
            self.Dvel = 5

        if not collided_right:
            self.Lvel = 5

        if not collided_bottom:
            self.Uvel = 5

    def Player_Bombs(self):
        if Tile_Size == 100:
            self.Bomb_Count = 3
        if Tile_Size == 75:
            self.Bomb_Count = 4
        if Tile_Size == 50:
            self.Bomb_Count = 6

    def Player_collision_Enemy(self, enemy):
        self.Pathfinding = False
        Pathfinding_cooldown = 1800

        player_mid_x = PHB.x + (PHB.w // 2)
        player_mid_y = PHB.y + (PHB.h // 2)

        # GIVES THE INDEX OF THE CELL IN THE MAZE WHERE THE PLAYER CURRENTLY IS
        for i in range(columns):
            square_x = 100 + (i * Tile_Size) + (Tile_Size // 2)

            if abs(square_x - player_mid_x) <= (Tile_Size // 2):
                self.maze_x = square_x - (Tile_Size // 4)

        for i in range(rows):
            square_y = 50 + (i * Tile_Size) + (Tile_Size // 2)

            if abs(square_y - player_mid_y) <= (Tile_Size // 2):
                self.maze_y = square_y - (Tile_Size // 4)

        for node in cell_grid:
            player_Diff_x = self.maze_x - node.x - (1 - (decimal.Decimal(Tile_Size) / decimal.Decimal(100)))
            player_Diff_y = self.maze_y - node.y - (1 - (decimal.Decimal(Tile_Size) / decimal.Decimal(100)))
            player_Diff_pos = decimal.Decimal(Tile_Size) / decimal.Decimal(4)

            if player_Diff_x == player_Diff_pos and player_Diff_y == player_Diff_pos:
                self.player_node = Index_Of(node.r, node.c)

            # ENSURES THE ENEMY CATCHES THE PLAYER IF THEY ARE WITHIN ONE SQUARE OF EACH OTHER
            if enemy.player_caught:
                if abs(enemy.Enemy_node - self.player_node) == 9:
                    enemy.Enemy_node = self.player_node

                if abs(enemy.Enemy_node - self.player_node) == 1:
                    enemy.Enemy_node = self.player_node

        if enemy.Enemy_node == self.player_node:
            self.Death_Screen = True
        else:
            self.Death_Screen = False

        if pygame.time.get_ticks() - self.Pathfinding_time > Pathfinding_cooldown:
            self.Pathfinding = True
            self.Pathfinding_time = pygame.time.get_ticks()

    def Maze_Complete(self, Exit_Node_E, Exit_Node_S):
        if self.player_node == Exit_Node_E or self.player_node == Exit_Node_S:
            self.Victory_Screen = True
        else:
            self.Victory_Screen = False


# HIT BOX
class Hit_Box:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def Update_Pos(self, character_pos):
        self.x = character_pos.x + (Tile_Size * 0.2)
        self.y = character_pos.y + (Tile_Size * 0.2)

    def Enemy_Update_Pos(self, character_pos):
        self.x = character_pos.x + (Tile_Size // 4)
        self.y = character_pos.y + (Tile_Size // 4)

    def draw(self):
        pygame.draw.rect(screen, white, (self.x, self.y, self.w, self.h))


# BOMBS
class Bomb:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.Bomb_Frame_List = []
        self.Blast_list = []
        self.Bomb_index = 0
        self.scale_factor = (decimal.Decimal(Tile_Size) / decimal.Decimal(25))
        self.Bomb_Placed = False
        self.Set_Pos = False
        self.Bomb_Exploded = True
        self.Bomb_explosion = False
        self.Animation_timer = pygame.time.get_ticks()
        self.Bomb_timer_start = pygame.time.get_ticks()

    def Bomb_Frames(self):
        for i in range(3):
            B_frame = Bomb_Sprite.get_image(0, i, 16, 16, self.scale_factor, white)
            self.Bomb_Frame_List.append(B_frame)

    def Bomb_draw(self, bomb_blast):
        Bomb_Ani_cooldown = 800
        Bomb_timer_end = 4000

        if self.Bomb_Placed:
            screen.blit(self.Bomb_Frame_List[-self.Bomb_index], (self.x, self.y))

            if pygame.time.get_ticks() - self.Animation_timer > Bomb_Ani_cooldown:
                self.Bomb_index += 1
                self.Animation_timer = pygame.time.get_ticks()

            if (pygame.time.get_ticks() - self.Bomb_timer_start) > Bomb_timer_end:
                self.Bomb_Placed = False
                self.Bomb_explosion = True
                bomb_blast.Explosion_start = pygame.time.get_ticks()

    def Bomb_Animation(self, PHB, Player, bomb_blast):
        key = pygame.key.get_pressed()

        player_mid_x = PHB.x + (PHB.w // 2)
        player_mid_y = PHB.y + (PHB.h // 2)

        if self.Bomb_Exploded:
            bomb_blast.Pathfinding = False
            if key[pygame.K_b] and Player.Bomb_Count != 0:
                Player.Bomb_Count -= 1
                self.Set_Pos = True
                self.Bomb_Placed = True
                self.Bomb_Exploded = False
                self.Bomb_timer_start = pygame.time.get_ticks()
                bomb_blast.Explosion_start = pygame.time.get_ticks()

        if self.Set_Pos:
            for i in range(columns):
                square_x = 100 + (i * Tile_Size) + (Tile_Size // 2)

                if abs(square_x - player_mid_x) <= (Tile_Size // 2):
                    self.x = square_x - (Tile_Size // 4)

            for i in range(rows):
                square_y = 50 + (i * Tile_Size) + (Tile_Size // 2)

                if abs(square_y - player_mid_y) <= (Tile_Size // 2):
                    self.y = square_y - (Tile_Size // 4)

            self.Set_Pos = False


# BOMB EXPLOSION

class Bomb_Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.Explosion_start = pygame.time.get_ticks()
        self.Blast_list = []
        self.Horiz_HB = None
        self.Vert_HB = None
        self.scale_factor = (decimal.Decimal(Tile_Size) / decimal.Decimal(80))
        self.Bomb_node = 0

    def Bomb_Frames(self):
        for i in range(3):
            Blast_frame = Blast_sprite.get_image(i, 1, 48, 48, self.scale_factor, black)
            self.Blast_list.append(Blast_frame)

    def Explosion(self, Bombs, Player, enemy):
        Explosion_end = 1200

        if Bombs.Bomb_explosion:
            screen.blit(self.Blast_list[0], (Bombs.x, Bombs.y))

            screen.blit(self.Blast_list[2], (Bombs.x + (Tile_Size // 2) - 2, Bombs.y + (0.08 * Tile_Size)))

            screen.blit(pygame.transform.flip(self.Blast_list[2].convert_alpha(), True, False),
                        (Bombs.x - (Tile_Size // 2) - 2, Bombs.y + (0.08 * Tile_Size)))

            screen.blit(pygame.transform.rotate(self.Blast_list[2].convert_alpha(), 270),
                        (Bombs.x - (0.08 * Tile_Size), Bombs.y + (Tile_Size // 2) + 2))

            screen.blit(pygame.transform.rotate(self.Blast_list[2].convert_alpha(), 90),
                        (Bombs.x + (0.08 * Tile_Size), Bombs.y - (Tile_Size // 2) - 2))

            # BOMB REMOVING BREAKABLE WALLS
            for node in cell_grid:
                Bomb_Diff_x = Bombs.x - node.x - (1 - (decimal.Decimal(Tile_Size) / decimal.Decimal(100)))
                Bomb_Diff_y = Bombs.y - node.y - (1 - (decimal.Decimal(Tile_Size) / decimal.Decimal(100)))
                Bomb_Diff_pos = decimal.Decimal(Tile_Size) / decimal.Decimal(4)

                if Bomb_Diff_x == Bomb_Diff_pos and Bomb_Diff_y == Bomb_Diff_pos:
                    self.Bomb_node = Index_Of(node.r, node.c)
                    Player.wall_list_gen = False

                    if self.Bomb_node < ((columns * rows) - columns):
                        Remove_walls(cell_grid[self.Bomb_node], cell_grid[(self.Bomb_node + columns)])

                    if self.Bomb_node < ((columns * rows) - 1):
                        Remove_walls(cell_grid[self.Bomb_node], cell_grid[self.Bomb_node + 1])

                    Remove_walls(cell_grid[self.Bomb_node], cell_grid[(self.Bomb_node - columns)])
                    Remove_walls(cell_grid[self.Bomb_node], cell_grid[self.Bomb_node - 1])

                    Player.wall_list_gen = True

            if pygame.time.get_ticks() - self.Explosion_start > Explosion_end:
                Bombs.Bomb_explosion = False
                self.Explosion_start = pygame.time.get_ticks()
                Bombs.Bomb_Exploded = True
                enemy.Move = True


# ENEMY CLASS
class Enemy:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.UpFrames = []
        self.RightFrames = []
        self.DownFrames = []
        self.LeftFrames = []
        self.Move_Left = False
        self.Move_Up = False
        self.Move_Down = False
        self.Move_Right = False
        self.FrameList = self.DownFrames
        self.scale_factor = (decimal.Decimal(Tile_Size) / decimal.Decimal(32))
        self.Sprite_Row = 0
        self.Animation_index = 0
        self.Ani_time = pygame.time.get_ticks()
        self.Move_time = pygame.time.get_ticks()
        self.Route = []
        self.index = -1
        self.Move = True
        self.player_caught = False
        self.Enemy_node = -1
        self.Enemy_Dead = False

    # GETTING ENEMY ANIMATION FRAMES FROM SPRITESHEET
    def Enemy_Frames(self):
        # UP
        for i in range(7):
            self.Sprite_Row = 0
            frame = enemy_sprite_sheet.get_image(self.Sprite_Row, i, 32, 32, self.scale_factor, white)
            self.UpFrames.append(frame)

        # RIGHT
        for i in range(7):
            self.Sprite_Row = 1
            frame = enemy_sprite_sheet.get_image(self.Sprite_Row, i, 32, 32, self.scale_factor, white)
            self.RightFrames.append(frame)

        # DOWN
        for i in range(7):
            self.Sprite_Row = 2
            frame = enemy_sprite_sheet.get_image(self.Sprite_Row, i, 32, 32, self.scale_factor, white)
            self.DownFrames.append(frame)

        # LEFT
        for i in range(7):
            self.Sprite_Row = 3
            frame = enemy_sprite_sheet.get_image(self.Sprite_Row, i, 32, 32, self.scale_factor, white)
            self.LeftFrames.append(frame)

    def Enemy_draw(self):
        screen.blit(self.FrameList[self.Animation_index], (self.x, self.y))

    def Enemy_move_animation(self):
        animation_cooldown = 50

        # ENEMY ANIMATION DEPENDING ON THE DIRECTION IT IS TRAVELLING
        if self.Move_Up:
            if pygame.time.get_ticks() - self.Ani_time > animation_cooldown:
                self.Animation_index += 1
                self.Ani_time = pygame.time.get_ticks()
                self.FrameList = self.UpFrames

        if self.Move_Right:
            if pygame.time.get_ticks() - self.Ani_time > animation_cooldown:
                self.Animation_index += 1
                self.Ani_time = pygame.time.get_ticks()
                self.FrameList = self.RightFrames

        if self.Move_Left:
            if pygame.time.get_ticks() - self.Ani_time > animation_cooldown:
                self.Animation_index += 1
                self.Ani_time = pygame.time.get_ticks()
                self.FrameList = self.LeftFrames

        if self.Move_Down:
            if pygame.time.get_ticks() - self.Ani_time > animation_cooldown:
                self.Animation_index += 1
                self.Ani_time = pygame.time.get_ticks()
                self.FrameList = self.DownFrames

    def Enemy_move(self, route, Enemy_HitBox, Explosion):
        Move_cooldown = 1200
        self.Route.clear()

        # CREATES A LIST OF THE NODES IN THE PATH FOUND BY THE DIJKSTRA'S ALGORITHM

        for node in route:
            self.Route.append(node)

        if self.Move and len(self.Route) > 0:
            if pygame.time.get_ticks() - self.Move_time > Move_cooldown:
                self.index -= 1

                # COMPARES ENEMY'S POSITION WITH NEXT NODE IN ROUTE_LIST TO DETERMINE WHICH DIRECTION IT IS MOVING
                if self.Route[self.index].x < self.x:
                    self.Move_Left = True
                else:
                    self.Move_Left = False

                if self.Route[self.index].y < self.y:
                    self.Move_Up = True
                else:
                    self.Move_Up = False

                if self.Route[self.index].y > self.y:
                    self.Move_Down = True
                else:
                    self.Move_Down = False

                if self.Route[self.index].x > self.x:
                    self.Move_Right = True
                else:
                    self.Move_Right = False

                self.x = self.Route[self.index].x
                self.y = self.Route[self.index].y
                self.Move_time = pygame.time.get_ticks()

        if self.index == -(len(self.Route)):
            self.player_caught = True
            self.Move = False

        for node in cell_grid:
            if Tile_Size != 100:
                Enemy_Diff_x = 1 + (Enemy_HitBox.x - node.x - (1 - (decimal.Decimal(Tile_Size) / decimal.Decimal(100))))
                Enemy_Diff_y = 1 + (Enemy_HitBox.y - node.y - (1 - (decimal.Decimal(Tile_Size) / decimal.Decimal(100))))
            else:
                Enemy_Diff_x = Enemy_HitBox.x - node.x - (1 - (decimal.Decimal(Tile_Size) / decimal.Decimal(100)))
                Enemy_Diff_y = Enemy_HitBox.y - node.y - (1 - (decimal.Decimal(Tile_Size) / decimal.Decimal(100)))

            Enemy_Diff_pos = decimal.Decimal(Tile_Size) / decimal.Decimal(4)

            if Enemy_Diff_x == Enemy_Diff_pos and Enemy_Diff_y == Enemy_Diff_pos:
                self.Enemy_node = Index_Of(node.r, node.c)

        if self.Enemy_node == Explosion.Bomb_node:
            self.Enemy_Dead = True
        else:
            self.Enemy_Dead = False


# MAZE GENERATION
class Tile:
    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.x = 100 + self.r * Tile_Size
        self.y = 50 + self.c * Tile_Size
        self.col = red
        self.wall_col = black
        self.Borders = {'N': True, 'E': True, 'S': True, 'W': True}  # DICTIONARY USED TO DEFINE A CELLS WALLS
        self.N_Border = None
        self.E_Border = None
        self.S_Border = None
        self.W_Border = None
        self.visited = False
        self.Wall_list = []

    def draw_current_cell(self):
        X = 100 + self.r * Tile_Size
        Y = 50 + self.c * Tile_Size

        pygame.draw.rect(screen, white, (X, Y, Tile_Size, Tile_Size))

    def draw(self):
        X = 100 + self.r * Tile_Size
        Y = 50 + self.c * Tile_Size

        if self.visited:
            pygame.draw.rect(screen, self.col, (X, Y, Tile_Size, Tile_Size))

        # DRAWS WALLS OF THE MAZE TO THE SCREEN
        if self.Borders['N']:
            self.N_Border = pygame.Rect((X, Y, Tile_Size, 2))
            pygame.draw.rect(screen, self.wall_col, self.N_Border)

        if self.Borders['E']:
            self.E_Border = pygame.Rect((X + Tile_Size, Y, 2, Tile_Size))
            pygame.draw.rect(screen, self.wall_col, self.E_Border)

        if self.Borders['S']:
            self.S_Border = pygame.Rect((X, Y + Tile_Size, Tile_Size, 2))
            pygame.draw.rect(screen, self.wall_col, self.S_Border)

        if self.Borders['W']:
            self.W_Border = pygame.Rect((X, Y, 2, Tile_Size))
            pygame.draw.rect(screen, self.wall_col, self.W_Border)

    def Test_Neighbours(self):
        # TEST_CURRENTCELL FUNCTION RETURNS THE CELL BEING TESTED POSITION IN CELL_GRID
        N = Test_CurrentCell(self.r, self.c - 1)
        E = Test_CurrentCell(self.r + 1, self.c)
        S = Test_CurrentCell(self.r, self.c + 1)
        W = Test_CurrentCell(self.r - 1, self.c)

        Neighbours = []

        # ADDS THE ADJACENT NODES TO THE CURRENT NODE TO THE NEIGHBOURS LIST
        if N and N.visited == False:
            Neighbours.append(N)

        if E and E.visited == False:
            Neighbours.append(E)

        if S and S.visited == False:
            Neighbours.append(S)

        if W and W.visited == False:
            Neighbours.append(W)

        # THE MAZE GENERATION ALGORITHM IS RANDOM SO THE NEXT NODE IS A RANDOM NODE FROM THE LIST OF NEIGHBOURS
        if Neighbours:
            return random.choice(Neighbours)


def Remove_walls(current, new):
    # CALCULATES DIFFERENCE IN POSITION OF THE NEXT NODE BEING TESTED COMPARED TO THE CURRENT NODE
    Diff_r = current.r - new.r
    Diff_c = current.c - new.c

    # DEPENDING ON WHICH DIRECTION THE DIFFERENCE IN POSITION IS DETERMINES WHICH WALL IS REMOVED
    if Diff_c == 1:
        current.Borders['N'] = False
        new.Borders['S'] = False

    if Diff_c == -1:
        current.Borders['S'] = False
        new.Borders['N'] = False

    if Diff_r == 1:
        current.Borders['W'] = False
        new.Borders['E'] = False

    if Diff_r == -1:
        current.Borders['E'] = False
        new.Borders['W'] = False


def Test_CurrentCell(r, c):
    if r < 0 or r > columns - 1 or c < 0 or c > rows - 1:
        return False

    return cell_grid[Index_Of(r, c)]


Maze_Gen = True


def Build_Maze(maze):
    # BUILDS THE MAZE AS 2D LIST OF CELLS
    for row in range(rows):
        for col in range(columns):
            maze += [Tile(col, row)]


# MAZE SETUP
stack = []
Checked_cells = []


# DIJKSTRA'S PATHFINDING ALGORITHM WHICH TAKES PARAMETERS OF THE MAZE, THE TARGET NODE AND THE STARTING NODE
def Dijkstra(maze, target, Start_Cell):
    global shortest_path, neighbour

    # SETUP VISITED AND UNVISITED LIST AND ADD ALL NODES TO UNVISITED LIST WITH AN INFINITE WEIGHT
    Unvisited_list = {Node: float('inf') for Node in maze}
    Unvisited_list[maze[Start_Cell]] = 0
    Visited_list = {}

    # SET GOAL NODE OF THE ALGORITHM TO BE THE PLAYERS POSITION
    goal = maze[target]

    # DICTIONARIES THAT WILL CONTAIN THE PATH THAT THE ENEMY WILL EVENTUALLY FOLLOW
    Back_Path = {}
    Path = {}

    # SET WEIGHT OF EACH INDIVIDUAL NODE TO BE 1
    node_weight = 1

    finished = False

    while not finished:

        # SET CURRENT NODE TO BE THE NODE FROM THE UNVISITED LIST WITH THE LOWEST COST
        current_node = min(Unvisited_list, key=Unvisited_list.get)

        # THEN ADDS THE CURRENT TO THE VISITED LIST
        Visited_list[current_node] = Unvisited_list[current_node]

        current_index = Index_Of(current_node.r, current_node.c)

        # TESTS FOR EACH DIRECTION AROUND THE CURRENT NODE
        for Border in 'NESW':
            if not current_node.Borders[Border]:
                if Border == 'N':
                    neighbour = maze[(current_index - columns)]

                elif Border == 'E':
                    neighbour = maze[(current_index + 1)]

                elif Border == 'S':
                    neighbour = maze[(current_index + columns)]

                elif Border == 'W':
                    neighbour = maze[current_index - 1]

                if neighbour in Visited_list:
                    continue

                # CALCULATES THE COST OF TRAVERSING TO THAT NODE
                new_cost = Unvisited_list[current_node] + node_weight

                # COMPARES THIS COST TO THE COST OF TRAVERSING TO OTHER NEIGHBOURING CELLS
                if new_cost < Unvisited_list[neighbour]:
                    Unvisited_list[neighbour] = new_cost
                    Back_Path[neighbour] = current_node

        # CHECKS TO SEE IF THE ALGORITHM HAS REACHED THE GOAL NODE
        if current_node == maze[target]:
            shortest_path = Visited_list[maze[target]]
            finished = True

        # REMOVES CURRENT NODE FORM THE UNVISITED LIST
        Unvisited_list.pop(current_node)

    # TRAVERSES BACKWARDS THROUGH THE VISITED LIST TO FIND THE SHORTEST PATH
    while goal != (maze[Start_Cell]):
        Path[Back_Path[goal]] = goal
        goal = Back_Path[goal]

    # RETURNS THE SHORTEST PATH AND THE COST OF THAT PATH
    return Path, shortest_path


# BUTTON SETUP
Main_Menu = True
Display_Back = False
button_play = Menu.Button(screen, Menu.Button_width, Menu.Button_height,
                          ((screen_width // 2) - (Menu.Button_width // 2)), 300, red, Font, black, "Play")

button_options = Menu.Button(screen, Menu.Button_width, Menu.Button_height,
                             ((screen_width // 2) - (Menu.Button_width // 2)), 450, red, Font, black, "Options")

button_quit = Menu.Button(screen, Menu.Button_width, Menu.Button_height,
                          ((screen_width // 2) - (Menu.Button_width // 2)), 600, red, Font, black, "Quit")

button_back = Menu.Button(screen, (Menu.Button_width // 2), (Menu.Button_height // 1.5), 20, (screen_height - 100),
                          black, Font, black, "Back")

Button_list = [button_play, button_options, button_quit]

# SLIDER SETUP
Display_Options = False
slider_Master_volume = Menu.Slider(screen, 200, 20, 100, 150, 200, white, red, Font, white, 'Master Volume')
slider_Music_volume = Menu.Slider(screen, 200, 20, 100, 150, 300, white, red, Font, white, 'Music Volume')
Slider_List = [slider_Master_volume, slider_Music_volume]

# TITLE TEXT SETUP
Title = "Maze Game"
Render_TText = Title_Font.render(Title, True, red)
Title_rect = Render_TText.get_rect()
Title_rect.center = ((screen_width // 2), 150)

# CHARACTER CLASS SETUPS
player = Player(100, 50, Tile_Size, Tile_Size)
PHB = Hit_Box(player.x, player.y, (Tile_Size - (Tile_Size * 0.4)), (Tile_Size - (Tile_Size * 0.4)))
player.Player_Bombs()

enemy = Enemy(screen_width - (100 + Tile_Size), screen_height - (50 + Tile_Size), Tile_Size, Tile_Size)
EHB = Hit_Box(enemy.x, enemy.y, (Tile_Size - (Tile_Size // 2)), (Tile_Size - (Tile_Size // 2)))

# BOMB SETUP
bomb = Bomb(player.x, player.y, 32, 32)
bomb_blast = Bomb_Explosion(0, 0)

Running = True
Game_start = False

while Running:
    screen.fill(grey)
    mouse = pygame.mouse.get_pos()
    key_pressed = pygame.key.get_pressed()

    # GAME SCREEN SETUP
    if Game_start:
        Main_Menu = False

        if Next_Level_Initialise:
            player = Player(100, 50, Tile_Size, Tile_Size)
            PHB = Hit_Box(player.x, player.y, (Tile_Size - (Tile_Size * 0.4)), (Tile_Size - (Tile_Size * 0.4)))
            player.Player_Bombs()

            enemy = Enemy(screen_width - (100 + Tile_Size), screen_height - (50 + Tile_Size), Tile_Size, Tile_Size)
            EHB = Hit_Box(enemy.x, enemy.y, (Tile_Size - (Tile_Size // 2)), (Tile_Size - (Tile_Size // 2)))
            enemy.Enemy_Dead = True

            bomb = Bomb(player.x, player.y, 32, 32)
            bomb_blast = Bomb_Explosion(0, 0)

        Next_Level_Initialise = False

        # MAZE SETUP
        for cell in cell_grid:
            cell.draw()

        current_cell.visited = True

        next_cell = current_cell.Test_Neighbours()

        if len(Checked_cells) == ((columns * rows) - 1):
            Maze_Gen = False

        # MAZE GENERATION
        if Maze_Gen:
            if next_cell:
                current_cell.draw_current_cell()
                next_cell.visited = True
                Checked_cells.append(next_cell)
                stack.append(current_cell)
                Remove_walls(current_cell, next_cell)
                current_cell = next_cell
            else:
                current_cell = stack.pop()
                current_cell.draw_current_cell()

            Pathfind = True

        if not Maze_Gen:
            # CALCULATING INDEX OF EXIT POINTS OF THE MAZE
            Exit_index_E = columns * (rows // 2) - 1
            Exit_index_S = rows * columns - (columns // 2) - 1

            cell_grid[Exit_index_E].col = exit_cell_col
            cell_grid[Exit_index_S].col = exit_cell_col

            # BOMB
            bomb.Bomb_draw(bomb_blast)
            bomb.Bomb_Frames()
            bomb.Bomb_Animation(PHB, player, bomb_blast)
            bomb_blast.Bomb_Frames()
            bomb_blast.Explosion(bomb, player, enemy)

            # PLAYER FUNCTION CALLS
            player.Player_Frames()
            player.Player_draw()
            player.Player_move_animation(cell_grid, PHB)
            player.Player_collision_Enemy(enemy)

            if player.Exit_check:
                player.Maze_Complete(Exit_index_E, Exit_index_S)

            if not player.Exit_check:
                enemy.Route.clear()

            PHB.Update_Pos(player)

            # ENEMY FUNCTION CALLS
            enemy.Enemy_Frames()
            enemy.Enemy_draw()
            enemy.Enemy_move_animation()

            if player.Pathfinding:
                enemy.Move = False
                enemy.index = -1
                Pathfind = True
            else:
                enemy.Move = True

            if enemy.player_caught:
                enemy.Move = False

            if not player.Exit_check:
                path, cost = Dijkstra(cell_grid, 1, ((rows * columns) - 1))

            if Pathfind and player.Exit_check:
                path, cost = Dijkstra(cell_grid, player.player_node, enemy.Enemy_node)

            Pathfind = False
            player.Exit_check = True

            enemy.Enemy_move(path, EHB, bomb_blast)
            EHB.Enemy_Update_Pos(enemy)
            player.Player_collision_Enemy(enemy)

            Render_Text = Font.render('Bomb Count: {}'.format(str(player.Bomb_Count)), True, white)
            text_rect = Render_Text.get_rect()
            text_rect.center = (210, 30)
            screen.blit(Render_Text, text_rect)

    # BUTTON MENU SETUP
    if key_pressed[pygame.K_p] and Main_Menu == False and Display_Options == False:
        Game_start = False
        button_play.button_name = 'Resume'
        Main_Menu = True
        player.Pause_Screen = True

    if player.Death_Screen:
        Game_start = False
        button_play.button_name = 'Try Again'
        Main_Menu = True
        player.x = 100
        player.y = 50
        enemy.x = screen_width - (100 + Tile_Size)
        enemy.y = screen_height - (50 + Tile_Size)
        enemy.player_caught = False
        enemy.index = -1

    if player.Victory_Screen:
        Game_start = False
        button_play.button_name = 'Next Maze'
        Main_Menu = True
        cell_grid.clear()
        Checked_cells.clear()
        Wall_list.clear()
        player.x = 100
        player.y = 50
        enemy.x = screen_width - (100 + Tile_Size)
        enemy.y = screen_height - (50 + Tile_Size)
        enemy.Route.clear()
        enemy.player_caught = False
        enemy.index = -1

    if Main_Menu:
        screen.blit(Render_TText, Title_rect)
        for Button in Button_list:
            Button.draw()
            Button.Hit_Button(mouse)

    if Display_Options:
        for Slider in Slider_List:
            Slider.draw()
            Slider.slide(mouse)

    if Display_Back:
        button_back.draw()
        button_back.Hit_Button(mouse)

    clock.tick(100)

    for event in pygame.event.get():

        # TESTING FOR BUTTONS PRESSED
        if event.type == pygame.MOUSEBUTTONDOWN and Game_start == False:
            # SLIDER
            for slider in Slider_List:
                if slider.sliding:
                    slider.R2width = mouse[0] - slider.x

            # BUTTONS
            for Button in Button_list:
                if Button.Pressed:
                    col_change = True
                    Button.col = white
                    Button.width -= 10
                    Button.height -= 5
                    Button.x += 5

                    if Button == button_play:

                        if player.Victory_Screen == False and player.Pause_Screen == False and player.Death_Screen == False:
                            # print('play')
                            Build_Maze(cell_grid)
                            current_cell = cell_grid[0]
                            Game_start = True

                        if (player.Pause_Screen or player.Death_Screen) and player.Victory_Screen == False:
                            # print('pause / died')
                            Main_Menu = False
                            player.Pause_Screen = False
                            player.Death_Screen = False
                            Game_start = True
                            player.Player_Bombs()

                        if player.Victory_Screen and player.Pause_Screen == False:
                            # print('next level')
                            if Tile_Size > 50:
                                Tile_Size -= 25

                            columns = (screen_width - 200) // Tile_Size
                            rows = (screen_height - 100) // Tile_Size
                            Build_Maze(cell_grid)
                            current_cell = cell_grid[0]
                            player.wall_list_gen = True
                            Game_start = True
                            Maze_Gen = True
                            player.Pathfinding_time = pygame.time.get_ticks()
                            player.Victory_Screen = False
                            player.Exit_check = False
                            Next_Level_Initialise = True

                    if Button == button_options:
                        Display_Options = True
                        Display_Back = True

                    if Button == button_quit:
                        Running = False

            if Display_Options:
                Main_Menu = False
                Display_Back = True
                player.Death_Screen = False
                player.Victory_Screen = False

            if button_back.Pressed:
                col_change = True
                button_back.col = white
                Main_Menu = True
                Display_Options = False
                Display_Back = False
                button_back.Pressed = False

        if event.type == pygame.MOUSEBUTTONUP:
            for Button in Button_list:
                Button.col = red
                Button.width = 400
                Button.height = 100
                Button.x = (screen_width // 2) - (Menu.Button_width // 2)
            button_back.col = red

        if event.type == pygame.QUIT:
            Running = False

    pygame.display.update()

pygame.quit()
