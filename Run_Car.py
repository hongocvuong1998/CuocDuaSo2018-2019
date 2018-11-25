import numpy as np
import cv2
import rospy
from std_msgs.msg import Float32
from sensor_msgs.msg import CompressedImage
import Center_Point
import math

DEBUG = False


class Lane_detect:

    # Name of the topic 
    team_name = 'UIT_ONE'
    steer_topic = '/' + team_name + '_steerAngle'
    speed_topic = '/' + team_name + '_speed'
    image_topic = '/' + team_name + '_image/compressed'
    
    def __init__(self, process_function):
        # Init all subscriber and publisher
        if DEBUG:
            print('Init sub and pub')
        self.process_function = process_function
        rospy.init_node('test', anonymous=True)
        self.speed_pub = rospy.Publisher(self.speed_topic ,
                                         Float32,
                                         queue_size=1)
        self.steer_pub = rospy.Publisher(self.steer_topic,
                                         Float32,
                                         queue_size=1)
        rospy.Subscriber(self.image_topic,
                         CompressedImage,
                         self.call_back,
                         queue_size=1, buff_size=230400)
        rospy.spin()

    def call_back(self, compressed_image):
        # Call back function which is called when new image is receive
        if DEBUG:
            print('New image %s receive' % compressed_image.format)
        np_arr = np.fromstring(compressed_image.data, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        '''Call process_function to detect lane and sign
        argument:
             @self: call set_speed and set_angle
             @image: image 
        '''
        self.process_function(self, image)

    def set_speed(self, speed):
        # set car's speed
        if DEBUG:
            print('speed: %f' % speed)
        self.speed_pub.publish(speed)

    def set_angle(self, angle):
        # set car's steer angle
        if DEBUG:
            print('steer angle: %f' % angle)
        self.steer_pub.publish(angle)


def test(control, image):
    # cv2.imshow('Frame', image)
    test=image.copy()
    angle=int(0.7*Center_Point.GetAngle(image,test))
    control.set_angle(angle) #if Angle >0 return Right else Left
    control.set_speed(60) #D:\Project\CuocDuaSo2018\src\DataFrame
    cv2.putText(test,'angle: '+str(angle),(10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8,(0,0,255),1,cv2.LINE_AA)
    cv2.imshow('test ', test)
    # name='/mnt/d/Project/CuocDuaSo2018/src/DataFrame/'+str(k)+'.jpg'
    # print(name)
    # cv2.imwrite(name,image)
    
    cv2.waitKey(100)

print('Start run car')
test = Lane_detect(test)
