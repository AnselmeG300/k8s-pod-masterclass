import logging
import os
import socket
import time
from contextlib import asynccontextmanager

import psycopg2
from fastapi import FastAPI, Response

# Configuration lue depuis l'environnement.
# En cluster, ces valeurs sont injectees par des env, des ConfigMap/Secret
# ou la Downward API (POD_NAME, POD_IP, node, etc.).
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "demo")
DB_USER = os.getenv("DB_USER", "demo")
DB_PASSWORD = os.getenv("DB_PASSWORD", "demo")
POD_NAME = os.getenv("POD_NAME", socket.gethostname())
NODE_NAME = os.getenv("NODE_NAME", "inconnu")
STARTUP_DELAY = int(os.getenv("STARTUP_DELAY", "15"))

# Logs vers stdout ET vers un fichier partage.
# Le fichier est ecrit dans un volume emptyDir monte aussi par le sidecar,
# qui se contente de le suivre (tail).
LOG_PATH = os.getenv("LOG_PATH", "/var/log/app/app.log")
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format=f"%(asctime)s %(levelname)s [{POD_NAME}] %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler(LOG_PATH)],
)
log = logging.getLogger("demo-api")

_boot = time.time()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    log.info("Demarrage sur le noeud %s, warm-up de %ss", NODE_NAME, STARTUP_DELAY)
    yield
    # Declenche a la reception de SIGTERM : c'est ici que se joue
    # l'arret propre (fin du cycle de vie du Pod).
    log.info("Arret propre en cours (SIGTERM recu)")


app = FastAPI(title="demo-api", lifespan=lifespan)


def warmed_up() -> bool:
    # Le warm-up est simule par un delai. Il rend la startup probe utile :
    # tant qu'il n'est pas ecoule, l'app n'est pas consideree comme demarree.
    return (time.time() - _boot) >= STARTUP_DELAY


def db_ok() -> bool:
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            connect_timeout=2,
        )
        conn.close()
        return True
    except Exception as exc:
        log.warning("Base injoignable: %s", exc)
        return False


@app.get("/")
def root():
    return {"app": "demo-api", "pod": POD_NAME, "node": NODE_NAME}


@app.get("/startupz")
def startupz(response: Response):
    # Cible de la startup probe : passe a 200 une fois le warm-up termine.
    if warmed_up():
        return {"status": "started", "pod": POD_NAME}
    response.status_code = 503
    return {"status": "starting", "pod": POD_NAME}


@app.get("/healthz")
def healthz():
    # Cible de la liveness probe : le process repond, donc il est vivant.
    # Ne depend volontairement pas de la base : une base coupee ne doit pas
    # faire redemarrer le conteneur.
    return {"status": "alive", "pod": POD_NAME}


@app.get("/readyz")
def readyz(response: Response):
    # Cible de la readiness probe : pret a recevoir du trafic seulement si
    # le warm-up est fini ET la base est joignable. Sinon 503, et le Pod
    # sort des endpoints du Service sans etre tue.
    if warmed_up() and db_ok():
        return {"status": "ready", "pod": POD_NAME}
    response.status_code = 503
    return {"status": "not-ready", "pod": POD_NAME}
