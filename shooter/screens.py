from __future__ import annotations

import random

from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Line, Rectangle, RoundedRectangle
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget


TEXT_PRIMARY = (0.9, 0.96, 1.0, 1)
TEXT_MUTED = (0.62, 0.78, 0.94, 1)
CYAN = (0.31, 0.85, 1.0, 1)
CYAN_SOFT = (0.21, 0.53, 0.9, 0.78)
PANEL_FILL = (0.05, 0.1, 0.2, 0.78)
SHIP_SPRITE = [
    "..11....11..",
    ".1221111221.",
    "122221222221",
    "122333333221",
    "112233332211",
    "..12333321..",
    "..11211211..",
    "...4....4...",
]
FIGHTER_SPRITE = [
    "..55..",
    ".5665.",
    "566665",
    "556655",
    ".5445.",
    "..55..",
]
METEOR_SPRITE = [
    ".777..",
    "777787",
    "778887",
    ".78887",
    ".77877",
    "..777.",
]
SHIP_PALETTE = {
    "1": (0.76, 0.94, 1.0, 1),
    "2": (0.32, 0.76, 1.0, 1),
    "3": (0.13, 0.28, 0.58, 1),
    "4": (1.0, 0.7, 0.2, 1),
}
FIGHTER_PALETTE = {
    "4": (1.0, 0.72, 0.28, 1),
    "5": (1.0, 0.42, 0.52, 1),
    "6": (0.58, 0.12, 0.22, 1),
}
METEOR_PALETTE = {
    "7": (0.72, 0.42, 0.22, 1),
    "8": (0.46, 0.24, 0.14, 1),
}


def action_button(text):
    return Button(
        text=text,
        size_hint_y=None,
        height=60,
        bold=True,
        color=TEXT_PRIMARY,
        background_normal="",
        background_down="",
        background_color=(0.12, 0.24, 0.4, 0.96),
    )


def draw_pixel_sprite(x, y, width, height, sprite_rows, palette, glow_color=None):
    columns = max(len(row) for row in sprite_rows)
    rows = len(sprite_rows)
    pixel_width = width / columns
    pixel_height = height / rows

    if glow_color is not None:
        Color(*glow_color)
        Rectangle(
            pos=(x - pixel_width * 0.6, y - pixel_height * 0.6),
            size=(width + pixel_width * 1.2, height + pixel_height * 1.2),
        )

    for row_index, row in enumerate(sprite_rows):
        for col_index, code in enumerate(row):
            if code == ".":
                continue
            color = palette.get(code)
            if color is None:
                continue
            Color(*color)
            Rectangle(
                pos=(x + col_index * pixel_width, y + (rows - row_index - 1) * pixel_height),
                size=(pixel_width, pixel_height),
            )


