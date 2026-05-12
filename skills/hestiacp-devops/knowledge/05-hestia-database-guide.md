# HestiaCP Database Maintenance (MariaDB)

## 1. Verified System Paths (Consult `01-hestia-system-paths.md`)
**CRITICAL:** Before editing configs, refer to `01-hestia-system-paths.md`.

| Component | Path |
| :--- | :--- |
| **Global Config** | `/etc/mysql/my.cnf` (Symlink to `mariadb.cnf`) |
| **Server Config** | `/etc/mysql/mariadb.conf.d/50-server.cnf` (**Optimization Here**) |
| **Error Log** | `/var/log/mysql/error.log` |
| **Data Dir** | `/var/lib/mysql` |

## 2. Environment
- **Binary:** `mariadb`
- **Dump Tool:** `mariadb-dump`
- **Socket:** `/run/mysqld/mysqld.sock`

## 3. Advanced Diagnostics (Live Monitoring)

### A. What is running NOW? (Processlist)
If the database is slow, check active queries:
```bash
sudo -n mariadb -e "SHOW FULL PROCESSLIST;"
# OR
sudo -n mariadb-admin proc -v
```
*Look for queries in `Query` state for > 5 seconds.*

### B. Slow Query Analysis (Why is it slow?)
To catch slow queries, enable the log temporarily:
1.  Enable on the fly (no restart needed):
    ```bash
    sudo -n mariadb -e "SET GLOBAL slow_query_log = 'ON';"
    sudo -n mariadb -e "SET GLOBAL long_query_time = 2;" # Log queries > 2 seconds
    ```
2.  Watch the log:
    ```bash
    sudo -n tail -f /var/log/mysql/mariadb-slow.log
    ```
3.  Disable when done:
    ```bash
    sudo -n mariadb -e "SET GLOBAL slow_query_log = 'OFF';"
    ```

### C. Connection Limits (Too many users?)
Check if you are hitting `max_connections`:
```bash
sudo -n mariadb -e "SHOW VARIABLES LIKE 'max_connections';"
sudo -n mariadb -e "SHOW STATUS LIKE 'Max_used_connections';"
```
*If `Max_used_connections` is close to `max_connections`, increase it in `50-server.cnf`.*

### D. InnoDB Status (Deep Dive)
For deadlocks or complex lock issues:
```bash
sudo -n mariadb -e "SHOW ENGINE INNODB STATUS\G"
```

## 4. Common Maintenance Tasks

### A. Backup Databases
**Recommended:** Use Hestia's backup tool which preserves metadata.
```bash
sudo -n /usr/local/hestia/bin/v-backup-user USER
```

### B. Repair & Optimize
If tables are crashed or slow:
```bash
sudo -n mariadb-check --auto-repair --optimize --all-databases
```

### C. Diagnosing Crashes (OOM Killer)
If MariaDB keeps stopping/restarting, it's 99% RAM exhaustion.
```bash
# Check System Logs for "Out of Memory" kills
sudo -n grep -i "killed process" /var/log/syslog | grep mariadb
# Check MariaDB Error Log
sudo -n tail -n 50 /var/log/mysql/error.log
```


## 5. Hestia CLI for Databases
- **Add DB:** `v-add-database USER DATABASE DBUSER DBPASS`
- **List DBs:** `v-list-databases USER`

