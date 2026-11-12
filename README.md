# qlog

## Description

- qlog stands for quick log, it's purpose is to quickly log something to a file
- The logs are added to files based on the "topic" you add to, and "key" is just a way to sort the logs inside the file

## Installation and Usage

```go
go build
./qlog --help
```

## Configuration

- qlog will attempt to load a configuration file from the following locations in order:
    - `~/.config/qlog/config.yaml`
    - `~/.config/qlog/config.yml`
    - `/usr/local/etc/qlog/config.yaml`
    - `/usr/local/etc/qlog/config.yml`
- An example configuration can be found in `config/config.yaml`

## Final thoughts

- I hope this helps you even a little bit
