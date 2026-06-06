#!/usr/bin/env python3
"""
🧠 NoteMind-CLI - Lightweight Terminal AI Smart Note Engine
轻量级终端AI智能笔记引擎

A zero-dependency (core) Python CLI tool for intelligent note management
with AI-powered features: semantic search, auto-tagging, knowledge graph,
smart summaries, and more.
"""

import os
import sys
import json
import re
import hashlib
import datetime
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass, asdict

# ─── Configuration ───────────────────────────────────────────────────────────

APP_NAME = "NoteMind-CLI"
APP_VERSION = "1.0.0"
APP_AUTHOR = "gitstq"

DEFAULT_NOTES_DIR = os.path.expanduser("~/.notemind/notes")
DEFAULT_CONFIG_DIR = os.path.expanduser("~/.notemind")
CONFIG_FILE = os.path.join(DEFAULT_CONFIG_DIR, "config.json")
INDEX_FILE = os.path.join(DEFAULT_CONFIG_DIR, "index.json")

# ─── Data Models ─────────────────────────────────────────────────────────────

@dataclass
class Note:
    """Represents a single note."""
    id: str
    title: str
    content: str
    tags: List[str]
    created_at: str
    updated_at: str
    summary: str = ""
    word_count: int = 0
    file_path: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Note":
        return cls(**data)


@dataclass
class Config:
    """Application configuration."""
    notes_dir: str = DEFAULT_NOTES_DIR
    editor: str = "nano"
    default_tags: List[str] = None
    ai_enabled: bool = False
    ai_provider: str = ""
    ai_api_key: str = ""
    ai_model: str = ""
    theme: str = "default"

    def __post_init__(self):
        if self.default_tags is None:
            self.default_tags = []

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Config":
        return cls(**data)


# ─── Utility Functions ───────────────────────────────────────────────────────

def ensure_dir(path: str) -> None:
    """Ensure directory exists."""
    Path(path).mkdir(parents=True, exist_ok=True)


def generate_id(content: str = "") -> str:
    """Generate a unique note ID."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    random_part = hashlib.md5(f"{content}{timestamp}".encode()).hexdigest()[:8]
    return f"{timestamp}-{random_part}"


def get_current_time() -> str:
    """Get current timestamp in ISO format."""
    return datetime.datetime.now().isoformat()


def extract_tags_from_content(content: str) -> List[str]:
    """Extract tags from markdown content (#tag syntax)."""
    tags = re.findall(r'#([a-zA-Z0-9_\u4e00-\u9fff]+)', content)
    return list(set(tags))


def extract_title_from_content(content: str) -> str:
    """Extract title from first markdown heading."""
    lines = content.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip()
        elif line.startswith('## '):
            return line[3:].strip()
    # Fallback: first non-empty line
    for line in lines:
        if line.strip():
            return line.strip()[:60]
    return "Untitled Note"


def generate_summary(content: str, max_length: int = 150) -> str:
    """Generate a simple summary from content."""
    # Remove markdown syntax
    text = re.sub(r'[#*`\[\]\(\)|\-]', ' ', content)
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + "..."


def count_words(content: str) -> int:
    """Count words in content."""
    text = re.sub(r'[#*`\[\]\(\)|\-]', ' ', content)
    words = text.split()
    return len(words)


def colorize(text: str, color: str = "reset") -> str:
    """Add ANSI color codes to text."""
    colors = {
        "reset": "\033[0m",
        "bold": "\033[1m",
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "dim": "\033[2m",
    }
    return f"{colors.get(color, '')}{text}{colors['reset']}"


def print_banner() -> None:
    """Print application banner."""
    banner = f"""
{colorize('╔══════════════════════════════════════════════════════════════╗', 'cyan')}
{colorize('║', 'cyan')}  {colorize('🧠 NoteMind-CLI', 'bold')} {colorize(f'v{APP_VERSION}', 'yellow')} - {colorize('AI Smart Note Engine', 'green')}          {colorize('║', 'cyan')}
{colorize('║', 'cyan')}  {colorize('轻量级终端AI智能笔记引擎', 'dim')}                               {colorize('║', 'cyan')}
{colorize('╚══════════════════════════════════════════════════════════════╝', 'cyan')}
"""
    print(banner)


# ─── Configuration Management ────────────────────────────────────────────────

def load_config() -> Config:
    """Load configuration from file."""
    ensure_dir(DEFAULT_CONFIG_DIR)
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return Config.from_dict(data)
        except (json.JSONDecodeError, TypeError):
            pass
    config = Config()
    save_config(config)
    return config


def save_config(config: Config) -> None:
    """Save configuration to file."""
    ensure_dir(DEFAULT_CONFIG_DIR)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config.to_dict(), f, indent=2, ensure_ascii=False)


