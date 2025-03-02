## Descripción

Este es un proyecto hecho con [Python](https://www.python.org/). Es una que se conecta al servicio de **AWS DynamoDB** para insertar la información extraida de la API de SpaceX.

### Configuración previa de la ejecución

Se debe reemplazar el nombre del archivo `.env.example` por `.env`.

Luego se debe agregar los valores correspondientes a las variables dentro este archivo para su correcto funcionamiento.

Debemos tener instalado ```Python``` para ejecutar los comando en la terminal.

En una terminal que esté en la raíz del proyecto debemos instalar los paquetes con ```pip``` con el siguiente comando:

```bash
$ pip install -r requirements.txt
```

### Ejecución de los test

Una vez hecho todo lo anterior ejecutamos el siguiente comando en una terminal que esté ubicada en la raíz del proyecto para ejecutar los test y comprobar que todo marche bien:

```bash
$ py test.py
```

### Ejecución manual de la función lambda

Para traer el contador de los registros almacenados en **DynamoDB** debe ejecutar el siguiente comando:

```bash
$ py count.py
```
Para cargar la información de **SpaceX** en **DynamoDB** debe ejecutar el siguiente comando:

```bash
$ py load.py
```

La respuesta de estos comandos se mostrarán en consola.