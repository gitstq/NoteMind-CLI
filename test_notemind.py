#!/usr/bin/env python3
"""
🧪 NoteMind-CLI Test Suite
"""

import os
import sys
import json
import tempfile
import shutil
import unittest
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from notemind import (
    generate_id, get_current_time, extract_tags_from_content,
    extract_title_from_content, generate_summary, count_words,
    create_note, read_note, update_note, delete_note,
    search_notes, list_notes, get_all_tags, get_stats,
    build_knowledge_graph, find_related_notes,
    Config, Note, load_config, save_config,
    load_index, save_index
)


class TestNoteMindCore(unittest.TestCase):
    """Test core NoteMind functionality."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp(prefix="notemind_test_")
        self.notes_dir = os.path.join(self.test_dir, "notes")
        self.config_dir = os.path.join(self.test_dir, ".notemind")
        os.makedirs(self.notes_dir, exist_ok=True)
        os.makedirs(self.config_dir, exist_ok=True)

        # Mock config
        self.config = Config(
            notes_dir=self.notes_dir,
            editor="nano",
            default_tags=["test"]
        )

        # Override global paths for testing
        import notemind
        notemind.DEFAULT_CONFIG_DIR = self.config_dir
        notemind.CONFIG_FILE = os.path.join(self.config_dir, "config.json")
        notemind.INDEX_FILE = os.path.join(self.config_dir, "index.json")
        notemind.DEFAULT_NOTES_DIR = self.notes_dir

    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_generate_id(self):
        """Test ID generation."""
        note_id = generate_id("test content")
        self.assertIsNotNone(note_id)
        self.assertIn("-", note_id)
        self.assertEqual(len(note_id.split("-")[0]), 14)  # timestamp part

    def test_extract_tags(self):
        """Test tag extraction from content."""
        content = "This is a #python note about #coding and #AI"
        tags = extract_tags_from_content(content)
        self.assertIn("python", tags)
        self.assertIn("coding", tags)
        self.assertIn("AI", tags)

    def test_extract_title(self):
        """Test title extraction."""
        content = "# My Awesome Note\n\nSome content here"
        title = extract_title_from_content(content)
        self.assertEqual(title, "My Awesome Note")

    def test_generate_summary(self):
        """Test summary generation."""
        content = "This is a very long note with lots of content that should be summarized"
        summary = generate_summary(content, max_length=20)
        self.assertLessEqual(len(summary), 25)
        self.assertTrue(summary.endswith("..."))

    def test_count_words(self):
        """Test word counting."""
        content = "Hello world this is a test"
        count = count_words(content)
        self.assertEqual(count, 6)

    def test_create_note(self):
        """Test note creation."""
        note = create_note(
            self.config,
            title="Test Note",
            content="# Test Note\n\nThis is a test #note",
            tags=["test"]
        )
        self.assertIsNotNone(note)
        self.assertEqual(note.title, "Test Note")
        self.assertIn("note", note.tags)
        self.assertTrue(os.path.exists(note.file_path))

    def test_read_note(self):
        """Test note reading."""
        note = create_note(
            self.config,
            title="Read Test",
            content="# Read Test\n\nContent here"
        )
        read = read_note(note.id)
        self.assertIsNotNone(read)
        self.assertEqual(read.title, "Read Test")

    def test_update_note(self):
        """Test note update."""
        note = create_note(
            self.config,
            title="Update Test",
            content="# Update Test"
        )
        updated = update_note(note.id, title="Updated Title")
        self.assertIsNotNone(updated)
        self.assertEqual(updated.title, "Updated Title")

    def test_delete_note(self):
        """Test note deletion."""
        note = create_note(
            self.config,
            title="Delete Test",
            content="# Delete Test"
        )
        result = delete_note(note.id)
        self.assertTrue(result)
        self.assertIsNone(read_note(note.id))

    def test_search_notes(self):
        """Test note search."""
        create_note(self.config, title="Python Guide", content="# Python\n\nGuide")
        create_note(self.config, title="JavaScript Tips", content="# JS\n\nTips")

        results = search_notes("python")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Python Guide")

    def test_list_notes(self):
        """Test note listing."""
        create_note(self.config, title="Note 1", content="# Note 1", tags=["tag1"])
        create_note(self.config, title="Note 2", content="# Note 2", tags=["tag2"])

        all_notes = list_notes()
        self.assertEqual(len(all_notes), 2)

        filtered = list_notes(tag="tag1")
        self.assertEqual(len(filtered), 1)

    def test_get_all_tags(self):
        """Test tag listing."""
        create_note(self.config, title="Note 1", content="# Note 1", tags=["python"])
        create_note(self.config, title="Note 2", content="# Note 2", tags=["python", "coding"])

        tags = get_all_tags()
        self.assertEqual(len(tags), 2)
        self.assertEqual(tags[0][0], "python")
        self.assertEqual(tags[0][1], 2)

    def test_get_stats(self):
        """Test statistics."""
        create_note(self.config, title="Stats Test", content="# Stats\n\nSome content here")
        stats = get_stats()
        self.assertEqual(stats["total_notes"], 1)
        self.assertGreater(stats["total_words"], 0)

    def test_knowledge_graph(self):
        """Test knowledge graph building."""
        create_note(self.config, title="Note 1", content="# N1", tags=["shared"])
        create_note(self.config, title="Note 2", content="# N2", tags=["shared"])

        graph = build_knowledge_graph()
        self.assertEqual(len(graph["nodes"]), 2)
        self.assertEqual(len(graph["edges"]), 1)

    def test_find_related(self):
        """Test finding related notes."""
        n1 = create_note(self.config, title="Note 1", content="# N1", tags=["tag"])
        n2 = create_note(self.config, title="Note 2", content="# N2", tags=["tag"])

        related = find_related_notes(n1.id)
        self.assertEqual(len(related), 1)
        self.assertEqual(related[0][0].id, n2.id)


class TestNoteMindConfig(unittest.TestCase):
    """Test configuration management."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="notemind_config_test_")
        self.config_dir = os.path.join(self.test_dir, ".notemind")
        os.makedirs(self.config_dir, exist_ok=True)

        import notemind
        notemind.DEFAULT_CONFIG_DIR = self.config_dir
        notemind.CONFIG_FILE = os.path.join(self.config_dir, "config.json")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_load_save_config(self):
        """Test config load and save."""
        config = Config(notes_dir="/tmp/notes", editor="vim")
        save_config(config)

        loaded = load_config()
        self.assertEqual(loaded.notes_dir, "/tmp/notes")
        self.assertEqual(loaded.editor, "vim")


if __name__ == "__main__":
    unittest.main(verbosity=2)
