# GlazeWM + Zebar Configuration

Personal Windows desktop setup with GlazeWM and Zebar.

Official GlazeWM repository:
https://github.com/glzr-io/glazewm

## Installation

1. Install GlazeWM from the official repository: https://github.com/glzr-io/glazewm
2. Copy `glazewm/config.yaml` to `%USERPROFILE%\.glzr\glazewm\config.yaml`.
3. Copy `glazewm/kill-focused-process.ps1` to `%USERPROFILE%\.glzr\glazewm\` (used by `Alt+Shift+Q`).
4. Restart GlazeWM.

## Zebar

Zebar comes bundled with GlazeWM and starts automatically. Its local settings are not part of this repository, so no manual installation is required.

## Screenshots

### 1) Clean desktop
![Clean desktop](doc/GlazeVM/1.png)

### 2) Multi-terminal tiling
![Multi-terminal tiling](doc/GlazeVM/2.png)

### 3) App launcher / quick search
![App launcher and quick search](doc/GlazeVM/3.png)

### 4) Terminal development flow
![Terminal development flow](doc/GlazeVM/4.png)

### 5) Neovim + work panel
![Neovim and work panel](doc/GlazeVM/5.png)

## Keybindings

| Action | Binding |
|--------|-------|
| Open Windows Terminal | `Alt+Enter` |
| Open File Explorer | `Alt+E` |
| Open Chrome | `Alt+B` |
| Focus (left/down/up/right) | `Alt+H/J/K/L` |
| Move window (left/down/up/right) | `Ctrl+Shift+H/J/K/L` |
| Resize window (left/down/up/right) | `Alt+Shift+H/J/K/L` |
| Enable resize mode | `Alt+R` |
| Toggle tiling | `Alt+T` |
| Toggle floating | `Alt+Shift+Space` |
| Toggle fullscreen | `Alt+F` |
| Minimize window | `Alt+M` |
| Cycle focus (tiling/floating/fullscreen) | `Alt+Space` |
| Toggle tiling direction | `Alt+V` |
| Switch workspace | `Alt+1` to `Alt+0` |
| Move window to workspace | `Alt+Shift+1` to `Alt+Shift+0` |
| Move workspace to monitor | `Alt+Shift+A/S/D/F` |
| Close window (graceful) | `Alt+Q` |
| Force-kill focused process | `Alt+Shift+Q` |
| Pause bindings | `Alt+Shift+P` |
| Reload config | `Alt+Shift+R` |
| Exit GlazeWM | `Alt+Shift+E` |
| Redraw windows | `Alt+Shift+W` |
| Screenshot | `PrintScreen` |

## Requirements

- Windows 10/11
- GlazeWM (official repo): https://github.com/glzr-io/glazewm
- Zebar (bundled with GlazeWM)
- Windows Terminal
- Google Chrome

## Documentation

- GlazeWM config docs: https://github.com/glzr-io/glazewm?tab=readme-ov-file#config-documentation
