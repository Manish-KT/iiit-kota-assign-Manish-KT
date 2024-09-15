import os

def print_directory_structure(root_dir, max_depth, current_depth=0):
    if current_depth > max_depth:
        return

    for root, dirs, files in os.walk(root_dir):
        # Calculate the current level by counting separators
        level = root.replace(root_dir, '').count(os.sep)
        if level > max_depth:
            continue

        indent = ' ' * 4 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f'{subindent}{f}')

        # Avoid walking into directories deeper than the max depth
        dirs[:] = [d for d in dirs if level + 1 <= max_depth]

if __name__ == "__main__":
    root_directory = '.'  # Change this to the directory you want to explore
    max_depth = 2
    print_directory_structure(root_directory, max_depth)
