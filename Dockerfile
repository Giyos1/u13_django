# FROM — asosiy image
FROM python:3.11-slim

# LABEL — metadata (ixtiyoriy)
LABEL maintainer="ism@email.com"
LABEL version="1.0"

# ENV — environment o'zgaruvchilari
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBUG=False

# WORKDIR — ishchi papka (bo'lmasa yaratadi)
WORKDIR /app

# COPY va ADD farqi:
# COPY — faqat local fayllar
# ADD  — URL va .tar.gz ham qo'llab-quvvatlaydi (kamroq ishlatiladi)
COPY requirements.txt .

# RUN — build paytida bajariladi (image ichiga yoziladi)
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# EXPOSE — hujjatlashtirish uchun (port ochilmaydi!)
EXPOSE 8000

# ARG — faqat build paytida ishlatiladigan o'zgaruvchi
ARG BUILD_VERSION=latest
RUN echo "Version: $BUILD_VERSION"

# USER — xavfsizlik uchun (root bo'lmaslik)
#RUN useradd -m appuser
#USER appuser

# ENTRYPOINT vs CMD
# CMD — override qilish mumkin
# ENTRYPOINT — asosiy buyruq, override qilib bo'lmaydi (odatda birga ishlatiladi)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]