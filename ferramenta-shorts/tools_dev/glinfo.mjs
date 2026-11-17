// node tools_dev/glinfo.mjs  -> mostra qual rasterizador o Chromium esta usando com as flags de CHARGS (e CHANNEL=chromium para o binario completo)
import { chromium } from 'playwright';
const args = (process.env.CHARGS || '--use-angle=swiftshader --enable-unsafe-swiftshader --ignore-gpu-blocklist').split(' ').filter(Boolean);
const opt = { args }; if (process.env.CHANNEL) opt.channel = process.env.CHANNEL;
let b; try { b = await chromium.launch(opt); } catch (e) { console.log('LAUNCH FAIL', String(e.message).split('\n')[0]); process.exit(1); }
const pg = await b.newPage();
const r = await pg.evaluate(() => { const c = document.createElement('canvas'); const gl = c.getContext('webgl2'); if (!gl) return 'SEM WEBGL2'; const e = gl.getExtension('WEBGL_debug_renderer_info'); return (e ? gl.getParameter(e.UNMASKED_RENDERER_WEBGL) : 'n/a') + ' | halfFloatRT=' + !!gl.getExtension('EXT_color_buffer_half_float') + ' floatRT=' + !!gl.getExtension('EXT_color_buffer_float'); });
console.log(r); await b.close();
