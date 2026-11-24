> **Uso defensivo:** ejecÃºtelo solo en SU computadora y en SUS repositorios. El kit solo lee: no instala, no actualiza, no corrige, no revisa otras computadoras ni envÃ­a nada: solo consulta los servidores de actualizaciÃ³n de su propio sistema.

# corrija-antes â€” el reloj de quien defiende

[![Corrija antes](guia/assets/banner-es.jpg)](https://linnoff88-dev.github.io/

**ðŸ‡§ðŸ‡· [PortuguÃªs](README.md) Â· ðŸ‡ºðŸ‡¸ [English](README.en.md) Â· ðŸ‡ªðŸ‡¸ [EspaÃ±ol](README.es.md)**

## QuÃ© es

En julio de 2026, las IA abiertas estaban de 4 a 7 meses detrÃ¡s de las cerradas en ataques. En octubre, en una prueba de intrusiÃ³n en la red de una empresa, esa distancia llegÃ³ a cero: quienes defienden perdieron la ventaja de tiempo. corrija-antes es un kit gratuito que hace, en tu computadora, las tres cosas que todavÃ­a funcionan: **actualizar mÃ¡s rÃ¡pido, vigilar la red y encontrar tus brechas antes que los demÃ¡s**. Un script de diagnÃ³stico muestra quÃ© corregir AHORA y quÃ© puede esperar hasta la semana, y un prompt listo le pide a la IA que revise tu cÃ³digo. Sirve para quienes tienen una computadora, un servidor o una aplicaciÃ³n en lÃ­nea y no trabajan con seguridad todos los dÃ­as. Necesitas Python 3 (Linux o macOS).

## ðŸ“– GuÃ­a de uso

GuÃ­a completa, con el video: **https://linnoff88-dev.github.io/

Video: [China liberÃ³ gratis la IA hacker que OpenAI bloqueÃ³](https://www.youtube.com/watch?v=1WFT-VgGuPM) Â· [versiÃ³n vertical](https://youtube.com/shorts/-R65CemeRvc)

## Prueba en 1 minuto

```bash
git clone https://github.com/linnoff88-dev/corrija-antes.git
cd corrija-antes
python3 relogio.py --repo ~/seu-projeto --saida relatorio
```

VerÃ¡s una lista en pantalla y un `relatorio/relatorio.md`. Cada elemento tiene una prioridad:

| Prioridad | QuÃ© significa |
|---|---|
| **AGORA** (AHORA) | correcciÃ³n de seguridad pendiente, base de datos/Redis/Ollama/pantalla remota abierta a la red, SSH con contraseÃ±a, secreto en el cÃ³digo |
| **SEMANA** (esta semana) | actualizaciÃ³n comÃºn, puerto abierto que debes revisar, firewall desactivado, imagen Docker de hace mÃ¡s de 4 meses, `.env` fuera del `.gitignore`, clave con cara de ejemplo, dependencias estancadas |
| **SEM TESTE** (SIN PRUEBA) | no se pudo verificar (faltan permisos o herramientas): no significa que sea seguro |
| **OK** (BIEN) | verificado y al dÃ­a |

Consulta un [informe de ejemplo](exemplos/relatorio-exemplo.md) (servidor ficticio de una tienda, con datos inventados).

## Los 3 bloques

1. **Actualiza**: paquetes del sistema con correcciones de seguridad (apt, dnf, Homebrew, macOS), snaps, paquetes globales de npm, imÃ¡genes Docker en uso de hace mÃ¡s de 4 meses, reinicio pendiente y **cuÃ¡ntos dÃ­as** han pasado desde la Ãºltima actualizaciÃ³n.
2. **Vigila la red**: quÃ© estÃ¡ escuchando solo en la computadora, solo en la red interna/VPN o abierto a cualquier red; puertos crÃ­ticos (bases de datos, Redis, Ollama, VNC/RDP, API de Docker); firewall; SSH con contraseÃ±a o como root; puertos que Docker publica **por encima de ufw**.
3. **Tus brechas** (`--repo`): `.env` dentro de git, `.gitignore` sin `.env`, claves y tokens escritos en el cÃ³digo (el valor aparece oculto), dependencias sin cambios desde hace mÃ¡s de 4 meses y el recordatorio de la revisiÃ³n con IA.

   Formatos reconocidos: AWS, OpenAI/Anthropic, DeepSeek, OpenRouter, Stripe, GitHub, Slack (token y webhook), Google, Telegram, Mercado Pago, Groq, Hugging Face, GitLab, SendGrid, npm, Resend, service_role de Supabase, clave privada, contraseÃ±a en una URL de base de datos y contraseÃ±as/claves de `wp-config.php`. Solo lee los archivos actuales, no el historial de git; una contraseÃ±a genÃ©rica (`password=â€¦`) o claves de otros servicios pasan sin aviso.

## Opciones

```bash
python3 relogio.py                              # solo la computadora
python3 relogio.py --repo ~/app --repo ~/api    # computadora + dos repositorios
python3 relogio.py --blocos vigie               # solo un bloque: atualize, vigie, codigo
python3 relogio.py --saida relatorio            # guarda relatorio.md y relatorio.json
python3 relogio.py --json                       # resultado en JSON en pantalla
python3 relogio.py --mostrar-ips                # no oculta IP, usuario ni nombre de la computadora
```

CÃ³digo de salida: `0` = nada para AHORA Â· `1` = hay elementos AHORA Â· `2` = error de uso. Sin `sudo`, algunos elementos aparecen como SIN PRUEBA (por ejemplo, las reglas del firewall); el script indica quÃ© comando ejecutar para verificarlos.

## El proceso, de principio a fin

1. ðŸ§  **TÃº** clonas el kit y ejecutas `python3 relogio.py --repo <seu projeto> --saida relatorio`.
2. âš™ï¸ **Script** lista los elementos AGORA / SEMANA / SEM TESTE / OK y guarda el informe (solo lee).
3. ðŸ§  **TÃº** haces una copia de seguridad y revisas el estado del sistema antes de cambiar nada.
4. ðŸ§  **TÃº** resuelves los elementos AGORA, uno a la vez ([ROTINA.md](ROTINA.md) (en portuguÃ©s)).
5. ðŸ¤– **IA** (Claude Code, Codex o modelo local) revisa tu cÃ³digo con el [prompt de revisiÃ³n](prompts/revisao-com-ia.md) (en portuguÃ©s).
6. âš™ï¸ **Script** vuelve a ejecutarse para confirmar; opcional: todos los lunes mediante cron.

## Para profundizar (kits ARCKHÉ de auditorÃ­a y diagnÃ³stico)

| Kit | Para quÃ© sirve |
|---|---|
| [auditoria-seguranca](https://linnoff88-dev.github.io/ | comprueba si tus herramientas aÃºn confÃ­an en certificados filtrados y si PHP tiene la vulnerabilidad PHP2Shell |
| [blinda-site](https://linnoff88-dev.github.io/ | diagnÃ³stico interno del sitio: plan, copia de seguridad, simulaciÃ³n y niveles de riesgo |
| [invada-seu-proprio-app](https://linnoff88-dev.github.io/ | las 5 brechas mÃ¡s comunes de una aplicaciÃ³n hecha con IA, probadas en tu copia de prueba |
| [agente-blindado](https://linnoff88-dev.github.io/ | 5 bloqueos contra la inyecciÃ³n de prompts y 10 ataques para probar tu agente |
| [caixa-do-agente](https://linnoff88-dev.github.io/ | evaluaciÃ³n de tu harness de agente y una caja Docker descartable, sin red ni `.env` |
| [ia-sem-censura-defensiva](https://linnoff88-dev.github.io/ | modelo abierto sin restricciones, usado solo para defensa y ejecutado en tu computadora |
| [protegendo-seus-repos](https://linnoff88-dev.github.io/ | copia de seguridad en 3 capas de tus repositorios contra bloqueos o intrusiones |

## Pruebas

```bash
python3 testes/run.py        # 82 pruebas con datos inventados
python3 testes/gera_exemplo.py   # vuelve a generar el informe de ejemplo
```

Python 3, sin dependencias. Contenido original. Licencia [MIT](LICENSE). MÃ¡s en [ARCKHÉ AI](https://ARCKHÉ AI).