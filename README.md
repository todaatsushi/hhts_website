# Higashi Hiroshima Volunteer Guide Group Website
The prototype website for the Higashi Hiroshima Volunteer Guide group.

## Project links
* [Website](https://saijosakaguradouri.pythonanywhere.com) - link to the site
* [Project page](https://www.atsushi.dev/work/higashi-hiroshima-volunteer-guide/) on atsushi.dev - link to more information on the project page on my site

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Installing

Using a virtual env (recommended), install dependencies from requirements.txt.

```
pip install -r requirements.txt
```

### .env variables
This project expects:
* SECRET_KEY - Django secret key
* DEBUG - True or False
* LOCAL_HOST - Local host name (loading settings)
* GMAIL_ADDRESS
* MAIL_PASSWORD

Put them in a .env file and set with:
```
set -a; source .env; set +a;
```
## Making a user
You will want to make a user to see and use the management systems:
```
python manage.py createsuperuser
```

## Deployment
```
python manage.py collectstatic
```

## Built With

* [Django](https://docs.djangoproject.com/en/2.2/) - The web framework used
* [Bootstrap 4](https://getbootstrap.com/docs/4.3/getting-started/introduction/) - CSS framework

## Authors

* **Me, Atsushi Toda** - [GitHub](https://github.com/broadsinatlanta) - [Actual atsushi.dev site](https://www.atsushi.dev)

## License

This project is licensed under the MIT License.

