# 🚀 Sistema de Inventario de Activos - Despliegue en Render

## 📋 Preparación del Proyecto

Tu proyecto Django ya está configurado y listo para desplegarse en **Render**. Aquí están todos los archivos que se han creado/modificado:

### ✅ Archivos Configurados:

- **`requirements.txt`** - Dependencias incluyendo PostgreSQL y Gunicorn
- **`settings.py`** - Configuración dual para desarrollo y producción
- **`render.yaml`** - Configuración de servicios de Render
- **`build.sh`** - Script de construcción automatizado
- **`.gitignore`** - Archivos a ignorar en Git

## 🌐 Pasos para Desplegar en Render

### 1. **Crear Repositorio en GitHub**

1. Inicializa Git en tu proyecto:
```bash
git init
git add .
git commit -m "Initial commit - Sistema de Inventario de Activos"
```

2. Crea un repositorio en GitHub y súbelo:
```bash
git remote add origin https://github.com/tuusuario/inventario-activos.git
git branch -M main
git push -u origin main
```

### 2. **Conectar con Render**

1. Ve a [render.com](https://render.com) y crea una cuenta
2. Haz clic en **"New +"** → **"Blueprint"**
3. Conecta tu repositorio de GitHub
4. Render detectará automáticamente el archivo `render.yaml`

### 3. **Configuración Automática**

Render creará automáticamente:
- ✅ **Web Service** (aplicación Django)
- ✅ **PostgreSQL Database** (base de datos)
- ✅ **Variables de entorno** (SECRET_KEY, DATABASE_URL)

### 4. **Proceso de Despliegue**

El script `build.sh` ejecutará automáticamente:
1. 📦 Instalación de dependencias
2. 🗃️ Recolección de archivos estáticos
3. 🔄 Migraciones de base de datos
4. 👤 Creación de superusuario (admin/admin123)
5. 📊 Datos iniciales (áreas y estados)

## 🔗 Acceso a tu Aplicación

Una vez desplegado, tendrás:

- **🌐 URL de la aplicación:** `https://inventario-activos.onrender.com`
- **👨‍💼 Panel de administración:** `https://inventario-activos.onrender.com/admin/`
- **🔑 Credenciales:** admin / admin123

## 🛠️ Funcionalidades Incluidas

### ✨ Sistema Completo:
- 📊 **Dashboard** con gráficos interactivos
- 📝 **CRUD** completo de equipos
- 🔢 **Numeración automática** de series
- 📄 **Exportación PDF** profesional
- 📊 **Importación Excel** masiva
- 🔍 **Filtros avanzados**
- 📱 **Diseño responsive**

### 🗂️ Gestión de Datos:
- **Áreas:** Administración, Contabilidad, Ventas, etc.
- **Estados:** Nuevo, Bueno, Regular, Malo, etc.
- **Tipos:** Computadora, Impresora, Monitor, etc.

## 🔧 Configuración Local

Para seguir desarrollando localmente:

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos (MySQL local)
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver
```

## 📈 Escalabilidad

### Plan Gratuito Render:
- ✅ **750 horas/mes** (suficiente para 1 app 24/7)
- ✅ **Base PostgreSQL** incluida
- ✅ **SSL automático**
- ✅ **Dominio personalizado**

### Upgrade ($7/mes):
- 🚀 **Sin límite de horas**
- 🚀 **No se duerme la app**
- 🚀 **Más recursos**

## 🆘 Resolución de Problemas

### Base de Datos:
Si tienes problemas con la BD, puedes ejecutar:
```bash
# En el dashboard de Render → Shell
python manage.py migrate
python manage.py createsuperuser
```

### Archivos Estáticos:
```bash
python manage.py collectstatic --no-input
```

### Variables de Entorno:
Render configurará automáticamente:
- `SECRET_KEY` (generada automáticamente)
- `DATABASE_URL` (conectada a PostgreSQL)
- `RENDER_EXTERNAL_HOSTNAME` (URL de tu app)

## 🎉 ¡Listo!

Tu **Sistema de Inventario de Activos** estará disponible en internet con:
- ⚡ **Alto rendimiento**
- 🔒 **Seguridad SSL**
- 🌍 **Acceso mundial**
- 📊 **Base de datos profesional**

¡Disfruta de tu aplicación en la nube! 🚀 