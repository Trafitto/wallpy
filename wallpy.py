import os
import random
import requests
import subprocess
import argparse
from typing import List, Dict

REPOS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "repos.txt")
CACHE_DIR = os.path.expanduser("~/.cache/wallpy")


def load_repos() -> List[str]:
    if not os.path.exists(REPOS_FILE):
        return []
    with open(REPOS_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]


def add_repo(repo: str):
    repos = load_repos()
    if repo in repos:
        print(f"Repository '{repo}' already exists")
        return
    with open(REPOS_FILE, "a") as f:
        f.write(f"{repo}\n")
    print(f"Added '{repo}'")


class WallPy:
    def __init__(self, repos: List[str]):
        self.repos = repos
        os.makedirs(CACHE_DIR, exist_ok=True)

    def fetch_contents(self, repo: str, path="") -> List[Dict]:
        api_url = f"https://api.github.com/repos/{repo}/contents/{path}"
        res = requests.get(api_url)
        res.raise_for_status()
        return res.json()

    def get_categories(self, repo: str) -> List[str]:
        contents = self.fetch_contents(repo)
        categories = []
        for item in contents:
            if item['type'] == 'dir' and not item['name'].startswith('.'):
                categories.append(item['name'])
        return categories

    def get_images(self, repo: str, category: str) -> List[Dict]:
        contents = self.fetch_contents(repo, category)
        return [item for item in contents if item['type'] == 'file' and item['name'].lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]

    def set_wallpaper(self, image_url: str):
        filename = image_url.split('/')[-1]
        filepath = os.path.join(CACHE_DIR, filename)

        print(f"Downloading {filename}...")
        res = requests.get(image_url)
        with open(filepath, 'wb') as f:
            f.write(res.content)

        print(f"Setting wallpaper: {filepath}")
        subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", f"file://{filepath}"])
        subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri-dark", f"file://{filepath}"])

    def random_wallpaper(self, category: str = None):
        if category:
            all_images = []
            for repo in self.repos:
                try:
                    images = self.get_images(repo, category)
                    all_images.extend(images)
                except Exception:
                    continue
            if not all_images:
                print(f"No images found in category '{category}'")
                return
        else:
            repo = random.choice(self.repos)
            cats = self.get_categories(repo)
            cat = random.choice(cats)
            all_images = self.get_images(repo, cat)

        img = random.choice(all_images)
        self.set_wallpaper(img['download_url'])


def main():
    parser = argparse.ArgumentParser(description="WallPy - Set random wallpapers from GitHub repos")
    parser.add_argument("--add", type=str, metavar="USER/REPO", help="Add a wallpaper repository")
    parser.add_argument("--list", action="store_true", help="List configured repositories")
    parser.add_argument("--categories", action="store_true", help="Show available categories")
    parser.add_argument("--category", type=str, metavar="NAME", help="Pick a random wallpaper from a specific category")

    args = parser.parse_args()
    repos = load_repos()

    if args.add:
        add_repo(args.add)
        return

    if args.list:
        if not repos:
            print("No repositories configured. Add one with --add USER/REPO")
            return
        print("Repositories:")
        for r in repos:
            print(f"  - {r}")
        return

    if not repos:
        print("No repositories configured. Add one with --add USER/REPO")
        return

    wallpy = WallPy(repos)
    if args.categories:
        for repo in repos:
            cats = wallpy.get_categories(repo)
            print(f"{repo}:")
            for cat in cats:
                print(f"\t{cat}")
        return
    wallpy.random_wallpaper(category=args.category)



if __name__ == "__main__":
    main()
