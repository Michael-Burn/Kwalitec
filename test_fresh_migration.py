#!/usr/bin/env python3
"""Test script to run migrations on a FRESH database to see full instrumentation."""

from __future__ import annotations

import logging
import shutil
import sys
from pathlib import Path

# Set up logging to show DEBUG level messages
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app import create_app
from app.extensions import db

# Configure logging for our instrumentation
logging.getLogger("alembic.instrumentation").setLevel(logging.DEBUG)
logging.getLogger("alembic").setLevel(logging.INFO)
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


def main():
    """Run migrations on a fresh database with instrumentation."""
    print("=" * 80)
    print("FRESH DATABASE MIGRATION TEST")
    print("=" * 80)
    
    # Create the Flask app
    app = create_app()
    
    with app.app_context():
        # Check database file location
        db_path = db.engine.url.database
        db_file = Path(db_path)
        
        print(f"\nDatabase path: {db_path}")
        
        # Backup and remove existing database to start fresh
        if db_file.exists():
            backup_path = db_file.with_suffix('.sqlite3.backup.test')
            shutil.copy(db_file, backup_path)
            print(f"Backed up existing database to: {backup_path}")
            db_file.unlink()
            print("Removed existing database for fresh migration test")
        
        print(f"Database exists: {db_file.exists()}")
        
        print("\n" + "=" * 80)
        print("RUNNING: flask db upgrade (FRESH DATABASE)")
        print("=" * 80 + "\n")
        
        # Run migrations using Flask-Migrate
        from flask_migrate import upgrade
        upgrade()
        
        print("\n" + "=" * 80)
        print("MIGRATION RUN COMPLETE")
        print("=" * 80)
        
        # Final check
        if db_file.exists():
            print(f"Database size after migration: {db_file.stat().st_size} bytes")
        
        # List all tables
        from sqlalchemy import inspect, text
        with db.engine.connect() as conn:
            inspector = inspect(conn)
            tables = inspector.get_table_names()
            print(f"\nFinal tables in database: {sorted(tables)}")
            
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"))
            sqlite_tables = [row[0] for row in result]
            print(f"Final sqlite_master tables: {sqlite_tables}")


if __name__ == "__main__":
    main()