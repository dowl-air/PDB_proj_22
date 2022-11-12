# Databázový systém pro správu knihovních služeb  

## Projekt do předmětu PDB

### Autoři

- Daniel Pátek (xpatek08)
- Ondřej Krejčí (xkrejc69)

## Instalace a spuštění

### Prerekvizity

Pro spuštění programu je třeba mít nainstalovaný `Docker` alespoň ve verzi `20.10.20`. Jelikož se jedná o program složený z více služeb, spuštění vyžaduje nainstalovaný také program `docker-compose`.

```bash
sudo apt install docker docker-compose
```

### Spuštění aplikace

Příkaz `make` provede sestavení a spuštění programu v prostředí `Docker`.  

```bash
make
```

### Lokální spuštění aplikace pro vývoj (bez dockerizace)

Příkaz `make venv` provede spuštění aplikace bez využití služeb programu `Docker`.  Využívá k tomu virtualizované prostředí `venv` pro Python.

```bash
sudo apt install python3 python3-venv
make venv
source venv/bin/activate
chmod 775 manage.py
./manage.py flask run
```
