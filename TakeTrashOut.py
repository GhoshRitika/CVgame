# file
# brief Creates a pygame environment with objects thats can be dragged and dropped to a goal using fingers through webcam input
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import random, pygame, cv2, sys, time

# brief A class that creates and keeps track of the trash objects floating on the screen
class Trash():
    # brief A static variable thats keeps track of whether the finger is already dragging an object
    grabbed = False
    # brief Initializes all the necessary public variables
    # param speed The speed at which this object goes upward
    # param paper Its is a pygame Surface object of the image of a paper ball, one of the choices of trash objects floating
    # param apple Its is a pygame Surface object of the image of a apple core, one of the choices of trash objects floating
    # param can Its is a pygame Surface object of the image of a tin can, one of the choices of trash objects floating
    # param fish Its is a pygame Surface object of the image of a fish bone, one of the choices of trash objects floating
    # param banana Its is a pygame Surface object of the image of a banana peel, one of the choices of trash objects floating
    # param bottle Its is a pygame Surface object of the image of a plastic bottle, one of the choices of trash objects floating
    def __init__(self, speed, paper, apple, can, fish, banana, bottle):
        #List of all recyclable trash objects
        self.recycle = [paper, can, bottle]
        #List of the non recyclable Trash objects
        self.trash = [apple, fish, banana]
        #Size of the screen/window
        self.width, self.height = 1280, 720
        #Choosing an object at random
        self.obj = random.choices([paper, apple, can, fish, banana, bottle], k=1)[0]
        #create a bounding box of Trash
        self.rectTrash = self.obj.get_rect()
        #Set the X & Y positon of top-left corner of Trash object rectangle
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
    # brief Updates the position depending on whether the finger has grabbed, dragged or dropped the object
    # param index_x The x position of the tip of the index finger
    # param index_y The y position of the tip of the index finger
    # param middle_x The x position of the tip of the middle finger
    # param middle_y The y position of the tip of the middle finger
    # param fingers List of 0s and 1s indicating whether a finger is upright or not
    # param l The distance between the tip of the index and middle fingers
    # param rectTrashCan The pygame Rect object containing information regarding the goal image bounding box
    def update_pos(self,index_x,index_y,middle_x, middle_y, fingers, l, rectTrashCan):
        #Checks if the finger is already dragging an objects or if this object is being dragged
        if not Trash.grabbed or self.picked:
            #If index or middle finger is within range of Trash bounding box, make Trash follow finger
            if self.rectTrash.collidepoint(index_x, index_y) or self.rectTrash.collidepoint(middle_x, middle_y):
                #Checking if both index and middle fingers are up and close to each other which is the criteria for grabbing and dragging an object
                if fingers[1] == 1 and fingers[2]==1 and l<65:
                    self.picked = True
            #If this object has been picked or grabbed by the finger, updates the position of the object such that it follows the finger
            if self.picked: 
                self.rectTrash.x = (index_x+middle_x)/2 - self.w_Trash/2
                self.rectTrash.y = (index_y+middle_y)/2 - self.ht_Trash/2
            #If either of the fingers dragging an object are close to the goal and the flingers are apart which should release the object scoring a goal
            if self.picked and (rectTrashCan.collidepoint(index_x, index_y) or rectTrashCan.collidepoint(middle_x, middle_y)) and l>45:
                self.goal = True
                self.end=True
                self.picked=False
            #If neither of the fingers dragging an object are close to the goal but are far apart releasing the object such that it continues to float upwards
            if self.picked and not (rectTrashCan.collidepoint(index_x, index_y) or rectTrashCan.collidepoint(middle_x, middle_y)) and l>70:
                self.picked=False
            if self.picked:
                Trash.grabbed=True
            else:
                Trash.grabbed=False
    # brief Updates the position depending on whether the finger has grabbed, dragged or dropped the object when there are 2 goals
    # param index_x The x position of the tip of the index finger
    # param index_y The y position of the tip of the index finger
    # param middle_x The x position of the tip of the middle finger
    # param middle_y The y position of the tip of the middle finger
    # param fingers List of 0s and 1s indicating whether a finger is upright or not
    # param l The distance between the tip of the index and middle fingers
    # param rectTrashCan The pygame Rect object containing information regarding the Trash Can goal image bounding box
    # param rectRecycling The pygame Rect object containing information regarding the Recycling bin goal image bounding box
    def update_pos_new(self,index_x,index_y,middle_x, middle_y, fingers, l, rectTrashCan, rectRecycling):
        #Checks if the finger is already dragging an objects or if this object is being dragged
        if not Trash.grabbed or self.picked:
            #If index or middle finger is within range of Trash bounding box, make Trash follow finger
            if self.rectTrash.collidepoint(index_x, index_y) or self.rectTrash.collidepoint(middle_x, middle_y):
                #Checking if both index and middle fingers are up and close to each other which is the criteria for grabbing and dragging an object
                if fingers[1] == 1 and fingers[2]==1 and l<65:
                    self.picked = True
            #If this object has been picked or grabbed by the finger, updates the position of the object such that it follows the finger
            if self.picked: 
                self.rectTrash.x = (index_x+middle_x)/2 - self.w_Trash/2
                self.rectTrash.y = (index_y+middle_y)/2 - self.ht_Trash/2
            #If either of the fingers dragging an object are close to the trash can goal and the fingers are apart which should release the object scoring a goal if the goal type is correct
            if self.picked and (rectTrashCan.collidepoint(index_x, index_y) or rectTrashCan.collidepoint(middle_x, middle_y)) and l>45:
                self.goal = True
                self.end=True
                self.picked=False
                if (self.obj in self.trash):
                    self.correctgoal = True
            # If either of the fingers dragging an object are close to the recycling bin goal and the fingers are apart which should release the object scoring a goal if the goal type is correct
            elif self.picked and (rectRecycling.collidepoint(index_x, index_y) or rectRecycling.collidepoint(middle_x, middle_y)) and l>45:
                self.goal = True
                self.end=True
                self.picked=False
                if (self.obj in self.recycle):
                    self.correctgoal = True
            # If neither of the fingers dragging an object are close to any of the goals but are far apart releasing the object such that it continues to float upwards
            if self.picked and not (rectTrashCan.collidepoint(index_x, index_y) or rectTrashCan.collidepoint(middle_x, middle_y)) and not (rectRecycling.collidepoint(index_x, index_y) or rectRecycling.collidepoint(middle_x, middle_y)) and l>70:
                self.picked=False
            if self.picked:
                Trash.grabbed=True
            else:
                Trash.grabbed=False
    # brief Updates the position of the trash object such that it floats upwards when it is not being dragged by the finger
    def move_up(self):
        # Checking whether this object has been picked up by the finger
        if not self.picked:
            self.rectTrash.y = self.rectTrash.y-self.speed
        # In case the trash object has reached the top
        if self.rectTrash.y<=0:
            self.end=True
            self.picked = False
            if Trash.grabbed:
                Trash.grabbed=False

