import numpy as np
from typing import List, Tuple

class CoordinateTransformer:
    def __init__(self, 
                 point1: Tuple[float, float, float], 
                 point2: Tuple[float, float, float], 
                 point3: Tuple[float, float, float]):
        """
        Transformator inicializiramo s tremi točkami na tleh.
        Podamo jih v koordinatah naprave s katero merimo (izhodišče (0,0,0) je naprava).    
        """
        self.p1 = np.array(point1)
        self.p2 = np.array(point2)
        self.p3 = np.array(point3)
        
        # Normalni vektor tal
        v1 = self.p2 - self.p1
        v2 = self.p3 - self.p1
        self.normal = np.cross(v1, v2)
        self.normal = self.normal / np.linalg.norm(self.normal)
        
        # Rotacijska matrika (koordinate naprave -> koordinate tal)
        self.z_axis = self.normal
        self.x_axis = v1 / np.linalg.norm(v1)
        self.y_axis = np.cross(self.z_axis, self.x_axis)
        
        self.rotation_matrix = np.vstack((self.x_axis, self.y_axis, self.z_axis)).T
        
        # Translacijski vektor (višina naprave nad tlemi)
        self.height = -np.dot(self.normal, self.p1)
        self.device_position = np.array([0, 0, -self.height])

    def device_to_floor_coordinates(self, point: Tuple[float, float, float]) -> Tuple[float, float, float]:
        point_array = np.array(point)
        transformed = np.dot(self.rotation_matrix.T, point_array) + self.device_position
        return tuple(round(x, 3) for x in transformed)

    def floor_to_device_coordinates(self, point: Tuple[float, float, float]) -> Tuple[float, float, float]:
        point_array = np.array(point)
        transformed = np.dot(self.rotation_matrix, point_array - self.device_position)
        return tuple(round(x, 3) for x in transformed)

def get_point_input(prompt):
    while True:
        try:
            print(prompt)
            coords = input()
            x, y, z = map(float, coords.split())
            return (x, y, z)
        except ValueError:
            print("Koordinate naj bodo ločene s presledki.")

def main():
    floor_point1 = get_point_input("\nPrva točka tal: ")
    floor_point2 = get_point_input("Druga točka tal: :")
    floor_point3 = get_point_input("Tretja točka tal: ")
    
    transformer = CoordinateTransformer(floor_point1, floor_point2, floor_point3)

    point = get_point_input("\nTočka: ")
    result = transformer.device_to_floor_coordinates(point)
    print(result)

if __name__ == "__main__":
    main()
