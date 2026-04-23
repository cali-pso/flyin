from hubs import Hub
from connections import Connection
from map import Map

import os
from typing import Optional

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"


class Visualiser:
    SPACE = 200
    OFFSET = 400
    import pygame

    def __init__(self, map: Map, paths: list[list[Hub | Connection]]) -> None:
        self.pygame.init()
        self.screen = self.pygame.display.set_mode((1920, 1080))
        self.clock = self.pygame.time.Clock()
        self.running = True

        self.map = map
        self.paths = paths
        self.get_centered_map()
        self.rainbow = self.pygame.image.load("rainbow.png").convert_alpha()
        self.turns = max([len(h) for h in self.paths])
        self.paths_by_turn: dict[int, list[Optional[Hub | Connection]]] = {
            i: [(h[i] if len(h) > i else None) for h in self.paths]
            for i in range(self.turns)
        }
        self.arrived = 0
        self.current_turn = 0

        self.small_font = self.pygame.font.SysFont("Arial", 12, bold=True)
        self.big_font = self.pygame.font.SysFont("Arial", 24, bold=True)
        self.paused = False

    def run(self) -> None:

        last_update = 0
        anim_time = 1250
        turn_time = 500

        while self.running and self.current_turn < self.turns:
            # 1. Calculate time logic
            current_time = self.pygame.time.get_ticks()
            time_elapsed = current_time - last_update

            # Clamp progress to a maximum of 1.0 (100%)
            if time_elapsed >= turn_time:
                progress = min(1.0, (time_elapsed - turn_time) / anim_time)
            else:
                progress = 0

            # 2. Event Handling
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    self.running = False

            # 3. Turn Progression Logic
            if progress >= 1.0:
                if time_elapsed >= anim_time:
                    self.current_turn += 1
                    if self.current_turn >= self.turns:
                        break
                    last_update = current_time
                    progress = 0

            self.screen.fill((15, 15, 15))

            self.print_turn()
            self.print_connections()
            self.print_hubs()
            self.per_frame_animation(progress)

            self.pygame.display.flip()

            self.clock.tick(30)

    def print_turn(self) -> None:
        text = self.big_font.render(
            f"{self.current_turn}/{self.turns - 1}", True, "white"
        )
        text_pos = 60, 40
        self.screen.blit(text, text_pos)

    def print_connections(self) -> None:
        for connec in self.map.connections:
            start_pos = self.get_drone_px(connec.start_node)
            end_pos = self.get_drone_px(connec.end_node)
            self.pygame.draw.line(
                self.screen,
                (150, 150, 150),
                start_pos,
                end_pos,
                int(self.space / 10),
            )

    def print_hubs(self) -> None:
        for hub in self.map.hubs:
            pos = self.get_drone_px(hub)
            if hub.color == "rainbow":
                self.rainbow = self.pygame.transform.scale(
                    self.rainbow, (self.space * 0.45, self.space * 0.45)
                )
                image_rect = self.rainbow.get_rect(center=pos)
                self.screen.blit(self.rainbow, image_rect)
            else:
                self.pygame.draw.circle(
                    self.screen, hub.color, pos, int(self.space / 4)
                )
            if hub.zone or hub.hub_type in ["start_hub", "end_hub"]:
                info = hub.zone if hub.zone else hub.hub_type
                text = self.small_font.render(f"{info}", True, "white")
                text_pos = (
                    pos[0] + int(self.space / 4),
                    pos[1] - int(self.space / 4),
                )
                self.screen.blit(text, text_pos)

            if hub.hub_type != "end_hub":
                current_usage = len(
                    [
                        h
                        for h in self.paths_by_turn[self.current_turn]
                        if h == hub
                    ]
                )
            else:
                current_usage = len(
                    [
                        h
                        for h in self.paths_by_turn[self.current_turn]
                        if not h or h == hub
                    ]
                )
            if current_usage > 0:
                text = self.small_font.render(
                    f"{current_usage}/{hub.max_drones}", True, "white"
                )
                text_pos = (
                    pos[0] - int(self.space / 4),
                    pos[1] - int(self.space / 4),
                )
                self.screen.blit(text, text_pos)

    def per_frame_animation(self, progress: float) -> None:
        """Calculates LERP for every drone and draws them."""
        for path in self.paths:
            # Prevent IndexError by capping the indices
            start_index = min(self.current_turn, len(path) - 1)
            next_index = min(self.current_turn + 1, len(path) - 1)

            start_loc = path[start_index]
            end_loc = path[next_index]

            # Ensuring we don't try to get positions of None
            if start_loc and end_loc:
                start_pos = self.get_drone_px(start_loc)
                end_pos = self.get_drone_px(end_loc)

                # Applying the Linear Interpolation formula
                current_x = (
                    start_pos[0] + (end_pos[0] - start_pos[0]) * progress
                )
                current_y = (
                    start_pos[1] + (end_pos[1] - start_pos[1]) * progress
                )
                current_pos = (current_x, current_y)

                self.pygame.draw.circle(
                    self.screen, "white", current_pos, int(self.space / 7)
                )
                self.pygame.draw.circle(
                    self.screen, "black", current_pos, int(self.space / 9)
                )

    def print_drones(self) -> None:
        for drone in self.paths_by_turn[self.current_turn]:
            if drone:
                self.pygame.draw.circle(
                    self.screen,
                    "white",
                    self.get_drone_px(drone),
                    int(self.space / 7),
                )
                self.pygame.draw.circle(
                    self.screen,
                    "black",
                    self.get_drone_px(drone),
                    int(self.space / 9),
                )

    def get_drone_px(self, loc: Hub | Connection) -> tuple[float, float]:

        if isinstance(loc, Hub):
            pos = (
                loc.x * self.space + self.offset_x,
                loc.y * self.space + self.offset_y,
            )
        elif isinstance(loc, Connection):
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
