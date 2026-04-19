#!/usr/bin/env python3
import sys

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>2048 — CGI</title>
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
            radial-gradient(ellipse 60% 40% at 50% -5%, rgba(255, 45, 149, 0.14) 0%, transparent 60%),
            linear-gradient(rgba(255, 45, 149, 0.025) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 45, 149, 0.025) 1px, transparent 1px);
        background-size: auto, 48px 48px, 48px 48px;
    }
    h1 {
        font-family: 'Press Start 2P', monospace;
        font-size: 2rem; letter-spacing: 0.1em;
        color: #ff2d95;
        filter: drop-shadow(0 0 18px rgba(255, 45, 149, 0.6));
    }
    .sub { font-size: 0.75rem; letter-spacing: 0.3em; color: rgba(255, 45, 149, 0.55); text-transform: uppercase; margin: 0.5rem 0 1.5rem; }
    .layout { display: flex; gap: 1.5rem; align-items: flex-start; position: relative; z-index: 1; }

    .board-wrap { position: relative; }
    .board {
        --gap: 10px;
        background: #0b1218;
        border: 2px solid rgba(255, 45, 149, 0.35);
        border-radius: 12px;
        padding: var(--gap);
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        grid-template-rows: repeat(4, 1fr);
        gap: var(--gap);
        width: 440px; height: 440px;
        box-shadow: 0 0 40px rgba(255, 45, 149, 0.12), inset 0 0 50px rgba(0,0,0,0.6);
    }
    .cell {
        background: rgba(255,255,255,0.03);
        border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        font-family: 'Press Start 2P', monospace;
        font-size: 1.4rem;
        color: #e8f4fd;
        transition: transform 0.12s ease, background 0.12s ease;
    }
    .cell[data-val="2"]    { background: #1f2a33; color: #cfe7f5; }
    .cell[data-val="4"]    { background: #27394a; color: #cfe7f5; }
    .cell[data-val="8"]    { background: #ff9f43; color: #0b1218; }
    .cell[data-val="16"]   { background: #ff7a3d; color: #0b1218; }
    .cell[data-val="32"]   { background: #ff5b5b; color: #fff; }
    .cell[data-val="64"]   { background: #ff2d95; color: #fff; }
    .cell[data-val="128"]  { background: #c970ff; color: #fff; font-size: 1.2rem; }
    .cell[data-val="256"]  { background: #a246ff; color: #fff; font-size: 1.2rem; }
    .cell[data-val="512"]  { background: #5c6bff; color: #fff; font-size: 1.15rem; }
    .cell[data-val="1024"] { background: #4fc3f7; color: #0b1218; font-size: 1rem; }
    .cell[data-val="2048"] { background: #7CFC00; color: #0b1218; font-size: 1rem; box-shadow: 0 0 28px rgba(124, 252, 0, 0.7); }
    .cell.pop { transform: scale(1.08); }

    .panel { display: flex; flex-direction: column; gap: 1rem; width: 200px; }
    .box {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 10px; padding: 1rem;
        backdrop-filter: blur(10px);
    }
    .label { font-family: 'Press Start 2P', monospace; font-size: 0.55rem; letter-spacing: 0.15em; color: rgba(255, 45, 149, 0.7); margin-bottom: 0.5rem; }
    .value { font-family: 'Press Start 2P', monospace; font-size: 1.2rem; color: #e8f4fd; }
    .keys { font-size: 0.7rem; line-height: 1.6; color: rgba(232,244,253,0.7); }
    .keys b { color: #ff2d95; }

    .btn {
        text-align: center; text-decoration: none; cursor: pointer;
        color: rgba(255, 45, 149, 0.85);
        font-family: 'Press Start 2P', monospace;
        font-size: 0.6rem; letter-spacing: 0.15em;
        padding: 0.7rem; background: transparent;
        border: 1px solid rgba(255, 45, 149, 0.4);
        border-radius: 8px; transition: all 0.2s;
    }
    .btn:hover { color: #ff2d95; border-color: #ff2d95; background: rgba(255, 45, 149, 0.08); }
    .back {
        text-align: center; text-decoration: none;
        color: rgba(79, 195, 247, 0.7);
        font-family: 'Press Start 2P', monospace;
        font-size: 0.55rem; letter-spacing: 0.15em;
        padding: 0.7rem;
        border: 1px solid rgba(79, 195, 247, 0.3);
        border-radius: 8px; transition: all 0.2s;
    }
    .back:hover { color: #4fc3f7; border-color: #4fc3f7; background: rgba(79, 195, 247, 0.08); }

    .overlay {
        position: absolute; inset: 0; display: none;
        align-items: center; justify-content: center;
        background: rgba(5, 7, 10, 0.88); backdrop-filter: blur(6px);
        border-radius: 12px; flex-direction: column; gap: 1rem;
    }
    .overlay h2 { font-family: 'Press Start 2P', monospace; font-size: 1.3rem; letter-spacing: 0.15em; }
    .overlay.win h2 { color: #7CFC00; }
    .overlay.lose h2 { color: #ff2d95; }
    .overlay p { font-size: 0.9rem; color: rgba(232,244,253,0.85); }
</style>
</head>
<body>
    <h1>2048</h1>
    <div class="sub">Served via Python CGI</div>
    <div class="layout">
        <div class="board-wrap">
            <div id="board" class="board"></div>
            <div id="overlay" class="overlay">
                <h2 id="overTitle">GAME OVER</h2>
                <p id="overMsg"></p>
                <button id="restart" class="btn">▶ RESTART</button>
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
                <div class="label">CONTROLS</div>
                <div class="keys">
                    <b>↑↓←→</b> / <b>WASD</b> Slide<br>
                    <b>R</b> Restart
                </div>
            </div>
            <button id="restart2" class="btn">▶ NEW GAME</button>
            <a href="/" class="back">◀ BACK TO ARCADE</a>
        </div>
    </div>

<script>
(function () {
    const N = 4;
    const boardEl = document.getElementById('board');
    const scoreEl = document.getElementById('score');
    const bestEl  = document.getElementById('best');
    const overlay = document.getElementById('overlay');
    const overTitle = document.getElementById('overTitle');
    const overMsg = document.getElementById('overMsg');

    let grid, score = 0, best = 0, wonShown = false;

    function make() { return Array.from({length: N}, () => new Array(N).fill(0)); }
    function clone(g) { return g.map(r => r.slice()); }
    function empties(g) {
        const out = [];
        for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) if (!g[y][x]) out.push({x, y});
        return out;
    }
    function spawn(g) {
        const e = empties(g);
        if (!e.length) return;
        const {x, y} = e[Math.floor(Math.random() * e.length)];
        g[y][x] = Math.random() < 0.9 ? 2 : 4;
    }
    function slideRow(row) {
        const filtered = row.filter(v => v);
        let gained = 0;
        for (let i = 0; i < filtered.length - 1; i++) {
            if (filtered[i] === filtered[i+1]) {
                filtered[i] *= 2;
                gained += filtered[i];
                filtered.splice(i+1, 1);
            }
        }
        while (filtered.length < N) filtered.push(0);
        return {row: filtered, gained};
    }
    function rotate(g) {
        const out = make();
        for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) out[x][N - 1 - y] = g[y][x];
        return out;
    }
    function move(dir) {
        // Normalize to "left"
        let g = clone(grid);
        let rotations = {left: 0, up: 3, right: 2, down: 1}[dir];
        for (let i = 0; i < rotations; i++) g = rotate(g);
        let gained = 0, changed = false;
        for (let y = 0; y < N; y++) {
            const before = g[y].slice();
            const {row, gained: gg} = slideRow(g[y]);
            g[y] = row;
            gained += gg;
            for (let x = 0; x < N; x++) if (before[x] !== row[x]) changed = true;
        }
        for (let i = 0; i < (4 - rotations) % 4; i++) g = rotate(g);
        if (!changed) return false;
        grid = g;
        spawn(grid);
        score += gained;
        if (score > best) best = score;
        render();
        checkEnd();
        return true;
    }
    function canMove() {
        if (empties(grid).length) return true;
        for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {
            if (x + 1 < N && grid[y][x] === grid[y][x+1]) return true;
            if (y + 1 < N && grid[y][x] === grid[y+1][x]) return true;
        }
        return false;
    }
    function hasWon() {
        for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) if (grid[y][x] === 2048) return true;
        return false;
    }
    function checkEnd() {
        if (!wonShown && hasWon()) {
            wonShown = true;
            overlay.className = 'overlay win';
            overTitle.textContent = 'YOU WIN!';
            overMsg.textContent = 'You reached 2048  ·  Score: ' + score;
            overlay.style.display = 'flex';
            return;
        }
        if (!canMove()) {
            overlay.className = 'overlay lose';
            overTitle.textContent = 'GAME OVER';
            overMsg.textContent = 'Score: ' + score + '  ·  Best: ' + best;
            overlay.style.display = 'flex';
        }
    }
    function render() {
        boardEl.innerHTML = '';
        for (let y = 0; y < N; y++) {
            for (let x = 0; x < N; x++) {
                const v = grid[y][x];
                const c = document.createElement('div');
                c.className = 'cell';
                if (v) {
                    c.dataset.val = v;
                    c.textContent = v;
                    c.classList.add('pop');
                    setTimeout(() => c.classList.remove('pop'), 120);
                }
                boardEl.appendChild(c);
            }
        }
        scoreEl.textContent = score;
        bestEl.textContent = best;
    }
    function reset() {
        grid = make();
        score = 0;
        wonShown = false;
        spawn(grid); spawn(grid);
        overlay.style.display = 'none';
        render();
    }

    document.addEventListener('keydown', (e) => {
        const k = e.key.toLowerCase();
        const map = {
            'arrowup': 'up', 'w': 'up',
            'arrowdown': 'down', 's': 'down',
            'arrowleft': 'left', 'a': 'left',
            'arrowright': 'right', 'd': 'right'
        };
        if (k === 'r') { reset(); return; }
        const dir = map[k];
        if (!dir) return;
        e.preventDefault();
        if (overlay.style.display === 'flex' && overlay.classList.contains('lose')) return;
        move(dir);
    });
    document.getElementById('restart').addEventListener('click', reset);
    document.getElementById('restart2').addEventListener('click', reset);

    reset();
})();
</script>
</body>
</html>"""

sys.stdout.write("Content-Type: text/html; charset=utf-8\r\n\r\n")
sys.stdout.write(HTML)
sys.stdout.flush()
