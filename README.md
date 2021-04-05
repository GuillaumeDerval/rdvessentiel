The app is only plain HTML/CSS/JS, and is distributed via Github pages.
Test it locally with

```
python -m http.server 8000
```

The python part is only a counter that helps me to estimate the visits to the website, without storing too much log.

# Updating translations

```
PYTHONPATH=$PYTHONPATH:`pwd` pybabel extract -F pybabel.ini -o locales/catalog.pot .
pybabel update -i locales/catalog.pot -o locales/fr.po -l fr
pybabel update -i locales/catalog.pot -o locales/en.po -l en
pybabel update -i locales/catalog.pot -o locales/nl.po -l nl
```