
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import random, pygame, cv2, sys, time
from fingers import Finger

class Balloon():
    grabbed = False
    def __init__(self, speed, paper, apple, can, fish, banana, bottle):
        self.recycle = [paper, can, bottle]
        self.trash = [apple, fish, banana]
        self.width, self.height = 1280, 720
        self.Red = random.choices([paper, apple, can, fish, banana, bottle], k=1)[0]
        #create a bounding box of balloon
        self.rectBalloon = self.Red.get_rect()
        # Set the X & Y positon of top-left corner of balloon rectangle
        self.w_balloon, self.ht_balloon = self.rectBalloon.size
        self.rectBalloon.x, self.rectBalloon.y = random.randint(self.w_balloon, self.width-self.w_balloon), self.height
        self.speed = speed
        self.picked=False
        self.goal=False
        self.end = False
        self.correctgoal = False
    def update_pos(self,far_x, far_y, fingers, rectTrashCan):
        if not Balloon.grabbed or self.picked:
            #If index finger is within range of balloon, make balloon follow finger
            if self.rectBalloon.collidepoint(far_x, far_y) and fingers>=2:
                self.picked = True
            if self.picked: 
                self.rectBalloon.x = far_x - self.w_balloon/2
                self.rectBalloon.y = far_y - self.ht_balloon/2
            if self.picked and rectTrashCan.collidepoint(far_x, far_y) and fingers<2:#improve this by checking if balloon is here
                self.goal = True
                self.end=True
                self.speed += 1 #this is no longer helpful if not respawning
                self.picked=False
            # if self.picked and not rectTrashCan.collidepoint(far_x, far_y) and fingers[2]==0:
            #     self.picked=False
            if self.picked:
                Balloon.grabbed=True
            else:
                Balloon.grabbed=False
    def update_pos_new(self,far_x,far_y, fingers, rectTrashCan, rectRecycling):
        if not Balloon.grabbed or self.picked:
            #If index finger is within range of balloon, make balloon follow finger
            if self.rectBalloon.collidepoint(far_x, far_y) and fingers>=2:
                # if fingers[1] == 1 and fingers[2]==1:
                self.picked = True
            if self.picked: 
                self.rectBalloon.x = far_x - self.w_balloon/2
                self.rectBalloon.y = far_y - self.ht_balloon/2
            if self.picked and rectTrashCan.collidepoint(far_x, far_y) and fingers<2:#improve this by checking if balloon is here
                self.goal = True
                self.end=True
                self.speed += 1 #this is no longer helpful if not respawning
                self.picked=False
                if (self.Red in self.trash):
                    self.correctgoal = True
            elif self.picked and rectRecycling.collidepoint(far_x, far_y) and fingers<2:#improve this by checking if balloon is here
                self.goal = True
                self.end=True
                self.speed += 1 #this is no longer helpful if not respawning
                self.picked=False
                if (self.Red in self.recycle):
                    self.correctgoal = True
            # if self.picked and not (rectTrashCan.collidepoint(index_x, index_y) or rectTrashCan.collidepoint(middle_x, middle_y)) and not (rectRecycling.collidepoint(index_x, index_y) or rectRecycling.collidepoint(middle_x, middle_y)) and fingers[2]==0:
            #     self.picked=False
            if self.picked:
                Balloon.grabbed=True
            else:
                Balloon.grabbed=False
    def move_up(self):
        # print(Balloon.grabbed, self.picked)
        if not self.picked:
            self.rectBalloon.y = self.rectBalloon.y-self.speed
        #Balloon has reached the top
        if self.rectBalloon.y<=0:
            self.end=True
            self.picked = False
            if Balloon.grabbed:
                Balloon.grabbed=False

class Button():
    def __init__(self, img, pos, font, txt, base, hov):
        self.img=img
        self.pos = pos
        self.imgrect=self.img.get_rect(center=self.pos)
        self.font = font
        self.base = base
        self.hover = hov
        self.input_txt = txt
        self.txt = self.font.render(self.input_txt, True, self.base)
        self.txtrect = self.txt.get_rect(center=self.pos)
    def upd(self, window):
        window.blit(self.img, self.imgrect)
        window.blit(self.txt, self.txtrect)
    def if_input(self, pos):
        if self.imgrect.left<=pos[0]<=self.imgrect.right and self.imgrect.top<=pos[1]<=self.imgrect.bottom:
            return True
        else:
            False
    def upd_color(self, pos):
        if self.imgrect.left<=pos[0]<=self.imgrect.right and self.imgrect.top<=pos[1]<=self.imgrect.bottom:
            self.txt = self.font.render(self.input_txt, True, self.hover)
        else:
            self.txt = self.font.render(self.input_txt, True, self.base)

