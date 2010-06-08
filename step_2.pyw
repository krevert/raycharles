from Tkinter import Tk, PhotoImage, Label
import math

class Vector3(object):
    def __init__(self, a, b, c):
        self.v = [a, b, c]
        
    def __str__(self):
        return "(%s, %s, %s)" % (self.v[0], self.v[1], self.v[2])
        
    def __repr__(self):
        return "Vector3: (%s, %s, %s)" % (self.v[0], self.v[1], self.v[2])
        
    def __add__(self, other):
        return Vector3(*[a+b for a, b in zip(self.v, other.v)])
            
    def __sub__(self, other):
        return Vector3(*[a-b for a, b in zip(self.v, other.v)])
            
    def resize(self, scalar):
        self.v = [scalar*a for a in self.v]
            
    def scalarmul(self, scalar):
        return Vector3(*[scalar*a for a in self.v])
            
    def length(self):
        return math.sqrt(sum([a*a for a in self.v]))
            
    def normalize(self):
        self.v = [a/float(self.length()) for a in self.v]
            
    def dot(self, other):
        return sum([a*b for a, b in zip(self.v, other.v)])
            
    def directionTo(self, other):
        return other - self

class Ray(object):
    def __init__(self, point_1, point_2):
        self.support = point_1
        self.direction = point_1.directionTo(point_2)
        self.direction.normalize()
        
class Raytracer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.image = PhotoImage(width=self.width, height=self.height)
        
        self.camera = Vector3(0, 0, -650)
        self.sphere_center = Vector3(0, 0, 15)
        self.light = Vector3(-100, 300, -650)
        self.sphere_radius =400
        self.color_sphere = '#%02X%02X%02X' #color mask
        self.color_background = '#000000' #black

        
    def render(self):
        
        #some preprocessing
        #ray hits sphere, if:
        #(vec_camera - vec_sphere_center)^2 * vec_direction_to_screen^2 -
        #((vec_camera - vec_sphere_center)^2 - sphere_radius^2) >= 0 
        part_1 = self.camera - self.sphere_center
        part_2 = -part_1.dot(part_1) + self.sphere_radius**2
        print part_1, part_2
        
        #iterate over screen
        for y in xrange(-self.height/2, self.height/2):
            for x in xrange(-self.width/2, self.width/2):
                
                #compute ray direction
                ray = Ray(self.camera, Vector3(x, y, 0))
                
                #color red, if ray hits sphere, black otherwise
                dotval = ray.direction.dot(part_1)
                discriminant = dotval**2 + part_2
                
                rgb = self.color_background
                if (discriminant >= 0):
                        hit_at_t = -dotval - math.sqrt(discriminant)
                        
                        hitpoint = ray.support + ray.direction.scalarmul(hit_at_t)
                        normalv = self.sphere_center.directionTo(hitpoint)
                        normalv.normalize()
                        
                        toLight = hitpoint.directionTo(self.light)
                        toLight.normalize();

                        cosalpha = max(0, normalv.dot(toLight))
                        redpart    = min(200 * cosalpha, 255)
                        greenpart = min(0 * cosalpha, 255)
                        bluepart   = min(0 * cosalpha, 255)
                        
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
    
    