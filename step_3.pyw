from Tkinter import Tk, PhotoImage, Label
from random import randrange, shuffle, seed
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
            
    def __getitem__(self, key):
        return self.v[key]
            
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
            
    def cross(self, other):
        return Vector3(self.v[1]*other.v[2] - self.v[2]*other.v[1],
                                 self.v[2]*other.v[0] - self.v[0]*other.v[2],
                                 self.v[0]*other.v[1] - self.v[1]*other.v[0])
            
    def directionTo(self, other):
        return other - self
 
class Primitive(object):
    def __init__(self):
        self.diffuse = [1.0, 0.0, 0.0]
        self.reflection = 0.0
        self.refraction = 1.0
        
        self.computeLightDistance = False
        
    def setDiffuse(self, red, green, blue):
        self.diffuse = [red, green, blue]
        
    def intersectionValue(self, ray):  raise NotImplementedError
    def preprocessCamera(self, camera): raise NotImplementedError
    def diffuseReflectionRefraction(self, atPoint, lights): raise NotImplementedError
        
class Sphere(Primitive):
    def __init__(self, center, radius):
        Primitive.__init__(self)
        self.center = center
        self.radius = radius
        
    def preprocessCamera(self, camera):
        self.camera_cache = camera
        self.part_1 = self.camera_cache - self.center
        self.part_2 = -self.part_1.dot(self.part_1) + self.radius**2
        
    def intersectionValue(self, ray):
        dotval = ray.direction.dot(self.part_1)
        discriminant = dotval**2 + self.part_2
        
        if (discriminant < 0):
            return None
            
        return -dotval - math.sqrt(discriminant)
 
        
    def diffuseReflectionRefraction(self, atPoint, lights):
        normalv = self.center.directionTo(atPoint)
        normalv.normalize()
        
        diffuse_color = [0.0, 0.0, 0.0]
        for light in lights:
            toLight = atPoint.directionTo(light)
            toLight.normalize();
            cosalpha = max(0, normalv.dot(toLight))
            diffuse_color[0] += self.diffuse[0] * cosalpha
            diffuse_color[1] += self.diffuse[1] * cosalpha
            diffuse_color[2] += self.diffuse[2] * cosalpha
        
        return diffuse_color, None, None
        
