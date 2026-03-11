# GlazeWM + Zebar Configuration

Configuracion personal de escritorio para Windows usando [GlazeWM](https://github.com/glzr-io/glazewm) y Zebar.

## Vista general

- Barra superior con workspaces `1-10`, media, stats del sistema y systray.
- Navegacion y movimiento de ventanas estilo Vim (`Alt+H/J/K/L`).
- Atajos para terminal, explorador y navegador.
- Workspaces con cambio rapido y mover ventanas entre espacios.

## Capturas del escritorio

### 1) Escritorio limpio
![Escritorio limpio](doc/GlazeVM/1.png)

### 2) Tiling con multiples terminales
![Tiling con terminales](doc/GlazeVM/2.png)

### 3) Launcher / busqueda rapida
![Launcher y busqueda](doc/GlazeVM/3.png)

### 4) Flujo de desarrollo en terminal
![Desarrollo en terminal](doc/GlazeVM/4.png)

### 5) Neovim + panel de trabajo
![Neovim y panel](doc/GlazeVM/5.png)

## Atajos principales

| Accion | Atajo |
|--------|-------|
| Abrir Windows Terminal | `Alt+Enter` |
| Abrir File Explorer | `Alt+E` |
| Abrir Chrome | `Alt+B` |
| Cambiar foco (izq/abajo/arriba/der) | `Alt+H/J/K/L` |
| Mover ventana (izq/abajo/arriba/der) | `Alt+Shift+H/J/K/L` |
| Activar modo resize | `Alt+R` |
| Toggle floating | `Alt+Shift+Space` |
| Toggle fullscreen | `Alt+F` |
| Cambiar workspace | `Alt+1` a `Alt+0` |
| Mover ventana a workspace | `Alt+Shift+1` a `Alt+Shift+0` |
| Cerrar ventana | `Alt+Q` |
| Pausar bindings | `Alt+Shift+P` |
| Recargar config | `Alt+Shift+R` |

## Requisitos

- Windows 10/11
- [GlazeWM](https://github.com/glzr-io/glazewm)
- Zebar
- Windows Terminal
- Google Chrome

## Instalacion

1. Copiar `glazewm/config.yaml` en `%APPDATA%\glazewm\config.yaml`.
2. Copiar la config de Zebar segun tu widget/layout.
3. Reiniciar GlazeWM.

## Referencia

- Documentacion de GlazeWM: [Config documentation](https://github.com/glzr-io/glazewm?tab=readme-ov-file#config-documentation)