class SpaceBackground(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        rng = random.Random(17)
        self.stars = [
            (rng.random(), rng.random(), rng.uniform(1.5, 4.8), rng.uniform(0.25, 0.95))
            for _ in range(90)
        ]
        self.spark_stars = [
            (rng.random(), rng.random(), rng.uniform(4.0, 7.0), rng.uniform(0.15, 0.4))
            for _ in range(12)
        ]
        self.bind(pos=self._redraw, size=self._redraw)
        self._redraw()

    def _redraw(self, *_args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.01, 0.015, 0.05, 1)
            Rectangle(pos=self.pos, size=self.size)

            Color(0.07, 0.11, 0.22, 0.9)
            Ellipse(
                pos=(self.x - self.width * 0.12, self.y + self.height * 0.58),
                size=(self.width * 0.72, self.height * 0.34),
            )
            Color(0.3, 0.1, 0.45, 0.28)
            Ellipse(
                pos=(self.x + self.width * 0.28, self.y + self.height * 0.42),
                size=(self.width * 0.74, self.height * 0.31),
            )
            Color(0.08, 0.4, 0.62, 0.18)
            Ellipse(
                pos=(self.x + self.width * 0.02, self.y + self.height * 0.12),
                size=(self.width * 0.82, self.height * 0.26),
            )

            planet_size = min(self.width, self.height) * 0.26
            planet_x = self.x + self.width * 0.7
            planet_y = self.y + self.height * 0.72
            Color(0.08, 0.18, 0.32, 1)
            Ellipse(pos=(planet_x, planet_y), size=(planet_size, planet_size))
            Color(0.23, 0.74, 1.0, 0.14)
            Ellipse(
                pos=(planet_x - planet_size * 0.14, planet_y - planet_size * 0.14),
                size=(planet_size * 1.28, planet_size * 1.28),
            )
            Color(0.12, 0.5, 0.82, 0.9)
            Line(
                ellipse=(planet_x - planet_size * 0.12, planet_y + planet_size * 0.1, planet_size * 1.24, planet_size * 0.42),
                width=1.2,
            )

            for star_x, star_y, star_size, star_alpha in self.stars:
                Color(0.86, 0.95, 1.0, star_alpha)
                Ellipse(
                    pos=(self.x + self.width * star_x, self.y + self.height * star_y),
                    size=(star_size, star_size),
                )

            for star_x, star_y, star_size, star_alpha in self.spark_stars:
                px = self.x + self.width * star_x
                py = self.y + self.height * star_y
                Color(0.52, 0.92, 1.0, star_alpha)
                Line(points=[px - star_size, py, px + star_size, py], width=1)
                Line(points=[px, py - star_size, px, py + star_size], width=1)


class ShipPreview(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self._redraw, size=self._redraw)
        self._redraw()

    def _redraw(self, *_args):
        self.canvas.clear()
        with self.canvas:
            ship_width = self.width * 0.55
            ship_height = self.height * 0.72
            draw_pixel_sprite(
                self.center_x - ship_width / 2,
                self.y + self.height * 0.1,
                ship_width,
                ship_height,
                SHIP_SPRITE,
                SHIP_PALETTE,
                glow_color=(0.12, 0.58, 0.92, 0.18),
            )


class BaseScreen(Screen):
    app = ObjectProperty(allownone=True)

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.add_widget(SpaceBackground())


class GlassCard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self._redraw, size=self._redraw)
        self._redraw()

    def _redraw(self, *_args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.02, 0.03, 0.08, 0.28)
            RoundedRectangle(pos=(self.x + 4, self.y - 4), size=self.size, radius=[26])
            Color(*PANEL_FILL)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[26])
            Color(*CYAN_SOFT)
            Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 26), width=1.2)


class LoginScreen(BaseScreen):
    status_text = StringProperty("Enter your pilot name to start.")

    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)
        root = BoxLayout(orientation="vertical", padding=24, spacing=18)
        root.add_widget(Label(text="SHOOTER", font_size="34sp", bold=True, color=TEXT_PRIMARY, size_hint_y=None, height=80))
        root.add_widget(Label(text="Auto-fire arcade shooter", font_size="18sp", color=TEXT_MUTED, size_hint_y=None, height=36))

        card = GlassCard(orientation="vertical", padding=20, spacing=16, size_hint=(1, None), height=320)
        self.username_input = TextInput(
            hint_text="Pilot name",
            multiline=False,
            size_hint_y=None,
            height=52,
            background_normal="",
            background_active="",
            background_color=(0.06, 0.12, 0.22, 0.96),
            foreground_color=TEXT_PRIMARY,
            hint_text_color=(0.48, 0.66, 0.84, 1),
            cursor_color=CYAN,
            padding=(16, 14, 16, 14),
        )
        card.add_widget(self.username_input)
        card.add_widget(Label(text="Ranking will save your best score locally.", color=TEXT_MUTED, size_hint_y=None, height=36))

        start_button = action_button("Continue")
        start_button.bind(on_release=self.handle_continue)
        card.add_widget(start_button)
        card.add_widget(Label(text="", size_hint_y=None, height=8))
        self.status_label = Label(text=self.status_text, color=CYAN, size_hint_y=None, height=48)
        card.add_widget(self.status_label)

        root.add_widget(card)
        root.add_widget(ShipPreview(size_hint=(1, 1)))
        self.add_widget(root)
        self.bind(status_text=self._sync_status)

    def _sync_status(self, *_args):
        self.status_label.text = self.status_text

    def on_pre_enter(self, *_args):
        self.username_input.text = self.app.current_player or ""

    def handle_continue(self, *_args):
        username = self.username_input.text.strip()
        if not username:
            self.status_text = "Pilot name is required."
            return

        self.app.login_player(username)
        self.status_text = "Enter your pilot name to start."


