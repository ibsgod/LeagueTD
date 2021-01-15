
from Enemy import Enemy
from Info import Info


class Katarina(Enemy):
    def __init__(self, x, y, hp):
        super().__init__(x, y, name="Katarina", hp=hp, atk=3, atkspd=1, speed=15, atkrange=50, colour=(100, 0, 0))
        Info.enemies.append(self)
        self.stack = 0
        self.passName = "Sinister Steel"
        self.passDesc = "Every third attack slashes in a circle"

    def fire(self):
        if self.stack == 2:
            for i in Info.champions:
                if i.checkRange((self.cx, self.cy), 200, i.hitbox):
                    i.takeDamage(self.atk)
            self.stack = 0
        else:
            self.target.takeDamage(self.atk + self.stack)
            self.stack += 1

    def checkRange(self, pos, rad, rect):
        distx = abs(pos[0] - rect.x - rect.width/2)
        disty = abs(pos[1] - rect.y - rect.height/2)
        if distx > (rect.width / 2 + rad):
            return False
        if disty > (rect.height / 2 + rad):
            return False
        if distx <= (rect.width / 2):
            return True
        if disty <= (rect.height / 2):
            return True
        cornerDistance_sq = (distx - rect.width / 2) ** 2 + (disty - rect.height / 2) ** 2
        return (cornerDistance_sq <= (rad ** 2))