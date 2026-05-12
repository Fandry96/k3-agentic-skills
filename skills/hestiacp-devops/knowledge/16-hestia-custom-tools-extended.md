# HestiaCP Custom Tools — Extended Reference

This document covers custom tools from `hestiacp-useful-tools` that are deployed alongside HestiaCP but are NOT yet included in `01-hestia-system-paths.md` §9. These tools should be registered with `v-log-action` and installed via symlink to `/usr/local/hestia/bin/`.

## v-fix-web-permissions

Resets file ownership and permissions to HestiaCP defaults for all or specific domains. CMS-aware: detects WordPress, Laravel, Drupal, Joomla, Magento, PrestaShop, OpenCart, Symfony, and generic PHP.

| Component | Path | Description |
| :--- | :--- | :--- |
| **Script** | `/usr/local/hestia/bin/v-fix-web-permissions` | Symlink to repo script |
| **Source** | `/root/hestiacp-useful-tools/scripts/fix-web-permissions/v-fix-web-permissions` | Repo source |
| **Log Dir** | `/var/log/hestia/fix-permissions/` | Change logs per execution |
| **Sentinel** | `/home/[USER]/web/[DOMAIN]/public_html/.no-fix-permissions` | Skip domain (custom perms) |

### Usage

```bash
v-fix-web-permissions USER DOMAIN         # Fix a single domain
v-fix-web-permissions USER                # Fix all domains for a user
v-fix-web-permissions --all               # Fix all users + domains
v-fix-web-permissions --all --audit       # Audit only (no changes)
v-fix-web-permissions --all --dry         # Dry-run (preview changes)
v-fix-web-permissions --all --email       # Run and email report to admin
v-fix-web-permissions --all --filter-wordpress  # Only fix WordPress sites
v-fix-web-permissions admin example.com --drupal # Force Drupal CMS mode
```

### CMS-Specific Behavior

| CMS | Config File Perm | Writable Dirs |
| :--- | :--- | :--- |
| WordPress | `wp-config.php` → 640 | `wp-content/uploads`, `cache`, `w3tc-config`, `upgrade`, `wc-logs` |
| Laravel | `.env` → 640, `artisan` → 755 | `storage/`, `bootstrap/cache/` |
| Drupal | `settings.php` → 444, `sites/default` → 555 | `sites/default/files`, `private` |
| Joomla | `configuration.php` → 640 | `cache`, `tmp`, `logs`, `images`, `media` |
| Magento | `app/etc/env.php` → 640, `bin/magento` → 755 | `var/`, `generated/`, `pub/media/` |
| PrestaShop | `config/settings.inc.php` → 640 | `cache`, `log`, `img`, `upload`, `download` |
| OpenCart | `config.php` → 640, `admin/config.php` → 640 | `system/storage`, `image/cache` |

### Default Permissions Applied

- Directories: `755`
- Files: `644`
- Ownership: `[USER]:[USER]` (matches FPM pool user)

### Built-in Security Scan

Each domain run also checks for:
- `.git` directory in public_html
- `.env` in public_html
- `install/`, `setup/` directories
- `phpinfo.php`, `test.php`, `debug.php`
- `composer.json` / `composer.lock` in public_html

---

## v-security-audit

Comprehensive security auditing tool. Performs read-only scans across 4 layers: system, backend (file-level), frontend (HTTP), and pentest (offensive). Produces scored reports with actionable findings.

| Component | Path | Description |
| :--- | :--- | :--- |
| **Script** | `/usr/local/hestia/bin/v-security-audit` | Symlink to repo script |
| **Source** | `/root/hestiacp-useful-tools/scripts/security-audit/v-security-audit` | Repo source |
| **Lib Dir** | `/root/hestiacp-useful-tools/scripts/security-audit/lib/` | Modular check libraries |
| **Log Dir** | `/var/log/hestia/security-audit/` | Execution logs |
| **YARA Rules** | `lib/backend/webshells.yar` (bundled) or `mktemp` fallback | Malware detection rules |

### Usage

```bash
v-security-audit --system                           # OS & services only
v-security-audit --backend                          # All users, all domains
v-security-audit --backend johndoe                  # All domains for one user
v-security-audit --backend johndoe example.com      # Single domain
v-security-audit --frontend https://example.com     # External scan
v-security-audit --pentest https://example.com      # Offensive self-attack
v-security-audit --all                              # Full audit (all 4 layers)
v-security-audit --all --json --quiet               # JSON output, only failures
v-security-audit --all --html                       # HTML dashboard report
v-security-audit --all --email                      # Email report to admin
```

### Module Architecture

| Layer | Dir | Checks |
| :--- | :--- | :--- |
| System | `lib/system/` | OS, SSH, firewall, Fail2Ban, HestiaCP panel, DB, mail, kernel hardening, PHP-FPM, Nginx, user accounts |
| Backend | `lib/backend/` | File exposure, malware (YARA/ClamAV), CMS hardening (WP/Laravel/Drupal/Joomla/Magento/PrestaShop/OpenCart/Moodle/generic), permissions |
| Frontend | `lib/frontend/` | SSL/TLS, security headers, cookies, redirects, info disclosure, security.txt, SRI |
| Pentest | `lib/pentest/` | SQLi, XSS, LFI, RCE, XXE, auth brute-force, HTTP methods, SSRF, rate limiting, WAF evasion, DNS attacks, cache poisoning, exposed services |

### Scoring

| Severity | Points | Grade Range |
| :--- | :--- | :--- |
| CRITICAL | -10 | A: 90-100 |
| FAIL | -5 | B: 75-89 |
| WARN | -2 | C: 60-74 |
| INFO | 0 | D: 40-59 |
| PASS | 0 | F: 0-39 |

### Optional Dependencies

| Tool | Purpose | Install |
| :--- | :--- | :--- |
| `dig` | DNS checks (SPF, DKIM, Zone transfers) | `apt install dnsutils` |
| `jq` | JSON formatting | `apt install jq` |
| `yara` | Advanced Web-Shell heuristics | `apt install yara` |
| `clamav` | Malware signatures | `apt install clamav` |
| `wp-cli` | WordPress user audit | Manual install |

### Key Paths Referenced

All paths align with `01-hestia-system-paths.md`:
- `/usr/local/hestia/conf/hestia.conf` — panel config
- `/usr/local/hestia/data/users/` — user database
- `/usr/local/hestia/data/firewall/` — firewall rules
- `/usr/local/hestia/data/keys/` — API access keys
- `/usr/local/hestia/data/sessions/` — panel sessions
- `/usr/local/hestia/ssl/certificate.crt` — panel SSL cert
- `/etc/php/[VER]/fpm/pool.d/` — PHP-FPM pools
- `/etc/nginx/nginx.conf` — Nginx global config
- `/etc/ssh/sshd_config` — SSH configuration
- `/home/[USER]/web/[DOMAIN]/public_html/` — document roots
- `/home/[USER]/conf/web/` — per-user web configs
