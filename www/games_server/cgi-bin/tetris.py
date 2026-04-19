#!/usr/bin/env python3
import sys

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>TETRIS — CGI</title>
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Orbitron:wght@700;900&display=swap" rel="stylesheet">
<style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
        font-family: 'Orbitron', sans-serif;
        background: #05070a;
        color: #e8f4fd;
        min-height: 100vh;
        display: flex; flex-direction: column; align-items: center;
        padding: 2rem 1rem;
        position: relative; overflow-x: hidden;
    }
    body::before {
        content: ''; position: fixed; inset: 0; pointer-events: none;
        background:
            radial-gradient(ellipse 70% 40% at 50% -5%, rgba(79, 195, 247, 0.15) 0%, transparent 60%),
            linear-gradient(rgba(79, 195, 247, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(79, 195, 247, 0.03) 1px, transparent 1px);
        background-size: auto, 48px 48px, 48px 48px;
    }
    h1 {
        font-family: 'Press Start 2P', monospace;
        font-size: 2rem; letter-spacing: 0.1em;
        color: #4fc3f7;
        filter: drop-shadow(0 0 18px rgba(79, 195, 247, 0.6));
        margin-bottom: 0.5rem;
    }
    .sub { font-size: 0.75rem; letter-spacing: 0.3em; color: rgba(79, 195, 247, 0.5); text-transform: uppercase; margin-bottom: 1.5rem; }
    .game-wrap {
        display: flex; gap: 1.5rem; align-items: flex-start;
        position: relative; z-index: 1;
    }
    canvas {
        background: #0b1218;
        border: 2px solid rgba(79, 195, 247, 0.4);
        border-radius: 10px;
        box-shadow: 0 0 40px rgba(79, 195, 247, 0.15), inset 0 0 50px rgba(0,0,0,0.8);
    }
    .panel {
        display: flex; flex-direction: column; gap: 1rem;
        width: 180px;
    }
    .panel .box {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 10px;
        padding: 1rem;
        backdrop-filter: blur(10px);
    }
    .label { font-family: 'Press Start 2P', monospace; font-size: 0.55rem; letter-spacing: 0.15em; color: rgba(79, 195, 247, 0.6); margin-bottom: 0.5rem; }
    .value { font-family: 'Press Start 2P', monospace; font-size: 1.1rem; color: #e8f4fd; }
    #next { width: 100%; height: 100px; background: #0b1218; border-radius: 6px; }
    .keys { font-size: 0.7rem; line-height: 1.6; color: rgba(232,244,253,0.7); }
    .keys b { color: #4fc3f7; }
    .back {
        margin-top: 1rem;
        text-align: center;
        text-decoration: none;
        color: rgba(79, 195, 247, 0.7);
        font-family: 'Press Start 2P', monospace;
        font-size: 0.55rem; letter-spacing: 0.15em;
        padding: 0.7rem;
        border: 1px solid rgba(79, 195, 247, 0.3);
        border-radius: 8px;
        transition: all 0.2s;
    }
    .back:hover { color: #4fc3f7; border-color: #4fc3f7; background: rgba(79, 195, 247, 0.08); }
    .overlay {
        position: absolute; inset: 0;
        display: none; align-items: center; justify-content: center;
        background: rgba(5, 7, 10, 0.85); backdrop-filter: blur(6px);
        border-radius: 10px; flex-direction: column; gap: 1rem;
    }
    .overlay h2 { font-family: 'Press Start 2P', monospace; font-size: 1.3rem; color: #ff2d95; letter-spacing: 0.15em; }
    .overlay p { font-size: 0.85rem; color: rgba(232,244,253,0.8); }
    .overlay button {
        margin-top: 0.5rem;
        font-family: 'Press Start 2P', monospace; font-size: 0.65rem; letter-spacing: 0.1em;
        padding: 0.8rem 1.2rem; background: transparent; color: #4fc3f7;
        border: 1px solid #4fc3f7; border-radius: 8px; cursor: pointer;
        transition: all 0.2s;
    }
    .overlay button:hover { background: rgba(79, 195, 247, 0.15); }
    .board-wrap { position: relative; }
</style>
</head>
<body>
    <h1>TETRIS</h1>
    <div class="sub">Served via Python CGI</div>
    <div class="game-wrap">
        <div class="board-wrap">
            <canvas id="board" width="300" height="600"></canvas>
            <div id="overlay" class="overlay">
                <h2 id="overTitle">GAME OVER</h2>
                <p id="overMsg">Press Start to try again</p>
                <button id="restartBtn">▶ START</button>
            </div>
        </div>
        <div class="panel">
            <div class="box">
                <div class="label">SCORE</div>
                <div id="score" class="value">0</div>
            </div>
            <div class="box">
                <div class="label">LEVEL</div>
                <div id="level" class="value">1</div>
            </div>
            <div class="box">
                <div class="label">LINES</div>
                <div id="lines" class="value">0</div>
            </div>
            <div class="box">
                <div class="label">NEXT</div>
                <canvas id="next" width="120" height="120"></canvas>
            </div>
            <div class="box">
                <div class="label">CONTROLS</div>
                <div class="keys">
                    <b>←→</b> Move<br>
                    <b>↓</b> Soft drop<br>
                    <b>↑</b> Rotate<br>
                    <b>SPACE</b> Hard drop<br>
                    <b>P</b> Pause
                </div>
            </div>
            <a href="/" class="back">◀ BACK TO ARCADE</a>
        </div>
    </div>

<script>
(function () {
    const COLS = 10, ROWS = 20, SIZE = 30;
    const canvas = document.getElementById('board');
    const ctx = canvas.getContext('2d');
    const nextCanvas = document.getElementById('next');
    const nctx = nextCanvas.getContext('2d');
    const scoreEl = document.getElementById('score');
    const levelEl = document.getElementById('level');
    const linesEl = document.getElementById('lines');
    const overlay = document.getElementById('overlay');
    const overTitle = document.getElementById('overTitle');
    const overMsg = document.getElementById('overMsg');
    const restartBtn = document.getElementById('restartBtn');

    const COLORS = {
        I: '#4fc3f7', O: '#ffd93d', T: '#c970ff', S: '#7CFC00',
        Z: '#ff2d95', J: '#5c6bff', L: '#ff9f43'
    };
    const SHAPES = {
        I: [[0,0,0,0],[1,1,1,1],[0,0,0,0],[0,0,0,0]],
        O: [[1,1],[1,1]],
        T: [[0,1,0],[1,1,1],[0,0,0]],
        S: [[0,1,1],[1,1,0],[0,0,0]],
        Z: [[1,1,0],[0,1,1],[0,0,0]],
        J: [[1,0,0],[1,1,1],[0,0,0]],
        L: [[0,0,1],[1,1,1],[0,0,0]]
    };
    const TYPES = Object.keys(SHAPES);

    let grid, current, next, score, lines, level, dropInterval, dropCounter, lastTime, running, paused;

    function newGrid() {
        const g = [];
        for (let r = 0; r < ROWS; r++) g.push(new Array(COLS).fill(0));
        return g;
    }
    function newPiece() {
        const type = TYPES[Math.floor(Math.random() * TYPES.length)];
        const shape = SHAPES[type].map(row => row.slice());
        return { type, shape, x: Math.floor((COLS - shape[0].length) / 2), y: 0 };
    }
    function rotate(shape) {
        const n = shape.length;
        const out = [];
        for (let i = 0; i < n; i++) {
            out.push([]);
            for (let j = 0; j < n; j++) out[i].push(shape[n - 1 - j][i]);
        }
        return out;
    }
    function collides(piece, grid, dx = 0, dy = 0, shape = piece.shape) {
        for (let y = 0; y < shape.length; y++) {
            for (let x = 0; x < shape[y].length; x++) {
                if (!shape[y][x]) continue;
                const nx = piece.x + x + dx;
                const ny = piece.y + y + dy;
                if (nx < 0 || nx >= COLS || ny >= ROWS) return true;
                if (ny >= 0 && grid[ny][nx]) return true;
            }
        }
        return false;
    }
    function merge(piece, grid) {
        for (let y = 0; y < piece.shape.length; y++) {
            for (let x = 0; x < piece.shape[y].length; x++) {
                if (piece.shape[y][x]) {
                    const ny = piece.y + y;
                    if (ny >= 0) grid[ny][piece.x + x] = piece.type;
                }
            }
        }
    }
    function clearLines() {
        let cleared = 0;
        for (let y = ROWS - 1; y >= 0; y--) {
            if (grid[y].every(c => c)) {
                grid.splice(y, 1);
                grid.unshift(new Array(COLS).fill(0));
                cleared++;
                y++;
            }
        }
        if (cleared > 0) {
            const pts = [0, 100, 300, 500, 800][cleared] * level;
            score += pts;
            lines += cleared;
            level = Math.floor(lines / 10) + 1;
            dropInterval = Math.max(80, 800 - (level - 1) * 60);
        }
    }
    function drawCell(c, x, y, s = SIZE, target = ctx) {
        const color = COLORS[c] || '#333';
        target.fillStyle = color;
        target.fillRect(x * s, y * s, s, s);
        target.fillStyle = 'rgba(255,255,255,0.18)';
        target.fillRect(x * s, y * s, s, 3);
        target.fillRect(x * s, y * s, 3, s);
        target.fillStyle = 'rgba(0,0,0,0.28)';
        target.fillRect(x * s + s - 3, y * s, 3, s);
        target.fillRect(x * s, y * s + s - 3, s, 3);
    }
    function drawGhost(piece) {
        let dy = 0;
        while (!collides(piece, grid, 0, dy + 1)) dy++;
        ctx.globalAlpha = 0.22;
        for (let y = 0; y < piece.shape.length; y++) {
            for (let x = 0; x < piece.shape[y].length; x++) {
                if (piece.shape[y][x]) {
                    drawCell(piece.type, piece.x + x, piece.y + y + dy);
                }
            }
        }
        ctx.globalAlpha = 1;
    }
    function draw() {
        ctx.fillStyle = '#0b1218';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.strokeStyle = 'rgba(79, 195, 247, 0.06)';
        for (let x = 1; x < COLS; x++) {
            ctx.beginPath(); ctx.moveTo(x * SIZE, 0); ctx.lineTo(x * SIZE, canvas.height); ctx.stroke();
        }
        for (let y = 1; y < ROWS; y++) {
            ctx.beginPath(); ctx.moveTo(0, y * SIZE); ctx.lineTo(canvas.width, y * SIZE); ctx.stroke();
        }
        for (let y = 0; y < ROWS; y++) {
            for (let x = 0; x < COLS; x++) {
                if (grid[y][x]) drawCell(grid[y][x], x, y);
            }
        }
        if (current) {
            drawGhost(current);
            for (let y = 0; y < current.shape.length; y++) {
                for (let x = 0; x < current.shape[y].length; x++) {
                    if (current.shape[y][x]) drawCell(current.type, current.x + x, current.y + y);
                }
            }
        }
        nctx.fillStyle = '#0b1218';
        nctx.fillRect(0, 0, nextCanvas.width, nextCanvas.height);
        if (next) {
            const s = 22;
            const ox = Math.floor((nextCanvas.width / s - next.shape[0].length) / 2);
            const oy = Math.floor((nextCanvas.height / s - next.shape.length) / 2);
            for (let y = 0; y < next.shape.length; y++) {
                for (let x = 0; x < next.shape[y].length; x++) {
                    if (next.shape[y][x]) drawCell(next.type, ox + x, oy + y, s, nctx);
                }
            }
        }
        scoreEl.textContent = score;
        levelEl.textContent = level;
        linesEl.textContent = lines;
    }
    function spawn() {
        current = next || newPiece();
        next = newPiece();
        if (collides(current, grid)) {
            running = false;
            overTitle.textContent = 'GAME OVER';
            overMsg.textContent = 'Final score: ' + score;
            restartBtn.textContent = '▶ RESTART';
            overlay.style.display = 'flex';
        }
    }
    function hardDrop() {
        while (!collides(current, grid, 0, 1)) current.y++;
        score += 2;
        lockPiece();
    }
    function lockPiece() {
        merge(current, grid);
        clearLines();
        spawn();
    }
    function tick(time = 0) {
        if (!running || paused) { lastTime = time; requestAnimationFrame(tick); return; }
        const delta = time - lastTime;
        lastTime = time;
        dropCounter += delta;
        if (dropCounter >= dropInterval) {
            dropCounter = 0;
            if (!collides(current, grid, 0, 1)) current.y++;
            else lockPiece();
        }
        draw();
        requestAnimationFrame(tick);
    }
    function reset() {
        grid = newGrid();
        next = newPiece();
        score = 0; lines = 0; level = 1;
        dropInterval = 800; dropCounter = 0; lastTime = 0;
        paused = false;
        spawn();
        running = true;
        overlay.style.display = 'none';
        draw();
    }

    document.addEventListener('keydown', (e) => {
        if (!running || !current) return;
        if (e.key === 'ArrowLeft') { if (!collides(current, grid, -1, 0)) current.x--; }
        else if (e.key === 'ArrowRight') { if (!collides(current, grid, 1, 0)) current.x++; }
        else if (e.key === 'ArrowDown') {
            if (!collides(current, grid, 0, 1)) { current.y++; score += 1; }
            else lockPiece();
        }
        else if (e.key === 'ArrowUp') {
            const rotated = rotate(current.shape);
            if (!collides(current, grid, 0, 0, rotated)) current.shape = rotated;
        }
        else if (e.key === ' ') { e.preventDefault(); hardDrop(); }
        else if (e.key === 'p' || e.key === 'P') { paused = !paused; }
        if (['ArrowLeft','ArrowRight','ArrowDown','ArrowUp',' '].includes(e.key)) e.preventDefault();
        draw();
    });
    restartBtn.addEventListener('click', reset);

    overTitle.textContent = 'READY?';
    overMsg.textContent = 'Arrow keys + space to play';
    restartBtn.textContent = '▶ START';
    overlay.style.display = 'flex';
    grid = newGrid();
    draw();
    requestAnimationFrame(tick);
})();
</script>
</body>
</html>"""

sys.stdout.write("Content-Type: text/html; charset=utf-8\r\n\r\n")
sys.stdout.write(HTML)
sys.stdout.flush()
