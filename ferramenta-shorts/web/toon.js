export const INK = "#16121A"; /* v9: tinta mais profunda estilo Ricks Clips */
export const SKIN = "#ffe2c2";
const WHITE = "#ffffff";
const MOUTH = "#5a1e28";
const TONGUE = "#e86e78";
const SH_SKIN = [
    0.93,
    0.9,
    0.96
];   // sombra LAVANDA no rosto (medido no canal: ~0,93/0,90/0,95; antes pessego)
const SH_CLOTH = [
    0.64,
    0.66,
    0.74
];
const SH_FELT = [
    0.62,
    0.62,
    0.7
];
const rad = (d)=>d * Math.PI / 180;
const clamp = (x, a, b)=>Math.max(a, Math.min(b, x));
export const mul = (c, m)=>{
    c = (typeof c === 'string' && c[0] === '#') ? c : '#8a8f98';   /* cor faltando no figurino nao derruba o render */
    const n = parseInt(c.slice(1), 16);
    const ch = (v, k)=>Math.min(255, Math.round(v * k)).toString(16).padStart(2, "0");
    return `#${ch(n >> 16 & 255, m[0])}${ch(n >> 8 & 255, m[1])}${ch(n & 255, m[2])}`;
};
export const shade = (c, k)=>mul(c, [
        k,
        k,
        k
    ]);
export const mix = (a, b, t)=>{
    a = (typeof a === 'string' && a[0] === '#') ? a : '#8a8f98'; b = (typeof b === 'string' && b[0] === '#') ? b : '#8a8f98';
    const A = parseInt(a.slice(1), 16), B = parseInt(b.slice(1), 16);
    const ch = (s)=>Math.round((A >> s & 255) * (1 - t) + (B >> s & 255) * t).toString(16).padStart(2, "0");
    return `#${ch(16)}${ch(8)}${ch(0)}`;
};
const rnd = (seed, k)=>{
    const x = Math.sin(seed * 127.1 + k * 311.7) * 43758.5453;
    return x - Math.floor(x);
};
const rotPts = (pts, a, cx, cy)=>pts.map(([x, y])=>[
            cx + (x - cx) * Math.cos(a) - (y - cy) * Math.sin(a),
            cy + (x - cx) * Math.sin(a) + (y - cy) * Math.cos(a)
        ]);
const rotAbout = (q, a, c)=>rotPts([
        q
    ], a, c[0], c[1])[0];
const lerp2 = (a, b, t)=>[
        a[0] + (b[0] - a[0]) * t,
        a[1] + (b[1] - a[1]) * t
    ];
const curve = (a, k, b, n = 10)=>{
    const c = [
        2 * k[0] - (a[0] + b[0]) / 2,
        2 * k[1] - (a[1] + b[1]) / 2
    ], out = [];
    for(let i = 0; i <= n; i++){
        const t = i / n, s = 1 - t;
        out.push([
            s * s * a[0] + 2 * s * t * c[0] + t * t * b[0],
            s * s * a[1] + 2 * s * t * c[1] + t * t * b[1]
        ]);
    }
    return out;
};
export const RIFLEMAN = {
    jacket: "#357650",
    pants: "#3d4440",
    boots: INK,
    hat: "shako",
    belt: "#f1efe6",
    buttons: "#d9dde0",
    rifle: true
};
export const OFFICER = {
    ...RIFLEMAN,
    hat: "shako_tall",
    buttons: "#e8c45a",
    sash: "#c0353a",
    sword: true,
    moustache: "#4a3020",
    rifle: false,
    belt: null,
    build: "stout"
};
export const KID = {
    jacket: "#f08a2c",
    pants: "#3b5b9a",
    boots: "#f4f1ea",
    hat: "cap",
    cap: "#e2453c",
    build: "kid"
};
export const PARENT = {
    jacket: "#7b5ac9",
    pants: "#3b3f52",
    boots: "#5a3b2a",
    hat: "hair",
    hair: "#5a3b2a"
};
export const SKINS = [
    SKIN,
    "#f5c9a0",
    "#ecd0b6",
    "#c99067"
];
export const soldier = (v = 0, extra = {})=>{
    const o = {
        ...RIFLEMAN,
        skin: SKINS[v % 4]
    };
    if (v % 4 === 1) o.moustache = "#4a3426";
    if (v % 4 === 3) o.moustache = "#2a201a";
    return {
        ...o,
        ...extra
    };
};
export const townsfolk = (v = 0)=>{
    const coats = [
        "#3f6fb5",
        "#8c3b4a",
        "#5d7a3a",
        "#b5653f",
        "#2f5f6a",
        "#7b5ac9"
    ];
    const o = {
        jacket: coats[v % 6],
        pants: "#3b3f52",
        boots: "#4a3426",
        skin: SKINS[v % 4]
    };
    return v % 2 ? {
        ...o,
        hat: "bonnet",
        dress: [
            "#d9a441",
            "#c25a7a",
            "#5a8fc2"
        ][v % 3]
    } : {
        ...o,
        hat: "tophat"
    };
};
export class Pen {
    g;
    ol = 12;
    rot = null;
    constructor(g){
        this.g = g;
    }
    P(x, y) {
        if (!this.rot) return [
            x,
            y
        ];
        const r = this.rot, a = r[0], cx = r[1], cy = r[2], dx = r.length > 3 ? r[3] : 0, dy = r.length > 4 ? r[4] : 0, c = Math.cos(a), s = Math.sin(a);
        return [
            cx + (x - cx) * c - (y - cy) * s + dx,
            cy + (x - cx) * s + (y - cy) * c + dy
        ];
    }
    path(pts, close) {
        const g = this.g;
        g.beginPath();
        pts.forEach((p, i)=>{
            const [x, y] = this.P(p[0], p[1]);
            if (i) g.lineTo(x, y);
            else g.moveTo(x, y);
        });
        if (close) g.closePath();
    }
    poly(pts, fill, ol) {
        const g = this.g, w = ol ?? this.ol;
        this.path(pts, true);
        if (fill) {
            g.fillStyle = fill;
            g.fill();
        }
        if (w) {
            g.lineWidth = w;
            g.strokeStyle = INK;
            g.lineJoin = "round";
            g.stroke();
        }
    }
    ell(cx, cy, rx, ry, fill, ol, a0 = 0, a1 = 360, rot = 0) {
        this.poly(ellPts(cx, cy, rx, ry, a0, a1, rot), fill, ol);
    }
    line(pts, fill, w, ink = true) {
        const g = this.g;
        g.lineCap = "round";
        g.lineJoin = "round";
        if (ink) {
            this.path(pts, false);
            g.strokeStyle = INK;
            g.lineWidth = w + 2 * this.ol * 0.9;
            g.stroke();
        }
        this.path(pts, false);
        g.strokeStyle = fill;
        g.lineWidth = w;
        g.stroke();
    }
    stroke(pts, w, fill = INK) {
        const g = this.g;
        g.lineCap = "round";
        g.lineJoin = "round";
        this.path(pts, false);
        g.strokeStyle = fill;
        g.lineWidth = w;
        g.stroke();
    }
    arc(cx, cy, rx, ry, a0, a1, w, fill = INK) {
        const pts = [];
        for(let i = 0; i <= 24; i++)pts.push([
            cx + rx * Math.cos(rad(a0 + (a1 - a0) * i / 24)),
            cy + ry * Math.sin(rad(a0 + (a1 - a0) * i / 24))
        ]);
        this.stroke(pts, w, fill);
    }
    dot(cx, cy, r, fill = INK) {
        const [x, y] = this.P(cx, cy);
        this.g.beginPath();
        this.g.arc(x, y, r, 0, Math.PI * 2);
        this.g.fillStyle = fill;
        this.g.fill();
    }
    clip(pts, fn) {
        const g = this.g;
        g.save();
        this.path(pts, true);
        g.clip();
        fn();
        g.restore();
    }
    shadedFill(pts, base, shadow, light, R, shift = 0.45, r0 = 1.05, r1 = 1.25) {
        if (typeof base !== 'string') base = '#6b4a2a'; if (typeof shadow !== 'string') shadow = mul(base, 0.75);   /* cor faltando no figurino (cabelo/chapeu) nao derruba o render */
        const g = this.g, n = pts.length;
        let cx = 0, cy = 0;
        for (const [x, y] of pts){
            cx += x / n;
            cy += y / n;
        }
        const [gx, gy] = this.P(cx + Math.cos(light) * shift * R, cy + Math.sin(light) * shift * R);
        const gr = g.createRadialGradient(gx, gy, 0, gx, gy, r1 * R);
        gr.addColorStop(0, base);
        gr.addColorStop(r0 / r1, base);
        gr.addColorStop(1, shadow);
        this.path(pts, true);
        g.fillStyle = gr;
        g.fill();
    }
    gradFill(pts, base, shadow, light, flat = 0.36) {
        const g = this.g, dx = Math.cos(light), dy = Math.sin(light), n = pts.length;
        let cx = 0, cy = 0, lo = Infinity, hi = -Infinity;
        for (const [x, y] of pts){
            cx += x / n;
            cy += y / n;
            const d = x * dx + y * dy;
            lo = Math.min(lo, d);
            hi = Math.max(hi, d);
        }
        const dc = cx * dx + cy * dy;
        const [ax, ay] = this.P(cx + dx * (hi - dc), cy + dy * (hi - dc)), [bx, by] = this.P(cx + dx * (lo - dc), cy + dy * (lo - dc));
        const gr = g.createLinearGradient(ax, ay, bx, by);
        gr.addColorStop(0, base);
        gr.addColorStop(flat, base);
        gr.addColorStop(Math.min(0.95, flat + 0.32), mix(base, shadow, 0.35));
        gr.addColorStop(1, shadow);
        this.path(pts, true);
        g.fillStyle = gr;
        g.fill();
    }
    inkRing(pts, w0, thick, k = 0.38, col = INK) /* v9: razao fino/grosso ~3x */ {
        const n = pts.length;
        let cx = 0, cy = 0;
        for (const [x, y] of pts){
            cx += x / n;
            cy += y / n;
        }
        const out = [], inn = [];
        pts.forEach((q, i)=>{
            const a = pts[(i + n - 1) % n], b = pts[(i + 1) % n];
            let nx = b[1] - a[1], ny = a[0] - b[0];
            const l = Math.hypot(nx, ny) || 1;
            nx /= l;
            ny /= l;
            const h = 0.5 * w0 * (1 + k * Math.cos(Math.atan2(q[1] - cy, q[0] - cx) - thick));
            out.push([
                q[0] + nx * h,
                q[1] + ny * h
            ]);
            inn.push([
                q[0] - nx * h,
                q[1] - ny * h
            ]);
        });
        const g = this.g;
        const trace = (r)=>{
            r.forEach(([x0, y0], i)=>{
                const [x, y] = this.P(x0, y0);
                if (i) g.lineTo(x, y);
                else g.moveTo(x, y);
            });
            g.closePath();
        };
        g.beginPath();
        trace(out);
        trace(inn.reverse());
        g.fillStyle = col;
        g.fill("evenodd");
    }
    band(pts, fill, w, rim, cap = "butt") {
        const g = this.g;
        g.lineCap = cap;
        g.lineJoin = "round";
        this.path(pts, false);
        g.strokeStyle = INK;
        g.lineWidth = w + 2 * rim;
        g.stroke();
        this.path(pts, false);
        g.strokeStyle = fill;
        g.lineWidth = w;
        g.stroke();
        g.lineCap = "round";
    }
}
const ellPts = (cx, cy, rx, ry, a0 = 0, a1 = 360, rot = 0, n = 48)=>{
    const r = rad(rot), pts = [];
    for(let i = 0; i <= n; i++){
        const a = rad(a0 + (a1 - a0) * i / n), x = rx * Math.cos(a), y = ry * Math.sin(a);
        pts.push([
            cx + x * Math.cos(r) - y * Math.sin(r),
            cy + x * Math.sin(r) + y * Math.cos(r)
        ]);
    }
    return pts;
};
const rrect = (x0, y0, x1, y1, r, n = 8)=>{
    const pts = [];
    for (const [cx, cy, a] of [
        [
            x1 - r,
            y0 + r,
            -90
        ],
        [
            x1 - r,
            y1 - r,
            0
        ],
        [
            x0 + r,
            y1 - r,
            90
        ],
        [
            x0 + r,
            y0 + r,
            180
        ]
    ])for(let i = 0; i <= n; i++)pts.push([
        cx + r * Math.cos(rad(a + 90 * i / n)),
        cy + r * Math.sin(rad(a + 90 * i / n))
    ]);
    return pts;
};
const taper = (p, a, b, wa, wb, col = INK)=>{
    const dx = b[0] - a[0], dy = b[1] - a[1], l = Math.hypot(dx, dy) || 1, nx = -dy / l, ny = dx / l;
    p.poly([
        [
            a[0] + nx * wa / 2,
            a[1] + ny * wa / 2
        ],
        [
            b[0] + nx * wb / 2,
            b[1] + ny * wb / 2
        ],
        [
            b[0] - nx * wb / 2,
            b[1] - ny * wb / 2
        ],
        [
            a[0] - nx * wa / 2,
            a[1] - ny * wa / 2
        ]
    ], col, 0);
    p.dot(a[0], a[1], wa / 2, col);
    p.dot(b[0], b[1], wb / 2, col);
};
export const blobPts = (cx, cy, B, n = 72)=>{
    const ph = [
        rnd(B.seed, 11),
        rnd(B.seed, 12),
        rnd(B.seed, 13)
    ].map((v)=>v * Math.PI * 2);
    const pts = [];
    for(let i = 0; i < n; i++){
        const t = i / n * Math.PI * 2, c = Math.cos(t), s = Math.sin(t), e = 2 / (s < 0 ? B.nTop : B.nBot);
        let X = Math.sign(c) * Math.abs(c) ** e;
        const Y = Math.sign(s) * Math.abs(s) ** e;
        X *= (1 + B.egg * Y) * (1 + B.asym * Math.sign(X));
        const r = 1 + B.noise * (Math.cos(2 * t + ph[0]) + 0.7 * Math.cos(3 * t + ph[1]) + 0.5 * Math.cos(4 * t + ph[2]));
        const x = B.a * X * r, y = B.b * Y * r;
        pts.push([
            cx + x * Math.cos(B.rot) - y * Math.sin(B.rot),
            cy + x * Math.sin(B.rot) + y * Math.cos(B.rot)
        ]);
    }
    return pts;
};
export const headBlob = (seed, a = 144, facing = 0)=>({
        /* v10-final: cabeca redonda limpa e grande estilo @RicksClips3000 */
        a,
        b: a * (0.985 + 0.02 * (rnd(seed, 1) - 0.5)),
        nTop: 2.02,
        nBot: 2.04,
        egg: -0.02,
        asym: 0.012 * (facing || 1),
        rot: rad(1.5 * (rnd(seed, 7) - 0.5)),
        noise: 0.002,
        seed
    });
export const thickAngle = (light)=>Math.atan2(-Math.sin(light) + 0.8, -Math.cos(light));
const DEF_LIGHT = rad(-120);
const FACE = {
    neutral: {
        eye: [
            "lid",
            "lid"
        ],
        brow: [
            0,
            -1
        ],
        mouth: "dash"
    },
    stern: {
        eye: [
            "lid",
            "lid"
        ],
        brow: [
            3,
            -2
        ],
        mouth: "frown"
    },
    grin: {
        eye: [
            "happy",
            "happy"
        ],
        brow: [
            -3,
            -3
        ],
        mouth: "grin"
    },
    laugh: {
        eye: [
            "squeeze",
            "squeeze"
        ],
        brow: [
            -4,
            -4
        ],
        mouth: "laugh"
    },
    whistle: {
        eye: [
            "dash",
            "dash"
        ],
        brow: [
            -2,
            -4
        ],
        mouth: "o"
    },
    nervous: {
        eye: [
            "small",
            "small"
        ],
        brow: [
            -3,
            2
        ],
        mouth: "wave"
    },
    shock: {
        eye: [
            "shock",
            "shock"
        ],
        brow: [
            -7,
            -6
        ],
        mouth: "O"
    },
    relief: {
        eye: [
            "happy",
            "happy"
        ],
        brow: [
            -2,
            1
        ],
        mouth: "smileWide"
    },
    relief_open: {
        eye: [
            "happy",
            "happy"
        ],
        brow: [
            -2,
            1
        ],
        mouth: "grin"
    },
    dazed: {
        eye: [
            "spiral",
            "spiral"
        ],
        brow: [
            -3,
            2
        ],
        mouth: "wave"
    },
    pained: {
        eye: [
            "squeeze",
            "lid"
        ],
        brow: [
            -3,
            2
        ],
        mouth: "teeth"
    },
    smile: {
        eye: [
            "dot",
            "dot"
        ],
        brow: [
            0,
            -1
        ],
        mouth: "smirk"
    },
    smile_closed: {
        eye: [
            "happy",
            "happy"
        ],
        brow: [
            0,
            -1
        ],
        mouth: "smile"
    },
    lick: {
        eye: [
            "dot",
            "dot"
        ],
        brow: [
            0,
            -1
        ],
        mouth: "lick"
    }
};
/* EXPRESSOES NOVAS (19/11, ordem do Gibson: "ver na cara do personagem"): preocupado, suplicando, insatisfeito, determinado, desconfiado forte, alegre */
Object.assign(FACE, {
    worried: { eye: ["dot", "dot"], brow: [-7, 6], mouth: "frown" },
    pleading: { eye: ["dot", "dot"], brow: [-8, 7], mouth: "o" },
    annoyed: { eye: ["lid", "lid"], brow: [5, -4], mouth: "frown" },
    determined: { eye: ["dot", "dot"], brow: [5, -4], mouth: "smirk" },
    distrust: { eye: ["slit", "lid"], brow: [4, -6], mouth: "smirk" },
    happy: { eye: ["happy", "happy"], brow: [-2, 0], mouth: "smileWide" }
});
const halfLid = (k)=>k === "dot" || k === "small" ? "lid" : k === "lid" ? "slit" : k === "shock" ? "shockHalf" : k;
const eyeKind = (k, lid)=>lid >= 1 && k !== "happy" && k !== "squeeze" && k !== "spiral" ? "dash" : lid > 0 ? halfLid(k) : k;
const lidOf = (b)=>b === true ? 1 : Number(b) || 0;
const eye = (p, kind, x, ey, u, side, look, skin)=>{
    const lx = x + look * 3 * u, lw = 3.8 * u;
    switch(kind){
        case "dot":
            p.ell(lx, ey, 5.2 * u, 6.8 * u, INK, 0);
            p.ell(lx - 1.5 * u, ey - 2.0 * u, 1.4 * u, 1.4 * u, "#ffffff", 0);
            break;
        case "small":
            p.ell(lx, ey, 4.2 * u, 5.6 * u, INK, 0);
            break;
        case "lid":
            p.ell(lx, ey - u, 7 * u, 6 * u, INK, 0, 0, 180);
            p.stroke([
                [
                    x - 9 * u,
                    ey - u
                ],
                [
                    x + 9 * u,
                    ey - u
                ]
            ], lw);
            break;
        case "slit":
            p.ell(lx, ey, 7 * u, 2.6 * u, INK, 0, 0, 180);
            p.stroke([
                [
                    x - 9 * u,
                    ey
                ],
                [
                    x + 9 * u,
                    ey
                ]
            ], lw);
            break;
        case "happy":
            p.arc(x, ey + 3 * u, 8 * u, 6 * u, 200, 340, lw);
            break;
        case "dash":
            p.stroke([
                [
                    x - 8.5 * u,
                    ey
                ],
                [
                    x + 8.5 * u,
                    ey
                ]
            ], lw);
            break;
        case "squeeze":
            p.stroke([
                [
                    x + 6 * u * side,
                    ey - 5 * u
                ],
                [
                    x - 6 * u * side,
                    ey
                ],
                [
                    x + 6 * u * side,
                    ey + 5 * u
                ]
            ], lw);
            break;
        case "shock":
        case "shockHalf":
            p.ell(x, ey, 11 * u, 11 * u, WHITE, 2.6 * u);
            p.dot(lx - side * 1.5 * u, ey + 1.5 * u, 3 * u);
            if (kind === "shockHalf") {
                p.ell(x, ey, 11 * u, 11 * u, skin, 0, 180, 360);
                p.stroke([
                    [
                        x - 11 * u,
                        ey
                    ],
                    [
                        x + 11 * u,
                        ey
                    ]
                ], 2.6 * u);
            }
            break;
        default:
            {
                const s = [];
                for(let t = 1; t < 15; t++)s.push([
                    x + Math.cos(t * 0.9) * t * 0.55 * u,
                    ey + Math.sin(t * 0.9) * t * 0.55 * u
                ]);
                p.stroke(s, 2.4 * u);
            }
    }
};
const dmouth = (p, mx, y, rx, ry, u, tongue = false)=>{
    p.ell(mx, y, rx, ry, MOUTH, 0, 0, 180);
    p.clip([
        [
            mx - rx,
            y
        ],
        [
            mx + rx,
            y
        ],
        [
            mx + rx,
            y + 3 * u
        ],
        [
            mx - rx,
            y + 3 * u
        ]
    ], ()=>p.ell(mx, y, rx, ry, WHITE, 0, 0, 180));
    if (tongue) p.ell(mx + 2 * u, y + 0.62 * ry, 0.4 * rx, 0.28 * ry, TONGUE, 0);
    p.ell(mx, y, rx, ry, null, 3 * u, 0, 180);
};
const mouth = (p, kind, mx, my, u, k = 1)=>{
    const mw = 4 * u;
    switch(kind){
        case "dash":
            p.stroke([
                [
                    mx - 5.5 * u * k,
                    my
                ],
                [
                    mx + 5.5 * u * k,
                    my - 0.8 * u
                ]
            ], mw);
            break;
        case "frown":
            p.arc(mx, my + 3 * u, 6.5 * u * k, 3.5 * u, 200, 340, mw);
            break;
        case "smirk":
            p.arc(mx + u, my - 3 * u, 7 * u * k, 4 * u, 10, 150, mw);
            break;
        case "smile":
            p.arc(mx, my - 3 * u, 8 * u * k, 4.5 * u, 20, 160, mw);
            break;
        case "smileWide":
            p.arc(mx, my - 4 * u, 11 * u * k, 6 * u, 15, 165, mw);
            break;
        case "grin":
            dmouth(p, mx, my - u, 12 * u * k, 8 * u, u);
            break;
        case "laugh":
            dmouth(p, mx, my, 16 * u * k, 11 * u, u, true);
            break;
        case "o":
            p.ell(mx + 4 * u, my, 3.5 * u, 4 * u, MOUTH, 2.8 * u);
            break;
        case "O":
            p.ell(mx, my + 2 * u, 9 * u * k, 11 * u, MOUTH, 3.2 * u);
            break;
        case "wave":
            {
                const s = [];
                for(let i = 0; i <= 12; i++)s.push([
                    mx - 9 * u * k + i * 1.5 * u * k,
                    my + 1.5 * u * Math.sin(i * 1.3)
                ]);
                p.stroke(s, 3 * u);
                break;
            }
        case "teeth":
            p.poly([
                [
                    mx - 12 * u * k,
                    my - 4 * u
                ],
                [
                    mx + 12 * u * k,
                    my - 4 * u
                ],
                [
                    mx + 11 * u * k,
                    my + 4 * u
                ],
                [
                    mx - 11 * u * k,
                    my + 4 * u
                ]
            ], WHITE, 3 * u);
            for (const j of [
                -1,
                0,
                1
            ])p.stroke([
                [
                    mx + j * 6 * u * k,
                    my - 4 * u
                ],
                [
                    mx + j * 6 * u * k,
                    my + 4 * u
                ]
            ], 1.5 * u);
            break;
        case "snarl": {   /* RAIVA: dentes cerrados com os cantos da boca para BAIXO (nao parece sorriso) */
            const T = [[mx - 12 * u * k, my + 1 * u], [mx - 6 * u * k, my - 3 * u], [mx + 6 * u * k, my - 3 * u], [mx + 12 * u * k, my + 1 * u], [mx + 11 * u * k, my + 6 * u], [mx + 5 * u * k, my + 3 * u], [mx - 5 * u * k, my + 3 * u], [mx - 11 * u * k, my + 6 * u]];
            p.poly(T, WHITE, 3 * u);
            p.stroke([[mx - 11 * u * k, my + 2.5 * u], [mx - 5 * u * k, my], [mx + 5 * u * k, my], [mx + 11 * u * k, my + 2.5 * u]], 1.5 * u);
            for (const j of [-1, 0, 1]) p.stroke([[mx + j * 5 * u * k, my - 3 * u], [mx + j * 5 * u * k, my + 3 * u]], 1.5 * u);
            break; }
        case "lick":
            p.arc(mx, my - 3 * u, 8 * u * k, 4.5 * u, 20, 160, mw);
            p.ell(mx + 6 * u * k, my + 3 * u, 3.6 * u, 4.6 * u, TONGUE, 2.4 * u);
            break;
    }
};
/* EXPRESSOES EMOCIONAIS extras (montadas com os olhos/bocas existentes): raiva, grito, tristeza, choro, convencido, surpresa, medo, desconfianca, tedio */
Object.assign(FACE, { angry: { eye: ["slit", "slit"], brow: [9, -5], mouth: "snarl" }, shout: { eye: ["lid", "lid"], brow: [7, -4], mouth: "O" }, sad: { eye: ["lid", "lid"], brow: [-5, 3], mouth: "frown" }, cry: { eye: ["squeeze", "squeeze"], brow: [-5, 3], mouth: "wave" },
    smug: { eye: ["happy", "lid"], brow: [-3, 2], mouth: "smirk" }, surprised: { eye: ["shock", "shock"], brow: [-6, -6], mouth: "o" }, scared: { eye: ["shock", "shock"], brow: [-5, 3], mouth: "wave" }, suspicious: { eye: ["slit", "slit"], brow: [3, -2], mouth: "dash" }, bored: { eye: ["slit", "slit"], brow: [0, 0], mouth: "dash" } });
