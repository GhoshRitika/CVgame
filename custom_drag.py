"""
Creates a pygame environment with objects thats can be dragged and dropped to a goal using fingers
through webcam input using histogram based skin color segmentation.
"""
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import random, pygame, cv2, sys, time
from fingers import Finger

"""
A class that creates and keeps track of the trash objects floating on the screen
"""
class Trash():
    """
    A static variable thats keeps track of whether the finger is already dragging an object
    """
    grabbed = False
    """
    Initializes all the necessary public variables
    :param speed The speed at which this object goes upward
    :param paper Its is a pygame Surface object of the image of a paper ball, one of the choices of trash objects floating
    :param apple Its is a pygame Surface object of the image of a apple core, one of the choices of trash objects floating
    :param can Its is a pygame Surface object of the image of a tin can, one of the choices of trash objects floating
    :param fish Its is a pygame Surface object of the image of a fish bone, one of the choices of trash objects floating
    :param banana Its is a pygame Surface object of the image of a banana peel, one of the choices of trash objects floating
    :param bottle Its is a pygame Surface object of the image of a plastic bottle, one of the choices of trash objects floating
    :return None
    """
    def __init__(self, speed, paper, apple, can, fish, banana, bottle):
        #List of all recyclable trash objects
        self.recycle = [paper, can, bottle]
        #List of the non recyclable Trash objects
        self.trash = [apple, fish, banana]
        #Size of the screen/window
        self.width, self.height = 1280, 720
        self.obj = random.choices([paper, apple, can, fish, banana, bottle], k=1)[0]
        #create a bounding box of Trash
        self.rectTrash = self.obj.get_rect()
        # Set the X & Y positon of top-left corner of Trash rectangle
        self.w_Trash, self.ht_Trash = self.rectTrash.size
        #Allowing a random starting point at the bottom of the window
        self.rectTrash.x, self.rectTrash.y = random.randint(self.w_Trash, self.width-self.w_Trash), self.height
        self.speed = speed
        #Flag keeping track of whether this object is being dragged
        self.picked=False
        #Flag keeping track of whether the object has reached its goal
        self.goal=False
        #Flag keepinng track of whther the object has either reached the end of the window height or reached the goal
        self.end = False
        #In the difficult mode this flag keeps track of whether the object has reached the correct goal
        self.correctgoal = False
    """
    Updates the position depending on whether the finger has grabbed, dragged or dropped the object
    :param far_x The x position of the tip of the finger
    :param far_y The y position of the tip of the finger
    :param fingers Number of open or extended fingers
    :param rectTrashCan The pygame Rect object containing information regarding the goal image bounding box
    :return None
    """
    def update_pos(self,far_x, far_y, fingers, rectTrashCan):
        #Checks if the finger is already dragging an objects or if this object is being dragged
        if not Trash.grabbed or self.picked:
            #If index finger is within range of Trash, make Trash follow finger
            if self.rectTrash.collidepoint(far_x, far_y) and fingers>=2:
                self.picked = True
            #If this object has been picked or grabbed by the finger, updates the position of the object such that it follows the finger
            if self.picked: 
                self.rectTrash.x = far_x - self.w_Trash/2
                self.rectTrash.y = far_y - self.ht_Trash/2
            #If the finger is dragging an object are close to the goal and the finger are apart which should release the object scoring a goal
            if self.picked and rectTrashCan.collidepoint(far_x, far_y) and fingers<2:
                self.goal = True
                self.end=True
                self.picked=False
            if self.picked:
                Trash.grabbed=True
            else:
                Trash.grabbed=False
    """
    Updates the position depending on whether the finger has grabbed, dragged or dropped the object when there are 2 goals
    :param far_x The x position of the tip of the finger
    :param far_y The y position of the tip of the finger
    :param fingers Number of open or extended fingers
    :param rectTrashCan The pygame Rect object containing information regarding the Trash Can goal image bounding box
    :param rectRecycling The pygame Rect object containing information regarding the Recycling bin goal image bounding box
    :return None
    """
    def update_pos_new(self,far_x,far_y, fingers, rectTrashCan, rectRecycling):
        #Checks if the finger is already dragging an objects or if this object is being dragged
        if not Trash.grabbed or self.picked:
            #If index finger is within range of Trash, make Trash follow finger
            if self.rectTrash.collidepoint(far_x, far_y) and fingers>=2:
                self.picked = True
            #If this object has been picked or grabbed by the finger, updates the position of the object such that it follows the finger
            if self.picked: 
                self.rectTrash.x = far_x - self.w_Trash/2
                self.rectTrash.y = far_y - self.ht_Trash/2
            # If either of the fingers dragging an object are close to the trash can goal and the fingers are apart which should release the object scoring a goal if the goal type is correct
            if self.picked and rectTrashCan.collidepoint(far_x, far_y) and fingers<2:
                self.goal = True
                self.end=True
                self.picked=False
                if (self.obj in self.trash):
                    self.correctgoal = True
            # If either of the fingers dragging an object are close to the recycling bin goal and the fingers are apart which should release the object scoring a goal if the goal type is correct
            elif self.picked and rectRecycling.collidepoint(far_x, far_y) and fingers<2:
                self.goal = True
                self.end=True
                self.picked=False
                if (self.obj in self.recycle):
                    self.correctgoal = True
            if self.picked:
                Trash.grabbed=True
            else:
                Trash.grabbed=False
    """
    Updates the position of the trash object such that it floats upwards when it is not being dragged by the finger
    """
    def move_up(self):
        # Checking whether this object has been picked up by the finger
        if not self.picked:
            self.rectTrash.y = self.rectTrash.y-self.speed
        #Trash has reached the top
        if self.rectTrash.y<=0:
            self.end=True
            self.picked = False
            if Trash.grabbed:
                Trash.grabbed=False

