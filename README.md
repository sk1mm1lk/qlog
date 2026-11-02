# yaki

## Description

- Yaki is a basic way to take notes in the terminal to a pre-configured directory and topics
- You set a note directory and when writing to a topic it appends to a file of that topic name

## Installation

```go
go build
./yaki --help
```

## Configuration

- Yaki will attempt to load a configuration file from the following locations in order:
    - `~/.config/yaki/config.yaml`
    - `~/.config/yaki/config.yml`
    - `/usr/local/etc/yaki/config.yaml`
    - `/usr/local/etc/yaki/config.yml`
- An example configuration can be found in `config/config.yaml`

## Final thoughts

- I hope this helps you even a little bit