const faceFront = (p, cx, cy, W, expr, facing, look, lid, brim, skin, moustache, stout = false, AX = {})=>{
    const u = W / 100, F = FACE[expr] || FACE.neutral, fx = cx + 7 * u * facing;
    /* ROSTO INDIVIDUAL: cada personagem tem seus tracos (distancia e altura dos olhos, sobrancelha, bochecha, sardas, pinta, olheira) */
    const FT = [{}, { gap: 2.5, bt: 1.6, bl: 1.5 }, { gap: -2, ey: 2, cheeks: 1 }, { gap: 1, bt: -1.2, freck: 1 }, { gap: -1, ey: -2, bt: 2.2, bags: 1 }, { gap: 3.5, ey: 1, mole: 1 }, { gap: 0, bt: -1.6, cheeks: 1, bl: -1.5 }, { gap: -2.5, ey: -1, bt: 1, freck: 1, mole: -1 }][(AX.face ?? 0) % 8];
    const ex = ((F.eye[0] === "shock" ? 15.5 : 16.5) + (FT.gap || 0) * 0.8) * u   /* olhos mais afastados (pedido do Gibson) */, ey = cy + (FT.ey || 0) * u;
    if (FT.cheeks) for (const sd of [-1, 1]) p.ell(fx + sd * (ex + 9 * u), ey + 13 * u, 7 * u, 4.5 * u, "#f6b3a8", 0);
    if (FT.freck) for (const sd of [-1, 1]) for (const [qx, qy] of [[5, 9], [10, 11.5], [14, 8.5]]) p.ell(fx + sd * (ex - 4 * u + qx * u), ey + qy * u, 1.1 * u, 1.1 * u, "#b9785a", 0);
    if (FT.mole) p.ell(fx + FT.mole * (ex + 6 * u), ey + 17 * u, 1.7 * u, 1.7 * u, "#3a2a22", 0);
    for (const side of [
        -1,
        1
    ]){
        const x = fx + side * ex;
        const kind = eyeKind(F.eye[(facing ? side === facing : side > 0) ? 1 : 0], lid);
        eye(p, kind, x, ey + (AX.lookY || 0) * 2.4 * u, u, side, look, skin);
        const sk = (AX.skeptic && (facing ? side === facing : side > 0)) ? -3.2 : 0;
        const dI = F.brow[0] + (AX.bI || 0), dO = F.brow[1] + (AX.bO || 0), by = ey - (brim ? 17 : 20) * u + ((AX.browUp || 0) + sk) * u;
        if (kind === "shock" || kind === "shockHalf") p.arc(x, by - 6 * u, 9 * u, 3 * u, 200, 340, 4 * u);
        else taper(p, [
            x - side * (8.5 + (FT.bl || 0)) * u,
            by + dI * u
        ], [
            x + side * (8.5 + (FT.bl || 0)) * u,
            by + dO * u
        ], (6.8 + (FT.bt || 0)) * u, (4.6 + (FT.bt || 0) * 0.5) * u);
        if (FT.bags) p.arc(x, ey + 7 * u, 7 * u, 3 * u, 20, 160, 1.3 * u);
    }
    const mx = cx + 8 * u * facing, my = cy + 20 * u;
    if ((AX.talk || 0) > 0.05) { const a = AX.talk; dmouth(p, mx, my - 2 * u, (7 + 5 * a) * u, (2.2 + 9 * a) * u, u, a > 0.7); }
    else mouth(p, F.mouth, mx, my, u);
    if (moustache) for (const s of [
        -1,
        1
    ])taper(p, [
        mx + s * 1.5 * u,
        cy + 12.5 * u
    ], [
        mx + s * (stout ? 19 : 15) * u,
        cy + (stout ? 10.5 : 15) * u
    ], stout ? 5.5 * u : 4.5 * u, 1.6 * u, moustache);
    if (AX.beard) { p.arc(mx, cy + 14 * u, 30 * u, 26 * u, 15, 165, 13 * u, AX.beard); p.arc(mx, cy + 22 * u, 20 * u, 18 * u, 25, 155, 10 * u, AX.beard); }   // barba cheia (variedade de personagem)
    if (AX.glasses) { for (const sd of [-1, 1]) p.arc(fx + sd * ex, ey, 12.5 * u, 12.5 * u, 0, 360, 2.6 * u); p.arc(fx, ey, ex - 12.5 * u, 3 * u, 200, 340, 2.4 * u); }   // oculos redondos
    if (expr === "nervous" || AX.sweat) p.ell(cx + 40 * u * (facing || 1), cy - 22 * u + (AX.sweatY || 0) * u, 3.6 * u, 6.2 * u, "#9fd4ff", 2.2 * u);
    if (expr === "angry" || expr === "shout") {
      const vx = cx + 38 * u * (facing || 1), vy = cy - 30 * u;
      p.stroke([[vx - 6 * u, vy - 5 * u], [vx - 2 * u, vy - 1 * u], [vx - 6 * u, vy + 3 * u]], 2.4 * u, "#d93829");
      p.stroke([[vx + 5 * u, vy - 5 * u], [vx + 1 * u, vy - 1 * u], [vx + 5 * u, vy + 3 * u]], 2.4 * u, "#d93829");
      if (AX.rage) {
        for (const sd of [-1, 1]) {
          const px_ = cx + sd * 62 * u, py_ = cy - 12 * u;
          p.ell(px_, py_, 13 * u, 10 * u, "#ffffff", 2.2 * u);
          p.ell(px_ + sd * 11 * u, py_ - 5 * u, 9 * u, 8 * u, "#ffffff", 2.0 * u);
          p.ell(px_ + sd * 6 * u, py_ + 6 * u, 8 * u, 7 * u, "#ffffff", 1.8 * u);
        }
      }
    }
    if (expr === "cry") for (const sd of [-1, 1]) { const tx = fx + sd * (ex + 2 * u);   /* CHORO: lagrimas escorrendo dos dois olhos */
        p.stroke([[tx, ey + 5 * u], [tx + sd * 1.5 * u, ey + 13 * u], [tx + sd * 1 * u, ey + 20 * u]], 3.4 * u, "#6fc3ff");
        p.ell(tx + sd * 1 * u, ey + 22 * u, 2.6 * u, 3.4 * u, "#6fc3ff", 1.2 * u); }
};
const faceSide = (p, hx, hy, W, expr, lid, brim, skin, moustache, stout = false)=>{
    const u = W / 100, F = FACE[expr] || FACE.neutral, ex = hx + 27 * u, ey = hy;
    const kind = eyeKind(F.eye[1], lid);
    eye(p, kind, ex, ey, u, 1, 0.6, skin);
    const by = ey - (brim ? 17 : 20) * u, [dI, dO] = F.brow;
    if (kind === "shock" || kind === "shockHalf") p.arc(ex, by - 6 * u, 9 * u, 3 * u, 200, 340, 4 * u);
    else taper(p, [
        ex + 8 * u,
        by + dI * u
    ], [
        ex - 7 * u,
        by - u + dO * u
    ], 5 * u, 2.5 * u);
    p.stroke([
        [
            hx + 44 * u,
            hy + 4 * u
        ],
        [
            hx + 47.5 * u,
            hy + 9 * u
        ],
        [
            hx + 43 * u,
            hy + 10 * u
        ]
    ], 3 * u);
    mouth(p, F.mouth, hx + 33 * u, hy + 21 * u, u, 0.62);
    if (moustache) taper(p, [
        hx + 41 * u,
        hy + 13.5 * u
    ], [
        hx + 25 * u,
        hy + (stout ? 11.5 : 16) * u
    ], stout ? 5.5 * u : 4.5 * u, 1.6 * u, moustache);
    if (expr === "nervous") p.ell(hx - 30 * u, hy - 24 * u, 3 * u, 5 * u, "#9fd4ff", 2 * u);
};
const BONNET = "#e9cf8f", BONNET_BRIM = "#d6b46a";
const hatBehind = (p, o, H, cx, hc, light, thick, ow, side)=>{
    if (o.hat === "hair" && (o.hairStyle === "long" || o.hairStyle === "bun")) {
        const u2 = H.a / 50, lg = o.hairStyle === "long";
        const hb = blobPts(cx - (side ? 10 : 0) * u2, hc + (lg ? 0.2 : -0.62) * 2 * H.b * (lg ? 1 : 1), { ...H, a: H.a * (lg ? 1.14 : 0.42), b: H.b * (lg ? 1.25 : 0.36), asym: 0, egg: 0, seed: H.seed + 5 });
        p.shadedFill(hb, o.hair, mul(o.hair, SH_FELT), light, H.a * 1.1); p.inkRing(hb, ow * 0.85, thick); return;
    }
    if (o.hat !== "bonnet") return;
    const bb = blobPts(cx - (side ? 12 : 0) * (H.a / 50), hc - 0.07 * 2 * H.b, {
        ...H,
        a: H.a * 1.17,
        b: H.b * 1.13,
        asym: 0,
        egg: 0.04,
        seed: H.seed + 3
    });
    p.shadedFill(bb, BONNET, mul(BONNET, SH_CLOTH), light, H.a * 1.17);
    p.inkRing(bb, ow * 0.85, thick);
};
const hatOn = (p, o, hp, H, cx, hc, light, seed, facing, side)=>{
    const HS = o.hat === 'hair' || o.hat === 'bonnet' ? 1 : 1.2;   /* chapeu 20% maior e mais enterrado na cabeca (ficava pequeno e pousado em cima) */
    const W = 2 * H.a * HS, HH = 2 * H.b, u = W / 100, crown = hc - H.b + (HS > 1 ? 5.5 * u : 0), ow = 0.85 * 5 * u / HS;
    const a = H.rot + rad(4 * (rnd(seed, 20) - 0.5));
    const R = (pts)=>rotPts(pts, a, cx, hc);
    const sag = (yb, wb)=>{
        const base = [];
        for(let i = 0; i <= 12; i++){
            const t = i / 12;
            base.push([
                cx + wb * (2 * t - 1),
                yb + 3 * u * (1 - (2 * t - 1) ** 2)
            ]);
        }
        return base;
    };
    if (o.hat === "shako" || o.hat === "shako_tall") {
        const tall = o.hat === "shako_tall", yb = crown + 0.25 * HH, ht = (tall ? 0.66 : 0.56) * HH, wb = 46 * u, wt = 52 * u;
        const body = R([
            ...sag(yb, wb).reverse(),
            [
                cx - wt,
                yb - ht
            ],
            [
                cx + wt,
                yb - ht
            ]
        ]);
        p.shadedFill(body, "#3a3d47", "#24262d", light, wt, 0.4);
        if (tall) p.clip(body, ()=>p.band(R([
                [
                    cx - wt - 5 * u,
                    yb - ht + 0.07 * HH
                ],
                [
                    cx + wt + 5 * u,
                    yb - ht + 0.07 * HH
                ]
            ]), "#e8c45a", 0.06 * HH, 1.5 * u));
        p.poly(body, null, ow);
        const deg = a * 180 / Math.PI;
        if (side) {
            p.poly(R([
                [
                    cx + 36 * u,
                    yb - 1 * u
                ],
                [
                    cx + 60 * u,
                    yb + 8 * u
                ],
                [
                    cx + 34 * u,
                    yb + 6 * u
                ]
            ]), "#16171b", 2.5 * u);
            const [tx, ty] = R([
                [
                    cx + 24 * u,
                    yb - ht - 6 * u
                ]
            ])[0];
            p.ell(tx, ty, 7 * u, 7 * u, "#2b7a4b", 2.5 * u);
        } else {
            const [px, py] = R([
                [
                    cx + 3 * u * facing,
                    yb + 3 * u
                ]
            ])[0];
            p.ell(px, py, 34 * u, 0.045 * HH, "#16171b", 2.5 * u, 0, 180, deg);
            const [bx, by] = R([
                [
                    cx,
                    yb - 0.45 * ht
                ]
            ])[0];
            p.ell(bx, by, 7 * u, 6 * u, tall ? "#e8c45a" : "#c9ccd2", 2 * u, 0, 360, deg);
            p.arc(bx, by, 3.5 * u, 2.8 * u, 200, 500, 1.6 * u);
            const [tx, ty] = R([
                [
                    cx,
                    yb - ht - 6 * u
                ]
            ])[0];
            p.ell(tx, ty, 7 * u, 7 * u, "#2b7a4b", 2.5 * u);
        }
    } else if (o.hat === "cap" || o.hat === "hair") {
        const cut = crown + (o.hat === "cap" ? 0.22 : 0.42) * HH;
        const keep = (x, y)=>y < cut || side && o.hat === "hair" && x < cx - 6 * u && y < hc + 0.42 * H.b;
        const n = hp.length, startIdx = Math.max(0, hp.findIndex(([x, y], i)=>keep(x, y) && !keep(hp[(i + n - 1) % n][0], hp[(i + n - 1) % n][1])));
        const arc = [
            ...hp.slice(startIdx),
            ...hp.slice(0, startIdx)
        ].filter(([x, y])=>keep(x, y)).map(([x, y])=>[
                cx + (x - cx) * 1.03,
                hc + (y - hc) * 1.03
            ]);
        if (arc.length < 3) return;
        if (o.hat === "hair") {
            const [x0, y0] = arc[arc.length - 1], [x1, y1] = arc[0];
            for(let i = 1; i < 6; i++)arc.push([
                x0 + (x1 - x0) * i / 6,
                y0 + (y1 - y0) * i / 6 + (i % 2 ? 4 * u : 0)
            ]);
        }
        const col = o.hat === "cap" ? o.cap : o.hair;
        p.shadedFill(arc, col, mul(col, SH_FELT), light, H.a, 0.35);
        p.poly(arc, null, ow);
        if (o.hat === "hair") {
            const s = side ? -1 : facing || 1;
            p.stroke([
                [
                    cx + s * 10 * u,
                    cut - 30 * u
                ],
                [
                    cx + s * 2 * u,
                    cut - 12 * u
                ]
            ], 1.2 * u);
        }
        if (o.hat === "hair" && o.swoop) { const deg = a * 180 / Math.PI, f_ = facing || 1, q_ = R([[cx - 46 * u * f_, cut + 0.02 * HH], [cx - 40 * u * f_, cut - 0.2 * HH], [cx - 6 * u * f_, cut - 0.31 * HH], [cx + 34 * u * f_, cut - 0.26 * HH], [cx + 52 * u * f_, cut - 0.1 * HH], [cx + 30 * u * f_, cut - 0.13 * HH], [cx - 4 * u * f_, cut - 0.1 * HH], [cx - 30 * u * f_, cut - 0.02 * HH]]); p.shadedFill(q_, o.hair, shade(o.hair, 0.8), light, 50 * u, 0.4); p.poly(q_, null, ow); p.stroke(R([[cx - 30 * u * f_, cut - 0.15 * HH], [cx + 4 * u * f_, cut - 0.22 * HH], [cx + 36 * u * f_, cut - 0.17 * HH]]), 1.4 * u, shade(o.hair, 0.65)); }   /* TOPETE (Trump) */
        if (o.hat === "cap" && o.capBack) { const deg = a * 180 / Math.PI, [vx, vy] = R([[cx + 8 * u * (facing || 1), cut - 0.25 * HH]])[0]; p.ell(vx, vy, 30 * u, 0.075 * HH, shade(col, 0.75), ow, 180, 360, deg + 12 * (facing || 1)); p.stroke(R([[cx - 14 * u, cut - 0.02 * HH], [cx + 14 * u, cut - 0.02 * HH]]), 3 * u, shade(col, 0.6)); }   /* BONE VIRADO PARA TRAS (Bukele) */
        else if (o.hat === "cap") {
            const deg = a * 180 / Math.PI;
            if (side) p.poly(R([
                [
                    cx + 40 * u,
                    cut - 2 * u
                ],
                [
                    cx + 74 * u,
                    cut + 4 * u
                ],
                [
                    cx + 40 * u,
                    cut + 6 * u
                ]
            ]), shade(col, 0.8), ow);
            else {
                const s = facing || (rnd(seed, 21) < 0.5 ? -1 : 1), [px, py] = R([
                    [
                        cx + s * 4 * u,
                        cut + 1.5 * u
                    ]
                ])[0];
                p.ell(px, py, 32 * u, 0.06 * HH, shade(col, 0.8), ow, 0, 180, deg);
            }
        }
    } else if (o.hat === "tophat") {
        const yb = crown + 0.22 * HH, ht = 0.8 * HH, wb = 0.31 * W, wt = 0.33 * W, col = "#2e2a36";
        const body = R([
            ...sag(yb, wb).reverse(),
            [
                cx - wt,
                yb - ht
            ],
            [
                cx + wt,
                yb - ht
            ]
        ]);
        p.shadedFill(body, col, mul(col, SH_FELT), light, wt, 0.4);
        p.clip(body, ()=>p.band(R([
                [
                    cx - wt - 4 * u,
                    yb - 0.13 * HH
                ],
                [
                    cx + wt + 4 * u,
                    yb - 0.13 * HH
                ]
            ]), shade(o.jacket, 0.9), 0.14 * HH, 0.8 * u));
        p.poly(body, null, ow);
        const [bx, by] = R([
            [
                cx,
                yb + 1 * u
            ]
        ])[0];
        p.ell(bx, by, 0.45 * W, 0.05 * HH, "#1d1b22", ow, 0, 360, a * 180 / Math.PI);
    } else if (["helmet", "bowler", "straw", "slouch", "fez", "turban", "crown", "beret", "wizard", "tricorn", "bicorne", "kepi", "pickelhaube", "stahlhelm", "brodie", "adrian", "m1", "quepe", "colonial", "bibico", "boonie"].includes(o.hat)) {
        /* chapeus novos (canal: >=25 tipos). dome = meia elipse sobre a testa */
        const deg = a * 180 / Math.PI, yb = crown + 0.24 * HH;
        const dome = (y, w, h, n = 16)=>{ const q = []; for(let i = 0; i <= n; i++){ const t = Math.PI * i / n; q.push([cx - w * Math.cos(t), y - h * Math.sin(t)]); } return q; };
        const brimE = (y, w, h, col)=>{ const [bx, by] = R([[cx + (side ? 6 * u : 0), y]])[0]; p.ell(bx, by, w, h, col, ow, 0, 360, deg); };
        if (o.hat === "helmet") { const col = o.cap || "#5a6334"; const body = R([...sag(yb + 2 * u, 53 * u).reverse(), ...dome(yb + 2 * u, 53 * u, 0.36 * HH)]); p.shadedFill(body, col, mul(col, SH_FELT), light, 53 * u, 0.4); p.poly(body, null, ow); p.clip(body, ()=>p.band(R([[cx - 60 * u, yb - 3 * u], [cx + 60 * u, yb - 3 * u]]), shade(col, 0.72), 0.035 * HH, 0.8 * u)); }
        else if (o.hat === "bowler") { const col = o.cap || "#2e2a36"; const body = R([...sag(yb, 40 * u).reverse(), ...dome(yb, 40 * u, 0.4 * HH)]); brimE(yb + 2 * u, 0.6 * W, 0.045 * HH, shade(col, 0.8)); p.shadedFill(body, col, mul(col, SH_FELT), light, 40 * u, 0.4); p.poly(body, null, ow); p.clip(body, ()=>p.band(R([[cx - 46 * u, yb - 0.07 * HH], [cx + 46 * u, yb - 0.07 * HH]]), shade(o.jacket || "#8a3a3a", 0.9), 0.07 * HH, 0.8 * u)); }
        else if (o.hat === "straw" || o.hat === "slouch") { const col = o.cap || (o.hat === "straw" ? "#e6c66a" : "#8a7a50"); brimE(yb + 3 * u, (o.hat === "straw" ? 0.82 : 0.72) * W, 0.07 * HH, shade(col, 0.86)); const body = R([...sag(yb, 38 * u).reverse(), ...dome(yb, 38 * u, 0.3 * HH)]); p.shadedFill(body, col, mul(col, SH_FELT), light, 38 * u, 0.4); p.poly(body, null, ow); p.clip(body, ()=>p.band(R([[cx - 44 * u, yb - 0.05 * HH], [cx + 44 * u, yb - 0.05 * HH]]), o.hat === "straw" ? "#b5452f" : shade(col, 0.6), 0.06 * HH, 0.8 * u)); }
        else if (o.hat === "fez") { const col = o.cap || "#b3262d"; const body = R([...sag(yb, 34 * u).reverse(), [cx - 27 * u, yb - 0.44 * HH], [cx + 27 * u, yb - 0.44 * HH]]); p.shadedFill(body, col, mul(col, SH_FELT), light, 34 * u, 0.4); p.poly(body, null, ow); const [tx, ty] = R([[cx, yb - 0.44 * HH]])[0], [qx, qy] = R([[cx + 30 * u, yb - 0.2 * HH]])[0]; p.stroke([[tx, ty], [qx, ty + 2 * u], [qx, qy]], 2 * u, "#1b1b1f"); p.ell(qx, qy, 4 * u, 6 * u, "#1b1b1f", 1 * u); }
        else if (o.hat === "turban") { const col = o.cap || "#f1ece0"; const body = R([...sag(yb + 4 * u, 55 * u).reverse(), ...dome(yb + 4 * u, 57 * u, 0.5 * HH)]); p.shadedFill(body, col, mul(col, SH_CLOTH), light, 57 * u, 0.4); p.poly(body, null, ow); p.clip(body, ()=>{ for (const k of [0.1, 0.22, 0.34]) p.stroke(R([[cx - 60 * u, yb - k * HH + 6 * u], [cx, yb - k * HH - 8 * u], [cx + 60 * u, yb - k * HH + 10 * u]]), 1.4 * u); }); const [jx, jy] = R([[cx, yb - 0.2 * HH]])[0]; p.ell(jx, jy, 6 * u, 7 * u, "#c0262d", 1.8 * u); }
        else if (o.hat === "crown") { const col = "#f2c230"; const q = [[cx + 40 * u, yb + 3 * u], [cx - 40 * u, yb + 3 * u]]; for(let i = 0; i <= 6; i++) q.push([cx - 44 * u + i * 88 * u / 6, yb - (i % 2 ? 0.16 : 0.34) * HH]); const body = R(q); p.shadedFill(body, col, mul(col, SH_FELT), light, 44 * u, 0.4); p.poly(body, null, ow); for (const k of [-1, 0, 1]) { const [jx, jy] = R([[cx + k * 24 * u, yb - 0.06 * HH]])[0]; p.ell(jx, jy, 4.5 * u, 4.5 * u, k ? "#3f6fb5" : "#c0262d", 1.4 * u); } }
        else if (o.hat === "beret") { const col = o.cap || "#8a2b2b"; const [bx, by] = R([[cx + 10 * u * (facing || 1), yb - 0.06 * HH]])[0]; p.ell(bx, by, 0.58 * W, 0.17 * HH, col, ow, 0, 360, deg - 8); const [sx, sy] = R([[cx + 10 * u * (facing || 1), yb - 0.25 * HH]])[0]; p.stroke([[sx, sy], [sx + 3 * u, sy - 7 * u]], 2.2 * u); }
        /* ===== CHAPEUS MILITARES DA EPOCA (19/11, referencias reais: Stahlhelm, Brodie, M1, Adrian, Pickelhaube, kepi, bicorne, tricornio) ===== */
        else if (o.hat === "tricorn") { const col = o.cap || "#24222a"; const q = R([[cx - 62 * u, yb - 0.02 * HH], [cx - 40 * u, yb - 0.3 * HH], [cx, yb - 0.2 * HH], [cx + 40 * u, yb - 0.3 * HH], [cx + 62 * u, yb - 0.02 * HH], [cx + 30 * u, yb + 5 * u], [cx, yb + 1 * u], [cx - 30 * u, yb + 5 * u]]); const crownP = R([...sag(yb - 4 * u, 36 * u).reverse(), ...dome(yb - 4 * u, 36 * u, 0.3 * HH)]); p.shadedFill(crownP, shade(col, 0.85), mul(col, SH_FELT), light, 36 * u, 0.4); p.poly(crownP, null, ow); p.shadedFill(q, col, mul(col, SH_FELT), light, 62 * u, 0.4); p.poly(q, null, ow); p.stroke(R([[cx - 60 * u, yb - 0.04 * HH], [cx - 40 * u, yb - 0.27 * HH], [cx, yb - 0.17 * HH], [cx + 40 * u, yb - 0.27 * HH], [cx + 60 * u, yb - 0.04 * HH]]), 2.4 * u, o.trim || "#e8c45a"); }
        else if (o.hat === "bicorne") { const col = o.cap || "#1d1b22"; const q = []; for (let i = 0; i <= 16; i++) { const t = Math.PI * i / 16; q.push([cx - 74 * u * Math.cos(t), yb + 2 * u - 0.42 * HH * Math.sin(t) ** 0.8]); } const body = R(q); p.shadedFill(body, col, mul(col, SH_FELT), light, 74 * u, 0.4); p.poly(body, null, ow); p.clip(body, ()=>p.band(R([[cx - 80 * u, yb - 1 * u], [cx + 80 * u, yb - 1 * u]]), o.trim || "#e8c45a", 0.03 * HH, 0.8 * u)); const [kx, ky] = R([[cx + 22 * u * (facing || 1), yb - 0.2 * HH]])[0]; p.ell(kx, ky, 8 * u, 8 * u, o.cockade || "#27408b", 1.8 * u); p.ell(kx, ky, 4.5 * u, 4.5 * u, "#f4f4f2", 0); p.ell(kx, ky, 2.2 * u, 2.2 * u, "#d8282f", 0); }
        else if (o.hat === "kepi" || o.hat === "quepe") { const kepi = o.hat === "kepi", col = o.cap || (kepi ? "#2a3a6a" : "#3e4a2e"), top = o.capTop || (kepi ? col : col); const ht = (kepi ? 0.34 : 0.24) * HH, wt = kepi ? 40 * u : 58 * u, sl = kepi ? 9 * u : 0; const body = R([...sag(yb, 44 * u).reverse(), [cx - wt + sl, yb - ht], [cx + wt + sl, yb - ht + (kepi ? 3 * u : 0)]]); p.shadedFill(body, top, mul(top, SH_FELT), light, wt, 0.4); p.poly(body, null, ow); p.clip(body, ()=>p.band(R([[cx - 70 * u, yb - 0.07 * HH], [cx + 70 * u, yb - 0.07 * HH]]), o.capBand || (kepi ? col : shade(col, 0.6)), 0.09 * HH, 0.8 * u)); if (o.capBand === "#e8c45a" || o.medals) p.clip(body, ()=>p.band(R([[cx - 70 * u, yb - 0.12 * HH], [cx + 70 * u, yb - 0.12 * HH]]), "#e8c45a", 0.02 * HH, 0.5 * u)); const vz = R([[cx - 36 * u, yb + 1 * u], [cx + 36 * u, yb + 1 * u], [cx + 30 * u * (facing || 1) + 14 * u, yb + 10 * u], [cx - 22 * u, yb + 9 * u]]); p.poly(vz, "#16171b", 2 * u); const [bx, by] = R([[cx, yb - 0.11 * HH]])[0]; p.ell(bx, by, 5.5 * u, 5 * u, "#e8c45a", 1.6 * u); }
        else if (o.hat === "pickelhaube") { const col = o.cap || "#1f1d22"; const body = R([...sag(yb + 3 * u, 50 * u).reverse(), ...dome(yb + 3 * u, 50 * u, 0.38 * HH)]); p.shadedFill(body, col, mul(col, SH_FELT), light, 50 * u, 0.5); p.poly(body, null, ow); const sp = R([[cx - 8 * u, yb - 0.37 * HH], [cx, yb - 0.66 * HH], [cx + 8 * u, yb - 0.37 * HH]]); p.poly(sp, "#e8c45a", 2 * u); const [ex, ey] = R([[cx, yb - 0.17 * HH]])[0]; p.ell(ex, ey, 14 * u, 11 * u, "#e8c45a", 1.8 * u); p.stroke(R([[cx - 50 * u, yb + 3 * u], [cx + 50 * u, yb + 3 * u], [cx + 40 * u * (facing || 1), yb + 9 * u]]), 3 * u, "#16171b"); }
        else if (o.hat === "stahlhelm") { const col = o.cap || "#5d6355"; const body = R([[cx - 60 * u, yb + 0.13 * HH], [cx - 47 * u, yb - 1 * u], ...dome(yb - 1 * u, 47 * u, 0.42 * HH), [cx + 47 * u, yb - 1 * u], [cx + 60 * u, yb + 0.13 * HH], [cx + 34 * u, yb + 0.07 * HH], [cx - 34 * u, yb + 0.07 * HH]]); p.shadedFill(body, col, mul(col, SH_FELT), light, 60 * u, 0.45); p.poly(body, null, ow); p.stroke(R([[cx - 47 * u, yb - 1 * u], [cx - 20 * u, yb + 2 * u], [cx + 20 * u, yb + 2 * u], [cx + 47 * u, yb - 1 * u]]), 1.6 * u, shade(col, 0.6)); }
        else if (o.hat === "brodie") { const col = o.cap || "#6a6a4a"; const brim = R([[cx - 72 * u, yb - 2 * u], [cx + 72 * u, yb - 2 * u], [cx + 64 * u, yb + 6 * u], [cx - 64 * u, yb + 6 * u]]); p.shadedFill(brim, shade(col, 0.9), mul(col, SH_FELT), light, 72 * u, 0.4); p.poly(brim, null, ow); const body = R([...sag(yb - 2 * u, 42 * u).reverse(), ...dome(yb - 2 * u, 42 * u, 0.27 * HH)]); p.shadedFill(body, col, mul(col, SH_FELT), light, 42 * u, 0.45); p.poly(body, null, ow); }
        else if (o.hat === "adrian") { const col = o.cap || "#7a8aa8"; const brim = R([[cx - 60 * u, yb + 1 * u], [cx + 60 * u, yb + 1 * u], [cx + 50 * u, yb + 8 * u], [cx - 50 * u, yb + 8 * u]]); p.shadedFill(brim, shade(col, 0.88), mul(col, SH_FELT), light, 60 * u, 0.4); p.poly(brim, null, ow); const body = R([...sag(yb, 46 * u).reverse(), ...dome(yb, 46 * u, 0.36 * HH)]); p.shadedFill(body, col, mul(col, SH_FELT), light, 46 * u, 0.45); p.poly(body, null, ow); const cr = R([[cx - 30 * u, yb - 0.3 * HH], [cx - 10 * u, yb - 0.44 * HH], [cx + 10 * u, yb - 0.44 * HH], [cx + 30 * u, yb - 0.3 * HH]]); p.stroke(cr, 6 * u, shade(col, 0.75)); p.stroke(cr, 1.6 * u); const [ex, ey] = R([[cx, yb - 0.15 * HH]])[0]; p.ell(ex, ey, 7 * u, 7 * u, shade(col, 0.7), 1.4 * u); }
        else if (o.hat === "m1") { const col = o.cap || "#4f5338"; const body = R([[cx - 54 * u, yb + 0.1 * HH], ...dome(yb + 0.1 * HH, 54 * u, 0.52 * HH).slice(1)]); p.shadedFill(body, col, mul(col, SH_FELT), light, 54 * u, 0.45); p.poly(body, null, ow); p.stroke(R([[cx - 53 * u, yb + 0.1 * HH], [cx, yb + 0.13 * HH], [cx + 53 * u, yb + 0.1 * HH]]), 3 * u, shade(col, 0.6)); if (o.camo) p.clip(body, ()=>{ for (let i = 0; i < 7; i++) { const [mx, my] = R([[cx + (rnd(seed, 40 + i) - 0.5) * 90 * u, yb - (0.05 + 0.4 * rnd(seed, 50 + i)) * HH]])[0]; p.ell(mx, my, 10 * u, 6 * u, o.camo, 0, 0, 360, 30 * i); } }); p.stroke(R([[cx - 50 * u, yb + 0.1 * HH], [cx - 46 * u, yb + 0.42 * HH]]), 1.5 * u, "#3a3020"); }
        else if (o.hat === "colonial") { const col = o.cap || "#efe6cc"; brimE(yb + 4 * u, 0.7 * W, 0.07 * HH, shade(col, 0.86)); const body = R([...sag(yb, 44 * u).reverse(), ...dome(yb, 44 * u, 0.46 * HH)]); p.shadedFill(body, col, mul(col, SH_FELT), light, 44 * u, 0.45); p.poly(body, null, ow); p.clip(body, ()=>p.band(R([[cx - 50 * u, yb - 0.05 * HH], [cx + 50 * u, yb - 0.05 * HH]]), shade(col, 0.8), 0.05 * HH, 0.8 * u)); const [tx, ty] = R([[cx, yb - 0.46 * HH]])[0]; p.ell(tx, ty, 5 * u, 4 * u, shade(col, 0.8), 1.4 * u); }
        else if (o.hat === "bibico") { const col = o.cap || "#5a5a3a"; const body = R([[cx - 46 * u, yb + 2 * u], [cx - 40 * u, yb - 0.2 * HH], [cx + 44 * u, yb - 0.14 * HH], [cx + 46 * u, yb + 2 * u]]); p.shadedFill(body, col, mul(col, SH_CLOTH), light, 46 * u, 0.4); p.poly(body, null, ow); p.stroke(R([[cx - 44 * u, yb - 3 * u], [cx + 45 * u, yb - 1 * u]]), 1.6 * u, shade(col, 0.6)); }
        else if (o.hat === "boonie") { const col = o.cap || "#6a6a44"; brimE(yb + 3 * u, 0.66 * W, 0.08 * HH, shade(col, 0.85)); const body = R([...sag(yb, 40 * u).reverse(), [cx - 34 * u, yb - 0.3 * HH], [cx + 34 * u, yb - 0.3 * HH]]); p.shadedFill(body, col, mul(col, SH_CLOTH), light, 40 * u, 0.4); p.poly(body, null, ow); if (o.camo) p.clip(body, ()=>{ for (let i = 0; i < 5; i++) { const [mx, my] = R([[cx + (rnd(seed, 60 + i) - 0.5) * 70 * u, yb - 0.15 * HH * rnd(seed, 70 + i)]])[0]; p.ell(mx, my, 9 * u, 5 * u, o.camo, 0); } }); }
        else if (o.hat === "wizard") { const col = o.cap || "#4a3a8a"; brimE(yb + 2 * u, 0.7 * W, 0.06 * HH, shade(col, 0.8)); const body = R([...sag(yb, 40 * u).reverse(), [cx - 4 * u, yb - 0.9 * HH], [cx + 14 * u, yb - 0.86 * HH]]); p.shadedFill(body, col, mul(col, SH_FELT), light, 40 * u, 0.4); p.poly(body, null, ow); }
    } else if (o.hat === "bonnet") {
        const [bx, by] = R([
            [
                cx + (side ? 6 * u : 0),
                crown + 0.16 * HH
            ]
        ])[0];
        p.arc(bx, by, 0.5 * W, 0.2 * HH, 200, 340, 7 * u, BONNET_BRIM);
        p.arc(bx, by, 0.5 * W + 3.5 * u, 0.2 * HH + 3.5 * u, 200, 340, 1.2 * u);
        const cy = hc + H.b * 0.98;
        p.stroke([
            [
                cx - 14 * u,
                cy - 4 * u
            ],
            [
                cx,
                cy + 2 * u
            ],
            [
                cx + 14 * u,
                cy - 4 * u
            ]
        ], 2 * u, BONNET_BRIM);
    }
};
const BUILD = {
    adult: {
        a: 118,
        torso: 1.1,
        legs: 1.4,
        tw: 0.8
    },
    stout: {
        a: 118,
        torso: 1.15,
        legs: 1.32,
        tw: 0.92
    },
    lanky: {
        /* v10-final: proporcao fiel @RicksClips3000 (cabeca grande + capsula compacta) */
        a: 146,
        torso: 0.90,
        legs: 1.32,
        tw: 0.86
    },
    kid: {
        a: 112,
        torso: 0.85,
        legs: 1.0,
        tw: 0.72
    }
};
const footStroke = (p, a, b, w, col)=>{
    if (col !== INK) p.stroke([
        a,
        b
    ], w + 3, INK);
    p.stroke([
        a,
        b
    ], w, col);
};
export const bodyFront = (p, o, opts)=>{
    if (o.shirtless) o = { ...o, jacket: o.skin || SKIN, tie: null, collar: null, buttons: null };   /* sem camisa (lutador): o tronco e' pele */
    const { phase = 0, expr = "neutral", mode = "march", look = 0, blink = false, lift = 60, hp: holdK = 0.3, prop = null, tilt = 0, headTilt = 0, wave, light = DEF_LIGHT, facing = 0, seed = 1, fx = null, gest = null, gk = 1, gt = 0, aim = 0 } = opts;
    const Bd = BUILD[o.build] || BUILD.adult, skin = o.skin ?? SKIN, two = Math.PI * 2, lid = lidOf(blink);
    const H = headBlob(seed, Bd.a, facing), W = 2 * H.a, HH = 2 * H.b, u = W / 100;
    const tall = (1 + Bd.torso + Bd.legs) * HH, sole = 975;
    const bob = mode === "march" ? 0.025 * tall * Math.cos(2 * two * phase) : mode === "stroll" ? 0.015 * tall * Math.cos(2 * two * phase) : 0;
    const torsoBot = mode === "sit" ? sole - 0.2 * HH : mode === "kneel" ? sole - 0.36 * Bd.legs * HH : sole - Bd.legs * HH + bob;   /* kneel (19/11): DE JOELHOS, corpo mais baixo */
    const chin = torsoBot - Bd.torso * HH, hc = chin - H.b, crown = hc - H.b, hipY = torsoBot - 0.12 * HH;
    const thick = thickAngle(light), ow = 3.5 * u;
    const legCol = mix(o.pants, INK, 0.86), armCol = mix(o.jacket, INK, 0.84), footCol = o.boots;   // pernas/bracos = traco de TINTA escura (canal: contraste 115-150 contra o chao)
    const legW = 4.6 * u, footW = 6.4 * u;
    p.rot = null;
    if (mode === "sit") {
        for (const side of [
            -1,
            1
        ]){
            const h = [
                300 + side * 15 * u,
                hipY
            ], k = [
                300 + side * 36 * u,
                hipY + 0.2 * HH
            ], f = [
                300 + side * 44 * u,
                sole - 8 * u
            ];
            p.stroke(curve(h, k, f), legW, legCol);
            footStroke(p, [
                f[0] - side * 2 * u,
                f[1]
            ], [
                f[0] + side * 12 * u,
                f[1] - 5 * u
            ], footW, footCol);
        }
    } else if (mode === "kneel") {   /* DE JOELHOS (19/11 v2): coxas abertas descendo ate os JOELHOS no chao (bolinhas marcadas), canelas deitadas para tras e para fora, sola do sapato aparecendo atras */
        for (const side of [-1, 1]) {
            const h = [300 + side * 13 * u, hipY], k = [300 + side * 30 * u, sole - 7 * u], ft = [300 + side * 58 * u, sole - 16 * u];
            p.stroke(curve(h, [300 + side * 24 * u, (hipY + k[1]) / 2], k), legW * 1.15, legCol);
            p.stroke(curve(k, [300 + side * 44 * u, sole - 6 * u], ft), legW, legCol);
            p.ell(k[0], k[1], 7 * u, 5.5 * u, mix(o.pants, INK, 0.55), 1.4 * u, 0, 360, 0);
            p.ell(ft[0] + side * 3 * u, ft[1] - 2 * u, 7 * u, 4 * u, footCol, 1.2 * u, 0, 360, side * 35);
        }
        p.ell(300, sole - 1 * u, 52 * u, 5 * u, "rgba(0,0,0,0.18)", 0, 0, 360, 0);
    } else if (mode === "fall") {
        const legs = [
            [
                [
                    300 - 15 * u,
                    hipY
                ],
                [
                    300 - 46 * u,
                    hipY + 0.5 * HH
                ],
                [
                    300 - 70 * u,
                    hipY + 0.72 * HH
                ]
            ],
            [
                [
                    300 + 15 * u,
                    hipY
                ],
                [
                    300 + 50 * u,
                    hipY + 0.45 * HH
                ],
                [
                    300 + 76 * u,
                    hipY + 0.22 * HH
                ]
            ]
        ];
        legs.forEach(([h, k, f], i)=>{
            p.stroke(curve(h, k, f), legW, legCol);
            footStroke(p, f, [
                f[0] + (i ? 14 : -14) * u,
                f[1] + (i ? -6 : 4) * u
            ], footW, footCol);
        });
    } else if (o.dress) {
        for (const side of [
            -1,
            1
        ]){
            const fx = 300 + side * 12 * u, fy = sole - 4 * u;
            p.stroke([
                [
                    fx,
                    sole - 0.4 * HH
                ],
                [
                    fx + side * u,
                    fy
                ]
            ], legW, legCol);
            footStroke(p, [
                fx - side * 3 * u,
                fy
            ], [
                fx + side * 12 * u,
                fy + u
            ], footW, footCol);
        }
    } else {
        const L = mode === "march" ? lift * 1.25 : mode === "stroll" ? lift * 0.55 : 0;
        for (const [side, ph] of [
            [
                -1,
                0
            ],
            [
                1,
                0.5
            ]
        ]){
            const up = Math.max(0, Math.sin(two * (phase + ph))) * L;
            const hx = 300 + side * 15 * u, fx = 300 + side * 22 * u, fy = sole - 4 * u - up;
            const k = [
                (hx + fx) / 2 + side * (4.8 * u + up * 0.22),
                (hipY + fy) / 2 - up * 0.10
            ];
            p.stroke(curve([
                hx,
                hipY
            ], k, [
                fx,
                fy
            ]), legW, legCol);
            footStroke(p, [
                fx - side * 3 * u,
                fy
            ], [
                fx + side * 13 * u,
                fy + 0.5 * u
            ], footW, footCol);
        }
    }
    const sway = mode === "march" ? 1.6 * Math.sin(two * phase) : mode === "stroll" ? 1.0 * Math.sin(two * phase) : 0;
    const A = tilt + sway;
    p.rot = A ? [
        rad(A),
        300,
        hipY
    ] : null;
    const dress = !!o.dress && mode !== "sit" && mode !== "fall";
    const T = {
        a: Bd.tw / 2 * W / 1.06,
        b: 0.5 * (torsoBot - (chin - 0.25 * HH)),
        nTop: 2.2,
        nBot: 2.6,
        egg: o.build === "stout" ? 0.17 : 0.12,
        asym: 0.04 * facing,
        rot: 0,
        noise: 0.006,
        seed: seed + 7
    };
    const tcx = 300 + 3 * u * facing, tcy = torsoBot - T.b, tp = blobPts(tcx, tcy, T);
    const sh = (side)=>[
            tcx + side * 0.85 * T.a,
            chin + 0.12 * HH
        ];
    const hang = (side, fwd)=>{
        const S = sh(side), ex = tcx + side * (1.12 * T.a + 4 * u);
        const hx = ex + side * 3 * u - side * 6 * u * Math.max(0, fwd) + side * 4 * u * Math.max(0, -fwd);
        return [
            S,
            [
                ex,
                S[1] + 0.48 * HH
            ],
            [
                hx,
                chin + 1.04 * HH - Math.abs(fwd) * 9 * u
            ]
        ];
    };
    const sw = mode === "march" || mode === "stroll" ? Math.sin(two * phase) : 0;
    /* MIRAR/ATIRAR (aim 0..1): o fuzil sai da posicao de descanso (em pe ao lado) e fica apontado para a frente, na altura do ombro */
    const R0 = [
        300 + (47 - 30 * aim) * u,
        torsoBot + 0.12 * HH - aim * (torsoBot + 0.12 * HH - (chin + 0.3 * HH))
    ], R1 = [
        300 + (64 + 78 * aim) * u,
        crown - 0.32 * HH + aim * ((chin + 0.2 * HH) - (crown - 0.32 * HH))
    ];
    const rifle = !!o.rifle && (mode === "march" || mode === "stand" || mode === "stroll");
    const arms = [];
    if (mode === "sit") for (const side of [
        -1,
        1
    ])arms.push({
        pts: [
            sh(side),
            [
                tcx + side * (1.1 * T.a + 6 * u),
                sh(side)[1] + 0.4 * HH
            ],
            [
                tcx + side * (1.2 * T.a + 10 * u),
                torsoBot + 0.04 * HH
            ]
        ],
        front: false
    });
    else if (mode === "fall") for (const side of [
        -1,
        1
    ])arms.push({
        pts: [
            sh(side),
            [
                tcx + side * (1.15 * T.a + 12 * u),
                sh(side)[1] - 0.25 * HH
            ],
            [
                tcx + side * (1.3 * T.a + 24 * u),
                sh(side)[1] - 0.68 * HH
            ]
        ],
        front: false
    });
    else {
        arms.push({
            pts: prop === "shako" ? hang(-1, 0) : hang(-1, -sw),
            front: false
        });
        if (rifle) {
            const G = lerp2(R0, R1, 0.1);
            arms.push({
                pts: [
                    sh(1),
                    [
                        tcx + 1.12 * T.a + 5 * u,
                        sh(1)[1] + 0.45 * HH
                    ],
                    G
                ],
                front: false
            });
        } else if (wave !== undefined) {
            const S = sh(1);
            arms.push({
                pts: [
                    S,
                    [
                        tcx + 1.1 * T.a + 10 * u + 3 * u * wave,
                        S[1] - 0.22 * HH
                    ],
                    [
                        tcx + 1.18 * T.a + 16 * u + 12 * u * wave,
                        S[1] - 0.6 * HH
                    ]
                ],
                front: false
            });
        } else if (prop === "icecream") {
            const S = sh(1);
            arms.push({
                pts: [
                    S,
                    [
                        tcx + 1.05 * T.a + 4 * u,
                        S[1] + 0.45 * HH
                    ],
                    [
                        tcx + 0.5 * T.a,
                        S[1] + 0.4 * HH
                    ]
                ],
                front: true
            });
        } else if (Array.isArray(prop)) {
            const S = sh(1), k = clamp(prop[1], 0, 1);
            const E = lerp2([
                tcx + 1.1 * T.a + 10 * u,
                S[1] - 0.15 * HH
            ], [
                tcx + 1.2 * T.a + 10 * u,
                S[1] + 0.3 * HH
            ], k);
            const Hd = lerp2([
                tcx + 1.15 * T.a + 14 * u,
                S[1] - 0.55 * HH
            ], [
                tcx + 1.45 * T.a + 22 * u,
                S[1] + 0.35 * HH
            ], k);
            arms.push({
                pts: [
                    S,
                    E,
                    Hd
                ],
                front: true
            });
        } else arms.push({
            pts: hang(1, sw),
            front: false
        });
    }
    // ---- gesture override (acting): arms are re-posed by name; gk = 0..1 blend from the hanging pose ----
    if (o.hold && !gest && (mode === "stand" || mode === "stroll") && arms.length) {
        /* quem segura um objeto mostra/usa o objeto: caneca e garrafa sobem ate a boca, papel e livro ficam na frente do peito, luneta vai ao olho, lanterna/tocha/bandeira ficam erguidas */
        const Qh = (xr, yr)=>[tcx + xr * HH, chin + yr * HH], k = o.hold, h = Math.max(0, Math.min(1, holdK));
        const rest = { mug: [0.74, 0.3], bottle: [0.74, 0.32], paper: [0.5, 0.42], book: [0.5, 0.42], spyglass: [0.7, 0.2], coin: [0.8, 0.2], money: [0.8, 0.1], sword: [0.85, 0.25], lantern: [0.95, 0.0], torch: [0.9, -0.1], flag: [0.85, 0.25], staff: [0.85, 0.25], pitchfork: [0.85, 0.25], shovel: [0.8, 0.3], tulip: [0.6, 0.3], bag: [0.62, 0.62] }[k] || [0.8, 0.3];
        const use = { mug: [0.2, -0.1], bottle: [0.2, -0.14], paper: [0.42, 0.26], book: [0.42, 0.26], spyglass: [0.36, -0.5], coin: [0.9, -0.05], money: [0.95, -0.15], sword: [0.9, -0.3], lantern: [1.0, -0.3], torch: [0.95, -0.35], flag: [0.85, 0.2], staff: [0.85, 0.22], pitchfork: [0.85, 0.22], shovel: [0.8, 0.28], tulip: [0.5, 0.0], bag: [0.62, 0.6] }[k] || rest;
        const hx = rest[0] + (use[0] - rest[0]) * h, hy = rest[1] + (use[1] - rest[1]) * h;
        arms[arms.length - 1] = { pts: [Qh(0.36, 0.12), Qh(0.36 + (hx - 0.36) * 0.55 + 0.12, 0.12 + (hy - 0.12) * 0.5 + 0.16), Qh(hx, hy)], front: true, top: hy < 0.08 };   /* mao perto do rosto fica na frente da cabeca */
    }
    if (gest && mode !== "sit" && mode !== "fall") {   /* kneel aceita gesto (maos de suplica) */
        const Q = (s, xr, yr)=>[tcx + s * xr * HH, chin + yr * HH];
        const wob = 0.035 * Math.sin(gt * 9), fs = (facing || 1) > 0 ? 1 : -1;
        const G = {
            point: (s)=>s === fs ? { pts: [Q(s, 0.36, 0.12), Q(s, 0.7, 0.3 - wob), Q(s, 1.32, -0.1 + wob)], front: false } : null,
            up: (s)=>({ pts: [Q(s, 0.36, 0.12), Q(s, 0.66, -0.06 + wob), Q(s, 0.74, -0.84 + wob * 1.5)], front: true }),   /* 20/11: na frente do tronco (soldado de farda larga escondia os bracos da comemoracao) */
            shrug: (s)=>({ pts: [Q(s, 0.36, 0.12), Q(s, 0.78, 0.44), Q(s, 1.05, 0.2 + wob)], front: false }),
            hips: (s)=>({ pts: [Q(s, 0.36, 0.12), Q(s, 0.9, 0.42), Q(s, 0.52, 0.72)], front: false }),
            scared: (s)=>({ pts: [Q(s, 0.36, 0.12), Q(s, 0.7, 0.3), Q(s, 0.3, -0.38 + wob)], front: true }),
            hold: (s)=>({ pts: [Q(s, 0.36, 0.12), Q(s, 0.6, 0.4), Q(s, 0.07, 0.3 + wob * 0.5)], front: true }),
            cross: (s)=>({ pts: [Q(s, 0.36, 0.12), Q(s, 0.68, 0.46), Q(-s, 0.3, 0.34)], front: true }),
            think: (s)=>s === fs ? { pts: [Q(s, 0.36, 0.12), Q(s, 0.5, 0.42), Q(s, 0.1, -0.08)], front: true, top: true } : null,
            facepalm: (s)=>s === fs ? { pts: [Q(s, 0.36, 0.12), Q(s, 0.62, -0.02), Q(s, 0.04, -0.86)], front: true, top: true } : null,
            salute: (s)=>s === fs ? { pts: [Q(s, 0.36, 0.12), Q(s, 0.78, -0.1), Q(s, 0.3, -0.97)], front: true, top: true } : null,
            /* GESTOS DE ACAO (19/11: a cena faz o que a narracao conta) */
            plead: (s)=>({ pts: [Q(s, 0.36, 0.12), Q(s, 0.42, 0.34), Q(s, 0.06, 0.02 + wob)], front: true }),   /* SUPLICA (19/11): as duas maos juntas na frente do peito */
            /* v9: GESTOS EXPRESSIVOS ESTILO RICKS CLIPS (bi-manuais, arco amplo, overshoot) */
            reach: (s)=>s === fs ? { pts: [Q(s, 0.36, 0.12), Q(s, 0.78, 0.18), Q(s, 1.24, 0.22 + wob)], front: true } : { pts: [Q(s, 0.36, 0.12), Q(s, 0.52, 0.38), Q(s, 0.44, 0.56)], front: false },
            pour: (s)=>s === fs ? { pts: [Q(s, 0.36, 0.12), Q(s, 0.80, -0.05), Q(s, 1.12, -0.18 + 0.18 * Math.sin(gt * 4))], front: true } : null,
            stir: (s)=>s === fs ? { pts: [Q(s, 0.36, 0.12), Q(s, 0.74, 0.24), Q(s, 1.02 + 0.22 * Math.cos(gt * 11), 0.42 + 0.10 * Math.sin(gt * 11))], front: true } : { pts: [Q(s, 0.36, 0.12), Q(s, 0.56, 0.32), Q(s, 0.46, 0.48)], front: false },
            throw: (s)=>{ const k = Math.min(1, gt * 2.8); const sw = Math.sin(k * Math.PI * 0.85); return s === fs ? { pts: [Q(s, 0.36, 0.12), Q(s, 0.42 + 0.48 * k, -0.45 + 0.55 * k), Q(s, 0.22 + 1.22 * k, -1.05 + 1.15 * k - 0.15 * sw)], front: true } : { pts: [Q(s, 0.36, 0.12), Q(s, 0.65, 0.30), Q(s, 0.82, 0.45)], front: false }; },
            hammer: (s)=>{ const k = Math.pow(Math.abs(Math.sin(gt * 8.5)), 0.7); return s === fs ? { pts: [Q(s, 0.36, 0.12), Q(s, 0.76, -0.22 + 0.35 * k), Q(s, 0.98, -0.88 + 1.25 * k)], front: true } : null; },
            write: (s)=>s === fs ? { pts: [Q(s, 0.36, 0.12), Q(s, 0.62, 0.34), Q(s, 0.48 + 0.12 * Math.sin(gt * 16), 0.34 + 0.05 * Math.cos(gt * 16))], front: true } : null,
            eat: (s)=>s === fs ? { pts: [Q(s, 0.36, 0.12), Q(s, 0.64, 0.08), Q(s, 0.14, -0.38 + 0.08 * Math.sin(gt * 14))], front: true, top: true, food: true } : null,
            lift: (s)=>({ pts: [Q(s, 0.36, 0.12), Q(s, 0.66, -0.26), Q(s, 0.50, -0.82 + wob * 1.6)], front: false }),
            push: (s)=>{ const k = Math.min(1, Math.sin(Math.min(1, gt * 2.6) * Math.PI * 0.65) * 1.15); return { pts: [Q(s, 0.36, 0.12), Q(s, 0.76 + 0.22 * k, 0.06), Q(s, 1.15 + 0.45 * k, 0.02 + wob)], front: true }; },
            punch: (s)=>{ const ph = Math.min(1, gt * 3.0); const k = ph < 0.25 ? -0.35 * (ph / 0.25) : Math.sin(Math.min(1, (ph - 0.25) / 0.75) * Math.PI) * 1.25; return s === fs ? { pts: [Q(s, 0.36, 0.12), Q(s, 0.62 + 0.34 * k, 0.06), Q(s, 0.76 + 0.88 * k, -0.04)], front: true } : { pts: [Q(s, 0.36, 0.12), Q(s, 0.58, 0.26), Q(s, 0.32, 0.12)], front: false }; },
            wave2: (s)=>s === fs ? { pts: [Q(s, 0.36, 0.12), Q(s, 0.78, -0.06 + wob), Q(s, 0.9 + 0.22 * Math.sin(gt * 11), -0.82)], front: false } : null
        };
        const g = G[gest];
        if (g) {
            const kk = Math.max(0, Math.min(1, gk)), mixp = (A, B)=>A.map((pt, i)=>[pt[0] + (B[i][0] - pt[0]) * kk, pt[1] + (B[i][1] - pt[1]) * kk]);
            for (const s of [-1, 1]) {
                const slot = s < 0 ? 0 : arms.length - 1, ga = g(s);
                if (!ga) continue;
                const base = s < 0 ? arms[0] : arms[arms.length - 1];
                const pts = mixp(base.pts, ga.pts);
                const entry = { pts, front: ga.front && kk > 0.35, top: !!ga.top && kk > 0.35, food: !!ga.food && kk > 0.35 };
                if (s < 0) arms[0] = entry; else arms[arms.length - 1] = entry;
            }
        }
    }
    /* objeto na mao (canal: maos seguram objetos). o.hold = bottle | mug | paper | lantern | pitchfork | staff | flag | torch | bag | coin | spyglass | book */
    const drawHeld = ((u)=>(x, y)=>{
        const k = o.hold, c2 = o.holdCol;
        if (k === "bottle") { p.band([[x, y + 6 * u], [x, y - 14 * u]], c2 || "#3f8a4f", 8 * u, 1.5 * u, "round"); p.band([[x, y - 14 * u], [x, y - 24 * u]], c2 || "#3f8a4f", 3.6 * u, 1.3 * u, "round"); p.band([[x - 3 * u, y - 2 * u], [x + 3 * u, y - 2 * u]], "#f1ece0", 6 * u, 0.8 * u); }
        else if (k === "mug") { p.poly([[x - 7 * u, y - 12 * u], [x + 7 * u, y - 12 * u], [x + 6 * u, y + 5 * u], [x - 6 * u, y + 5 * u]], c2 || "#c9a060", 1.6 * u); p.arc(x + 8 * u, y - 3 * u, 5 * u, 6 * u, 270, 450, 1.8 * u); p.band([[x - 6 * u, y - 13 * u], [x + 6 * u, y - 13 * u]], "#fff8e8", 4 * u, 0.8 * u, "round"); }
        else if (k === "paper" || k === "book") { const w = 11 * u, h = k === "book" ? 13 * u : 15 * u; p.poly([[x - w, y - h - 6 * u], [x + w, y - h - 8 * u], [x + w, y + h - 8 * u], [x - w, y + h - 6 * u]], c2 || (k === "book" ? "#8a3a3a" : "#fbf6e6"), 1.6 * u); if (k === "paper") for (const q of [-8, -2, 4]) p.stroke([[x - 7 * u, y + q * u - 7 * u], [x + 7 * u, y + q * u - 8 * u]], 0.9 * u); else p.stroke([[x, y - h - 7 * u], [x, y + h - 7 * u]], 1.2 * u); }
        else if (k === "lantern") { p.stroke([[x, y], [x, y + 9 * u]], 1.4 * u); p.poly([[x - 7 * u, y + 9 * u], [x + 7 * u, y + 9 * u], [x + 8 * u, y + 28 * u], [x - 8 * u, y + 28 * u]], "#ffd75a", 1.6 * u); p.band([[x - 8 * u, y + 9 * u], [x + 8 * u, y + 9 * u]], "#3a3d47", 3 * u, 0.9 * u); p.band([[x - 9 * u, y + 28 * u], [x + 9 * u, y + 28 * u]], "#3a3d47", 3 * u, 0.9 * u); p.ell(x, y + 19 * u, 2.5 * u, 4 * u, "#ff9a3a", 0.8 * u); }
        else if (k === "pitchfork" || k === "staff" || k === "flag" || k === "torch") { const top = y - (k === "torch" ? 26 : 78) * u, bot = y + (k === "torch" ? 10 : 54) * u; p.band([[x, bot], [x, top]], "#8a5a34", 3.6 * u, 1.3 * u, "round");
            if (k === "pitchfork") { p.stroke([[x - 9 * u, top - 16 * u], [x - 9 * u, top], [x + 9 * u, top], [x + 9 * u, top - 16 * u]], 2 * u, "#8d949c"); p.stroke([[x, top], [x, top - 18 * u]], 2 * u, "#8d949c"); }
            if (k === "flag") { const c1 = c2 || "#c0262d", c3 = o.holdCol2 || "#f4f1e8", w = 52 * u, h = 34 * u, y0 = top + 2 * u; const wv = (t) => 4 * u * Math.sin(t * 5.2 + 0.6);   /* bandeira maior, ondulada, com faixa de 2a cor e ponteira dourada */
                const top_ = [], bot_ = [], mid1 = [], mid2 = []; for (let q = 0; q <= 8; q++) { const t = q / 8, xx = x + 2 * u + w * t; top_.push([xx, y0 + wv(t)]); bot_.push([xx, y0 + h + wv(t + 0.15)]); mid1.push([xx, y0 + h * 0.36 + wv(t + 0.05)]); mid2.push([xx, y0 + h * 0.64 + wv(t + 0.1)]); }
                p.poly([...top_, ...bot_.slice().reverse()], c1, 1.8 * u); p.poly([...mid1, ...mid2.slice().reverse()], c3, 0); p.poly([...top_, ...bot_.slice().reverse()], null, 1.8 * u); p.ell(x, top - 3 * u, 4 * u, 4 * u, "#f2c230", 1.3 * u); }
            if (k === "torch") { p.ell(x, top - 7 * u, 7 * u, 11 * u, "#ff9a3a", 1.4 * u); p.ell(x, top - 4 * u, 3.5 * u, 6 * u, "#ffe07a", 0.6 * u); } }
        else if (k === "tulip") { const c1 = c2 || "#e2332f"; p.band([[x, y + 8 * u], [x, y - 22 * u]], "#3f8a3a", 3 * u, 1.2 * u, "round"); p.poly([[x - 2 * u, y - 4 * u], [x - 13 * u, y - 14 * u], [x - 3 * u, y - 12 * u]], "#4fa84a", 1.2 * u); p.poly([[x - 8 * u, y - 22 * u], [x - 9 * u, y - 37 * u], [x - 4 * u, y - 31 * u], [x, y - 40 * u], [x + 4 * u, y - 31 * u], [x + 9 * u, y - 37 * u], [x + 8 * u, y - 22 * u], [x, y - 18 * u]], c1, 1.8 * u); }
        else if (k === "shovel") { p.band([[x, y - 30 * u], [x, y + 42 * u]], "#8a5a34", 3.6 * u, 1.3 * u, "round"); p.poly([[x - 9 * u, y + 40 * u], [x + 9 * u, y + 40 * u], [x + 8 * u, y + 58 * u], [x, y + 66 * u], [x - 8 * u, y + 58 * u]], "#9aa0a8", 1.6 * u); p.band([[x - 6 * u, y - 31 * u], [x + 6 * u, y - 31 * u]], "#8a5a34", 3.4 * u, 1.2 * u, "round"); }
        else if (k === "bag") { p.stroke([[x, y], [x, y + 8 * u]], 1.6 * u); p.ell(x, y + 22 * u, 13 * u, 15 * u, c2 || "#b98448", 1.8 * u); p.stroke([[x - 6 * u, y + 10 * u], [x + 6 * u, y + 10 * u]], 1.6 * u); }
        else if (k === "coin") { p.ell(x, y - 8 * u, 7 * u, 7 * u, "#f2c230", 1.5 * u); }
        else if (k === "sword") { p.band([[x, y + 6 * u], [x, y - 70 * u]], "#c9d0d8", 4.5 * u, 1.3 * u, "round"); p.band([[x, y - 70 * u], [x, y - 78 * u]], "#c9d0d8", 2 * u, 1 * u, "round"); p.band([[x - 10 * u, y - 2 * u], [x + 10 * u, y - 2 * u]], "#8a5a34", 3.2 * u, 1.2 * u, "round"); p.ell(x, y + 10 * u, 3 * u, 3 * u, "#f2c230", 1 * u); }   /* espada */
        else if (k === "money") { for (const [dx, rot] of [[-9, -0.35], [0, 0], [9, 0.35]]) { const cx = x + dx * u, cy = y - 16 * u, w = 8 * u, h = 15 * u, c = Math.cos(rot), sn = Math.sin(rot), R = (px, py) => [cx + px * c - py * sn, cy + px * sn + py * c]; p.poly([R(-w, -h), R(w, -h), R(w, h), R(-w, h)], "#6fbf73", 1.5 * u); p.ell(cx, cy, 3.6 * u, 4.6 * u, "#d9f2c8", 1 * u); } }   /* notas de dolar em leque */
        else if (k === "spyglass") { p.band([[x - 4 * u, y], [x + 20 * u, y - 10 * u]], "#c9a060", 6 * u, 1.3 * u, "round"); p.band([[x + 20 * u, y - 10 * u], [x + 30 * u, y - 14 * u]], "#3a3d47", 8 * u, 1.3 * u, "round"); }
    })(u * 1.7);
    const drawArm = (a)=>{
        p.stroke(curve(a.pts[0], a.pts[1], a.pts[2]), 4.2 * u, armCol);
        if (o.hold && a === (arms.find((q)=>q.front) || arms[arms.length - 1])) drawHeld(a.pts[2][0], a.pts[2][1]);
        if (a.food) { const fx = a.pts[2][0], fy = a.pts[2][1] - 4 * u; p.dot(fx, fy, 11 * u, INK); p.dot(fx, fy, 9 * u, '#e8d9a8'); p.dot(fx - 3 * u, fy - 3 * u, 3 * u, '#fff6d8'); p.band([[fx, fy - 9 * u], [fx + 2 * u, fy - 16 * u]], '#6aa84f', 3 * u, 1.2 * u, 'round'); }   /* bulbo/cebola na mao ao comer */
        p.dot(a.pts[2][0], a.pts[2][1], 5.5 * u);
        if (opts.speedLines && a.front) {
          const hx_ = a.pts[2][0], hy_ = a.pts[2][1], sd_ = (facing || 1) >= 0 ? 1 : -1;
          for (const dy_ of [-14, 0, 14]) p.stroke([[hx_ - sd_ * 42 * u, hy_ + dy_ * u], [hx_ - sd_ * 12 * u, hy_ + dy_ * u]], 2.2 * u, "#ffffff");
        }
        if (o.gloves) { p.dot(a.pts[2][0], a.pts[2][1], 15 * u, INK); p.dot(a.pts[2][0], a.pts[2][1], 12.8 * u, o.gloves); p.dot(a.pts[2][0] - 3 * u, a.pts[2][1] - 4 * u, 3.5 * u, mix(o.gloves, '#ffffff', 0.45)); }   /* LUVA DE BOXE */
    };
    if (rifle) drawRifle(p, R0, R1, u);
    if (o.sword && mode !== "sit") {
        const s0 = [
            tcx - 0.75 * T.a,
            torsoBot - 0.2 * HH
        ];
        p.band([
            s0,
            [
                s0[0] - Math.sin(rad(25)) * 0.8 * HH,
                s0[1] + Math.cos(rad(25)) * 0.8 * HH
            ]
        ], "#c9ccd2", 3 * u, 1.2 * u, "round");
    }
    for (const a of arms)if (!a.front) drawArm(a);
    if (dress) {
        const D = {
            a: 0.5 * W * 0.98,
            b: 0.5 * (sole - 0.35 * HH - (chin - 0.2 * HH)),
            nTop: 2.0,
            nBot: 3.0,
            egg: 0.35,
            asym: 0.03 * facing,
            rot: 0,
            noise: 0.006,
            seed: seed + 9
        };
        const dp = blobPts(300, sole - 0.35 * HH - D.b, D);
        p.gradFill(dp, o.dress, mul(o.dress, SH_CLOTH), light);
        p.inkRing(dp, ow, thick);
        const Sw = {
            a: 0.37 * W,
            b: 0.3 * HH,
            nTop: 2.2,
            nBot: 2.4,
            egg: 0.1,
            asym: 0,
            rot: 0,
            noise: 0.006,
            seed: seed + 8
        };
        const sp = blobPts(300, chin + 0.12 * HH, Sw);
        p.gradFill(sp, o.jacket, mul(o.jacket, SH_CLOTH), light);
        p.inkRing(sp, ow * 0.9, thick);
    } else {
        p.gradFill(tp, o.jacket, mul(o.jacket, SH_CLOTH), light);
        p.clip(tp, ()=>{
            if (o.belt) {
                for (const s of [
                    -1,
                    1
                ])p.band([
                    [
                        tcx - s * 0.75 * T.a,
                        chin - 0.05 * HH
                    ],
                    [
                        tcx + s * 0.8 * T.a,
                        torsoBot - 0.1 * HH
                    ]
                ], o.belt, 5.5 * u, 1.8 * u);
                const xc = tcx + 0.025 * T.a, yc = chin - 0.05 * HH + (torsoBot - 0.1 * HH - (chin - 0.05 * HH)) * (0.75 / 1.55);
                p.poly([
                    [
                        xc - 3.5 * u,
                        yc - 3.5 * u
                    ],
                    [
                        xc + 3.5 * u,
                        yc - 3.5 * u
                    ],
                    [
                        xc + 3.5 * u,
                        yc + 3.5 * u
                    ],
                    [
                        xc - 3.5 * u,
                        yc + 3.5 * u
                    ]
                ], "#d9dde0", 1.5 * u);
            }
            if (o.logo) { const ly = chin + 0.42 * (torsoBot - chin), lw = 0.34 * T.a, lh = 0.16 * (torsoBot - chin), th = 0.075 * T.a, lc = o.logoColor || '#f4f1e8';   /* LOGO NO PEITO (19/11): Musk de camiseta preta com o X/T; quem e quem pela roupa */
              const bar = (x0, y0, x1, y1) => { const dx = x1 - x0, dy = y1 - y0, L_ = Math.hypot(dx, dy) || 1, nx = -dy / L_ * th, ny = dx / L_ * th; p.poly([[x0 + nx, y0 + ny], [x1 + nx, y1 + ny], [x1 - nx, y1 - ny], [x0 - nx, y0 - ny]], lc, 0.6 * u); };
              if (o.logo === 'X') { bar(tcx - lw, ly - lh, tcx + lw, ly + lh); bar(tcx + lw, ly - lh, tcx - lw, ly + lh); }
              else if (o.logo === 'T') { p.poly([[tcx - lw * 1.1, ly - lh], [tcx + lw * 1.1, ly - lh], [tcx + lw * .8, ly - lh * .55], [tcx - lw * .8, ly - lh * .55]], lc, 0.6 * u); bar(tcx, ly - lh * .6, tcx, ly + lh * 1.1); } }
            if (o.tie) { p.poly([[tcx - 0.2 * T.a, chin + 0.04 * HH], [tcx + 0.2 * T.a, chin + 0.04 * HH], [tcx + 0.3 * T.a, torsoBot - 0.3 * HH], [tcx, torsoBot - 0.16 * HH], [tcx - 0.3 * T.a, torsoBot - 0.3 * HH]], o.tie, 1.6 * u); p.poly([[tcx - 0.42 * T.a, chin], [tcx, chin + 0.16 * HH], [tcx + 0.42 * T.a, chin]], '#f4f1e8', 1.4 * u); }   /* gravata comprida + colarinho */
            if (o.sash) p.band([
                [
                    tcx - 1.3 * T.a,
                    torsoBot - 0.32 * HH
                ],
                [
                    tcx + 1.3 * T.a,
                    torsoBot - 0.32 * HH
                ]
            ], o.sash, 0.13 * HH, 1.8 * u);
            if (!o.shirtless && !o.camo && !o.tie && !o.logo) {
                p.poly([[tcx - 0.32 * T.a, chin - 0.02 * HH], [tcx, chin + 0.24 * HH], [tcx + 0.32 * T.a, chin - 0.02 * HH]], '#f4f0e6', 1.2 * u);
                if (!o.belt && !o.sash) {
                    for (const s_ of [-1, 1]) {
                        p.band([[tcx + s_ * 0.38 * T.a, chin + 0.02 * HH], [tcx + s_ * 0.42 * T.a, torsoBot - 0.08 * HH]], shade(o.jacket, 0.55), 3.2 * u, 0.9 * u);
                    }
                }
                p.poly([[tcx + 0.28 * T.a, chin + 0.42 * HH], [tcx + 0.66 * T.a, chin + 0.42 * HH], [tcx + 0.64 * T.a, chin + 0.64 * HH], [tcx + 0.30 * T.a, chin + 0.64 * HH]], shade(o.jacket, 0.86), 1.0 * u);
            }
            for(let i = 0; i < 3; i++){
                const y = chin + 0.30 * HH + i * 0.19 * HH;
                if (o.shirtless) break; if (o.sash && Math.abs(y - (torsoBot - 0.32 * HH)) < 0.08 * HH) continue;
                p.dot(tcx + 2 * u * facing, y, 1.8 * u + 0.6 * u, INK);
                p.dot(tcx + 2 * u * facing, y, 1.8 * u, o.buttons ?? shade(o.jacket, 0.72));
            }
            if (o.trunks) { p.poly([[tcx - 3 * T.a, torsoBot - 0.2 * HH], [tcx + 3 * T.a, torsoBot - 0.2 * HH], [tcx + 3 * T.a, torsoBot + 0.3 * HH], [tcx - 3 * T.a, torsoBot + 0.3 * HH]], o.trunks, 0); p.band([[tcx - 3 * T.a, torsoBot - 0.2 * HH], [tcx + 3 * T.a, torsoBot - 0.2 * HH]], o.trunkBand || '#f4f4f2', 0.045 * HH, 1.2 * u); }   /* SHORT DE LUTADOR (19/11) */ if (o.shirtless) { for (const s_ of [-1, 1]) p.stroke([[tcx + s_ * 0.15 * T.a, chin + 0.2 * HH], [tcx + s_ * 0.6 * T.a, chin + 0.24 * HH], [tcx + s_ * 0.95 * T.a, chin + 0.17 * HH]], 1.6 * u, shade(o.jacket, 0.62)); p.stroke([[tcx, chin + 0.3 * HH], [tcx, chin + 0.46 * HH]], 1.4 * u, shade(o.jacket, 0.62)); } if (o.camo) for (let i = 0; i < 16; i++) { const rx = ((i * 37) % 17) / 17 - 0.5, ry = ((i * 53) % 13) / 13; p.dot(tcx + rx * 2.6 * T.a, chin + 0.05 * HH + ry * (torsoBot - chin), (4 + (i % 3) * 1.6) * u, i % 2 ? o.camo : shade(o.camo, 0.75)); }   /* CAMUFLADO (soldado moderno) */
            if (o.collar) p.band([[tcx - 1.4 * T.a, chin + 0.04 * HH], [tcx + 1.4 * T.a, chin + 0.04 * HH]], o.collar, 0.1 * HH, 1.6 * u);   /* gola (arminho do rei/imperador, colarinho branco do terno) */
            if (o.medals) for (let i = 0; i < o.medals; i++) { const mx = tcx - (0.35 + 0.24 * i) * T.a, my = chin + 0.24 * HH; p.poly([[mx - 2.4 * u, my - 5 * u], [mx + 2.4 * u, my - 5 * u], [mx + 2.4 * u, my + 1 * u], [mx - 2.4 * u, my + 1 * u]], ['#c8302a', '#27408b', '#2f8a4a', '#e8c45a'][i % 4], 1.1 * u); p.dot(mx, my + 4 * u, 3 * u, INK); p.dot(mx, my + 4 * u, 2.3 * u, '#e8c45a'); }   /* MEDALHAS (patente) */
            if (o.epaulets) for (const s of [-1, 1]) { p.dot(tcx + s * 1.05 * T.a, chin + 0.06 * HH, 6.5 * u, INK); p.dot(tcx + s * 1.05 * T.a, chin + 0.06 * HH, 5.6 * u, o.epaulets); for (let k = -2; k <= 2; k++) p.stroke([[tcx + s * 1.05 * T.a + k * 2 * u, chin + 0.06 * HH + 4 * u], [tcx + s * 1.05 * T.a + k * 2.2 * u, chin + 0.06 * HH + 9 * u]], 1.4 * u, o.epaulets); }   /* DRAGONAS douradas (oficial) */
        });
        if (o.sash) {
            const s = facing || 1;
            p.poly([
                [
                    tcx + s * 0.55 * T.a,
                    torsoBot - 0.3 * HH
                ],
                [
                    tcx + s * 0.75 * T.a,
                    torsoBot + 0.05 * HH
                ],
                [
                    tcx + s * 0.45 * T.a,
                    torsoBot + 0.02 * HH
                ]
            ], o.sash, 1.6 * u);
        }
        p.inkRing(tp, ow, thick);
    }
    for (const a of arms)if (a.front && !a.top) {
        drawArm(a);
        const [hx, hy] = a.pts[2];
        if (prop === "icecream") {
            p.poly([
                [
                    hx - 8 * u,
                    hy - 12 * u
                ],
                [
                    hx + 8 * u,
                    hy - 12 * u
                ],
                [
                    hx,
                    hy + 7 * u
                ]
            ], "#e0a35a", 1.8 * u);
            p.ell(hx, hy - 19 * u, 11 * u, 10 * u, "#f7c6d9", 2.2 * u);
            p.dot(hx, hy, 5.5 * u);
        } else if (Array.isArray(prop)) {
            const ang = rad(-70 + 105 * clamp(prop[1], 0, 1));
            const Rh = (pts)=>rotPts(pts, ang, hx, hy);
            p.band(Rh([
                [
                    hx,
                    hy + 12 * u
                ],
                [
                    hx,
                    hy - 44 * u
                ]
            ]), "#8a5a34", 5 * u, 1.5 * u, "round");
            p.poly(Rh([
                [
                    hx - 12 * u,
                    hy - 58 * u
                ],
                [
                    hx + 20 * u,
                    hy - 58 * u
                ],
                [
                    hx + 20 * u,
                    hy - 42 * u
                ],
                [
                    hx - 12 * u,
                    hy - 42 * u
                ]
            ]), "#7d848c", 2.2 * u);
            p.dot(hx, hy, 5.5 * u);
        }
    }
    if (prop === "shako") {
        const [hx, hy] = arms[0].pts[2];
        p.poly([
            [
                hx - 14 * u,
                hy + 3 * u
            ],
            [
                hx + 14 * u,
                hy + 3 * u
            ],
            [
                hx + 16 * u,
                hy + 30 * u
            ],
            [
                hx - 16 * u,
                hy + 30 * u
            ]
        ], "#3a3d47", 2.2 * u);
        p.ell(hx, hy + 31 * u, 3.5 * u, 3.5 * u, "#2b7a4b", 1.5 * u);
        p.dot(hx, hy, 5.5 * u);
    }
    const Ah = A + headTilt, [cpx, cpy] = rotAbout([
        300,
        chin
    ], rad(A), [
        300,
        hipY
    ]);
    p.rot = Ah ? [
        rad(Ah),
        300,
        chin,
        cpx - 300,
        cpy - chin
    ] : null;
    hatBehind(p, o, H, 300, hc, light, thick, ow, false);
    const hp = blobPts(300, hc, H);
    p.shadedFill(hp, skin, mul(skin, SH_SKIN), light, H.a);
    if ((expr === "angry" || expr === "shout") && fx && fx.rage) {
      p.clip(hp, () => {
        const g_ = p.g, grd = g_.createLinearGradient(300, hc - H.b, 300, hc + H.b * 0.45);
        grd.addColorStop(0, "rgba(148, 36, 206, 0.78)");
        grd.addColorStop(0.6, "rgba(196, 62, 224, 0.32)");
        grd.addColorStop(1, "rgba(255, 255, 255, 0)");
        g_.fillStyle = grd; g_.fillRect(300 - H.a * 1.2, hc - H.b * 1.2, H.a * 2.4, H.b * 2.4);
      });
    }
    p.inkRing(hp, ow, thick);
    hatOn(p, o, hp, H, 300, hc, light, seed, facing, false);
    const brim = !!o.hat && o.hat !== "hair" && o.hat !== "bonnet" && o.hat !== "cap";
    faceFront(p, 300, hc, W, expr, facing, look, lid, brim, skin, o.moustache, o.build === "stout", { ...(fx || {}), beard: o.beard, glasses: o.glasses, face: o.faceId });
    if (o.noseMetal) { const u_ = W / 100, nx = 300 + 7 * u_ * (facing || 0), ny = hc + 6 * u_; p.ell(nx, ny, 6.5 * u_, 5 * u_, INK, 0); p.ell(nx, ny, 5.3 * u_, 3.9 * u_, o.noseMetal, 0); p.ell(nx - 1.6 * u_, ny - 1.3 * u_, 1.7 * u_, 1.2 * u_, "#fff6d0", 0); }   /* NARIZ DE METAL (Tycho Brahe) */
    for (const a of arms)if (a.top) drawArm(a);
    p.rot = null;
};
const ik = (hip, ank, l1, l2)=>{
    const dx = ank[0] - hip[0], dy = ank[1] - hip[1], d = clamp(Math.hypot(dx, dy), 1, l1 + l2 - 0.01);
    const A = Math.acos(clamp((l1 * l1 + d * d - l2 * l2) / (2 * l1 * d), -1, 1)), k = Math.atan2(dy, dx) - A;
    return [
        hip[0] + l1 * Math.cos(k),
        hip[1] + l1 * Math.sin(k)
    ];
};
const SWING_HIP = 733;
const drawRifle = (p, R0, R1, u) => {   
        const dx = R1[0] - R0[0], dy = R1[1] - R0[1], L = Math.hypot(dx, dy) || 1, nx = -dy / L, ny = dx / L, at = (t) => lerp2(R0, R1, t), off = (q, k) => [q[0] + nx * k, q[1] + ny * k];
        p.poly([off(at(0), 6.5 * u), off(at(0), -4 * u), off(at(0.3), -2.4 * u), off(at(0.3), 2.6 * u)], "#6a3f22", 1.5 * u);   /* coronha */
        p.band([at(0.28), at(0.62)], "#8a5532", 4.2 * u, 1.4 * u, "round");                                                       /* corpo */
        p.poly([off(at(0.36), -2 * u), off(at(0.42), -6.5 * u), off(at(0.46), -2 * u)], "#3a3d47", 1 * u);                         /* gatilho */
        p.band([at(0.55), R1], "#8d949c", 2.4 * u, 1.2 * u, "round");                                                             /* cano */
        p.band([at(0.97), at(1.0)], "#3a3d47", 3.2 * u, 0.8 * u, "round");                                                        /* boca do cano */
    };   /* FUZIL de verdade: coronha, corpo com gatilho, cano de metal */
