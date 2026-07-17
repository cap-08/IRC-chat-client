# Minimal IRC Client

A lightweight, dependency-free IRC client written in Python. Connects to any
IRC server, joins a channel, and lets you chat from the terminal with
color-coded output.

## Features

- Plain TCP or TLS connections
- Auto-registration handling (waits for server welcome before joining)
- Automatic nickname collision handling (retries with `_` suffix)
- Keeps the connection alive via PING/PONG
- Color-coded events: messages, joins, parts, quits, nick changes
- Simple in-chat commands: `/join`, `/quit`

## Requirements

- Python 3.7+
- No external dependencies (uses only the standard library)

## Usage

```bash
python irc_client.py --server irc.libera.chat --port 6667 --nick YourNick --channel "#test"
```

### With TLS (recommended)

```bash
python irc_client.py --server irc.libera.chat --port 6697 --nick YourNick --channel "#test" --tls
```

### Arguments

| Flag         | Default              | Description                        |
|--------------|-----------------------|-------------------------------------|
| `--server`   | `irc.libera.chat`    | IRC server hostname                |
| `--port`     | `6667`               | Server port                        |
| `--nick`     | `JacobBot`           | Nickname to register with          |
| `--channel`  | `#test`              | Channel to auto-join on connect    |
| `--tls`      | off                  | Connect using TLS                  |

## In-chat commands

| Command          | Effect                          |
|-------------------|----------------------------------|
| `/join #channel`  | Leave current context and join a new channel |
| `/quit`            | Disconnect and exit               |
| anything else      | Sent as a message to the current channel |

## Notes / Limitations

- This is a minimal educational client, not a hardened production tool.
- No message logging, no multi-channel tracking, no SASL authentication.
- Not intended for use with sensitive credentials on untrusted networks.

## License

MIT
