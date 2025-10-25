# bqs-node-manager

Small Node Manager service that provides node ID leases over gRPC. This repo contains a small server (`src/node_manager.py`) and a simple client (`src/node.py`) and uses a local SQLite database to persist leases.

## Goals

- Provide a way to allocate and manage node ID leases for callers (callsigns).
- Allow allocation from a configured ID range (or disable range allocation).

## Prerequisites

- Python 3.10+ (project uses modern typing features)
- pip
- A working terminal (PowerShell is used in the examples below)

Optional dependencies (may already be included in the project's environment):

- grpcio
- protobuf

If the project exposes dependencies in `pyproject.toml`, install them into a virtual environment (recommended):

```powershell
# create and activate venv (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# install package in editable mode (if pyproject defines install_requires)
pip install -e .
```

If you don't have an editable install available, you can instead `pip install grpcio protobuf` manually before running the scripts.

## Database schema

The service persists leases in a `leases` table. Create a SQLite database and the `leases` table using the following schema (example):

```sql
CREATE TABLE IF NOT EXISTS leases (
    node_id INTEGER PRIMARY KEY,
    callsign TEXT,
    expiry INTEGER,
    created_at INTEGER,
    created_by TEXT,
    updated_at INTEGER,
    updated_by TEXT,
    deleted_at INTEGER NULL,
    deleted_by TEXT NULL,
    row_version INTEGER DEFAULT 0,
    is_active INTEGER DEFAULT 1
);
```

Notes:

- `node_id` is the primary key.
- `is_active` is expected to be 1 for active leases and 0 for released/deleted leases. The repository queries only active leases when determining availability.

## Configuration

The code expects two configuration objects returned by the project's configuration initializer (`utils.initialize_config()`):

1) `dbConfig` — an object used to construct data access repositories.

   - When using the provided `data_access.Config` class, `dbConfig` should include at minimum the following attributes:
     - `db_name` (str): path to the SQLite database file (e.g., `"./bqs.db"`)
     - `node_id_range_start` (int): inclusive start of allocatable node id range (example: `1000`)
     - `node_id_range_end` (int): inclusive end of allocatable node id range. Set to `0` to disable range allocation.

   Example Python snippet to create the `dbConfig` object manually:

   ```python
   from data_access.config import Config

   dbConfig = Config(db_name="./bqs.db", node_id_range_start=1000, node_id_range_end=1999)
   ```

   - Important behavior enforced by the repository:
     - If `node_id_range_end` is set to `0`, the allocatable range is disabled and the repository will not auto-assign IDs.
     - The repository only allocates node IDs from within the configured range when range allocation is enabled.
     - IDs that are not currently `is_active = 1` are considered available for re-use.

2) `config` — runtime settings used by the server and client. This is expected to be a mapping (dict-like) with at least the following structure:

   ```yaml
   rpc:
     host: "127.0.0.1"
     port: 50051

   node:
     callsign: "MYNODE"
   ```

   Example Python dict:

   ```python
   config = {
       "rpc": {"host": "127.0.0.1", "port": 50051},
       "node": {"callsign": "MYNODE"}
   }
   ```

## Running the server (manual)

1. Make sure the database file exists and the `leases` table has been created (see the SQL above). You can create the DB with the sqlite3 CLI:

   ```powershell
   # create database and table (PowerShell example)
   sqlite3 .\bqs.db < create_schema.sql
   ```

2. Start the server from the project root (activate the venv first if used):

```powershell
python src\node_manager.py
```

The server will call `utils.initialize_config()` to load `dbConfig` and `config` and then start a gRPC server listening on `config['rpc']['port']`.

## Running the client (manual)

With the server running, run the client script. The client uses the `config['rpc']['host']` and `config['rpc']['port']` values to connect and will request a lease for the callsign in `config['node']['callsign']`.

```powershell
python src\node.py
```

## Creating a `dbConfig` when testing in REPL

If you want to exercise the repository directly in a Python REPL or test script, construct the configuration and repository like this:

```python
from data_access.config import Config
from data_access.repository import LeaseRepository

dbConfig = Config(db_name="./bqs.db", node_id_range_start=1000, node_id_range_end=1999)
repo = LeaseRepository(dbConfig)

# Example: request a lease for node_id=0 (auto-assign within range)
lease = repo.create_lease(0, "TESTNODE", expiry=0)
print(lease)
```

## Behavior notes and constraints

- Range-only allocation: the repository will only allocate node IDs from the configured range when `node_id_range_end` is non-zero. If the range is disabled (`node_id_range_end == 0`) the repository will not auto-assign IDs — callers must provide a valid `node_id` when creating leases.
- Reuse of IDs: a node ID is considered available for allocation if there is no active lease (`is_active = 1`) currently using it.
- If the configured range is exhausted (no available IDs) the repository will raise an error — that condition should be handled by the caller or surfaced to the operator.

## Troubleshooting

- If the server fails to start, check logs printed to the console. Confirm the `config` structure contains the `rpc.port` and, if used, that `dbConfig.db_name` points to a writable SQLite file.
- If lease allocation fails with a `ValueError` about the configured range, either expand the range or free up inactive leases in the DB.