class MenuScreen(BaseScreen):
    welcome_text = StringProperty("Welcome, Pilot")
    stats_text = StringProperty("Best Score: 0\nGames Played: 0")

    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)
        root = BoxLayout(orientation="vertical", padding=24, spacing=18)
        root.add_widget(Label(text="Mission Bay", font_size="32sp", bold=True, color=TEXT_PRIMARY, size_hint_y=None, height=72))
        self.welcome_label = Label(text=self.welcome_text, font_size="20sp", color=CYAN, size_hint_y=None, height=44)
        self.stats_label = Label(text=self.stats_text, font_size="18sp", color=TEXT_MUTED, size_hint_y=None, height=84)
        root.add_widget(self.welcome_label)
        root.add_widget(self.stats_label)

        for title, handler in (
            ("Play Game", self.start_game),
            ("View Ranking", self.show_ranking),
            ("Switch Player", self.go_login),
        ):
            button = action_button(title)
            button.bind(on_release=handler)
            root.add_widget(button)

        root.add_widget(ShipPreview(size_hint=(1, 1)))
        self.add_widget(root)
        self.bind(welcome_text=self._sync_text)
        self.bind(stats_text=self._sync_text)

    def _sync_text(self, *_args):
        self.welcome_label.text = self.welcome_text
        self.stats_label.text = self.stats_text

    def on_pre_enter(self, *_args):
        username = self.app.current_player or "Pilot"
        record = self.app.storage.ensure_player(username)
        self.welcome_text = f"Welcome, {username}"
        self.stats_text = (
            f"Best Score: {record.get('best_score', 0)}\n"
            f"Games Played: {record.get('games_played', 0)}"
        )

    def start_game(self, *_args):
        self.manager.current = "game"

    def show_ranking(self, *_args):
        self.manager.current = "ranking"

    def go_login(self, *_args):
        self.manager.current = "login"