export const bodySide = (p, o, opts)=>{
    if (o.shirtless) o = { ...o, jacket: o.skin || SKIN, tie: null, collar: null, buttons: null };   /* sem camisa (lutador): o tronco e' pele */
    const { phase = 0, expr = "neutral", mode = "march", blink = false, stomp = 1, pose = 0, stride = 1, light = DEF_LIGHT, seed = 1, aim = 0 } = opts;
    const Bd = BUILD[o.build] || BUILD.adult, skin = o.skin ?? SKIN, two = Math.PI * 2, lid = lidOf(blink);
    const H = {
        ...headBlob(seed, Bd.a, 1),
        asym: 0.12,
        rot: rad(3 + 3 * (rnd(seed, 7) - 0.5))
    };
    const W = 2 * H.a, HH = 2 * H.b, u = W / 100, sole = 975, ankY = sole - 4 * u;
    const thick = thickAngle(light), ow = 3.5 * u;
    const legLen = (Bd.legs + 0.12) * HH - 4 * u, l1 = legLen / 2, l2 = legLen / 2;
    const nearCol = mix(o.pants, INK, 0.86), farCol = mix(o.pants, INK, 0.92), footCol = o.boots;
    const legs = [];
    let hipY = ankY - legLen * 0.995, lean = 0, nearFwd = 0;
    if (mode === "march") {
        const S = 370 * stride, liftH = Math.max(22, 40 + 70 * (stomp - 1));
        const st = (ph)=>{
            const c = ((phase + ph) % 1 + 1) % 1;
            if (c < 0.5) {
                const s = c / 0.5;
                return {
                    x: S / 2 - S * s,
                    h: 0,
                    stance: true,
                    s
                };
            }
            const s = (c - 0.5) / 0.5;
            return {
                x: -S / 2 + S * s - S / Math.PI * Math.sin(2 * Math.PI * s),
                h: liftH * Math.sin(Math.PI * s),
                stance: false,
                s
            };
        };
        const nL = st(0), fL = st(0.5), stance = nL.stance ? nL : fL;
        const Leff = legLen * (1 - 0.035 * Math.sin(Math.PI * stance.s));
        hipY = ankY - Math.sqrt(Math.max(1, Leff * Leff - stance.x * stance.x));
        for (const [L, near] of [
            [
                fL,
                false
            ],
            [
                nL,
                true
            ]
        ])legs.push({
            ank: [
                300 + L.x,
                ankY - L.h
            ],
            pitch: L.stance ? 0 : rad(35 * Math.sin(Math.PI * L.s) * (1 - 1.6 * L.s)),
            near
        });
        lean = 4 + 3 * Math.cos(2 * two * phase);
        nearFwd = nL.x / (S / 2);
    } else if (mode === "push") {
        hipY = ankY - 0.87 * legLen;
        legs.push({
            ank: [
                300 - 0.5 * legLen,
                ankY
            ],
            pitch: rad(-8),
            near: false
        }, {
            ank: [
                300 + 0.32 * legLen,
                ankY
            ],
            pitch: 0,
            near: true
        });
        lean = 14 * pose;
    } else if (mode === "swing") {
        hipY = SWING_HIP;
        const a = rad(60 * pose);
        for (const [dx, near] of [
            [
                -6,
                false
            ],
            [
                0,
                true
            ]
        ]){
            const knee = [
                300 + l1 * 0.98 + dx * u,
                hipY + 6 * u
            ];
            legs.push({
                ank: [
                    knee[0] + l2 * Math.sin(a),
                    knee[1] + l2 * Math.cos(a)
                ],
                pitch: -a * 0.5,
                near
            });
        }
    } else {
        legs.push({
            ank: [
                300 - 4 * u,
                ankY
            ],
            pitch: 0,
            near: false
        }, {
            ank: [
                300 + 4 * u,
                ankY
            ],
            pitch: 0,
            near: true
        });
    }
    const torsoBot = hipY + 0.12 * HH, chin = torsoBot - Bd.torso * HH, hc = chin - H.b, crown = hc - H.b, hip = [
        300,
        hipY
    ];
    p.rot = null;
    for (const L of legs){
        const knee = mode === "swing" ? [
            300 + l1 * 0.98 + (L.near ? 0 : -6 * u),
            hipY + 6 * u
        ] : ik(hip, L.ank, l1, l2);
        const hp0 = [
            300 + (L.near ? 0 : -5 * u),
            hipY
        ];
        p.stroke([
            hp0,
            knee,
            L.ank
        ], 5.8 * u, L.near ? nearCol : farCol);
        const c = Math.cos(L.pitch), s = Math.sin(L.pitch);
        footStroke(p, [
            L.ank[0] - 3 * u * c,
            L.ank[1] - 3 * u * s
        ], [
            L.ank[0] + 13 * u * c,
            L.ank[1] + 13 * u * s + 0.5 * u
        ], 7.5 * u, L.near ? footCol : footCol === INK ? INK : shade(footCol, 0.82));
    }
    p.rot = lean ? [
        rad(lean),
        300,
        hipY
    ] : null;
    const T = {
        a: (o.build === "stout" ? 0.36 : 0.31) * W,
        b: 0.5 * (torsoBot - (chin - 0.25 * HH)),
        nTop: 2.2,
        nBot: 2.5,
        egg: 0.1,
        asym: 0.06,
        rot: 0,
        noise: 0.006,
        seed: seed + 7
    };
    const tcx = 300 + 2 * u, tcy = torsoBot - T.b, tp = blobPts(tcx, tcy, T);
    const armCol = mix(o.jacket, INK, 0.5), farArm = mix(o.jacket, INK, 0.68);
    const S = [
        tcx + 0.05 * T.a,
        chin + 0.14 * HH
    ], aLen = 0.95 * HH;
    const swingArm = (ang)=>{
        const e = [
            S[0] + Math.sin(ang) * aLen * 0.5,
            S[1] + Math.cos(ang) * aLen * 0.5
        ], a2 = ang + rad(16) * Math.sign(ang || 1);
        return [
            S,
            e,
            [
                e[0] + Math.sin(a2) * aLen * 0.5,
                e[1] + Math.cos(a2) * aLen * 0.5
            ]
        ];
    };
    const rifle = !!o.rifle && (mode === "march" || mode === "stand");
    const B0 = [   /* de lado: fuzil no ombro; com aim (atirando) aponta para a frente, na altura do peito */
        tcx + (0.72 - 0.9 * aim) * T.a,
        chin + (0.58 - 0.3 * aim) * HH
    ], B1 = [
        tcx + (-0.95 + 3.1 * aim) * T.a + (-22 + 52 * aim) * u,
        crown - 0.4 * HH + aim * ((chin + 0.24 * HH) - (crown - 0.4 * HH))
    ];
    let near, far;
    if (mode === "swing") {
        near = [
            S,
            [
                S[0] + 12 * u,
                S[1] - 0.16 * HH
            ],
            [
                300 + 6 * u,
                chin - 0.3 * HH
            ]
        ];
        far = [
            S,
            [
                S[0] + 8 * u,
                S[1] - 0.18 * HH
            ],
            [
                300 + 2 * u,
                chin - 0.36 * HH
            ]
        ];
    } else if (mode === "push") {
        const reach = 0.55 * HH + 0.45 * HH * pose;
        let hN = [
            S[0] + reach,
            S[1] + 0.06 * HH
        ];
        if (opts.hand) {
            const th = -rad(lean), dx = opts.hand[0] - 300, dy = opts.hand[1] - hipY;
            const tg = [
                300 + dx * Math.cos(th) - dy * Math.sin(th),
                hipY + dx * Math.sin(th) + dy * Math.cos(th)
            ];
            hN = [
                hN[0] + (tg[0] - hN[0]) * pose,
                hN[1] + (tg[1] - hN[1]) * pose
            ];
        }
        near = [
            S,
            [
                (S[0] + hN[0]) / 2,
                (S[1] + hN[1]) / 2 + 0.06 * HH
            ],
            hN
        ];
        far = [
            S,
            [
                (S[0] + hN[0]) / 2 - 4 * u,
                (S[1] + hN[1]) / 2 - 0.02 * HH
            ],
            [
                hN[0] - 6 * u,
                hN[1] - 0.08 * HH
            ]
        ];
    } else if (rifle) {
        near = [
            S,
            [
                S[0] - 4 * u,
                S[1] + 0.42 * HH
            ],
            B0
        ];
        far = mode === "march" ? swingArm(rad(30) * nearFwd) : swingArm(0);
    } else {
        near = swingArm(rad(-30) * nearFwd);
        far = mode === "march" ? swingArm(rad(30) * nearFwd) : null;
    }
    if (far) {
        p.stroke(curve(far[0], far[1], far[2]), 5.2 * u, farArm);
        p.dot(far[2][0], far[2][1], 5.5 * u);
    }
    p.gradFill(tp, o.jacket, mul(o.jacket, SH_CLOTH), light);
    p.clip(tp, ()=>{
        if (o.belt) p.band([
            [
                tcx - 0.65 * T.a,
                chin - 0.05 * HH
            ],
            [
                tcx + 0.75 * T.a,
                torsoBot - 0.1 * HH
            ]
        ], o.belt, 5.5 * u, 1.8 * u);
        if (o.sash) p.band([
            [
                tcx - 1.3 * T.a,
                torsoBot - 0.32 * HH
            ],
            [
                tcx + 1.3 * T.a,
                torsoBot - 0.32 * HH
            ]
        ], o.sash, 0.13 * HH, 1.8 * u);
        if (!o.dress) for(let i = 0; i < 3; i++){
            const y = chin + 0.16 * HH + i * 0.24 * HH; if (o.shirtless) break;
            p.dot(tcx + 0.8 * T.a, y, 3 * u, INK);
            p.dot(tcx + 0.8 * T.a, y, 2.2 * u, o.buttons ?? shade(o.jacket, 0.7));
        }
        if (o.trunks) { p.poly([[tcx - 3 * T.a, torsoBot - 0.2 * HH], [tcx + 3 * T.a, torsoBot - 0.2 * HH], [tcx + 3 * T.a, torsoBot + 0.3 * HH], [tcx - 3 * T.a, torsoBot + 0.3 * HH]], o.trunks, 0); p.band([[tcx - 3 * T.a, torsoBot - 0.2 * HH], [tcx + 3 * T.a, torsoBot - 0.2 * HH]], o.trunkBand || '#f4f4f2', 0.045 * HH, 1.2 * u); }   /* SHORT DE LUTADOR (19/11) */ if (o.shirtless) { for (const s_ of [-1, 1]) p.stroke([[tcx + s_ * 0.15 * T.a, chin + 0.2 * HH], [tcx + s_ * 0.6 * T.a, chin + 0.24 * HH], [tcx + s_ * 0.95 * T.a, chin + 0.17 * HH]], 1.6 * u, shade(o.jacket, 0.62)); p.stroke([[tcx, chin + 0.3 * HH], [tcx, chin + 0.46 * HH]], 1.4 * u, shade(o.jacket, 0.62)); } if (o.camo) for (let i = 0; i < 16; i++) { const rx = ((i * 37) % 17) / 17 - 0.5, ry = ((i * 53) % 13) / 13; p.dot(tcx + rx * 2.6 * T.a, chin + 0.05 * HH + ry * (torsoBot - chin), (4 + (i % 3) * 1.6) * u, i % 2 ? o.camo : shade(o.camo, 0.75)); }   /* CAMUFLADO (soldado moderno) */
        if (o.collar) p.band([[tcx - 1.4 * T.a, chin + 0.04 * HH], [tcx + 1.4 * T.a, chin + 0.04 * HH]], o.collar, 0.1 * HH, 1.6 * u);   /* gola (arminho do rei/imperador, colarinho branco do terno) */
        if (o.medals) for (let i = 0; i < o.medals; i++) { const mx = tcx - (0.35 + 0.24 * i) * T.a, my = chin + 0.24 * HH; p.poly([[mx - 2.4 * u, my - 5 * u], [mx + 2.4 * u, my - 5 * u], [mx + 2.4 * u, my + 1 * u], [mx - 2.4 * u, my + 1 * u]], ['#c8302a', '#27408b', '#2f8a4a', '#e8c45a'][i % 4], 1.1 * u); p.dot(mx, my + 4 * u, 3 * u, INK); p.dot(mx, my + 4 * u, 2.3 * u, '#e8c45a'); }   /* MEDALHAS (patente) */
        if (o.epaulets) for (const s of [-1, 1]) { p.dot(tcx + s * 1.05 * T.a, chin + 0.06 * HH, 6.5 * u, INK); p.dot(tcx + s * 1.05 * T.a, chin + 0.06 * HH, 5.6 * u, o.epaulets); for (let k = -2; k <= 2; k++) p.stroke([[tcx + s * 1.05 * T.a + k * 2 * u, chin + 0.06 * HH + 4 * u], [tcx + s * 1.05 * T.a + k * 2.2 * u, chin + 0.06 * HH + 9 * u]], 1.4 * u, o.epaulets); }   /* DRAGONAS douradas (oficial) */
    });
    p.inkRing(tp, ow, thick);
    if (rifle) drawRifle(p, B0, B1, u);
    p.stroke(curve(near[0], near[1], near[2]), 5.2 * u, armCol);
    p.dot(near[2][0], near[2][1], 5.5 * u);
    const hx = 300 + 4 * u;
    hatBehind(p, o, H, hx, hc, light, thick, ow, true);
    const hp = blobPts(hx, hc, H);
    p.shadedFill(hp, skin, mul(skin, SH_SKIN), light, H.a);
    p.inkRing(hp, ow, thick);
    hatOn(p, o, hp, H, hx, hc, light, seed, 1, true);
    const brim = !!o.hat && o.hat !== "hair" && o.hat !== "bonnet" && o.hat !== "cap";
    faceSide(p, hx, hc, W, expr, lid, brim, skin, o.moustache, o.build === "stout");
    p.rot = null;
};
export const swingKid = (p, o, kick, expr, light = DEF_LIGHT, blink = 0)=>{
    const rope = 1830, k = 1.1, HH = 2 * headBlob(5, BUILD[o.build ?? "adult"].a, 1).b;
    const seat = rope + 18, x0 = 150, x1 = 550;
    p.line([
        [
            350,
            20
        ],
        [
            x0 + 16,
            seat + 4
        ]
    ], "#a07a4c", 10);
    p.poly(rrect(x0, seat, x1, seat + 36, 10), "#b5653f", 9);
    const g = p.g;
    g.save();
    g.translate(350 - 300 * k, rope + 18 - (SWING_HIP + 0.12 * HH) * k);
    g.scale(k, k);
    bodySide(new Pen(g), o, {
        expr,
        mode: "swing",
        pose: kick,
        light,
        seed: 5,
        blink
    });
    g.restore();
    p.line([
        [
            350,
            20
        ],
        [
            x1 - 16,
            seat + 4
        ]
    ], "#a07a4c", 10);
};
export const fxNote = (p, kind, col = "#1f2a44")=>{
    p.ell(70, 200, 46, 34, col, 8, 0, 360, -20);
    p.stroke([
        [
            110,
            190
        ],
        [
            110,
            40
        ]
    ], 14);
    if (kind === 0) p.poly([
        [
            110,
            40
        ],
        [
            170,
            70
        ],
        [
            170,
            110
        ],
        [
            110,
            82
        ]
    ], col, 8);
    else {
        p.ell(150, 170, 40, 30, col, 8, 0, 360, -20);
        p.stroke([
            [
                186,
                160
            ],
            [
                186,
                20
            ]
        ], 14);
        p.poly([
            [
                110,
                40
            ],
            [
                186,
                20
            ],
            [
                186,
                50
            ],
            [
                110,
                70
            ]
        ], col, 8);
    }
};
export const fxBurst = (p, t, col = "#fff3b0", rays = 10, r0 = 40, r1 = 230)=>{
    const c = 250, e = 1 - (1 - t) ** 3;
    for(let i = 0; i < rays; i++){
        const a = rad(i * 360 / rays + 7 * (i % 2)), ra = r0 + (r1 - r0) * e * (0.75 + 0.25 * (i % 2));
        p.poly([
            [
                c + r0 * 0.5 * Math.cos(a + 0.18),
                c + r0 * 0.5 * Math.sin(a + 0.18)
            ],
            [
                c + ra * Math.cos(a),
                c + ra * Math.sin(a)
            ],
            [
                c + r0 * 0.5 * Math.cos(a - 0.18),
                c + r0 * 0.5 * Math.sin(a - 0.18)
            ]
        ], col, Math.max(3, 8 * (1 - t)));
    }
    if (t < 0.5) p.ell(c, c, r0 * (1.4 - t), r0 * (1.4 - t), WHITE, 8);
};
export const fxSplash = (p, t)=>{
    const c = 400, size = 800, rise = Math.sin(Math.min(1, t * 1.3) * Math.PI);
    const blue = "#bfe8ff", deep = "#6cc0f0";
    if (rise > 0.02) {
        const pts = [];
        for(let i = 0; i < 19; i++){
            const h = (i % 2 ? 260 : 130) * rise * (0.7 + 0.3 * Math.sin(i * 1.7));
            pts.push([
                c - 330 + 660 * i / 18,
                size - 120 - h
            ]);
        }
        p.poly([
            ...pts,
            [
                c + 330,
                size - 90
            ],
            [
                c - 330,
                size - 90
            ]
        ], blue, 10);
        p.ell(c, size - 100, 360, 46, deep, 10);
    }
    for(let i = 0; i < 8; i++){
        const a = rad(200 + i * 18), d = 120 + 380 * t, y = size - 160 + d * Math.sin(a) + 520 * t * t, r = 26 * (1 - t) + 6;
        if (t > 0.08 && y < size - 40) p.ell(c + d * Math.cos(a), y, r, r * 1.25, blue, 7);
    }
};
export const fxPuff = (p, t)=>{
    for(let i = 0; i < 5; i++){
        const a = rad(160 + i * 55), d = 40 + 70 * t, r = (34 + 20 * (i % 2)) * (1 - 0.6 * t);
        p.ell(150 + d * Math.cos(a), 180 + d * 0.45 * Math.sin(a), r, r * 0.8, `rgba(238,225,205,${(1 - t).toFixed(3)})`, 0);
    }
};
export const fxStars = (p, t)=>{
    for(let i = 0; i < 4; i++){
        const a = t * Math.PI * 2 + i * Math.PI / 2, x = 210 + 150 * Math.cos(a), y = 110 + 40 * Math.sin(a), pts = [];
        for(let k = 0; k < 10; k++){
            const r = k % 2 ? 14 : 34, b = rad(k * 36 - 90);
            pts.push([
                x + r * Math.cos(b),
                y + r * Math.sin(b)
            ]);
        }
        p.poly(pts, "#ffd84a", 6);
    }
};
export const fxCreak = (p, t)=>{
    const j = 6 * Math.sin(t * 40);
    for (const a of [
        -30,
        0,
        30
    ]){
        const b = rad(a - 90);
        p.stroke([
            [
                150 + 70 * Math.cos(b) + j,
                230 + 70 * Math.sin(b)
            ],
            [
                150 + 100 * Math.cos(b) + 10 + j,
                230 + 100 * Math.sin(b)
            ],
            [
                150 + 130 * Math.cos(b) + j,
                230 + 130 * Math.sin(b)
            ]
        ], 10);
    }
};
export const fxRing = (p, t)=>{
    const g = p.g;
    for(let k = 0; k < 3; k++){
        const u = t - k * 0.22;
        if (u <= 0 || u >= 1) continue;
        g.beginPath();
        g.ellipse(300, 300, 60 + 230 * u, 60 + 230 * u, 0, 0, Math.PI * 2);
        g.strokeStyle = k === 0 ? "#f6fcff" : "#cfe8fa";
        g.lineWidth = 9 * (1 - u) + 3;
        g.stroke();
    }
};
export const fxSign = (p)=>{
    const g = p.g, RED = "#d42f2f";
    p.poly(rrect(14, 14, 686, 506, 40), "#f6ecd2", 0);
    p.poly(rrect(14, 14, 686, 506, 40), null, 14);
    p.poly(rrect(70, 352, 630, 384, 8), "#8a5a3a", 9);
    g.beginPath();
    g.moveTo(112, 470);
    g.quadraticCurveTo(350, 300, 588, 470);
    g.strokeStyle = INK;
    g.lineWidth = 16;
    g.lineCap = "round";
    g.stroke();
    for (const x of [
        88,
        612
    ])p.poly(rrect(x - 16, 384, x + 16, 470, 4), "#8a5a3a", 9);
    for (const x of [
        150,
        278,
        406,
        534
    ]){
        p.poly(rrect(x - 30, 150, x + 30, 214, 14), "#357650", 9);
        p.stroke([
            [
                x - 8,
                210
            ],
            [
                x + 34,
                262
            ],
            [
                x + 46,
                338
            ]
        ], 15, INK);
        p.stroke([
            [
                x + 6,
                210
            ],
            [
                x - 12,
                274
            ],
            [
                x - 36,
                336
            ]
        ], 15, INK);
        p.poly(rrect(x + 30, 330, x + 74, 350, 9), INK, 0);
        p.poly(rrect(x - 52, 328, x - 8, 348, 9), INK, 0);
    }
    for (const [a, b] of [
        [
            [
                96,
                70
            ],
            [
                604,
                452
            ]
        ],
        [
            [
                604,
                70
            ],
            [
                96,
                452
            ]
        ]
    ]){
        p.stroke([
            a,
            b
        ], 58, "#ffffff");
        p.stroke([
            a,
            b
        ], 42, RED);
    }
};
export const fxCloud = (p, seed)=>{
    const blobs = [
        [
            150,
            190,
            80
        ],
        [
            250,
            150,
            105
        ],
        [
            360,
            160,
            95
        ],
        [
            450,
            195,
            70
        ],
        [
            300,
            210,
            90
        ]
    ];
    for (const [x, y, r] of blobs)p.ell(x + seed * 37 % 20 - 10, y, r, r * 0.8, "#ffffff", 0);
    p.ell(300, 235, 230, 40, "#ffffff", 0);
};
export const fxShadow = (p, col)=>{
    const g = p.g;
    g.fillStyle = WHITE;
    g.fillRect(0, 0, 128, 256);
    g.save();
    g.filter = "blur(9px)";
    const lg = g.createLinearGradient(0, 205, 0, 22);
    lg.addColorStop(0, mix(col, WHITE, 0.08));
    lg.addColorStop(0.55, mix(col, WHITE, 0.3));
    lg.addColorStop(1, mix(col, WHITE, 0.85));
    g.fillStyle = lg;
    g.beginPath();
    g.moveTo(40, 205);
    g.bezierCurveTo(36, 120, 46, 50, 64, 30);
    g.bezierCurveTo(82, 50, 92, 120, 88, 205);
    g.closePath();
    g.fill();
    g.fillStyle = col;
    g.beginPath();
    g.ellipse(64, 205, 30, 17, 0, 0, Math.PI * 2);
    g.fill();
    g.restore();
};
export const fxContact = (p, col)=>{
    const g = p.g;
    g.fillStyle = WHITE;
    g.fillRect(0, 0, 128, 128);
    const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64);
    for (const [r, k] of [
        [
            0,
            0
        ],
        [
            0.32,
            0.02
        ],
        [
            0.5,
            0.22
        ],
        [
            0.66,
            0.58
        ],
        [
            0.82,
            0.88
        ],
        [
            1,
            1
        ]
    ])gr.addColorStop(r, mix(col, WHITE, k));
    g.fillStyle = gr;
    g.fillRect(0, 0, 128, 128);
};
export const fxPlank = (p)=>{
    p.poly(rrect(14, 30, 306, 78, 10), "#a8744a", 9);
    p.line([
        [
            40,
            46
        ],
        [
            150,
            44
        ],
        [
            270,
            50
        ]
    ], "#7d5234", 4);
    p.line([
        [
            60,
            62
        ],
        [
            200,
            64
        ],
        [
            284,
            60
        ]
    ], "#7d5234", 4);
    p.dot(36, 54, 5, INK);
    p.dot(284, 54, 5, INK);
};
export const fxDrum = (p)=>{
    p.poly(rrect(40, 70, 220, 190, 16), "#f1ece0", 9);
    p.poly(rrect(32, 58, 228, 86, 12), "#c9373a", 8);
    p.poly(rrect(32, 176, 228, 204, 12), "#c9373a", 8);
    p.line([
        [
            52,
            88
        ],
        [
            82,
            172
        ],
        [
            112,
            88
        ],
        [
            142,
            172
        ],
        [
            172,
            88
        ],
        [
            202,
            172
        ]
    ], INK, 6);
    p.ell(130, 58, 98, 18, "#f7f3ea", 8);
};
export const fxBlob = (p, col)=>{
    const g = p.g;
    g.fillStyle = WHITE;
    g.fillRect(0, 0, 128, 128);
    const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64);
    for (const [r, k] of [
        [
            0,
            0
        ],
        [
            0.5,
            0.04
        ],
        [
            0.64,
            0.18
        ],
        [
            0.76,
            0.42
        ],
        [
            0.87,
            0.72
        ],
        [
            0.95,
            0.92
        ],
        [
            1,
            1
        ]
    ])gr.addColorStop(r, mix(col, WHITE, k));
    g.fillStyle = gr;
    g.fillRect(0, 0, 128, 128);
};
FACE.snore = { eye: ["dash", "dash"], brow: [0, -1], mouth: "o" };
FACE.stubborn = { eye: ["lid", "lid"], brow: [4, -3], mouth: "frown" };
FACE.squint = { eye: ["slit", "slit"], brow: [3, -2], mouth: "dash" };

