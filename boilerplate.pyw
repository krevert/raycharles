from Tkinter import Tk, Canvas


class Raytracer(object):
    def __init__(self, canvas):
        self.canvas = canvas
        self.width = int(self.canvas.cget("width"))
        self.height = int(self.canvas.cget("height"))

        
    def render(self):
        
        rgb = '#FF0000'
        
        for y in xrange(self.height):
            for x in xrange(self.width):
                    if (x % 50 == 0):
                            self.canvas.create_line(x, y, x, y+1, fill=rgb)
                    if (y % 50 == 0):
                            self.canvas.create_line(x, y, x, y+1, fill=rgb)
                                
                    

            #self.canvas.update()


if __name__ == "__main__":
    
    root = Tk()
    canvas = Canvas(root, bg="white", width=640, heigh=480)
    canvas.pack()
    
    rt = Raytracer(canvas)
    rt.render()
    
    root.mainloop()
    
    