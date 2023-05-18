# 
# Run this program
# 
#   An window will open with the first frame of the movie 
#  
#   Click mouse to start rectangle drawing
#   Move mouse
#   Click mouse to end rectangle drawing
#   Press Enter key on keyboard
#   
#   The video will start and the object will be tracked
#   Try other videos
#
#   Use ESC key to quit
#

    #  pip install imutils
    #  pip install opencv-contrib-python
    
from imutils.video import VideoStream
from imutils.video import FPS
import cv2         # pip install opencv-python

# current working directory 
video_source = "object_tracker_clip.mp4"     

# create a tracker
tracker_type = "CSRT"
tracker = cv2.TrackerCSRT_create()

# Get the video file and read first frame
video = cv2.VideoCapture(video_source)
ret, frame = video.read()

if not ret:
    print('Cannot read the video')
    exit()
    
frame_height, frame_width = frame.shape[:2]
output = cv2.VideoWriter(f'{tracker_type}.avi', 
                         cv2.VideoWriter_fourcc(*'XVID'), 30.0, 
                         (frame_width, frame_height), True)

#    
# cv2.selectROI()  - explained
# This function waits for user input 
#   Click mouse to start rectangle
#   Move mouse
#   Click mouse to end rectangle 
#   Press enter key on keyboard and video will start playing

bbox = cv2.selectROI(frame, False)
ret = tracker.init(frame, bbox)
cv2.destroyAllWindows()

failure = False

# Start tracking
while True:
    ret, frame = video.read()
    if not ret:
        print('something went wrong')
        break
    timer = cv2.getTickCount()
    ret, bbox = tracker.update(frame)
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    if ret:
        point1 = (int(bbox[0]), int(bbox[1]))
        point2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, point1, point2, (255,0,0), 2, 1)
    else:
        failure = True
    if failure:
        cv2.putText(frame, "Tracking failure detected", (50,80), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
    else:    
        cv2.putText(frame, tracker_type + " Tracker", (1,20), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2)
        cv2.putText(frame, "FPS : " + str(int(fps)), (1,50), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2)
    cv2.imshow("Tracking", frame)
    output.write(frame)
    k = cv2.waitKey(1) & 0xff
    
    # ESC key will close
    if k == 27 : break
        
video.release()
output.release()
cv2.destroyAllWindows()