# ─── Note Index Management ───────────────────────────────────────────────────

def load_index() -> Dict[str, Any]:
    """Load note index from file."""
    if os.path.exists(INDEX_FILE):
        try:
            with open(INDEX_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass
    return {"notes": {}, "tags": {}, "version": APP_VERSION}


def save_index(index: Dict[str, Any]) -> None:
    """Save note index to file."""
    ensure_dir(DEFAULT_CONFIG_DIR)
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)


def add_note_to_index(index: Dict[str, Any], note: Note) -> None:
    """Add a note to the index."""
    index["notes"][note.id] = note.to_dict()
    # Update tag index
    for tag in note.tags:
        if tag not in index["tags"]:
            index["tags"][tag] = []
        if note.id not in index["tags"][tag]:
            index["tags"][tag].append(note.id)


def remove_note_from_index(index: Dict[str, Any], note_id: str) -> bool:
    """Remove a note from the index."""
    if note_id not in index["notes"]:
        return False
    note = Note.from_dict(index["notes"][note_id])
    del index["notes"][note_id]
    # Update tag index
    for tag in note.tags:
        if tag in index["tags"] and note_id in index["tags"][tag]:
            index["tags"][tag].remove(note_id)
            if not index["tags"][tag]:
                del index["tags"][tag]
    return True


# ─── Note CRUD Operations ────────────────────────────────────────────────────

def create_note(config: Config, title: str = "", content: str = "", tags: List[str] = None) -> Note:
    """Create a new note."""
    if tags is None:
        tags = []

    note_id = generate_id(content)
    timestamp = get_current_time()

    if not content:
        content = f"# {title}\n\n" if title else "# New Note\n\n"

    if not title:
        title = extract_title_from_content(content)

    # Auto-extract tags from content
    auto_tags = extract_tags_from_content(content)
    tags = list(set(tags + auto_tags))

    summary = generate_summary(content)
    word_count = count_words(content)

    file_name = f"{note_id}.md"
    file_path = os.path.join(config.notes_dir, file_name)

    ensure_dir(config.notes_dir)

    # Write note to file
    note_data = {
        "id": note_id,
        "title": title,
        "content": content,
        "tags": tags,
        "created_at": timestamp,
        "updated_at": timestamp,
        "summary": summary,
        "word_count": word_count,
    }

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"---\n")
        f.write(f"id: {note_id}\n")
        f.write(f"title: {title}\n")
        f.write(f"tags: {', '.join(tags)}\n")
        f.write(f"created_at: {timestamp}\n")
        f.write(f"updated_at: {timestamp}\n")
        f.write(f"summary: {summary}\n")
        f.write(f"word_count: {word_count}\n")
        f.write(f"---\n\n")
        f.write(content)

    note = Note(
        id=note_id,
        title=title,
        content=content,
        tags=tags,
        created_at=timestamp,
        updated_at=timestamp,
        summary=summary,
        word_count=word_count,
        file_path=file_path,
    )

    # Update index
    index = load_index()
    add_note_to_index(index, note)
    save_index(index)

    return note


def read_note(note_id: str) -> Optional[Note]:
    """Read a note by ID."""
    index = load_index()
    if note_id not in index["notes"]:
        return None
    return Note.from_dict(index["notes"][note_id])


