import pygame
import math
import random
import sys


class SetUpSettings:
    map_coord = set()
    height = 800
    width = 800
    # width = 1080
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 30)
    half_height = height / 2
    fps = 30
    world_map = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 0, 1, 0, 1, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]

    def __init__(self):
        self.cell_size = int(self.height / len(self.world_map))
        self.rect_len_x = self.width / len(self.world_map[0])
        self.rect_len_y = self.height / len(self.world_map)
        self.font = pygame.font.SysFont('Arial', 30)
        self.__put_coord_in_set()
        self.collision_list = []
        for j, row in enumerate(self.world_map):
            for i, char in enumerate(row):
                if int(char):
                    self.collision_list.append(pygame.Rect(i * self.cell_size, j*self.cell_size, self.cell_size, self.cell_size))

    @classmethod
    def __put_coord_in_set(cls):
        for row_count, row_value in enumerate(cls.world_map):
            for column_count, column_value in enumerate(row_value):
                if column_value:
                    cls.map_coord.add(
                        (cls.width / len(row_value) * column_count, cls.height / len(cls.world_map) * row_count))

    def draw_2d(self):
        for coord in einstellungen.map_coord:
            pygame.draw.polygon(screen, color.grey, (coord, (coord[0] + self.cell_size, coord[1]),
                                                     (coord[0] + self.cell_size, coord[1] + self.cell_size),
                                                     (coord[0], coord[1] + self.cell_size)), 0)

    @staticmethod
    def event_check():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()


