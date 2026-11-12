package main

import (
	"flag"
	"fmt"
	"time"
	"bufio"
	"log"
	"os"
	"path/filepath"

	"github.com/sk1mm1lk/qlog/config"
)

type noteMessage struct {
	topic    string
	key      string
	datetime string
	message  string
}

func stringEmpty(target string) bool {
	return target == ""
}

func promptUser(inputText string, defaultText string, target *string) {
	fmt.Printf("%s [%s]> ", inputText, defaultText)

	scanner := bufio.NewScanner(os.Stdin)
	scanner.Scan()
	err := scanner.Err()
	if err != nil {
		log.Fatal(err)
	}
	if scanner.Text() == "" {
		*target = defaultText
	} else {
		*target = scanner.Text()
	}
}

func createMessage(topic, key, message string) noteMessage {
	t := time.Now()
	datetime := t.Format("2006-01-02-15:04:05")

	return noteMessage{
		topic: topic,
		key: key,
		datetime: datetime,
		message: message,
	}
}

func formatMessage(msg noteMessage) string {
	outputMessage := "- [ ] "
	outputMessage += "(" + msg.datetime + ") "
	outputMessage += msg.key + ": "
	outputMessage += msg.message

	return outputMessage
}

func publishMessage(cfg *config.Config, msg noteMessage) error {
	topicPath := cfg.PathFromTopic(msg.topic)
	topicDirPath := filepath.Dir(topicPath)

	if err:= os.MkdirAll(topicDirPath, 0750); err != nil {
		return err
	}

	messageText := formatMessage(msg) + "\n"

	f, err := os.OpenFile(topicPath, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		return err
	}

	if _, err := f.Write([]byte(messageText)); err != nil {
		return err
	}

	if err := f.Close(); err != nil {
		return err
	}

	return nil
}

func main() {
	var topic string
	var key string
	var message string

	topicDefault := "all"
	keyDefault := "all"
	messageDefault := "ping"

	flag.StringVar(&topic, "topic", topicDefault, "Sets the topic to which the note is appended to")
	flag.StringVar(&key, "key", keyDefault, "Sets the key of the note")
	flag.StringVar(&message, "message", messageDefault, "Sets the message of the note")
	flag.Parse()

	if topic == topicDefault {
		promptUser("topic", topicDefault, &topic)
	}

	if key == keyDefault {
		promptUser("key", keyDefault, &key)
	}

	if message == messageDefault {
		promptUser("message", messageDefault, &message)
	}

	cfg := config.Load()

	msg := createMessage(topic, key, message)
	
	if err := publishMessage(cfg, msg); err != nil {
		panic(err)
	}
}