class GameScreen(BaseScreen):
    score = NumericProperty(0)
    ship_x = NumericProperty(0.5)
    status_text = StringProperty("Drag left or right to dodge and auto-fire.")

    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)
        self.bullets = []
        self.enemies = []
        self._loop_event = None
        self.fire_cooldown = 0.0
        self.spawn_cooldown = 0.0
        self.elapsed_time = 0.0
        self.game_over = False
        self.ship_destroyed = False
        self.explosion_particles = []
        self.explosion_timer = 0.0
        self.pending_finish = False
        rng = random.Random(44)
        self.playfield_stars = [
            (rng.random(), rng.random(), rng.uniform(1.2, 3.8), rng.uniform(0.18, 0.7))
            for _ in range(48)
        ]

        layout = BoxLayout(orientation="vertical", padding=20, spacing=16)
        self.score_label = Label(text="Score: 0", font_size="22sp", bold=True, color=TEXT_PRIMARY, size_hint_y=None, height=40)
        self.warning_label = Label(text="Hull: one hit destroyed", font_size="20sp", color=CYAN, size_hint_y=None, height=32)
        self.info_label = Label(text=self.status_text, font_size="16sp", color=TEXT_MUTED, size_hint_y=None, height=52)
        layout.add_widget(self.score_label)
        layout.add_widget(self.warning_label)
        layout.add_widget(self.info_label)

        self.playfield = Widget()
        self.playfield.bind(size=self._redraw_playfield, pos=self._redraw_playfield)
        layout.add_widget(self.playfield)

        controls = BoxLayout(size_hint_y=None, height=62, spacing=14)
        end_button = action_button("End Run")
        end_button.bind(on_release=self.end_run)
        menu_button = action_button("Menu")
        menu_button.bind(on_release=self.go_menu)
        controls.add_widget(end_button)
        controls.add_widget(menu_button)
        layout.add_widget(controls)

        self.add_widget(layout)
        self.bind(score=self._sync_labels, status_text=self._sync_labels)
        self._loop_event = Clock.schedule_interval(self._update_game, 1 / 60)

    def _sync_labels(self, *_args):
        self.score_label.text = f"Score: {self.score}"
        self.warning_label.text = "Ship destroyed" if self.ship_destroyed else "Hull: one hit destroyed"
        self.info_label.text = self.status_text

    def _redraw_playfield(self, *_args):
        self.playfield.canvas.clear()
        with self.playfield.canvas:
            Color(0.03, 0.04, 0.1, 0.96)
            Rectangle(pos=self.playfield.pos, size=self.playfield.size)
            Color(0.12, 0.32, 0.64, 0.08)
            RoundedRectangle(pos=(self.playfield.x, self.playfield.y), size=self.playfield.size, radius=[28])
            Color(0.22, 0.82, 1.0, 0.2)
            Line(rounded_rectangle=(self.playfield.x, self.playfield.y, self.playfield.width, self.playfield.height, 28), width=1.2)

            for index in range(1, 6):
                y = self.playfield.y + self.playfield.height * index / 6
                Color(0.2, 0.72, 1.0, 0.08)
                Line(points=[self.playfield.x + 12, y, self.playfield.right - 12, y], width=1)

            for star_x, star_y, star_size, star_alpha in self.playfield_stars:
                Color(0.84, 0.95, 1.0, star_alpha)
                Ellipse(
                    pos=(
                        self.playfield.x + self.playfield.width * star_x,
                        self.playfield.y + self.playfield.height * star_y,
                    ),
                    size=(star_size, star_size),
                )

            for bullet in self.bullets:
                Color(1.0, 0.94, 0.45, 1)
                Rectangle(pos=(bullet["x"], bullet["y"]), size=(bullet["w"], bullet["h"]))

            for enemy in self.enemies:
                if enemy["kind"] == "meteor":
                    draw_pixel_sprite(
                        enemy["x"],
                        enemy["y"],
                        enemy["w"],
                        enemy["h"],
                        METEOR_SPRITE,
                        METEOR_PALETTE,
                        glow_color=(0.32, 0.12, 0.04, 0.15),
                    )
                else:
                    draw_pixel_sprite(
                        enemy["x"],
                        enemy["y"],
                        enemy["w"],
                        enemy["h"],
                        FIGHTER_SPRITE,
                        FIGHTER_PALETTE,
                        glow_color=(0.4, 0.08, 0.12, 0.14),
                    )

            if not self.ship_destroyed:
                ship = self._ship_rect()
                draw_pixel_sprite(
                    ship["x"],
                    ship["y"],
                    ship["w"],
                    ship["h"],
                    SHIP_SPRITE,
                    SHIP_PALETTE,
                    glow_color=(0.12, 0.58, 0.92, 0.18),
                )

            for particle in self.explosion_particles:
                Color(*particle["color"][:3], particle["alpha"])
                Rectangle(pos=(particle["x"], particle["y"]), size=(particle["size"], particle["size"]))

    def _ship_rect(self):
        ship_width = self.playfield.width * 0.12
        ship_height = self.playfield.height * 0.1
        center_x = self.playfield.x + self.playfield.width * self.ship_x
        left = max(self.playfield.x, min(center_x - ship_width / 2, self.playfield.right - ship_width))
        bottom = self.playfield.y + self.playfield.height * 0.06
        return {"x": left, "y": bottom, "w": ship_width, "h": ship_height}

    def _move_ship_from_touch(self, touch):
        if self.playfield.collide_point(*touch.pos):
            if self.playfield.width > 0:
                relative = (touch.x - self.playfield.x) / self.playfield.width
                self.ship_x = min(1.0, max(0.0, relative))
                self._redraw_playfield()
            return True
        return False

    def on_touch_down(self, touch):
        if self._move_ship_from_touch(touch):
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self._move_ship_from_touch(touch):
            return True
        return super().on_touch_move(touch)

    def on_pre_enter(self, *_args):
        self.score = 0
        self.ship_x = 0.5
        self.status_text = "Drag left or right to dodge and auto-fire."
        self.bullets = []
        self.enemies = []
        self.fire_cooldown = 0.0
        self.spawn_cooldown = 0.35
        self.elapsed_time = 0.0
        self.game_over = False
        self.ship_destroyed = False
        self.explosion_particles = []
        self.explosion_timer = 0.0
        self.pending_finish = False
        self._sync_labels()
        self._redraw_playfield()

    def _update_game(self, dt):
        if not self.manager or self.manager.current != "game":
            return
        if self.pending_finish:
            self._update_explosion(dt)
            self._redraw_playfield()
            return
        if self.game_over:
            return
        if self.playfield.width <= 0 or self.playfield.height <= 0:
            return

        self.elapsed_time += dt
        self.fire_cooldown -= dt
        self.spawn_cooldown -= dt

        if self.fire_cooldown <= 0:
            self._spawn_bullet()
            self.fire_cooldown = 0.2

        if self.spawn_cooldown <= 0:
            self._spawn_enemy()
            self.spawn_cooldown = max(0.22, 0.75 - self.elapsed_time * 0.025)

        self._advance_bullets(dt)
        self._advance_enemies(dt)
        self._resolve_collisions()
        self._redraw_playfield()

    def _update_explosion(self, dt):
        if self.explosion_timer > 0:
            self.explosion_timer = max(0.0, self.explosion_timer - dt)

        updated_particles = []
        for particle in self.explosion_particles:
            particle["x"] += particle["dx"] * dt
            particle["y"] += particle["dy"] * dt
            particle["dy"] -= 25 * dt
            particle["alpha"] = max(0.0, particle["alpha"] - dt * 1.6)
            particle["size"] = max(2.0, particle["size"] - dt * 5)
            if particle["alpha"] > 0.03:
                updated_particles.append(particle)
        self.explosion_particles = updated_particles

        if self.explosion_timer <= 0 and not self.explosion_particles:
            self.pending_finish = False
            self.end_run()

    def _spawn_bullet(self):
        ship = self._ship_rect()
        bullet_width = max(6.0, self.playfield.width * 0.018)
        bullet_height = max(18.0, self.playfield.height * 0.04)
        self.bullets.append(
            {
                "x": ship["x"] + ship["w"] / 2 - bullet_width / 2,
                "y": ship["y"] + ship["h"],
                "w": bullet_width,
                "h": bullet_height,
                "speed": max(360.0, self.playfield.height * 1.12),
            }
        )

    def _spawn_enemy(self):
        kind = "meteor" if random.random() < 0.58 else "fighter"
        if kind == "meteor":
            width = self.playfield.width * random.uniform(0.1, 0.16)
            height = width
            speed = self.playfield.height * random.uniform(0.26, 0.39)
            reward = 8
        else:
            width = self.playfield.width * random.uniform(0.09, 0.13)
            height = self.playfield.height * random.uniform(0.07, 0.1)
            speed = self.playfield.height * random.uniform(0.32, 0.46)
            reward = 12

        min_x = self.playfield.x + 6
        max_x = max(min_x, self.playfield.right - width - 6)
        self.enemies.append(
            {
                "kind": kind,
                "x": random.uniform(min_x, max_x),
                "y": self.playfield.top + height,
                "w": width,
                "h": height,
                "speed": speed + self.elapsed_time * 3.2,
                "reward": reward,
            }
        )

    def _advance_bullets(self, dt):
        updated = []
        for bullet in self.bullets:
            bullet["y"] += bullet["speed"] * dt
            if bullet["y"] <= self.playfield.top:
                updated.append(bullet)
        self.bullets = updated

    def _advance_enemies(self, dt):
        updated = []
        for enemy in self.enemies:
            enemy["y"] -= enemy["speed"] * dt
            if enemy["y"] + enemy["h"] >= self.playfield.y - 4:
                updated.append(enemy)
        self.enemies = updated

    def _resolve_collisions(self):
        ship = self._ship_rect()
        remaining_bullets = []
        hit_enemy_ids = set()

        for bullet in self.bullets:
            bullet_hit = False
            for enemy in self.enemies:
                enemy_id = id(enemy)
                if enemy_id in hit_enemy_ids:
                    continue
                if self._rects_overlap(bullet, enemy):
                    bullet_hit = True
                    hit_enemy_ids.add(enemy_id)
                    self.score += enemy["reward"]
                    break
            if not bullet_hit:
                remaining_bullets.append(bullet)

        remaining_enemies = []
        for enemy in self.enemies:
            if id(enemy) in hit_enemy_ids:
                continue
            if self._rects_overlap(enemy, ship):
                self._trigger_game_over(ship)
                return
            remaining_enemies.append(enemy)

        self.bullets = remaining_bullets
        self.enemies = remaining_enemies

    @staticmethod
    def _rects_overlap(first, second):
        return (
            first["x"] < second["x"] + second["w"]
            and first["x"] + first["w"] > second["x"]
            and first["y"] < second["y"] + second["h"]
            and first["y"] + first["h"] > second["y"]
        )

    def _trigger_game_over(self, ship):
        self.game_over = True
        self.ship_destroyed = True
        self.pending_finish = True
        self.explosion_timer = 0.9
        self.status_text = "Direct hit. Ship destroyed."
        self.bullets = []
        self.enemies = []
        self.explosion_particles = self._create_explosion(ship)
        self._sync_labels()

    def _create_explosion(self, ship):
        particles = []
        center_x = ship["x"] + ship["w"] / 2
        center_y = ship["y"] + ship["h"] / 2
        colors = [
            (1.0, 0.92, 0.45, 1),
            (1.0, 0.62, 0.18, 1),
            (0.95, 0.28, 0.12, 1),
            (0.62, 0.82, 1.0, 1),
        ]
        for _ in range(28):
            angle = random.uniform(0.0, 6.28318)
            speed = random.uniform(70.0, 220.0)
            particles.append(
                {
                    "x": center_x + random.uniform(-ship["w"] * 0.15, ship["w"] * 0.15),
                    "y": center_y + random.uniform(-ship["h"] * 0.15, ship["h"] * 0.15),
                    "dx": speed * random.uniform(-1.0, 1.0),
                    "dy": speed * random.uniform(-0.2, 1.0),
                    "size": random.uniform(6.0, 16.0),
                    "alpha": 1.0,
                    "color": random.choice(colors),
                }
            )
        return particles

    def end_run(self, *_args):
        if self.app.current_player:
            self.app.storage.update_score(self.app.current_player, self.score)
        self.manager.current = "ranking"

    def go_menu(self, *_args):
        self.manager.current = "menu"


