**EXPLICACION DEL USO DE del Bot "Pericote Raws"**
> El Bot de Discord "Pericote Raws" es una monda diseñada para asistir en la administración y gestión de las raws de naver,

# **1. /crearserie**
```Descripción:
Registra una serie en Firestore con datos esenciales: canal, nombre, link, día y precio.

Roles Permitidos:
- Pericote
- Moderacion
- Above

Parámetros:
1. serie: Canal de Discord asociado a la serie.
2. nombre: Nombre de la serie.
3. link: Enlace directo a la serie.
4. dia: Día de estreno (Lunes/Monday, Martes/Tuesday, etc.).
5. precio: Precio (1.5 usd o 0 usd).```
**Flujo del Comando:**
> *Se selecciona un canal para la serie desde las opciones autocompletadas (máximo 25).
> El usuario completa los otros parámetros obligatorios: nombre, link, día y precio.
> El bot registra la información en la base de datos Firestore en la colección nuevasseries.
Embed de Respuesta:
**Éxito:**
```Título: Serie Registrada
Descripción: Serie registrada para las raws correctamente.
Color: Dorado (#FFD700)```
**Error:**
```Título: Error
Descripción: No se pudo registrar la serie, lo siento perrillo.
Color: Rojo (#FF0000)```

# **2. /getlink**
```Descripción:
Obtiene los links de todas las series registradas para un día específico.

Roles Permitidos:
- Pericote
- Moderacion
- Above

Parámetros:
1. dia: Día de estreno (Lunes/Monday, Martes/Tuesday, etc.).```
**Flujo del Comando:**
> El usuario selecciona un día de estreno.
> El bot consulta en la base de datos Firestore las series asociadas a ese día.
> Responde con un embed que lista:
> -Nombre de la serie.
> -Canal asociado.
> -Link.
Embed de Respuesta:
```Título: Raws de {dia}
Descripción:
Estas son las raws del día:
1. Nombre: La doncella secreta del conde
   Serie: #la-doncella-secreta-del-conde
   Link: [Haz clic aquí](https://comic.naver.com/webtoon/list?titleId=830106)```
# **3. /addregister**
```Descripción:
Registra capítulos mensuales para una serie en Firestore.
Roles Permitidos:
- Pericote
- Moderacion
- Above
Parámetros:
1. nombre: Selecciona una serie registrada.
2. chapter: Número del capítulo.
3. mes: Mes del registro (octubre2024, noviembre2024, etc.).```
**Flujo del Comando:**
> El usuario selecciona una serie y completa los campos chapter y mes.
> El bot registra la información en la base de datos Firestore en la colección registroderaws.
Embed de Respuesta:
```Título: Registro Agregado
Descripción:
Registro agregado correctamente:
- Nombre: La doncella secreta del conde
- Chapter: 1
- Mes: octubre2024```
# **4. /verregistro**
```Descripción:
Muestra un resumen de los capítulos registrados en un mes.
Roles Permitidos:
- Moderacion
- Above
Parámetros:
1. mes: Selecciona un mes para ver el registro.```
**Flujo del Comando:**
> El usuario selecciona un mes.
> El bot consulta en Firestore la colección registroderaws para el mes seleccionado.
> Devuelve un resumen con el total de capítulos registrados y sus precios.
Embed de Respuesta:
```Título: Registro de las raws del {mes}
Descripción:
Hay un total de raws registradas en {mes}: {total}
1. Nombre: La doncella secreta del conde
   Chapter: 1
   Precio: 1.5 usd```
# **5. /pagoraws**
```Descripción:
Calcula el monto total de raws registradas en un mes.
Roles Permitidos:
- Moderacion
- Above
Parámetros:
1. mes: Selecciona un mes para calcular el total.```
**Flujo del Comando:**
> El usuario selecciona un mes.
> El bot consulta los precios de la colección registroderaws y los suma.
Embed de Respuesta:
```Título: Pago Total de Raws del {mes}
Descripción:
Total a pagar por las raws registradas:
- Monto: {total_usd} usd```
# **Comandos con Prefijo ($)**
> Los comandos con prefijo ofrecen flexibilidad para interacciones rápidas.
# **1. $pericote saluda**
```Descripción:
Saluda al usuario confirmando el funcionamiento del prefijo.```
# **2. $pericote rm <tiempo>**
```Descripción:
Crea un recordatorio en un tiempo específico.

Formato del Tiempo:
- s: segundos
- m: minutos
- h: horas```
**Flujo del Comando:**
```Envía un mensaje al canal de origen: "Pregunta hecha perrillo".
Envía el recordatorio al canal #Pericote etiquetando el rol Pericote.```
# **3. $pericote cambiar prefijo**
```Descripción:
Cambia el prefijo del bot a uno personalizado.```
# **4. $pericote borrar <cantidad>**
```Descripción:
Borra una cantidad específica de mensajes en el canal donde se ejecuta.```
# **5. $pericote borratodo**
```Descripción:
Borra todos los mensajes del canal donde se ejecuta.```