# Reference
# Author : Baraltech
# github link : https://github.com/baraltech/Menu-System-PyGame/blob/main/button.py
# brief Creates a button in the pygame interface
class Button():
    # brief initializes the public variables when creating an instance of Button
    # param img The backdround image of the button
    # param pos The position in the window where the button will appear
    # param font The font of the text which appears on the button
    # param text The text that appears on the button
    # param base The default color of the text on the button
    # param hov The color of the text on the button when the mouse is hovering over the button
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
    # brief Draws the button image and text on the display window
    # param window The pygame surface object representing the game display console
    def upd(self, window):
        window.blit(self.img, self.imgrect)
        window.blit(self.txt, self.txtrect)
    # brief Checks whether the cursor is within the bounds of the button
    # param pos The x,y position of the cursor (could be mouse or finger)
    def if_input(self, pos):
        if self.imgrect.left<=pos[0]<=self.imgrect.right and self.imgrect.top<=pos[1]<=self.imgrect.bottom:
            return True
        else:
            False
    # brief If the cursor is within the bounding box of the button, it changes the color of the text
    # param pos The x,y position of the cursor (could be mouse or finger)
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
pygame.display.set_caption("Time to take the Trash Out")
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

# brief Starts the easy mode of the drag and drop game
# param speed The speed at which the object float upwards, the default is 15
def game_easy(speed=15):
    # Initialize Clock for FPS
    fps = 30
    clock = pygame.time.Clock()
    score = 0
    startTime = time.time()
    totalTime = 60
    # Detects hands with confidance 0f 80%
    detector = HandDetector(detectionCon=0.8, maxHands=2)
    running = True
    # Flag checking whether new trash object has been created in given time frame
    addedTrash = False
    # List of all the trash objects currently on screen
    Trash_list=[Trash(speed, paper, apple, can, fish,banana, bottle)]
    # The main loop
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
            # Get hand from cvzone Hand detector
            hands= detector.findHands(img, draw=False, flipType=False)
            # Updating the positions of all the trash objects such that it floats upwards
            for i in range(len(Trash_list)):
                    Trash_list[i].move_up()
            if hands:
            # Incase of 2 hands appearing on screen, choose the right hand
                if hands[0]["type"] == "Right":
                    hand = hands[0]
                elif len(hands)>1:
                    hand = hands[1]
                else:
                    hand=hands[0]
                # Getting the landmarks information of the hand detected
                lmList = hand["lmList"]
                # index fingertip x and y position
                index_x, index_y=lmList[8][:2]
                # middle fingertip x and y position
                middle_x, middle_y=lmList[12][:2]
                # List of fingers that are upright
                fingers = detector.fingersUp(hand)
                # Distance between index and middle fingetips
                l, _ = detector.findDistance(lmList[8][:2], lmList[12][:2])
                temp_img = img.copy()
                # If the finger has grabbed or is dragging an object show a purple circle
                if Trash.grabbed:
                    cv2.circle(temp_img, (middle_x, middle_y), 25, (255, 0, 255), cv2.FILLED)
                    img = cv2.addWeighted(temp_img, 0.5, img, 0.5, 0)
                # If the fingers are just moving draw red circle on index and middle finger tips
                else:
                    cv2.circle(temp_img, (index_x, index_y), 25, (0, 0, 255), cv2.FILLED)
                    cv2.circle(temp_img, (middle_x, middle_y), 25, (0, 0, 255), cv2.FILLED)
                    img = cv2.addWeighted(temp_img, 0.5, img, 0.5, 0)
                # List of trash objects that have either reached a goal or is at the end of the display window
                deleted =[]
                # Updating the positions of all the trash objects
                for i in range(len(Trash_list)):
                    Trash_list[i].update_pos(index_x,index_y,middle_x, middle_y, fingers, l, rectTrashCan)
                    if Trash_list[i].goal==True:
                        # If it has reached the correct goal, it will be removed from the list of current trash objects and score will increase
                        score+=10
                    # Updates the list of trash objects that have need to be removed form the screen
                    if Trash_list[i].end==True:
                        deleted.append(i)
                # Removing all the trash objects from the screen that have reached its end
                for i in range(len(deleted)):
                    index = deleted[i]
                    #If it has reached the top delete form the list
                    Trash_list.pop(index)
            # Adding new trash objects every other second
            if time_left%2==0 and not addedTrash:
                addedTrash=True
                obj = Trash(speed, paper, apple, can, fish,banana, bottle)
                Trash_list.append(obj)
            elif time_left%2!=0 and addedTrash:
                addedTrash=False
            # Using the webcam feed as the base image for the display window
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgRGB = np.rot90(imgRGB)
            frame = pygame.surfarray.make_surface(imgRGB).convert()
            frame = pygame.transform.flip(frame, True, False)
            window.blit(frame, (0, 0))
            # Displaying the goal
            window.blit(TrashCan, rectTrashCan)
            # Displaying all the current tash objects on the screen as an overlay
            for i in range(len(Trash_list)):
                window.blit(Trash_list[i].obj, Trash_list[i].rectTrash)
            # Displaying the time left and the score on the top of the window
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

