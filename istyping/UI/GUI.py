#referenced this for classes: https://www.w3schools.com/python/python_classes.asp
class Button:
    def __init__(self, xPos, yPos, width, height, visual, color):
        self.xPos = xPos
        self.yPos = yPos
        self.width = width
        self.height = height
        self.visual = visual
        self.color = color
    
    def checkMousePress(self, mouseX, mouseY):
        if mouseX > self.xPos and mouseX < self.xPos + self.width and mouseY > self.yPos and mouseY < self.yPos + self.height:
            print("clicked")