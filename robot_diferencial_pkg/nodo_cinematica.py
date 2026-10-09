#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from nav_msgs.msg import Odometry
import math
import numpy as np

class CinematicaDiferencial(Node):
    def __init__(self):
        super().__init__('nodo_cinematica')
        
        # Parámetros del robot (Coincidentes con el Xacro)
        self.r = 0.05
        self.L = 0.30
        
        # Variables de estado (Pose integrada q = [x, y, theta])
        self.q = np.array([0.0, 0.0, 0.0])
        self.last_time = None
        
        # Odometría del plugin de Gazebo
        self.odom_gz = np.array([0.0, 0.0, 0.0])
        
        # Suscriptores
        self.sub_joint_states = self.create_subscription(
            JointState, '/joint_states', self.joint_states_callback, 10)
            
        self.sub_odom = self.create_subscription(
            Odometry, '/odom', self.odom_callback, 10)
            
    def odom_callback(self, msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        
        # Extracción de Yaw (theta) desde cuaternión
        q = msg.pose.pose.orientation
        siny_cosp = 2 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
        theta = math.atan2(siny_cosp, cosy_cosp)
        
        self.odom_gz = np.array([x, y, theta])
        
    def joint_states_callback(self, msg):
        current_time = self.get_clock().now()
        
        if self.last_time is None:
            self.last_time = current_time
            return
            
        dt = (current_time - self.last_time).nanoseconds / 1e9
        self.last_time = current_time
        
        try:
            idx_left = msg.name.index('left_wheel_joint')
            idx_right = msg.name.index('right_wheel_joint')
        except ValueError:
            return 
            
        w_I = msg.velocity[idx_left]
        w_D = msg.velocity[idx_right]
        
        theta = self.q[2]
        
        # Matriz cinemática planteada
        matriz_cinematica = np.array([
            [ (self.r/2)*math.cos(theta),  (self.r/2)*math.cos(theta)],
            [ (self.r/2)*math.sin(theta),  (self.r/2)*math.sin(theta)],
            [ self.r/self.L,              -self.r/self.L]
        ])
        
        w_vec = np.array([w_D, w_I])
        dq = matriz_cinematica @ w_vec
        
        # Integración de Euler
        self.q += dq * dt
        self.q[2] = math.atan2(math.sin(self.q[2]), math.cos(self.q[2]))
        
        # Cálculo del error
        error = np.abs(self.q - self.odom_gz)
        
        self.get_logger().info(
            f'\nCalc : x={self.q[0]:.3f}, y={self.q[1]:.3f}, th={self.q[2]:.3f}\n'
            f'Odom : x={self.odom_gz[0]:.3f}, y={self.odom_gz[1]:.3f}, th={self.odom_gz[2]:.3f}\n'
            f'Error: x={error[0]:.4f}, y={error[1]:.4f}, th={error[2]:.4f}'
        )

def main(args=None):
    rclpy.init(args=args)
    nodo = CinematicaDiferencial()
    rclpy.spin(nodo)
    nodo.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()