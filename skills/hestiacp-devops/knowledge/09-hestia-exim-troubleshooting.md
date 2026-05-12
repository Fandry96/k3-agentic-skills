# Exim4 Troubleshooting Guide for HestiaCP

## 1. Quick Diagnostics
**Service Status:**
```bash
systemctl status exim4
```

**Queue Status:**
```bash
exim -bpc  # Count
exim -bp   # List details
```

**Log Analysis (The Source of Truth):**
*   **Received Emails:** `sudo -n grep "<=" /var/log/exim4/mainlog` (Email arrived at the server)
*   **Delivered Emails:** `sudo -n grep "=>" /var/log/exim4/mainlog` (Normal delivery, either local or external)
*   **Additional Address:** `sudo -n grep "->" /var/log/exim4/mainlog` (Forwarded or aliased delivery)
*   **Failed Emails:** `sudo -n grep "\*\*" /var/log/exim4/mainlog` (Delivery permanently failed/bounced)
*   **Deferred Emails:** `sudo -n grep "==" /var/log/exim4/mainlog` (Delivery temporarily delayed/in queue)
*   **Completed:** `sudo -n grep "Completed" /var/log/exim4/mainlog` (Processing for this message ID is finished)
*   **Authenticated Senders:** `sudo -n grep "A=dovecot_login" /var/log/exim4/mainlog` or `A=dovecot_plain` (Crucial to verify if an email was sent via SMTP auth by the user).

**CRITICAL RULE FOR LOG ANALYSIS:** Never assume `0 =>` means 0 emails were sent. The emails might have failed (`**`) or been deferred (`==`). Always check the full message ID lifecycle.

**Specific Address Search:** `sudo -n exigrep "user@domain.com" /var/log/exim4/mainlog` (exigrep is powerful because it groups the entire transaction by message ID).

**Domain Ownership Lookup:**
To find which HestiaCP user owns a domain (and thus where its config lives):
```bash
/usr/local/hestia/bin/v-search-domain-owner example.com
# Output: username
```

## 2. Historical Search & Rotated Logs (CRITICAL)
Debian rotates Exim logs daily. `mainlog` is today, `mainlog.1` is usually yesterday, `mainlog.2.gz` is older.
**NEVER ASSUME THE DATE BASED ON THE FILENAME NUMBER.**
1.  **Search everywhere:** To find an email from the past, always use `zgrep` to include compressed files:
    ```bash
    sudo -n zgrep "user@domain.com" /var/log/exim4/mainlog*
    ```
2.  **Summarize first:** If asking for a whole day, **DO NOT DUMP THE WHOLE LOG**. Count it or process it in chunks:
    ```bash
    # Count how many emails were sent/received across all files
    sudo -n zgrep -c "olgafreitas" /var/log/exim4/mainlog*
    ```
3.  **Filter by exact date:**
    ```bash
    sudo -n zgrep "^2026-03-15" /var/log/exim4/mainlog.1
    ```

## 3. Common Issues
### "Unroutable address"
*   Check if the domain exists in HestiaCP: `v-list-mail-domains [USER]`
*   Check DNS: `dig +short MX domain.com`

### "Connection refused"
*   Check if Exim is listening: `sudo -n netstat -plnt | grep :25`
*   Check Firewall: `v-list-firewall`

## 4. Advanced Diagnostics (Rejections & Blocks)

### Why was an email rejected?
Check the `rejectlog` for detailed reasons (SPF, DNSBL, Relay denied):
```bash
sudo -n grep "user@domain.com" /var/log/exim4/rejectlog
```

### Common Rejection Codes
*   **550 Unrouteable address:** The destination domain is not in HestiaCP or DNS is failing.
*   **550 Relay not permitted:** You are trying to send email *through* this server without authentication.
*   **550 Administrative prohibition:** Blocked by a custom rule or DNSBL.

### Check if IP is Blocked (DNSBL/Blacklist)
If you see "JunkMail rejected" or "SpamAssassin" blocks:
```bash
sudo -n grep "rejected after DATA" /var/log/exim4/mainlog | grep "user@domain.com"
```

### Trace a Conversation (SMTP Debug)
To see exactly what happened during the SMTP handshake:
```bash
sudo -n exigrep "user@domain.com" /var/log/exim4/mainlog
```

## 5. Queue Management (Frozen/Stuck Emails)
Sometimes emails get stuck. Here is how to manage them.

**List Frozen Messages:**
```bash
sudo -n exim -bpr | grep frozen
```

**Force Delivery (Try to send now):**
```bash
sudo -n exim -M [MESSAGE_ID]
# Example: sudo -n exim -M 1xQyZz-000000-00
```

**View Message Headers (Who sent it?):**
```bash
sudo -n exim -Mvh [MESSAGE_ID]
```

**View Message Body (What is inside?):**
```bash
sudo -n exim -Mvb [MESSAGE_ID]
```
*(CRITICAL: NEVER invent or hallucinate the body of an email. If you cannot read it with this command, state that it is unavailable. Do NOT create fake marketing emails or responses.)*

**View Delivery Log (Why is it stuck?):**
```bash
sudo -n exim -Mvl [MESSAGE_ID]
```

**Remove/Delete a Message:**
```bash
sudo -n exim -Mrm [MESSAGE_ID]
```

**Remove ALL Frozen Messages (Cleanup):**
```bash
sudo -n exiqgrep -z -i | xargs sudo -n exim -Mrm
```

## 6. Spam & Security Analysis
**Find Top Senders (Potential Spammers):**
```bash
sudo -n exim -bp | awk '{print $4}' | sort | uniq -c | sort -nr | head
```

**Check for Compromised Scripts (PHP Mail):**
Look for emails sent by `www-data` or the user ID, not an SMTP login:
```bash
sudo -n grep "U=www-data" /var/log/exim4/mainlog | head
```

