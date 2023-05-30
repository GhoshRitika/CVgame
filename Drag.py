
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import random, pygame, cv2, cvzone, time

def check_within_goal(goal_pos, rad, pos):
    if goal_pos[0]-rad<pos[0]<goal_pos[0]+rad and goal_pos[1]-rad<pos[1]<goal_pos[1]+rad:
        return True
    else:
        return False

def main():
    #Pygame setup
    pygame.init()
    width, height = 1280, 720
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Balloon Drag")
    #Get feed from webcam
    capture = cv2.VideoCapture(0)
    capture.set(3, width)
    capture.set(4, height)
    # Initialize Clock for FPS
    fps = 30
    clock = pygame.time.Clock()
    speed = 15
    score = 0
    startTime = time.time()
    totalTime = 6 #60
    #Get Images
    BalloonRed = pygame.image.load('./assests/BalloonRed.png').convert_alpha()
    #create a bounding box of balloon
    rectBalloon = BalloonRed.get_rect()
    # Set the X & Y positon of top-left corner of balloon rectangle
    rectBalloon.x, rectBalloon.y = 500, 620
    w_balloon, ht_balloon = rectBalloon.size
    #Single hand playe with confidance 0f 80%
    detector = HandDetector(detectionCon=0.8, maxHands=1)
    Goal_pos = (width-100, 100)
    Goal_rad = 50
    #the main loop
    running = True
    picked = False
    while running:
        #Check if quitting the game
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
                pygame.quit()
        if int(totalTime -(time.time()-startTime)) <= 0:
            window.fill((0,0,0))
            font_size = 55
            font = pygame.font.Font(None, font_size)
            textScore = font.render(f'Your Score: {score}', True, (50, 50, 255))
            textTime = font.render(f'Time UP', True, (255, 0, 0))
            window.blit(textScore, (450, 350))
            window.blit(textTime, (530, 275))
            # time.sleep(1)
            running=False
        else:
            #getting the frames
            suc, img = capture.read()
            #Does a horizontal flip, we want our left and right are same
            img = cv2.flip(img, 1)
            #Get hand from Hand detector
            hands, img= detector.findHands(img, flipType=False)
            #Balloons moves up
            if not picked:
                rectBalloon.y = rectBalloon.y-speed
            #Check if balloon unpopped balloon has reached the top of the frame
            if rectBalloon.y<=0:
                #reset the balloon
                rectBalloon.x=random.randint(w_balloon, width-w_balloon)
                rectBalloon.y=height # not sure + ht_balloon
            if hands:
            #Find position of landmark with our image
            # lmList, _ = detector.findPosition(img)
                hand = hands[0]
                lmList = hand["lmList"]
                #index finger x and y position
                index_x, index_y=lmList[8][:2]
                fingers = detector.fingersUp(hand)
                #If inndex finger is within range of balloon, make balloon follow finger
                if picked or rectBalloon.collidepoint(index_x, index_y):
                    # if fingers[0] == 1 and fingers[1] == 1:
                    picked = True
                    rectBalloon.x = index_x - w_balloon/2
                    rectBalloon.y = index_y - ht_balloon/2
                if picked and check_within_goal(Goal_pos, Goal_rad, (index_x, index_y)):
                    # if fingers[0] == 1 and fingers[1] == 0: #Check if middle finger is released
                    rectBalloon.x=random.randint(w_balloon, width-w_balloon)
                    rectBalloon.y=height # not sure + ht_balloon
                    score +=10
                    speed += 1
                    picked=False
            temp_img = img.copy()
            cv2.circle(temp_img, (width-100, 100), 50, (0,0,255,0), thickness=5, lineType=8)
            # Blend the temporary image with the original image using addWeighted
            img = cv2.addWeighted(temp_img, 0.5, img, 0.5, 0)
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgRGB = np.rot90(imgRGB)
            frame = pygame.surfarray.make_surface(imgRGB).convert()
            frame = pygame.transform.flip(frame, True, False)
            window.blit(frame, (0, 0))
            window.blit(BalloonRed, rectBalloon)
            font = pygame.font.Font(None, 50)
            textScore = font.render(f'Score: {score}', True, (50, 50, 255))
            textTime = font.render(f'Time: {int(totalTime -(time.time()-startTime))}', True, (50, 50, 255))
            window.blit(textScore, (35, 35))
            window.blit(textTime, (1000, 35))
        # Update Display
        pygame.display.update()
        # Set FPS
        clock.tick(fps)

if __name__ == '__main__':
    main()