from hubs import Hub
from connections import Connection
from map import Map

import pygame


class Visualiser:
    SPACE = 200
    OFFSET = 400

    def __init__(self, map: Map, paths: list[list[Hub]]) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080))
        self.clock = pygame.time.Clock()
        self.running = True

        self.map = map
        self.paths = paths
        self.get_centered_map()

    def run(self) -> None:

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill("black")

            for connec in self.map.connections:
                start_pos = (
                    connec.start_node.x * self.space + self.offset_x,
                    connec.start_node.y * self.space + self.offset_y,
                )
                end_pos = (
                    connec.end_node.x * self.space + self.offset_x,
                    connec.end_node.y * self.space + self.offset_y,
                )
                pygame.draw.line(
                    self.screen,
                    "white",
                    start_pos,
                    end_pos,
                    int(self.space / 10),
                )

            for hub in self.map.hubs:
                pos = (
                    hub.x * self.space + self.offset_x,
                    hub.y * self.space + self.offset_y,
                )
                pygame.draw.circle(
                    self.screen, hub.color, pos, int(self.space / 4)
                )

            self.per_frame_animation()

            pygame.display.flip()
            self.clock.tick(10)

    def per_frame_animation(self) -> None:
        for path in self.paths:
            for hub in path:
                pygame.draw.circle(
                    self.screen,
                    "purple",
                    self.get_drone_px(hub),
                    int(self.space / 8),
                )

    def get_drone_px(self, loc: Hub | Connection) -> int:

        if isinstance(loc, Hub):
            pos = (
                loc.x * self.space + self.offset_x,
                loc.y * self.space + self.offset_y,
            )
        else:
            start_x, start_y = self.get_drone_px(loc.start_node)
            end_x, end_y = self.get_drone_px(loc.end_node)
            pos = ((start_x + end_x) / 2, (start_y + end_y) / 2)
        return pos

    def get_centered_map(self) -> None:
        xs = [i.x for i in self.map.hubs]
        ys = [i.y for i in self.map.hubs]
        min_x, max_x, min_y, max_y = min(xs), max(xs), min(ys), max(ys)
        screen_width, screen_height = self.screen.get_size()

        delta_x = max(1, max_x - min_x)
        delta_y = max(1, max_y - min_y)
        available_width = screen_width * 0.8
        available_height = screen_height * 0.8
        self.space = min(available_width / delta_x, available_height / delta_y)

        map_width = (max_x - min_x) * self.space
        map_height = (max_y - min_y) * self.space
        self.offset_x = (screen_width - map_width) // 2 - (min_x * self.space)
        self.offset_y = (screen_height - map_height) // 2 - (
            min_y * self.space
        )
