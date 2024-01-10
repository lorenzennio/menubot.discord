# TU Garching lunch menu discord bot 

This discord bot sends the Garching TUM Mensa lunch menu to a channel every day at a certain time.

## Setup

In a `.env` file specify
```
DISCORD_TOKEN=...
CHANNEL=...
```

## Running

Run via `systemctl`:
- `cp discordbot.service ~/.local/lib/systemd/system`
- `systemctl --user enable discordbot.service`
- `systemctl --user start discordbot.service`

Check status:
- `systemctl --user status discordbot.service`

Restart:
- `systemctl --user restart discordbot.service`

