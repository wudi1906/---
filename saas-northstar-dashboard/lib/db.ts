import Database from 'better-sqlite3'
import { existsSync, mkdirSync } from 'node:fs'
import { dirname, join } from 'node:path'

const DB_PATH = join(process.cwd(), 'data', 'dashboard.db')
const DB_DIR = dirname(DB_PATH)

if (!existsSync(DB_DIR)) {
  mkdirSync(DB_DIR, { recursive: true })
}

const db = new Database(DB_PATH)
db.pragma('journal_mode = WAL')

db.exec(`
CREATE TABLE IF NOT EXISTS imports (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  template_id TEXT NOT NULL,
  datasets_json TEXT NOT NULL,
  mappings_json TEXT NOT NULL,
  calculation_json TEXT NOT NULL,
  created_at TEXT NOT NULL
);
`)

export function withTransaction<T>(fn: () => T): T {
  const transaction = db.transaction(fn)
  return transaction()
}

export function getDb() {
  return db
}
