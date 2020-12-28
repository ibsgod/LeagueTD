import pygame

from Info import Info


class Enemy:
    def __init__(self, x, y, name, hp, atk, atkspd, speed, img):
        self.x = x
        self.y = y
        self.name = name
        self.hp = hp
        self.maxhp = hp
        self.atk = atk
        self.atkspd = atkspd
        self.speed = speed
        self.img = pygame.image.load(img)
        self.path = 1
        self.width = 60
        self.height = 60
        self.size = 60
        self.cx = self.x + self.width/2
        self.cy = self.y + self.height/2
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.flip = False
        self.slow = (0, 0)

    def draw(self, screen):
        # screen.blit(pygame.transform.flip(self.img, self.flip, False), (int(self.x), int(self.y)))
        maxbar = pygame.Surface((self.size, 5))
        maxbar.set_alpha(80)
        maxbar.fill((0, 0, 0))
        screen.blit(maxbar, (self.x + (self.size - maxbar.get_width()) / 2, self.y - 15))
        pygame.draw.rect(screen, (min(255, int((self.maxhp - self.hp) * 255 / (self.maxhp - 1))),
                                  max(0, int(255 - (self.maxhp - self.hp) * 255 / (self.maxhp - 1))), 0), (
                         self.x + (self.size - maxbar.get_width()) / 2, self.y - 15,
                         max(0, maxbar.get_width() / self.maxhp * self.hp), 5))

        pygame.draw.rect(screen, (150, 0, 150), (int(self.x), int(self.y), self.width, self.height))

    def tick(self, mousePos, click, pause=False):
        if not pause:
            self.move()
        if self.hitbox.collidepoint(mousePos) and Info.summoning is None:
            if click:
                Info.selected = self
                return 2
            return 1
        return

    def move(self):
        newspeed = self.speed
        if self.slow[1] > pygame.time.get_ticks():
            newspeed *= self.slow[0]
        if self.path < len(Info.enemypath):
            if self.cx != Info.enemypath[self.path][0]:
                if abs(Info.enemypath[self.path][0] - (self.cx)) > newspeed:
                    self.x += newspeed * (Info.enemypath[self.path][0] - (self.cx)) / abs(Info.enemypath[self.path][0] - (self.cx))
                else:
                    self.x += Info.enemypath[self.path][0] - (self.cx)
            if self.cy != Info.enemypath[self.path][1]:
                if abs(Info.enemypath[self.path][1] - (self.cy)) > newspeed:
                    self.y += newspeed * (Info.enemypath[self.path][1] - (self.cy)) / abs(Info.enemypath[self.path][1] - (self.cy))
                else:
                    self.y += Info.enemypath[self.path][1] - (self.cy)
            if self.cx == Info.enemypath[self.path][0] and self.cy == Info.enemypath[self.path][1]:
                self.path += 1
        self.cx = self.x + self.width / 2
        self.cy = self.y + self.height / 2
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def takeDamage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            Info.enemies.remove(self)
            if Info.selected is self:
                Info.selected = None
            for i in Info.champions:
                if self is i.target:
                    i.target = None
