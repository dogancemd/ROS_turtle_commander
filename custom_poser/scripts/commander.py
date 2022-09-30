#!/usr/bin/env python3

from custom_poser.srv import pose_change
import rospy
import sys

rospy.init_node("commander_node",anonymous=True)


if __name__=="__main__":
    x,y=int(sys.argv[1]),int(sys.argv[2])

    rospy.wait_for_service("pose_change")
    client=rospy.ServiceProxy("pose_change",pose_change)

    client.call(x,y)