# brief Starts the difficult mode of the drag and drop game
# param speed The speed at which the object float upwards, the default is 20
# param num The frquency with which new trash objects are created
def game_difficult(speed=20, num=15):
    # Initialize Clock for FPS
    fps = 30
    clock = pygame.time.Clock()
    score = 0
    startTime = time.time()
    totalTime = 60
    # Detects hands with confidance 0f 80%
    detector = HandDetector(detectionCon=0.8, maxHands=2)
    running = True
    # Flag checking whether new trash object has been created in given time frame
    addedTrash = False
    # List of all the trash objects currently on screen
    Trash_list=[Trash(speed, paper, apple, can, fish,banana, bottle)]
    # Count tracking when the last object was created
    count=0
    # The main loop
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
            # Get hand from cvzone Hand detector
            hands= detector.findHands(img, draw=False, flipType=False)
            # Updating the positions of all the trash objects such that it floats upwards
            for i in range(len(Trash_list)):
                    Trash_list[i].move_up()
            if hands:
            # Incase of 2 hands appearing on screen, choose the right hand
                if hands[0]["type"] == "Right":
                    hand = hands[0]
                elif len(hands)>1:
                    hand = hands[1]
                else:
                    hand=hands[0]
                # Getting the landmarks information of the hand detected
                lmList = hand["lmList"]
                # index fingertip x and y position
                index_x, index_y=lmList[8][:2]
                # middle fingertip x and y position
                middle_x, middle_y=lmList[12][:2]
                # List of fingers that are upright
                fingers = detector.fingersUp(hand)
                # Distance between index and middle fingetips
                l, _ = detector.findDistance(lmList[8][:2], lmList[12][:2])
                temp_img = img.copy()
                # If the finger has grabbed or is dragging an object show a purple circle
                if Trash.grabbed:
                    cv2.circle(temp_img, (middle_x,middle_y), 35, (255, 0, 255), cv2.FILLED)
                    img = cv2.addWeighted(temp_img, 0.5, img, 0.5, 0)
                # If the fingers are just moving draw red circle on index and middle finger tips
                else:
                    cv2.circle(temp_img, (index_x, index_y), 25, (0, 0, 255), cv2.FILLED)
                    cv2.circle(temp_img, (middle_x, middle_y), 25, (0, 0, 255), cv2.FILLED)
                    img = cv2.addWeighted(temp_img, 0.5, img, 0.5, 0)
                # List of trash objects that have either reached a goal or is at the end of the display window
                deleted =[]
                # Updating the positions of all the trash objects
                for i in range(len(Trash_list)):
                    Trash_list[i].update_pos_new(index_x,index_y,middle_x, middle_y, fingers, l, rectTrashCan, rectRecycling)
                    if Trash_list[i].goal==True:
                        if Trash_list[i].correctgoal==True:
                            # If it has reached the correct goal, it will be removed from the list of current trash objects and score will increase
                            score+=10
                        else:
                            # If it has reached the incorrect goal, it will be removed from the list of current trash objects and score will decrease
                            score-=10
                    # Updates the list of trash objects that have need to be removed form the screen
                    if Trash_list[i].end==True:
                        deleted.append(i)
                # Removing all the trash objects from the screen that have reached its end
                for i in range(len(deleted)):
                    index = deleted[i]
                    # If it has reached the top delete form the list
                    Trash_list.pop(index)
            # If new trash object has not been added in the given time period or given number of frames
            if not addedTrash:
                addedTrash=True
                obj = Trash(speed, paper, apple, can, fish, banana, bottle)
                Trash_list.append(obj)
            # If given number of frames has passed and no new trash object has been added
            elif count==num and addedTrash:
                addedTrash=False
                #reset the count
                count=0
            # Using the webcam feed as the base image for the display window
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgRGB = np.rot90(imgRGB)
            frame = pygame.surfarray.make_surface(imgRGB).convert()
            frame = pygame.transform.flip(frame, True, False)
            window.blit(frame, (0, 0))
            # Displaying the goals
            window.blit(TrashCan, rectTrashCan)
            window.blit(RecyclingBin, rectRecycling)
            # Displaying all the current tash objects on the screen as an overlay
            for i in range(len(Trash_list)):
                window.blit(Trash_list[i].obj, Trash_list[i].rectTrash)
            # Displaying the time left and the score on the top of the window
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

