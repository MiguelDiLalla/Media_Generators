import os

def update_directory_tree(path, output_file="notebooks/directory_tree.txt"):
    """
    Generates a directory tree for the given path and saves it to a .txt file.

    Parameters:
        path (str): The root directory to generate the tree from.
        output_file (str): The file to save the directory tree to.
    """

    # Comments for specific folders
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
        """
        Recursively generates the directory tree structure.

        Parameters:
            path (str): The directory path to analyze.
            prefix (str): The prefix to use for tree structure formatting.

        Returns:
            list: Lines of the tree structure.
        """
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

    # Generate the directory tree
    tree_lines = generate_tree(path)

    # Save the tree to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(tree_lines))

    print(f"Directory tree saved to {output_file}")

if __name__ == "__main__":
    # Define the root directory of the project
    root_dir = os.getcwd()  # Current directory as root
    output_file = "notebooks/directory_tree.txt"  # Target file
    update_directory_tree(root_dir, output_file)
