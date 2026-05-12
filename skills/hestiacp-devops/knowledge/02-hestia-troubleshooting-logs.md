# HestiaCP Logs & Troubleshooting Guide

## 1. Verified System Paths (Consult `01-hestia-system-paths.md`)
**CRITICAL:** Before checking any log, refer to `01-hestia-system-paths.md` for the exact location. This guide summarizes common diagnostic workflows using those verified paths.

## 2. Essential Log Commands
Use these commands to extract meaningful data. **Always use `sudo -n`**.

| Component | Goal | Command Pattern |
| :--- | :--- | :--- |
| **Email (Live)** | Watch incoming/outgoing mail | `sudo -n tail -f /var/log/exim4/mainlog` |
| **Email (History)** | Find specific address (incl. rotated) | `sudo -n zgrep "user@domain.com" /var/log/exim4/mainlog*` |
| **Email (Count)** | Count emails without dumping log | `sudo -n zgrep -c "user@domain.com" /var/log/exim4/mainlog*` |
| **Web Errors** | Real-time website errors | `sudo -n tail -f /var/log/apache2/domains/DOMAIN.error.log` |
| **Web Access** | Who is visiting now? | `sudo -n tail -f /var/log/nginx/domains/DOMAIN.log` |
| **PHP Crash** | Check for OOM/Segfaults | `sudo -n grep "segfault" /var/log/syslog` |
| **DB Crash** | Why did MariaDB die? | `sudo -n tail -n 50 /var/log/mysql/error.log` |
| **Firewall Bans** | Who is banned by Fail2Ban? | `sudo -n tail -n 50 /var/log/fail2ban.log` |
| **Virus Scan** | ClamAV mail/security results | `sudo -n tail -n 50 /var/log/clamav/clamav.log` |
| **SSH Brute Force** | Who is trying to hack SSH? | `sudo -n grep "Failed password" /var/log/auth.log \| tail -n 20` |

## 3. Component-Specific Diagnostics

### A. Web Server (Nginx + Apache + PHP-FPM)
**Symptoms:** 502 Bad Gateway, 504 Gateway Time-out, White Screen of Death.

1.  **Check Service Status:**
    ```bash
    sudo -n systemctl status nginx apache2 php*-fpm
    ```
2.  **Analyze Global Errors (Root Cause):**
    ```bash
    sudo -n tail -n 20 /var/log/nginx/error.log
    sudo -n tail -n 20 /var/log/apache2/error.log
    ```
3.  **Analyze Domain-Specific Errors:**
    *   Path: `/var/log/apache2/domains/[DOMAIN].error.log` (Apache handles the backend logic).
    *   Path: `/var/log/nginx/domains/[DOMAIN].error.log` (Nginx handles proxy/static errors).
4.  **PHP-FPM Debugging:**
    *   Check specific version logs: `/var/log/php[VER]-fpm.log`.
    *   **Pro Tip:** If a site is slow, check if it's hitting `max_children` limits in its pool config (`/etc/php/[VER]/fpm/pool.d/[DOMAIN].conf`).

### B. Mail System (Exim4 + Dovecot)
**Symptoms:** Email not delivered, "User unknown", "Relay not permitted".

1.  **Trace an Email:**
    The `mainlog` is your best friend. It tracks every stage (Arrival `<=`, Delivery `=>`, Completion `Completed`).
    ```bash
    sudo -n grep "MSG_ID_OR_EMAIL" /var/log/exim4/mainlog
    ```
2.  **Check Rejections:**
    If an email was blocked immediately (DNSBL, Spam), it's in `rejectlog`.
    ```bash
    sudo -n tail -n 20 /var/log/exim4/rejectlog
    ```
3.  **Authentication Errors:**
    If a user can't login to Outlook/Thunderbird, check Dovecot.
    ```bash
    sudo -n tail -f /var/log/dovecot.log
    ```

### C. Database (MariaDB)
**Symptoms:** "Error Establishing Database Connection", Slow queries.

1.  **Check if Alive:**
    ```bash
    sudo -n systemctl status mariadb
    ```
2.  **Analyze Crash Logs:**
    If MariaDB restarts often, it's likely Out of Memory (OOM).
    ```bash
    sudo -n grep -i "shutdown" /var/log/mysql/error.log
    sudo -n dmesg | grep -i "kill"
    ```
3.  **Optimization:**
    Check `innodb_buffer_pool_size` in `/etc/mysql/mariadb.conf.d/50-server.cnf` vs available RAM.

## 4. Advanced Log Techniques

### A. Watching Multiple Logs (Real-time)
Instead of opening 5 terminals, watch all web errors at once:
```bash
# Watch all Nginx domain errors
sudo -n tail -f /var/log/nginx/domains/*.error.log

# Watch all Apache domain errors
sudo -n tail -f /var/log/apache2/domains/*.error.log
```

### B. Filtering by Time (What happened today?)
Don't scroll through millions of lines. Filter by date:
```bash
# Find errors from Today (regex matches date format in logs)
sudo -n grep "^$(date +%Y/%m/%d)" /var/log/nginx/domains/example.com.error.log
```

### C. Systemd Logs (Journalctl)
Some services (like php-fpm or mariadb) log startup/crash errors to systemd, not just files.
```bash
# Why did the service fail to start?
sudo -n journalctl -u mariadb.service --no-pager -n 50

# Follow live output of a service
sudo -n journalctl -u php8.2-fpm.service -f
```

### D. Finding the "Top" Errors
What is the most common error on your server?
```bash
# Top 10 Nginx errors
sudo -n grep "error" /var/log/nginx/error.log | awk -F'] ' '{print $2}' | sort | uniq -c | sort -nr | head -n 10
```

### E. Summarizing Massive Log Outputs (Batch Processing)
**CRITICAL:** Never `cat` or `zgrep` a full day's log without summarizing first. Massive outputs will crash your context limit.
1.  **Count matches first:** Use `zgrep -c` or `wc -l`.
    ```bash
    # Count how many emails were sent/received by this address across all logs
    sudo -n zgrep -c "olgafreitas@koolfitness.pt" /var/log/exim4/mainlog*
    ```
2.  **Filter by time blocks (Batching):** If you need to read the contents of a busy day, chunk it by hours.
    ```bash
    # Show emails only between 10:00 and 10:59 on March 15
    sudo -n zgrep "^2026-03-15 10:" /var/log/exim4/mainlog.1
    ```
3.  **Use `head` or `tail` for previews:**
    ```bash
    # Look at the first 50 results to understand the pattern before dumping everything
    sudo -n zgrep "olgafreitas@koolfitness.pt" /var/log/exim4/mainlog.1 | head -n 50
    ```


