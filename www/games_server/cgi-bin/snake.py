#!/usr/bin/env python3
import sys

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>SNAKE — CGI</title>
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Orbitron:wght@700;900&display=swap" rel="stylesheet">
<style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
        font-family: 'Orbitron', sans-serif;
        background: #05070a; color: #e8f4fd;
        min-height: 100vh; padding: 2rem 1rem;
        display: flex; flex-direction: column; align-items: center;
        position: relative; overflow-x: hidden;
    }
    body::before {
        content: ''; position: fixed; inset: 0; pointer-events: none;
        background:
            radial-gradient(ellipse 60% 40% at 50% -5%, rgba(124, 252, 0, 0.14) 0%, transparent 60%),
            linear-gradient(rgba(124, 252, 0, 0.025) 1px, transparent 1px),
            linear-gradient(90deg, rgba(124, 252, 0, 0.025) 1px, transparent 1px);
        background-size: auto, 48px 48px, 48px 48px;
    }
    h1 {
        font-family: 'Press Start 2P', monospace;
        font-size: 2rem; letter-spacing: 0.1em;
        color: #7CFC00;
        filter: drop-shadow(0 0 18px rgba(124, 252, 0, 0.6));
    }
    .sub { font-size: 0.75rem; letter-spacing: 0.3em; color: rgba(124, 252, 0, 0.55); text-transform: uppercase; margin: 0.5rem 0 1.5rem; }
    .game-wrap { display: flex; gap: 1.5rem; align-items: flex-start; position: relative; z-index: 1; }
    canvas#board {
        background: #0b1218;
        border: 2px solid rgba(124, 252, 0, 0.4);
        border-radius: 10px;
        box-shadow: 0 0 40px rgba(124, 252, 0, 0.15), inset 0 0 50px rgba(0,0,0,0.7);
    }
    .panel { display: flex; flex-direction: column; gap: 1rem; width: 190px; }
    .box {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 10px; padding: 1rem;
        backdrop-filter: blur(10px);
    }
    .label { font-family: 'Press Start 2P', monospace; font-size: 0.55rem; letter-spacing: 0.15em; color: rgba(124, 252, 0, 0.6); margin-bottom: 0.5rem; }
    .value { font-family: 'Press Start 2P', monospace; font-size: 1.1rem; color: #e8f4fd; }
    .keys { font-size: 0.7rem; line-height: 1.6; color: rgba(232,244,253,0.7); }
    .keys b { color: #7CFC00; }
    .back {
        text-align: center; text-decoration: none;
        color: rgba(124, 252, 0, 0.7);
        font-family: 'Press Start 2P', monospace;
        font-size: 0.55rem; letter-spacing: 0.15em;
        padding: 0.7rem;
        border: 1px solid rgba(124, 252, 0, 0.3);
        border-radius: 8px; transition: all 0.2s;
    }
    .back:hover { color: #7CFC00; border-color: #7CFC00; background: rgba(124, 252, 0, 0.08); }
    .overlay {
        position: absolute; inset: 0; display: none;
        align-items: center; justify-content: center;
        background: rgba(5, 7, 10, 0.85); backdrop-filter: blur(6px);
        border-radius: 10px; flex-direction: column; gap: 1rem;
    }
    .overlay h2 { font-family: 'Press Start 2P', monospace; font-size: 1.3rem; color: #ff2d95; letter-spacing: 0.15em; }
    .overlay p { font-size: 0.85rem; color: rgba(232,244,253,0.8); }
    .overlay button {
        font-family: 'Press Start 2P', monospace; font-size: 0.65rem;
        padding: 0.8rem 1.2rem; background: transparent; color: #7CFC00;
        border: 1px solid #7CFC00; border-radius: 8px; cursor: pointer;
        letter-spacing: 0.1em; transition: all 0.2s;
    }
    .overlay button:hover { background: rgba(124, 252, 0, 0.15); }
    .board-wrap { position: relative; }
</style>
</head>
<body>
    <h1>SNAKE</h1>
    <div class="sub">Served via Python CGI</div>

    <div class="game-wrap">
        <div class="board-wrap">
            <canvas id="board" width="500" height="500"></canvas>
            <div id="overlay" class="overlay">
                <h2 id="overTitle">READY?</h2>
                <p id="overMsg">Use arrow keys / WASD</p>
                <button id="startBtn">▶ START</button>
            </div>
        </div>

        <div class="panel">
            <div class="box">
                <div class="label">SCORE</div>
                <div id="score" class="value">0</div>
            </div>
            <div class="box">
                <div class="label">BEST</div>
                <div id="best" class="value">0</div>
            </div>
            <div class="box">
                <div class="label">SPEED</div>
                <div id="speed" class="value">1.0x</div>
            </div>
            <div class="box">
                <div class="label">CONTROLS</div>
                <div class="keys">
                    <b>↑↓←→</b> / <b>WASD</b><br>
                    <b>P</b> Pause<br>
                    <b>R</b> Restart
                </div>
            </div>
            <a href="/" class="back">◀ BACK TO ARCADE</a>
        </div>
    </div>

<script>
(function () {
    const SIZE = 25, COLS = 20, ROWS = 20;
    const canvas = document.getElementById('board');
    const ctx = canvas.getContext('2d');
    const scoreEl = document.getElementById('score');
    const bestEl = document.getElementById('best');
    const speedEl = document.getElementById('speed');
    const overlay = document.getElementById('overlay');
    const overTitle = document.getElementById('overTitle');
    const overMsg = document.getElementById('overMsg');
    const startBtn = document.getElementById('startBtn');

    let snake, dir, nextDir, food, score, best = 0, tickMs, running, paused, loopId;

    function reset() {
        snake = [{x: 10, y: 10},{x: 9, y: 10},{x: 8, y: 10}];
        dir = {x: 1, y: 0}; nextDir = dir;
        score = 0;
        tickMs = 120;
        paused = false;
        placeFood();
        running = true;
        overlay.style.display = 'none';
        clearInterval(loopId);
        loopId = setInterval(tick, tickMs);
        draw();
    }
    function placeFood() {
        while (true) {
            const x = Math.floor(Math.random() * COLS);
            const y = Math.floor(Math.random() * ROWS);
            if (!snake.some(s => s.x === x && s.y === y)) {
                food = {x, y}; return;
            }
        }
    }
    function tick() {
        if (!running || paused) return;
        dir = nextDir;
        const head = {x: snake[0].x + dir.x, y: snake[0].y + dir.y};
        if (head.x < 0 || head.x >= COLS || head.y < 0 || head.y >= ROWS) return die();
        if (snake.some(s => s.x === head.x && s.y === head.y)) return die();
        snake.unshift(head);
        if (head.x === food.x && head.y === food.y) {
            score += 10;
            if (snake.length % 5 === 0 && tickMs > 55) {
                tickMs -= 6;
                clearInterval(loopId); loopId = setInterval(tick, tickMs);
                speedEl.textContent = (120 / tickMs).toFixed(1) + 'x';
            }
            placeFood();
        } else {
            snake.pop();
        }
        draw();
    }
    function die() {
        running = false;
        if (score > best) best = score;
        bestEl.textContent = best;
        overTitle.textContent = 'GAME OVER';
        overMsg.textContent = 'Score: ' + score + '  ·  Best: ' + best;
        startBtn.textContent = '▶ RESTART';
        overlay.style.display = 'flex';
        clearInterval(loopId);
    }
    function draw() {
        ctx.fillStyle = '#0b1218';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.strokeStyle = 'rgba(124, 252, 0, 0.05)';
        for (let x = 1; x < COLS; x++) { ctx.beginPath(); ctx.moveTo(x * SIZE, 0); ctx.lineTo(x * SIZE, canvas.height); ctx.stroke(); }
        for (let y = 1; y < ROWS; y++) { ctx.beginPath(); ctx.moveTo(0, y * SIZE); ctx.lineTo(canvas.width, y * SIZE); ctx.stroke(); }

        // food
        ctx.save();
        ctx.shadowColor = '#ff2d95'; ctx.shadowBlur = 16;
        ctx.fillStyle = '#ff2d95';
        ctx.beginPath();
        ctx.arc(food.x * SIZE + SIZE / 2, food.y * SIZE + SIZE / 2, SIZE / 2 - 4, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();

        // snake
        snake.forEach((s, i) => {
            const alpha = 1 - i / (snake.length + 5);
            ctx.fillStyle = i === 0 ? '#e8f4fd' : `rgba(124, 252, 0, ${0.4 + alpha * 0.6})`;
            const pad = i === 0 ? 2 : 3;
            const r = 5;
            roundRect(ctx, s.x * SIZE + pad, s.y * SIZE + pad, SIZE - pad*2, SIZE - pad*2, r);
            ctx.fill();
        });

        scoreEl.textContent = score;
    }
    function roundRect(ctx, x, y, w, h, r) {
        ctx.beginPath();
        ctx.moveTo(x + r, y);
        ctx.arcTo(x + w, y, x + w, y + h, r);
        ctx.arcTo(x + w, y + h, x, y + h, r);
        ctx.arcTo(x, y + h, x, y, r);
        ctx.arcTo(x, y, x + w, y, r);
        ctx.closePath();
    }

    document.addEventListener('keydown', (e) => {
        const k = e.key.toLowerCase();
        if (k === 'p') { paused = !paused; return; }
        if (k === 'r') { reset(); return; }
        const moves = {
            'arrowup': {x: 0, y: -1}, 'w': {x: 0, y: -1},
            'arrowdown': {x: 0, y: 1}, 's': {x: 0, y: 1},
            'arrowleft': {x: -1, y: 0}, 'a': {x: -1, y: 0},
            'arrowright': {x: 1, y: 0}, 'd': {x: 1, y: 0}
        };
        const m = moves[k];
        if (!m) return;
        e.preventDefault();
        if (m.x === -dir.x && m.y === -dir.y) return;
        nextDir = m;
    });
    startBtn.addEventListener('click', reset);

    // init idle
    snake = [{x: 10, y: 10},{x: 9, y: 10},{x: 8, y: 10}];
    food = {x: 15, y: 10};
    dir = {x: 1, y: 0};
    draw();
    overlay.style.display = 'flex';
})();
</script>
</body>
</html>"""

sys.stdout.write("Content-Type: text/html; charset=utf-8\r\n\r\n")
sys.stdout.write(HTML)
sys.stdout.flush()