# brief Updates the window to display a 'Game Over' console
# param score The score of the player
def end(score):
    # The 3 backgrounds images which alternate to give an animation effect
    BG1 = pygame.image.load('./assests/NoBackground1.png').convert_alpha()
    BG1 = pygame.transform.scale(BG1, (width, height))
    BG2 = pygame.image.load('./assests/NoBackground2.png').convert_alpha()
    BG2 = pygame.transform.scale(BG2, (width, height))
    BG3 = pygame.image.load('./assests/NoBackground3.png').convert_alpha()
    BG3 = pygame.transform.scale(BG3, (width, height))
    # Detects hands with confidance 0f 80%
    detector = HandDetector(detectionCon=0.8, maxHands=2)
    running = True
    # Flag checking if button has been clicked
    button_clicked = False
    clicks=0
    # A count to assisst with the alternating backgrounds
    c=0
    while running:
        # getting the frames from webcam input
        suc, img = capture.read()
        # Does a horizontal flip, so that the left and right are same on screen
        img = cv2.flip(img, 1)
        # Get hand from cvzone Hand detector
        hands= detector.findHands(img, draw=False, flipType=False)
        if hands:
        # Incase of 2 hands appearing on screen, choose the right hand
            if hands[0]["type"] == "Right":
                hand = hands[0]
            elif len(hands)>1:
                hand = hands[1]
            else:
                hand=hands[0]
            # Getting the landmarks information of the hand detected
            lmList = hand["lmList"]
            # index fingertip x and y position
            index_x, index_y=lmList[8][:2]
            # Distance between index and middle fingetips
            l, _ = detector.findDistance(lmList[8][:2], lmList[12][:2])
            # Updating the cursor with index fingertip position
            MENU_MOUSE_POS = index_x, index_y
            # If the middle and index finger tips are close together, it is clicking
            if l<30:
                # To make sure it is a deliberate click, checks if the clicking gesture is consistant for 3 frames
                clicks+=1
                if clicks >=3:
                    button_clicked=True
            # In case of releasing the click
            if button_clicked and l>45:
                button_clicked=False
                clicks=0
        else:
            # If no hands are detected, the mouse input is used
            MENU_MOUSE_POS = pygame.mouse.get_pos()
        # Using the webcam feed as the base image for the display window
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgRGB = np.rot90(imgRGB)
        frame = pygame.surfarray.make_surface(imgRGB).convert()
        frame = pygame.transform.flip(frame, True, False)
        window.blit(frame, (0, 0))
        # Alternating between the backgrounds to create an animation effect
        if c==0:
            window.blit(BG1, (0, 0))
        elif c==1:
            window.blit(BG2, (0, 0))
        else:
            window.blit(BG3, (0, 0))
            c=-1
        # Intitializing the heading text, time, score and different option to be displayed
        font_main = pygame.font.Font("./assests/font.ttf", 100)
        font_button = pygame.font.Font("./assests/font.ttf", 75)
        text_score = font_button.render(f'Score: {score}', True, "#b8e600")
        text_time = font_main.render(f'Game Over', True, "#b8e600")
        score_rect = text_score.get_rect(center=(640, 250))
        time_rect = text_time.get_rect(center=(640, 100))
        # Creating a Return to menu page option
        MAIN_BUTTON = Button(img=pygame.image.load("./assests/Diff Rect.png"), pos=(640, 400), 
                            txt="MAIN MENU", font=font_button, base="#e65c00", hov="#e6b800")
        # Creating a quit game option
        QUIT_BUTTON = Button(img=pygame.image.load("./assests/Quit Rect.png"), pos=(640, 550), 
                            txt="QUIT", font=font_button, base="#e65c00", hov="#e6b800")
        window.blit(text_time, time_rect)
        window.blit(text_score, score_rect)
        # Checking if mouse is hovering over a button and displaying the objects 
        for button in [MAIN_BUTTON, QUIT_BUTTON]:
            button.upd_color(MENU_MOUSE_POS)
            button.upd(window)
        # Checking if the mouse has clciked any of the buttons
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MAIN_BUTTON.if_input(MENU_MOUSE_POS):
                    menu()
                if QUIT_BUTTON.if_input(MENU_MOUSE_POS):
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
        # Checking if the finger cursor has clicked any of the buttons
        if button_clicked:
            if MAIN_BUTTON.if_input(MENU_MOUSE_POS):
                menu()
            if QUIT_BUTTON.if_input(MENU_MOUSE_POS):
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
        c+=1
        pygame.display.update()
