#!/usr/bin/env python3
"""
Startup script for the Text Processing API
"""

import os
import subprocess
import sys


def start_server():
    """Start the FastAPI server"""
    try:
        print("Starting Text Processing API...")
        print("=" * 50)
        print("🚀 Server will be available at:")
        print("   - API: http://localhost:8000")
        print("   - Interactive Docs: http://localhost:8000/docs")
        print("   - ReDoc: http://localhost:8000/redoc")
        print("=" * 50)
        print("Press Ctrl+C to stop the server")
        print()

        # Change to the directory containing the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)

        # Start the server
        subprocess.run(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "api.main:app",
                "--host",
                "0.0.0.0",
                "--port",
                "8000",
                "--reload",  # Auto-reload on code changes
            ]
        )

    except KeyboardInterrupt:
        print("\n" + "=" * 50)
        print("🛑 Server stopped")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

    return True


if __name__ == "__main__":
    print("Setting up Text Processing API...")

    # Start server
    start_server()
