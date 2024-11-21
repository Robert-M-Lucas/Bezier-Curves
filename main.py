import pygame
from Handle import *

screen_size = (1000, 1000)
screen = pygame.display.set_mode(screen_size)


handles = [Handle((120, 120, 120), (150, 150)), Handle(pos=(170, 150)), Handle((120, 120, 120), (150, 170)), Handle(pos=(170, 170))]

lerp_handles = [LerpHandle(handles[0], handles[1]),
                LerpHandle(handles[1], handles[2]),
                LerpHandle(handles[2], handles[3])]

lerp2_handles = [LerpHandle(lerp_handles[0], lerp_handles[1], (0, 0, 255)),
                LerpHandle(lerp_handles[1], lerp_handles[2], (0, 0, 255))]

lerp3_handle = LerpHandle(lerp2_handles[0], lerp2_handles[1], (255, 255, 255))

pygame.font.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)
text1 = font.render("W : Show permanent line", True, (255, 0, 255))
text2 = font.render("S : Show derivation animation", True, (255, 0, 255))
text3 = font.render("+ : Increase derivation detail", True, (255, 0, 255))
text4 = font.render("- : Decrease derivation detail", True, (255, 0, 255))

doAnimation = False
sustainedLines = False

anim_progress = 0

points = []

increment = 0.0005

level = 4

held_handle = None
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and held_handle is None:
            for i, h in enumerate(handles):
                if h.pos[0] - h.r <= pygame.mouse.get_pos()[0] <= h.pos[0] + h.r and h.pos[1] - h.r <= \
                        pygame.mouse.get_pos()[1] <= h.pos[1] + h.r:
                    held_handle = i
        elif event.type == pygame.MOUSEBUTTONUP:
            held_handle = None

        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_s]:
                doAnimation = True
                sustainedLines = False
                anim_progress = 0
                points = []
            elif keys[pygame.K_w]:
                anim_progress = 0
                sustainedLines = not sustainedLines
                points = []
            elif keys[pygame.K_MINUS]:
                level -= 1
                if level < 0:
                    level = 0
            elif keys[pygame.K_EQUALS] or keys[pygame.K_PLUS]:
                level += 1
                if level > 4:
                    level = 4

    if held_handle is not None:
        if handles[held_handle].pos != pygame.mouse.get_pos():
            points = []
            handles[held_handle].pos = pygame.mouse.get_pos()

    loop = 1

    if sustainedLines:
        points = []
        loop = int(1 / increment)
        anim_progress = 0

    screen.fill((0, 0, 0))

    for f in range(loop):
        # Update
        if doAnimation or sustainedLines:
            anim_progress += increment
            if anim_progress > 1:
                doAnimation = False

            for l in lerp_handles:
                l.progress = anim_progress

            for l in lerp2_handles:
                l.progress = anim_progress

            lerp3_handle.progress = anim_progress

            points += [lerp3_handle.pos]

        # Handle lines
        pygame.draw.line(screen, (255, 0, 0), handles[0].pos, handles[1].pos)
        pygame.draw.line(screen, (255, 0, 0), handles[2].pos, handles[3].pos)

        if doAnimation or sustainedLines:
            # Extra handle line
            if not sustainedLines and level > 0:
                pygame.draw.line(screen, (120, 120, 120), handles[1].pos, handles[2].pos)

            # First level handles
            for l in lerp_handles:
                l.draw(screen, not sustainedLines and level > 0)

            # First level lines
            if not sustainedLines and level > 1:
                pygame.draw.line(screen, (0, 255, 0), lerp_handles[0].pos, lerp_handles[1].pos)
                pygame.draw.line(screen, (0, 255, 0), lerp_handles[1].pos, lerp_handles[2].pos)

            # Second level handles
            for l in lerp2_handles:
                l.draw(screen, not sustainedLines and level > 1)

            # Second level lines
            if not sustainedLines and level > 2:
                pygame.draw.line(screen, (0, 0, 255), lerp2_handles[0].pos, lerp2_handles[1].pos)

            # Final handle
            lerp3_handle.draw(screen, not sustainedLines and level > 2)

    # Draw points so far
    if sustainedLines or level > 3:
        for p in points:
            if not sustainedLines:
                pygame.draw.circle(screen, (120, 120, 120), p, 3)
            else:
                pygame.draw.circle(screen, (255, 255, 255), p, 3)

    for h in handles:
        h.draw(screen)

    screen.blit(text1, (0, 0))
    screen.blit(text2, (0, 30))
    screen.blit(text3, (0, 60))
    screen.blit(text4, (0, 90))

    pygame.display.update()

    clock.tick(120)