// ---------------- Roman-era cast (our own designs), built on the Pen / blob / face helpers above ----------------
const STEEL = "#aeb6bf", BRASS = "#d9a845", LEATHER = "#7a4a2a";
export const OUTFITS = {
  legion: { tunic: "#b8322f", cape: "#8f2228", skin: SKIN, helmet: true, armor: true, spear: true, shield: true },
  old: { tunic: "#9c4a3c", cape: "#6e3330", skin: "#f3d6bb", helmet: "old", armor: true, spear: true, shield: false, beard: "#f4f1ea", brows: "#f4f1ea" },
  toga: { tunic: "#f1ead8", skin: "#f5c9a0", toga: "#6b3c8f", hair: "#3b2a20", stout: true },
  civA: { tunic: "#4f7fb8", skin: "#f5c9a0", hair: "#5a3b2a" },
  civB: { tunic: "#d9a441", skin: SKIN, hair: "#2b211c", dress: "#c25a7a" },
  civC: { tunic: "#5d8a3a", skin: "#c99067", hair: "#1e1714", stout: true },
  workA: { tunic: "#8a5d3b", skin: "#f5c9a0", cap: "#c2733a", apron: "#d8c9a6" },
  cook: { tunic: "#f7f4ee", skin: "#f5c9a0", cap: "#d8452f", apron: "#d8452f", moustache: "#5a3b2a", stout: true },
  workB: { tunic: "#3f6a6f", skin: "#ecd0b6", cap: "#5b4a8a", moustache: "#4a3020" },
};

