# Forense de Emails (Exim4 e Dovecot) no HestiaCP

Para responder a perguntas como "quantos emails recebeu", "quais foram os subjects", e "quem enviou", o Agente DEVE usar as seguintes regras rigorosas, pois as configurações padrão de Linux não se aplicam ao HestiaCP.

## 1. Onde os emails estão fisicamente guardados?
HestiaCP NÃO usa `/var/vmail/`. Todos os emails entregues estão organizados por utilizador do painel, domínio, e conta de correio, no seguinte caminho:
`/home/<Utilizador_Hestia>/mail/<Dominio>/<Conta>/`

Pastas principais da Maildir localizadas diretamente dentro da conta:
- `new/` (Emails acabados de chegar, ainda não lidos)
- `cur/` (Emails já processados/lidos pelo cliente)

**Exemplo:** Se o painel Hestia tem o utilizador `admin`, o domínio `koolfitness.pt` e a conta de email `geral`, o caminho é:
`/home/admin/mail/koolfitness.pt/geral/`

## 2. Ler "Subjects" e "From" (Remetentes)
O ficheiro `/var/log/exim4/mainlog` **NÃO GUARDA** os "Subjects" (assuntos) por defeito no HestiaCP. Nunca tentes encontrar Subjects no `mainlog`.
Também não deves usar o `exim -Mvh` para emails antigos porque o Exim apaga-os da *queue* (`/var/spool/exim4/`) assim que são entregues.

**A ÚNICA forma fidedigna** de ler quem enviou e o assunto de emails recentes é fazer `find` nas diretoria `new` e `cur` cruzando com um `grep`, pois o telemóvel/outlook do cliente pode já ter movido o ficheiro do `new` para o `cur`.

**Para extrair Subjects e Froms APENAS de HOJE (usando `find` com `-mtime -1` ou `-mmin -1440`):**
```bash
# Lembra-te: Os emails vão parar ao 'cur' muito rapidamente se o IMAP estiver ligado! Procura sempre nos dois!
sudo find /home/*/mail/koolfitness.pt/geral/new /home/*/mail/koolfitness.pt/geral/cur -type f -mmin -1440 -exec grep -H -i "^Subject:" {} + 2>/dev/null
sudo find /home/*/mail/koolfitness.pt/geral/new /home/*/mail/koolfitness.pt/geral/cur -type f -mmin -1440 -exec grep -H -i "^From:" {} + 2>/dev/null
```

## 3. Contar Emails Reais Recebidos Hoje
Para contar APENAS os emails que efetivamente entraram e foram entregues na caixa local hoje (para evitar contar tentativas falhadas ou bounces da queue principal):
1. Vai ao `mainlog`
2. Filtra pela data (ex: `2026-04-09`)
3. Filtra pelo símbolo de entrega local em caixa de correio `=> <conta>@<dominio>`

**Exemplo:**
```bash
sudo grep "^2026-04-09" /var/log/exim4/mainlog | grep "=> geral <geral@koolfitness.pt>" | wc -l
```

## 4. O que NUNCA deves fazer:
- NUNCA procurars em `/var/vmail/`.
- NUNCA deduzir subjects do `/var/log/exim4/mainlog`. Se o utilizador pedir Subjects, corre LOGO os comandos `grep` na `Maildir` física de `/home/`.
- NUNCA tentar adivinhar nomes de ficheiros de spool do exim que o comando `exim -Mvh` não consegue encontrar.
