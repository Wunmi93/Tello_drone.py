import time, cv2
from threading import Thread
from djitellopy import Tello


from tello import *

LAND = 7
tello = Tello()
tello.connect()

keepRecording = True
tello.streamon()
frame_read = tello.get_frame_read()


def videoRecorder():
    # create a VideoWrite object, recoring to ./video.avi
    height, width, _ = frame_read.frame.shape
    video = cv2.V9ideoWriter('video.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))

    while keepRecording:
        video.write(frame_read.frame)
        time.sleep(1 / 30)

    video.release()


def tello_user_instruction(user_instruction, action_value):
    tello_action = {
        1: tello.rotate_clockwise(action_value),
        2: tello.rotate_counter_clockwise(action_value),
        3: tello.move_up(action_value),
        4: tello.move_down(action_value),
        5: tello.move_back(action_value),
        6: tello.move_forward(action_value),

    }

    return tello_action[user_instruction]


# we need to run the recorder in a seperate thread, otherwise blocking options
#  would prevent frames from getting added to the video
recorder = Thread(target=videoRecorder)
recorder.start()

tello.takeoff()
user_instruction = None
while user_instruction != LAND:
    user_instruction = int(input("Enter Drone instruction number:"))
    action_value = int(input("By how many degrees/cm?"))
    tello_user_instruction(user_instruction, action_value)



# if user_instruction ==1:
#     tello.rotate_clockwise(180)
# else:
#     if user_instruction == 2:
#         tello.rotate_counter_clockwise(180)
#     else:
#         if user_instruction == 4:
#             tello.move_up(50)
#         else:
#             if user_instruction == 5:
#                 tello.move_down(50)
# 1            else:
#                 if user_instruction == 8:
#                     tello.move_forward(20)
#                 else:
#                     if user_instruction == 7:
#                         tello.move_back(20)


keepRecording = False
recorder.join()
