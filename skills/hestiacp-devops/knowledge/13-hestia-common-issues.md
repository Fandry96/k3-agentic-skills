# HestiaCP Common Issues & Troubleshooting Playbook

This guide provides step-by-step decision trees for resolving the most frequent HestiaCP issues on Debian 12.
**ROLE:** Use this as your "Expert Heuristic" when diagnosing problems.

## 1. Web Service Failures (Nginx/Apache/PHP)

### Scenario: "Website gives 500 Error"
1.  **Check Backend (PHP-FPM):**
    *   Action: `systemctl list-units --type=service | grep php` to find version.
    *   Action: `systemctl status php[VER]-fpm`.
    *   *If Down:* `systemctl restart php[VER]-fpm`.
    *   *If Up:* Check logs: `sudo -n grep "error" /var/log/php[VER]-fpm.log | tail -n 20`.
2.  **Check Config Syntax:**
    *   Action: `nginx -t` AND `apache2ctl -t`.
    *   *If Fail:* Report the syntax error line.
3.  **Check Permissions:**
    *   Action: `namei -l /home/[USER]/web/[DOMAIN]/public_html/index.php`
    *   *Fix:* `chown -R [USER]:[USER] /home/[USER]/web/[DOMAIN]/public_html`.

### Scenario: "Website gives 502 Bad Gateway"
*   **Cause:** Nginx cannot talk to Apache or PHP-FPM.
*   **Diagnosis:**
    1.  Is Apache running? `systemctl status apache2`.
    2.  Is PHP-FPM running? `systemctl status php[VER]-fpm`.
    3.  Check Nginx error log: `sudo -n tail -n 20 /var/log/nginx/domains/[DOMAIN].error.log`.

## 2. Database Failures (MariaDB)

### Scenario: "Error Establishing Database Connection"
1.  **Check Service:**
    *   Action: `systemctl status mariadb`.
    *   *If Stopped:* `systemctl start mariadb`.
2.  **Check Connection:**
    *   Action: `mariadb-admin ping`.
    *   *If Fail:* Check credentials in `/etc/mysql/debian.cnf` vs reality.
3.  **Check Resources (OOM):**
    *   Action: `dmesg | grep -i "kill" | grep -i "mariadb"`.
    *   *If Killed:* Server ran out of RAM. Restart MariaDB and warn user to upgrade RAM or add Swap.

## 3. Email Failures (Exim/Dovecot)

### Scenario: "Emails not sending"
1.  **Check Service:**
    *   Action: `systemctl status exim4`.
2.  **Check Queue:**
    *   Action: `exim -bpc`.
    *   *If High (>50):* Check frozen emails: `exim -bp | grep frozen`.
3.  **Check External Block:**
    *   Action: `sudo -n tail -n 50 /var/log/exim4/mainlog | grep "rejected"`.

## 4. Hestia Panel Failures

### Scenario: "Command not found" or "Error 3"
1.  **Path Issue:**
    *   *Fix:* ALWAYS use absolute path `/usr/local/hestia/bin/v-[COMMAND]`.
2.  **Permission Issue:**
    *   *Fix:* ALWAYS use `sudo -n`.
3.  **Variable Issue:**
    *   *Fix:* Hestia commands often need `user` as first argument. Check `v-list-users` first.

## 5. Generic "Fix It" Protocol
If a service is down:
1.  **Pre-Flight Check (MANDATORY):** If the service is `nginx`, `apache2`, or `exim4`, validate syntax FIRST (`nginx -t`, `apache2ctl configtest`, `exim -bV`). If syntax fails, FIX THE CONFIG before restarting.
2.  **Try Restart:** `systemctl restart [service]`.
3.  **Verify:** `systemctl status [service]`.
4.  **If Fail:** Read Logs (`sudo -n journalctl -u [service] -n 50`).
5.  **Report:** "Service [X] failed to start due to [Error from Log]."
