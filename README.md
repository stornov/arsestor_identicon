# Identicon Generator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Generates GitHub-style identicons from MD5-hashed strings. Returns a `PIL.Image.Image` object for flexible image manipulation.

## Installation

```bash
pip install arsestor-identicon
```

## Quick Start
```python
from arsestor_identicon import IdenticonGen

# Create a generator (block size = 50 pixels)
generator = IdenticonGen(pixel_size=50)

# Generate an identicon
image = generator.generate_identicon("example")

# Save to a file
image.save("filename.png")

# Preview using Pillow's built-in viewer
image.show()
```

## Features
* **Customizable Size**:\
  Adjust the `pixel_size` parameter to change the block size.
  ```python
  generator = IdenticonGen(pixel_size=120)  # Larger blocks
  ```

* Flexible Output: Returns a PIL.Image.Image object, which allows you to:
  - Save in any format (PNG, JPEG, etc.).
  - Modify using Pillow (resize, filters, overlays).
  - Embed in GUI applications (Tkinter, PyQt).

* Deterministic\
  Same input → same identicon, always.

## Usage Examples
### **1. High-Resolution Saving**
```python
generator = IdenticonGen(pixel_size=120)
image = generator.generate_identicon("example")
image.save("high_res_identicon.jpg", quality=90)
```
## **2. Integration with Flask (Web Server)**
```python
from flask import Flask, send_file
from arsestor_identicon import IdenticonGen

app = Flask(__name__)

@app.route("/identicon/<username>")
def get_identicon(username):
    generator = IdenticonGen()
    image = generator.generate_identicon(username)
    return send_file(image, mimetype="image/png")

if __name__ == "__main__":
    app.run()
```

## License
MIT License.\
Copyright (c) 2025 Archip Storozhev.\
For details, see [LICENSE](LICENSE)