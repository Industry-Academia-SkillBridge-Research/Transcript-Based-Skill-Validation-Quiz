# 🔧 Production MySQL Setup Guide

Complete guide for setting up SkillBridge with MySQL in production.

## 📋 Prerequisites

- MySQL 8.0+ installed and running
- Python 3.8+ with virtual environment
- Git (for cloning the repository)

---

## 🚀 Fresh Installation Steps

### 1. Clone and Setup Project

```powershell
# Clone repository
git clone <your-repo-url>
cd Transcript-Based-Skill-Validation-Quiz

# Create Python virtual environment
cd backend
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1  # Windows
# source .venv/bin/activate    # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 2. Create MySQL Database

```sql
-- Connect to MySQL as root
mysql -u root -p

-- Create database
CREATE DATABASE IF NOT EXISTS skillbridge_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Verify
SHOW DATABASES;
```

### 3. Create Dedicated MySQL User

**Option A: Using SQL Script (Recommended)**

```powershell
# Edit the SQL script with your chosen password
# File: backend/scripts/setup_mysql_user.sql

# Run the script
mysql -u root -p < scripts/setup_mysql_user.sql
```

**Option B: Using Interactive Helper**

```powershell
cd backend
python scripts/setup_user_interactive.py
```

**Option C: Manual SQL Commands**

```sql
CREATE USER 'skillbridge_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON skillbridge_db.* TO 'skillbridge_user'@'localhost';
FLUSH PRIVILEGES;

-- Verify
SELECT User, Host FROM mysql.user WHERE User = 'skillbridge_user';
SHOW GRANTS FOR 'skillbridge_user'@'localhost';
```

### 4. Configure Environment Variables

```powershell
cd backend/src

# Copy example file
cp .env.example .env

# Edit .env with your actual credentials
# DATABASE_URL=mysql+pymysql://skillbridge_user:your_password@localhost:3306/skillbridge_db?charset=utf8mb4
```

**Important:** Never commit the `.env` file to version control!

### 5. Run Database Migrations

```powershell
cd backend/src

# Run Alembic migrations to create tables
alembic upgrade head

# Verify tables were created
python -c "from app.db import engine; from sqlalchemy import inspect; print(inspect(engine).get_table_names())"
```

### 6. Verify Database Setup

```powershell
cd backend
python scripts/verify_mysql_setup.py
```

This will check:
- ✅ Database connection
- ✅ Table engines (InnoDB)
- ✅ Foreign keys
- ✅ Character sets
- ✅ Indexes

### 7. Start the Application

```powershell
cd backend/src
python -m uvicorn app.main:app --reload

# Access:
# - API: http://localhost:8000
# - Docs: http://localhost:8000/docs
# - Health: http://localhost:8000/health
```

---

## 🔄 Alembic Migration Commands

### Creating New Migrations

```powershell
cd backend/src

# Auto-generate migration from model changes
alembic revision --autogenerate -m "Description of changes"

# Review the generated migration file
# Edit if needed: alembic/versions/<revision>_description.py

# Apply migration
alembic upgrade head
```

### Common Migration Operations

```powershell
# Show current revision
alembic current

# Show migration history
alembic history

# Upgrade to specific revision
alembic upgrade <revision>

# Downgrade one revision
alembic downgrade -1

# Downgrade to base (empty database)
alembic downgrade base

# Show SQL without executing
alembic upgrade head --sql
```

---

## 🔍 Database Verification

### Check Table Engines

```sql
SELECT table_name, engine 
FROM information_schema.tables 
WHERE table_schema = 'skillbridge_db';

-- All tables should be InnoDB
```

### Check Foreign Keys

```sql
SELECT 
    constraint_name,
    table_name,
    column_name,
    referenced_table_name,
    referenced_column_name
FROM information_schema.key_column_usage
WHERE table_schema = 'skillbridge_db'
AND referenced_table_name IS NOT NULL;
```

### Convert Table Engine (if needed)

```sql
-- If any table is not InnoDB:
ALTER TABLE <table_name> ENGINE=InnoDB;
```

---

## 🛡️ Security Best Practices

### 1. Strong Password Policy

```sql
-- Set password validation policy
SET GLOBAL validate_password.policy = STRONG;
SET GLOBAL validate_password.length = 12;
```

### 2. Limit User Permissions

```sql
-- Only grant necessary privileges
GRANT SELECT, INSERT, UPDATE, DELETE ON skillbridge_db.* TO 'skillbridge_user'@'localhost';

