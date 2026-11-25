> **Uso defensivo:** ejecêÂºtelo solo en SU computadora y en SUS repositorios. El kit solo lee: no instala, no actualiza, no corrige, no revisa otras computadoras ni envêÂ­a nada: solo consulta los servidores de actualizaciêÂ³n de su propio sistema.

# corrija-antes ê¢â¬â el reloj de quien defiende

[![Corrija antes](guia/assets/banner-es.jpg)](https://linnoff88-dev.github.io/

**ê°Å¸â¡Â§ê°Å¸â¡Â· [PortuguêÂªs](README.md) êÂ· ê°Å¸â¡Âºê°Å¸â¡Â¸ [English](README.en.md) êÂ· ê°Å¸â¡Âªê°Å¸â¡Â¸ [EspaêÂ±ol](README.es.md)**

## QuêÂ© es

En julio de 2026, las IA abiertas estaban de 4 a 7 meses detrêÂ¡s de las cerradas en ataques. En octubre, en una prueba de intrusiêÂ³n en la red de una empresa, esa distancia llegêÂ³ a cero: quienes defienden perdieron la ventaja de tiempo. corrija-antes es un kit gratuito que hace, en tu computadora, las tres cosas que todavêÂ­a funcionan: **actualizar mêÂ¡s rêÂ¡pido, vigilar la red y encontrar tus brechas antes que los demêÂ¡s**. Un script de diagnêÂ³stico muestra quêÂ© corregir AHORA y quêÂ© puede esperar hasta la semana, y un prompt listo le pide a la IA que revise tu cêÂ³digo. Sirve para quienes tienen una computadora, un servidor o una aplicaciêÂ³n en lêÂ­nea y no trabajan con seguridad todos los dêÂ­as. Necesitas Python 3 (Linux o macOS).

## ê°Å¸ââ GuêÂ­a de uso

GuêÂ­a completa, con el video: **https://linnoff88-dev.github.io/

Video: [China liberêÂ³ gratis la IA hacker que OpenAI bloqueêÂ³](https://www.youtube.com/watch?v=1WFT-VgGuPM) êÂ· [versiêÂ³n vertical](https://youtube.com/shorts/-R65CemeRvc)

## Prueba en 1 minuto

```bash
git clone https://github.com/linnoff88-dev/corrija-antes.git
cd corrija-antes
python3 relogio.py --repo ~/seu-projeto --saida relatorio
```

VerêÂ¡s una lista en pantalla y un `relatorio/relatorio.md`. Cada elemento tiene una prioridad:

| Prioridad | QuêÂ© significa |
|---|---|
| **AGORA** (AHORA) | correcciêÂ³n de seguridad pendiente, base de datos/Redis/Ollama/pantalla remota abierta a la red, SSH con contraseêÂ±a, secreto en el cêÂ³digo |
| **SEMANA** (esta semana) | actualizaciêÂ³n comêÂºn, puerto abierto que debes revisar, firewall desactivado, imagen Docker de hace mêÂ¡s de 4 meses, `.env` fuera del `.gitignore`, clave con cara de ejemplo, dependencias estancadas |
| **SEM TESTE** (SIN PRUEBA) | no se pudo verificar (faltan permisos o herramientas): no significa que sea seguro |
| **OK** (BIEN) | verificado y al dêÂ­a |

Consulta un [informe de ejemplo](exemplos/relatorio-exemplo.md) (servidor ficticio de una tienda, con datos inventados).

## Los 3 bloques

1. **Actualiza**: paquetes del sistema con correcciones de seguridad (apt, dnf, Homebrew, macOS), snaps, paquetes globales de npm, imêÂ¡genes Docker en uso de hace mêÂ¡s de 4 meses, reinicio pendiente y **cuêÂ¡ntos dêÂ­as** han pasado desde la êÂºltima actualizaciêÂ³n.
2. **Vigila la red**: quêÂ© estêÂ¡ escuchando solo en la computadora, solo en la red interna/VPN o abierto a cualquier red; puertos crêÂ­ticos (bases de datos, Redis, Ollama, VNC/RDP, API de Docker); firewall; SSH con contraseêÂ±a o como root; puertos que Docker publica **por encima de ufw**.
3. **Tus brechas** (`--repo`): `.env` dentro de git, `.gitignore` sin `.env`, claves y tokens escritos en el cêÂ³digo (el valor aparece oculto), dependencias sin cambios desde hace mêÂ¡s de 4 meses y el recordatorio de la revisiêÂ³n con IA.

   Formatos reconocidos: AWS, OpenAI/Anthropic, DeepSeek, OpenRouter, Stripe, GitHub, Slack (token y webhook), Google, Telegram, Mercado Pago, Groq, Hugging Face, GitLab, SendGrid, npm, Resend, service_role de Supabase, clave privada, contraseêÂ±a en una URL de base de datos y contraseêÂ±as/claves de `wp-config.php`. Solo lee los archivos actuales, no el historial de git; una contraseêÂ±a genêÂ©rica (`password=ê¢â¬Â¦`) o claves de otros servicios pasan sin aviso.

## Opciones

```bash
python3 relogio.py                              # solo la computadora
python3 relogio.py --repo ~/app --repo ~/api    # computadora + dos repositorios
python3 relogio.py --blocos vigie               # solo un bloque: atualize, vigie, codigo
python3 relogio.py --saida relatorio            # guarda relatorio.md y relatorio.json
python3 relogio.py --json                       # resultado en JSON en pantalla
python3 relogio.py --mostrar-ips                # no oculta IP, usuario ni nombre de la computadora
```

CêÂ³digo de salida: `0` = nada para AHORA êÂ· `1` = hay elementos AHORA êÂ· `2` = error de uso. Sin `sudo`, algunos elementos aparecen como SIN PRUEBA (por ejemplo, las reglas del firewall); el script indica quêÂ© comando ejecutar para verificarlos.

## El proceso, de principio a fin

1. ê°Å¸Â§Â  **TêÂº** clonas el kit y ejecutas `python3 relogio.py --repo <seu projeto> --saida relatorio`.
2. ê¢Å¡â¢ê¯Â¸Â **Script** lista los elementos AGORA / SEMANA / SEM TESTE / OK y guarda el informe (solo lee).
3. ê°Å¸Â§Â  **TêÂº** haces una copia de seguridad y revisas el estado del sistema antes de cambiar nada.
4. ê°Å¸Â§Â  **TêÂº** resuelves los elementos AGORA, uno a la vez ([ROTINA.md](ROTINA.md) (en portuguêÂ©s)).
5. ê°Å¸Â¤â **IA** (Claude Code, Codex o modelo local) revisa tu cêÂ³digo con el [prompt de revisiêÂ³n](prompts/revisao-com-ia.md) (en portuguêÂ©s).
6. ê¢Å¡â¢ê¯Â¸Â **Script** vuelve a ejecutarse para confirmar; opcional: todos los lunes mediante cron.

## Para profundizar (kits ARCKHê de auditorêÂ­a y diagnêÂ³stico)

| Kit | Para quêÂ© sirve |
|---|---|
| [auditoria-seguranca](https://linnoff88-dev.github.io/ | comprueba si tus herramientas aêÂºn confêÂ­an en certificados filtrados y si PHP tiene la vulnerabilidad PHP2Shell |
| [blinda-site](https://linnoff88-dev.github.io/ | diagnêÂ³stico interno del sitio: plan, copia de seguridad, simulaciêÂ³n y niveles de riesgo |
| [invada-seu-proprio-app](https://linnoff88-dev.github.io/ | las 5 brechas mêÂ¡s comunes de una aplicaciêÂ³n hecha con IA, probadas en tu copia de prueba |
| [agente-blindado](https://linnoff88-dev.github.io/ | 5 bloqueos contra la inyecciêÂ³n de prompts y 10 ataques para probar tu agente |
| [caixa-do-agente](https://linnoff88-dev.github.io/ | evaluaciêÂ³n de tu harness de agente y una caja Docker descartable, sin red ni `.env` |
| [ia-sem-censura-defensiva](https://linnoff88-dev.github.io/ | modelo abierto sin restricciones, usado solo para defensa y ejecutado en tu computadora |
| [protegendo-seus-repos](https://linnoff88-dev.github.io/ | copia de seguridad en 3 capas de tus repositorios contra bloqueos o intrusiones |

## Pruebas

```bash
python3 testes/run.py        # 82 pruebas con datos inventados
python3 testes/gera_exemplo.py   # vuelve a generar el informe de ejemplo
```

Python 3, sin dependencias. Contenido original. Licencia [MIT](LICENSE). MêÂ¡s en [ARCKHê AI](https://ARCKHê AI).