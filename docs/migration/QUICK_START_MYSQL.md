# 🚀 Quick Start - MySQL Production Setup

## For New Team Members (Fresh Install)

### 1. Prerequisites
```bash
✓ MySQL 8.0+ running
✓ Python 3.8+
✓ Git
```

### 2. Setup (5 minutes)

```powershell
# Clone and install
git clone <repo-url>
cd Transcript-Based-Skill-Validation-Quiz/backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Create database and user (MySQL root)
mysql -u root -p
```

```sql
CREATE DATABASE skillbridge_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'skillbridge_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON skillbridge_db.* TO 'skillbridge_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

```powershell
# Configure environment
cd src
cp .env.example .env
# Edit .env with your password

# Run migrations
python -m alembic upgrade head

# Verify setup
cd ..
python scripts/verify_mysql_setup.py

# Start application
cd src
python -m uvicorn app.main:app --reload
```

✅ Done! Visit http://localhost:8000/docs

---

## Essential Commands

### Application
```powershell
cd backend/src
python -m uvicorn app.main:app --reload    # Development
```

### Migrations
```powershell
cd backend/src
python -m alembic upgrade head              # Apply migrations
python -m alembic current                   # Check version
python -m alembic history                   # View history
```

### Verification
```powershell
cd backend
python scripts/verify_mysql_setup.py       # Full check
```

### Database
```powershell
mysql -u skillbridge_user -p skillbridge_db
```

---

## Making Schema Changes

```powershell
cd backend/src

# 1. Edit model (e.g., app/models/student.py)
# Add new column, change type, etc.

# 2. Generate migration
python -m alembic revision --autogenerate -m "Add phone number"

# 3. Review migration file
# Check alembic/versions/<revision>_add_phone_number.py

# 4. Apply migration
python -m alembic upgrade head

# 5. Commit both files
git add app/models/student.py alembic/versions/<revision>_*.py
git commit -m "feat: add phone number to student"
```

---

## Troubleshooting

### Can't connect to MySQL
```powershell
# Check MySQL is running
services.msc → MySQL

# Test connection
mysql -u skillbridge_user -p -e "SELECT 1"
```

### Migration errors
```powershell
# Check current state
cd backend/src
python -m alembic current

# View SQL without executing
python -m alembic upgrade head --sql
```

### Import errors
```powershell
# Ensure in correct directory
cd backend/src
python -c "from app.db import engine; print('OK')"
```

---

## File Locations

```
backend/
├── requirements.txt         # Dependencies (includes alembic)
├── scripts/
│   ├── setup_mysql_user.sql           # User creation
│   ├── verify_mysql_setup.py          # Verification
│   └── setup_user_interactive.py      # Interactive setup
└── src/
    ├── .env                 # Your credentials (not in git)
    ├── .env.example         # Template
    ├── alembic.ini          # Alembic config
    ├── alembic/versions/    # Migration files
    └── app/
        ├── db.py            # Database config
        └── models/          # SQLAlchemy models
```

---

## Documentation

- 📚 [MYSQL_PRODUCTION_SETUP.md](../MYSQL_PRODUCTION_SETUP.md) - Complete guide
- 📋 [MYSQL_PRODUCTION_SUMMARY.md](../MYSQL_PRODUCTION_SUMMARY.md) - Full changes
- 📖 [MYSQL_MIGRATION_COMPLETE.md](../MYSQL_MIGRATION_COMPLETE.md) - Initial migration

---

## Quick Checks

### Is everything working?
```powershell
cd backend
python scripts/verify_mysql_setup.py
# Should show: ✅ ALL VERIFICATIONS PASSED
```

### What version am I on?
```powershell
cd backend/src
python -m alembic current
# Shows: 62e2378f40de (head)
```

### Can I connect?
```powershell
cd backend/src
python -c "from app.db import engine; engine.connect(); print('✅ Connected')"
```

---

**Need help?** See full documentation or run verification script.