/** galea: iron bowl, brass brow band, cheek guards, transverse red crest */
const galea = (p, H, cx, hc, light, thick, ow, old, u) => {
  const crest = old ? "#8d4b3f" : "#d2372f", bowl = old ? "#8f8a7e" : STEEL;
  // crest (behind the bowl top)
  const cy0 = hc - H.b * 0.98;
  const cr = ellPts(cx, cy0, 0.66 * 2 * H.a, 0.42 * 2 * H.b, 180, 360, 0, 40);
  cr.push([cx + 0.66 * 2 * H.a * 0.98, cy0 + 4 * u], [cx - 0.66 * 2 * H.a * 0.98, cy0 + 4 * u]);
  const crP = [...ellPts(cx, cy0 + 2 * u, 0.62 * 2 * H.a, 0.36 * 2 * H.b, 180, 360, 0, 40)];
  p.shadedFill(crP, crest, mul(crest, [0.7, 0.62, 0.7]), light, 0.62 * 2 * H.a, 0.3);
  p.clip(crP, () => { for (let i = -9; i <= 9; i++) p.stroke([[cx + i * 7.4 * u, cy0], [cx + i * 9.4 * u, cy0 - 0.62 * H.b * Math.cos(i / 11)]], 1.4 * u, mul(crest, [0.62, 0.55, 0.62])); });
  if (old) p.clip(crP, () => { for (let i = 0; i < 6; i++) p.ell(cx + (i - 3) * 22 * u, cy0 - 18 * u - (i % 2) * 10 * u, 9 * u, 5 * u, "#6f6a5e", 0); });
  p.inkRing(crP, ow * 0.85, thick);
  p.poly(rrect(cx - 10 * u, cy0 - 6 * u, cx + 10 * u, cy0 + 6 * u, 3 * u), BRASS, 2 * u);
  // bowl: upper head cap
  const bandY = hc - H.b * 0.42;
  const bp = ellPts(cx, bandY, H.a * 1.05, H.b * 0.66, 180, 360, 0, 48);
  p.shadedFill(bp, bowl, mul(bowl, [0.62, 0.64, 0.72]), light, H.a, 0.4);
  p.clip(bp, () => {
    p.stroke(ellPts(cx - 20 * u, bandY - 0.3 * H.b, 0.25 * H.a, 0.18 * H.b, 200, 300, 0, 16), 4 * u, "#ffffff55");
    if (old) for (let i = 0; i < 9; i++) p.ell(cx + Math.sin(i * 2.3) * 0.8 * H.a, bandY - (0.08 + 0.5 * ((i * 0.37) % 1)) * H.b, (3 + (i % 3) * 2) * u, (2 + (i % 2)) * u, "#8a4b22", 0);
  });
  p.inkRing(bp, ow * 0.9, thick);
  p.band([[cx - H.a * 1.04, bandY], [cx + H.a * 1.04, bandY]], old ? "#a88a4a" : BRASS, 7 * u, 1.8 * u, "round");
  for (const s of [-1, 1]) p.dot(cx + s * 0.55 * H.a, bandY, 2.2 * u, "#fff3c4");
};
const cheeks = (p, H, cx, hc, light, ow, old, u) => {
  const bowl = old ? "#8f8a7e" : STEEL;
  for (const s of [-1, 1]) {
    const x0 = cx + s * 0.78 * H.a, x1 = cx + s * 1.07 * H.a, y0 = hc - H.b * 0.42, y1 = hc + H.b * 0.48;
    const pts = [[x0, y0], [x1, y0], [x1 - s * 0.04 * H.a, y1 - 0.1 * H.b], [x0 + s * 0.06 * H.a, y1], [x0 - s * 0.05 * H.a, (y0 + y1) / 2]];
    p.shadedFill(pts, bowl, mul(bowl, [0.62, 0.64, 0.72]), light, 0.2 * H.a, 0.3);
    p.poly(pts, null, ow * 0.8);
    p.dot((x0 + x1) / 2, (y0 + y1) / 2 - 0.05 * H.b, 2.2 * u, BRASS);
  }
};
const cobweb = (p, cx, cy, r, u) => {
  const g = p.g; g.save(); g.globalAlpha = 0.8;
  for (let i = 0; i < 7; i++) { const a = -Math.PI * (0.05 + 0.9 * i / 6); p.stroke([[cx, cy], [cx + Math.cos(a) * r, cy + Math.sin(a) * r]], 1.1 * u, "#f2f2f2"); }
  for (let k = 1; k <= 4; k++) { const rr = r * k / 4.3, pts = []; for (let i = 0; i < 7; i++) { const a = -Math.PI * (0.05 + 0.9 * i / 6); pts.push([cx + Math.cos(a) * rr, cy + Math.sin(a) * rr]); } p.stroke(pts, 1 * u, "#f2f2f2"); }
  g.restore();
};

