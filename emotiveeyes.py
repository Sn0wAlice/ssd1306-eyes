# emotiveeyes.py - Neutral eyes only (Anki Cozmo style: full rounded glowing squares centered)
from PIL import Image, ImageDraw
import math
import time

WIDTH = 128
HEIGHT = 64
EYE_SPACING = 44
FPS = 24

class EmotiveEyes:
    def __init__(self, device):
        self.device = device
        self.eye_w = 16  # réduit
        self.eye_h = 20  # réduit
        self.frame = 0

        # Recalculer les centres pour occuper ~2/3 de l'écran et centrer verticalement
        total_eye_width = self.eye_w * 2 + EYE_SPACING
        start_x = (WIDTH - total_eye_width) // 2
        self.center_left = (start_x + self.eye_w, HEIGHT // 2)
        self.center_right = (start_x + self.eye_w + EYE_SPACING, HEIGHT // 2)

    #                       
    #   ____                
    #  |    \ ___ ___ _ _ _ 
    #  |  |  |  _| .'| | | |
    #  |____/|_| |__,|_____|
    #                       
    def draw(self, expression="neutral", offset=(0, 0)):
        ox, oy = offset

        image = Image.new("1", (WIDTH, HEIGHT))
        draw = ImageDraw.Draw(image)

        if expression == "neutral":
            self._draw_neutral(draw, self.center_left, ox, oy)
            self._draw_neutral(draw, self.center_right, ox, oy)
        elif expression == "happy":
            self._draw_happy(draw, self.center_left, ox, oy)
            self._draw_happy(draw, self.center_right, ox, oy)
        elif expression == "glee":
            self._draw_glee(draw, self.center_left, ox, oy)
            self._draw_glee(draw, self.center_right, ox, oy)
        elif expression == "sad":
            self._draw_sad(draw, self.center_left, ox, oy, flip=False)
            self._draw_sad(draw, self.center_right, ox, oy, flip=True)
        elif expression == "worried":
            self._draw_worried(draw, self.center_left, ox, oy)
            self._draw_worried(draw, self.center_right, ox, oy, flip=True)
        elif expression == "focused":
            self._draw_focused(draw, self.center_left, ox, oy)
            self._draw_focused(draw, self.center_right, ox, oy)
        elif expression == "annoyed":
            self._draw_annoyed(draw, self.center_left, ox, oy)
            self._draw_annoyed(draw, self.center_right, ox, oy, flip=True)
        elif expression == "surprised":
            self._draw_surprised(draw, self.center_left, ox, oy)
            self._draw_surprised(draw, self.center_right, ox, oy)
        elif expression == "skeptic":
            self._draw_surprised(draw, self.center_left, ox, oy)
            self._draw_sad(draw, self.center_right, ox, oy)
        elif expression == "angry":
            self._draw_sad(draw, self.center_left, ox, oy, flip=True)
            self._draw_sad(draw, self.center_right, ox, oy)
        elif expression == "loving":
            self._draw_loving(draw, self.center_left, ox, oy)
            self._draw_loving(draw, self.center_right, ox, oy)
        else:
            pass  # Future expressions placeholder

        self.device.display(image)

    def _draw_neutral(self, draw, center, ox, oy):
        cx, cy = center

        # Remplir chaque œil d’un carré arrondi plein (pas de pupille)
        draw.rounded_rectangle([
            cx - self.eye_w + ox,
            cy - self.eye_h + oy,
            cx + self.eye_w + ox,
            cy + self.eye_h + oy
        ], radius=6, fill=255)
    
    def _draw_happy(self, draw, center, ox, oy):
        cx, cy = center

        # Demi-lune vers le haut : arrondi sur le haut, plat en bas
        box = [cx - self.eye_w + ox, cy - self.eye_h // 2 + oy,
            cx + self.eye_w + ox, cy + self.eye_h // 2 + oy]

        # Dessine la partie supérieure seulement
        draw.pieslice(box, start=180, end=360, fill=255)

    def _draw_glee(self, draw, center, ox, oy):
        cx, cy = center

        # Haut : comme happy
        box = [cx - self.eye_w + ox, cy - self.eye_h // 2 + oy,
            cx + self.eye_w + ox, cy + self.eye_h // 2 + oy]
        draw.pieslice(box, start=180, end=360, fill=255)

        # Bas : fine courbe douce sous la demi-lune
        arc_box = [cx - self.eye_w + ox, cy + self.eye_h // 4 + oy,
                cx + self.eye_w + ox, cy + self.eye_h // 2 + oy]
        draw.arc(arc_box, start=180, end=360, fill=255)

    def _draw_sad(self, draw, center, ox, oy, flip=False):
        cx, cy = center
        w = self.eye_w
        scale_h = 0.4
        h = int(self.eye_h * scale_h)
        radius = 4
        inner_offset = 4
        shift = 5

        if flip:
            top_left = (cx - w + ox, cy - h + oy)
            top_right = (cx + w + ox, cy - h + oy + shift)
        else:
            top_left = (cx - w + ox, cy - h + oy + shift)
            top_right = (cx + w + ox, cy - h + oy)

        bottom_left = (cx - w + ox, cy + h + oy)
        bottom_right = (cx + w + ox, cy + h + oy)

        # Corps principal (dessus en diagonale)
        draw.polygon([top_left, top_right, bottom_right, bottom_left], fill=255)

        # Ajout d’une bande centrale pour combler proprement le bas
        base_top = bottom_left[1] - radius
        draw.rectangle([bottom_left[0] + inner_offset, base_top,
                        bottom_right[0] - inner_offset, bottom_right[1]], fill=255)


        # Coins arrondis internes (gauche et droite)
        draw.pieslice([bottom_left[0] - radius + inner_offset, bottom_left[1] - radius,
                    bottom_left[0] + radius + inner_offset, bottom_left[1] + radius],
                    start=90, end=180, fill=255)

        draw.pieslice([bottom_right[0] - radius - inner_offset, bottom_right[1] - radius,
                    bottom_right[0] + radius - inner_offset, bottom_right[1] + radius],
                    start=0, end=90, fill=255)
        
        draw.rectangle([
                        bottom_left[0] - radius + inner_offset + 5, bottom_left[1] - radius,
                        bottom_right[0] + radius - inner_offset -5, bottom_right[1] + radius ], fill=255)
        
    def _draw_worried(self, draw, center, ox, oy, flip=False):
        cx, cy = center

        # Ajustement des dimensions
        w = self.eye_w
        scale_h = (0.6 if flip else 0.4)  # plus haut pour worried
        h = int(self.eye_h * scale_h)

        radius = 4
        inner_offset = 4
        shift = 5

        if flip:
            top_left = (cx - w + ox, cy - h + oy)
            top_right = (cx + w + ox, cy - h + oy + shift)
        else:
            top_left = (cx - w + ox, cy - h + oy + shift)
            top_right = (cx + w + ox, cy - h + oy)

        bottom_left = (cx - w + ox, cy + h + oy)
        bottom_right = (cx + w + ox, cy + h + oy)

        # Corps principal
        draw.polygon([top_left, top_right, bottom_right, bottom_left], fill=255)

        # Bande du bas entre les arrondis
        base_top = bottom_left[1] - radius
        draw.rectangle([bottom_left[0] + inner_offset, base_top,
                        bottom_right[0] - inner_offset, bottom_right[1]], fill=255)

        # Arrondis inférieurs gauche
        draw.pieslice([bottom_left[0] - radius + inner_offset, bottom_left[1] - radius,
                    bottom_left[0] + radius + inner_offset, bottom_left[1] + radius],
                    start=90, end=180, fill=255)

        # Arrondis inférieurs droit
        draw.pieslice([bottom_right[0] - radius - inner_offset, bottom_right[1] - radius,
                    bottom_right[0] + radius - inner_offset, bottom_right[1] + radius],
                    start=0, end=90, fill=255)

        # Bande basse finale (comme sad, mais plus large ici)
        draw.rectangle([
            bottom_left[0] - radius + inner_offset + 5, bottom_left[1] - radius,
            bottom_right[0] + radius - inner_offset - 5, bottom_right[1] + radius
        ], fill=255)

    def _draw_focused(self, draw, center, ox, oy):
        cx, cy = center
        w = self.eye_w
        h = int(self.eye_h * 0.4)  # plus fin que neutral
        r = 6  # arrondi doux

        x0 = cx - w + ox
        y0 = cy - h + oy
        x1 = cx + w + ox
        y1 = cy + h + oy

        draw.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=255)

    def _draw_annoyed(self, draw, center, ox, oy, flip=False):
        cx, cy = center
        tmph = self.eye_h
        # si flip est True, la taille de l'oeil div /2
        if flip:
            tmph //= 2

        # Demi-lune inversée : plat en haut, arrondi vers le bas
        box = [
            cx - self.eye_w + ox,
            cy - tmph // 2 + oy,
            cx + self.eye_w + ox,
            cy + tmph // 2 + oy
        ]

        # Dessine la partie inférieure uniquement
        draw.pieslice(box, start=0, end=180, fill=255)

        # Boucher le haut avec un rectangle plat (pour le rendre propre)
        draw.rectangle(
            [box[0], box[1], box[2], cy + oy],
            fill=255
        )

    def _draw_surprised(self, draw, center, ox, oy):
        cx, cy = center

        # Yeux grands ouverts
        w = self.eye_w
        h = int(self.eye_h * 0.9)  # plus grands que neutral
        r = 10  # rayon d’arrondi plus grand

        x0 = cx - w + ox
        y0 = cy - h + oy
        x1 = cx + w + ox
        y1 = cy + h + oy

        draw.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=255)

    def _draw_loving(self, draw, center, ox, oy):
        cx, cy = center

        # Yeux style "surprised"
        w = self.eye_w
        h = int(self.eye_h * 0.9)
        r = 10

        x0 = cx - w + ox
        y0 = cy - h + oy
        x1 = cx + w + ox
        y1 = cy + h + oy

        # Eye outline
        draw.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=255)

        # --- Heart shape ---
        heart_w = int(w * 0.4)
        heart_h = int(h * 0.4)
        hx = cx + ox
        hy = cy + oy

        # Arcs = upper lobes
        left_arc = [hx - heart_w, hy - heart_h, hx, hy]
        right_arc = [hx, hy - heart_h, hx + heart_w, hy]

        # Triangle = bottom of heart, closer to the arcs
        triangle = [
            (hx - heart_w , hy -3),
            (hx + heart_w , hy -3),
            (hx, hy + heart_h - 1)
        ]

        draw.pieslice(left_arc, start=180, end=360, fill=0)
        draw.pieslice(right_arc, start=180, end=360, fill=0)
        draw.polygon(triangle, fill=0)

    #                     
    #   _____ _   _ _     
    #  |  |  | |_|_| |___ 
    #  |  |  |  _| | |_ -|
    #  |_____|_| |_|_|___|
    #                     
    def animate_expression(self, expression="neutral", duration=2):
        start = time.time()
        while time.time() - start < duration:
            # get random between 0.5 and 2
            rand =  math.sin(self.frame / 10.0) * 0.5 + 1.5
            offset_y = int(math.sin(self.frame / 2.0) * rand)
            self.draw(expression=expression, offset=(0, offset_y))
            time.sleep(1.0 / FPS)
            self.frame += 1

    def blink(self, duration=0.002, steps=4, original_expression="neutral"):
        # Blink: yeux se ferment puis se rouvrent
        delay = duration / (steps * 2)
        original_h = self.eye_h

        # Fermeture progressive
        for i in range(steps):
            self.eye_h = max(1, original_h - (i * original_h // steps))
            self.draw(expression=original_expression)
            time.sleep(delay)

        # Ligne fine
        self.eye_h = 1
        self.draw(expression=original_expression)
        time.sleep(delay)

        # Réouverture progressive
        for i in range(steps, -1, -1):
            self.eye_h = max(1, original_h - (i * original_h // steps))
            self.draw(expression=original_expression)
            time.sleep(delay)

        # Reset taille normale
        self.eye_h = original_h
