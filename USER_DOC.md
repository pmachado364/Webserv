# User Documentation

## Overview

Webserv is an HTTP/1.1 web server written in C++98.

It is configured through a `.conf` file using an Nginx-inspired block syntax. The server can serve static files, handle configured routes, process basic HTTP methods, and execute CGI scripts depending on the provided configuration.

This document explains how to build, configure, run, and test the server.

For the full configuration reference, see [CONFIG.md](CONFIG.md).

---

## Prerequisites

- Linux environment
- `g++` with C++98 support
- `make`
- `curl` for command-line testing
- A web browser for manual testing

---

## Building the Server

From the root of the repository:

```bash
make
```

The resulting binary is named:

```
webserv
```

Available Makefile rules:

```bash
# Build the binary
make

# Remove object files
make clean

# Remove object files and the binary
make fclean

# Rebuild from scratch
make re

# Run with Valgrind, if supported by the Makefile
make val
```

---

## Running the Server

Run the server with a configuration file:

```bash
./webserv config/default.conf
```

General usage:

```bash
./webserv [config_file]
```

A configuration file must be provided.

---

## Configuration

The server is configured through a `.conf` file composed of one or more `server` blocks. Each server block defines how the server listens for connections and how it handles requests.

A server block may also contain `location` blocks, which define behaviour for specific URL paths.

### Basic example

```nginx
server {
    listen 8080;
    root /var/www/html;
    server_name example.com;

    location / {
        methods GET;
        index index.html;
    }
}
```

For the full list of supported directives, see [CONFIG.md](CONFIG.md).

---

## Testing the Server

Once the server is running, you can test it with a browser:

```
http://localhost:8080/
```

You can also test it with `curl`.

### Basic GET request
```bash
curl http://localhost:8080/
```

### POST request with body
```bash
curl -X POST http://localhost:8080/upload -d "data=hello"
```

### DELETE request
```bash
curl -X DELETE http://localhost:8080/uploads/file.txt
```

### Show response headers
```bash
curl -i http://localhost:8080/
```

---

## Stopping the Server

To stop the server, press:

```
Ctrl + C
```

---

## Checking Server Output

The server prints runtime information to the terminal.

You can redirect output to a file for inspection:

```bash
./webserv config/default.conf > server.log 2>&1
```

Then inspect the file with:

```bash
cat server.log
```

or:

```bash
tail -f server.log
```

---

## Common Issues

### Port already in use

If the configured port is already being used by another process, the server may fail to start.

You can check which process is using a port with:

```bash
lsof -i :8080
```

You can also try changing the `listen` port in the configuration file.

---

### File not found

If a request returns `404 Not Found`, check that:

- the configured `root` path is correct
- the requested file exists inside that root directory
- the matching `location` block points to the expected directory

Example:

```nginx
server {
    listen 8080;
    root /var/www/html;

    location / {
        index index.html;
    }
}
```

A request to `http://localhost:8080/index.html` will look for `/var/www/html/index.html`.

---

### Method not allowed

If a request returns `405 Method Not Allowed`, check the `methods` directive in the matching server or location block.

Example:

```nginx
location /upload {
    methods POST;
}
```

In this case, a GET request to `/upload` will be rejected, while a POST request is allowed.

---

### Configuration error

If the server refuses to start, check the configuration file syntax.

Common mistakes include:

- missing semicolons
- missing closing braces
- invalid directive names
- invalid port numbers
- duplicated or conflicting directives

Example of a missing semicolon:

```nginx
server {
    listen 8080
    root /var/www/html;
}
```

Correct version:

```nginx
server {
    listen 8080;
    root /var/www/html;
}
```

---

## Useful Commands

### Send a custom Host header

Useful for testing how requests look when sent with a specific `Host` header.

```bash
curl -H "Host: example.com" http://localhost:8080/
```

### Send a POST request from a file

```bash
curl -X POST http://localhost:8080/upload --data-binary @file.txt
```

### Save the response body to a file

```bash
curl http://localhost:8080/index.html -o output.html
```

### Verbose curl output

```bash
curl -v http://localhost:8080/
```

---

## More Information

For configuration details, supported directives, and examples, see [CONFIG.md](CONFIG.md).