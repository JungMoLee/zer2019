#!/usr/bin/env python
# license removed for brevity
import rospy
import numpy as np
import cv2
from core_msgs.msg import Location
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped

path = Path()
first = [ 126.773048401, 37.2390632629]
def mainloop():
    global path
    path.poses = []
    path.header.frame_id = 'car_frame'
    pub = rospy.Publisher('gpspath', Path, queue_size=10)
    rospy.init_node('gps2map', anonymous=True)
    rospy.Subscriber('/Location_msg', Location, cb)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        pub.publish(path)
        drawmap(path)
        rate.sleep()

def drawmap(path) :
    dir = rospy.get_param('/dir')
    file_name = 'secondpath.jpg'
    img = np.zeros((512,512,3), dtype = np.uint8)
    tmp = None
    for i in path.poses :
        if tmp != None :
            cv2.line( img, (int(tmp.pose.position.x) + 256, int(tmp.pose.position.y)), (int(i.pose.position.x) + 256, int(i.pose.position.y)), (255,255,255), 1 )
        tmp = i
    cv2.imwrite(dir+file_name,img)
    cv2.imshow('path',img)
    cv2.waitKey(1)

def cb(data) :
    global first
    global path
    dx = 0.00001
    dy = 0.00001
    pose = PoseStamped()
    pose.pose.position.x = (data.Long - first[0])/dx
    pose.pose.position.y = (data.Lat - first[1])/dy
    pose.pose.orientation.w = 1
    path.poses.append(pose)

if __name__ == '__main__':
    try:
        mainloop()
    except rospy.ROSInterruptException:
        pass