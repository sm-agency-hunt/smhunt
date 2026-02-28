#!/usr/bin/env python3
"""
SMHunt Setup Script
Automated setup and initialization for SMHunt Client Acquisition Agent
"""

import os
import sys
import subprocess
import getpass
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def print_step(step, description):
    """Print step with description"""
    print(f"\n🔹 {step}. {description}")


def check_python_version():
    """Check if Python 3.9+ is installed"""
    print_step(1, "Checking Python version")

    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9+ is required")
        print(f"   Current version: {version.major}.{version.minor}")
        return False

    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True


def create_virtual_environment():
    """Create virtual environment"""
    print_step(2, "Creating virtual environment")

    try:
        if not os.path.exists("venv"):
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
            print("✅ Virtual environment created")
        else:
            print("✅ Virtual environment already exists")
        return True
    except Exception as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False


def activate_and_install_requirements():
    """Activate virtual environment and install requirements"""
    print_step(3, "Installing dependencies")

    try:
        # Determine the pip executable path
        if os.name == 'nt':  # Windows
            pip_path = os.path.join("venv", "Scripts", "pip.exe")
        else:  # Unix/Linux/Mac
            pip_path = os.path.join("venv", "bin", "pip")

        # Install requirements
        subprocess.run([pip_path, "install", "-r", "requirements.txt"],
                       check=True)
        print("✅ Dependencies installed successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def setup_environment_file():
    """Setup environment configuration file"""
    print_step(4, "Setting up environment configuration")

    if os.path.exists(".env"):
        print("✅ Environment file already exists")
        return True

    try:
        # Copy example file
        with open(".env.example", "r") as src, open(".env", "w") as dst:
            dst.write(src.read())

        print("✅ Environment file created from example")
        print("   Please edit .env file with your configuration")
        return True
    except Exception as e:
        print(f"❌ Failed to create environment file: {e}")
        return False


def get_database_config():
    """Get database configuration from user"""
    print_step(5, "Database Configuration")

    print("\nPlease enter your PostgreSQL database configuration:")

    db_host = (input("   Database host (default: localhost): ")
               ).strip() or "localhost"
    db_port = input("   Database port (default: 5432): ").strip() or "5432"
    db_name = input("   Database name (default: smhunt): ").strip() or "smhunt"
    db_user = input("   Database username: ").strip()
    db_pass = getpass.getpass("   Database password: ")

    if not db_user or not db_pass:
        print("❌ Database username and password are required")
        return None

    return f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"


def get_api_keys():
    """Get API keys from user"""
    print_step(6, "API Key Configuration")

    print("\nPlease enter your API keys (press Enter to skip):")

    keys = {}
    keys['OPENAI_API_KEY'] = input("   OpenAI API Key: ").strip()
    keys['ANTHROPIC_API_KEY'] = input("   Anthropic API Key: ").strip()
    keys['GOOGLE_MAPS_API_KEY'] = input("   Google Maps API Key: ").strip()
    keys['SENDGRID_API_KEY'] = input("   SendGrid API Key: ").strip()

    return keys


def update_env_file():
    """Update environment file with user configuration"""
    if not os.path.exists(".env"):
        print("❌ Environment file not found")
        return False

    try:
        # Get user configuration
        database_url = get_database_config()
        if not database_url:
            return False

        api_keys = get_api_keys()

        # Read current .env file
        with open(".env", "r") as f:
            lines = f.readlines()

        # Update configuration
        updated_lines = []
        for line in lines:
            if line.startswith("DATABASE_URL="):
                updated_lines.append(f"DATABASE_URL={database_url}\n")
            elif (line.startswith("OPENAI_API_KEY=") and
                  api_keys.get('OPENAI_API_KEY')):
                updated_lines.append(f"OPENAI_API_KEY="
                                     f"{api_keys['OPENAI_API_KEY']}\n")
            elif (line.startswith("ANTHROPIC_API_KEY=") and
                  api_keys.get('ANTHROPIC_API_KEY')):
                updated_lines.append(f"ANTHROPIC_API_KEY="
                                     f"{api_keys['ANTHROPIC_API_KEY']}\n")
            elif (line.startswith("GOOGLE_MAPS_API_KEY=") and
                  api_keys.get('GOOGLE_MAPS_API_KEY')):
                updated_lines.append(f"GOOGLE_MAPS_API_KEY="
                                     f"{api_keys['GOOGLE_MAPS_API_KEY']}\n")
            elif (line.startswith("SENDGRID_API_KEY=") and
                  api_keys.get('SENDGRID_API_KEY')):
                updated_lines.append(f"SENDGRID_API_KEY="
                                     f"{api_keys['SENDGRID_API_KEY']}\n")
            elif line.startswith("SECRET_KEY="):
                import secrets
                secret_key = secrets.token_urlsafe(32)
                updated_lines.append(f"SECRET_KEY={secret_key}\n")
            else:
                updated_lines.append(line)

        # Write updated configuration
        with open(".env", "w") as f:
            f.writelines(updated_lines)

        print("✅ Environment configuration updated successfully")
        return True

    except Exception as e:
        print(f"❌ Failed to update environment configuration: {e}")
        return False


def create_logs_directory():
    """Create logs directory"""
    print_step(7, "Creating logs directory")

    try:
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        print("✅ Logs directory created")
        return True
    except Exception as e:
        print(f"❌ Failed to create logs directory: {e}")
        return False


def test_database_connection():
    """Test database connection"""
    print_step(8, "Testing database connection")

    try:
        # Add src to Python path
        src_path = os.path.join(os.path.dirname(__file__), 'src')
        sys.path.insert(0, src_path)

        # Import and test database connection
        from src.database.connection import health_check

        if health_check():
            print("✅ Database connection successful")
            return True
        else:
            print("❌ Database connection failed")
            return False

    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        return False


def final_setup_message():
    """Display final setup completion message"""
    print_header("SETUP COMPLETE")
    print("\n🎉 SMHunt has been successfully configured!")
    print("\n🚀 Next Steps:")
    print("   1. Start the application: python main.py")
    print("   2. Access the API documentation: http://localhost:8000/docs")
    print("   3. Login with default credentials:")
    print("      - Email: admin@smhunt.online")
    print("      - Password: admin123")
    print("\n📋 For detailed usage instructions, see README.md")
    print("\n⚠️  Important Security Note:")
    print("   - Change the default admin password immediately")
    print("   - Keep your API keys secure and never commit them")
    print("     to version control")
    print("   - Review and customize your .env configuration")


def main():
    """Main setup function"""
    print_header("SMHUNT AUTONOMOUS CLIENT ACQUISITION AGENT SETUP")

    # Run setup steps
    steps = [
        check_python_version,
        create_virtual_environment,
        activate_and_install_requirements,
        setup_environment_file,
        update_env_file,
        create_logs_directory,
        test_database_connection
    ]

    for step_func in steps:
        if not step_func():
            print(f"\n❌ Setup failed at step: {step_func.__name__}")
            print("Please check the error above and try again.")
            return False

    final_setup_message()
    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        sys.exit(1)