"""
Reference
Author : Baraltech
github link : https://github.com/baraltech/Menu-System-PyGame/blob/main/button.py
Creates a button in the pygame interface
"""
class Button():
    """
    Initializes the public variables when creating an instance of Button
    :param img The backdround image of the button
    :param pos The position in the window where the button will appear
    :param font The font of the text which appears on the button
    :param text The text that appears on the button
    :param base The default color of the text on the button
    :param hov The color of the text on the button when the mouse is hovering over the button
    :return None
    """
    def __init__(self, img, pos, font, txt, base, hov):
        self.img = img
        self.pos = pos
        # Creating a bounding rectangle of the button using the given image
        self.imgrect = self.img.get_rect(center=self.pos)
        self.font = font
        self.base = base
        self.hover = hov
        self.input_txt = txt
        # Rendering the text to be shown on the button with base color
        self.txt = self.font.render(self.input_txt, True, self.base)
        # Creating a bounding rectangle for the text positioning it right on top of button image
        self.txtrect = self.txt.get_rect(center=self.pos)
    """
    Draws the button image and text on the display window
    :param window The pygame surface object representing the game display console
    :return None
    """
    def upd(self, window):
        window.blit(self.img, self.imgrect)
        window.blit(self.txt, self.txtrect)
    """
    Checks whether the cursor is within the bounds of the button
    :param pos The x,y position of the cursor (could be mouse or finger)
    :return If the cursor is within the bounds of the button
    """
    def if_input(self, pos):
        if self.imgrect.left<=pos[0]<=self.imgrect.right and self.imgrect.top<=pos[1]<=self.imgrect.bottom:
            return True
        else:
            False
    """
    If the cursor is within the bounding box of the button, it changes the color of the text
    :param pos The x,y position of the cursor (could be mouse or finger)
    :return None
    """
    def upd_color(self, pos):
        if self.imgrect.left<=pos[0]<=self.imgrect.right and self.imgrect.top<=pos[1]<=self.imgrect.bottom:
            self.txt = self.font.render(self.input_txt, True, self.hover)
        else:
            self.txt = self.font.render(self.input_txt, True, self.base)

