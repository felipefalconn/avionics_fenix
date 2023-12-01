from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile, Vec3
from direct.task import Task

loadPrcFile('settings.prc')

class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.rocket = loader.loadModel("./files/spacex_bfr_wip.glb")
        self.rocket.setPos(0, 150, -20)
        self.rocket.setHpr(0, -90, 180)
        self.rocket.reparentTo(render)

        self.rotation_speeds = [45, -30] 
        self.current_rotation_speed = 0  
        self.rotation_index = 0  

        self.taskMgr.add(self.updateRocket, "updateRocket")

    def updateRocket(self, task):
        if self.rotation_index < len(self.rotation_speeds):
            self.current_rotation_speed = self.rotation_speeds[self.rotation_index]
            self.rotation_index += 1

        dt = globalClock.getDt()


        # Setting rotate speed
        self.rocket.setH(self.rocket.getH() + self.current_rotation_speed * dt)

        return Task.cont

game = MyGame()
game.run()
