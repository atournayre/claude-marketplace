# Symfony Framework Development Skill

## Overview

This skill provides comprehensive guidance and tools for developing applications with Symfony 6.4, the leading PHP framework for web applications, APIs, and microservices.

## Features

- **Complete Symfony 6.4 Documentation**: Core concepts, best practices, and advanced patterns
- **Code Generation Scripts**: Automated tools for entity and CRUD generation
- **Deployment Automation**: Production-ready deployment scripts
- **Security Configurations**: Advanced authentication and authorization patterns
- **Performance Optimization**: Caching strategies and query optimization techniques
- **Testing Strategies**: Unit, functional, and integration testing patterns

## Structure

```
symfony-skill/
├── SKILL.md                # Main skill file with core instructions
├── README.md               # This file
├── LICENSE                 # MIT License
├── scripts/                # Automation scripts
│   ├── generate-entity.php    # Entity generator
│   ├── generate-crud.php      # CRUD generator
│   └── deploy.sh              # Deployment automation
└── references/             # Detailed documentation
    ├── doctrine-advanced.md   # Advanced ORM patterns
    ├── security-detailed.md   # Security configurations
    └── testing-complete.md    # Testing strategies
```

## Quick Start

### Using the Skill

1. **Load the skill** in your Claude conversation
2. **Reference specific topics** when needed
3. **Use scripts** for code generation tasks
4. **Check references** for detailed documentation

### Common Commands

```bash
# Create new Symfony project
symfony new my_project --version="6.4.*" --webapp

# Generate entity
php scripts/generate-entity.php Product name:string price:decimal

# Generate CRUD
php scripts/generate-crud.php Product

# Deploy application
./scripts/deploy.sh production main
```

## Key Capabilities

### 1. Project Setup & Configuration
- Environment configuration
- Service container setup
- Bundle management
- Package installation

### 2. Development Patterns
- MVC architecture
- Dependency injection
- Event-driven programming
- Repository pattern
- Service layer pattern

### 3. Database & ORM
- Entity management
- Relationships mapping
- Query optimization
- Migration strategies
- Performance tuning

### 4. Security
- Authentication methods
- Authorization with voters
- JWT tokens
- OAuth integration
- Two-factor authentication

### 5. API Development
- RESTful APIs
- GraphQL integration
- API versioning
- Rate limiting
- CORS configuration

### 6. Testing
- Unit testing
- Functional testing
- Integration testing
- Test fixtures
- Mocking strategies

### 7. Performance
- Caching strategies
- Query optimization
- Asset optimization
- Profiling tools
- Production optimization

### 8. Deployment
- Environment preparation
- Automated deployment
- Zero-downtime deployment
- Rollback procedures
- Health checks

## Usage Examples

### Creating a New Feature

1. **Generate the entity**:
```bash
php scripts/generate-entity.php Article title:string content:text author:relation:ManyToOne:User
```

2. **Create the CRUD**:
```bash
php scripts/generate-crud.php Article
```

3. **Add business logic** in services
4. **Write tests** for the feature
5. **Deploy** using the deployment script

### API Development

1. **Create API controller** using the --api flag:
```bash
php scripts/generate-crud.php Product --api
```

2. **Configure serialization groups** in your entity
3. **Add validation rules**
4. **Implement authentication**
5. **Document with OpenAPI/Swagger**

## Best Practices

1. **Always use dependency injection** - Never instantiate services manually
2. **Keep controllers thin** - Move business logic to services
3. **Write tests first** - Follow TDD approach for critical features
4. **Cache expensive operations** - Use Symfony's cache component
5. **Optimize database queries** - Use eager loading and query optimization
6. **Follow Symfony conventions** - Use recommended directory structure and naming
7. **Use environment variables** - For configuration that changes between environments
8. **Implement proper error handling** - Use exceptions and proper HTTP status codes
9. **Document your code** - Use PHPDoc and keep documentation updated
10. **Regular security updates** - Keep dependencies updated and check for vulnerabilities

## Common Issues & Solutions

### Issue: Services not autowiring
**Solution**: Check service configuration and ensure autowiring is enabled

### Issue: Database connection errors
**Solution**: Verify DATABASE_URL in .env file and database credentials

### Issue: Cache permissions
**Solution**: Set proper permissions on var/cache directory

### Issue: Route not found
**Solution**: Clear cache and check route configuration with debug:router

### Issue: Migration failures
**Solution**: Check migration status and resolve conflicts manually if needed

## Requirements

- PHP 8.1 or higher
- Composer
- Symfony CLI (recommended)
- Database (MySQL/PostgreSQL/SQLite)
- Web server (Apache/Nginx)
- Node.js & NPM (for assets)

## Compatibility

- Symfony 6.4 LTS
- PHP 8.1, 8.2, 8.3
- MySQL 5.7+, PostgreSQL 10+, SQLite 3+
- Compatible with Docker environments

## Contributing

This skill is designed to be extended. To add new capabilities:

1. Update SKILL.md with new patterns
2. Add scripts to scripts/ directory
3. Create reference documentation in references/
4. Test thoroughly before deployment

## Support

For Symfony-specific questions:
- Official Documentation: https://symfony.com/doc/6.4/
- Symfony Slack: https://symfony.com/slack
- Stack Overflow: Tag with `symfony`

## Version History

- **1.0.0** - Initial release with Symfony 6.4 support
  - Complete documentation coverage
  - Entity and CRUD generators
  - Deployment automation
  - Advanced patterns documentation

## License

MIT License - See LICENSE file for details

## Credits

Created for Claude AI to enhance Symfony development capabilities.
Based on official Symfony 6.4 documentation and community best practices.