#Pygame setup
pygame.init()
width, height = 1280, 720
window = pygame.display.set_mode((width, height)) #,pygame.FULLSCREEN
pygame.display.set_caption("Time to take the Trash Out")
#Get feed from webcam
capture = cv2.VideoCapture(0)
capture.set(3, width)
capture.set(4, height)
#set up pyautogui screen???????????????????????????????????????
#Get Images
paper = pygame.image.load('./assests/paperball.png').convert_alpha()
paper = pygame.transform.scale(paper, (100, 100))
apple = pygame.image.load('./assests/apple.png').convert_alpha()
apple = pygame.transform.scale(apple, (50, 100))
can = pygame.image.load('./assests/tincan.png').convert_alpha()
can = pygame.transform.scale(can, (100, 150))
fish = pygame.image.load('./assests/fishbones.png').convert_alpha()
fish = pygame.transform.scale(fish, (125, 100))
banana = pygame.image.load('./assests/banana_peel.png').convert_alpha()
banana = pygame.transform.scale(banana, (150, 100))
bottle = pygame.image.load('./assests/plastic_bottle.png').convert_alpha()
bottle = pygame.transform.scale(bottle, (75, 150))
TrashCan = pygame.image.load('./assests/TrashCan.png').convert_alpha()
TrashCan = pygame.transform.scale(TrashCan, (150, 200))
rectTrashCan = TrashCan.get_rect()
RecyclingBin = pygame.image.load('./assests/recycling.png').convert_alpha()
RecyclingBin = pygame.transform.scale(RecyclingBin, (150, 200))
rectRecycling = RecyclingBin.get_rect()
# rectTrashCan.x, rectTrashCan.y = 100, height-rectTrashCan.width - 100
rectTrashCan.x, rectTrashCan.y = width-150-100, 100
rectRecycling.x, rectRecycling.y = 100, 100

