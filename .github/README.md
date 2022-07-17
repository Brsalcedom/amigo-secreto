
Una aplicación de cli desarrollada en python3 para el sorteo de amigo secreto.

![](/images/main.png)

> Testeado en python 3.10 - Linux

# Instalación

```
git clone https://github.com/Brsalcedom/amigo-secreto --depth 1
cd amigo-secreto
pip3 install -r requirements.txt
python3 main.py
```
**Antes de utilizar llenar los campos del archivo [config.py](/config.py)**.

## Enviar correos utilizando GMAIL

Para utilizar el servidor stmp de google para el envío de correos, se debe contar con una cuenta de gmail protegida con segundo factor de autenticación (2FA).

1. Ir a Administrar tu cuenta de Google.

![](/images/gmail-1.png)

2. Ir a **Seguridad** y activar verificación en dos pasos.

![](/images/gmail-2.png)

3. Ir a **Contraseña de aplicaciones**.

![](/images/gmail-3.png)

4. Como aplicación seleccionar **correo**, en dispositivo **otra** y finalmente darle un nombre

![](/images/gmail-4.png)

5. Se generará una contraseña que puede ser utilizada para el envío de correos.

![](/images/gmail-5.png)


> Referencia: [support.google.com](https://support.google.com/accounts/answer/185833?hl=es)

# To-do

* Dockerizar
* Construir como aplicación web