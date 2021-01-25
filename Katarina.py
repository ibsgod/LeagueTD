import pygame

from Enemy import Enemy
from Info import Info


class Katarina(Enemy):
    def __init__(self, x, y, hp):
        super().__init__(x, y, name="Katarina", hp=hp, atk=3, atkspd=1, speed=15, atkrange=50, colour=(100, 0, 0))
        Info.enemies.append(self)
        self.stack = -1
        self.passName = "Sinister Steel"
        self.passDesc = "Every third attack slashes in a circle"

    def draw(self, screen):
        if len(self.atkAnim) > 0 and self.animStart is not None and self.animStart + self.atkspd * 1000 > Info.acTime:
            self.img = self.atkAnim[len(self.atkAnim) - int(
                (self.animStart + self.atkspd * 1000 - Info.acTime) / self.atkspd / 1000 * len(self.atkAnim)) - 1]
        else:
            self.img = self.idleimg
        if self.stack == 2 and Info.acTime - Info.atkTimers[self] < self.atkspd * 700 and not self.firing:
            surface1 = pygame.Surface((500, 500))
            surface1.set_colorkey((0, 0, 0))
            surface1.set_alpha(max(0, 255 - int(Info.acTime - Info.atkTimers[self]) + 500))
            pygame.draw.circle(surface1, (150, 0, 0), (250, 250), 200)
            screen.blit(surface1, (self.cx - 250, self.cy - 250))
        screen.blit(pygame.transform.flip(self.img, self.rot >= 90 or self.rot <= -90, False),
                    (int(self.x), int(self.y)))
        if Info.selected is self:
            pygame.draw.circle(screen, (255, 0, 0), (int(self.cx), int(self.cy)), self.atkrange + 50, 5)
        maxbar = pygame.Surface((self.size, 5))
        maxbar.set_alpha(80)
        maxbar.fill((0, 0, 0))
        screen.blit(maxbar, (self.x + (self.size - maxbar.get_width()) / 2, self.y - 15))
        pygame.draw.rect(screen, (min(255, int((self.maxhp - self.hp) * 255 / (self.maxhp))),
                                  max(0, int(255 - (self.maxhp - self.hp) * 255 / (self.maxhp))), 0), (
                             self.x + (self.size - maxbar.get_width()) / 2, self.y - 15,
                             max(0, maxbar.get_width() / self.maxhp * self.hp), 5))
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