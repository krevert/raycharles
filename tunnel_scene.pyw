from Tkinter import Tk
from step_3 import *


if __name__ == "__main__":
   
    root = Tk()

    rt = Raytracer( 1000, 1000)
   
    sphere1 = Sphere(Vector3(-350, 350, 350), 160)
    sphere1.setDiffuse(1.0, 0.0, 0.0)
   
    sphere2 = Sphere(Vector3(350, 350, 350), 160)
    sphere2.setDiffuse(0.0,1.0, 0.0)
   
    sphere3 = Sphere(Vector3(-350, -350, 350), 160)
    sphere3.setDiffuse(0.0, 0.0, 1.0)
   
    sphere4 = Sphere(Vector3(350, -350, 350), 160)
    sphere4.setDiffuse(1.0, 1.0, 0.0)
    
    rt.addObject(sphere1)
    rt.addObject(sphere2)
    rt.addObject(sphere3)
    rt.addObject(sphere4)
   
    #floor
    plane1 = Plane(Vector3(0, -350, 0), Vector3(0, -350, 1),  Vector3(1, -350, 0))
    plane1.setDiffuse(1.0, 1.0, 1.0)
    plane1.checker = True
    rt.addObject(plane1)
   
    #ceiling
    plane2 = Plane(Vector3(0, 350, 0), Vector3(0, 350, 1),  Vector3(-1, 350, 0))
    plane2.setDiffuse(1.0, 1.0, 1.0)
    plane2.checker = True
    rt.addObject(plane2)
   
    #back
    plane3 = Plane(Vector3(0, 0, 5000), Vector3(0, 1, 5000),  Vector3(1, 0, 5000))
    plane3.setDiffuse(1.0, 1.0, 1.0)
    plane3.checker = True
    rt.addObject(plane3)

    #left wall
    plane4 = Plane(Vector3(-500, 0, 0), Vector3(-500, 1, 0),  Vector3(-500, 0, 1))
    plane4.setDiffuse(0.0, 0.0, 0.0)
    plane4.checker = True
    rt.addObject(plane4)
   
    #right wall
    plane5 = Plane(Vector3(500, 0, 0), Vector3(500, 1, 0),  Vector3(500, 0, -1))
    plane5.setDiffuse(0.0, 0.0, 0.0)
    plane5.checker = True
    rt.addObject(plane5)

    rt.addLight(Vector3(0,0, -650))
    rt.addLight(Vector3(0, 0, 4500))
   
##     for i in range(5):
##         seed()
##         sphere = Sphere(Vector3(randrange(-300, 300), randrange(-350, 50), randrange(0, 500)), randrange(50, 200))
##         sphere.setDiffuse(randrange(100, 255), randrange(100, 255), randrange(100, 255))
##         rt.addObject(sphere)
   
    
   
    renderimage = rt.render()
    label = Label(root, image=renderimage)
    label.pack()
  
    root.mainloop() 