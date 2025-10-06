#!/usr/bin/env python
"""
Pre-deployment test script
"""
import os
import sys
import django
import subprocess

def check_requirements():
    """Check if all required packages are available"""
    print("🔍 Checking requirements...")
    
    required_packages = [
        'Django==5.2.7',
        'djangorestframework==3.15.2', 
        'django-cors-headers==4.4.0',
        'Pillow==10.0.0',
        'whitenoise==6.5.0'
    ]
    
    try:
        result = subprocess.run(['pip', 'freeze'], capture_output=True, text=True)
        installed = result.stdout
        
        for package in required_packages:
            package_name = package.split('==')[0].lower()
            if package_name not in installed.lower():
                print(f"❌ Missing: {package}")
                return False
            else:
                print(f"✅ Found: {package_name}")
        
        return True
    except Exception as e:
        print(f"❌ Error checking requirements: {e}")
        return False

def test_django_settings():
    """Test Django configuration"""
    print("\n🔍 Testing Django settings...")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geomap_project.settings')
        django.setup()
        
        from django.conf import settings
        from django.core.management import execute_from_command_line
        
        # Test critical settings
        assert hasattr(settings, 'ALLOWED_HOSTS'), "ALLOWED_HOSTS not configured"
        assert '.vercel.app' in settings.ALLOWED_HOSTS, "Vercel domains not in ALLOWED_HOSTS"
        assert 'whitenoise' in str(settings.MIDDLEWARE), "WhiteNoise not configured"
        
        print("✅ Django settings look good")
        return True
        
    except Exception as e:
        print(f"❌ Django settings error: {e}")
        return False

def test_static_files():
    """Test static files configuration"""
    print("\n🔍 Testing static files...")
    
    try:
        from django.conf import settings
        
        # Check static files settings
        assert settings.STATIC_URL, "STATIC_URL not set"
        assert settings.STATIC_ROOT, "STATIC_ROOT not set"
        assert 'staticfiles_build' in settings.STATIC_ROOT, "Incorrect STATIC_ROOT path"
        
        print("✅ Static files configuration looks good")
        return True
        
    except Exception as e:
        print(f"❌ Static files error: {e}")
        return False

def test_database():
    """Test database connection and basic operations"""
    print("\n🔍 Testing database...")
    
    try:
        from django.db import connection
        from maps.models import GeoJSONFile, MapLayer
        
        # Test database connection
        connection.ensure_connection()
        
        # Test model imports
        assert GeoJSONFile, "GeoJSONFile model not accessible"
        assert MapLayer, "MapLayer model not accessible"
        
        print("✅ Database connection and models work")
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def check_vercel_files():
    """Check if Vercel configuration files exist"""
    print("\n🔍 Checking Vercel configuration...")
    
    required_files = [
        'vercel.json',
        'build_files.sh',
        'requirements.txt'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ Found: {file}")
        else:
            print(f"❌ Missing: {file}")
            all_exist = False
    
    return all_exist

def main():
    """Run all pre-deployment checks"""
    print("🚀 Pre-deployment checks for Vercel\n")
    
    checks = [
        ("Requirements", check_requirements),
        ("Vercel Files", check_vercel_files),
        ("Django Settings", test_django_settings),
        ("Static Files", test_static_files),
        ("Database", test_database),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"❌ {name} check failed: {e}")
            results.append(False)
    
    print(f"\n{'='*50}")
    if all(results):
        print("🎉 All checks passed! Ready for Vercel deployment")
        print("\nNext steps:")
        print("1. Push your code to GitHub/GitLab")
        print("2. Connect repository to Vercel")
        print("3. Deploy!")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == '__main__':
    main()