/** front-facing Roman-era character. opts: expr, blink, look, facing, seed, L/R arm poses, tilt, headTilt, bob, nohelmet, light */
export const romanFront = (p, key, opts = {}) => {
  const O = typeof key === "string" ? OUTFITS[key] : key;
  const { expr = "neutral", blink = 0, look = 0, facing = 0, seed = 3, L = "hang", R = O.spear ? "spear" : "hang", tilt = 0, headTilt = 0,
    bob = 0, nohelmet = false, light = rad(-120), web = false, step = 0 } = opts;
  const lid = lidOf(blink), skin = O.skin ?? SKIN;
  const H = headBlob(seed, 118, facing), W = 2 * H.a, HH = 2 * H.b, u = W / 100;
  const torsoL = O.stout ? 1.12 : 1.08, legsL = 1.38, sole = 975;
  const torsoBot = sole - legsL * HH - bob * HH, chin = torsoBot - torsoL * HH, hc = chin - H.b, hipY = torsoBot - 0.12 * HH;
  const thick = thickAngle(light), ow = 5 * u, cx = 300;
  const legCol = mix(O.tunic, INK, 0.62), armCol = mix(O.tunic, INK, 0.5);
  const helmet = !!O.helmet && !nohelmet, old = O.helmet === "old";
  p.rot = null;
  // ---- cape behind everything ----
  if (O.cape) {
    const cp = [[cx - 0.48 * W, chin + 0.08 * HH], [cx + 0.48 * W, chin + 0.08 * HH], [cx + 0.62 * W, sole - 0.55 * HH], [cx + 0.2 * W, sole - 0.45 * HH], [cx - 0.2 * W, sole - 0.5 * HH], [cx - 0.62 * W, sole - 0.55 * HH]];
    p.gradFill(cp, O.cape, mul(O.cape, [0.6, 0.6, 0.7]), light); p.inkRing(cp, ow * 0.8, thick);
  }
  // ---- legs ----
  const dress = !!O.dress;
  for (const side of [-1, 1]) {
    const up = Math.max(0, Math.sin(Math.PI * 2 * (step + (side > 0 ? 0.5 : 0)))) * 30 * (step ? 1 : 0);
    const hx = cx + side * 16 * u, fx = cx + side * 22 * u, fy = sole - 4 * u - up;
    p.stroke(curve([hx, hipY], [(hx + fx) / 2 + side * 2 * u, (hipY + fy) / 2], [fx, fy]), 5.8 * u, legCol);
    const sandal = O.helmet ? LEATHER : "#5a3b2a";
    p.stroke([[fx - side * 3 * u, fy], [fx + side * 13 * u, fy + 0.5 * u]], 7.5 * u + 3, INK);
    p.stroke([[fx - side * 3 * u, fy], [fx + side * 13 * u, fy + 0.5 * u]], 7.5 * u, sandal);
    if (O.helmet) for (let k = 1; k <= 3; k++) p.stroke([[fx - 4 * u, fy - k * 0.07 * HH], [fx + 4 * u, fy - k * 0.07 * HH - 2 * u]], 2 * u, LEATHER);
  }
  // ---- upper body ----
  p.rot = tilt ? [rad(tilt), cx, hipY] : null;
  const T = { a: (0.4 * W) / 1.06 * (O.stout ? 1.12 : 1), b: 0.5 * (torsoBot - (chin - 0.25 * HH)), nTop: 2.2, nBot: 2.6, egg: O.stout ? 0.17 : 0.12, asym: 0.04 * facing, rot: 0, noise: 0.006, seed: seed + 7 };
  const tcx = cx + 3 * u * facing, tcy = torsoBot - T.b, tp = blobPts(tcx, tcy, T);
  const S = (side) => [tcx + side * 0.85 * T.a, chin + 0.12 * HH];
  const arm = (side, pose) => {
    const s = S(side), X = (k) => tcx + side * (T.a * 1.1 + k * u);
    switch (pose) {
      case "spear": return { pts: [s, [X(6), s[1] + 0.42 * HH], [X(10), s[1] + 0.2 * HH]], front: false };
      case "point": return { pts: [s, [X(28), s[1] - 0.02 * HH], [X(62), s[1] - 0.1 * HH]], front: false, finger: true };
      case "up": return { pts: [s, [X(14), s[1] - 0.3 * HH], [X(22), s[1] - 0.75 * HH]], front: false };
      case "wave": return { pts: [s, [X(16), s[1] - 0.2 * HH], [X(30 + 10 * Math.sin(opts.wv || 0)), s[1] - 0.62 * HH]], front: false };
      case "hip": return { pts: [s, [X(22), s[1] + 0.3 * HH], [tcx + side * T.a * 0.95, torsoBot - 0.3 * HH]], front: false };
      case "belly": return { pts: [s, [X(8), s[1] + 0.45 * HH], [tcx + side * 0.25 * T.a, torsoBot - 0.35 * HH]], front: true };
      case "temple": return { pts: [s, [X(26), s[1] + 0.05 * HH], [cx + side * (H.a + 16 * u), hc - 0.1 * HH]], front: false, swirl: true };
      case "lift": return { pts: [s, [X(20), s[1] - 0.25 * HH], [X(4), s[1] - 0.82 * HH]], front: false };
      case "shield": return { pts: [s, [X(4), s[1] + 0.4 * HH], [tcx + side * 0.6 * T.a, torsoBot - 0.1 * HH]], front: true };
      case "cross": return { pts: [s, [X(2), s[1] + 0.38 * HH], [tcx - side * 0.45 * T.a, s[1] + 0.32 * HH]], front: true };
      case "reach": { const lf = (opts.lift || 0) * 0.62 * HH; return { pts: [s, [X(42), s[1] - 0.12 * HH - lf * 0.6], [X(82), s[1] - 0.5 * HH - lf]], front: false }; }
      case "cheek": return { pts: [s, [X(16), s[1] + 0.05 * HH], [cx + side * (H.a + 2 * u), hc + 0.25 * H.b]], front: false };
      case "thumb": return { pts: [s, [X(20), s[1] + 0.12 * HH], [X(44), s[1] - 0.12 * HH]], front: false, thumb: true };
      default: return { pts: [s, [X(4), s[1] + 0.48 * HH], [X(3), chin + 1.04 * HH]], front: false };
    }
  };
  const arms = [arm(-1, L), arm(1, R)];
  const drawArm = (a) => {
    p.stroke(curve(a.pts[0], a.pts[1], a.pts[2]), 5.2 * u, armCol);
    const [hx, hy] = a.pts[2];
    p.dot(hx, hy, 5.5 * u);
    if (a.finger) { const dx = a.pts[2][0] - a.pts[1][0], dy = a.pts[2][1] - a.pts[1][1], l = Math.hypot(dx, dy); p.stroke([[hx, hy], [hx + dx / l * 14 * u, hy + dy / l * 14 * u]], 2.6 * u); }
    if (a.thumb) p.stroke([[hx, hy], [hx + Math.sign(hx - cx) * 6 * u, hy - 12 * u]], 2.6 * u);
  };
  // spear behind
  if (O.spear && R === "spear") {
    const [hx, hy] = arms[1].pts[2], s0 = [hx + 2 * u, sole - 2 * u], s1 = [hx - 3 * u, 70];
    p.band([s0, s1], old ? "#6d5236" : "#8a5a34", 4.2 * u, 1.4 * u, "round");
    const tip = [[s1[0] - 7 * u, s1[1] + 6 * u], [s1[0], s1[1] - 34 * u], [s1[0] + 7 * u, s1[1] + 6 * u], [s1[0], s1[1] + 14 * u]];
    p.poly(tip, old ? "#8b7c6a" : "#c9cfd6", 2 * u);
    if (web) cobweb(p, s1[0] - 2 * u, s1[1] + 60 * u, 70 * u, u);
  }
  for (const a of arms) if (!a.front) drawArm(a);
  // torso
  if (dress) {
    const D = { a: 0.5 * W * 0.98, b: 0.5 * ((sole - 0.35 * HH) - (chin - 0.2 * HH)), nTop: 2.0, nBot: 3.0, egg: 0.35, asym: 0, rot: 0, noise: 0.006, seed: seed + 9 };
    const dp = blobPts(cx, sole - 0.35 * HH - D.b, D);
    p.gradFill(dp, O.dress, mul(O.dress, SH_CLOTH), light); p.inkRing(dp, ow, thick);
  }
  // skirt / pteruges below the torso
  if (!dress) {
    const sk = [[tcx - 0.92 * T.a, torsoBot - 0.2 * HH], [tcx + 0.92 * T.a, torsoBot - 0.2 * HH], [tcx + 1.0 * T.a, torsoBot + 0.3 * HH], [tcx - 1.0 * T.a, torsoBot + 0.3 * HH]];
    p.gradFill(sk, O.tunic, mul(O.tunic, SH_CLOTH), light); p.poly(sk, null, ow * 0.8);
    if (O.armor) for (let i = -3; i <= 3; i++) { const x = tcx + i * 0.27 * T.a, st = [[x - 9 * u, torsoBot - 0.05 * HH], [x + 9 * u, torsoBot - 0.05 * HH], [x + 9 * u, torsoBot + 0.22 * HH], [x - 9 * u, torsoBot + 0.22 * HH]]; p.poly(st, old ? "#5e4632" : LEATHER, 1.6 * u); }
  }
  p.gradFill(tp, O.tunic, mul(O.tunic, SH_CLOTH), light);
  p.clip(tp, () => {
    if (O.armor) {
      const top = chin - 0.1 * HH, bot = torsoBot - 0.25 * HH, n = 5;
      for (let i = 0; i < n; i++) {
        const y0 = top + (bot - top) * i / n, y1 = top + (bot - top) * (i + 1) / n;
        const c = old ? (i % 2 ? "#8d8679" : "#9a9384") : (i % 2 ? "#a7b0ba" : "#bcc4cc");
        p.poly([[tcx - 1.5 * T.a, y0], [tcx + 1.5 * T.a, y0 + 3 * u], [tcx + 1.5 * T.a, y1 + 3 * u], [tcx - 1.5 * T.a, y1]], c, 1.8 * u);
      }
      p.band([[tcx - 1.4 * T.a, torsoBot - 0.2 * HH], [tcx + 1.4 * T.a, torsoBot - 0.2 * HH]], LEATHER, 0.08 * HH, 1.5 * u);
      for (let i = -2; i <= 2; i++) p.dot(tcx + i * 0.3 * T.a, torsoBot - 0.2 * HH, 2.4 * u, BRASS);
      if (old) for (let i = 0; i < 5; i++) p.ell(tcx + Math.sin(i * 1.7) * 0.7 * T.a, top + (bot - top) * ((i * 0.31) % 1), 6 * u, 3 * u, "#8a4b22", 0);
    } else {
      p.band([[tcx - 1.4 * T.a, torsoBot - 0.24 * HH], [tcx + 1.4 * T.a, torsoBot - 0.24 * HH]], O.apron ? "#5a3b2a" : "#e2c27a", 0.05 * HH, 1.2 * u);
      if (O.toga) p.band([[tcx - 1.0 * T.a, chin - 0.1 * HH], [tcx + 1.1 * T.a, torsoBot - 0.1 * HH]], O.toga, 0.16 * HH, 1.6 * u);
      if (O.apron) p.poly([[tcx - 0.55 * T.a, torsoBot - 0.2 * HH], [tcx + 0.55 * T.a, torsoBot - 0.2 * HH], [tcx + 0.6 * T.a, torsoBot + 0.2 * HH], [tcx - 0.6 * T.a, torsoBot + 0.2 * HH]], O.apron, 1.6 * u);
      p.stroke([[tcx - 0.2 * T.a, chin + 0.02 * HH], [tcx, chin + 0.16 * HH], [tcx + 0.2 * T.a, chin + 0.02 * HH]], 2 * u);
    }
  });
  p.inkRing(tp, ow, thick);
  if (O.armor) for (const s of [-1, 1]) { // shoulder plates
    const sp = ellPts(tcx + s * 0.72 * T.a, chin + 0.1 * HH, 0.42 * T.a, 0.13 * HH, 180, 360, s * 8, 20);
    p.poly(sp, old ? "#9a9384" : "#c5ccd3", 1.8 * u);
  }
  if (O.moss) {/* reserved */}
  for (const a of arms) if (a.front) drawArm(a);
  // shield in front, held by the left hand
  if (O.shield && L === "shield") {
    const sx = tcx - 0.55 * T.a, sy = torsoBot + 0.05 * HH, sw = 0.36 * W, sh = 0.78 * HH;
    const sp = rrect(sx - sw, sy - sh, sx + sw, sy + sh, 8 * u);
    p.gradFill(sp, "#c0302c", "#7d1d22", light);
    p.clip(sp, () => {
      p.band([[sx - sw, sy], [sx + sw, sy]], BRASS, 6 * u, 1.2 * u);
      p.band([[sx, sy - sh], [sx, sy + sh]], BRASS, 6 * u, 1.2 * u);
      for (const s of [-1, 1]) { p.stroke([[sx + s * 12 * u, sy - 14 * u], [sx + s * 34 * u, sy - 46 * u], [sx + s * 22 * u, sy - 44 * u], [sx + s * 46 * u, sy - 74 * u]], 3.5 * u, BRASS); p.stroke([[sx + s * 12 * u, sy + 14 * u], [sx + s * 34 * u, sy + 46 * u], [sx + s * 22 * u, sy + 44 * u], [sx + s * 46 * u, sy + 74 * u]], 3.5 * u, BRASS); }
      p.stroke(ellPts(sx - sw * 0.5, sy - sh * 0.7, sw * 0.3, sh * 0.1, 200, 320, 0, 10), 3 * u, "#ffffff44");
    });
    p.ell(sx, sy, 13 * u, 13 * u, "#e6c068", 2.2 * u);
    p.inkRing(sp, ow, thick);
  }
  // ---- head ----
  const [cpx, cpy] = rotAbout([cx, chin], rad(tilt), [cx, hipY]);
  const Ah = tilt + headTilt;
  p.rot = Ah ? [rad(Ah), cx, chin, cpx - cx, cpy - chin] : null;
  if (helmet) galea(p, H, cx, hc, light, thick, ow, old, u);
  const hp = blobPts(cx, hc, H);
  if (O.hair && !helmet) { const hb = blobPts(cx, hc - 0.03 * HH, { ...H, a: H.a * 1.04, b: H.b * 1.05 }); p.poly(hb, O.hair, 0); }
  p.shadedFill(hp, skin, mul(skin, SH_SKIN), light, H.a);
  p.inkRing(hp, ow, thick);
  if (helmet) {
    const bandY = hc - H.b * 0.42, bp = ellPts(cx, bandY, H.a * 1.05, H.b * 0.66, 180, 360, 0, 48);
    p.shadedFill(bp, old ? "#8f8a7e" : STEEL, mul(old ? "#8f8a7e" : STEEL, [0.62, 0.64, 0.72]), light, H.a, 0.4);
    p.clip(bp, () => { p.stroke(ellPts(cx - 20 * u, bandY - 0.3 * H.b, 0.25 * H.a, 0.18 * H.b, 200, 300, 0, 16), 5 * u, "#ffffff66");
      if (old) for (let i = 0; i < 9; i++) p.ell(cx + Math.sin(i * 2.3) * 0.8 * H.a, bandY - (0.08 + 0.5 * ((i * 0.37) % 1)) * H.b, (4 + (i % 3) * 2) * u, (2.5 + (i % 2)) * u, "#8a4b22", 0); });
    p.poly(bp, null, ow * 0.9);
    p.band([[cx - H.a * 1.05, bandY], [cx + H.a * 1.05, bandY]], old ? "#a88a4a" : BRASS, 7 * u, 1.8 * u, "round");
    p.poly(rrect(cx - 4 * u, bandY - 0.55 * H.b, cx + 4 * u, bandY - 3 * u, 2 * u), old ? "#a88a4a" : BRASS, 1.5 * u);
    cheeks(p, H, cx, hc, light, ow, old, u);
  } else if (O.cap) hatOn(p, { hat: "cap", cap: O.cap, jacket: O.tunic }, hp, H, cx, hc, light, seed, facing, false);
  else if (O.hair) hatOn(p, { hat: "hair", hair: O.hair, jacket: O.tunic }, hp, H, cx, hc, light, seed, facing, false);
  else if (O.helmet && nohelmet) { // bald old head with white side tufts
    for (const s of [-1, 1]) p.ell(cx + s * 0.9 * H.a, hc - 0.1 * H.b, 0.22 * H.a, 0.3 * H.b, "#f4f1ea", 3 * u);
  }
  if (O.beard) {
    const bd = blobPts(cx + 6 * u * facing, hc + 0.85 * H.b, { a: 0.62 * H.a, b: 0.75 * H.b, nTop: 2.4, nBot: 1.6, egg: -0.35, asym: 0, rot: 0, noise: 0.02, seed: seed + 4 });
    p.shadedFill(bd, O.beard, mul(O.beard, [0.86, 0.86, 0.92]), light, 0.6 * H.a, 0.3);
    p.clip(bd, () => { for (let i = -3; i <= 3; i++) p.stroke([[cx + i * 9 * u, hc + 0.45 * H.b], [cx + i * 7 * u, hc + 1.35 * H.b]], 1.2 * u, "#c9c4bb"); });
    p.inkRing(bd, ow * 0.8, thick);
  }
  faceFront(p, cx, hc, W, expr, facing, look, lid, helmet, skin, O.beard ? O.beard : O.moustache, !!O.stout);
  if (O.brows) for (const s of [-1, 1]) p.ell(cx + 7 * u * facing + s * 14 * u, hc - 20 * u, 11 * u, 5 * u, O.brows, 2 * u);
  if (O.beard) { // re-draw the mouth over the beard for open mouths
    if (expr === "shock" || expr === "snore") p.ell(cx + 8 * u * facing, hc + 22 * u, 6 * u, 7 * u, "#5a1e28", 2 * u);
  }
  p.rot = null;
  if (arms.some((a) => a.swirl)) { // cuckoo swirl next to the temple
    const a = arms.find((x) => x.swirl), [hx, hy] = a.pts[2], ph = opts.swirl || 0, pts = [];
    for (let i = 0; i < 40; i++) { const t = i / 40 * Math.PI * 4 + ph, r = (4 + i * 0.7) * u; pts.push([hx + Math.cos(t) * r, hy - 40 * u + Math.sin(t) * r]); }
    p.stroke(pts, 3 * u, "#ffffff"); p.stroke(pts, 1.4 * u, INK);
  }
};

