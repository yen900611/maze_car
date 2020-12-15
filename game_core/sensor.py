import Box2D

class Sensor():
    def __init__(self, world, position):
        self.body = world.CreateDynamicBody(position=position)
        ball = self.body.CreateCircleFixture(radius=0.1)
        pass

    def update(self):
        pass