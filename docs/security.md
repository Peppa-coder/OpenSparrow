# 🔐 Security Model

OpenSparrow exposes **shell execution and file system access** via web and chat interfaces. Security is treated as a **first-class subsystem**, not an afterthought.

## Threat Model

| Threat | Mitigation |
|--------|-----------|
| Unauthorized access | Token auth + RBAC |
| Path traversal | Workspace sandbox with resolve-and-check |
| Destructive commands | Risk classification + approval gates |
| Secret leakage | Auto-redaction in logs and UI |
| Brute force | Rate limiting |
| Compromised channel | Per-channel trust levels |

## Authentication

- **JWT Tokens**: Stateless auth with configurable expiration
- **Admin Token**: Auto-generated on first run for initial setup
- **Per-Channel Auth**: Each messaging adapter verifies user identity independently

## Authorization (RBAC)

| Action | Admin | Member | Viewer |
|--------|:-----:|:------:|:------:|
| Read files | ✅ | ✅ | ✅ |
| Write files | ✅ | ✅ | ❌ |
| Delete files | ✅ | ❌ | ❌ |
| Execute commands | ✅ | ✅ | ❌ |
| Execute dangerous commands | ✅ | ❌ | ❌ |
| Approve tasks | ✅ | ❌ | ❌ |
| View audit log | ✅ | ❌ | ✅ |
| Manage config | ✅ | ❌ | ❌ |
| Backup/restore | ✅ | ❌ | ❌ |

## Workspace Sandbox

All file operations are **restricted to `workspace_root`** (default: `~/sparrow-workspace`).

```python
# Every path is resolved and validated:
resolved = (workspace_root / user_path).resolve()
resolved.relative_to(workspace_root)  # Raises if outside boundary
```

Protects against: `../../etc/passwd`, symlink escapes, absolute path injection.

## Command Risk Classification

| Level | Behavior | Examples |
|-------|----------|---------|
| **AUTO** | Execute immediately | `ls`, `cat`, `pwd` |
| **CONFIRM** | User must approve | `cp`, `mv`, general commands |
| **ADMIN** | Admin approval required | `rm -rf`, `git push --force`, `pip install` |
| **FORBIDDEN** | Always blocked | `rm -rf /`, `mkfs`, fork bombs |

## Audit Trail

Every operation is recorded:

```json
{
  "id": "...",
  "timestamp": "2026-04-27T15:30:00Z",
  "user_id": "alice",
  "action": "shell.execute",
  "target": "git status",
  "result": "success",
  "channel": "telegram"
}
```

Secrets are automatically redacted: API keys, tokens, passwords are replaced with `[REDACTED]` in all logs.

## Best Practices

1. **Change default admin token** after first setup
2. **Use Ollama** for maximum data privacy (no data leaves your machine)
3. **Restrict Telegram users** via `SPARROW_TELEGRAM_ALLOWED_USERS`
4. **Review audit logs** regularly via the Dashboard
5. **Back up** the SQLite database periodically