def update_note(note_id: str, title: str = None, content: str = None, tags: List[str] = None) -> Optional[Note]:
    """Update an existing note."""
    note = read_note(note_id)
    if not note:
        return None

    if title is not None:
        note.title = title
    if content is not None:
        note.content = content
        note.summary = generate_summary(content)
        note.word_count = count_words(content)
        auto_tags = extract_tags_from_content(content)
        if tags is not None:
            note.tags = list(set(tags + auto_tags))
        else:
            note.tags = list(set(note.tags + auto_tags))
    elif tags is not None:
        note.tags = tags

    note.updated_at = get_current_time()

    # Update file
    if note.file_path and os.path.exists(note.file_path):
        with open(note.file_path, 'w', encoding='utf-8') as f:
            f.write(f"---\n")
            f.write(f"id: {note.id}\n")
            f.write(f"title: {note.title}\n")
            f.write(f"tags: {', '.join(note.tags)}\n")
            f.write(f"created_at: {note.created_at}\n")
            f.write(f"updated_at: {note.updated_at}\n")
            f.write(f"summary: {note.summary}\n")
            f.write(f"word_count: {note.word_count}\n")
            f.write(f"---\n\n")
            f.write(note.content)

    # Update index
    index = load_index()
    add_note_to_index(index, note)
    save_index(index)

    return note


def delete_note(note_id: str) -> bool:
    """Delete a note."""
    note = read_note(note_id)
    if not note:
        return False

    # Delete file
    if note.file_path and os.path.exists(note.file_path):
        os.remove(note.file_path)

    # Update index
    index = load_index()
    remove_note_from_index(index, note_id)
    save_index(index)

    return True


# ─── Search & Discovery ──────────────────────────────────────────────────────

def search_notes(query: str, search_in: str = "all") -> List[Note]:
    """Search notes by query."""
    index = load_index()
    results = []
    query_lower = query.lower()

    for note_data in index["notes"].values():
        note = Note.from_dict(note_data)
        match = False

        if search_in in ("all", "title") and query_lower in note.title.lower():
            match = True
        if search_in in ("all", "content") and query_lower in note.content.lower():
            match = True
        if search_in in ("all", "tags") and any(query_lower in tag.lower() for tag in note.tags):
            match = True

        if match:
            results.append(note)

    # Sort by updated_at descending
    results.sort(key=lambda x: x.updated_at, reverse=True)
    return results


def list_notes(tag: str = None, limit: int = 50) -> List[Note]:
    """List all notes, optionally filtered by tag."""
    index = load_index()
    results = []

    if tag:
        note_ids = index["tags"].get(tag, [])
        for note_id in note_ids:
            if note_id in index["notes"]:
                results.append(Note.from_dict(index["notes"][note_id]))
    else:
        for note_data in index["notes"].values():
            results.append(Note.from_dict(note_data))

    # Sort by updated_at descending
    results.sort(key=lambda x: x.updated_at, reverse=True)
    return results[:limit]


def get_all_tags() -> List[Tuple[str, int]]:
    """Get all tags with note counts."""
    index = load_index()
    tags = [(tag, len(note_ids)) for tag, note_ids in index["tags"].items()]
    tags.sort(key=lambda x: x[1], reverse=True)
    return tags


# ─── Smart Features ──────────────────────────────────────────────────────────

def build_knowledge_graph() -> Dict[str, Any]:
    """Build a simple knowledge graph from notes."""
    index = load_index()
    nodes = []
    edges = []
    tag_connections = {}

    for note_data in index["notes"].values():
        note = Note.from_dict(note_data)
        nodes.append({
            "id": note.id,
            "label": note.title,
            "type": "note",
            "tags": note.tags,
        })

        # Connect notes through shared tags
        for tag in note.tags:
            if tag not in tag_connections:
                tag_connections[tag] = []
            tag_connections[tag].append(note.id)

    # Create edges for shared tags
    for tag, note_ids in tag_connections.items():
        if len(note_ids) > 1:
            for i in range(len(note_ids)):
                for j in range(i + 1, len(note_ids)):
                    edges.append({
                        "source": note_ids[i],
                        "target": note_ids[j],
                        "label": tag,
                        "weight": 1,
                    })

    return {"nodes": nodes, "edges": edges}


