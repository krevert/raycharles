from Tkinter import Tk, Canvas, PhotoImage, Label
import math


class Raytracer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.image = PhotoImage(width=self.width, height=self.height)
        
        self.camera = [0, 0, -3]
        self.sphere_center = [0, 0, 3]
        self.light = [0, -1, 0]
        self.sphere_radius = 5.9995
        self.color_sphere = '#FF0000' #red
        self.color_background = '#000000' #black

        
    def render(self):
        
        #some preprocessing
        #ray hits sphere, if:
        #(vec_camera - vec_sphere_center)^2 * vec_direction_to_screen^2 -
        #((vec_camera - vec_sphere_center)^2 - sphere_radius^2) >= 0 
        component_1 = [(a - b) for a, b in zip(self.camera, self.sphere_center)]
        component_2 = -sum([a**2 for a in component_1]) + self.sphere_radius**2
        print component_1, component_2
        
        #iterate over screen
        for y in xrange(-self.height/2, self.height/2):
            for x in xrange(-self.width/2, self.width/2):
                
                #compute ray direction
                direction = [x - self.camera[0],
                                 y - self.camera[1],
                                 0 - self.camera[2]]
                
                #normalize
                length = math.sqrt(direction[0]**2 + direction[1]**2 + direction[2]**2)
                direction = [a/length for a in direction]
                
                #color red, if ray hits sphere, black otherwise
                value = sum([a*b for a, b in zip(component_1, direction)])**2 + component_2
                
                rgb = self.color_background
                if (value >= 0):
                        rgb = self.color_sphere
                
                x_pos = x + self.width/2
                y_pos = y + self.width/2
                
                self.image.put(rgb, to=(x_pos,y_pos))

        return self.image


if __name__ == "__main__":
    
    root = Tk()

    rt = Raytracer( 640, 640)
    renderimage = rt.render()
    label = Label(root, image=renderimage)
    label.pack()
   
    root.mainloop()
    
    