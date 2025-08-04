# MySQL Database Migration Guide

## Overview

The Bangladeshi Fitness App has been successfully migrated from SQLite to MySQL database. This provides better scalability, performance, and multi-user support.

## Changes Made

### 1. **New Database Architecture**
- **Primary**: MySQL database
- **Fallback**: SQLite (for development/testing)
- **Connection Management**: Automatic fallback if MySQL is unavailable

### 2. **New Files Created**
- `database.py` - MySQL database manager and connection handling
- `setup_mysql.py` - MySQL setup and configuration script
- Updated `config.py` - MySQL configuration settings

### 3. **Updated Files**
- `main.py` - Now uses the new Database class
- `utils.py` - Updated to use MySQL queries with parameterized statements
- `test_app.py` - Updated to test MySQL connection
- `install.py` - Added MySQL setup step
- `requirements.txt` - Added MySQL dependencies

## Key Features

### **Automatic Fallback System**
```python
# If MySQL is not available, automatically falls back to SQLite
try:
    connection = mysql.connector.connect(...)
except mysql.connector.Error:
    # Fallback to SQLite
    connection = sqlite3.connect(...)
```

### **Enhanced Database Schema**
- **Auto-increment IDs**: Better for multi-user environments
- **Foreign Key Constraints**: Data integrity
- **Timestamps**: Created/updated tracking
- **UTF-8 Support**: Full Bangla character support
- **Water Logs**: New table for water intake tracking

### **Improved Data Management**
- **Parameterized Queries**: SQL injection protection
- **Transaction Support**: Data consistency
- **Connection Pooling**: Better performance
- **Error Handling**: Graceful failure handling

## Installation Steps

### **1. Install Dependencies**
```bash
pip install mysql-connector-python pymysql
```

### **2. Setup MySQL Database**
```bash
python3 setup_mysql.py
```

### **3. Test Connection**
```bash
python3 test_app.py
```

### **4. Run Application**
```bash
python3 main.py
```

## Configuration Options

### **Environment Variables**
```bash
DB_HOST=localhost
DB_PORT=3306
DB_NAME=bangladeshi_fitness
DB_USER=root
DB_PASSWORD=your_password
```

### **Config File Settings**
```python
# In config.py
DATABASE_TYPE = "mysql"  # or "sqlite"
DATABASE_HOST = "localhost"
DATABASE_PORT = 3306
DATABASE_NAME = "bangladeshi_fitness"
DATABASE_USER = "root"
DATABASE_PASSWORD = ""
```

## Database Schema

### **Users Table**
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    age INT,
    weight DECIMAL(5,2),
    height DECIMAL(5,2),
    goal VARCHAR(50),
    target_calories INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### **Foods Table**
```sql
CREATE TABLE foods (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name_bangla VARCHAR(255) NOT NULL,
    name_english VARCHAR(255) NOT NULL,
    calories_per_100g INT NOT NULL,
    protein DECIMAL(5,2),
    carbs DECIMAL(5,2),
    fat DECIMAL(5,2),
    category VARCHAR(50),
    serving_size VARCHAR(100),
    serving_weight DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **Food Logs Table**
```sql
CREATE TABLE food_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    food_id INT,
    amount DECIMAL(8,2),
    date DATE,
    meal_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (food_id) REFERENCES foods(id) ON DELETE CASCADE
);
```

## Benefits of MySQL Migration

### **1. Performance**
- **Faster Queries**: Optimized for complex joins
- **Indexing**: Better search performance
- **Connection Pooling**: Reduced connection overhead

### **2. Scalability**
- **Multi-User Support**: Concurrent user access
- **Data Volume**: Handles large datasets efficiently
- **Backup/Restore**: Professional database management

### **3. Features**
- **Foreign Keys**: Data integrity
- **Transactions**: ACID compliance
- **Stored Procedures**: Complex operations
- **Triggers**: Automated data updates

### **4. Development**
- **Better Error Messages**: Detailed MySQL errors
- **Query Optimization**: MySQL query analyzer
- **Monitoring**: Performance monitoring tools

## Troubleshooting

### **Common Issues**

#### **1. MySQL Connection Failed**
```bash
# Check MySQL service
sudo systemctl status mysql

# Start MySQL service
sudo systemctl start mysql
```

#### **2. Permission Denied**
```bash
# Create MySQL user
mysql -u root -p
CREATE USER 'fitness_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON bangladeshi_fitness.* TO 'fitness_user'@'localhost';
FLUSH PRIVILEGES;
```

#### **3. Character Encoding Issues**
```sql
-- Set proper character encoding
ALTER DATABASE bangladeshi_fitness CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### **Fallback to SQLite**
If MySQL setup fails, the app automatically falls back to SQLite:
```python
# The app will work with SQLite if MySQL is unavailable
python3 main.py
```

## Testing

### **Run All Tests**
```bash
python3 test_app.py
```

### **Test MySQL Connection**
```bash
python3 setup_mysql.py
```

### **Test App Functionality**
```bash
python3 main.py
```

## Migration Checklist

- [ ] Install MySQL Server
- [ ] Install MySQL Connector/Python
- [ ] Run setup_mysql.py
- [ ] Test database connection
- [ ] Run application tests
- [ ] Verify all features work
- [ ] Test fallback to SQLite

## Support

For MySQL-related issues:
1. Check MySQL service status
2. Verify database credentials
3. Test connection manually
4. Check error logs
5. Use SQLite fallback if needed

---

**The migration to MySQL provides better performance, scalability, and features while maintaining backward compatibility with SQLite for development and testing.** 