-- For production, consider read-only user for reporting
CREATE USER 'skillbridge_readonly'@'localhost' IDENTIFIED BY 'password';
GRANT SELECT ON skillbridge_db.* TO 'skillbridge_readonly'@'localhost';
```

### 3. Enable SSL/TLS (Production)

```sql
-- Require SSL for connections
ALTER USER 'skillbridge_user'@'localhost' REQUIRE SSL;
```

### 4. Regular Backups

```powershell
# Backup database
mysqldump -u skillbridge_user -p skillbridge_db > backup_$(date +%Y%m%d).sql

# Restore database
mysql -u skillbridge_user -p skillbridge_db < backup_20260302.sql
```

---

## 🔧 Troubleshooting

### Connection Refused

```
Problem: Can't connect to MySQL server on 'localhost'
Solution:
1. Check MySQL is running: services.msc → MySQL
2. Verify port 3306 is open
3. Check firewall settings
```

### Authentication Failed

```
Problem: Access denied for user 'skillbridge_user'@'localhost'
Solution:
1. Verify user exists: SELECT User, Host FROM mysql.user;
2. Reset password: ALTER USER 'skillbridge_user'@'localhost' IDENTIFIED BY 'new_password';
3. Update .env file with new password
```

### Table Creation Errors

```
Problem: Alembic migration fails
Solution:
1. Check DATABASE_URL in .env
2. Verify user has CREATE privileges
3. Check alembic/env.py imports all models
4. Run: alembic upgrade head --sql (review SQL)
```

### Foreign Key Errors

```
Problem: Cannot add foreign key constraint
Solution:
1. Ensure both tables use InnoDB engine
2. Ensure referenced column exists and is indexed
3. Check data types match exactly
```

---

## 📊 Performance Tuning

### Connection Pooling

Already configured in `app/db.py`:
```python
engine = create_engine(
    DATABASE_URL,
    pool_size=10,        # Number of persistent connections
    max_overflow=20,     # Additional connections if needed
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=3600    # Recycle connections after 1 hour
)
```

### MySQL Configuration

Add to `/etc/mysql/my.cnf` (Linux) or `my.ini` (Windows):

```ini
[mysqld]
# Connection settings
max_connections = 200
max_allowed_packet = 64M

# InnoDB settings
innodb_buffer_pool_size = 1G
innodb_log_file_size = 256M
innodb_flush_log_at_trx_commit = 2

# Character set
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci
```

---

## 📝 Environment Variables Reference

```env
# Required
DATABASE_URL=mysql+pymysql://skillbridge_user:password@localhost:3306/skillbridge_db?charset=utf8mb4

# Optional (for multiple environments)
# DATABASE_URL_DEV=mysql+pymysql://user:pass@localhost:3306/skillbridge_dev
# DATABASE_URL_TEST=mysql+pymysql://user:pass@localhost:3306/skillbridge_test
# DATABASE_URL_PROD=mysql+pymysql://user:pass@prod-server:3306/skillbridge_prod
```

---

## ✅ Verification Checklist

Before deploying to production:

- [ ] MySQL user created with strong password
- [ ] Database created with utf8mb4 charset
- [ ] All tables using InnoDB engine
- [ ] Foreign keys properly configured
- [ ] Alembic migrations applied successfully
- [ ] Database verification script passes
- [ ] Application starts without errors
- [ ] API endpoints respond correctly
- [ ] Backup strategy implemented
- [ ] Monitoring and logging configured

---

## 🔗 Related Files

- [`backend/scripts/setup_mysql_user.sql`](scripts/setup_mysql_user.sql) - SQL user creation
- [`backend/scripts/setup_user_interactive.py`](scripts/setup_user_interactive.py) - Interactive setup
- [`backend/scripts/verify_mysql_setup.py`](scripts/verify_mysql_setup.py) - Database verification
- [`backend/scripts/init_mysql_db.py`](scripts/init_mysql_db.py) - Direct table creation (legacy)
- [`backend/src/.env.example`](src/.env.example) - Environment template
- [`backend/src/alembic/`](src/alembic/) - Migration files

---

## 📞 Support

For issues or questions:
1. Check this guide first
2. Run verification script: `python scripts/verify_mysql_setup.py`
3. Check application logs
4. Review Alembic migration history: `alembic history`

---

**Last Updated:** March 2, 2026  
**MySQL Version:** 8.0+  
**Python Version:** 3.8+