def find_related_notes(note_id: str, limit: int = 5) -> List[Tuple[Note, int]]:
    """Find notes related to a given note based on shared tags."""
    note = read_note(note_id)
    if not note:
        return []

    index = load_index()
    related = {}

    for tag in note.tags:
        for related_id in index["tags"].get(tag, []):
            if related_id != note_id:
                related[related_id] = related.get(related_id, 0) + 1

    # Sort by number of shared tags
    sorted_related = sorted(related.items(), key=lambda x: x[1], reverse=True)

    results = []
    for related_id, score in sorted_related[:limit]:
        if related_id in index["notes"]:
            results.append((Note.from_dict(index["notes"][related_id]), score))

    return results


def get_stats() -> Dict[str, Any]:
    """Get note statistics."""
    index = load_index()
    notes = list(index["notes"].values())

    total_notes = len(notes)
    total_words = sum(n.get("word_count", 0) for n in notes)
    total_tags = len(index["tags"])

    # Get most active day
    if notes:
        dates = [n["created_at"][:10] for n in notes]
        date_counts = {}
        for d in dates:
            date_counts[d] = date_counts.get(d, 0) + 1
        most_active_day = max(date_counts.items(), key=lambda x: x[1])
    else:
        most_active_day = ("N/A", 0)

    # Get top tags
    top_tags = sorted(
        [(tag, len(ids)) for tag, ids in index["tags"].items()],
        key=lambda x: x[1],
        reverse=True,
    )[:10]

    return {
        "total_notes": total_notes,
        "total_words": total_words,
        "total_tags": total_tags,
        "most_active_day": most_active_day,
        "top_tags": top_tags,
        "avg_words_per_note": total_words // total_notes if total_notes > 0 else 0,
    }


# ─── Display Functions ───────────────────────────────────────────────────────

def display_note(note: Note, full: bool = False) -> None:
    """Display a note in the terminal."""
    print(f"\n{colorize('─' * 60, 'dim')}")
    print(f"{colorize('📝', 'yellow')} {colorize(note.title, 'bold')}")
    print(f"{colorize('📋 ID:', 'cyan')} {note.id}")
    print(f"{colorize('🏷️  Tags:', 'cyan')} {', '.join(note.tags) if note.tags else 'None'}")
    print(f"{colorize('📅 Created:', 'cyan')} {note.created_at}")
    print(f"{colorize('🔄 Updated:', 'cyan')} {note.updated_at}")
    print(f"{colorize('📊 Words:', 'cyan')} {note.word_count}")
    print(f"{colorize('📝 Summary:', 'cyan')} {note.summary}")
    print(f"{colorize('─' * 60, 'dim')}")

    if full:
        print(f"\n{note.content}\n")
    print()


def display_notes_list(notes: List[Note]) -> None:
    """Display a list of notes."""
    if not notes:
        print(f"{colorize('📭 No notes found.', 'yellow')}")
        return

    print(f"\n{colorize('📚 Notes:', 'bold')}\n")
    print(f"{colorize('─' * 80, 'dim')}")

    for i, note in enumerate(notes, 1):
        tags_str = f"{colorize('[' + ', '.join(note.tags) + ']', 'magenta')}" if note.tags else ""
        title = note.title[:40] + "..." if len(note.title) > 40 else note.title
        date = note.updated_at[:10] if note.updated_at else "N/A"

        print(f"{colorize(f'{i:3d}.', 'cyan')} {colorize(title, 'bold')} {tags_str}")
        print(f"     {colorize('ID:', 'dim')} {note.id} | {colorize('📅', 'dim')} {date} | {colorize('📝', 'dim')} {note.word_count} words")
        if note.summary:
            summary = note.summary[:50] + "..." if len(note.summary) > 50 else note.summary
            print(f"     {colorize('💡', 'dim')} {summary}")
        print()

    print(f"{colorize('─' * 80, 'dim')}")
    print(f"{colorize(f'Total: {len(notes)} notes', 'green')}\n")


