#!/usr/bin/env python3
"""
SMHUNT Production Deployment Script
Handles the complete deployment of SMHUNT services including:
- Backend API service
- Frontend dashboard
- Background workers
- Scheduler services
- Database initialization
"""

import sys
import subprocess
import time
from pathlib import Path
import argparse


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def print_step(step, description):
    """Print step with description"""
    print(f"\n🔹 {step}. {description}")


def check_docker_installed():
    """Check if Docker is installed"""
    print_step(1, "Checking Docker installation")
    
    try:
        result = subprocess.run(
            ["docker", "--version"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        print(f"✅ Docker version: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker is not installed or not in PATH")
        print("   Please install Docker Desktop.")
        return False


def check_docker_compose_installed():
    """Check if Docker Compose is installed"""
    print_step(2, "Checking Docker Compose installation")
    
    try:
        result = subprocess.run(
            ["docker-compose", "--version"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        print(f"✅ Docker Compose version: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            # Try docker compose (newer versions)
            result = subprocess.run(
                ["docker", "compose", "version"], 
                capture_output=True, 
                text=True, 
                check=True
            )
            print(f"✅ Docker Compose version: {result.stdout.strip()}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Docker Compose is not installed")
            return False


def check_env_file():
    """Check if .env file exists"""
    print_step(3, "Checking environment configuration")
    
    env_file = Path(".env")
    if env_file.exists():
        print("✅ Environment file (.env) found")
        return True
    else:
        print("❌ Environment file (.env) not found")
        print("   Please create a .env file with your configuration")
        return False


def build_services():
    """Build all Docker services"""
    print_step(4, "Building Docker services")
    
    try:
        # Build services using production compose file
        subprocess.run(
            [
                "docker-compose", 
                "-f", "docker/docker-compose.prod.yml", 
                "build"
            ], 
            check=True, 
            capture_output=True, 
            text=True
        )
        
        print("✅ Services built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to build services: {e}")
        print(e.output)
        return False


def start_services():
    """Start all services in detached mode"""
    print_step(5, "Starting services")
    
    try:
        # Start all services in detached mode
        subprocess.run(
            [
                "docker-compose", 
                "-f", "docker/docker-compose.prod.yml", 
                "up", "-d"
            ], 
            check=True, 
            capture_output=True, 
            text=True
        )
        
        print("✅ Services started successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start services: {e}")
        print(e.output)
        return False


def wait_for_services():
    """Wait for services to be healthy"""
    print_step(6, "Waiting for services to be ready")
    
    services = ["db", "redis", "backend"]
    
    for service in services:
        print(f"   Waiting for {service}...")
        max_attempts = 30
        attempt = 0
        
        while attempt < max_attempts:
            try:
                # Check if service is running and healthy
                result = subprocess.run(
                    [
                        "docker-compose",
                        "-f", "docker/docker-compose.prod.yml",
                        "ps"
                    ], 
                    capture_output=True, 
                    text=True, 
                    check=True
                )
                
                if service in result.stdout and "Up" in result.stdout:
                    print(f"   ✅ {service} is ready")
                    break
            except subprocess.CalledProcessError:
                pass
            
            attempt += 1
            time.sleep(10)  # Wait 10 seconds between checks
        
        if attempt >= max_attempts:
            print(f"   ⚠️  {service} may not be ready yet (continuing anyway)")
    
    return True


def run_database_migrations():
    """Run database migrations"""
    print_step(7, "Running database migrations")
    
    try:
        # Execute migrations in the backend container
        subprocess.run(
            [
                "docker-compose",
                "-f", "docker/docker-compose.prod.yml",
                "exec", "backend",
                "alembic", "upgrade", "head"
            ], 
            check=True, 
            capture_output=True, 
            text=True
        )
        
        print("✅ Database migrations completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to run migrations: {e}")
        print(e.output)
        return False


def display_deployment_info():
    """Display deployment information"""
    print_step(8, "Deployment Information")
    
    print("\n📊 Services Running:")
    print("   - Backend API: http://localhost:8000")
    print("   - Frontend Dashboard: http://localhost:3000")
    print("   - Public Access: http://localhost (via Nginx)")
    print("   - PostgreSQL: localhost:5432")
    print("   - Redis: localhost:6379")
    
    print("\n🔧 Management Commands:")
    print("   - View logs: docker-compose -f logs -f")
    print("   - Stop services: docker-compose -f down")
    print("   - Restart: docker-compose -f restart")
    print("   - Exec: docker-compose -f exec backend bash")
    
    print("\n🔐 Security Notes:")
    print("   - Change default passwords in .env file")
    print("   - Configure SSL certificates for production")
    print("   - Set up proper firewall rules")
    print("   - Regularly backup your database")


def deploy_production():
    """Complete production deployment"""
    print_header("SMHUNT PRODUCTION DEPLOYMENT")
    
    # Check prerequisites
    if not check_docker_installed():
        return False
    
    if not check_docker_compose_installed():
        return False
    
    if not check_env_file():
        return False
    
    # Build and start services
    if not build_services():
        print("❌ Deployment failed during build phase")
        return False
    
    if not start_services():
        print("❌ Deployment failed during start phase")
        return False
    
    # Wait for services and run migrations
    wait_for_services()
    
    # Run database migrations
    run_database_migrations()
    
    # Display final information
    display_deployment_info()
    
    print_header("DEPLOYMENT COMPLETE")
    print("\n🎉 SMHUNT Production Environment is now running!")
    print("\n🚀 Next Steps:")
    print("   1. Access the admin dashboard at http://localhost:3000")
    print("   2. Monitor logs for any issues")
    print("   3. Configure SSL/TLS for production security")
    print("   4. Set up automated backups for your database")
    print("   5. Configure monitoring and alerting")
    
    return True


def stop_production():
    """Stop production services"""
    print_header("STOPPING SMHUNT PRODUCTION SERVICES")
    
    try:
        subprocess.run(
            [
                "docker-compose", 
                "-f", "docker/docker-compose.prod.yml", 
                "down"
            ], 
            check=True, 
            capture_output=True, 
            text=True
        )
        
        print("✅ Services stopped successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to stop services: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='SMHUNT Production Deployment Tool'
    )
    parser.add_argument(
        'action', 
        choices=['deploy', 'stop'], 
        help='Action to perform: deploy or stop services'
    )
    
    args = parser.parse_args()
    
    if args.action == 'deploy':
        success = deploy_production()
        sys.exit(0 if success else 1)
    elif args.action == 'stop':
        success = stop_production()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()