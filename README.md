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

Sestavení a spuštění programu v prostředí `Docker` funguje pomocí dvou následujících příkazů. Volitelný parametr `-d` značí spuštění na pozadí.

```bash
docker compose build
docker compose up -d
```

Pro vypnutí běžícího kontejneru na pozadí je nutné zadat níže uvedený příkaz.

```bash
docker compose down
```

### Lokální spuštění aplikace pro vývoj (bez dockerizace)

Spuštění aplikace bez využití služeb programu `Docker` vyžaduje mít naistalovány všechny požadované služby a knihovny. Zejména se jedná o databáze MySQL, MongoDB a platformu Apache Kafka včetně 

Je vhodné využít virtualizované prostředí `venv` pro Python.

```bash
python3 install -r requirements.txt
python3 app/run.py
./run_consumer.sh
```

### Spuštění testů

Pro spuštění testů je zapotřebí buď běžící docker container (spuštěný pomocí příkazů uvedených výše) nebo lokálně spuštěné všechny potřebné služby popsané v odstavci výše. Samotné spuštění testů se provede příkazem `./run_tests.sh`.

V případě spouštění v docker containeru je nejprve potřeba se do daného konteineru připojit. K tomu slouží následující příkaz.

```bash
docker exec -it rest_api bash
./run_tests.sh
```
