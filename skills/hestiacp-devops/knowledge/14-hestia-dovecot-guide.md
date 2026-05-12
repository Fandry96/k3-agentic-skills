# HestiaCP Dovecot (IMAP/POP3) Troubleshooting Guide

## 1. Verified System Paths (Consult `01-hestia-system-paths.md`)
**CRITICAL:** Dovecot handles all IMAP/POP3 connections AND provides SMTP authentication for Exim.

| Component | Path |
| :--- | :--- |
| **Main Config** | `/etc/dovecot/dovecot.conf` |
| **Config Includes** | `/etc/dovecot/conf.d/` |
| **Auth Config** | `/etc/dovecot/conf.d/10-auth.conf` |
| **Mail Location** | `/etc/dovecot/conf.d/10-mail.conf` |
| **SSL Config** | `/etc/dovecot/conf.d/10-ssl.conf` |
| **Main Log** | `/var/log/dovecot.log` |
| **Sockets** | `/var/run/dovecot/` |
| **User Mailboxes** | `/home/[USER]/mail/[DOMAIN]/[MAILBOX]/` |

## 2. Service Management
```bash
# Check status
sudo -n systemctl status dovecot

# Restart (safe — no syntax pre-check needed for Dovecot)
sudo -n systemctl restart dovecot

# Show active configuration
sudo -n doveconf -n
```

## 3. Common Issues

### A. "Authentication Failed" (IMAP/SMTP login fails)
This is the #1 Dovecot issue. The user can't log in to their email client.

1.  **Check Dovecot Log (FIRST STEP):**
    ```bash
    sudo -n grep "auth-worker" /var/log/dovecot.log | tail -n 20
    ```
    *Look for:* `auth failed`, `password mismatch`, `unknown user`.

2.  **Verify Credentials in HestiaCP:**
    ```bash
    # Check if the mail account exists
    sudo -n /usr/local/hestia/bin/v-list-mail-account-ssl USER DOMAIN ACCOUNT
    ```

3.  **Reset Password (If needed):**
    ```bash
    sudo -n /usr/local/hestia/bin/v-change-mail-account-password USER DOMAIN ACCOUNT NEWPASSWORD
    ```

4.  **Check if Dovecot is actually authenticating Exim (SMTP):**
    If Exim cannot authenticate users, outbound SMTP fails.
    ```bash
    sudo -n grep "dovecot_login\|dovecot_plain" /var/log/exim4/mainlog | tail -n 10
    ```

### B. "Connection Refused" on port 993/143
1.  **Check if Dovecot is listening:**
    ```bash
    sudo -n ss -tlnp | grep -E "993|143|995|110"
    ```
    *Expected:* Port 993 (IMAPS), 143 (IMAP), 995 (POP3S), 110 (POP3).

2.  **Check if Fail2Ban banned the user's IP:**
    ```bash
    sudo -n fail2ban-client status dovecot-iptables 2>/dev/null || echo "No Dovecot jail found"
    ```

3.  **Check Firewall:**
    ```bash
    sudo -n /usr/local/hestia/bin/v-list-firewall-ban json | grep "USER_IP"
    ```

### C. "Mailbox is Full" / Quota Exceeded
1.  **Check Current Usage:**
    ```bash
    sudo -n /usr/local/hestia/bin/v-list-mail-account USER DOMAIN ACCOUNT
    ```

2.  **Check Disk Usage Directly:**
    ```bash
    sudo -n du -sh /home/USER/mail/DOMAIN/ACCOUNT/
    ```

3.  **Increase Quota (if needed):**
    ```bash
    # Syntax: v-change-mail-account-quota USER DOMAIN ACCOUNT QUOTA_MB
    sudo -n /usr/local/hestia/bin/v-change-mail-account-quota USER DOMAIN ACCOUNT 1024
    ```

### D. "SSL Certificate Error" in Email Client
Users see "Certificate mismatch" or "Untrusted certificate" when connecting.

1.  **Check Mail Domain SSL:**
    ```bash
    sudo -n openssl x509 -enddate -noout -in /home/USER/conf/mail/DOMAIN/ssl/DOMAIN.crt
    ```

2.  **Renew/Apply Mail SSL:**
    ```bash
    sudo -n /usr/local/hestia/bin/v-add-mail-domain-ssl USER DOMAIN
    ```

3.  **Verify Dovecot is using the right cert:**
    ```bash
    sudo -n doveconf -n | grep ssl_cert
    ```

## 4. Advanced Diagnostics

### A. Connection Debugging
To see exactly what happens during an IMAP login:
```bash
# Test IMAP login manually
sudo -n openssl s_client -connect localhost:993 -quiet 2>/dev/null <<< "a1 LOGIN user@domain.com password"
```

### B. Process Issues
If Dovecot is eating too much RAM or CPU:
```bash
# Count Dovecot processes
sudo -n pgrep -c dovecot

# Check what it's doing
sudo -n doveadm who
```

### C. Mailbox Repair
If a user's mailbox is corrupted (errors in log about index files):
```bash
# Force reindex
sudo -n doveadm force-resync -u user@domain.com '*'
```

## 5. Key Relationship: Dovecot ↔ Exim
**CRITICAL:** If Dovecot is down, Exim's SMTP authentication also breaks (because Exim uses `dovecot_login`/`dovecot_plain` authenticators).
*   **Symptom:** Users can receive email but cannot SEND via SMTP.
*   **Diagnosis:** Check `/var/log/exim4/mainlog` for `authenticator failed`.
*   **Fix:** Restart Dovecot: `sudo -n systemctl restart dovecot`.
