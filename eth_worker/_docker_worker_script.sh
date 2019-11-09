#!/usr/bin/env bash
sleep 10

if [ "$CONTAINER_MODE" = 'TEST' ]; then
  echo pass
elif [ "$CONTAINER_TYPE" == 'BEAT' ]; then
  celery -A worker beat --loglevel=WARNING
elif [ "$CONTAINER_TYPE" == 'FILTER' ]; then
  python ethereum_filter_test.py
elif [ "$CONTAINER_TYPE" == 'PROCESSOR' ]; then
  celery -A eth_manager worker --loglevel=INFO --concurrency=1 --pool=eventlet -Q=processor
else
  alembic upgrade head
  celery -A eth_manager worker --loglevel=INFO --concurrency=10 --pool=eventlet
fi

#
#celery -A worker beat --loglevel=WARNING