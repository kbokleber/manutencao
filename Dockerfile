FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Instala as dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala as dependências Python uma por uma para evitar conflitos
RUN pip install --no-cache-dir \
    Django==5.0.1 \
    django-crispy-forms==2.1 \
    crispy-bootstrap5==2023.10 \
    Pillow==10.2.0 \
    django-widget-tweaks==1.5.0 \
    django-filter==23.5 \
    django-notifications-hq==1.8.2 \
    plotly==5.18.0 \
    django-plotly-dash==2.2.2 \
    channels==4.0.0 \
    whitenoise==6.6.0 \
    gunicorn==21.2.0 \
    psycopg2-binary==2.9.9

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "maintenance_project.wsgi:application"] 