# HestiaCP ClamAV & Security Guide

## 1. Verified System Paths (Consult `01-hestia-system-paths.md`)
**CRITICAL:** ClamAV is resource-intensive. Check logs if RAM is high.

| Component | Path |
| :--- | :--- |
| **Daemon Config** | `/etc/clamav/clamd.conf` |
| **Updater Config** | `/etc/clamav/freshclam.conf` |
| **Log File** | `/var/log/clamav/clamav.log` |
| **Update Log** | `/var/log/clamav/freshclam.log` |
| **Virus DB** | `/var/lib/clamav` (`daily.cld`, `main.cld`) |

## 2. Service Management
```bash
# Check Daemon (Scanning)
sudo -n systemctl status clamav-daemon

# Check Updater
sudo -n systemctl status clamav-freshclam
```

## 3. Manual Virus Database Update
If `freshclam` is failing or locked:
```bash
# 1. Stop the service first (locks the DB)
sudo -n systemctl stop clamav-freshclam

# 2. Run manual update
sudo -n freshclam

# 3. Restart service
sudo -n systemctl start clamav-freshclam
```

## 4. Manual Scanning (Ad-Hoc)
**Use `clamdscan` (Daemon) instead of `clamscan` (Standalone).**
`clamdscan` is faster because it uses the already loaded database in RAM.

```bash
# Scan a specific web directory
sudo -n clamdscan --multiscan --fdpass /home/USER/web/DOMAIN/public_html
```

**Options:**
*   `--multiscan`: Use multiple threads.
*   `--fdpass`: Pass file descriptor permissions (Fixes "Access Denied").
*   `--log=/var/log/clamav/manual-scan.log`: Save results.

## 5. Performance Tuning
If ClamAV kills the server (OOM):
1.  **Check `clamdtop`:** Live view of what it's scanning.
2.  **Exclude Paths:** Edit `/etc/clamav/clamd.conf` -> `ExcludePath`.
3.  **RAM Usage:** ClamAV needs ~1.5GB RAM just to load definitions. If you have < 4GB RAM, add Swap (`fallocate -l 2G /swapfile && mkswap /swapfile && swapon /swapfile`) or consider upgrading the VPS RAM. Do NOT disable ClamAV as a first resort — security should always be preserved.

## 6. Integration
*   **Mail:** Enabled via Hestia UI -> Mail Domain -> Edit -> Antivirus.
*   **File System:** Hestia does NOT auto-scan files. You must setup a cron or run manually.

