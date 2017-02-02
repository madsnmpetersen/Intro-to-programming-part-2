from swampy.TurtleWorld import *

class FractalWorld(TurtleWorld):
  def __init__(self,interactive=False,width=400,height=400,delay=0.5):
    World.__init__(self)
    self.title('TurtleWorld')

    # the interpreter executes user-provided code
    g = globals()
    g['world'] = self
    self.make_interpreter(g)

    # make the GUI
    self.setup(width,height,delay)
    if interactive:
      self.setup_interactive()
  def setup(self, width, height, delay):
    """Create the GUI."""

    # canvas width and height and delay
    self.ca_width = width
    self.ca_height = height
    self.delay = delay

    self.row()
    self.canvas = self.ca(width=self.ca_width,height=self.ca_height,bg='white')

class Fractal(Turtle):
  def __init__(self, world=None, draw=True):
    Turtle.__init__(self, world)
    if not draw:
      self.draw = lambda: None

def fd(self,dist=1, width=1, color=None):
  """Moves the turtle foward by the given distance."""
  x, y = self.x, self.y
  p1 = [x, y]
  p2 = self.polar(x, y, dist, self.heading)
  self.x, self.y = p2

  # if the pen is down, draw a line
  if self.pen:
    if not color:
      color = self.pen_color
    self.world.canvas.line([p1, p2], fill=color, width=width)
  self.redraw()
