---
name: hestiacp-devops
description: "Autonomous HestiaCP server management with AI agents. Two-brain Orchestrator+Sentinel architecture for VPS monitoring, troubleshooting, security hardening, PHP-FPM tuning, Exim mail forensics, and post-compromise detection. Use when: HestiaCP, VPS, server monitoring, DevOps agent, Linux admin, Nginx/Apache, PHP-FPM, Exim, Fail2Ban, ClamAV, SSL, backup."
---

# HestiaCP DevOps AI Skill

> **Source:** `webxtekstudio/hestiacp-useful-tools` (GitHub, MIT License)
> **Architecture:** Two-brain Orchestrator + Sentinel pattern
> **Platform:** HestiaCP on Debian 12 (Bookworm)
> **Blueprint:** See `hestiacp_two_brain_blueprint.md` in session artifacts

## When to Use

- Server health monitoring and automated reporting
- HestiaCP CLI operations (`v-*` commands)
- PHP-FPM pool tuning and troubleshooting (502/504 errors)
- Exim4 mail queue forensics and spam mitigation
- Fail2Ban management and attack response
- SSL certificate management (Let's Encrypt)
- Post-compromise detection (rogue ports, temp executables, webshells)
- Backup verification and disaster recovery
- Nginx/Apache reverse proxy debugging
- CMS permission hardening (WordPress, Laravel, Drupal, Joomla, Magento)

## Architecture: Two-Brain Model

### Brain 1: Sentinel (Passive Monitor)
- **File:** `prompts/System-Monitor-Prompt.md`
- **Input:** CRON-injected telemetry (RAM, CPU, Disk, Services, Logs)
- **Output:** Structured health report (HEALTHY ✅ / WARNING ⚠️ / CRITICAL 🔴)
- **Tool:** `run_ssh_command` (Round 3 deep dives only)
- **Key Innovation:** Post-compromise detection, attack-is-root-cause principle

### Brain 2: Orchestrator (Active DevOps)
- **File:** `prompts/DevOps-Agent-Prompt.md`
- **Input:** User request or Sentinel alert trigger
- **Output:** Diagnosis + remediation + verification report
- **Tools:** `run_ssh_command` + `ask_knowledge_expert` (RAG)
- **Constraint:** Max 10 ReAct steps

## Decision Heuristics (Mandatory)

```
1. LOOK BEFORE LEAP     — cp config.conf config.conf.bak
2. LEAST DESTRUCTIVE    — nginx -t BEFORE systemctl restart
3. SILENT EXECUTION     — Act safely, report async (no permission prompts in automation)
4. FALSIFIABILITY TEST  — After "fixing", run the command that PROVES it's fixed
```

## Noise Filter (False Positive Suppression)

Ignore these — they are NORMAL in HestiaCP:
- `cloud-init`, `cloud-config`, `cloud-final` service failures
- Apache on port 8080 (backend behind Nginx — this IS the architecture)
- SSH brute-force in auth logs (Fail2Ban handles it)
- High memory if mostly buffers/cache
- Zombie count ≤ 5
- Load spikes during `v-backup-users`
- Transient PHP-FPM CPU spikes during backup windows

## Severity Classification

| Level | Trigger |
|---|---|
| ✅ HEALTHY | Zero thresholds breached, or only marginal |
| ⚠️ WARNING | Clear threshold breach with operational concern |
| 🔴 CRITICAL | Service down, disk >90%, backup FAILED, active attack, OOM kills, compromise indicators |

**Attack Principle:** When PHP-FPM CPU is high AND attack vectors are present, the ROOT CAUSE is the attack — not PHP-FPM. Report as attack, not "busy workload."

## Critical Thresholds

| Resource | Warning | Critical |
|---|---|---|
| Disk (`/` or `/home`) | >80% | >90% |
| Load (1min) | > nproc | > nproc × 2 |
| RAM (excl. cache) | >85% | — |
| Swap | >1GB | >2GB (OOM risk) |
| Mail Queue (Exim) | >10 messages | >50 messages |
| Backup Age | >8 days | STATUS=FAILED |
| SSL Expiry | <14 days | <7 days |

## Post-Compromise Detection (6 Vectors)

| Vector | Check | Critical |
|---|---|---|
| Rogue Ports | `ss -tlnp` vs expected | 4444, 5555, 6666, 8888 → 🔴 |
| Temp Executables | `/tmp`, `/var/tmp`, `/dev/shm` | ANY executable → 🔴 |
| User Audit | UID ≥ 1000 with `/bin/bash` | Unknown user → 🔴 |
| Recent PHP Mods | Files modified <6hrs | `shell.php`, `c99.php` → 🔴 |
| Outbound C2 | `ss -tnp state established` | IRC 6667, crypto 3333 → 🔴 |
| Suspicious Cron | `curl`, `wget`, `base64`, `/tmp/` | 🔴 possible backdoor |

## Service Name Gotchas

| Service | Correct | WRONG |
|---|---|---|
| Mail | `exim4` | ~~exim~~ |
| Database | `mariadb` | ~~mysql~~ |
| PHP | `php8.2-fpm` | ~~php-fpm~~ |
| DB CLI | `mariadb` | ~~mysql~~ |

## PHP-FPM Tuning Formula

```
Max Total Workers = (Total RAM - 2GB) / 60MB

Low Traffic:    2-5 workers
Medium Traffic: 10-20 workers
High Traffic:   30-50 workers
```

## Exim Log Decoder

```
<=  Email arrived at server
=>  Normal delivery (local or external)
->  Forwarded or aliased delivery
**  Delivery permanently FAILED (bounced)
==  Delivery temporarily DELAYED (queued)
```

**CRITICAL:** `mainlog` does NOT store email subjects. To get subjects, grep the physical Maildir:
```
/home/<user>/mail/<domain>/<account>/new/  (unread)
/home/<user>/mail/<domain>/<account>/cur/  (read)
```

## False Path Map (Never Use These)

| Generic Path | HestiaCP Reality |
|---|---|
| `/etc/letsencrypt/live` | `/home/[USER]/conf/web/[DOMAIN]/ssl/` |
| `/etc/nginx/sites-enabled` | `/etc/nginx/conf.d/domains/` |
| `/var/www/html` | `/home/[USER]/web/[DOMAIN]/public_html/` |

## Knowledge Base (16 files in `knowledge/`)

| # | File | Size | Domain |
|---|---|---|---|
| 01 | `hestia-system-paths.md` | 11.5KB | Complete path map |
| 02 | `hestia-troubleshooting-logs.md` | 5.7KB | Diagnostic commands |
| 03 | `hestia-cron-guide.md` | 2.7KB | CRON management |
| 04 | `hestia-php-tuning.md` | 4.2KB | PHP-FPM optimization |
| 05 | `hestia-database-guide.md` | 2.6KB | MariaDB config |
| 06 | `hestia-fail2ban-guide.md` | 2.0KB | Jail management |
| 07 | `hestia-ssl-guide.md` | 2.2KB | SSL lifecycle |
| 08 | `hestia-clamav-guide.md` | 2.1KB | Antivirus config |
| 09 | `hestia-exim-troubleshooting.md` | 5.0KB | Mail queue forensics |
| 10 | `hestia-nginx-templates.md` | 1.8KB | Proxy templates |
| 11 | `hestia-backups.md` | 3.1KB | Backup/restore |
| 12 | `hestia-cli-reference.md` | 23.2KB | **400+ v-commands** |
| 13 | `hestia-common-issues.md` | 3.1KB | Decision trees |
| 14 | `hestia-dovecot-guide.md` | 4.4KB | IMAP/POP3 debug |
| 15 | `exim-forensics.md` | 2.8KB | Maildir forensics |
| 16 | `hestia-custom-tools-extended.md` | 6.3KB | v-fix-web-permissions, v-security-audit |

## Integration

- **Skill Router:** Category 4 (Deploy & Ops)
- **Related Skills:** `@gcp-cloud-run`, `@docker-expert`, `@security-auditor`, `@systematic-debugging`
- **MRL Index:** Rebuild `mrl_index.pkl` to include these 19 files for semantic search