/** loose helmet prop card (lifted off the old soldier) */
export const helmetCard = (p) => {
  const H = headBlob(3, 118, 0), u = 2 * H.a / 100, hc = 560, light = rad(-120), thick = thickAngle(light), ow = 5 * u;
  galea(p, H, 300, hc, light, thick, ow, true, u);
  const bandY = hc - H.b * 0.42, bp = ellPts(300, bandY, H.a * 1.05, H.b * 0.66, 180, 360, 0, 48);
  // dark inside visible from below
  p.ell(300, bandY, H.a * 1.05, 0.12 * H.b, "#2a221e", 0);
  p.shadedFill(bp, "#8f8a7e", mul("#8f8a7e", [0.62, 0.64, 0.72]), light, H.a, 0.4);
  p.clip(bp, () => { for (let i = 0; i < 9; i++) p.ell(300 + Math.sin(i * 2.3) * 0.8 * H.a, bandY - (0.08 + 0.5 * ((i * 0.37) % 1)) * H.b, (4 + (i % 3) * 2) * u, (2.5 + (i % 2)) * u, "#8a4b22", 0); });
  p.poly(bp, null, ow * 0.9);
  p.band([[300 - H.a * 1.05, bandY], [300 + H.a * 1.05, bandY]], "#a88a4a", 7 * u, 1.8 * u, "round");
  cheeks(p, H, 300, hc, light, ow, true, u);
};

/** ZZZ for the sleeping guard */
export const fxZ = (p, t) => {
  const g = p.g; g.save(); g.font = "900 120px Arial Black, Arial"; g.lineJoin = "round";
  for (let i = 0; i < 3; i++) {
    const k = (t + i / 3) % 1, x = 220 + i * 70 + Math.sin(k * 6) * 20, y = 700 - k * 500, s = 0.5 + k * 0.7;
    g.save(); g.translate(x, y); g.scale(s, s); g.globalAlpha = Math.min(1, (1 - k) * 2.5);
    g.lineWidth = 16; g.strokeStyle = INK; g.strokeText("Z", 0, 0); g.fillStyle = "#ffffff"; g.fillText("Z", 0, 0); g.restore();
  }
  g.restore();
};
/** falling leaf */
export const fxLeaf = (p, col) => { p.poly([[300, 380], [420, 470], [300, 620], [180, 470]], col, 14); p.stroke([[300, 400], [300, 600]], 8); };
/** dust cloud puff (k 0..1 growth) */
export const fxDust = (p, k, col = "#e8dcc4") => {
  const g = p.g; g.save(); g.globalAlpha = Math.max(0, 1 - k * k);
  const B = []; for (let i = 0; i < 9; i++) { const a = i / 9 * Math.PI * 2 + 0.3, r = 95 + 150 * k + (i % 3) * 22; B.push([300 + Math.cos(a) * r, 520 + Math.sin(a) * r * 0.62 - 30 * k, 92 + 50 * k + (i % 2) * 18, 80 + 42 * k + (i % 2) * 12]); }
  B.push([300, 500 - 40 * k, 150 + 90 * k, 120 + 60 * k]);
  for (const b of B) p.ell(b[0], b[1], b[2] + 7, b[3] + 7, INK, 0);          // dark underlay a little bigger -> ONE outline around the whole cloud
  for (const b of B) p.ell(b[0], b[1], b[2], b[3], col, 0);                    // flat fill on top
  g.globalAlpha *= 0.5; for (let i = 0; i < 4; i++) p.ell(235 + i * 42, 450 - 20 * k + (i % 2) * 36, 44, 30, "#fffaf0", 0);   // soft light on the top of the cloud (big, no dots)
  g.restore();
};
export const fxDrip = (p) => p.ell(300, 500, 40, 64, "#9fd4ff", 10);
export const fxWood = (p, seed) => { p.poly([[200, 420], [400, 400], [420, 560], [230, 600]], "#5b3d22", 14); p.stroke([[240, 450], [380, 440]], 6, "#3a2614"); p.ell(330, 520, 26, 18, "#4d7a32", 0); };

export const headCenter = (seed = 3) => { const H = headBlob(seed, 118, 0), HH = 2 * H.b; return 975 - 1.38 * HH - 1.08 * HH - H.b; };
// ---- the pig, drawn in the same inked/shaded card style as the cast (side view, faces LEFT) ----
export const PIGC = { body: "#f7a8b8", shade: [0.84, 0.66, 0.74], pink: "#f08aa0", pink2: "#e8708a", belly: "#ffd0d9", dark: "#e58fa4", bristle: "#d9728a", brow: "#c25c78", white: "#fff4ee", hoof: "#efe0cc", ink: INK };
const spiral = (cx, cy, t, wig) => { const pts = []; for (let i = 0; i <= 18; i++) { const a = i / 18 * 5.2 + wig, r = 20 - i * 0.8; pts.push([cx + Math.cos(a) * r * (1 - i / 40) + i * 1.2, cy - i * 2.2 + Math.sin(a) * r * 0.9]); } return pts; };
export const pigSideOld = (p, o = {}) => {
  const { state = "root", phase = 0, down = 0, blink = 0, ear = 0, tail = 0, expr = "normal", fall = 0, t = 0, light = rad(-120) } = o;
  const g = p.g, thick = thickAngle(light), ow = 6.5, u = 1.0;
  const trot = state === "trot" ? 1 : 0;
  const bob = trot * 7 * Math.cos(4 * Math.PI * phase) + (state === "root" ? 2.5 * Math.abs(Math.sin(t * 5.5)) : 0);
  const bodyC = [320, 742 + bob];
  g.save();
  if (fall > 0) { const ang = -fall * Math.PI * 0.96; g.translate(bodyC[0], bodyC[1]); g.rotate(ang); g.translate(-bodyC[0], -bodyC[1]); }
  p.rot = null;
  const legs = [{ x: 205, ph: 0 }, { x: 255, ph: 0.5 }, { x: 395, ph: 0.5 }, { x: 445, ph: 0 }];
  const drawLeg = (L, back) => {
    const sw = trot * Math.sin(2 * Math.PI * (phase + L.ph)) * 34, lift = trot * Math.max(0, Math.cos(2 * Math.PI * (phase + L.ph))) * 24;
    const hip = [L.x, 790 + bob], knee = [L.x + sw * 0.55 + (fall ? (L.x < 330 ? -30 : 30) : 0), 868 + bob * 0.4 - lift * 0.6], foot = [L.x + sw + (fall ? (L.x < 330 ? -44 : 46) : 0), 958 - lift - (fall ? 30 : 0)];
    const col = back ? PIGC.dark : PIGC.body;
    p.line([hip, knee, foot], col, 44 - (back ? 4 : 0));
    p.poly(rrect(foot[0] - 22, foot[1] - 26, foot[0] + 20, foot[1] + 10, 8), PIGC.white, 5);
    p.ell(foot[0] - 2, foot[1] + 8, 24, 11, PIGC.hoof, 4);
  };
  drawLeg(legs[1], true); drawLeg(legs[3], true);
  // tail (curly, wiggles)
  p.line(spiral(515, 690 + bob, t, tail), PIGC.body, 11);
  // body
  const body = blobPts(bodyC[0], bodyC[1], { a: 228, b: 128, nTop: 2.4, nBot: 2.05, egg: 0.06, asym: -0.04, rot: 0, noise: 0.012, seed: 17 }, 90);
  p.gradFill(body, PIGC.body, mul(PIGC.body, PIGC.shade), light, 0.2);
  p.clip(body, () => {
    p.ell(300, 868 + bob, 210, 52, PIGC.belly, 0);                               // lighter belly
    p.stroke([[170, 650 + bob], [250, 626 + bob], [370, 628 + bob], [470, 660 + bob]], 12, "#ffffff55");   // back light
    for (let i = 0; i < 4; i++) p.stroke([[420 + i * 8, 660 + i * 22 + bob], [446 + i * 5, 690 + i * 22 + bob]], 3, "#00000022");
    p.ell(450, 742 + bob, 78, 88, "#c8587014", 0);
  });
  p.inkRing(body, ow * 0.85, thick);
  // bristle ridge
  for (let i = 0; i < 9; i++) { const x = 190 + i * 38; p.poly([[x - 9, 622 + 2 * Math.abs(i - 4) + bob], [x + 2, 598 + 2 * Math.abs(i - 4) + bob + Math.sin(t * 6 + i) * 2], [x + 11, 624 + 2 * Math.abs(i - 4) + bob]], PIGC.bristle, 3); }
  drawLeg(legs[0], false); drawLeg(legs[2], false);
  // ---- head ----
  const hd = (state === "root" ? 52 + 22 * Math.sin(t * 5.5) : state === "alert" ? -28 : state === "trot" ? -6 : 0) + down;
  const hc = [118, 742 + bob + hd];
  const neck = blobPts(172, 742 + bob + hd * 0.5, { a: 78, b: 98, nTop: 2.2, nBot: 2.2, egg: 0, asym: 0, rot: 0, noise: 0.01, seed: 3 }, 50);
  p.gradFill(neck, PIGC.body, mul(PIGC.body, PIGC.shade), light, 0.2); p.inkRing(neck, ow * 0.7, thick);
  const head = blobPts(hc[0], hc[1], { a: 96, b: 88, nTop: 2.3, nBot: 2.0, egg: -0.1, asym: -0.04, rot: rad(-6), noise: 0.012, seed: 9 }, 70);
  p.gradFill(head, PIGC.body, mul(PIGC.body, PIGC.shade), light, 0.2);
  // snout + disc + nostrils
  const sn = blobPts(hc[0] - 98, hc[1] + 26, { a: 52, b: 40, nTop: 2.4, nBot: 2.2, egg: 0, asym: 0, rot: 0, noise: 0.008, seed: 5 }, 40);
  p.gradFill(sn, PIGC.pink, mul(PIGC.pink, [0.86, 0.8, 0.88]), light, 0.2); p.inkRing(sn, ow * 0.8, thick);
  const disc = blobPts(hc[0] - 138, hc[1] + 24, { a: 16, b: 34, nTop: 2.2, nBot: 2.2, egg: 0, asym: 0, rot: 0, noise: 0, seed: 6 }, 24);
  p.poly(disc, PIGC.pink2, 5);
  p.ell(hc[0] - 142, hc[1] + 12, 5, 9, INK, 0); p.ell(hc[0] - 142, hc[1] + 36, 5, 9, INK, 0);
  p.inkRing(head, ow * 0.85, thick);
  p.stroke([[hc[0] - 92, hc[1] + 56], [hc[0] - 60, hc[1] + 62], [hc[0] - 28, hc[1] + 52]], 4, INK);        // mouth
  if (expr === "happy") p.arc(hc[0] - 60, hc[1] + 50, 34, 18, 10, 170, 5, INK);
  // cheek blush
  p.ell(hc[0] - 34, hc[1] + 30, 20, 13, "#ff8fa8", 0);
  p.inkRing(head, ow * 0.85, thick);
  // eye
  const ex = hc[0] - 52, ey = hc[1] - 18;
  if (fall > 0.4 || expr === "x") { p.stroke([[ex - 14, ey - 14], [ex + 14, ey + 14]], 6, INK); p.stroke([[ex + 14, ey - 14], [ex - 14, ey + 14]], 6, INK); }
  else if (blink > 0.5 || expr === "sleep") p.stroke([[ex - 16, ey], [ex, ey + 6], [ex + 16, ey]], 6, INK);
  else { p.ell(ex, ey, 18, 20, "#ffffff", 4); p.ell(ex - 3, ey + 1, 11, 13, "#4a2c1c", 0); p.ell(ex - 4, ey + 1, 6, 8, INK, 0); p.dot(ex - 8, ey - 5, 3.2, "#ffffff"); }
  p.stroke([[ex - 22, ey - 28 - (expr === "alert" ? 6 : 0)], [ex + 2, ey - 34], [ex + 22, ey - 24]], 7, PIGC.brow);       // brow
  // ears: front ear flops over the head, back ear peeks behind
  const ea = ear * 14 + (state === "trot" ? 10 : 0) + (state === "alert" ? -16 : 0);
  const earBack = [[hc[0] + 20, hc[1] - 70], [hc[0] + 66, hc[1] - 120 - ea * 0.2], [hc[0] + 98, hc[1] - 60 + ea], [hc[0] + 52, hc[1] - 56]];
  p.poly(earBack, PIGC.dark, ow * 0.7);
  const earF = [[hc[0] - 4, hc[1] - 74], [hc[0] + 18, hc[1] - 132 - ea * 0.3], [hc[0] + 78, hc[1] - 94 + ea * 0.5], [hc[0] + 70, hc[1] - 18 + ea], [hc[0] + 36, hc[1] - 36]];
  p.gradFill(earF, PIGC.body, mul(PIGC.body, PIGC.shade), light, 0.2); p.inkRing(earF, ow * 0.7, thick);
  p.poly([[hc[0] + 14, hc[1] - 78], [hc[0] + 28, hc[1] - 112 - ea * 0.2], [hc[0] + 58, hc[1] - 86 + ea * 0.4], [hc[0] + 52, hc[1] - 40 + ea], [hc[0] + 36, hc[1] - 52]], PIGC.pink2, 0);
  if (o.angel) {
    const wf = Math.sin(t * 7) * 18;
    for (const k of [0, 1]) { const w = [[330 + k * 40, 660 + bob], [300 + k * 40, 540 - wf + bob], [380 + k * 40, 500 - wf * 1.2 + bob], [430 + k * 40, 590 - wf * 0.6 + bob], [410 + k * 40, 660 + bob]]; p.gradFill(w, "#ffffff", "#cfe0f5", light, 0.2); p.inkRing(w, ow * 0.7, thick); }
    p.ell(hc[0] + 10, hc[1] - 150, 52, 14, null, 8); p.ell(hc[0] + 10, hc[1] - 150, 52, 14, "#ffe08a", 5);
  }
  g.restore();
};
export const fxZZ = 0;

// ---- "O PORQUINHO" — the user-approved pig design (round head, pointy ears, big snout, blush, thin dark legs). Faces LEFT (flip in the card).
// expressions: principal (smile + tongue) | eat (happy eyes + potato) | scared | neutral | dead (X eyes). state picks one if expr is not given.
export const PIGT = { body: "#ffb6d2", belly: "#ffcce0", earIn: "#ff8fb8", snout: "#ff9cc2", nostril: "#7a2c45", cheek: "#ff95ba", mouthIn: "#6b1f2f", leg: "#2e1c1e", potato: "#c49a5a", tongue: "#e8717a", shadow: "#d6d1cb" };
export const pigToon = (p, o = {}) => {
  const g = p.g, { state = "stand", phase = 0, blink = 0, ear = 0, tail = 0, fall = 0, t = 0 } = o;
  const expr = o.expr && o.expr !== "normal" ? o.expr : state === "root" ? "eat" : state === "alert" ? "scared" : state === "trot" ? "principal" : state === "fall" ? "dead" : "neutral";
  const trot = state === "trot" ? 1 : 0, bob = trot * 7 * Math.abs(Math.sin(2 * Math.PI * phase * 2)) + (state === "root" ? 3 * Math.abs(Math.sin(t * 5.5)) : 0);
  const bc = [350, 742 - bob], OL = 9;
  g.save(); p.rot = null;
  p.ell(330, 962 + (fall > 0 ? 6 : 0), 270, 26, PIGT.shadow, 0);
  if (fall > 0) { const f = Math.min(1, fall), e = f * f * (3 - 2 * f), sy = Math.cos(f * Math.PI), Y0 = bc[1] + (843 - bc[1]) * e; g.translate(0, Y0); g.scale(1, Math.abs(sy) < 0.04 ? 0.04 : sy); g.translate(0, -bc[1]); }
  // legs: thin dark sticks with little feet; diagonal pairs swing when trotting
  const leg = (x, ph, back) => { const sw = trot * Math.sin(2 * Math.PI * (phase + ph)) * 20 + (fall >= 1 ? Math.sin(t * 11 + ph * 6) * 14 : 0), lift = trot * Math.max(0, Math.cos(2 * Math.PI * (phase + ph))) * 22; const hip = [x, bc[1] + 112], foot = [x + sw, 950 - lift - (fall > 0 ? 40 : 0)]; p.stroke([hip, [x + sw * 0.5, (hip[1] + foot[1]) / 2], foot], 15, PIGT.leg); p.ell(foot[0] + (back ? 4 : -4), foot[1] + 6, 20, 9, PIGT.leg, 0); };
  leg(250, 0.5, true); leg(470, 0, true);
  // tail: out of the rump, up, then a big loop (as in the reference sheet)
  { const tw = Math.sin(t * 8) * 4 + tail * 6; const B = [bc[0] + 184, bc[1] - 14]; const pts = [B, [B[0] + 30, B[1] - 20 + tw * 0.3], [B[0] + 46, B[1] - 56 + tw]];
    const C = [B[0] + 28 + tw * 0.5, B[1] - 84]; for (let i = 0; i <= 22; i++) { const a = (-20 + i * 17) * Math.PI / 180, r = 26 - i * 0.55; pts.push([C[0] + Math.cos(a) * r, C[1] - Math.sin(a) * r]); }
    p.stroke(pts, 10, PIGT.leg); }
  // body
  p.ell(bc[0], bc[1], 192, 132, PIGT.body, OL);
  p.clip(blobPts(bc[0], bc[1], { a: 188, b: 128, nTop: 2, nBot: 2, egg: 0, asym: 0, rot: 0, noise: 0, seed: 1 }, 70), () => { p.ell(bc[0] - 10, bc[1] + 52, 150, 70, PIGT.belly, 0); p.stroke([[bc[0] - 150, bc[1] - 70], [bc[0] - 90, bc[1] - 112], [bc[0] + 10, bc[1] - 124]], 16, "#ffffffaa"); });
  p.ell(bc[0], bc[1], 192, 132, null, OL);
  leg(215, 0, false); leg(505, 0.5, false);
  // head (big round, overlapping the front of the body)
  const hd = (state === "root" ? 26 + 18 * Math.sin(t * 5.5) : state === "alert" ? -22 : 0), hc = [168, 712 - bob * 0.6 + hd];
  const ew = ear * 12 + (trot ? 8 : 0) + (state === "alert" ? -10 : 0);
  for (const s of [-1, 1]) {   // ears first (behind the head)
    const base = [[hc[0] + s * 96, hc[1] - 70], [hc[0] + s * (116 + ew * 0.3), hc[1] - 188 + ew * 0.4], [hc[0] + s * 22, hc[1] - 118]];
    p.poly(base, PIGT.body, OL); p.poly([[hc[0] + s * 84, hc[1] - 92], [hc[0] + s * (100 + ew * 0.2), hc[1] - 164 + ew * 0.3], [hc[0] + s * 38, hc[1] - 118]], PIGT.earIn, 0);
    { const ax = hc[0] + s * (116 + ew * 0.3), ay = hc[1] - 188 + ew * 0.4; p.stroke([[ax - s * 14, ay + 6], [ax + s * 6, ay - 6], [ax + s * 22, ay + 10]], 8, PIGT.leg); p.stroke([[ax - s * 8, ay + 14], [ax + s * 8, ay + 6]], 6, PIGT.earIn); }
  }
  p.ell(hc[0], hc[1], 128, 126, PIGT.body, OL);
  p.stroke([[hc[0] - 92, hc[1] - 52], [hc[0] - 64, hc[1] - 92], [hc[0] - 20, hc[1] - 108]], 14, "#ffffffbb");   // shine
  for (const s of [-1, 1]) p.ell(hc[0] + s * 84, hc[1] + 30, 30, 19, PIGT.cheek, 0);                           // blush
  // eyes
  const ex = (s) => [hc[0] + s * 50, hc[1] - 22];
  for (const s of [-1, 1]) {
    const [x, y] = ex(s);
    if (expr === "dead") { p.stroke([[x - 16, y - 16], [x + 16, y + 16]], 7, INK); p.stroke([[x + 16, y - 16], [x - 16, y + 16]], 7, INK); }
    else if (expr === "eat" || blink > 0.5) p.arc(x, y + 4, 18, 14, 200, 340, 7, INK);
    else if (expr === "scared") { p.ell(x, y, 22, 24, "#ffffff", 6); p.ell(x + (s > 0 ? -3 : 3), y + 2, 9, 11, INK, 0); p.arc(x, y - 36, 24, 14, 200, 340, 6, INK); }
    else { const r = expr === "neutral" ? 12 : 21; p.ell(x, y, r, r * 1.05, "#2b1a22", 0); p.dot(x - r * 0.3, y - r * 0.35, r * 0.28, "#ffffff"); }
  }
  // snout
  p.ell(hc[0], hc[1] + 38, 66, 44, PIGT.snout, OL);
  p.ell(hc[0] - 22, hc[1] + 36, 11, 18, PIGT.nostril, 0); p.ell(hc[0] + 22, hc[1] + 36, 11, 18, PIGT.nostril, 0);
  // mouth
  if (expr === "scared" || expr === "dead") p.ell(hc[0], hc[1] + 104, 16, 22, PIGT.mouthIn, 5);
  else if (expr === "principal") { p.arc(hc[0], hc[1] + 96, 36, 16, 20, 160, 7, INK); p.ell(hc[0] + 6, hc[1] + 112, 9, 12, PIGT.tongue, 3); }
  else if (expr === "eat") { p.arc(hc[0], hc[1] + 96, 28, 12, 20, 160, 6, INK); p.ell(hc[0] + 26, hc[1] + 96, 36, 25, PIGT.potato, 6); for (const [dx, dy] of [[14, -4], [30, 6], [40, -6]]) p.dot(hc[0] + dx + 8, hc[1] + 96 + dy, 3, "#7a5a2a"); }
  else p.arc(hc[0], hc[1] + 98, 24, 10, 20, 160, 6, INK);
  // angel extras
  if (o.angel) {
    const wf = Math.sin(t * 7) * 16;
    for (const k of [0, 1]) for (let i = 0; i < 4; i++) { const wx = bc[0] + 20 + k * 46 + i * 12, wy = bc[1] - 120 - i * 20 - wf * (0.4 + i * 0.25); p.ell(wx, wy, 56 - i * 6, 24, "#ffffff", 7); }
    p.ell(hc[0], hc[1] - 178, 62, 15, null, 9); p.ell(hc[0], hc[1] - 178, 62, 15, "#ffe08a", 5);
  }
  g.restore();
};

