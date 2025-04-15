package main

import (
	"encoding/json"
	"fmt"
	"io"
	"math/rand"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"sync"
	"time"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/go-chi/cors"
)

type api struct {
	addr string
	urls map[string]struct{}
	mu   sync.Mutex
}

type urlResponse struct {
	URL string `json:"url"`
}

// GenerateRandomSuffix generates a random string of the given length.
func GenerateRandomSuffix(length int) string {
	const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	seed := rand.New(rand.NewSource(time.Now().UnixNano()))
	suffix := make([]byte, length)
	for i := range suffix {
		suffix[i] = charset[seed.Intn(len(charset))]
	}
	return string(suffix)
}

// GetUrl generates a unique URL suffix and adds it to the API's URL set.
func (server *api) GetUrl(w http.ResponseWriter, r *http.Request) {
	suffix := GenerateRandomSuffix(10)
	url := "/url/" + suffix

	server.mu.Lock()
	server.urls[url] = struct{}{}
	server.mu.Unlock()

	response := urlResponse{URL: suffix}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

// UploadPhoto handles image uploads, saving them to a directory named after the code.
func (server *api) UploadPhoto(w http.ResponseWriter, r *http.Request) {
	code := chi.URLParam(r, "code")
	url := "/url/" + code

	server.mu.Lock()
	_, exists := server.urls[url]
	server.mu.Unlock()

	if !exists {
		http.Error(w, "URL not found", http.StatusForbidden)
		return
	}

	// Parse multipart form
	err := r.ParseMultipartForm(32 << 20) // 32MB limit
	if err != nil {
		http.Error(w, fmt.Sprintf("Error parsing form: %v", err), http.StatusBadRequest)
		return
	}

	file, header, err := r.FormFile("image")
	if err != nil {
		if strings.Contains(err.Error(), "multipart: NextPart: EOF") {
			http.Error(w, "Incomplete or malformed multipart form", http.StatusBadRequest)
			return
		}
		http.Error(w, fmt.Sprintf("Error getting file: %v", err), http.StatusBadRequest)
		return
	}
	defer file.Close()

	// Create directories for the file
	assetsDir := "./assets"
	codeDir := filepath.Join(assetsDir, code)
	err = os.MkdirAll(codeDir, os.ModePerm)
	if err != nil {
		http.Error(w, "Error creating directory for the code", http.StatusInternalServerError)
		return
	}

	// Save the file
	filePath := filepath.Join(codeDir, header.Filename)
	destFile, err := os.Create(filePath)
	if err != nil {
		http.Error(w, "Error saving file", http.StatusInternalServerError)
		return
	}
	defer destFile.Close()

	_, err = io.Copy(destFile, file)
	if err != nil {
		http.Error(w, "Error saving file", http.StatusInternalServerError)
		return
	}

	// Respond with success
	w.Header().Set("Content-Type", "text/plain")
	w.Write([]byte(fmt.Sprintf("File successfully saved to %s", filePath)))
}

func (server *api) SendPrediction(w http.ResponseWriter, r *http.Request) {
	assetsDir := "./assets"

	// Find the latest folder
	dirs, err := os.ReadDir(assetsDir)
	if err != nil {
		http.Error(w, "Error reading assets directory", http.StatusInternalServerError)
		return
	}

	var latestDir string
	var latestTime time.Time
	for _, dir := range dirs {
		if dir.IsDir() {
			info, err := dir.Info()
			if err != nil {
				continue
			}
			if info.ModTime().After(latestTime) {
				latestTime = info.ModTime()
				latestDir = filepath.Join(assetsDir, dir.Name())
			}
		}
	}

	if latestDir == "" {
		http.Error(w, "No directories found in assets", http.StatusInternalServerError)
		return
	}

	// Call the Python script
	cmd := exec.Command("python", "../../../../src/main.py ", latestDir, latestDir)
	output, err := cmd.CombinedOutput()
	if err != nil {
		fmt.Printf("Error: %v\n", err)
	}
	fmt.Printf("Output:\n%s\n", string(output))
	err = cmd.Run()
	if err != nil {
		http.Error(w, "Error running Python script", http.StatusInternalServerError)
		return
	}

	logPath := filepath.Join(latestDir, "log.txt")
	logContent, err := os.ReadFile(logPath)
	for err != nil {
		logContent, err = os.ReadFile(logPath)
	}

	w.Header().Set("Content-Type", "text/plain")
	w.Write(logContent)
}

func main() {
	api := &api{
		addr: ":8080",
		urls: make(map[string]struct{}),
	}

	// Configure the router and middleware
	r := chi.NewRouter()
	r.Use(middleware.RequestID)
	r.Use(middleware.RealIP)
	r.Use(middleware.Logger)
	r.Use(middleware.Recoverer)
	r.Use(middleware.Timeout(60 * time.Second))
	r.Use(cors.Handler(cors.Options{
		AllowedOrigins:   []string{"http://localhost:5173"},
		AllowedMethods:   []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowedHeaders:   []string{"Accept", "Authorization", "Content-Type", "X-CSRF-Token"},
		ExposedHeaders:   []string{"Link"},
		AllowCredentials: true,
		MaxAge:           300, // Cache preflight request for 5 minutes
	}))

	// Routes
	r.Get("/url", api.GetUrl)
	r.Post("/upload/{code}", api.UploadPhoto)
	r.Get("/predict", api.SendPrediction)

	// Start the server
	server := http.Server{
		Addr:    api.addr,
		Handler: r,
	}
	if err := server.ListenAndServe(); err != nil {
		fmt.Println("Error starting server:", err)
	}
}