class Plane(Primitive):
    def __init__(self, point_1, point_2, point_3):
        Primitive.__init__(self)
        self.support = point_1
        self.direction_1 = point_1.directionTo(point_2)
        self.direction_2 = point_1.directionTo(point_3)
        self.normalv = self.direction_1.cross(self.direction_2)
        self.normalv.normalize()
        print self.direction_1, self.direction_2, self.normalv
        self.d_value = self.support.dot(self.normalv) #needed for algebraic form (Hesse normal form)
        
        self.checker = True
        
    def preprocessCamera(self, camera):
        self.camera_cache = camera
        self.numerator = self.d_value - self.camera_cache.dot(self.normalv)
        
    def intersectionValue(self, ray):
        denominator = ray.direction.dot(self.normalv)
        if (denominator >= 0):
            return None
        return self.numerator / float(denominator)
 
        
    def diffuseReflectionRefraction(self, atPoint, lights):
 
        if (self.computeLightDistance):
            lightMagnitude = max((toLight.length()/600.0)**2, 1.0)
            lightMagnitude = 1.0/lightMagnitude
        else:
            lightMagnitude = 1.0
        
        color = self.diffuse
          
        temp = atPoint - self.support
        first_row       = Vector3(self.direction_1[0] + self.direction_1[2],  self.direction_2[0] + self.direction_2[2], temp[0] + temp[2])
        second_row = Vector3(self.direction_1[1] + self.direction_1[2],  self.direction_2[1] + self.direction_2[2], temp[1] + temp[2])
        #u_denominator = self.direction_1[0]*self.direction_2[1]-self.direction_1[1]*self.direction_2[0]
        #w_denominator = self.direction_2[0]*self.direction_1[1]-self.direction_2[1]*self.direction_1[0]
        
        u_denominator = first_row[0]*second_row[1]-second_row[0]*first_row[1]
        w_denominator = first_row[1]*second_row[0]-second_row[1]*first_row[0]
 
        u = w = 0
        if (u_denominator):
            #u = float(temp[0] * self.direction_2[1] - temp[1]*self.direction_2[0]) / u_denominator
            u = float(first_row[2] * second_row[1] - second_row[2]*first_row[1]) / u_denominator
        if (w_denominator):
            #w = float(temp[0] * self.direction_1[1] - temp[1]*self.direction_1[0]) / w_denominator
            w = float(first_row[2] * second_row[0] - second_row[2]*first_row[0]) / w_denominator
        
        if (self.checker):
            flip = False
            point_z =  u % 200 #atPoint[2] % 200
            if (point_z <= 100):
                flip = True
            point_x = w % 200 #atPoint[0] % 200
            if flip:
                if (point_x <= 100):
                    color = [1.0 - self.diffuse[0], 1.0 - self.diffuse[1], 1.0 - self.diffuse[2]]
            else:
                if (point_x > 100):
                     color = [1.0 - self.diffuse[0], 1.0 - self.diffuse[1], 1.0 - self.diffuse[2]]
 
        diffuse_color = [0.0, 0.0, 0.0]
        for light in lights:
            toLight = atPoint.directionTo(light)
            toLight.normalize();
            cosalpha = max(0, self.normalv.dot(toLight))
            diffuse_color[0] += color[0] * cosalpha
            diffuse_color[1] += color[1] * cosalpha
            diffuse_color[2] += color[2] * cosalpha
        
        return diffuse_color, None, None
 
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
 
        self.objects = list()
        self.camera = Vector3(0, 0, -650)
        self.lights = list()
 
        self.color_mask = '#%02X%02X%02X' #color mask
        self.color_background = '#000000' #black
 
    def addObject(self, obj):
        self.objects.append(obj)
        
    def addLight(self, light):
        self.lights.append(light)
        
    def render(self):
        
        for obj in self.objects:
            obj.preprocessCamera(self.camera)
 
        #iterate over screen
        for y in xrange(-self.height/2, self.height/2):
            for x in xrange(-self.width/2, self.width/2):
                
                #compute ray direction
                ray = Ray(self.camera, Vector3(x, y, 0))
                
                #search for nearest hit point
                nearest_t = 100000
                foundObject = None
                for obj in self.objects:
                    t = obj.intersectionValue(ray)
                    if (t and t < nearest_t):
                        nearest_t = t
                        foundObject = obj
 
                rgb = self.color_background
                if (foundObject):
                        nearestPoint = ray.support + ray.direction.scalarmul(nearest_t)
                        diffuse, ref, refr = foundObject.diffuseReflectionRefraction(nearestPoint, self.lights)
                        
                        diffuse = [min(a*255, 255) for a in diffuse]
                        
                        rgb = self.color_mask % (int(diffuse[0]), int(diffuse[1]), int(diffuse[2]))
                
                x_pos =   x + self.width/2
                y_pos = -y + self.height/2
                
                self.image.put(rgb, to=(x_pos,y_pos))
 
        return self.image        
 
 
if __name__ == "__main__":
    
    root = Tk()
 
    rt = Raytracer( 350, 350)
    
    sphere1 = Sphere(Vector3(-80, 80, 150), 60)
    sphere1.setDiffuse(1.0, 0.0, 0.0)
    
    sphere2 = Sphere(Vector3(80, 80, 150), 60)
    sphere2.setDiffuse(0.0, 1.0, 0.0)
    
    sphere3 = Sphere(Vector3(-80, -80, 80), 60)
    sphere3.setDiffuse(0.0, 0.0, 1.0)
    
    sphere4 = Sphere(Vector3(80, -80, 80), 60)
    sphere4.setDiffuse(1.0, 1.0, 0.0)
    
    rt.addObject(sphere1)
    rt.addObject(sphere2)
    rt.addObject(sphere3)
    rt.addObject(sphere4)
    
    #plane1 = Plane(Vector3(0, 0, 400), Vector3(0, -1, 400),  Vector3(-1, 0, 400))
    plane1 = Plane(Vector3(0, -150, 0), Vector3(0, -150, 1),  Vector3(1, -150, 0))
    plane1.setDiffuse(1.0, 1.0, 1.0)
    plane1.checker = True
    rt.addObject(plane1)
    
    rt.addLight(Vector3(0,650, -650))
 
##     for i in range(10):
##         seed()
##         sphere = Sphere(Vector3(randrange(-200, 200), randrange(-200, 200), randrange(0, 500)), randrange(50, 60))
##         sphere.setDiffuse(randrange(100, 255), randrange(100, 255), randrange(100, 255))
##         rt.addObject(sphere)
    
    renderimage = rt.render()
    label = Label(root, image=renderimage)
    label.pack()
   
    root.mainloop()
     