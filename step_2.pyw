from Tkinter import Tk, Canvas, PhotoImage, Label
import math

class Vector3(object):
    def __init__(self, a, b, c):
        self.v = [a, b, c]
        
    def __str__(self):
        return "(%s, %s, %s)" % (self.v[0], self.v[1], self.v[2])
        
    def __repr__(self):
        return "Vector3(%s, %s, %s)" % (self.v[0], self.v[1], self.v[2])
        
    def __add__(self, other):
        return [a+b for a, b in zip(self.v, other.v)]
            
    def __sub__(self, other):
        return [a-b for a, b in zip(self.v, other.v)]
            
    def resize(self, scalar):
        self.v = [scalar*a for a in self.v]
            
    def length(self):
        return math.sqrt(sum([a*a for a in self.v]))
            
    def normalize(self):
        self.v = [float(a)/self.length for a in self.v]
            
    def dot(self, other):
        return sum([a*b for a, b in zip(self.v, other.v)])


class Raytracer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.image = PhotoImage(width=self.width, height=self.height)
        
        self.camera = [0, 0, -350]
        self.sphere_center = [0, 0, 15]
        self.sphere_radius =200
        self.color_sphere = '#%02X%02X%02X' #color mask
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
                dotval = sum([a*b for a, b in zip(component_1, direction)])
                sqrtval = dotval**2 + component_2
                
                rgb = self.color_background
                if (sqrtval >= 0):
                        hit_at_t = -dotval - math.sqrt(sqrtval)

                        hitpoint = [self.camera[0] + hit_at_t *direction[0],
                                       self.camera[1] + hit_at_t *direction[1],
                                       self.camera[2] + hit_at_t *direction[2]]
                        
                        normalv = [hitpoint[0] - self.sphere_center[0],
                                        hitpoint[1] - self.sphere_center[1],
                                        hitpoint[2] - self.sphere_center[2]]
                        #normalize
                        lengthv = math.sqrt(normalv[0]**2 + normalv[1]**2 + normalv[2]**2)
                        normalv = [a/length for a in normalv]
                            
                        cosalpha = - sum([a*b for a,b in zip(direction, normalv)])
                        redpart    = min(200 * cosalpha, 255)
                        greenpart = min(200 * cosalpha, 255)
                        bluepart   = min(200 * cosalpha, 255)
                        
                        rgb = self.color_sphere % (int(redpart), int(greenpart), int(bluepart))
                
                x_pos =   x + self.width/2
                y_pos = -y + self.height/2
                
                self.image.put(rgb, to=(x_pos,y_pos))

        return self.image


if __name__ == "__main__":
    
    root = Tk()

    rt = Raytracer( 200, 200)
    renderimage = rt.render()
    label = Label(root, image=renderimage)
    label.pack()
   
    root.mainloop()
    
    