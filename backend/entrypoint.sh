#!/bin/sh
set -e

echo "در انتظار آمادگی PostgreSQL..."
RETRIES=30
until python manage.py check --database default 2>/tmp/db_check_error.log || [ $RETRIES -eq 0 ]; do
  echo "هنوز آماده نیست، تلاش دوباره... ($RETRIES باقی‌مانده)"
  cat /tmp/db_check_error.log
  RETRIES=$((RETRIES-1))
  sleep 2
done

if [ $RETRIES -eq 0 ]; then
  echo "❌ اتصال به دیتابیس بعد از چند تلاش شکست خورد. خطای آخر:"
  cat /tmp/db_check_error.log
  exit 1
fi

echo "اجرای migrate..."
python manage.py migrate --noinput

echo "اجرای سرور..."
exec "$@"
