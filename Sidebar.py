import pygame

from Button import Button
from Champion import Champion
from Info import Info


class Sidebar:
    def draw(self, screen, selected, hover=False):
        pygame.draw.rect(screen, (0, 0, 200), (1050, 200, 250, 450))
        if selected is None:
            return
        nameLbl = pygame.font.SysFont("Microsoft Yahei UI Light", 40).render(selected.name, 1, (255, 255, 255))
        screen.blit(nameLbl, (1175 - nameLbl.get_width()/2, 210))
        maxbar = pygame.Surface((200, 20))
        maxbar.set_alpha(80)
        maxbar.fill((0, 0, 0))
        screen.blit(maxbar, (1075, 250))
        pygame.draw.rect(screen, (min(255, int((selected.maxhp - selected.hp) * 255 / (selected.maxhp - 1))),
                                  max(0, int(255 - (selected.maxhp - selected.hp) * 255 / (selected.maxhp - 1))), 0), (
                             1075, 250, max(0, maxbar.get_width() / selected.maxhp * selected.hp), 20))
        hpLbl = pygame.font.SysFont("Microsoft Yahei UI Light", 20).render(str(selected.hp) + " / " + str(selected.maxhp), 1, (255, 255, 255))
        screen.blit(hpLbl, ((1175 - hpLbl.get_width()/2, 253)))
        if hasattr(selected, "mana"):
            screen.blit(maxbar, (1075, 270))
            pygame.draw.rect(screen, (0, 100, 200), (1075, 270, max(0, maxbar.get_width() / selected.maxmana * selected.mana), 20))
            manaLbl = pygame.font.SysFont("Microsoft Yahei UI Light", 20).render(
                str(selected.mana) + " / " + str(selected.maxmana), 1, (255, 255, 255))
            screen.blit(manaLbl, ((1175 - manaLbl.get_width() / 2, 273)))
        y = self.drawText(screen, "Attack: " + '{0:.3g}'.format(selected.atk), (255, 255, 255),
                          pygame.Rect(1065, 310, 220, 300), pygame.font.SysFont("Microsoft Yahei UI Light", 27))
        y = self.drawText(screen, "Attack speed: " + '{0:.3g}'.format(1/selected.atkspd), (255, 255, 255),
                          pygame.Rect(1065, y + 10, 220, 300), pygame.font.SysFont("Microsoft Yahei UI Light", 27))
        if hasattr(selected, "passDesc"):
            y = self.drawText(screen, selected.passName + " - Passive: " + selected.passDesc, (255, 255, 255),
                     pygame.Rect(1065, y + 10, 220, 300), pygame.font.SysFont("Microsoft Yahei UI Light", 27))
            y = self.drawText(screen, selected.actName + " - Active: " + selected.actDesc, (255, 255, 255),
                          pygame.Rect(1065, y + 10, 220, 300), pygame.font.SysFont("Microsoft Yahei UI Light", 27))
        if isinstance(selected, Champion) and not hover:
            setattr(Info.buttDict["use"].coll, "y", y + 20)
            setattr(Info.buttDict["sell"].coll, "y", Info.buttDict["use"].coll.height + y + 30)

    def drawText(self, surface, text, color, rect, font, aa=False, bkg=None):
        y = rect.top
        lineSpacing = -2

        # get the height of the font
        fontHeight = font.size("Tg")[1]

        while text:
            i = 1

            # determine if the row of text will be outside our area
            if y + fontHeight > rect.bottom:
                break

            # determine maximum width of line
            while font.size(text[:i])[0] < rect.width and i < len(text):
                i += 1

            # if we've wrapped the text, then adjust the wrap to the last word
            if i < len(text):
                i = text.rfind(" ", 0, i) + 1

            # render the line and blit it to the surface
            if bkg:
                image = font.render(text[:i], 1, color, bkg)
                image.set_colorkey(bkg)
            else:
                image = font.render(text[:i], aa, color)

            surface.blit(image, (rect.left, y))
            y += fontHeight + lineSpacing

            # remove the text we just blitted
            text = text[i:]

        return y
