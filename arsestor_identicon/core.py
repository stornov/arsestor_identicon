from hashlib import md5
from PIL.ImageOps import expand
from PIL.Image import new, Image
from PIL.ImageDraw import Draw


class IdenticonGen:
    """Generate GitHub-style identicons from user IDs."""
    
    def __init__(self, pixel_size: int = 50):
        self.pixel_size = pixel_size
    
    def __md5_hash(self, text: str) -> str:
        return md5(text.encode("utf-8")).hexdigest()
    
    def __hex_to_int_list(self, hex_str: str) -> list[int]:
        return [int(c, 16) for c in hex_str]
    
    def __get_color_from_hash(self, hash_str: str) -> tuple[int, int, int]:
        nibbles = self.__hex_to_int_list(hash_str[-7:])
        hue = (nibbles[0] << 8) + (nibbles[1] << 4) + nibbles[2]
        saturation = (nibbles[3] << 4) + nibbles[4]
        lightness = (nibbles[5] << 4) + nibbles[6]

        h = (hue / 4095.0) * 360
        s = 0.65 - (saturation / 255.0) * 0.5
        l = 0.75 - (lightness / 255.0) * 0.5

        return self.__hsl_to_rgb(h, s, l)
    
    def __hsl_to_rgb(self, h: float, s: float, l: float) -> tuple[int, int, int]:
        c = (1 - abs(2 * l - 1)) * s
        hp = h / 60.0
        x = c * (1 - abs(hp % 2 - 1))
        r1, g1, b1 = 0, 0, 0

        if 0 <= hp < 1:
            r1, g1, b1 = c, x, 0
        elif 1 <= hp < 2:
            r1, g1, b1 = x, c, 0
        elif 2 <= hp < 3:
            r1, g1, b1 = 0, c, x
        elif 3 <= hp < 4:
            r1, g1, b1 = 0, x, c
        elif 4 <= hp < 5:
            r1, g1, b1 = x, 0, c
        elif 5 <= hp < 6:
            r1, g1, b1 = c, 0, x

        m = l - c / 2
        r = int((r1 + m) * 255)
        g = int((g1 + m) * 255)
        b = int((b1 + m) * 255)

        return (r, g, b)
    
    def generate_identicon(self, user_id: str) -> Image:
        """
        Generate identicon image from text.

        Args:
            user_id (str): Unique string (e.g., username or email).

        Returns:
            Image: Pillow Image object. You can show it with .show() or save it with .save("filename.png").
        """
        hash_str = self.__md5_hash(user_id)
        nibbles = self.__hex_to_int_list(hash_str)

        pattern = [nibbles[i] % 2 == 0 for i in range(15)]
        
        grid = []
        grid_size = 5
        for row in range(grid_size):
            row_pattern = pattern[row * 3 : row * 3 + 3]
            row_pattern += row_pattern[0:2][::-1]
            grid.append(row_pattern)

        color = self.__get_color_from_hash(hash_str)

        img_size = self.pixel_size * grid_size
        image = new("RGB", (img_size, img_size), (240, 240, 240))
        draw = Draw(image)

        for y in range(grid_size):
            for x in range(grid_size):
                if grid[y][x]:
                    x0 = x * self.pixel_size
                    y0 = y * self.pixel_size
                    x1 = x0 + self.pixel_size
                    y1 = y0 + self.pixel_size
                    draw.rectangle([x0, y0, x1, y1], fill=color)

        return expand(image, self.pixel_size, (240, 240, 240))