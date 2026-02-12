from pathlib import Path
from datetime import datetime
import argparse
import os

class ProjectTreeGenerator:
    def __init__(self):
        self.exclude_dirs = {
            '__pycache__', 
            '.git', 
            '.pytest_cache', 
            '.ipynb_checkpoints',
            'uv.venv',
            'node_modules'
        }
        self.always_show_dirs = {
            'child_envs',
            'mother_env',
            'HELPFILES',
            'notebooks',
            'scripts'
        }
        self.include_extensions = {
            '.py',      # Python files
            '.ipynb',   # Jupyter notebooks
            '.md',      # Markdown files
            '.txt',     # Text files
            '.csv',     # CSV files
            '.xlsx',    # Excel files
            '.json',    # JSON files
            '.pdf',     # PDF files
            '.docx',    # Word documents
            '.bat',     # Batch files
            '.yml',     # YAML files
            '.yaml'     # YAML files
        }

    def generate_tree(self, start_path: Path, output_file: str = None, max_depth: int = 3) -> str:
        def _add_to_tree(current_path: Path, prefix: str = '', depth: int = 0) -> list:
            if max_depth is not None and depth >= max_depth:
                return []

            lines = []
            dirs = []
            files = []

            try:
                for path in sorted(current_path.iterdir()):
                    if path.is_dir() and self.should_show_directory(path):
                        dirs.append(path)
                    elif path.is_file() and path.suffix in self.include_extensions:
                        files.append(path)
            except PermissionError:
                return [f"{prefix}!!! Permission Denied !!!"]

            for i, path in enumerate(dirs):
                is_last = (i == len(dirs) - 1) and not files
                connector = '└──' if is_last else '├──'
                icon = '📂' if path.name in self.always_show_dirs else '📁'
                lines.append(f"{prefix}{connector} {icon} {path.name}/")

                extension = '    ' if is_last else '│   '
                lines.extend(_add_to_tree(path, prefix + extension, depth + 1))

            for i, path in enumerate(files):
                is_last = i == len(files) - 1
                connector = '└──' if is_last else '├──'
                icon = self.get_file_icon(path)
                lines.append(f"{prefix}{connector} {icon} {path.name}")

            return lines

        header = [
            f"JPNB-DYAD Project Tree Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Root: {start_path.absolute()}",
            "(c) 2024 Hans Hendrickx - MIT License",
            "In cooperation with v0 AI Assistant",
            "",
            "Project Structure Legend:",
            "📂 - Key Project Directory",
            "📁 - Regular Directory",
            "🐍 - Python Source File",
            "📓 - Jupyter Notebook",
            "📝 - Markdown File",
            "📊 - Excel or CSV File",
            "📄 - PDF File",
            "📃 - Word Document",
            "⚙️ - Batch File",
            "🔧 - JSON or YAML File",
            "-" * 80,
            ""
        ]

        tree_lines = _add_to_tree(start_path)
        full_tree = header + tree_lines

        if output_file:
            os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(full_tree))

        return '\n'.join(full_tree)

    def should_show_directory(self, path: Path) -> bool:
        return (path.name in self.always_show_dirs or 
                (path.name not in self.exclude_dirs and 
                 not any(excluded in path.parts for excluded in self.exclude_dirs)))

    def get_file_icon(self, path: Path) -> str:
        if path.suffix == '.py':
            return '🐍'
        elif path.suffix == '.ipynb':
            return '📓'
        elif path.suffix == '.md':
            return '📝'
        elif path.suffix in ['.csv', '.xlsx']:
            return '📊'
        elif path.suffix == '.pdf':
            return '📄'
        elif path.suffix == '.docx':
            return '📃'
        elif path.suffix == '.bat':
            return '⚙️'
        elif path.suffix in ['.json', '.yml', '.yaml']:
            return '🔧'
        else:
            return '📄'

def main():
    parser = argparse.ArgumentParser(description='Generate JPNB-DYAD project tree structure')
    parser.add_argument('--path', type=str, default='.',
                       help='Path to generate tree from (default: current directory)')
    parser.add_argument('--output', type=str, default='HELPFILES/project_structure.txt',
                       help='Output file path (default: HELPFILES/project_structure.txt)')
    parser.add_argument('--max-depth', type=int, default=3,
                       help='Maximum folder depth to display (default: 3)')

    args = parser.parse_args()

    generator = ProjectTreeGenerator()
    tree = generator.generate_tree(
        Path(args.path),
        args.output,
        args.max_depth
    )

    print(tree)
    print(f"\nProject structure saved to {args.output}")

if __name__ == "__main__":
    main()