# test_settings.py
"""
Test script to verify environment variables and configuration are loading properly
"""

import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import settings


def test_environment_loading():
    """Test if all environment variables are loaded correctly"""

    print("🔍 Testing Environment Configuration...")
    print("=" * 60)

    # Test required API keys
    print("📋 API Keys Status:")
    print(
        f"✅ COMPOSIO_API_KEY: {'✓ Loaded' if settings.COMPOSIO_API_KEY else '❌ Missing'}"
    )
    print(
        f"✅ NEBIUS_API_KEY: {'✓ Loaded' if settings.NEBIUS_API_KEY else '❌ Missing'}"
    )

    # Show first/last 4 chars for security
    if settings.COMPOSIO_API_KEY:
        key_preview = (
            f"{settings.COMPOSIO_API_KEY[:4]}...{settings.COMPOSIO_API_KEY[-4:]}"
        )
        print(f"   Preview: {key_preview}")

    if settings.NEBIUS_API_KEY:
        key_preview = f"{settings.NEBIUS_API_KEY[:4]}...{settings.NEBIUS_API_KEY[-4:]}"
        print(f"   Preview: {key_preview}")

    print("\n🤖 Nebius LLM Configuration:")
    print(f"✅ Model: {settings.NEBIUS_MODEL}")
    print(f"✅ Base URL: {settings.NEBIUS_BASE_URL}")

    print("\n📂 Project Configuration:")
    print(f"✅ Target Repository: {settings.TARGET_REPOSITORY}")
    print(f"✅ Entity ID: {settings.ENTITY_ID}")
    print(f"✅ Bug Label: {settings.BUG_LABEL}")
    print(f"✅ Meeting Duration: {settings.MEETING_DURATION_MINUTES} minutes")

    print("\n" + "=" * 60)

    # Validation checks
    errors = []

    if not settings.COMPOSIO_API_KEY:
        errors.append("COMPOSIO_API_KEY is missing")

    if not settings.NEBIUS_API_KEY:
        errors.append("NEBIUS_API_KEY is missing")

    if errors:
        print("❌ Configuration Errors Found:")
        for error in errors:
            print(f"   - {error}")
        print("\n💡 Make sure to:")
        print("   1. Create a .env file in the backend/ directory")
        print("   2. Add your API keys to the .env file")
        print("   3. Format: COMPOSIO_API_KEY=your_key_here")
        return False
    else:
        print("✅ All Configuration Tests Passed!")
        print("🚀 Ready to proceed with the next component!")
        return True


def test_env_file_exists():
    """Check if .env file exists"""
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        print(f"✅ .env file found at: {env_path}")
        return True
    else:
        print(f"❌ .env file not found at: {env_path}")
        print("💡 Create a .env file with your API keys")
        return False


if __name__ == "__main__":
    print("🧪 Configuration Test Suite")
    print("=" * 60)

    # Test 1: Check .env file
    print("\n📁 Test 1: Environment File Check")
    env_exists = test_env_file_exists()

    # Test 2: Load and validate settings
    print("\n⚙️  Test 2: Settings Validation")
    settings_valid = test_environment_loading()

    # Final result
    print("\n" + "=" * 60)
    if env_exists and settings_valid:
        print("🎉 ALL TESTS PASSED! Configuration is ready!")
        print("✅ You can now proceed to build the next component")
    else:
        print("⚠️  Some tests failed. Fix the issues above before continuing.")

    print("=" * 60)
