# HestiaCP Fail2Ban & Firewall Guide

## 1. Verified System Paths (Consult `01-hestia-system-paths.md`)
**CRITICAL:** Fail2Ban state is persisted in SQLite.

| Component | Path |
| :--- | :--- |
| **Active Config** | `/etc/fail2ban/jail.local` |
| **Log File** | `/var/log/fail2ban.log` |
| **Database** | `/var/lib/fail2ban/fail2ban.sqlite3` |
| **Hestia Rules** | `/usr/local/hestia/data/firewall/rules.conf` |

## 2. Check Status
### A. List Active Jails
```bash
sudo -n fail2ban-client status
```
*Common Jails:* `ssh-iptables`, `exim-iptables`, `dovecot-iptables`, `recidive`.

### B. Inspect Specific Jail
```bash
# Syntax: fail2ban-client status JAIL
sudo -n fail2ban-client status ssh-iptables
```

## 3. Unbanning IPs
**Method 1: Hestia CLI (Preferred)**
Removes from Hestia's firewall chain AND Fail2Ban.
```bash
# 1. Find the ban
sudo -n /usr/local/hestia/bin/v-list-firewall-ban json

# 2. Unban
# Syntax: v-delete-firewall-ban IP CHAIN
sudo -n /usr/local/hestia/bin/v-delete-firewall-ban 1.2.3.4 SSH
```

**Method 2: Fail2Ban Client (Direct)**
Use this if Hestia CLI fails or IP is only in Fail2Ban memory.
```bash
# Syntax: fail2ban-client set JAIL unbanip IP
sudo -n fail2ban-client set ssh-iptables unbanip 1.2.3.4
```

## 4. Whitelisting (Permanent)
To prevent an IP from EVER being banned:

1.  **Edit Config:**
    ```bash
    sudo -n nano /etc/fail2ban/jail.local
    ```
2.  **Add to IgnoreIP:**
    Find `[DEFAULT]` section. Add IP to `ignoreip` (space separated).
    ```ini
    ignoreip = 127.0.0.1/8 ::1 192.168.1.50
    ```
3.  **Restart:**
    ```bash
    sudo -n systemctl restart fail2ban
    ```

## 5. Troubleshooting
**Symptoms:** User can't connect, but site works for others.

1.  **Check Logs for Ban:**
    ```bash
    sudo -n grep "Ban" /var/log/fail2ban.log | grep "1.2.3.4"
    ```
2.  **Check IPTables Direct:**
    Sometimes Hestia/Fail2Ban are out of sync.
    ```bash
    sudo -n iptables -L -n -v | grep "1.2.3.4"
    ```

