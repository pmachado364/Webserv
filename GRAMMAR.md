# Configuration Language Grammar

This document defines the formal syntax of the Webserv configuration language using EBNF (Extended Backus–Naur Form).

Since the parser is implemented as a recursive descent parser, each grammar rule maps directly to a parsing function in the code.

---

## 1. Lexical Structure

Before the parser runs, the raw file is broken into tokens.

### Token Types

| Token | Definition |
|---|---|
| `WORD` | Any sequence of characters containing no whitespace or symbols |
| `LBRACE` | `{` |
| `RBRACE` | `}` |
| `SEMICOLON` | `;` |

The tokenizer does not classify words as numbers, paths, methods, or keywords. All semantic interpretation happens during parsing.

Each token stores the line number where it was found, used for precise error reporting.

### Comments

A `#` starts a comment, and everything from `#` to the end of the line is ignored.

### Whitespace

Whitespace, tabs, and newlines are ignored except as token separators.

---

## 2. Structural Grammar

### Configuration

```
config → server_block+
```

A configuration file consists of one or more server blocks.

---

### Server Block

```
server_block → "server" LBRACE server_body RBRACE
```

---

### Server Body

```
server_body → (
    listen_directive
  | server_name_directive
  | root_directive
  | client_max_body_size_directive
  | error_page_directive
  | methods_directive
  | location_block
)*
```

Directives may appear in any order inside a server block.

---

### Listen Directive

```
listen_directive → "listen" WORD SEMICOLON
```

The `WORD` may be a `PORT` (e.g. `8080`) or a `HOST:PORT` (e.g. `127.0.0.1:8080`).
If only a port is provided, the host defaults to `0.0.0.0`.

---

### Server Name Directive

```
server_name_directive → "server_name" WORD+ SEMICOLON
```

One or more names are allowed. Example: `server_name example.com localhost;`

---

### Root Directive

```
root_directive → "root" WORD SEMICOLON
```

Only one `root` directive is allowed per server block.

---

### Client Max Body Size Directive

```
client_max_body_size_directive → "client_max_body_size" WORD SEMICOLON
```

Examples: `client_max_body_size 10M;` or `client_max_body_size 1024k;`

---

### Error Page Directive

```
error_page_directive → "error_page" error_code+ path SEMICOLON
error_code → WORD
path → WORD
```

One or more error codes followed by a single path.
Example: `error_page 500 502 503 /errors/50x.html;`

---

### Methods Directive

```
methods_directive → "methods" WORD+ SEMICOLON
```

If present, must contain at least one method. Example: `methods GET POST;`

---

### Location Block

```
location_block → "location" WORD LBRACE location_body RBRACE
```

Example: `location /images { ... }`

---

### Location Body

```
location_body → (
    root_directive
  | methods_directive
  | autoindex_directive
  | index_directive
  | upload_dir_directive
  | client_max_body_size_directive
  | cgi_ext_directive
  | error_page_directive
  | return_directive
)*
```

Nested location blocks are structurally forbidden.

---

### Autoindex Directive

```
autoindex_directive → "autoindex" WORD SEMICOLON
```

Allowed values: `on` | `off`

---

### Index Directive

```
index_directive → "index" WORD+ SEMICOLON
```

One or more filenames. The server tries each in order when a directory is requested.
Example: `index index.html index.htm;`

---

### Upload Directory Directive

```
upload_dir_directive → "upload_dir" WORD SEMICOLON
```

Example: `upload_dir /var/www/uploads;`

---

### CGI Extension Directive

```
cgi_ext_directive → "cgi_ext" WORD WORD SEMICOLON
```

Maps a file extension to a CGI interpreter. May appear multiple times inside a location block.
Example: `cgi_ext .py /usr/bin/python3;`

---

### Return Directive

```
return_directive → "return" WORD WORD SEMICOLON
```

Example: `return 301 /new-path;`

---

## 3. Semantic Constraints

These rules are enforced after structural parsing. A file may be syntactically valid but still fail validation.

### Structural Constraints

- At least one `server` block must exist
- Each `server` block must contain at least one `listen` directive
- A server block may define `root` at most once
- A server block may define `methods` at most once
- A server block may define `server_name` at most once
- Nested `location` blocks are forbidden

### Data Validation Constraints

- No two `listen` directives anywhere in the configuration file may share the same `host:port` combination — duplicates are rejected at startup.
- Location paths must start with `/`
- Paths in `root` and `upload_dir` must be valid filesystem paths
- Ports must be integers in the range `1–65535`
- `client_max_body_size` must be a valid numeric format (e.g. `10M`, `1024k`)
- `error_page` codes must be valid integers
- `cgi_ext` extensions must start with `.` (e.g. `.py`)
- `return` codes must be `301` or `302`
- Unknown directives cause an immediate parsing error

### Error Handling

- All errors must report the correct line number
- The server exits with error code `1` if parsing fails