#!/usr/bin/env python3
import math
import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist,PoseStamped
import time
from custom_poser.srv import pose_change
class Position:
    def __init__(self,x=0,y=0,theta=0):
        self.x=x
        self.y=y
        self.theta=theta
    def print_pos(self):
        print(f"x:{self.x},y:{self.y},theta:{self.theta}")
    def pos(self):
        return self.x,self.y,self.theta
    def set_pos(self,x,y=0,theta=0):
        if type(x)==int:
            self.x,self.y,self.theta=x,y,theta
        elif type(x)==tuple:
            self.x,self.y,self.theta=x[0],x[1],x[2]
def pose_cmd_handler(req):
    global target_position
    target_position.x,target_position.y=req.x,req.y
    return True
def callback(data):
    global current_position
    current_position.x,current_position.y,current_position.theta=data.x,data.y,data.theta
def msg_setter(target,current):
    global pub,msg
    msg.linear.x=target.x-current.x
    msg.linear.y=target.y-current.y
    
rospy.init_node("publisher_node",anonymous=True)
pub=rospy.Publisher("/turtle1/cmd_vel",Twist,queue_size=1000)
current_position=Position()
sub=rospy.Subscriber("/turtle1/pose",Pose,callback)
msg=Twist()
target_position=Position()
time.sleep(1)
target_position.set_pos(current_position.pos())
rospy.Service("pose_change",pose_change,pose_cmd_handler)
if __name__=="__main__":
    r=rospy.Rate(1)
    while True:
        msg_setter(target_position,current_position)
        pub.publish(msg)
        msg.linear.x,msg.linear.y=0,0
        r.sleep()