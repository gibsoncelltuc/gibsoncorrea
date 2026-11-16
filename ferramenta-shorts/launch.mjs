// Lancamento unico do Chromium (WebGL por software). Flags medidas: canvas 2D por software = ~20% mais rapido que o 2D acelerado via SwiftShader.
import { chromium } from 'playwright';
export const ARGS = (process.env.CHARGS || '--use-angle=swiftshader --enable-unsafe-swiftshader --ignore-gpu-blocklist --disable-gpu-rasterization --disable-accelerated-2d-canvas').split(' ');
export const launch = () => chromium.launch({ args: ARGS });