class CharacterSettings:
    def __init__(self):
        # movement settings
        self.speed = einstellungen.width*einstellungen.height//130000
        self.x = 500
        self.y = 150
        self.z = 0
        self.angle = 0
        self.jump = False
        jump_list = [i for i in range(0, 100, 9)]
        self.jump_list = jump_list + jump_list[::-1]
        self.jump_index = 0

        self.previous_mouse_x, self.previous_mouse_y = pygame.mouse.get_pos()

        # ray casting settings
        self.range_of_vision = math.pi / 8 * 3.5
        self.half_range_of_vision = self.range_of_vision / 2
        self.rays_count = einstellungen.width
        self.delta_angle_between_rays = self.range_of_vision / self.rays_count
        self.depth_of_vision = 700
        self.scale = einstellungen.width // self.rays_count
        self.dist = self.rays_count / (2 * math.tan(self.range_of_vision / 2))
        self.coefficient_of_scale = 2 * self.dist * einstellungen.cell_size

        self.side = 10
        self.rectangle = pygame.Rect(*self.get_pos(), self.side, self.side)

    def movement(self):
        def detect_collision(dx, dy):
            next_rect = self.rectangle.copy()
            next_rect.move_ip(dx, dy)
            hit_indexes = next_rect.collidelistall(einstellungen.collision_list)

            if len(hit_indexes):
                delta_x, delta_y = 0, 0
                for hit_index in hit_indexes:
                    hit_rect = einstellungen.collision_list[hit_index]
                    if dx > 0:
                        delta_x += next_rect.right - hit_rect.left
                    else:
                        delta_x += hit_rect.right - next_rect.left
                    if dy > 0:
                        delta_y += next_rect.bottom - hit_rect.top
                    else:
                        delta_y += hit_rect.bottom - next_rect.top

                if abs(delta_x - delta_y) < 10:
                    dx, dy = 0, 0
                elif delta_x > delta_y:
                    dy = 0
                elif delta_y > delta_x:
                    dx = 0
            self.x += dx
            self.y += dy

        # settings
        angle = 100 * 10 ** -4
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        key = pygame.key.get_pressed()
        freeze_coord = pygame.mouse.get_pressed()[2]
        if not freeze_coord:
            current_mouse_x, current_mouse_y = pygame.mouse.get_pos()
        else:
            self.previous_mouse_x, self.previous_mouse_y = pygame.mouse.get_pos()
        speed = self.speed*3 if pygame.mouse.get_pressed()[1] else self.speed

        # if statements
        if key[pygame.K_w]:
            dx = speed * cos_a
            dy = speed * sin_a
            detect_collision(dx, dy)
        if key[pygame.K_s]:
            dx = -speed * cos_a
            dy = -speed * sin_a
            detect_collision(dx, dy)
        if key[pygame.K_a]:
            dx = speed * sin_a
            dy = -speed * cos_a
            detect_collision(dx, dy)
        if key[pygame.K_d]:
            dx = -speed * sin_a
            dy = speed * cos_a
            detect_collision(dx, dy)
        if key[pygame.K_SPACE] and not self.jump:
            self.jump = True
            self.z += self.jump_list[self.jump_index]
        if not freeze_coord:
            if self.previous_mouse_x-current_mouse_x != 0:
                self.angle -= angle*(self.previous_mouse_x-current_mouse_x)
            self.previous_mouse_x, self.previous_mouse_y = current_mouse_x, current_mouse_y

    def get_pos(self):
        return (self.x, self.y)

    def view_2d(self):
        ray_angle = self.angle - self.range_of_vision / 2
        delta_angle_between_rays = self.range_of_vision / self.rays_count
        for ray in range(0, self.rays_count):
            prev_coord = self.get_pos()
            for ray_depth in range(self.depth_of_vision):
                line_x = self.x + ray_depth * math.cos(ray_angle)
                line_y = self.y + ray_depth * math.sin(ray_angle)
                if (float(line_x // einstellungen.cell_size * einstellungen.cell_size),
                    float(line_y // einstellungen.cell_size *
                          einstellungen.cell_size)) in einstellungen.map_coord:
                    pygame.draw.line(screen, color.light_grey, self.get_pos(), prev_coord)
                    break
                prev_coord = (line_x, line_y)
            else:
                pygame.draw.line(screen, color.light_grey, self.get_pos(),
                                 (self.x + self.depth_of_vision * math.cos(ray_angle),
                                  self.y + self.depth_of_vision * math.sin(ray_angle)))
            ray_angle += delta_angle_between_rays

    def ray_casting(self):
        def optimization_hack(a, b):
            return (a // einstellungen.cell_size) * einstellungen.cell_size, (
                    b // einstellungen.cell_size) * einstellungen.cell_size

        ox, oy = self.get_pos()
        xm, ym = optimization_hack(ox, oy)
        cur_angle = self.angle - self.half_range_of_vision
        for ray in range(self.rays_count):
            sin_a = math.sin(cur_angle)
            cos_a = math.cos(cur_angle)
            sin_a = sin_a if sin_a else 1*10**-8
            cos_a = cos_a if cos_a else 1*10**-8

            # intersections
            # verticals intersection
            x, dx = (xm + einstellungen.cell_size, 1) if cos_a >= 0 else (xm, -1)
            for i in range(0, einstellungen.width, einstellungen.cell_size):
                depth_v = (x - ox) / cos_a
                y_vertical = oy + depth_v * sin_a
                if optimization_hack(x + dx, y_vertical) in einstellungen.map_coord:
                    break
                x += dx * einstellungen.cell_size

            # horizontals intersection
            y, dy = (ym + einstellungen.cell_size, 1) if sin_a >= 0 else (ym, -1)
            for i in range(0, einstellungen.height, einstellungen.cell_size):
                depth_h = (y - oy) / sin_a
                x_horizontal = ox + depth_h * cos_a
                if optimization_hack(x_horizontal, y + dy) in einstellungen.map_coord:
                    break
                y += dy * einstellungen.cell_size

            # projection
            depth = depth_v if depth_v < depth_h else depth_h
            depth *= math.cos(self.angle - cur_angle)
            depth = max(depth, 1*10**-6)
            proj_height = min(int(self.coefficient_of_scale / depth), 2*einstellungen.height)
            c = 255 / (1 + depth * depth * 2*10**-5)
            color_inner = (c, c // 1.5, c // 1.5)
            pygame.draw.rect(screen, color_inner,
                             (ray * self.scale,
                              einstellungen.half_height - proj_height // 2 + self.jump_list[self.jump_index],
                              self.scale, proj_height + self.jump_list[self.jump_index]/100))
            cur_angle += self.delta_angle_between_rays
        if self.jump:
            self.jump_index += 1
            if self.jump_index == len(self.jump_list):
                self.jump = False
                self.jump_index = 0


class ColorSettings:
    def __init__(self):
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.sky_blue = (135, 206, 235)
        self.grey = (125, 125, 125)
        self.light_grey = (169, 169, 169)
        self.yellow_sun = (240, 230, 140)
        self.brown = (139, 69, 19)


pygame.init()

einstellungen = SetUpSettings()
character = CharacterSettings()
color = ColorSettings()

screen = pygame.display.set_mode((einstellungen.width, einstellungen.height))
clock = pygame.time.Clock()

while True:
    einstellungen.event_check()

    screen.fill(color.black)
    pygame.draw.rect(screen, color.sky_blue, (0, 0, einstellungen.width, einstellungen.half_height+50))
    # pygame.draw.rect(screen, color.brown, (0, einstellungen.half_height+50, einstellungen.width, einstellungen.height))

    character.movement()
    character.ray_casting()

    # einstellungen.draw_2d()
    # pygame.draw.circle(screen, color.white, character.get_pos(), 10, 0)
    # character.view_2d()
    # einstellungen.draw_2d()

    screen.blit(einstellungen.font.render(f'{clock.get_fps()}'[:6], False, color.white), (0, 0))
    clock.tick(einstellungen.fps)
    pygame.display.update()
