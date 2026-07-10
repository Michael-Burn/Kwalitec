"""Test that the StartupService fix works correctly."""
import os
import sys
import subprocess

def test_flask_db_upgrade():
    """Test that flask db upgrade completes without hanging."""
    print("Testing flask db upgrade...")
    env = {**os.environ, "FLASK_ENV": "development", "FLASK_APP": "app"}
    
    try:
        result = subprocess.run(
            ["flask", "db", "upgrade"],
            capture_output=True,
            text=True,
            env=env,
            timeout=30  # Add timeout to detect hanging
        )
    except subprocess.TimeoutExpired:
        print("FAILED: flask db upgrade hung (timed out after 30 seconds)")
        return False
    
    # Check both stdout and stderr for the skip message
    output = result.stdout + result.stderr
    
    print(f"Return code: {result.returncode}")
    print(f"Output length: {len(output)}")
    
    if result.returncode != 0:
        print(f"FAILED: flask db upgrade failed with return code {result.returncode}")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        return False
    
    if "Skipping curriculum import during Flask CLI command" not in output:
        print("FAILED: Curriculum import was not skipped during flask db upgrade")
        print("OUTPUT:", output)
        return False
    
    print("✓ flask db upgrade completed successfully")
    print("✓ Curriculum import was correctly skipped during CLI command")
    return True


def test_normal_app_startup():
    """Test that normal application startup imports curricula."""
    print("\nTesting normal application startup...")
    
    # Clean up database first to ensure fresh state
    subprocess.run(["rm", "-f", "instance/kwalitec.sqlite3"], check=True)
    
    # First, run flask db upgrade to create tables
    env = {**os.environ, "FLASK_ENV": "development", "FLASK_APP": "app"}
    upgrade_result = subprocess.run(
        ["flask", "db", "upgrade"],
        env=env,
        capture_output=True,
        text=True
    )
    
    print(f"Upgrade return code: {upgrade_result.returncode}")
    if upgrade_result.returncode != 0:
        print(f"FAILED: flask db upgrade failed in test_normal_app_startup")
        print("STDOUT:", upgrade_result.stdout)
        print("STDERR:", upgrade_result.stderr)
        return False
    
    # Verify the database was created and has the expected tables
    if not os.path.exists("instance/kwalitec.sqlite3"):
        print("FAILED: Database file was not created")
        return False
    
    # Verify curricula table exists
    import sqlite3
    conn = sqlite3.connect("instance/kwalitec.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='curricula'")
    if not cursor.fetchone():
        print("FAILED: curricula table was not created by migrations")
        conn.close()
        return False
    conn.close()
    
    # Create a test script that imports the app
    test_script = """
import sys
import os
os.environ['FLASK_ENV'] = 'development'

# Mock sys.argv to simulate normal app startup (not a CLI command)
sys.argv = ['python', 'app.py']

from app import create_app
app = create_app()

# Check if curricula were imported
from app.models.curriculum import Curriculum
with app.app_context():
    try:
        count = Curriculum.query.count()
        print(f"CURRICULA_COUNT:{count}")
        if count > 0:
            print("✓ Curricula were imported during normal startup")
        else:
            print("✗ No curricula were imported")
            sys.exit(1)
    except Exception as e:
        print(f"✗ Error querying curricula: {e}")
        sys.exit(1)
"""
    
    result = subprocess.run(
        [sys.executable, "-c", test_script],
        capture_output=True,
        text=True,
        cwd=os.getcwd()
    )
    
    print("STDOUT:", result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    if result.returncode != 0:
        print(f"FAILED: Normal app startup test failed with return code {result.returncode}")
        return False
    
    if "CURRICULA_COUNT:0" in result.stdout:
        print("FAILED: No curricula were imported during normal startup")
        return False
    
    return True


def test_curriculum_import_idempotent():
    """Test that curriculum import is idempotent."""
    print("\nTesting curriculum import idempotency...")
    
    # Clean up database first to ensure fresh state
    subprocess.run(["rm", "-f", "instance/kwalitec.sqlite3"], check=True)
    
    # First, run flask db upgrade to create tables
    env = {**os.environ, "FLASK_ENV": "development", "FLASK_APP": "app"}
    upgrade_result = subprocess.run(
        ["flask", "db", "upgrade"],
        env=env,
        capture_output=True,
        text=True
    )
    
    print(f"Upgrade return code: {upgrade_result.returncode}")
    if upgrade_result.returncode != 0:
        print(f"FAILED: flask db upgrade failed in test_curriculum_import_idempotent")
        print("STDOUT:", upgrade_result.stdout)
        print("STDERR:", upgrade_result.stderr)
        return False
    
    # Verify the database was created and has the expected tables
    if not os.path.exists("instance/kwalitec.sqlite3"):
        print("FAILED: Database file was not created")
        return False
    
    # Verify curricula table exists
    import sqlite3
    conn = sqlite3.connect("instance/kwalitec.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='curricula'")
    if not cursor.fetchone():
        print("FAILED: curricula table was not created by migrations")
        conn.close()
        return False
    conn.close()
    
    # Run normal startup twice
    test_script = """
import sys
import os
os.environ['FLASK_ENV'] = 'development'

# Mock sys.argv to simulate normal app startup
sys.argv = ['python', 'app.py']

from app import create_app
app = create_app()

from app.models.curriculum import Curriculum
with app.app_context():
    try:
        count1 = Curriculum.query.count()
    except Exception as e:
        print(f"✗ Error on first count: {e}")
        sys.exit(1)
    
    # Trigger import again
    from app.services.startup_service import StartupService
    StartupService._run_curriculum_import(app)
    
    try:
        count2 = Curriculum.query.count()
    except Exception as e:
        print(f"✗ Error on second count: {e}")
        sys.exit(1)
    
    print(f"FIRST_COUNT:{count1}")
    print(f"SECOND_COUNT:{count2}")
    
    if count1 == count2:
        print("✓ Curriculum import is idempotent")
    else:
        print("✗ Curriculum import is NOT idempotent")
        sys.exit(1)
"""
    
    result = subprocess.run(
        [sys.executable, "-c", test_script],
        capture_output=True,
        text=True,
        cwd=os.getcwd()
    )
    
    print("STDOUT:", result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    if result.returncode != 0:
        print(f"FAILED: Idempotency test failed with return code {result.returncode}")
        return False
    
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("Testing StartupService fix")
    print("=" * 60)
    
    tests = [
        test_flask_db_upgrade,
        test_normal_app_startup,
        test_curriculum_import_idempotent,
    ]
    
    results = []
    for i, test in enumerate(tests):
        try:
            # Clean up database before each test to ensure isolation
            subprocess.run(["rm", "-f", "instance/kwalitec.sqlite3"], check=True)
            print(f"\nCleaned up database before {test.__name__}")
            results.append(test())
        except Exception as e:
            print(f"FAILED: {test.__name__} raised exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if all(results):
        print("✓ ALL TESTS PASSED")
        sys.exit(0)
    else:
        print("✗ SOME TESTS FAILED")
        sys.exit(1)
