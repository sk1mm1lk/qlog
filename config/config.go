package config

import (
	"os"
	"os/user"
	"path/filepath"
	"strings"

	"go.yaml.in/yaml/v4"
)

var LatestVersion = 1

type Config struct {
	Version    int         `yaml:"version"`
	NoteRoot   string      `yaml:"note_root"`
	TopicPaths []TopicPath `yaml:"topics"`
}

type TopicPath struct {
	Name string `yaml:"name"`
	Path string `yaml:"path"`
}

func Load() *Config {
	configPath := getConfigPath()

	cwd, err := os.Getwd()
	if err != nil {
		panic(err)
	}


	if configPath == "" {
		return &Config{
			Version: LatestVersion,
			NoteRoot: cwd,
			TopicPaths: []TopicPath{},
		}
	}

	fileBytes, err := os.ReadFile(configPath)
	if err != nil {
		panic(err)
	}

	var config Config
	if err := yaml.Load(fileBytes, &config); err != nil {
		panic(err)
	}

	config.validate()

	return &config
}

func (cfg *Config) validate() {
	usr, _ := user.Current()
	if cfg.NoteRoot == "~" {
		cfg.NoteRoot = usr.HomeDir
	} else if strings.HasPrefix(cfg.NoteRoot, "~/") {
		cfg.NoteRoot = filepath.Join(usr.HomeDir, cfg.NoteRoot[2:])
	}

	for index, path := range cfg.TopicPaths {
		if path.Path == "~" {
			cfg.TopicPaths[index].Path = usr.HomeDir
		} else if strings.HasPrefix(path.Path, "~/") {
			cfg.TopicPaths[index].Path = filepath.Join(usr.HomeDir, path.Path[2:])
		}
	}
}

func (cfg *Config) PathFromTopic(targetTopic string) string {
	for _, topic := range cfg.TopicPaths {
		if targetTopic == topic.Name {
			return topic.Path
		}
	}

	return filepath.Join(cfg.NoteRoot, targetTopic + ".md")
}

func getConfigPath() string {
	usr, _ := user.Current()
	homeDir := usr.HomeDir

	localYaml := filepath.Join(homeDir, ".config/yaki/config.yaml")
	localYml := filepath.Join(homeDir, ".config/yaki/config.yml")
	globalYaml := "/usr/local/etc/yaki/config.yaml"
	globalYml := "/usr/local/etc/yaki/config.yml"

	if _, err := os.Stat(localYaml); err == nil {
		return localYaml
	}
	if _, err := os.Stat(localYml); err == nil {
		return localYml
	}
	if _, err := os.Stat(globalYaml); err == nil {
		return globalYaml
	}
	if _, err := os.Stat(globalYml); err == nil {
		return globalYml
	}

	return ""
}
