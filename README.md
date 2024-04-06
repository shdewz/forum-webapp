# Keskustelusovellus

*\[Finnish\] Practice project for course TKT20019*

Sovelluksessa näkyy eri aiheisia keskustelualueita, sisältäen viesteistä koostuvia ketjuja.

## Ominaisuudet

- [ ] Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen
- [x] Käyttäjä näkee sovelluksen etusivulla listan alueista sekä jokaisen alueen ja ketjun viimeksi lähetetyn viestin ajankohdan
- [x] Käyttäjä voi selata alueita ja ketjuja
- [ ] Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön
- [ ] Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun
- [ ] Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä. Käyttäjä voi myös poistaa ketjun tai viestin
- [ ] Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana
- [ ] Ylläpitäjä voi lisätä ja poistaa keskustelualueita
- [ ] Ylläpitäjä voi luoda salaisen alueen ja määrittää, keillä käyttäjillä on pääsy alueelle
  - [x] Salaiset alueet ovat oletuksena piilossa
- [x] Sovellus on tyylitelty

## Käyttö

Kloonaa repositorio ja luo juurikansioon esimerkin mukainen `.env`-tiedosto:

```dotenv
DATABASE_URL=<tietokannan-osoite>
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