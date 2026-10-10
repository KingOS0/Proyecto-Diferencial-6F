# Entrega 1 - Simulación de Robot Diferencial en ROS 2

**Institución:** Universidad EIA\
**Programa:** Ingeniería Mecatrónica

### Integrantes del Equipo

* Idekel Plaza Osorio
* Cristian Ramirez
* Samuel Patiño
* Matteo Paganessi

---

## 1. Descripción General del Proyecto

Este paquete de ROS 2 implementa la simulación completa de un robot móvil de tracción diferencial con fines académicos. El sistema abarca:

* **Modelado Físico y Cinemático:** Definición del chasis, ruedas y dimensiones mediante archivos URDF/Xacro.
* **Percepción y Sensores:** Integración de un sensor LiDAR y una cámara frontal simulados, conectados mediante el puente de comunicación de Gazebo (`ros_gz_bridge`).
* **Entorno de Simulación:** Un laberinto personalizado en Gazebo Sim (SDF) de 10x10 metros que incluye muros perimetrales continuos, curvas, estrechamientos, obstáculos geométricos (cilindros y esferas), una zona de spawn definida y "callejones sin salida" (trampas) diseñados para evaluar algoritmos de navegación y evasión.
* **Visualización:** Monitoreo de los tópicos del robot y los datos del sensor en tiempo real utilizando RViz2.

---

## 2. Estructura y Distribución del Repositorio

Una vez clonado el repositorio dentro de la carpeta `src` de tu espacio de trabajo, los archivos se organizan de la siguiente manera:

```text
robot_diferencial_pkg/
├── config/
│   └── visor.rviz                # Configuración predeterminada de visualización en RViz2
├── launch/
│   └── gazebo.launch.py          # Lanzador maestro (Levanta Gazebo, spawnea el robot y abre RViz
├── urdf/
│   └── robot.urdf.xacro          # Definición geométrica y física del robot, chasis y sensores
├── worlds/
│   └── pista.sdf                 # Mapa tridimensional del laberinto, muros y obstáculos
├── robot_diferencial_pkg/
│   └── nodo_cinematica.py        # Nodo personalizado en Python para el control cinemático
├── package.xml                   # Dependencias del paquete para ROS 2
├── setup.py                      # Script de configuración e instalación del paquete en Python
└── README.md                     # Documentación oficial del proyecto
```
## 3. Guía de Ejecución Paso a Paso - Simulación de Robot Diferencial
Nota Importante: Cada vez que abras una nueva terminal, es un requisito indispensable cargar las variables de entorno antes de ejecutar cualquier comando. Hazlo siempre con:
```bash
cd ~/ws_rob_diff_entrega
source install/setup.bash
```
Lanzamiento de la Simulación Principal, movimiento y nodo.
1. Abre la Terminal 1 y ejecuta:
   ```bash
   cd ~/ws_rob_diff_entrega
   source install/setup.bash
   ros2 launch robot_diferencial_pkg gazebo.launch.py
   ```
   
2. Abre terminal 2 y ejecuta:
   ```bash
   cd ~/ws_rob_diff_entrega
   source install/setup.bash
   ros2 run teleop_twist_keyboard teleop_twist_keyboard
   ```
   En esta parte usar las siguientes teclas para mover el robot con la terminal seleccionada:\
   I: Avanzar hacia adelante.\
   J: Girar a la izquierda.\
   K: Detener el robot (Freno).\
   L: Girar a la derecha.\

3. Abre la Termimnal 3 y ejecuta:
   ```bash
   cd ~/ws_rob_diff_entrega
   source install/setup.bash
   ros2 run robot_diferencial_pkg nodo_cinematica
   ```
   
