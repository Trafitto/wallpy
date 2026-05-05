# WallPy

Change wallpaper by scraping GitHub repos.


## Usage

Add a wallpaper repository:

```bash
python wallpy.py --add USER/REPO
```

Set a random wallpaper:

```bash
python wallpy.py
```

Pick from a specific category:

```bash
python wallpy.py --category <name>
```

List configured repositories:

```bash
python wallpy.py --list
```

Show available categories:

```bash
python wallpy.py --categories
```

## How it works

WallPy fetches images from public GitHub repos using the GitHub API, caches them locally in `~/.cache/wallpy`, and applies them via `gsettings` (GNOME).

## Repo structure

WallPy expects repositories to be organized with top-level directories acting as categories, each containing image files (`.png`, `.jpg`, `.jpeg`, `.webp`). For example:

```
repo/
  category-a/
    wallpaper1.png
    wallpaper2.jpg
  category-b/
    wallpaper3.webp
```

See [X2Borgo/Instal-wallpapers](https://github.com/X2Borgo/Instal-wallpapers) for a reference.