def menu():
    # The 3 backgrounds images which alternate to give an animation effect
    BG1 = pygame.image.load('./assests/NoBackground1.png').convert_alpha()
    BG1 = pygame.transform.scale(BG1, (width, height))
    BG2 = pygame.image.load('./assests/NoBackground2.png').convert_alpha()
    BG2 = pygame.transform.scale(BG2, (width, height))
    BG3 = pygame.image.load('./assests/NoBackground3.png').convert_alpha()
    BG3 = pygame.transform.scale(BG3, (width, height))
    # Detects hands with confidance 0f 80%
    detector = HandDetector(detectionCon=0.8, maxHands=2)
    running = True
    # Flag checking if button has been clicked
    button_clicked = False
    # A count to assisst with the alternating backgrounds
    c=0
    # A count to make sure the button has been clicked
    clicks=0
    while running:
        # getting the frames from webcam input
        suc, img = capture.read()
        # Does a horizontal flip, so that the left and right are same on screen
        img = cv2.flip(img, 1)
        # Get hand from cvzone Hand detector
        hands= detector.findHands(img, draw=False, flipType=False)
        if hands:
        # Incase of 2 hands appearing on screen, choose the right hand
            if hands[0]["type"] == "Right":
                hand = hands[0]
            elif len(hands)>1:
                hand = hands[1]
            else:
                hand=hands[0]
            # Getting the landmarks information of the hand detected
            lmList = hand["lmList"]
            # index fingertip x and y position
            index_x, index_y=lmList[8][:2]
            # Distance between index and middle fingetips
            l, _ = detector.findDistance(lmList[8][:2], lmList[12][:2])
            # Updating the cursor with index fingertip position
            MENU_MOUSE_POS = index_x, index_y
            # If the middle and index finger tips are close together, it is clicking
            if l<30:
                # To make sure it is a deliberate click, checks if the clicking gesture is consistant for 3 frames
                clicks+=1
                if clicks >=3:
                    button_clicked=True
            # In case of releasing the click
            if button_clicked and l>45:
                button_clicked=False
                clicks=0
        else:
            # If no hands are detected, the mouse input is used
            MENU_MOUSE_POS = pygame.mouse.get_pos()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgRGB = np.rot90(imgRGB)
        frame = pygame.surfarray.make_surface(imgRGB).convert()
        frame = pygame.transform.flip(frame, True, False)
        window.blit(frame, (0, 0))
        # Alternating between the backgrounds to create an animation effect
        if c==0:
            window.blit(BG1, (0, 0))
        elif c==1:
            window.blit(BG2, (0, 0))
        else:
            window.blit(BG3, (0, 0))
            c=-1
        # Intitializing the heading text and different option to be displayed
        font_main = pygame.font.Font("./assests/font.ttf", 100)
        font_button = pygame.font.Font("./assests/font.ttf", 75)
        MENU_TEXT = font_main.render("MAIN MENU", True, "#e62e00")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        # Creating a button to start easy mode option
        EASY_BUTTON = Button(img=pygame.image.load("./assests/Play Rect.png"), pos=(640, 250), 
                            txt="EASY", font=font_button,  base="#e65c00", hov="#e6b800")
        # Creating a button to difficult easy mode option
        DIFFICULT_BUTTON = Button(img=pygame.image.load("./assests/Diff Rect.png"), pos=(640, 400), 
                            txt="DIFFICULT", font=font_button,  base="#e65c00", hov="#e6b800")
        # Creating a quit game option
        QUIT_BUTTON = Button(img=pygame.image.load("./assests/Quit Rect.png"), pos=(640, 550), 
                            txt="QUIT", font=font_button,  base="#e65c00", hov="#e6b800")
        window.blit(MENU_TEXT, MENU_RECT)
        # Checking if mouse is hovering over a button and displaying the objects 
        for button in [EASY_BUTTON, DIFFICULT_BUTTON, QUIT_BUTTON]:
            button.upd_color(MENU_MOUSE_POS)
            button.upd(window)
        # Checking if the mouse has clicked any of the buttons
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
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
        # Checking if the finger cursor has clicked any of the buttons
        if button_clicked:
            if EASY_BUTTON.if_input(MENU_MOUSE_POS):
                game_easy()
            if DIFFICULT_BUTTON.if_input(MENU_MOUSE_POS):
                game_difficult()
            if QUIT_BUTTON.if_input(MENU_MOUSE_POS):
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
        c+=1
        pygame.display.update()

if __name__ == '__main__':
    menu()