import os

# ===== CONFIG =====
OUTPUT_FILE = "repo_dump.txt"
INCLUDE_EXTENSIONS = {
    ".py", ".txt", ".md", ".java", ".js", ".html", ".css", ".json", ".yaml", ".yml"
}
EXCLUDE_DIRS = {
    ".git", "__pycache__", "node_modules", "venv", ".idea", ".vscode", "dist", "build"
}
MAX_FILE_SIZE = 200 * 1024  # 200 KB per file

# ==================

def is_text_file(file_path):
    _, ext = os.path.splitext(file_path)
    return ext.lower() in INCLUDE_EXTENSIONS


def should_skip_dir(dirname):
    return dirname in EXCLUDE_DIRS


def generate_tree(root_dir):
    tree_lines = []
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if not should_skip_dir(d)]

        level = root.replace(root_dir, "").count(os.sep)
        indent = "  " * level
        tree_lines.append(f"{indent}{os.path.basename(root)}/")

        sub_indent = "  " * (level + 1)
        for f in files:
            tree_lines.append(f"{sub_indent}{f}")
    return "\n".join(tree_lines)


def dump_files(root_dir, out):
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if not should_skip_dir(d)]

        for file in files:
            path = os.path.join(root, file)

            if not is_text_file(path):
                continue

            if os.path.getsize(path) > MAX_FILE_SIZE:
                out.write(f"\n===== SKIPPED (TOO LARGE): {path} =====\n")
                continue

            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()

                out.write(f"\n===== FILE: {path} =====\n")
                out.write(content + "\n")

            except Exception as e:
                out.write(f"\n===== ERROR READING: {path} =====\n{e}\n")


def main():
    root_dir = os.getcwd()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("===== REPO STRUCTURE =====\n")
        out.write(generate_tree(root_dir))

        out.write("\n\n===== FILE CONTENTS =====\n")
        dump_files(root_dir, out)

    print(f"Dump created: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()