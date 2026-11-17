// Lancamento unico do Chromium (WebGL por software).
// RASTER=llvmpipe (padrao, Mesa/LLVM: ~3x mais rapido que o SwiftShader, imagem equivalente) | swiftshader (antigo). Se o Mesa nao estiver instalado, cai sozinho no SwiftShader.
// CHARGS sobrepoe as flags. Canvas 2D por software = ~20% mais rapido.
import { chromium } from 'playwright'; import fs from 'fs';
const SW = '--use-angle=swiftshader --enable-unsafe-swiftshader --ignore-gpu-blocklist --disable-gpu-rasterization --disable-accelerated-2d-canvas';
const LL = '--use-gl=angle --use-angle=gl-egl --ignore-gpu-blocklist --disable-gpu-sandbox --disable-gpu-rasterization --disable-accelerated-2d-canvas';
const hasMesa = ['/usr/lib/x86_64-linux-gnu/dri/swrast_dri.so', '/usr/lib/x86_64-linux-gnu/libEGL_mesa.so.0'].some((p) => fs.existsSync(p));
export const RASTER = process.env.RASTER || (hasMesa && process.platform === 'linux' ? 'llvmpipe' : 'swiftshader');
export const ARGS = (process.env.CHARGS || (RASTER === 'llvmpipe' ? LL : SW)).split(' ').filter(Boolean);
const env = RASTER === 'llvmpipe' ? { ...process.env, LIBGL_ALWAYS_SOFTWARE: '1', GALLIUM_DRIVER: 'llvmpipe', LP_NUM_THREADS: process.env.LP_NUM_THREADS || '1' } : process.env;
export const launch = () => chromium.launch({ args: ARGS, env });
