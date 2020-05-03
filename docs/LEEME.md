# SocialPwned

<p align="right">
  <a href=https://github.com/MrTuxx/SocialPwned/blob/master/README.md>English🗨</a>
</p>

![SocialPwned](https://github.com/MrTuxx/SocialPwned/blob/master/docs/images/SocialPwned.PNG "SocialPwned Welcome")

[![Python 3.6|3.7|3.8](https://img.shields.io/badge/Python-3.6%2F3.7%2F3.8-blue.svg)](https://www.python.org/download/releases/3.0/) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/MrTuxx/SocialPwned/blob/master/LICENSE)

<p align="justify">
  SocialPwned es una herramienta OSINT que permite obtener los correos electrónicos, de un objetivo, publicados en redes sociales como Instagram, Linkedin y Twitter, para encontrar las posibles fugas de credenciales en PwnDB.
</p>
<p align="justify">
  La finalidad de esta herramienta es facilitar la búsqueda de objetivos vulnerables durante la fase de Footprinting en un Hacking Ético. Es habitual que los empleados de una compañía publiquen sus correos electrónicos en redes sociales, ya bien sean profesionales o personales, por tanto, si dichos correos poseen fugas de credenciales, es posible que las contraseñas encontradas hayan sido reutilizadas en el entorno que se pretende auditar. En caso de no ser así, al menos se tendría una idea de los patrones que sigue dicho objetivo para crear las contraseñas y poder realizar otros ataques con un mayor nivel de eficacia.
 </p>
 
 SocialPwned hace uso de diferentes módulos:
 
- **Instragram**: Haciendo uso de la [API no oficial de Instagram ](https://github.com/LevPasha/Instagram-API-python) de @LevPasha, se desarrollaron diferentes métodos que obtienen los correos electrónicos publicados por los usuarios. Es necesario una cuenta de Instagram.
- **Linkedin**: Haciendo uso de la [API no oficial de Linkedin](https://github.com/tomquirk/linkedin-api) de @tomquirk, se desarrollaron diferentes métodos que permiten obtener los empleados de una empresa y su información de contacto (email, twitter o teléfono). Además, es posible añadir a tus contactos los empleados encontrados, para así posteriormente tener acceso a su red de contactos y su información. Es necesario una cuenta de Linkedin.
- **Twint**: Haciendo uso de [Twint](https://github.com/twintproject/twint) de @twintproject se rastrean todos los Tweets publicados por un usuario en busca de algún correo electrónico. No es necesario una cuenta de Twitter.
- **PwnDB**: Inspirado por la herramienta [PwnDB](https://github.com/davidtavarez/pwndb) creada por @davidtavarez se ha desarrollado un modulo que busca todas las fugas de credenciales de los correos electrónicos encontrados. Además, por cada correo electrónico se realiza una petición POST a [HaveIBeenPwned](https://haveibeenpwned.com/) para conocer la fuente de la fuga de información.

## Instalación 🛠

La instalación de **Tor** depende del sistema operativo. En Debian:
```
$ sudo apt-get install tor
$ /etc/init.d/tor start
```
>NOTA: El servicio de tor debe estar arrancado para que se conecte al puerto 9050

Clona el repositorio usuando **Git**:
```
$ git clone https://github.com/MrTuxx/SocialPwned.git
$ cd SocialPwned
$ pip3 install -r requirements.txt
```
## Uso

Para hacer uso de las características de Instagram y Linkedin es necesario tener una cuenta creada en cada una de las redes sociales. Las credenciales deben ser indicadas en un archivo JSON:
```
{
    "instagram":{
        "username":"username",
        "password":"password"
    },
    "linkedin":{
        "email":"email",
        "password":"password"
    }
}

```
```
usage: socialpwned.py [-h] --credentials CREDENTIALS [--pwndb] [--output FILE] [--tor-proxy PROXY] [--instagram] [--info QUERY]
                      [--location LOCATION_ID] [--hashtag-ig QUERY] [--target-ig USER_ID] [--search-users-ig QUERY] [--my-followers]
                      [--my-followings] [--followers-ig] [--followings-ig] [--linkedin] [--company COMPANY_ID] [--search-companies QUERY]
                      [--employees] [--my-contacts] [--user-contacts USER_ID] [--search-users-in QUERY] [--target-in USERNAME] [--add-contacts]
                      [--add-a-contact USER_ID] [--twitter] [--limit LIMIT] [--year YEAR] [--since DATE] [--until DATE] [--profile-full]
                      [--all-tw] [--target-tw USERNAME] [--hashtag-tw USERNAME] [--followers-tw] [--followings-tw]
```

## Ejemplos Básicos y Combos 🚀

A continuación, se muestran algunos ejemplos:

### Instagram

![SocialPwned](https://github.com/MrTuxx/SocialPwned/blob/master/docs/images/1-3.png "Users with email in Instagram")
![SocialPwned](https://github.com/MrTuxx/SocialPwned/blob/master/docs/images/1-4.png "Leaks Found")
```
python3 socialpwned.py --credentials credentials.json --instagram --info España
```
```
python3 socialpwned.py --credentials credentials.json --instagram --location 832578276
```
```
python3 socialpwned.py --credentials credentials.json --instagram --hashtag-ig someHashtag --pwndb
```
```
python3 socialpwned.py --credentials credentials.json --instagram --target-ig username --pwndb
```
```
python3 socialpwned.py --credentials credentials.json --instagram --target-ig username --followers-ig --followings-ig --pwndb
```

### Linkedin

![SocialPwned](https://github.com/MrTuxx/SocialPwned/blob/master/docs/images/2-2.png "Searching employees of a company in Linkedin")
![SocialPwned](https://github.com/MrTuxx/SocialPwned/blob/master/docs/images/2-4.png "Leaks Found")
```
python3 socialpwned.py --credentials credentials.json --linkedin --search-companies "My Target"
```
```
python3 socialpwned.py --credentials credentials.json --linkedin --search-companies "My Target" --employees --pwndb
```
```
python3 socialpwned.py --credentials credentials.json --linkedin --company 123456789 --employees --pwndb
```
```
python3 socialpwned.py --credentials credentials.json --linkedin --company 123456789 --employees --add-contacts
```
```
python3 socialpwned.py --credentials credentials.json --linkedin --user-contacts user-id --pwndb
```
```
python3 socialpwned.py --credentials credentials.json --linkedin --user-contacts user-id --add-contacts
```
### Twitter
![SocialPwned](https://github.com/MrTuxx/SocialPwned/blob/master/docs/images/3-1.png "Searching in Twitter")

```
python3 socialpwned.py --credentials credentials.json --twitter --hashtag-tw someHashtag --pwndb --limit 200
```
```
python3 socialpwned.py --credentials credentials.json --twitter --target-tw username --all-tw --pwndb
```
```
python3 socialpwned.py --credentials credentials.json --twitter --target-tw username --all-tw --followers-tw --followings-tw --pwndb
```

### Combos

```
python3 socialpwned.py --credentials credentials.json --instagram --target-ig username --followers-ig --followings-ig --linkedin --company 123456789 --employees --twitter --target-tw username --all-tw --pwndb --output results.txt
```
```
python3 socialpwned.py --credentials credentials.json --instagram --target-ig username --linkedin --target-in username --twitter --target-tw username --all-tw --pwndb
```

## Limitaciones

## Referencias

## Disclaimer
