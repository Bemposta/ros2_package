import rclpy
from pymata4 import pymata4

from rclpy.node import Node

from std_msgs.msg import Int32, Bool, String

import yaml

TRIGGER_PIN = 12
ECHO_PIN = 13
LINEA_PIN = 10

CB_PIN_MODE = 0
CB_PIN = 1
CB_VALUE = 2
CB_TIME = 3

class ArduinoNode(Node):

    def __init__(self):
        super().__init__('ArduinoFirmataControler')
        self.publisher_hc_sr04 = self.create_publisher(Int32, 'distancia', 1)
        self.publisher_linea = self.create_publisher(Bool, 'lineas', 1)
        self.subscriber_motor = self.create_subscription(String, 'motorControl', self.motor_callback, 10)

        self.board = pymata4.Pymata4()
        self.board.set_pin_mode_sonar(TRIGGER_PIN, ECHO_PIN, callback=self.callback_hc_sr04)
        self.board.set_pin_mode_digital_input(LINEA_PIN, callback=self.callback_linea)
        
        print('ArduinoFirmataControler start!!')


    def motor_callback(self, msg):
        self.get_logger().info('Motor VEL: "%s"' % msg.data)
        #Comando solo para probar con "ros2 topic pub -1 /motorControl std_msgs/msg/String 'data: {L: -200, R: 155}'"
        comando = yaml.safe_load(msg.data)
        print("R:", comando['R'])
        print("L:", comando['L'])
        
    def callback_hc_sr04(self, data):
        msg = Int32()
        msg.data = data[CB_VALUE]
        self.publisher_hc_sr04.publish(msg)
        #self.get_logger().info('Publishing: "%s"' % msg.data)

    def callback_linea(self, data):
        msg = Bool()
        msg.data = data[CB_VALUE] != 0
        self.publisher_linea.publish(msg)
        #self.get_logger().info('Publishing: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)

    arduino_node = ArduinoNode()

    rclpy.spin(arduino_node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    arduino_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