export const pigSide = (p, o = {}) => pigToon(p, o);
// ---- ANIMAL CATALOG (2D, same inked/shaded card style as the cast). Side view, faces LEFT, soles at y=975.
// usage:  T.animalSide(p, { species: 'pig'|'cow'|'horse'|'sheep'|'goat'|'dog'|'cat'|'donkey', state: 'stand'|'root'|'trot'|'alert'|'fall', phase, down, blink, ear, tail, expr, fall, t, angel })
//         T.birdSide(p, { species: 'chicken'|'rooster'|'duck'|'goose'|'gull', state: 'stand'|'peck'|'walk'|'fly', phase, blink, t })
const AN = {
  pig:    { body: "#f7a8b8", shade: [0.84, 0.66, 0.74], belly: "#ffd0d9", dark: "#e58fa4", snout: "#f08aa0", nose: "#e8708a", ear: "pig", tail: "curl", hoof: "#efe0cc", sock: null, a: 228, b: 128, hipY: 790, kneeY: 868, legW: 44, neck: 78, head: { a: 96, b: 88, sn: 52, sh: 40 }, extra: "bristle" },
  cow:    { body: "#fbf7f0", shade: [0.82, 0.8, 0.88], belly: "#ffe3e8", dark: "#d8d2ca", snout: "#f4b6c0", nose: "#e8909e", ear: "cow", tail: "long", hoof: "#3a3238", sock: null, a: 245, b: 140, hipY: 770, kneeY: 860, legW: 46, neck: 92, head: { a: 92, b: 92, sn: 60, sh: 48 }, extra: "cowspots", horns: true, udder: true },
  bear:   { body: "#7a4e30", shade: [0.7, 0.6, 0.62], belly: "#8f6040", dark: "#5a361f", snout: "#a8764f", nose: "#2a1810", ear: "cow", tail: "stub", hoof: "#3a2418", sock: null, a: 235, b: 150, hipY: 770, kneeY: 860, legW: 54, neck: 84, head: { a: 92, b: 88, sn: 54, sh: 46 } },
  horse:  { body: "#a25f36", shade: [0.72, 0.62, 0.62], belly: "#b7774a", dark: "#7a4526", snout: "#8a4f2c", nose: "#3a2418", ear: "point", tail: "flow", hoof: "#3a2f2a", sock: "#f4eee4", a: 215, b: 105, hipY: 700, kneeY: 835, legW: 34, neck: 70, head: { a: 70, b: 98, sn: 92, sh: 40 }, mane: "#3a2418", tall: true },
  sheep:  { body: "#f6f2ea", shade: [0.82, 0.8, 0.9], belly: "#efe9dd", dark: "#d9d3c8", snout: "#3d343b", nose: "#2b2430", ear: "sheep", tail: "stub", hoof: "#2b2430", sock: null, a: 205, b: 120, hipY: 820, kneeY: 890, legW: 30, neck: 60, head: { a: 70, b: 72, sn: 40, sh: 34 }, wool: true, face: "#3d343b" },
  goat:   { body: "#efe3cf", shade: [0.8, 0.74, 0.8], belly: "#f7efe0", dark: "#cdbfa8", snout: "#e3d3ba", nose: "#4a3a30", ear: "goat", tail: "up", hoof: "#4a3a30", sock: null, a: 190, b: 100, hipY: 790, kneeY: 870, legW: 30, neck: 62, head: { a: 66, b: 74, sn: 44, sh: 30 }, horns: true, beard: true },
  dog:    { body: "#d49a5c", shade: [0.76, 0.66, 0.7], belly: "#f4e2c4", dark: "#a8703a", snout: "#e9c28f", nose: "#2b2430", ear: "floppy", tail: "wag", hoof: "#f4e2c4", sock: null, a: 170, b: 90, hipY: 800, kneeY: 880, legW: 28, neck: 54, head: { a: 70, b: 70, sn: 44, sh: 32 }, patch: "#f4e2c4" },
  cat:    { body: "#ec9a44", shade: [0.78, 0.62, 0.62], belly: "#fbe3c0", dark: "#c0702a", snout: "#fbe3c0", nose: "#f08aa0", ear: "pointcat", tail: "catlong", hoof: "#fbe3c0", sock: null, a: 150, b: 74, hipY: 840, kneeY: 905, legW: 24, neck: 46, head: { a: 62, b: 58, sn: 26, sh: 24 }, stripes: true, whiskers: true },
  donkey: { body: "#9a958f", shade: [0.74, 0.7, 0.78], belly: "#d8d2c8", dark: "#6e6a66", snout: "#e1dad0", nose: "#3a3330", ear: "long", tail: "tuft", hoof: "#3a3330", sock: null, a: 200, b: 100, hipY: 760, kneeY: 860, legW: 32, neck: 66, head: { a: 74, b: 84, sn: 70, sh: 36 }, mane: "#6e6a66" },
};

// animais sem desenho 2D proprio: derivados de um parecido, com cor e orelha certas (antes: travava com "hipY")
Object.assign(AN, {
  wolf:     { ...AN.dog, body: "#8a8f98", belly: "#d8dce2", dark: "#5f646c", snout: "#c9ccd2", ear: "pointcat", tail: "long" },
  fox:      { ...AN.dog, body: "#e0782a", belly: "#fbeede", dark: "#a8501a", snout: "#fbeede", ear: "pointcat", tail: "flow" },
  deer:     { ...AN.goat, body: "#b07a48", belly: "#efe0c8", dark: "#7e5530", snout: "#d9b48a", nose: "#2b2430", tail: "stub", horns: true },
  rabbit:   { ...AN.cat, body: "#e8e2da", belly: "#ffffff", dark: "#bdb4aa", snout: "#ffffff", ear: "long", tail: "stub" },
  lion:     { ...AN.dog, body: "#d9a24a", belly: "#f2d49a", dark: "#a8742c", snout: "#f2d49a", ear: "pointcat", tail: "tuft", a: 220, b: 118, mane: "#8a4f1c" },
  elephant: { ...AN.cow, body: "#9aa0a8", belly: "#b6bbc2", dark: "#70757c", snout: "#9aa0a8", nose: "#70757c", ear: "cow", tail: "tuft", udder: false, horns: false, extra: null },
});

export const animalSide = (p, o = {}) => {
  if ((o.species || "pig") === "pig") return pigToon(p, o);
  const A = AN[o.species || "pig"], g = p.g, light = o.light ?? rad(-120), thick = thickAngle(light), ow = 6.5;
  const { state = "stand", phase = 0, down = 0, blink = 0, ear = 0, tail = 0, expr = "normal", fall = 0, t = 0 } = o;
  const trot = state === "trot" ? 1 : 0, root = state === "root";
  const bob = trot * 7 * Math.cos(4 * Math.PI * phase) + (root ? 2.5 * Math.abs(Math.sin(t * 5.5)) : 0);
  const bodyC = [320, A.hipY - 48 + bob];
  g.save();
  if (fall > 0) { const ang = -fall * Math.PI * 0.96; g.translate(bodyC[0], bodyC[1]); g.rotate(ang); g.translate(-bodyC[0], -bodyC[1]); }
  p.rot = null;
  const legX = [bodyC[0] - A.a * 0.58, bodyC[0] - A.a * 0.32, bodyC[0] + A.a * 0.38, bodyC[0] + A.a * 0.62];
  const drawLeg = (x, ph, back) => {
    const sw = trot * Math.sin(2 * Math.PI * (phase + ph)) * 34, lift = trot * Math.max(0, Math.cos(2 * Math.PI * (phase + ph))) * 24;
    const hip = [x, A.hipY + bob], knee = [x + sw * 0.55 + (fall ? (x < 330 ? -30 : 30) : 0), A.kneeY + bob * 0.4 - lift * 0.6], foot = [x + sw + (fall ? (x < 330 ? -44 : 46) : 0), 958 - lift - (fall ? 30 : 0)];
    p.line([hip, knee, foot], back ? A.dark : A.body, A.legW - (back ? 4 : 0));
    if (A.sock) p.poly(rrect(foot[0] - A.legW * 0.5, foot[1] - 30, foot[0] + A.legW * 0.5, foot[1] + 8, 8), A.sock, 5);
    p.ell(foot[0] - 2, foot[1] + 8, A.legW * 0.55, 11, A.hoof, 4);
  };
  drawLeg(legX[1], 0.5, true); drawLeg(legX[3], 0, true);
  // tail
  const tb = [bodyC[0] + A.a - 12, bodyC[1] - 52];
  if (A.tail === "curl") { const pts = []; for (let i = 0; i <= 18; i++) { const a = i / 18 * 5.2 + tail, r = 20 - i * 0.8; pts.push([tb[0] + 8 + Math.cos(a) * r * (1 - i / 40) + i * 1.2, tb[1] - 40 - i * 2.2 + Math.sin(a) * r * 0.9]); } p.line(pts, A.body, 11); }
  if (A.tail === "long" || A.tail === "flow" || A.tail === "tuft") { const L = A.tail === "flow" ? 230 : 190; const sway = Math.sin(t * 3) * 14 + tail * 20; const pts = [[tb[0], tb[1] + 20], [tb[0] + 26 + sway * 0.3, tb[1] + L * 0.4], [tb[0] + 16 + sway, tb[1] + L * 0.85]]; p.line(pts, A.tail === "flow" ? A.mane : A.dark, A.tail === "flow" ? 22 : 9); p.ell(pts[2][0], pts[2][1] + 10, A.tail === "flow" ? 26 : 22, A.tail === "flow" ? 40 : 30, A.tail === "flow" ? A.mane : "#3a2f2a", 5); }
  if (A.tail === "stub") p.ell(tb[0] + 6, tb[1] + 16, 20, 26, A.body, 5);
  if (A.tail === "up") p.line([[tb[0], tb[1] + 20], [tb[0] + 22, tb[1] - 36], [tb[0] + 34, tb[1] - 46 + Math.sin(t * 6) * 4]], A.body, 14);
  if (A.tail === "wag") p.line([[tb[0], tb[1] + 20], [tb[0] + 34, tb[1] - 40 + Math.sin(t * 14) * 10], [tb[0] + 56, tb[1] - 84 + Math.sin(t * 14) * 18]], A.body, 16);
  if (A.tail === "catlong") p.line([[tb[0], tb[1] + 30], [tb[0] + 60, tb[1] + 10 + Math.sin(t * 3) * 8], [tb[0] + 92, tb[1] - 80], [tb[0] + 78 + Math.sin(t * 3) * 10, tb[1] - 150]], A.body, 16);
  // body
  const body = blobPts(bodyC[0], bodyC[1], { a: A.a, b: A.b, nTop: 2.4, nBot: 2.05, egg: 0.06, asym: -0.04, rot: 0, noise: A.wool ? 0.03 : 0.012, seed: 17 }, A.wool ? 120 : 90);
  p.gradFill(body, A.body, mul(A.body, A.shade), light, 0.2);
  p.clip(body, () => {
    p.ell(bodyC[0] - 20, bodyC[1] + A.b * 0.78, A.a * 0.92, A.b * 0.42, A.belly, 0);
    p.stroke([[bodyC[0] - A.a * 0.7, bodyC[1] - A.b * 0.8], [bodyC[0] - A.a * 0.3, bodyC[1] - A.b * 0.95], [bodyC[0] + A.a * 0.3, bodyC[1] - A.b * 0.93], [bodyC[0] + A.a * 0.8, bodyC[1] - A.b * 0.6]], 12, "#ffffff44");
    if (A.extra === "cowspots") { for (const [x, y, rx, ry] of [[-110, -40, 62, 48], [20, -70, 54, 40], [120, 10, 70, 54], [-30, 40, 40, 30]]) p.ell(bodyC[0] + x, bodyC[1] + y, rx, ry, "#2b2530", 0); }
    if (A.patch) p.ell(bodyC[0] + 40, bodyC[1] - 20, 58, 44, A.patch, 0);
    if (A.stripes) for (let i = 0; i < 6; i++) p.stroke([[bodyC[0] - 100 + i * 36, bodyC[1] - A.b], [bodyC[0] - 90 + i * 36, bodyC[1] - A.b * 0.2]], 8, A.dark);
    if (A.wool) for (let i = 0; i < 14; i++) p.ell(bodyC[0] - 190 + i * 28, bodyC[1] - A.b * 0.7 + (i % 3) * 14, 26, 22, "#ffffff55", 0);
  });
  p.inkRing(body, ow * 0.85, thick);
  if (A.wool) for (let i = 0; i < 16; i++) { const a = i / 16 * Math.PI * 2; if (Math.sin(a) < 0.2) p.ell(bodyC[0] + Math.cos(a) * A.a * 0.98, bodyC[1] + Math.sin(a) * A.b * 0.98, 26, 24, A.body, 4); }
  if (A.extra === "bristle") for (let i = 0; i < 9; i++) { const x = bodyC[0] - 130 + i * 38; p.poly([[x - 9, bodyC[1] - 120 + 2 * Math.abs(i - 4)], [x + 2, bodyC[1] - 144 + 2 * Math.abs(i - 4) + Math.sin(t * 6 + i) * 2], [x + 11, bodyC[1] - 118 + 2 * Math.abs(i - 4)]], "#d9728a", 3); }
  if (A.mane) { for (let i = 0; i < 7; i++) { const x = bodyC[0] - A.a * 0.8 + i * 16; p.poly([[x, bodyC[1] - A.b * 0.9], [x - 18 + Math.sin(t * 4 + i) * 5, bodyC[1] - A.b * 0.9 - 54], [x + 24, bodyC[1] - A.b * 0.85]], A.mane, 4); } }
  if (A.udder) p.ell(bodyC[0] + 90, bodyC[1] + A.b - 6, 34, 26, "#f4b6c0", 5);
  drawLeg(legX[0], 0, false); drawLeg(legX[2], 0.5, false);
  // neck + head
  const H = A.head, hd = (root ? 52 + 22 * Math.sin(t * 5.5) : state === "alert" ? -28 : state === "trot" ? -6 : 0) + down;
  const hx = bodyC[0] - A.a - (A.tall ? 40 : 10), hy = bodyC[1] - (A.tall ? 70 : 0) + hd;
  const neckPts = blobPts(bodyC[0] - A.a + 40, bodyC[1] - (A.tall ? 60 : 0) + hd * 0.5, { a: A.neck, b: A.tall ? 120 : 98, nTop: 2.2, nBot: 2.2, egg: 0, asym: 0, rot: A.tall ? rad(-24) : 0, noise: 0.01, seed: 3 }, 50);
  p.gradFill(neckPts, A.body, mul(A.body, A.shade), light, 0.2); p.inkRing(neckPts, ow * 0.7, thick);
  const head = blobPts(hx, hy, { a: H.a, b: H.b, nTop: 2.3, nBot: 2.0, egg: -0.1, asym: -0.04, rot: A.tall ? rad(24) : rad(-6), noise: 0.012, seed: 9 }, 70);
  const faceCol = A.face || A.body;
  p.gradFill(head, faceCol, mul(faceCol, A.shade), light, 0.2);
  const sn = blobPts(hx - H.a - H.sn * 0.5 + 12, hy + (A.tall ? 38 : 26), { a: H.sn, b: H.sh, nTop: 2.4, nBot: 2.2, egg: 0, asym: 0, rot: A.tall ? rad(12) : 0, noise: 0.008, seed: 5 }, 40);
  p.gradFill(sn, A.snout, mul(A.snout, [0.86, 0.8, 0.88]), light, 0.2); p.inkRing(sn, ow * 0.8, thick);
  if (A.ear === "pig" || A.species === "pig" || (o.species || "pig") === "pig") { const disc = blobPts(hx - H.a - H.sn * 0.9, hy + 24, { a: 16, b: 34, nTop: 2.2, nBot: 2.2, egg: 0, asym: 0, rot: 0, noise: 0, seed: 6 }, 24); p.poly(disc, A.nose, 5); p.ell(hx - H.a - H.sn - 4, hy + 12, 5, 9, INK, 0); p.ell(hx - H.a - H.sn - 4, hy + 36, 5, 9, INK, 0); }
  else p.ell(hx - H.a - H.sn + 18, hy + (A.tall ? 44 : 22), 9, 11, A.nose, 0);
  p.inkRing(head, ow * 0.85, thick);
  p.stroke([[hx - H.a + 4, hy + 56], [hx - H.a + 36, hy + 62], [hx - H.a + 68, hy + 52]], 4, INK);
  if (expr === "happy") p.arc(hx - H.a + 36, hy + 50, 34, 18, 10, 170, 5, INK);
  // horns / beard
  if (A.horns) { const hc = A.species === "goat" || (o.species === "goat") ? "#d8cdb8" : "#f0e6cf"; p.line([[hx + 6, hy - H.b + 6], [hx + 16, hy - H.b - 40], [hx - (o.species === "goat" ? -22 : 8), hy - H.b - 70]], hc, 16); }
  if (A.beard) p.poly([[hx - H.a + 24, hy + 52], [hx - H.a + 50, hy + 112 + Math.sin(t * 3) * 4], [hx - H.a + 66, hy + 52]], "#f4ecdc", 5);
  if (A.whiskers) for (const k of [-1, 0, 1]) { p.stroke([[hx - H.a - 6, hy + 28 + k * 8], [hx - H.a - 56, hy + 20 + k * 18]], 3, INK); }
  // eye
  const ex = hx - H.a * 0.5, ey = hy - H.b * 0.2;
  if (fall > 0.4 || expr === "x") { p.stroke([[ex - 14, ey - 14], [ex + 14, ey + 14]], 6, INK); p.stroke([[ex + 14, ey - 14], [ex - 14, ey + 14]], 6, INK); }
  else if (blink > 0.5 || expr === "sleep") p.stroke([[ex - 16, ey], [ex, ey + 6], [ex + 16, ey]], 6, INK);
  else { p.ell(ex, ey, 18, 20, "#ffffff", 4); p.ell(ex - 3, ey + 1, 11, 13, "#4a2c1c", 0); p.ell(ex - 4, ey + 1, 6, 8, INK, 0); p.dot(ex - 8, ey - 5, 3.2, "#ffffff"); }
  p.stroke([[ex - 22, ey - 28 - (expr === "alert" ? 6 : 0)], [ex + 2, ey - 34], [ex + 22, ey - 24]], 7, A.dark);
  // ears
  const ea = ear * 14 + (state === "trot" ? 10 : 0) + (state === "alert" ? -16 : 0);
  const E = (pts, c) => { p.gradFill(pts, c, mul(c, A.shade), light, 0.2); p.inkRing(pts, ow * 0.7, thick); };
  const e0 = [hx + H.a * 0.3, hy - H.b * 0.8];
  if (A.ear === "pig" || (o.species || "pig") === "pig") { p.poly([[hx + 20, hy - 70], [hx + 66, hy - 120 - ea * 0.2], [hx + 98, hy - 60 + ea], [hx + 52, hy - 56]], A.dark, ow * 0.7); E([[hx - 4, hy - 74], [hx + 18, hy - 132 - ea * 0.3], [hx + 78, hy - 94 + ea * 0.5], [hx + 70, hy - 18 + ea], [hx + 36, hy - 36]], A.body); p.poly([[hx + 14, hy - 78], [hx + 28, hy - 112 - ea * 0.2], [hx + 58, hy - 86 + ea * 0.4], [hx + 52, hy - 40 + ea], [hx + 36, hy - 52]], A.nose, 0); }
  else if (A.ear === "point" || A.ear === "pointcat") { const h = A.ear === "pointcat" ? 70 : 90; E([[e0[0] - 14, e0[1] + 10], [e0[0] + 6, e0[1] - h - ea * 0.3], [e0[0] + 34, e0[1] + 6]], A.body); p.poly([[e0[0] - 4, e0[1] + 4], [e0[0] + 8, e0[1] - h * 0.65], [e0[0] + 24, e0[1] + 2]], A.belly, 0); }
  else if (A.ear === "long") { E([[e0[0] - 16, e0[1] + 12], [e0[0] - 6, e0[1] - 150 - ea * 0.4], [e0[0] + 30, e0[1] - 140], [e0[0] + 36, e0[1] + 8]], A.body); p.poly([[e0[0] - 2, e0[1]], [e0[0] + 2, e0[1] - 120], [e0[0] + 18, e0[1] - 116], [e0[0] + 22, e0[1] + 2]], A.belly, 0); }
  else if (A.ear === "floppy") E([[e0[0] - 8, e0[1] + 6], [e0[0] + 30, e0[1] - 20], [e0[0] + 56, e0[1] + 60 + ea], [e0[0] + 22, e0[1] + 86 + ea], [e0[0] - 6, e0[1] + 40]], A.dark);
  else if (A.ear === "cow") E([[e0[0] - 10, e0[1] + 18], [e0[0] + 64, e0[1] - 8 + ea * 0.4], [e0[0] + 84, e0[1] + 30 + ea], [e0[0] + 6, e0[1] + 40]], "#2b2530");
  else if (A.ear === "goat") E([[e0[0] - 10, e0[1] + 18], [e0[0] + 66, e0[1] - 4 + ea * 0.4], [e0[0] + 76, e0[1] + 26 + ea], [e0[0] + 6, e0[1] + 34]], A.body);
  else if (A.ear === "sheep") E([[e0[0] - 6, e0[1] + 16], [e0[0] + 50, e0[1] - 4 + ea * 0.3], [e0[0] + 62, e0[1] + 30 + ea], [e0[0] + 4, e0[1] + 36]], A.face || A.body);
  g.restore();
};
// ---- birds ----
const BD = {
  chicken: { body: "#fbf6ee", wing: "#f1e6d4", tailC: "#e9dcc6", beak: "#f2b84a", comb: "#e0403c", leg: "#f2b84a", s: 1.0, comb2: false },
  rooster: { body: "#c8622a", wing: "#8a3a1c", tailC: "#2e6a4a", beak: "#f2b84a", comb: "#e0403c", leg: "#d8a03a", s: 1.15, comb2: true },
  duck:    { body: "#ffe36a", wing: "#f2c84a", tailC: "#f2c84a", beak: "#f08a2a", comb: null, leg: "#f08a2a", s: 0.95, flat: true },
  goose:   { body: "#fbfbf8", wing: "#e8e8e2", tailC: "#e8e8e2", beak: "#f08a2a", comb: null, leg: "#f08a2a", s: 1.3, flat: true, longNeck: true },
  emu:     { body: "#8a6a4e", wing: "#6e523c", tailC: "#5a4232", beak: "#6a5a4a", comb: null, leg: "#7a6a58", s: 1.45, flat: false, longNeck: true, nl: 150, lift: 70 },
  gull:    { body: "#f7f9fc", wing: "#9aa7ba", tailC: "#dfe6ef", beak: "#f2b84a", comb: null, leg: "#f2a05a", s: 1.0, flat: false },
};
export const birdSide = (p, o = {}) => {
  const B = BD[o.species || "chicken"], g = p.g, light = rad(-120), thick = thickAngle(light), ow = 6;
  const { state = "stand", phase = 0, blink = 0, t = 0 } = o; const walk = state === "walk" ? 1 : 0, peck = state === "peck" ? Math.max(0, Math.sin(t * 7)) : 0;
  g.save(); g.translate(300, 975); g.scale(B.s, B.s); g.translate(-300, -975); p.rot = null;
  const bob = walk * 6 * Math.abs(Math.sin(phase * Math.PI * 4));
  const bc = [310, 800 - bob - (B.lift || 0)];
  // legs
  for (const [x, ph] of [[300, 0], [340, 0.5]]) { const sw = walk * Math.sin(2 * Math.PI * (phase + ph)) * 26; p.line([[x, bc[1] + 60], [x + sw * 0.5, 920], [x + sw, 968]], B.leg, 9); p.line([[x + sw - 22, 968], [x + sw + 4, 968], [x + sw + 24, 962]], B.leg, 7); }
  // tail feathers
  for (let i = 0; i < 4; i++) p.poly([[bc[0] + 90, bc[1] - 20], [bc[0] + 150 + i * 8, bc[1] - 90 - i * 22 + Math.sin(t * 5 + i) * 4], [bc[0] + 110 + i * 4, bc[1] + 10]], i % 2 ? B.tailC : B.wing, 4);
  // body
  const body = blobPts(bc[0], bc[1], { a: 110, b: 82, nTop: 2.2, nBot: 2.0, egg: -0.1, asym: 0, rot: rad(-8), noise: 0.01, seed: 4 }, 70);
  p.gradFill(body, B.body, mul(B.body, [0.8, 0.76, 0.84]), light, 0.2); p.inkRing(body, ow * 0.85, thick);
  const wing = blobPts(bc[0] + 20, bc[1] - 4 + Math.sin(t * 10 * (state === "fly" ? 1 : 0.1)) * (state === "fly" ? 30 : 2), { a: 64, b: 44, nTop: 2.2, nBot: 2.2, egg: 0.1, asym: 0, rot: rad(14), noise: 0.01, seed: 8 }, 40);
  p.gradFill(wing, B.wing, mul(B.wing, [0.8, 0.76, 0.84]), light, 0.2); p.inkRing(wing, ow * 0.7, thick);
  // neck + head
  const nl = B.nl || (B.longNeck ? 120 : 70), hd = peck * 90; const hx = bc[0] - 96 - peck * 40, hy = bc[1] - nl - 30 + hd;
  p.line([[bc[0] - 70, bc[1] - 30], [bc[0] - 96, bc[1] - nl * 0.6 + hd * 0.4], [hx, hy + 8]], B.body, B.longNeck ? 34 : 44);
  const head = blobPts(hx, hy, { a: B.longNeck ? 34 : 44, b: B.longNeck ? 30 : 42, nTop: 2.3, nBot: 2.1, egg: 0, asym: 0, rot: 0, noise: 0.01, seed: 2 }, 40);
  p.gradFill(head, B.body, mul(B.body, [0.8, 0.76, 0.84]), light, 0.2); p.inkRing(head, ow * 0.75, thick);
  if (B.comb) { for (let i = 0; i < (B.comb2 ? 4 : 3); i++) p.ell(hx - 6 + i * 14, hy - 40 - (i % 2) * 8, 11, 14, B.comb, 4); p.ell(hx - 40, hy + 34, 9, 16, B.comb, 4); }
  p.poly(B.flat ? [[hx - 40, hy + 6], [hx - 96, hy + 14], [hx - 92, hy + 30], [hx - 38, hy + 26]] : [[hx - 40, hy + 2], [hx - 78, hy + 16], [hx - 40, hy + 28]], B.beak, 5);
  if (blink > 0.5) p.stroke([[hx - 24, hy - 4], [hx - 10, hy - 2]], 5, INK); else { p.ell(hx - 16, hy - 6, 9, 10, "#ffffff", 3); p.dot(hx - 18, hy - 5, 4.2, INK); p.dot(hx - 20, hy - 8, 1.6, "#ffffff"); }
  g.restore();
};
