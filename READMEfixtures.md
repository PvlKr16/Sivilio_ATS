change users' passwords:
docker compose exec web python manage.py changepassword bob.supervisor
docker compose exec web python manage.py changepassword carol.recruiter
docker compose exec web python manage.py changepassword dan.intern

# Add fixtures
docker compose exec web python manage.py loaddata <fixture1> <fixture2> <fixture3> etc.

# Clear everything except structure
docker compose exec web python manage.py flush --no-input

# Add fixtures after flush
docker compose exec web python manage.py create_initial_data && \
docker compose exec web python manage.py loaddata <fixture1> <fixture2> <fixture3> etc.