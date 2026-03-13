#!/usr/bin/env python3
# Copyright 2026 simplesoft, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Analyze a codebase and output a JSON summary of its structure, languages, and dependencies."""

import json
import os
import sys
from pathlib import Path
from collections import Counter

def find_files(root, skip_dirs=None):
    """Walk directory tree, skipping common non-source directories."""
    if skip_dirs is None:
        skip_dirs = {
            '.git', 'node_modules', 'vendor', '.vendor', '__pycache__',
            '.tox', '.venv', 'venv', 'env', '.env', 'dist', 'build',
            '.next', '.nuxt', 'target', 'bin', 'obj', '.idea', '.vscode',
            '.docker', 'coverage', '.cache', 'tmp', 'temp',
        }
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs and not d.startswith('.')]
        for f in filenames:
            yield Path(dirpath) / f

LANG_MAP = {
    '.py': 'Python', '.php': 'PHP', '.js': 'JavaScript', '.ts': 'TypeScript',
    '.tsx': 'TypeScript (React)', '.jsx': 'JavaScript (React)',
    '.rb': 'Ruby', '.java': 'Java', '.kt': 'Kotlin', '.scala': 'Scala',
    '.go': 'Go', '.rs': 'Rust', '.cs': 'C#', '.cpp': 'C++', '.c': 'C',
    '.swift': 'Swift', '.m': 'Objective-C', '.pl': 'Perl',
    '.sh': 'Shell', '.bash': 'Shell', '.zsh': 'Shell',
    '.html': 'HTML', '.htm': 'HTML', '.css': 'CSS', '.scss': 'SCSS',
    '.sass': 'Sass', '.less': 'Less', '.vue': 'Vue', '.svelte': 'Svelte',
    '.sql': 'SQL', '.r': 'R', '.lua': 'Lua', '.ex': 'Elixir',
    '.exs': 'Elixir', '.erl': 'Erlang', '.hs': 'Haskell',
    '.tpl': 'Smarty/Template',
}

DEP_FILES = {
    'package.json': 'Node.js/npm',
    'composer.json': 'PHP/Composer',
    'requirements.txt': 'Python/pip',
    'Pipfile': 'Python/Pipenv',
    'pyproject.toml': 'Python/Poetry or PEP 517',
    'setup.py': 'Python/setuptools',
    'Gemfile': 'Ruby/Bundler',
    'Cargo.toml': 'Rust/Cargo',
    'go.mod': 'Go Modules',
    'pom.xml': 'Java/Maven',
    'build.gradle': 'Java/Gradle',
    'build.gradle.kts': 'Kotlin/Gradle',
    'mix.exs': 'Elixir/Mix',
    'Makefile': 'Make',
    'CMakeLists.txt': 'CMake',
    'pubspec.yaml': 'Dart/Flutter',
}

CONFIG_FILES = {
    'Dockerfile': 'Docker',
    'docker-compose.yml': 'Docker Compose',
    'docker-compose.yaml': 'Docker Compose',
    '.dockerignore': 'Docker',
    '.env': 'Environment variables',
    '.env.example': 'Environment variables',
    '.env.sample': 'Environment variables',
    'nginx.conf': 'Nginx',
    'httpd.conf': 'Apache',
    '.htaccess': 'Apache',
    '.github': 'GitHub Actions',
    '.gitlab-ci.yml': 'GitLab CI',
    'Jenkinsfile': 'Jenkins',
    '.circleci': 'CircleCI',
    '.travis.yml': 'Travis CI',
    'jest.config.js': 'Jest',
    'jest.config.ts': 'Jest',
    'phpunit.xml': 'PHPUnit',
    'phpunit.xml.dist': 'PHPUnit',
    'pytest.ini': 'pytest',
    'setup.cfg': 'Python config',
    'tsconfig.json': 'TypeScript',
    'webpack.config.js': 'Webpack',
    'vite.config.js': 'Vite',
    'vite.config.ts': 'Vite',
    'rollup.config.js': 'Rollup',
    'babel.config.js': 'Babel',
    '.babelrc': 'Babel',
    '.eslintrc': 'ESLint',
    '.eslintrc.js': 'ESLint',
    '.eslintrc.json': 'ESLint',
    'eslint.config.js': 'ESLint',
    '.prettierrc': 'Prettier',
    'tailwind.config.js': 'Tailwind CSS',
    'tailwind.config.ts': 'Tailwind CSS',
}

def read_file_safe(path, max_bytes=50000):
    """Read file content safely, returning empty string on error."""
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read(max_bytes)
    except Exception:
        return ''

def parse_json_file(path):
    """Parse a JSON file, returning empty dict on error."""
    content = read_file_safe(path)
    try:
        return json.loads(content)
    except Exception:
        return {}

def analyze_package_json(root):
    """Extract info from package.json."""
    path = root / 'package.json'
    if not path.exists():
        return None
    data = parse_json_file(path)
    return {
        'name': data.get('name', ''),
        'description': data.get('description', ''),
        'version': data.get('version', ''),
        'scripts': list(data.get('scripts', {}).keys()),
        'dependencies': list(data.get('dependencies', {}).keys()),
        'devDependencies': list(data.get('devDependencies', {}).keys()),
        'engines': data.get('engines', {}),
    }

