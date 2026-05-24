from __future__ import annotations

from pathlib import Path

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import FadeTransition, ScreenManager

from shooter.screens import GameScreen, LoginScreen, MenuScreen, RankingScreen
from shooter.storage import PlayerStorage


class ShooterApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Shooter"
        self.current_player = ""
        self.storage = PlayerStorage(Path(__file__).resolve().parent.parent / "data" / "players.json")

    def build(self):
        Window.size = (420, 740)
        manager = ScreenManager(transition=FadeTransition())
        manager.add_widget(LoginScreen(app=self, name="login"))
        manager.add_widget(MenuScreen(app=self, name="menu"))
        manager.add_widget(GameScreen(app=self, name="game"))
        manager.add_widget(RankingScreen(app=self, name="ranking"))
        return manager

    def login_player(self, username: str) -> None:
        normalized = username.strip()
        self.current_player = normalized
        self.storage.ensure_player(normalized)
        if self.root:
            self.root.current = "menu"
