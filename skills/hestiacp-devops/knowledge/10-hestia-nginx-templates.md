# HestiaCP Web Templates Guide (Nginx & Apache)

## 1. Verified System Paths (Consult `01-hestia-system-paths.md`)
**CRITICAL:** Templates are the ONLY way to make permanent config changes.

| Template Type | Directory |
| :--- | :--- |
| **Nginx (Proxy)** | `/usr/local/hestia/data/templates/web/nginx/` |
| **Apache2 (Backend)** | `/usr/local/hestia/data/templates/web/apache2/php-fpm/` |
| **PHP-FPM (Pools)** | `/usr/local/hestia/data/templates/web/php-fpm/` |

## 2. Core Principle
**NEVER edit generated configuration files** (like `/home/user/conf/web/...` or `/etc/nginx/conf.d/...`) directly. HestiaCP overwrites these files whenever a domain is rebuilt or the panel is updated.
**ALWAYS use Templates.**

## 3. How to Create a Custom Template
1.  **Copy an existing template:**
    ```bash
    cd /usr/local/hestia/data/templates/web/nginx/
    cp default.tpl my-custom.tpl
    cp default.stpl my-custom.stpl
    ```
    *Note: `.stpl` is for SSL (HTTPS). You must create both.*

2.  **Edit the new template:**
    ```bash
    nano my-custom.stpl
    ```
    *Use placeholders like `%ip%`, `%domain%`, `%docroot%`.*

3.  **Apply the template to a domain:**
    ```bash
    sudo -n /usr/local/hestia/bin/v-change-web-domain-proxy-tpl USER DOMAIN my-custom
    ```
    *(For Apache backend, use `v-change-web-domain-tpl`)*

## 4. Common Variables
- `%ip%`: Server IP
- `%domain%`: Domain name
- `%docroot%`: `/home/user/web/domain.com/public_html`
- `%backend_lsnr%`: Backend listener (e.g., `127.0.0.1:8080`)

## 5. Troubleshooting
- **Rebuild Domain:** If changes don't appear, force a rebuild:
  ```bash
  sudo -n /usr/local/hestia/bin/v-rebuild-web-domain USER DOMAIN
  ```
- **Test Nginx Config:**
  ```bash
  sudo -n nginx -t
  ```