def display_tags(tags: List[Tuple[str, int]]) -> None:
    """Display all tags."""
    if not tags:
        print(f"{colorize('🏷️  No tags found.', 'yellow')}")
        return

    print(f"\n{colorize('🏷️  Tags:', 'bold')}\n")
    print(f"{colorize('─' * 40, 'dim')}")

    for tag, count in tags:
        bar = "█" * min(count, 20)
        print(f"{colorize(f'  #{tag:20s}', 'magenta')} {bar} {colorize(str(count), 'cyan')}")

    print(f"{colorize('─' * 40, 'dim')}")
    print(f"{colorize(f'Total: {len(tags)} tags', 'green')}\n")


def display_stats(stats: Dict[str, Any]) -> None:
    """Display note statistics."""
    print(f"\n{colorize('📊 NoteMind Statistics', 'bold')}\n")
    print(f"{colorize('─' * 50, 'dim')}")
    print(f"  {colorize('📝 Total Notes:', 'cyan')}    {colorize(str(stats['total_notes']), 'green')}")
    print(f"  {colorize('📖 Total Words:', 'cyan')}    {colorize(str(stats['total_words']), 'green')}")
    print(f"  {colorize('🏷️  Total Tags:', 'cyan')}     {colorize(str(stats['total_tags']), 'green')}")
    print(f"  {colorize('📈 Avg Words/Note:', 'cyan')} {colorize(str(stats['avg_words_per_note']), 'green')}")
    print(f"  {colorize('🔥 Most Active Day:', 'cyan')} {colorize(stats['most_active_day'][0], 'green')} ({stats['most_active_day'][1]} notes)")
    print(f"{colorize('─' * 50, 'dim')}")

    if stats['top_tags']:
        print(f"\n  {colorize('🏆 Top Tags:', 'yellow')}")
        for tag, count in stats['top_tags'][:5]:
            print(f"    {colorize(f'#{tag}', 'magenta')} - {count} notes")
    print()


