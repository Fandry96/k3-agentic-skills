# HestiaCP Cron Jobs & Automation Guide

## 1. Verified System Paths (Consult `01-hestia-system-paths.md`)
**CRITICAL:** Cron jobs are split between Hestia users and system-wide configurations.

| Component | Path |
| :--- | :--- |
| **Hestia User Crons** | `/var/spool/cron/crontabs/[USER]` |
| **System Crontab** | `/etc/crontab` |
| **System Daily** | `/etc/cron.daily/` |
| **System Hourly** | `/etc/cron.hourly/` |
| **Cron Log** | `/var/log/syslog` (grep CRON) |

## 2. Managing Hestia User Crons
These are managed via the panel or CLI and run as the specific user.

### A. List Jobs
```bash
# Admin users
sudo -n /usr/local/hestia/bin/v-list-cron-jobs admin

# Specific user
sudo -n /usr/local/hestia/bin/v-list-cron-jobs USER
```

### B. Debugging Failures
1.  **Check Exit Code:**
    Hestia doesn't log stdout/stderr by default unless configured.
    Check `/var/log/syslog` for execution:
    ```bash
    sudo -n grep "CRON" /var/log/syslog | grep "USER" | tail -n 20
    ```

2.  **Manually Run a Job:**
    To test a job, run it as the user (NOT root):
    ```bash
    sudo -u USER bash -c "COMMAND"
    ```

## 3. Managing System Crons (Root)
These run as root and are critical for maintenance.

### A. List System Jobs
```bash
# Main crontab
sudo -n cat /etc/crontab

# Daily scripts
ls -l /etc/cron.daily/
```

### B. Custom Maintenance Schedule
Our server has specific custom automation split between Panel and OS levels.

**Sunday Morning Maintenance Sequence:**
This sequence is critical for system health.

1.  **01:00** - `v-backup-users-custom` (Panel Cron - User: `admin`)
    *   *Purpose:* Enhanced backup with symlink support.
2.  **04:30** - `v-clean-garbage` (System Cron - `/etc/cron.d/`)
    *   *Purpose:* Deep system cleanup, log rotation, and temp file removal.
3.  **06:00** - `v-github-mirror` (System Cron - `/etc/cron.d/`)
    *   *Purpose:* Syncs repositories to backup locations.
4.  **08:00** - `v-system-report` (System Cron - `/etc/cron.d/`)
    *   *Purpose:* Generates weekly health status report.

**Daily Routine:**
*   **05:10** - `v-update-sys-queue` (Updates stats/counters)
*   **Daily** - `v-update-sys-hestia-all` (Auto-updates)

**Important:** If troubleshooting "High Load" on Sunday mornings, check this schedule first.

## 4. Common Issues
1.  **"Permission Denied":** The script is not executable (`chmod +x`) or user lacks permissions.
2.  **"Command not found":** Cron has a limited `$PATH`. Always use absolute paths (e.g., `/usr/bin/php` instead of `php`).
3.  **Timezone Mismatch:** Cron runs in system time (`/etc/timezone`). Check `date`.
