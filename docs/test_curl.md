# API (REST)

## Créer une classe
```bash
curl -X POST http://localhost:8000/api/classes \
  -H "Content-Type: application/json" \
  -d '{"number":"6A","name":"Sixième A","level":"6e"}'
```

## Lister les classes
```bash
curl http://localhost:8000/api/classes
```

## Récupérer par numéro
```bash
curl http://localhost:8000/api/classes/by-number/6A
```

## Ajouter un créneau
```bash
curl -X POST http://localhost:8000/api/schedules/class/1 \
  -H "Content-Type: application/json" \
  -d '{
    "subject":"Maths",
    "teacher":"Mme Dupont",
    "room":"101",
    "start_time":"2026-03-18T09:00:00",
    "end_time":"2026-03-18T10:00:00"
  }'
```

## Lister l'emploi du temps (fenêtré)
```bash
curl "http://localhost:8000/api/schedules/class/1?start=2026-03-18T00:00:00&end=2026-03-19T00:00:00"
```

## Supprimer un créneau
```bash
curl -X DELETE http://localhost:8000/api/schedules/1 -i
```

# MCP Server (Model Context Protocol)

## Lister les classes (MCP)
```bash
curl -X POST http://localhost:8000/mcp/list_classes
```

## Récupérer une classe par numéro (MCP)
```bash
curl -X POST http://localhost:8000/mcp/get_class_by_number \
  -H "Content-Type: application/json" \
  -d '{"arguments": {"number": "6A"}}'
```

## Ajouter un créneau via MCP
```bash
curl -X POST http://localhost:8000/mcp/add_schedule_entry \
  -H "Content-Type: application/json" \
  -d '{"arguments": {"class_id": 1, "subject": "Maths", "start_time": "2026-03-18T09:00:00", "end_time": "2026-03-18T10:00:00"}}'
```