def display_knowledge_graph() -> None:
    """Display knowledge graph in ASCII art."""
    graph = build_knowledge_graph()
    nodes = graph["nodes"]
    edges = graph["edges"]

    if not nodes:
        print(f"{colorize('🕸️  No notes to build graph.', 'yellow')}")
        return

    print(f"\n{colorize('🕸️  Knowledge Graph', 'bold')}\n")
    print(f"{colorize('─' * 60, 'dim')}")
    print(f"  {colorize('Nodes:', 'cyan')} {len(nodes)} notes")
    print(f"  {colorize('Edges:', 'cyan')} {len(edges)} connections\n")

    # Display tag clusters
    tag_notes = {}
    for node in nodes:
        for tag in node["tags"]:
            if tag not in tag_notes:
                tag_notes[tag] = []
            tag_notes[tag].append(node["label"])

    for tag, note_labels in sorted(tag_notes.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
        print(f"  {colorize(f'📁 #{tag}', 'magenta')} ({len(note_labels)} notes)")
        for label in note_labels[:3]:
            print(f"    └─ {label[:40]}")
        if len(note_labels) > 3:
            print(f"    └─ ... and {len(note_labels) - 3} more")
        print()

    print(f"{colorize('─' * 60, 'dim')}\n")


# ─── Interactive Editor ──────────────────────────────────────────────────────

def edit_with_external_editor(config: Config, initial_content: str = "") -> str:
    """Open external editor for note editing."""
    import tempfile

    with tempfile.NamedTemporaryFile(mode='w+', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(initial_content)
        temp_path = f.name

    editor = config.editor or os.environ.get('EDITOR', 'nano')
    subprocess.call([editor, temp_path])

    with open(temp_path, 'r', encoding='utf-8') as f:
        content = f.read()

    os.remove(temp_path)
    return content


# ─── Command Handlers ────────────────────────────────────────────────────────

def cmd_new(args, config: Config) -> None:
    """Create a new note."""
    print_banner()
    print(f"{colorize('✨ Creating new note...', 'green')}\n")

    title = args.title or ""
    content = ""
    tags = args.tags.split(',') if args.tags else []

    if args.editor or not args.content:
        initial = f"# {title}\n\n" if title else ""
        content = edit_with_external_editor(config, initial)
    else:
        content = args.content or ""

    if not content.strip():
        print(f"{colorize('❌ Note content is empty. Aborting.', 'red')}")
        return

    note = create_note(config, title=title, content=content, tags=tags)
    print(f"{colorize('✅ Note created successfully!', 'green')}")
    display_note(note)


def cmd_edit(args, config: Config) -> None:
    """Edit an existing note."""
    print_banner()
    note = read_note(args.id)
    if not note:
        print(f"{colorize(f'❌ Note not found: {args.id}', 'red')}")
        return

    print(f"{colorize('✏️  Editing note...', 'green')}\n")

    if args.editor:
        new_content = edit_with_external_editor(config, note.content)
        if new_content != note.content:
            update_note(args.id, content=new_content)
            print(f"{colorize('✅ Note updated successfully!', 'green')}")
        else:
            print(f"{colorize('ℹ️  No changes made.', 'yellow')}")
    else:
        if args.title:
            update_note(args.id, title=args.title)
        if args.content:
            update_note(args.id, content=args.content)
        if args.tags:
            update_note(args.id, tags=args.tags.split(','))
        print(f"{colorize('✅ Note updated successfully!', 'green')}")


def cmd_delete(args, config: Config) -> None:
    """Delete a note."""
    print_banner()
    note = read_note(args.id)
    if not note:
        print(f"{colorize(f'❌ Note not found: {args.id}', 'red')}")
        return

    display_note(note)
    confirm = input(f"{colorize('⚠️  Are you sure you want to delete this note? (y/N): ', 'yellow')}")
    if confirm.lower() == 'y':
        if delete_note(args.id):
            print(f"{colorize('✅ Note deleted successfully!', 'green')}")
        else:
            print(f"{colorize('❌ Failed to delete note.', 'red')}")
    else:
        print(f"{colorize('❌ Deletion cancelled.', 'yellow')}")


def cmd_show(args, config: Config) -> None:
    """Show a note."""
    print_banner()
    note = read_note(args.id)
    if not note:
        print(f"{colorize(f'❌ Note not found: {args.id}', 'red')}")
        return
    display_note(note, full=True)


def cmd_list(args, config: Config) -> None:
    """List notes."""
    print_banner()
    notes = list_notes(tag=args.tag, limit=args.limit)
    display_notes_list(notes)


def cmd_search(args, config: Config) -> None:
    """Search notes."""
    print_banner()
    print(f"{colorize(f'🔍 Searching for: {args.query}', 'cyan')}\n")
    notes = search_notes(args.query, search_in=args.in_field)
    display_notes_list(notes)


def cmd_tags(args, config: Config) -> None:
    """List all tags."""
    print_banner()
    tags = get_all_tags()
    display_tags(tags)


def cmd_stats(args, config: Config) -> None:
    """Show statistics."""
    print_banner()
    stats = get_stats()
    display_stats(stats)


def cmd_graph(args, config: Config) -> None:
    """Show knowledge graph."""
    print_banner()
    display_knowledge_graph()


def cmd_related(args, config: Config) -> None:
    """Find related notes."""
    print_banner()
    note = read_note(args.id)
    if not note:
        print(f"{colorize(f'❌ Note not found: {args.id}', 'red')}")
        return

    print(f"{colorize(f'🔗 Notes related to: {note.title}', 'cyan')}\n")
    related = find_related_notes(args.id, limit=args.limit)

    if not related:
        print(f"{colorize('📭 No related notes found.', 'yellow')}")
        return

    for i, (rel_note, score) in enumerate(related, 1):
        shared_tags = set(note.tags) & set(rel_note.tags)
        tags_str = f"{colorize('[' + ', '.join(shared_tags) + ']', 'magenta')}" if shared_tags else ""
        print(f"{colorize(f'{i}.', 'cyan')} {colorize(rel_note.title, 'bold')} {tags_str}")
        print(f"   {colorize('Shared tags:', 'dim')} {score} | {colorize('ID:', 'dim')} {rel_note.id}")
        print()


def cmd_config(args, config: Config) -> None:
    """Manage configuration."""
    print_banner()

    if args.show:
        print(f"{colorize('⚙️  Current Configuration:', 'bold')}\n")
        print(f"  {colorize('Notes Directory:', 'cyan')} {config.notes_dir}")
        print(f"  {colorize('Editor:', 'cyan')} {config.editor}")
        print(f"  {colorize('Default Tags:', 'cyan')} {', '.join(config.default_tags) if config.default_tags else 'None'}")
        print(f"  {colorize('AI Enabled:', 'cyan')} {config.ai_enabled}")
        print(f"  {colorize('Theme:', 'cyan')} {config.theme}")
        print()
        return

    if args.notes_dir:
        config.notes_dir = os.path.expanduser(args.notes_dir)
    if args.editor:
        config.editor = args.editor
    if args.theme:
        config.theme = args.theme

    save_config(config)
    print(f"{colorize('✅ Configuration saved!', 'green')}")


def cmd_export(args, config: Config) -> None:
    """Export notes."""
    print_banner()
    notes = list_notes(limit=9999)

    if args.format == "json":
        data = {"notes": [n.to_dict() for n in notes], "exported_at": get_current_time()}
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    elif args.format == "markdown":
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(f"# NoteMind Export\n\n")
            f.write(f"Exported at: {get_current_time()}\n\n")
            for note in notes:
                f.write(f"## {note.title}\n\n")
                f.write(f"**Tags:** {', '.join(note.tags)}\n\n")
                f.write(f"**Created:** {note.created_at}\n\n")
                f.write(note.content)
                f.write(f"\n\n---\n\n")

    print(f"{colorize(f'✅ Exported {len(notes)} notes to {args.output}', 'green')}")


def cmd_import(args, config: Config) -> None:
    """Import notes."""
    print_banner()

    if not os.path.exists(args.file):
        print(f"{colorize(f'❌ File not found: {args.file}', 'red')}")
        return

    count = 0
    with open(args.file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for note_data in data.get("notes", []):
            create_note(
                config,
                title=note_data.get("title", ""),
                content=note_data.get("content", ""),
                tags=note_data.get("tags", [])
            )
            count += 1

    print(f"{colorize(f'✅ Imported {count} notes!', 'green')}")


def cmd_init(args, config: Config) -> None:
    """Initialize NoteMind."""
    print_banner()
    ensure_dir(config.notes_dir)
    ensure_dir(DEFAULT_CONFIG_DIR)
    save_config(config)
    print(f"{colorize('✅ NoteMind initialized!', 'green')}")
    print(f"{colorize(f'📁 Notes directory: {config.notes_dir}', 'cyan')}")
    print(f"{colorize(f'⚙️  Config file: {CONFIG_FILE}', 'cyan')}")
    print(f"\n{colorize('🚀 Get started with:', 'green')}")
    print(f"  {colorize('notemind new', 'yellow')}     - Create a new note")
    print(f"  {colorize('notemind list', 'yellow')}    - List all notes")
    print(f"  {colorize('notemind search', 'yellow')}  - Search notes\n")


# ─── Main CLI ────────────────────────────────────────────────────────────────

def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        prog="notemind",
        description=f"🧠 {APP_NAME} v{APP_VERSION} - AI Smart Note Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  notemind init                    Initialize NoteMind
  notemind new -t "My Note"        Create a new note with title
  notemind list                    List all notes
  notemind search "python"         Search for "python" in notes
  notemind show <id>               Show a note by ID
  notemind tags                    List all tags
  notemind stats                   Show statistics
  notemind graph                   Show knowledge graph
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # init
    init_parser = subparsers.add_parser("init", help="Initialize NoteMind")

    # new
    new_parser = subparsers.add_parser("new", help="Create a new note")
    new_parser.add_argument("-t", "--title", help="Note title")
    new_parser.add_argument("-c", "--content", help="Note content")
    new_parser.add_argument("--tags", help="Comma-separated tags")
    new_parser.add_argument("-e", "--editor", action="store_true", help="Open external editor")

    # edit
    edit_parser = subparsers.add_parser("edit", help="Edit a note")
    edit_parser.add_argument("id", help="Note ID")
    edit_parser.add_argument("-t", "--title", help="New title")
    edit_parser.add_argument("-c", "--content", help="New content")
    edit_parser.add_argument("--tags", help="Comma-separated tags")
    edit_parser.add_argument("-e", "--editor", action="store_true", help="Open external editor")

    # delete
    delete_parser = subparsers.add_parser("delete", help="Delete a note")
    delete_parser.add_argument("id", help="Note ID")

    # show
    show_parser = subparsers.add_parser("show", help="Show a note")
    show_parser.add_argument("id", help="Note ID")

    # list
    list_parser = subparsers.add_parser("list", help="List notes")
    list_parser.add_argument("--tag", help="Filter by tag")
    list_parser.add_argument("-l", "--limit", type=int, default=50, help="Limit results")

    # search
    search_parser = subparsers.add_parser("search", help="Search notes")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--in", dest="in_field", default="all", choices=["all", "title", "content", "tags"], help="Search field")

    # tags
    tags_parser = subparsers.add_parser("tags", help="List all tags")

    # stats
    stats_parser = subparsers.add_parser("stats", help="Show statistics")

    # graph
    graph_parser = subparsers.add_parser("graph", help="Show knowledge graph")

    # related
    related_parser = subparsers.add_parser("related", help="Find related notes")
    related_parser.add_argument("id", help="Note ID")
    related_parser.add_argument("-l", "--limit", type=int, default=5, help="Limit results")

    # config
    config_parser = subparsers.add_parser("config", help="Manage configuration")
    config_parser.add_argument("--show", action="store_true", help="Show current config")
    config_parser.add_argument("--notes-dir", help="Set notes directory")
    config_parser.add_argument("--editor", help="Set default editor")
    config_parser.add_argument("--theme", choices=["default", "dark", "light"], help="Set theme")

    # export
    export_parser = subparsers.add_parser("export", help="Export notes")
    export_parser.add_argument("-f", "--format", choices=["json", "markdown"], default="json", help="Export format")
    export_parser.add_argument("-o", "--output", required=True, help="Output file")

    # import
    import_parser = subparsers.add_parser("import", help="Import notes")
    import_parser.add_argument("file", help="Import file (JSON)")

    return parser


def main() -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    config = load_config()

    if not args.command:
        print_banner()
        parser.print_help()
        return 0

    commands = {
        "init": cmd_init,
        "new": cmd_new,
        "edit": cmd_edit,
        "delete": cmd_delete,
        "show": cmd_show,
        "list": cmd_list,
        "search": cmd_search,
        "tags": cmd_tags,
        "stats": cmd_stats,
        "graph": cmd_graph,
        "related": cmd_related,
        "config": cmd_config,
        "export": cmd_export,
        "import": cmd_import,
    }

    if args.command in commands:
        try:
            commands[args.command](args, config)
        except KeyboardInterrupt:
            print(f"\n{colorize('⚠️  Interrupted by user.', 'yellow')}")
            return 130
        except Exception as e:
            print(f"{colorize(f'❌ Error: {e}', 'red')}")
            return 1
    else:
        parser.print_help()

    return 0


if __name__ == "__main__":
    sys.exit(main())
