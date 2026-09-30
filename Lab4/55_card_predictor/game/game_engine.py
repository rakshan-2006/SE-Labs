# pyrefly: ignore [missing-import]
import pygame
from game.deck import Deck


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.deck = Deck()

        self.current_card = self.deck.draw()
        self.next_card = None
        self.score = 0
        self.streak = 0

        # Card reveal state
        self.revealing = False
        self.reveal_start_time = 0
        self.reveal_duration = 1500  # milliseconds

        self.status_msg = "Will the next card be HIGHER or LOWER?"
        self.status_color = (220, 220, 220)

        btn_w, btn_h = 140, 48
        self.btn_higher = pygame.Rect(
            width // 2 - btn_w - 20,
            height - 90,
            btn_w,
            btn_h
        )
        self.btn_lower = pygame.Rect(
            width // 2 + 20,
            height - 90,
            btn_w,
            btn_h
        )

        self.font_title = pygame.font.SysFont(None, 40)
        self.font_medium = pygame.font.SysFont(None, 30)
        self.font_small = pygame.font.SysFont(None, 24)

    def evaluate_guess(self, guess):
        """Draw the next card and evaluate the player's prediction."""

        # Do not allow another guess while the cards are being revealed.
        if self.revealing:
            return

        self.next_card = self.deck.draw()

        # Check for a tie before evaluating HIGHER or LOWER.
        if (
            self.next_card.numeric_rank
            == self.current_card.numeric_rank
        ):
            # A tie preserves both score and streak.
            self.status_msg = "PUSH / TIE! Rank matched."
            self.status_color = (255, 220, 0)

        else:
            # Compare numeric ranks:
            # 2 < 3 < ... < 10 < J < Q < K < A
            if guess == "HIGHER":
                correct = (
                    self.next_card.numeric_rank
                    > self.current_card.numeric_rank
                )
            else:
                correct = (
                    self.next_card.numeric_rank
                    < self.current_card.numeric_rank
                )

            if correct:
                # Increase consecutive win streak.
                self.streak += 1

                # Apply streak multiplier.
                if self.streak >= 5:
                    multiplier = 3
                elif self.streak >= 3:
                    multiplier = 2
                else:
                    multiplier = 1

                points_earned = multiplier
                self.score += points_earned

                self.status_msg = (
                    f"CORRECT! {self.next_card.rank_str} "
                    f"vs {self.current_card.rank_str} | "
                    f"Streak: {self.streak} | "
                    f"+{points_earned} points"
                )
                self.status_color = (80, 220, 80)

            else:
                # Incorrect guess resets the streak.
                self.streak = 0

                self.score = max(0, self.score - 1)

                self.status_msg = (
                    f"WRONG! {self.next_card.rank_str} "
                    f"vs {self.current_card.rank_str} | "
                    f"Streak reset | -1 point"
                )
                self.status_color = (235, 75, 75)

        # Start the side-by-side reveal.
        self.revealing = True
        self.reveal_start_time = pygame.time.get_ticks()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            # Ignore button presses while cards are being revealed.
            if self.revealing:
                return

            if self.btn_higher.collidepoint(event.pos):
                self.evaluate_guess("HIGHER")

            elif self.btn_lower.collidepoint(event.pos):
                self.evaluate_guess("LOWER")

    def update(self):
        """Update the card reveal animation state."""

        if self.revealing:
            elapsed = pygame.time.get_ticks() - self.reveal_start_time

            if elapsed >= self.reveal_duration:
                # Reveal is complete.
                # The newly drawn card becomes the current card.
                self.current_card = self.next_card
                self.next_card = None
                self.revealing = False

                self.status_msg = (
                    "Will the next card be HIGHER or LOWER?"
                )
                self.status_color = (220, 220, 220)

    def render(self, screen):
        screen.fill((25, 80, 45))

        title_surf = self.font_title.render(
            "High-Low Card Predictor",
            True,
            (245, 245, 245)
        )
        screen.blit(
            title_surf,
            (
                self.width // 2 - title_surf.get_width() // 2,
                25
            )
        )

        # Score
        score_surf = self.font_medium.render(
            f"Score: {self.score}",
            True,
            (255, 220, 80)
        )
        screen.blit(score_surf, (30, 30))

        # Streak
        streak_surf = self.font_medium.render(
            f"Streak: {self.streak}",
            True,
            (255, 220, 80)
        )
        screen.blit(
            streak_surf,
            (30, 65)
        )

        # Remaining cards
        rem_surf = self.font_small.render(
            f"Deck: {self.deck.remaining} left",
            True,
            (210, 210, 210)
        )
        screen.blit(
            rem_surf,
            (
                self.width - rem_surf.get_width() - 30,
                35
            )
        )

        card_w, card_h = 130, 180

        if self.revealing and self.next_card is not None:
            # During the reveal, show both cards side-by-side.

            left_x = self.width // 2 - card_w - 30
            right_x = self.width // 2 + 30
            card_y = 100

            # Previous card
            self.current_card.render(
                screen,
                left_x,
                card_y,
                card_w,
                card_h
            )

            # Newly revealed card
            self.next_card.render(
                screen,
                right_x,
                card_y,
                card_w,
                card_h
            )

            # Labels above the cards
            previous_label = self.font_small.render(
                "PREVIOUS",
                True,
                (220, 220, 220)
            )
            screen.blit(
                previous_label,
                (
                    left_x
                    + card_w // 2
                    - previous_label.get_width() // 2,
                    75
                )
            )

            new_label = self.font_small.render(
                "NEW CARD",
                True,
                (220, 220, 220)
            )
            screen.blit(
                new_label,
                (
                    right_x
                    + card_w // 2
                    - new_label.get_width() // 2,
                    75
                )
            )

        else:
            # Normal game state: show only the current card.
            self.current_card.render(
                screen,
                self.width // 2 - card_w // 2,
                100,
                card_w,
                card_h
            )

        # Status message
        status_surf = self.font_small.render(
            self.status_msg,
            True,
            self.status_color
        )
        screen.blit(
            status_surf,
            (
                self.width // 2
                - status_surf.get_width() // 2,
                310
            )
        )

        # Disable-looking buttons during the reveal.
        if self.revealing:
            higher_color = (80, 80, 80)
            lower_color = (80, 80, 80)
        else:
            higher_color = (40, 140, 60)
            lower_color = (170, 50, 50)

        # HIGHER button
        pygame.draw.rect(
            screen,
            higher_color,
            self.btn_higher,
            border_radius=8
        )
        pygame.draw.rect(
            screen,
            (220, 220, 220),
            self.btn_higher,
            width=2,
            border_radius=8
        )

        high_surf = self.font_medium.render(
            "HIGHER",
            True,
            (255, 255, 255)
        )
        screen.blit(
            high_surf,
            (
                self.btn_higher.centerx
                - high_surf.get_width() // 2,
                self.btn_higher.centery
                - high_surf.get_height() // 2
            )
        )

        # LOWER button
        pygame.draw.rect(
            screen,
            lower_color,
            self.btn_lower,
            border_radius=8
        )
        pygame.draw.rect(
            screen,
            (220, 220, 220),
            self.btn_lower,
            width=2,
            border_radius=8
        )

        low_surf = self.font_medium.render(
            "LOWER",
            True,
            (255, 255, 255)
        )
        screen.blit(
            low_surf,
            (
                self.btn_lower.centerx
                - low_surf.get_width() // 2,
                self.btn_lower.centery
                - low_surf.get_height() // 2
            )
        )