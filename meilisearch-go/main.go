// package main

// import (
// 	"encoding/json"
// 	"io"
//  "os"

// 	"github.com/meilisearch/meilisearch-go"
// )

// func main() {
// 	client := meilisearch.NewClient(meilisearch.ClientConfig{
// 		Host:   "http://localhost:7700",
// 		APIKey: "QtcbkGgDs5SnOtTTzzgafR_S8eQoQCo5MAmhUfuXQkI",
// 	})

// 	jsonFile, _ := os.Open("../opendata/data/t000002d0000000030-88c26d73c154f9d05f542234c287ff63-0.json")
// 	defer jsonFile.Close()

// 	byteValue, _ := io.ReadAll(jsonFile)
// 	var data []map[string]interface{}
// 	json.Unmarshal(byteValue, &data)

// 	println(data)

// 	_, err := client.Index("meguro-data").AddDocuments(data)
// 	if err != nil {
// 		panic(err)
// 	}
// }

package main

import (
	"encoding/json"
	"fmt"
	"io"
	"os"
)

func main() {
	// jsonFile, _ := os.Open("../opendata/data/t000002d0000000030-88c26d73c154f9d05f542234c287ff63-0.json")
	jsonFile, err := os.Open("../opendata/data/main.json")
	if err != nil {
		fmt.Println("JSONファイルを開けません", err)
		return
	}
	defer jsonFile.Close()

	byteValue, err := io.ReadAll(jsonFile)
	if err != nil {
		fmt.Println("JSONデータを読み込めません", err)
		return
	}

	// var data []map[string]interface{}
	type Data struct {
		name string
		age  int
	}
	var data Data
	json.Unmarshal(byteValue, &data)

	// jsonData, err := json.Marshal(jsonFile)
	// if err != nil {
	// 	fmt.Println(err)
	// 	return
	// }

	fmt.Print(data)
}