# Pygame setup
pygame.init()
# Size of the screen/window
width, height = 1280, 720
window = pygame.display.set_mode((width, height)) #,pygame.FULLSCREEN
pygame.display.set_caption("Time to take the Trash Out Part 2")
# Getting feed from webcam
capture = cv2.VideoCapture(0)
capture.set(3, width)
capture.set(4, height)
# Get Images of the trash objects and goals
# Image of paper ball
paper = pygame.image.load('./assests/paperball.png').convert_alpha()
paper = pygame.transform.scale(paper, (100, 100))
# Image of apple core
apple = pygame.image.load('./assests/apple.png').convert_alpha()
apple = pygame.transform.scale(apple, (50, 100))
# Image of tin can
can = pygame.image.load('./assests/tincan.png').convert_alpha()
can = pygame.transform.scale(can, (100, 150))
# Image of fish bones
fish = pygame.image.load('./assests/fishbones.png').convert_alpha()
fish = pygame.transform.scale(fish, (125, 100))
# Image of banana peel
banana = pygame.image.load('./assests/banana_peel.png').convert_alpha()
banana = pygame.transform.scale(banana, (150, 100))
# Image of plastic bottle
bottle = pygame.image.load('./assests/plastic_bottle.png').convert_alpha()
bottle = pygame.transform.scale(bottle, (75, 150))
# Image of a regualr trash can
TrashCan = pygame.image.load('./assests/TrashCan.png').convert_alpha()
TrashCan = pygame.transform.scale(TrashCan, (150, 200))
rectTrashCan = TrashCan.get_rect()
rectTrashCan.x, rectTrashCan.y = width-150-100, 100
# Image of recycling bin
RecyclingBin = pygame.image.load('./assests/recycling.png').convert_alpha()
RecyclingBin = pygame.transform.scale(RecyclingBin, (150, 200))
rectRecycling = RecyclingBin.get_rect()
rectRecycling.x, rectRecycling.y = 100, 100
# Adding background music to run on loop
pygame.mixer.music.load('./assests/jelly_fish_jam.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

"""
Starts the easy mode of the drag and drop game
:param speed The speed at which the object float upwards, the default is 15
:return None
"""
def game_easy(speed=15):
    # Initialize Clock for FPS
    fps = 30
    clock = pygame.time.Clock()
    score = 0
    startTime = time.time()
    totalTime = 60
    # Initializes finger detection module
    finger = Finger()
    running = True
    # Flag checking whether new trash object has been created in given time frame
    addedTrash = False
    # List of all the trash objects currently on screen
    Trash_list=[Trash(speed, paper, apple, can, fish,banana, bottle)]
    #the main loop
    while running:
        #Check if quitting the game
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
                pygame.quit()
        time_left=int(totalTime -(time.time()-startTime))
        if time_left <= 0:
            # Calling the game over screen
            running=False
            end(score)
        else:
            # getting the frames from webcam input
            suc, img = capture.read()
            # Does a horizontal flip, so that the left and right are same on screen
            img = cv2.flip(img, 1)
            far, cnt = finger.detect_fingers(img)
            for i in range(len(Trash_list)):
                    Trash_list[i].move_up()
            temp_img = img.copy()
            if Trash.grabbed:
                cv2.circle(temp_img, (far[0], far[1]), 25, (255, 0, 255), cv2.FILLED)
                img = cv2.addWeighted(temp_img, 0.5, img, 0.5, 0)
            else:
                cv2.circle(temp_img, (far[0], far[1]), 25, (0, 0, 255), cv2.FILLED)
                img = cv2.addWeighted(temp_img, 0.5, img, 0.5, 0)
            deleted =[]
            for i in range(len(Trash_list)):
                Trash_list[i].update_pos(far[0], far[1], cnt, rectTrashCan)
                if Trash_list[i].goal==True:
                    #If it has reached the correct goal, it will be removed from the list of Trash_list and score will increase
                    score+=10
                if Trash_list[i].end==True:
                    deleted.append(i)
            for i in range(len(deleted)):
                index = deleted[i]
                #If it has reached the top delete form the list
                Trash_list.pop(index)
            if time_left%2==0 and not addedTrash:
                addedTrash=True
                obj = Trash(speed, paper, apple, can, fish,banana, bottle)
                Trash_list.append(obj)
            elif time_left%2!=0 and addedTrash:
                addedTrash=False
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgRGB = np.rot90(imgRGB)
            frame = pygame.surfarray.make_surface(imgRGB).convert()
            frame = pygame.transform.flip(frame, True, False)
            window.blit(frame, (0, 0))
            window.blit(TrashCan, rectTrashCan)
            for i in range(len(Trash_list)):
                window.blit(Trash_list[i].obj, Trash_list[i].rectTrash)
            font_size = 50
            font = pygame.font.Font("./assests/font.ttf", font_size)
            textScore = font.render(f'Score: {score}', True, (50, 50, 255))
            textTime = font.render(f'Time: {time_left}', True, (50, 50, 255))
            window.blit(textScore, (35, 35))
            window.blit(textTime, (800, 35))
        # Update Display
        pygame.display.update()
        # Set FPS
        clock.tick(fps)
"""
Starts the difficult mode of the drag and drop game
:param speed The speed at which the object float upwards, the default is 20
:param num The frquency with which new trash objects are created
:return None
"""
def game_difficult(speed=15, num=30):
    # Initialize Clock for FPS
    fps = 30
    clock = pygame.time.Clock()
    score = 0
    startTime = time.time()
    totalTime = 60
    finger = Finger()
    running = True
    addedTrash = False
    Trash_list=[Trash(speed, paper, apple, can, fish,banana, bottle)]
    count=0
    #the main loop
    while running:
        #Check if quitting the game
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
                pygame.quit()
        time_left=int(totalTime -(time.time()-startTime))
        if time_left <= 0:
            end(score)
            running=False
        else:
            #getting the frames
            suc, img = capture.read()
            #Does a horizontal flip, we want our left and right are same
            img = cv2.flip(img, 1)
            far, cnt = finger.detect_fingers(img)
            for i in range(len(Trash_list)):
                    Trash_list[i].move_up()
            temp_img = img.copy()
            if Trash.grabbed:
                cv2.circle(temp_img, (far[0],far[1]), 35, (255, 0, 255), cv2.FILLED)
                img = cv2.addWeighted(temp_img, 0.5, img, 0.5, 0)
            else:
                cv2.circle(temp_img, (far[0],far[1]), 25, (0, 0, 255), cv2.FILLED)
                img = cv2.addWeighted(temp_img, 0.5, img, 0.5, 0)
            deleted =[]
            for i in range(len(Trash_list)):
                Trash_list[i].update_pos_new(far[0],far[1], cnt, rectTrashCan, rectRecycling)
                if Trash_list[i].goal==True:
                    if Trash_list[i].correctgoal==True:
                    #If it has reached the correct goal, it will be removed from the list of Trash_list and score will increase
                        score+=10
                    else:
                        score-=10
                if Trash_list[i].end==True:
                    deleted.append(i)
            for i in range(len(deleted)):
                index = deleted[i]
                #If it has reached the top delete form the list
                Trash_list.pop(index)
                # num = random.randint(1, 3)
            if not addedTrash:
                # for j in range(num):
                addedTrash=True
                obj = Trash(speed, paper, apple, can, fish, banana, bottle)
                Trash_list.append(obj)
            elif count==num and addedTrash:
                addedTrash=False
                count=0 #reset the count
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgRGB = np.rot90(imgRGB)
            frame = pygame.surfarray.make_surface(imgRGB).convert()
            frame = pygame.transform.flip(frame, True, False)
            window.blit(frame, (0, 0))
            window.blit(TrashCan, rectTrashCan)
            window.blit(RecyclingBin, rectRecycling)
            for i in range(len(Trash_list)):
                window.blit(Trash_list[i].obj, Trash_list[i].rectTrash)
            font_size = 50
            font = pygame.font.Font("./assests/font.ttf", font_size)
            textScore = font.render(f'Score: {score}', True, (50, 50, 255))
            textTime = font.render(f'Time: {time_left}', True, (50, 50, 255))
            window.blit(textScore, (35, 35))
            window.blit(textTime, (800, 35))
        # Update Display
        pygame.display.update()
        # Set FPS
        clock.tick(fps)
        count+=1


"""
Updates the window to display a 'Game Over' console
:param score The score of the player
:return None
"""
def end(score):
    BG1 = pygame.image.load('./assests/NoBackground1.png').convert_alpha()
    BG1 = pygame.transform.scale(BG1, (width, height))
    BG2 = pygame.image.load('./assests/NoBackground2.png').convert_alpha()
    BG2 = pygame.transform.scale(BG2, (width, height))
    BG3 = pygame.image.load('./assests/NoBackground3.png').convert_alpha()
    BG3 = pygame.transform.scale(BG3, (width, height))
    detector = HandDetector(detectionCon=0.8, maxHands=2)
    running = True
    button_clicked = False
    clicks=0
    c=0
    while running:
        #getting the frames
        suc, img = capture.read()
        #Does a horizontal flip, we want our left and right are same
        img = cv2.flip(img, 1)
        finger=Finger()
        far, cnt=finger.detect_fingers(img)
        if cnt>=0:
            MENU_MOUSE_POS = far[0], far[1]
            if cnt>=2:
                    button_clicked=True
            if button_clicked and cnt<2:
                button_clicked=False
                clicks=0
        else:
            MENU_MOUSE_POS = pygame.mouse.get_pos()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgRGB = np.rot90(imgRGB)
        frame = pygame.surfarray.make_surface(imgRGB).convert()
        frame = pygame.transform.flip(frame, True, False)
        window.blit(frame, (0, 0))
        if c==0:
            window.blit(BG1, (0, 0))
        elif c==1:
            window.blit(BG2, (0, 0))
        else:
            window.blit(BG3, (0, 0))
            c=-1
        font_main = pygame.font.Font("./assests/font.ttf", 100)
        font_button = pygame.font.Font("./assests/font.ttf", 75)
        text_score = font_button.render(f'Score: {score}', True, "#b8e600")
        text_time = font_main.render(f'Game Over', True, "#b8e600")
        score_rect = text_score.get_rect(center=(640, 250))
        time_rect = text_time.get_rect(center=(640, 100))

        MAIN_BUTTON = Button(img=pygame.image.load("./assests/Diff Rect.png"), pos=(640, 400), 
                            txt="MAIN MENU", font=font_button, base="#e65c00", hov="#e6b800")
        QUIT_BUTTON = Button(img=pygame.image.load("./assests/Quit Rect.png"), pos=(640, 550), 
                            txt="QUIT", font=font_button, base="#e65c00", hov="#e6b800")
        window.blit(text_time, time_rect)
        window.blit(text_score, score_rect)

        for button in [MAIN_BUTTON, QUIT_BUTTON]:
            button.upd_color(MENU_MOUSE_POS)
            button.upd(window)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MAIN_BUTTON.if_input(MENU_MOUSE_POS):
                    main()
                if QUIT_BUTTON.if_input(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        if button_clicked:
            if MAIN_BUTTON.if_input(MENU_MOUSE_POS):
                main()
            if QUIT_BUTTON.if_input(MENU_MOUSE_POS):
                pygame.quit()
                sys.exit()
        c+=1
        pygame.display.update()

"""
Displays the main menu window
:param score The score of the player
:return None
"""
def main():
    BG1 = pygame.image.load('./assests/NoBackground1.png').convert_alpha()
    BG1 = pygame.transform.scale(BG1, (width, height))
    BG2 = pygame.image.load('./assests/NoBackground2.png').convert_alpha()
    BG2 = pygame.transform.scale(BG2, (width, height))
    BG3 = pygame.image.load('./assests/NoBackground3.png').convert_alpha()
    BG3 = pygame.transform.scale(BG3, (width, height))
    detector = HandDetector(detectionCon=0.8, maxHands=2)
    running = True
    button_clicked = False
    c=0
    clicks=0
    while running:
        #getting the frames
        suc, img = capture.read()
        #Does a horizontal flip, we want our left and right are same
        img = cv2.flip(img, 1)
        finger=Finger()
        far, cnt=finger.detect_fingers(img)
        if cnt>=0:
            MENU_MOUSE_POS = far[0], far[1]
            if cnt>=2:
                    button_clicked=True
            if button_clicked and cnt<2:
                button_clicked=False
                clicks=0
        else:
            MENU_MOUSE_POS = pygame.mouse.get_pos()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgRGB = np.rot90(imgRGB)
        frame = pygame.surfarray.make_surface(imgRGB).convert()
        frame = pygame.transform.flip(frame, True, False)
        window.blit(frame, (0, 0))
        if c==0:
            window.blit(BG1, (0, 0))
        elif c==1:
            window.blit(BG2, (0, 0))
        else:
            window.blit(BG3, (0, 0))
            c=-1
        # MENU_MOUSE_POS = pygame.mouse.get_pos()
        font_main = pygame.font.Font("./assests/font.ttf", 100)
        font_button = pygame.font.Font("./assests/font.ttf", 75)
        MENU_TEXT = font_main.render("MAIN MENU", True, "#e62e00")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        EASY_BUTTON = Button(img=pygame.image.load("./assests/Play Rect.png"), pos=(640, 250), 
                            txt="EASY", font=font_button,  base="#e65c00", hov="#e6b800")
        DIFFICULT_BUTTON = Button(img=pygame.image.load("./assests/Diff Rect.png"), pos=(640, 400), 
                            txt="DIFFICULT", font=font_button,  base="#e65c00", hov="#e6b800")
        QUIT_BUTTON = Button(img=pygame.image.load("./assests/Quit Rect.png"), pos=(640, 550), 
                            txt="QUIT", font=font_button,  base="#e65c00", hov="#e6b800")

        window.blit(MENU_TEXT, MENU_RECT)

        for button in [EASY_BUTTON, DIFFICULT_BUTTON, QUIT_BUTTON]:
            button.upd_color(MENU_MOUSE_POS)
            button.upd(window)
        # print(button_clicked)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if EASY_BUTTON.if_input(MENU_MOUSE_POS):
                    game_easy()
                if DIFFICULT_BUTTON.if_input(MENU_MOUSE_POS):
                    game_difficult()
                if QUIT_BUTTON.if_input(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        if button_clicked:
            if EASY_BUTTON.if_input(MENU_MOUSE_POS):
                game_easy()
            if DIFFICULT_BUTTON.if_input(MENU_MOUSE_POS):
                game_difficult()
            if QUIT_BUTTON.if_input(MENU_MOUSE_POS):
                pygame.quit()
                sys.exit()
        c+=1
        pygame.display.update()

if __name__ == '__main__':
    main()