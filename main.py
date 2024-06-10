import subprocess
import time

# Iniciar servicio de usuarios
service_sqlite = subprocess.Popen(['python', 'micro_service_sqlite/app.py'])

# Esperar un momento para asegurarse de que el servicio de usuarios esté en funcionamiento
time.sleep(1)

# Iniciar servicio de tareas
service_mongodb = subprocess.Popen(['python', 'micro_service_mongo/app.py'])

# Esperar un momento para asegurarse de que el servicio de tareas esté en funcionamiento
time.sleep(1)

# Iniciar el API Gateway
gateway = subprocess.Popen(['python', 'gateway/app.py'])

# Mantener el script en ejecución para que los servicios se mantengan activos
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping services...")
    service_sqlite.terminate()
    service_mongodb.terminate()
    gateway.terminate()
