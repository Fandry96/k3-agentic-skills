# HestiaCP SSL Certificate Management

## 1. Verified System Paths (Consult `01-hestia-system-paths.md`)
**CRITICAL:** HestiaCP stores certificates in specific user locations, NOT in `/etc/letsencrypt/live`.

| Component | Path |
| :--- | :--- |
| **Web Certs** | `/home/[USER]/conf/web/[DOMAIN]/ssl/[DOMAIN].crt` |
| **Web Keys** | `/home/[USER]/conf/web/[DOMAIN]/ssl/[DOMAIN].key` |
| **Mail Certs** | `/home/[USER]/conf/mail/[DOMAIN]/ssl/[DOMAIN].crt` |
| **Panel Cert** | `/usr/local/hestia/ssl/certificate.crt` |
| **LE Logs** | `/var/log/hestia/LE-[USER]-[DOMAIN].log` |

## 2. Checking SSL Status (The Fast Way)
Don't use `openssl s_client` against localhost (it often fails due to SNI/hosts). Check the files directly.

### A. Check All Web Certs Expiration
```bash
sudo -n find /home/*/conf/web -name "*.crt" -exec openssl x509 -enddate -noout -in {} \; -print | paste -d " " - -
```

### B. Check Panel SSL
```bash
sudo -n openssl x509 -enddate -noout -in /usr/local/hestia/ssl/certificate.crt
```

## 3. Common Tasks

### A. Force Renewal (Let's Encrypt)
If a cert is expired or expiring soon:
```bash
# Syntax: v-update-letsencrypt-ssl USER DOMAIN
sudo -n /usr/local/hestia/bin/v-update-letsencrypt-ssl admin example.com
```

### B. Enable SSL for a New Domain
```bash
# Syntax: v-add-letsencrypt-domain USER DOMAIN [ALIASES]
sudo -n /usr/local/hestia/bin/v-add-letsencrypt-domain admin example.com www.example.com
```

### C. Apply SSL to HestiaCP Panel
To secure port 8083 with a valid domain cert:
```bash
sudo -n /usr/local/hestia/bin/v-change-sys-hestia-ssl example.com
```

### D. Apply SSL to Mail Domain
Required for secure SMTP/IMAP:
```bash
sudo -n /usr/local/hestia/bin/v-add-mail-domain-ssl admin example.com
```

## 4. Troubleshooting
**Symptoms:** "Verify error:Invalid response", "Timeout".

1.  **Check DNS:** Ensure domain points to server IP.
2.  **Check Logs:**
    ```bash
    sudo -n tail -n 50 /var/log/hestia/LE-admin-example.com.log
    ```
3.  **Test Connection:**
    Ensure Let's Encrypt can reach `.well-known/acme-challenge/`.
    *   Check if Nginx isn't blocking it in `/etc/nginx/conf.d/`.

