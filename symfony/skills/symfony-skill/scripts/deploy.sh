#!/bin/bash

# Symfony Deployment Script
# Usage: ./deploy.sh [environment] [branch]
# Example: ./deploy.sh production main

set -e

# Configuration
ENVIRONMENT=${1:-production}
BRANCH=${2:-main}
PROJECT_PATH="/var/www/symfony-app"
BACKUP_PATH="/var/backups/symfony-app"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_requirements() {
    log_info "Checking requirements..."
    
    # Check if PHP is installed
    if ! command -v php &> /dev/null; then
        log_error "PHP is not installed"
        exit 1
    fi
    
    # Check if Composer is installed
    if ! command -v composer &> /dev/null; then
        log_error "Composer is not installed"
        exit 1
    fi
    
    # Check if Git is installed
    if ! command -v git &> /dev/null; then
        log_error "Git is not installed"
        exit 1
    fi
    
    # Check PHP version
    PHP_VERSION=$(php -r "echo PHP_VERSION;")
    MIN_PHP_VERSION="8.1.0"
    
    if [ "$(printf '%s\n' "$MIN_PHP_VERSION" "$PHP_VERSION" | sort -V | head -n1)" != "$MIN_PHP_VERSION" ]; then
        log_error "PHP version must be at least $MIN_PHP_VERSION (current: $PHP_VERSION)"
        exit 1
    fi
    
    log_info "All requirements met"
}

