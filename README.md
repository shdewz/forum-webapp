# Keskustelusovellus

*\[Finnish\] Practice project for course TKT20019*

Sovelluksessa näkyy eri aiheisia keskustelualueita, sisältäen viesteistä koostuvia ketjuja.

## Ominaisuudet

- [x] Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen
- [x] Käyttäjä näkee sovelluksen etusivulla listan alueista sekä jokaisen alueen ja ketjun viimeksi lähetetyn viestin ajankohdan
- [x] Käyttäjä voi selata alueita ja ketjuja
- [x] Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön
- [x] Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun
- [x] Käyttäjä voi poistaa lähettämänsä viestin tai ketjun
- [ ] Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana
- [x] Ylläpitäjä voi lisätä uusia keskustelualueita
- [x] Ylläpitäjä voi luoda salaisen alueen
  - [x] Ylläpitäjä voi määrittää, kenellä on pääsy alueelle
  - [x] Salaiset alueet ovat oletuksena piilossa
- [x] Sovellus on tyylitelty

## Käyttö

Kloonaa repositorio ja luo juurikansioon esimerkin mukainen `.env`-tiedosto:

```dotenv
DATABASE_URL=<tietokannan-osoite>
SECRET=<secret-key>
```

Aktivoi virtuaaliympäristö ja asenna riippuvuudet komennoilla

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r ./requirements.txt
```

Määritä tietokannan skeema komennolla

```bash
$ psql < schema.sql
```

Aja sovellus komennolla

```bash
$ flask run
```