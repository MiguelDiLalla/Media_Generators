import os

def create_project_structure(root_dir):
    structure = {
        "assets": ["audio", "images", "videos"],
        "docs": [],
        "exports": ["reels", "shorts", "horizontal"],
        "presets": [],
        "scenes": ["examples", "storytelling", "educational", "transitions"],
        "scripts": [],
        "templates": [],
        "tests": [],
        "notebooks": []  # Notebooks for development and exploration
    }

    files = {
        "docs": ["README.md", "SETUP.md", "USAGE.md", "ROADMAP.md"],
        "presets": ["color_schemes.py", "transitions.py", "effects.py", "typography.py"],
        "scripts": ["batch_render.py", "audio_sync.py", "video_export.py", "util.py"],
        "templates": ["base_scene.py", "audio_scene.py"],
        "tests": ["test_presets.py", "test_scenes.py", "test_utils.py"],
        "notebooks": ["README.md"],  # Added README for notebooks folder
        "root": [".gitignore", "config.py", "requirements.txt", "run.py"]
    }

    comments = {
        "assets": "# Media files for animations (audio, images, videos)",
        "docs": "# Documentation of the project",
        "exports": "# Exported videos (reels, shorts, horizontal)",
        "notebooks": "# Notebooks for development and exploration",
        "presets": "# Reusable visual effects and style configurations",
        "scenes": "# Manim scenes (examples, storytelling, etc.)",
        "scripts": "# Automation tools and utility functions",
        "templates": "# Base classes and reusable components for scenes",
        "tests": "# Unit tests for ensuring stability"
    }

    # Create root directory
    os.makedirs(root_dir, exist_ok=True)

    # Create folders and subfolders
    for folder, subfolders in structure.items():
        folder_path = os.path.join(root_dir, folder)
        os.makedirs(folder_path, exist_ok=True)

        for subfolder in subfolders:
            os.makedirs(os.path.join(folder_path, subfolder), exist_ok=True)

    # Create files in specific folders
    for folder, filenames in files.items():
        target_dir = root_dir if folder == "root" else os.path.join(root_dir, folder)

        for filename in filenames:
            file_path = os.path.join(target_dir, filename)
            with open(file_path, "w") as f:
                if filename.endswith(".md"):
                    f.write(f"# {filename.split('.')[0]}\n")  # Basic header for Markdown files
                elif filename == ".gitignore":
                    f.write("# Ignore files\n*.pyc\n__pycache__/\n")
                else:
                    f.write("# Placeholder content\n")

    print(f"Project structure created at: {root_dir}")

def create_directory_tree_txt(path, output_file=None):
    if output_file is None:
        output_file = os.path.join(path, "directory_tree.txt")

    comments = {
        "assets": "# Media files for animations (audio, images, videos)",
        "docs": "# Documentation of the project",
        "exports": "# Exported videos (reels, shorts, horizontal)",
        "notebooks": "# Notebooks for development and exploration",
        "presets": "# Reusable visual effects and style configurations",
        "scenes": "# Manim scenes (examples, storytelling, etc.)",
        "scripts": "# Automation tools and utility functions",
        "templates": "# Base classes and reusable components for scenes",
        "tests": "# Unit tests for ensuring stability"
    }

    def generate_tree(path, prefix=""):
        entries = os.listdir(path)
        entries.sort()
        lines = []
        for index, entry in enumerate(entries):
            full_path = os.path.join(path, entry)
            connector = "└── " if index == len(entries) - 1 else "├── "
            comment = f" {comments.get(entry, '')}" if entry in comments else ""
            lines.append(f"{prefix}{connector}{entry}{comment}")
            if os.path.isdir(full_path):
                extension = "    " if index == len(entries) - 1 else "│   "
                lines.extend(generate_tree(full_path, prefix + extension))
        return lines

    tree_lines = generate_tree(path)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(tree_lines))

    print(f"Directory tree saved to {output_file}")

if __name__ == "__main__":
    root_dir = "manim_project"
    create_project_structure(root_dir)
    create_directory_tree_txt(root_dir)
