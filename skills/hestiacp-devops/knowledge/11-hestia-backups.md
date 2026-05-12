# HestiaCP Backup & Restore Guide

## 1. Verified System Paths (Consult `01-hestia-system-paths.md`)
**CRITICAL:** We use a custom backup script (`v-backup-users-custom`).

| Component | Path |
| :--- | :--- |
| **Custom Script** | `/usr/local/hestia/bin/v-backup-users-custom` |
| **Config** | `/etc/hestiacp-backup-custom.conf` |
| **Backup Storage** | `/backup` |
| **Log File** | `/var/log/hestia/backup.log` |

## 2. Our Custom Backup System (`v-backup-users-custom`)
This server uses a **custom wrapper script** that enhances standard Hestia backups.
*   **Feature:** Handles symlinks properly (e.g., shared `public_html`).
*   **Schedule:** Runs via Panel Cron (Admin) or System Cron (Root). Check `hestia-cron-guide.md`.

### A. Run Manual Backup (All Users)
```bash
sudo -n /usr/local/hestia/bin/v-backup-users-custom
```

### B. Run Standard Backup (Single User)
For debugging or quick snapshots:
```bash
# Syntax: v-backup-user USER
sudo -n /usr/local/hestia/bin/v-backup-user admin
```

## 3. Restoration (DANGEROUS)
**WARNING:** Overwrites existing data. Confirm with user first.

### A. Full Restore
```bash
# Syntax: v-restore-user USER BACKUP_FILE
sudo -n /usr/local/hestia/bin/v-restore-user admin admin.2024-03-15.tar
```

### B. Partial Restore (Selective)
Restore ONLY specific components (e.g., DBs only).
**Syntax:** `v-restore-user USER BACKUP [WEB] [DNS] [MAIL] [DB] [CRON] [UDIR] [NOTIFY]`

```bash
# Restore ONLY Databases
sudo -n /usr/local/hestia/bin/v-restore-user admin admin.tar no no no yes no no no
```

## 4. Advanced Backup Management

### A. Integrity Check (Verify without Restore)
To check if a backup file is valid (corrupted gzip/tar):
```bash
# List contents (test read)
tar -tvf /backup/admin.2024-03-15.tar >/dev/null && echo "Backup OK" || echo "Backup Corrupt"
```

### B. Manual Cleanup (Disk Full Emergency)
If `/backup` is full and you need space immediately:
1.  **Find oldest backups:**
    ```bash
    ls -lt --time-style=long-iso /backup | tail -n 10
    ```
2.  **Delete specific file:**
    ```bash
    rm /backup/admin.2023-01-01.tar
    ```
3.  **Update Hestia Database (Important!):**
    If you delete files manually, Hestia still thinks they exist.
    ```bash
    v-update-user-backup-exclusions admin
    # Or just wait for the next nightly run to sync.
    ```

### C. Debugging Stuck Backups
If `v-backup-users` is running forever:
1.  **Check the Queue:**
    ```bash
    v-list-sys-queue
    ```
2.  **Check the Process:**
    ```bash
    ps aux | grep "v-backup"
    ```
3.  **Clear the Lock (Only if 100% stuck):**
    ```bash
    rm /usr/local/hestia/data/queue/backup.pipe
    ```

## 5. Troubleshooting Logs
**Symptoms:** "Backup failed", "Disk full".

1.  **Check Logs:**
    ```bash
    sudo -n tail -n 50 /var/log/hestia/backup.log
    ```
2.  **Check Exclusions:**
    If backups are too big, check exclusion lists:
    ```bash
    /usr/local/hestia/bin/v-list-user-backup-exclusions admin
    ```