def analyze_composer_json(root):
    """Extract info from composer.json."""
    path = root / 'composer.json'
    if not path.exists():
        return None
    data = parse_json_file(path)
    return {
        'name': data.get('name', ''),
        'description': data.get('description', ''),
        'require': {k: v for k, v in data.get('require', {}).items()},
        'require_dev': {k: v for k, v in data.get('require-dev', {}).items()},
        'autoload': data.get('autoload', {}),
    }

def analyze_requirements_txt(root):
    """Extract info from requirements.txt."""
    path = root / 'requirements.txt'
    if not path.exists():
        return None
    content = read_file_safe(path)
    deps = []
    for line in content.strip().split('\n'):
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('-'):
            deps.append(line)
    return {'dependencies': deps}

def analyze_gemfile(root):
    """Extract gem names from Gemfile."""
    path = root / 'Gemfile'
    if not path.exists():
        return None
    content = read_file_safe(path)
    gems = []
    for line in content.strip().split('\n'):
        line = line.strip()
        if line.startswith('gem '):
            parts = line.split("'")
            if len(parts) >= 2:
                gems.append(parts[1])
            else:
                parts = line.split('"')
                if len(parts) >= 2:
                    gems.append(parts[1])
    return {'gems': gems}

def detect_env_vars(root):
    """Detect environment variable patterns from .env files."""
    env_vars = []
    for name in ['.env.example', '.env.sample', '.env.dist', '.env']:
        path = root / name
        if path.exists():
            content = read_file_safe(path)
            for line in content.strip().split('\n'):
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key = line.split('=')[0].strip()
                    env_vars.append(key)
            break
    return env_vars

def detect_top_dirs(root, max_depth=2):
    """Get top-level and second-level directory structure."""
    dirs = []
    root = Path(root)
    skip = {'.git', 'node_modules', 'vendor', '__pycache__', '.venv', 'venv',
            '.idea', '.vscode', 'dist', 'build', '.next', 'target', 'coverage', '.cache'}
    try:
        for item in sorted(root.iterdir()):
            if item.is_dir() and item.name not in skip and not item.name.startswith('.'):
                subdirs = []
                try:
                    for sub in sorted(item.iterdir()):
                        if sub.is_dir() and sub.name not in skip and not sub.name.startswith('.'):
                            subdirs.append(sub.name)
                except PermissionError:
                    pass
                dirs.append({'name': item.name, 'subdirs': subdirs[:15]})
    except PermissionError:
        pass
    return dirs

def detect_existing_docs(root):
    """Detect existing documentation files."""
    doc_files = {}
    for name in ['README.md', 'README', 'README.txt', 'CLAUDE.md',
                  'CONTRIBUTING.md', 'CHANGELOG.md', 'DOCS.md', 'docs']:
        path = root / name
        if path.exists():
            if path.is_file():
                content = read_file_safe(path, max_bytes=10000)
                doc_files[name] = content
            else:
                doc_files[name] = '[directory]'
    return doc_files

def detect_database(root):
    """Detect database usage from config files and code patterns."""
    indicators = []

    # Check for common DB config patterns
    for f in ['database.yml', 'database.yaml', 'knexfile.js', 'ormconfig.json',
              'ormconfig.ts', 'prisma/schema.prisma', 'alembic.ini', 'migrations']:
        if (root / f).exists():
            indicators.append(f)

    # Check for SQL files
    sql_count = 0
    for fp in find_files(root):
        if fp.suffix == '.sql':
            sql_count += 1
        if sql_count >= 3:
            break
    if sql_count > 0:
        indicators.append(f'{sql_count}+ SQL files')

    return indicators

def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    root = root.resolve()

    if not root.is_dir():
        print(json.dumps({'error': f'Not a directory: {root}'}))
        sys.exit(1)

    # Count languages
    lang_counter = Counter()
    file_count = 0
    for fp in find_files(root):
        ext = fp.suffix.lower()
        if ext in LANG_MAP:
            lang_counter[LANG_MAP[ext]] += 1
        file_count += 1

    # Detect dependency/config files
    found_dep_files = {}
    found_config = {}
    for fp in find_files(root):
        name = fp.name
        if name in DEP_FILES:
            found_dep_files[name] = DEP_FILES[name]
        if name in CONFIG_FILES:
            found_config[name] = CONFIG_FILES[name]
    # Also check root-level directories
    for name in ['.github', '.circleci']:
        if (root / name).is_dir():
            found_config[name] = CONFIG_FILES.get(name, name)

    result = {
        'project_root': str(root),
        'project_name': root.name,
        'total_files': file_count,
        'languages': dict(lang_counter.most_common(10)),
        'dependency_files': found_dep_files,
        'config_files': found_config,
        'directory_structure': detect_top_dirs(root),
        'env_vars': detect_env_vars(root),
        'database_indicators': detect_database(root),
        'existing_docs': detect_existing_docs(root),
        'package_json': analyze_package_json(root),
        'composer_json': analyze_composer_json(root),
        'requirements_txt': analyze_requirements_txt(root),
        'gemfile': analyze_gemfile(root),
    }

    # Remove None values
    result = {k: v for k, v in result.items() if v is not None}

    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
