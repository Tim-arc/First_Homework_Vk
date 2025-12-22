set -e 

DB_NAME="askpupkin_db"
DB_USER="askpupkin_user"
DB_PASSWORD="password" 

# Добавили команды DROP ... IF EXISTS
sudo -u postgres psql -v ON_ERROR_STOP=1 <<-EOSQL
    -- 1. Сначала отключаем всех, кто может быть подключен к базе (опционально, но полезно)
    SELECT pg_terminate_backend(pg_stat_activity.pid)
    FROM pg_stat_activity
    WHERE pg_stat_activity.datname = '$DB_NAME'
      AND pid <> pg_backend_pid();

    -- 2. Удаляем базу, если она есть
    DROP DATABASE IF EXISTS $DB_NAME;

    -- 3. Удаляем пользователя, если он есть (чтобы пересоздать с гарантированно правильным паролем)
    DROP USER IF EXISTS $DB_USER;

    -- 4. Создаем пользователя
    CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
    
    -- 5. Настраиваем пользователя
    ALTER ROLE $DB_USER SET client_encoding TO 'utf8';
    ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';
    ALTER ROLE $DB_USER SET timezone TO 'UTC';

    -- 6. Создаем базу данных и сразу назначаем владельца (это заменяет GRANT)
    CREATE DATABASE $DB_NAME OWNER $DB_USER;
    
    -- 7. На всякий случай выдаем права (хотя OWNER уже дает полные права)
    GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
EOSQL

echo "База данных '$DB_NAME' и пользователь '$DB_USER' успешно пересозданы."