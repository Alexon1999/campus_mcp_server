# Assistant scolaire intelligent

Le but de projet est de donner accès à un LLM une basse de conaissance et outils afin de gérer et répondre au mieux les besoins des nouveaux arrivants (élèves, parents)

Pour cela on va utiliser MCP server. clique-ici pour en savoir plus sur le concept de [MCP server](./docs/mcp_server.md)

## Implémentation

1) Une **API REST FastAPI** qui expose des endpoints pour gérer les classes et leurs emplois du temps (identifiées par un numéro de classe).
2) Un **serveur MCP (Model Context Protocol)** qui fournit des outils (tools) utilisables par un LLM. Le LLM interagit avec le serveur MCP, qui appelle ensuite notre API REST pour effectuer les actions demandées.

## Architecture

### Vue d'ensemble

Le flux principal est :

- Le **LLM** (via MCP) interroge le serveur MCP en lui demandant d'exécuter un outil (ex : `list_classes`, `get_schedule`, `add_entry`).
- Le **serveur MCP** transforme l'appel en requêtes HTTP vers l'**API FastAPI**.
- L'**API FastAPI** utilise **SQLAlchemy** pour accéder à la base **SQLite** (`school.db`).

```
LLM  →  MCP Server (tools: list_classes, get_class, add_class, get_schedule, add_entry, ...)
           ↓ HTTP
        FastAPI (REST)
           ↓ SQLAlchemy
         SQLite (school.db)
```

### Composants clés

- **MCP Server** : expose des outils (`tools`) que le LLM peut appeler. C'est le point d'entrée pour toute interaction LLM → application.
- **FastAPI (REST)** : API métier pour gérer les classes, emplois du temps et les données associées.
- **SQLAlchemy** : couche ORM pour accéder et manipuler les données dans **SQLite**.

### Outils MCP exposés

Quelques outils disponibles :

- `list_classes` : liste toutes les classes.
- `get_class` : détail d'une classe.
- `add_class` : créer une nouvelle classe.
- `get_schedule` : récupérer l'emploi du temps.
- `add_entry` : ajouter un créneau/événement dans l'emploi du temps.

> Pour plus de détails sur le protocole MCP et comment il fonctionne, voir [docs/mcp_server.md](./docs/mcp_server.md).

## Commandes pour lancer le serveur
docker-compose up -d

docker-compose logs api -f

## Améliorations

- Inclure ce MCP server dans un LLM
- Ajouter un logger
- Ajouter un swagger/open api pour notre api rest
- Ajouter un système de migration avec Alembic
- Ajouter une sécurité JWT / API Key
- Création de front React/Vite pour visualiser les emplois du temps