create_backup() {
    log_info "Creating backup..."
    
    # Create backup directory if it doesn't exist
    mkdir -p "$BACKUP_PATH"
    
    # Backup database
    if [ -f "$PROJECT_PATH/.env.local" ]; then
        source "$PROJECT_PATH/.env.local"
        
        if [ ! -z "$DATABASE_URL" ]; then
            # Parse database URL
            DB_USER=$(echo $DATABASE_URL | sed -E 's/.*:\/\/([^:]+):.*/\1/')
            DB_PASS=$(echo $DATABASE_URL | sed -E 's/.*:\/\/[^:]+:([^@]+)@.*/\1/')
            DB_HOST=$(echo $DATABASE_URL | sed -E 's/.*@([^:\/]+).*/\1/')
            DB_NAME=$(echo $DATABASE_URL | sed -E 's/.*\///')
            
            mysqldump -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" > "$BACKUP_PATH/db_backup_$TIMESTAMP.sql"
            log_info "Database backup created: db_backup_$TIMESTAMP.sql"
        fi
    fi
    
    # Backup files
    tar -czf "$BACKUP_PATH/files_backup_$TIMESTAMP.tar.gz" \
        -C "$PROJECT_PATH" \
        --exclude=var/cache \
        --exclude=var/log \
        --exclude=vendor \
        --exclude=node_modules \
        .
    
    log_info "Files backup created: files_backup_$TIMESTAMP.tar.gz"
    
    # Keep only last 5 backups
    ls -1dt "$BACKUP_PATH"/* | tail -n +11 | xargs -r rm -f
}

pull_latest_code() {
    log_info "Pulling latest code from $BRANCH branch..."
    
    cd "$PROJECT_PATH"
    
    # Stash any local changes
    git stash
    
    # Fetch latest changes
    git fetch origin
    
    # Checkout and pull the specified branch
    git checkout "$BRANCH"
    git pull origin "$BRANCH"
    
    log_info "Code updated to latest version"
}

install_dependencies() {
    log_info "Installing dependencies..."
    
    cd "$PROJECT_PATH"
    
    # Install Composer dependencies
    if [ "$ENVIRONMENT" = "production" ]; then
        composer install --no-dev --optimize-autoloader --no-interaction
    else
        composer install --optimize-autoloader --no-interaction
    fi
    
    # Install NPM dependencies if package.json exists
    if [ -f "package.json" ]; then
        npm ci
        
        # Build assets
        if [ "$ENVIRONMENT" = "production" ]; then
            npm run build
        else
            npm run dev
        fi
    fi
    
    log_info "Dependencies installed"
}

run_migrations() {
    log_info "Running database migrations..."
    
    cd "$PROJECT_PATH"
    
    # Check if there are pending migrations
    PENDING=$(php bin/console doctrine:migrations:status --show-versions | grep "not migrated" | wc -l)
    
    if [ "$PENDING" -gt 0 ]; then
        log_info "Found $PENDING pending migration(s)"
        
        # Run migrations
        php bin/console doctrine:migrations:migrate --no-interaction --allow-no-migration
        
        log_info "Migrations completed"
    else
        log_info "No pending migrations"
    fi
}

clear_cache() {
    log_info "Clearing cache..."
    
    cd "$PROJECT_PATH"
    
    # Clear Symfony cache
    php bin/console cache:clear --env="$ENVIRONMENT" --no-warmup
    php bin/console cache:warmup --env="$ENVIRONMENT"
    
    # Clear OPcache if available
    if command -v cachetool &> /dev/null; then
        cachetool opcache:reset
        log_info "OPcache cleared"
    fi
    
    log_info "Cache cleared and warmed up"
}

update_permissions() {
    log_info "Updating file permissions..."
    
    cd "$PROJECT_PATH"
    
    # Set proper permissions for var directory
    chmod -R 775 var/
    
    # Set proper ownership (adjust user:group as needed)
    if [ ! -z "$WEB_USER" ]; then
        chown -R "$WEB_USER":"$WEB_USER" var/
    fi
    
    log_info "Permissions updated"
}

run_tests() {
    log_info "Running tests..."
    
    cd "$PROJECT_PATH"
    
    # Run PHPUnit tests if they exist
    if [ -f "bin/phpunit" ] || [ -f "vendor/bin/phpunit" ]; then
        if [ "$ENVIRONMENT" != "production" ]; then
            php bin/phpunit --testdox || {
                log_error "Tests failed! Deployment aborted."
                exit 1
            }
            log_info "All tests passed"
        else
            log_warning "Skipping tests in production environment"
        fi
    else
        log_warning "PHPUnit not found, skipping tests"
    fi
}

restart_services() {
    log_info "Restarting services..."
    
    # Restart PHP-FPM
    if systemctl is-active --quiet php8.1-fpm; then
        systemctl reload php8.1-fpm
        log_info "PHP-FPM reloaded"
    fi
    
    # Restart web server
    if systemctl is-active --quiet nginx; then
        systemctl reload nginx
        log_info "Nginx reloaded"
    elif systemctl is-active --quiet apache2; then
        systemctl reload apache2
        log_info "Apache reloaded"
    fi
    
    # Restart queue workers if Messenger is used
    if systemctl is-active --quiet symfony-messenger; then
        systemctl restart symfony-messenger
        log_info "Messenger workers restarted"
    fi
}

health_check() {
    log_info "Performing health check..."
    
    cd "$PROJECT_PATH"
    
    # Check if the application responds
    if [ ! -z "$APP_URL" ]; then
        HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$APP_URL/health-check")
        
        if [ "$HTTP_STATUS" -eq 200 ]; then
            log_info "Health check passed (HTTP $HTTP_STATUS)"
        else
            log_error "Health check failed (HTTP $HTTP_STATUS)"
            exit 1
        fi
    fi
    
    # Check database connection
    php bin/console doctrine:query:sql "SELECT 1" > /dev/null 2>&1 || {
        log_error "Database connection failed"
        exit 1
    }
    
    log_info "All health checks passed"
}

notify_deployment() {
    MESSAGE="$1"
    
    # Send notification (configure your notification method)
    # Example: Slack webhook
    if [ ! -z "$SLACK_WEBHOOK" ]; then
        curl -X POST -H 'Content-type: application/json' \
            --data "{\"text\":\"Deployment: $MESSAGE\"}" \
            "$SLACK_WEBHOOK"
    fi
    
    # Log to deployment log
    echo "[$(date)] $MESSAGE" >> "$PROJECT_PATH/var/log/deployments.log"
}

rollback() {
    log_error "Deployment failed! Rolling back..."
    
    # Restore database from backup
    if [ -f "$BACKUP_PATH/db_backup_$TIMESTAMP.sql" ]; then
        mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" < "$BACKUP_PATH/db_backup_$TIMESTAMP.sql"
        log_info "Database restored from backup"
    fi
    
    # Restore files from backup
    if [ -f "$BACKUP_PATH/files_backup_$TIMESTAMP.tar.gz" ]; then
        rm -rf "$PROJECT_PATH"/*
        tar -xzf "$BACKUP_PATH/files_backup_$TIMESTAMP.tar.gz" -C "$PROJECT_PATH"
        log_info "Files restored from backup"
    fi
    
    clear_cache
    restart_services
    
    notify_deployment "❌ Deployment failed and rolled back on $ENVIRONMENT"
    exit 1
}

# Main deployment process
main() {
    log_info "========================================="
    log_info "Starting Symfony deployment"
    log_info "Environment: $ENVIRONMENT"
    log_info "Branch: $BRANCH"
    log_info "Timestamp: $TIMESTAMP"
    log_info "========================================="
    
    # Set error trap
    trap rollback ERR
    
    # Execute deployment steps
    check_requirements
    create_backup
    pull_latest_code
    install_dependencies
    run_migrations
    clear_cache
    update_permissions
    run_tests
    restart_services
    health_check
    
    # Remove error trap after successful deployment
    trap - ERR
    
    log_info "========================================="
    log_info "Deployment completed successfully!"
    log_info "========================================="
    
    notify_deployment "✅ Successfully deployed to $ENVIRONMENT from $BRANCH"
}

# Run main function
main

# Exit successfully
exit 0