class RankingScreen(BaseScreen):
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)
        root = BoxLayout(orientation="vertical", padding=24, spacing=16)
        root.add_widget(Label(text="Ranking", font_size="32sp", bold=True, color=TEXT_PRIMARY, size_hint_y=None, height=72))
        self.board_label = Label(text="No pilots yet.", color=TEXT_MUTED, valign="top")
        root.add_widget(self.board_label)

        controls = BoxLayout(size_hint_y=None, height=60, spacing=14)
        back_button = action_button("Menu")
        back_button.bind(on_release=self.go_menu)
        login_button = action_button("Switch Player")
        login_button.bind(on_release=self.go_login)
        controls.add_widget(back_button)
        controls.add_widget(login_button)
        root.add_widget(controls)
        self.add_widget(root)

    def on_pre_enter(self, *_args):
        rows = self.app.storage.leaderboard()
        if not rows:
            self.board_label.text = "No pilots yet.\nPlay one run to create the ranking."
            return

        lines = []
        for index, (username, details) in enumerate(rows[:10], start=1):
            lines.append(
                f"{index}. {username}   Best: {details.get('best_score', 0)}   "
                f"Games: {details.get('games_played', 0)}"
            )
        self.board_label.text = "\n".join(lines)

    def go_menu(self, *_args):
        self.manager.current = "menu"

    def go_login(self, *_args):
        self.manager.current = "login"
