# Spotify Server Client

Spotify Server Client is a program for testing the backoff strategy between the client and the server. Spotify servers responding with regarding the time schedule.

## Usage

If you want to run program as server

```bash
python3 spotify.py server [INTERFACE] [PORT]
```

Example:

```bash
python3 spotify.py server 127.0.0.1 3030
```

If you want to run program as client

```bash
python3 spotify.py client [HOSTNAME] [PORT]
```

Example:

```bash
python3 spotify.py client 127.0.0.1 3030
```