def game_easy(speed=15):
    # Initialize Clock for FPS
    fps = 30
    clock = pygame.time.Clock()
    # speed = 15
    score = 0
    startTime = time.time()
    totalTime = 60
    #Single hand playe with confidance 0f 80%
    # detector = HandDetector(detectionCon=0.8, maxHands=2)
    finger = Finger()
    running = True
    addedBalloons = False
    Balloons=[Balloon(speed, paper, apple, can, fish,banana, bottle)]
    #the main loop
    while running:
        #Check if quitting the game
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
                pygame.quit()
        time_left=int(totalTime -(time.time()-startTime))
        if time_left <= 0:
            # window.fill((0,0,0))
            # font_size = 50
            # font = pygame.font.Font("./assests/font.ttf", font_size)
            # textScore = font.render(f'Your Score: {score}', True, (50, 50, 255))
            # textTime = font.render(f'Time UP', True, (255, 0, 0))
            # window.blit(textScore, (450, 350))
            # window.blit(textTime, (530, 275))
            # time.sleep(1)
            end(score)
            running=False
        else:
            #getting the frames
            suc, img = capture.read()
            #Does a horizontal flip, we want our left and right are same
            img = cv2.flip(img, 1)
            #Get hand from Hand detector
            # hands= detector.findHands(img, draw=False, flipType=False)
            far, cnt = finger.manage_image_opr(img)
            for i in range(len(Balloons)):
                    Balloons[i].move_up()
            # if hands:
            # #Find position of landmark with our image
            # # lmList, _ = detector.findPosition(img)
            #     if hands[0]["type"] == "Right":
            #         hand = hands[0]
            #     elif len(hands)>1:
            #         hand = hands[1]
            #     else:
            #         hand=hands[0]
            #     lmList = hand["lmList"]
            #     #index finger x and y position
            #     index_x, index_y=lmList[8][:2]
            #     middle_x, middle_y=lmList[12][:2]
            #     fingers = detector.fingersUp(hand)
            #     l, _ = detector.findDistance(lmList[8][:2], lmList[12][:2])
            temp_img = img.copy()
            if Balloon.grabbed:
                cv2.circle(temp_img, (far[0], far[1]), 25, (255, 0, 255), cv2.FILLED)
                img = cv2.addWeighted(temp_img, 0.5, img, 0.5, 0)
            else:
                cv2.circle(temp_img, (far[0], far[1]), 25, (0, 0, 255), cv2.FILLED)
                img = cv2.addWeighted(temp_img, 0.5, img, 0.5, 0)
            # l, info= detector.findDistance(lmList[8][:2], lmList[12][:2])
            deleted =[]
            for i in range(len(Balloons)):
                Balloons[i].update_pos(far[0], far[1], cnt, rectTrashCan)
                if Balloons[i].goal==True:
                    #If it has reached the correct goal, it will be removed from the list of balloons and score will increase
                    score+=10
                if Balloons[i].end==True:
                    deleted.append(i)
            for i in range(len(deleted)):
                index = deleted[i]
                #If it has reached the top delete form the list
                Balloons.pop(index)
                # num = random.randint(1, 3)
            if time_left%2==0 and not addedBalloons:
                # for j in range(num):
                addedBalloons=True
                obj = Balloon(speed, paper, apple, can, fish,banana, bottle)
                Balloons.append(obj)
            elif time_left%2!=0 and addedBalloons:
                addedBalloons=False
            # temp_img = img.copy()
            # cv2.circle(temp_img, (width-100, 100), 50, (0,0,255,0), thickness=5, lineType=8)
            # Blend the temporary image with the original image using addWeighted
            # img = cv2.addWeighted(temp_img, 0.5, img, 0.5, 0)
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgRGB = np.rot90(imgRGB)
            frame = pygame.surfarray.make_surface(imgRGB).convert()
            frame = pygame.transform.flip(frame, True, False)
            window.blit(frame, (0, 0))
            window.blit(TrashCan, rectTrashCan)
            for i in range(len(Balloons)):
                # print(Balloons[i].rectBalloon.x, Balloons[i].rectBalloon.y)
                window.blit(Balloons[i].Red, Balloons[i].rectBalloon)
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
def game_difficult(speed=15, num=30):
    # Initialize Clock for FPS
    fps = 30
    clock = pygame.time.Clock()
    score = 0
    startTime = time.time()
    totalTime = 60
    #Single hand playe with confidance 0f 80%
    # detector = HandDetector(detectionCon=0.8, maxHands=2)
    finger = Finger()
    running = True
    addedBalloons = False
    Balloons=[Balloon(speed, paper, apple, can, fish,banana, bottle)]
    count=0
    #the main loop
    while running:
        #Check if quitting the game
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
                pygame.quit()
        time_left=int(totalTime -(time.time()-startTime))
        # print(count, time_left)
        if time_left <= 0:
            # window.fill((0,0,0))
            # font_size = 50
            # font = pygame.font.Font("./assests/font.ttf", font_size)
            # textScore = font.render(f'Your Score: {score}', True, (50, 50, 255))
            # textTime = font.render(f'Time UP', True, (255, 0, 0))
            # window.blit(textScore, (450, 350))
            # window.blit(textTime, (530, 275))
            # time.sleep(1)
            end(score)
            running=False
        else:
            #getting the frames
            suc, img = capture.read()
            #Does a horizontal flip, we want our left and right are same
            img = cv2.flip(img, 1)
            #Get hand from Hand detector
            # hands, img= detector.findHands(img, flipType=False)
            # hands= detector.findHands(img, draw=False, flipType=False)
            far, cnt = finger.manage_image_opr(img)
            for i in range(len(Balloons)):
                    Balloons[i].move_up()
            # if hands:
            # #Find position of landmark with our image
            # # lmList, _ = detector.findPosition(img)
            #     if hands[0]["type"] == "Right":
            #         hand = hands[0]
            #     elif len(hands)>1:
            #         hand = hands[1]
            #     else:
            #         hand=hands[0]
            #     lmList = hand["lmList"]
            #     #index finger x and y position
            #     index_x, index_y=lmList[8][:2]
            #     middle_x, middle_y=lmList[12][:2]
            #     fingers = detector.fingersUp(hand)
            #     l, _ = detector.findDistance(lmList[8][:2], lmList[12][:2])
            temp_img = img.copy()
            if Balloon.grabbed:
                # print((middle_x)/2, (middle_y)/2)
                # x, y = (float)((index_x+middle_x)/2), (float)((index_y+middle_y)/2)
                cv2.circle(temp_img, (far[0],far[1]), 35, (255, 0, 255), cv2.FILLED)
                img = cv2.addWeighted(temp_img, 0.5, img, 0.5, 0)
            else:
                cv2.circle(temp_img, (far[0],far[1]), 25, (0, 0, 255), cv2.FILLED)
                # cv2.circle(temp_img, (middle_x, middle_y), 25, (0, 0, 255), cv2.FILLED)
                img = cv2.addWeighted(temp_img, 0.5, img, 0.5, 0)
            # l, info= detector.findDistance(lmList[8][:2], lmList[12][:2])
            deleted =[]
            for i in range(len(Balloons)):
                Balloons[i].update_pos_new(far[0],far[1], cnt, rectTrashCan, rectRecycling)
                if Balloons[i].goal==True:
                    if Balloons[i].correctgoal==True:
                    #If it has reached the correct goal, it will be removed from the list of balloons and score will increase
                        score+=10
                    else:
                        score-=10
                if Balloons[i].end==True:
                    deleted.append(i)
            for i in range(len(deleted)):
                index = deleted[i]
                #If it has reached the top delete form the list
                Balloons.pop(index)
                # num = random.randint(1, 3)
            if not addedBalloons:
                # for j in range(num):
                addedBalloons=True
                obj = Balloon(speed, paper, apple, can, fish, banana, bottle)
                Balloons.append(obj)
            elif count==num and addedBalloons:
                addedBalloons=False
                count=0 #reset the count
            # temp_img = img.copy()
            # cv2.circle(temp_img, (width-100, 100), 50, (0,0,255,0), thickness=5, lineType=8)
            # Blend the temporary image with the original image using addWeighted
            # img = cv2.addWeighted(temp_img, 0.5, img, 0.5, 0)
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgRGB = np.rot90(imgRGB)
            frame = pygame.surfarray.make_surface(imgRGB).convert()
            frame = pygame.transform.flip(frame, True, False)
            window.blit(frame, (0, 0))
            window.blit(TrashCan, rectTrashCan)
            window.blit(RecyclingBin, rectRecycling)
            for i in range(len(Balloons)):
                # print(Balloons[i].rectBalloon.x, Balloons[i].rectBalloon.y)
                window.blit(Balloons[i].Red, Balloons[i].rectBalloon)
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
def end(score):
    # BG = pygame.image.load('./assests/BackgroundBlue.jpg').convert_alpha()
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
        #Get hand from Hand detector
        # hands, img= detector.findHands(img, flipType=False)
        # hands= detector.findHands(img, draw=False, flipType=False)
        finger=Finger()
        far, cnt=finger.manage_image_opr(img)
        # if hands:
        # #Find position of landmark with our image
        # # lmList, _ = detector.findPosition(img)
        #     if hands[0]["type"] == "Right":
        #         hand = hands[0]
        #     elif len(hands)>1:
        #         hand = hands[1]
        #     else:
        #         hand=hands[0]
        #     lmList = hand["lmList"]
        #     #index finger x and y position
        #     index_x, index_y=lmList[8][:2]
        #     l, _ = detector.findDistance(lmList[8][:2], lmList[12][:2])
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
        # window.blit(BG, (0, 0))
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
def main():
    # print("CALLLLLLLLLLLLLLLLEEEEEEEEEEEEEEEDDDDDDDDDDDDDDDDDDDDDDD")
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
        #Get hand from Hand detector
                # hands, img= detector.findHands(img, flipType=False)
        # hands= detector.findHands(img, draw=False, flipType=False)
        finger=Finger()
        far, cnt=finger.manage_image_opr(img)
        # if hands:
        # #Find position of landmark with our image
        # # lmList, _ = detector.findPosition(img)
        #     if hands[0]["type"] == "Right":
        #         hand = hands[0]
        #     elif len(hands)>1:
        #         hand = hands[1]
        #     else:
        #         hand=hands[0]
        #     lmList = hand["lmList"]
        #     #index finger x and y position
        #     index_x, index_y=lmList[8][:2]
        #     l, _ = detector.findDistance(lmList[8][:2], lmList[12][:2])
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
                # print("DIFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFICULT CLICKED")
                game_difficult()
            if QUIT_BUTTON.if_input(MENU_MOUSE_POS):
                pygame.quit()
                sys.exit()
        c+=1
        pygame.display.update()

if __name__ == '__main__':
    main()