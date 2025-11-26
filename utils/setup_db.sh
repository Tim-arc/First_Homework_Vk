set -e 

DB_NAME="askpupkin_db"
DB_USER="askpupkin_user"
DB_PASSWORD="password" 

# Команда psql для создания БД и пользователя
sudo -u postgres psql -v ON_ERROR_STOP=1 <<-EOSQL
    CREATE DATABASE $DB_NAME;
    CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
    ALTER ROLE $DB_USER SET client_encoding TO 'utf8';
    ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';
    ALTER ROLE $DB_USER SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
    
EOSQL

echo "База данных '$DB_NAME' и пользователь '$DB_USER' успешно созданы."