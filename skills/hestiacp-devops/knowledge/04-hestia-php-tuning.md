# PHP-FPM Performance Tuning Guide

## 1. Verified System Paths (Consult `01-hestia-system-paths.md`)
**CRITICAL:** Before checking any config, refer to `01-hestia-system-paths.md` for the exact location.

| Config Type | Path Pattern |
| :--- | :--- |
| **Per-Domain Performance** | `/etc/php/[VER]/fpm/pool.d/[DOMAIN].conf` |
| **Global PHP Settings** | `/etc/php/[VER]/fpm/php.ini` |
| **Hestia Templates** | `/usr/local/hestia/data/templates/web/php-fpm/` |

## 2. Diagnosis & Troubleshooting
When a site is slow or returns 502/504 errors, check if PHP-FPM is hitting limits or crashing.

### A. Real-time Monitoring
Check active PHP processes and memory usage:
```bash
# Count processes per pool
sudo -n ps aux | grep "php-fpm: pool" | awk '{print $12}' | sort | uniq -c | sort -nr

# Check RAM usage per process (Average)
sudo -n ps --no-headers -o "rss,cmd" -C php-fpm8.2 | awk '{ sum+=$1 } END { printf ("%d%s\n", sum/NR/1024,"Mb") }'
```

### B. Log Analysis (The "Why")
```bash
# 1. Global FPM Log (Process Manager warnings)
# Look for "server reached pm.max_children setting"
sudo -n grep "max_children" /var/log/php*-fpm.log | tail -n 20

# 2. Domain Error Log (Timeouts/Fatal Errors)
# Look for "upstream timed out" (504) or "recv() failed" (502)
sudo -n grep -E "timed out|recv\(\) failed" /var/log/nginx/domains/*.error.log | tail -n 20
```

### C. Identifying OOM Kills (Out of Memory)
If PHP processes disappear or the service restarts, the OS might be killing them to save RAM.
```bash
sudo -n grep -i "killed process" /var/log/syslog | grep php
dmesg | grep -i "oom-killer"
```

### D. Slow Log Analysis (Find the bad script)
To find *exactly* which PHP script is slow:
1.  Edit the domain pool: `/etc/php/[VER]/fpm/pool.d/[DOMAIN].conf`
2.  Add/Uncomment:
    ```ini
    request_slowlog_timeout = 5s
    slowlog = /var/log/php[VER]-fpm-[DOMAIN].slow.log
    ```
3.  Restart PHP-FPM.
4.  Wait for slowness, then check the log:
    ```bash
    sudo -n cat /var/log/php[VER]-fpm-[DOMAIN].slow.log
    ```

## 3. Tuning Per-Domain Performance (The Right Way)
**Do NOT edit `php.ini` for site-specific performance.** HestiaCP uses separate pools for each domain.

### A. Adjusting `pm.max_children` (Worker Limit)
If your logs say `server reached pm.max_children setting`, you need more workers for that specific site.

1.  **Identify the PHP version:**
    Check the domain config or use `v-list-web-domain USER DOMAIN`.
2.  **Edit the Pool Config:**
    ```bash
    sudo -n nano /etc/php/[VER]/fpm/pool.d/[DOMAIN].conf
    ```
3.  **Modify the PM Settings:**
    Find `pm.max_children`.
    *   **Low Traffic:** 2-5
    *   **Medium Traffic:** 10-20
    *   **High Traffic:** 30-50 (Ensure you have RAM! ~60MB per worker)
    *   *Formula:* `(Total RAM - 2GB) / 60MB = Max Total Workers`
4.  **Restart PHP-FPM:**
    ```bash
    sudo -n systemctl restart php[VER]-fpm
    ```

### B. Creating a Custom Template (Permanent Fix)
Editing the pool file directly works, but Hestia might overwrite it on rebuild. The best practice is to create a custom template.

1.  **Copy default template:**
    ```bash
    cd /usr/local/hestia/data/templates/web/php-fpm/
    cp default.tpl high-traffic.tpl
    ```
2.  **Edit the new template:**
    Set `pm.max_children = 40` (or your calculated value).
3.  **Apply to Domain:**
    ```bash
    v-change-web-domain-backend-tpl USER DOMAIN high-traffic
    ```

## 4. Tuning Global PHP Settings (php.ini)
Use this for `memory_limit`, `upload_max_filesize`, etc.

**Commands (using sed for quick edits):**
Replace `8.2` with the correct PHP version.

```bash
# Check current config
sudo -n grep -E "memory_limit|max_execution_time|upload_max_filesize" /etc/php/8.2/fpm/php.ini

# Increase Memory Limit to 512MB
sudo -n sed -i "s/memory_limit = .*/memory_limit = 512M/" /etc/php/8.2/fpm/php.ini

# Increase Upload Size to 64M
sudo -n sed -i "s/upload_max_filesize = .*/upload_max_filesize = 64M/" /etc/php/8.2/fpm/php.ini
sudo -n sed -i "s/post_max_size = .*/post_max_size = 64M/" /etc/php/8.2/fpm/php.ini

# Restart PHP-FPM
sudo -n systemctl restart php8.2-fpm
```

