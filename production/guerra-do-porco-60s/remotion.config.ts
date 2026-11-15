import { Config } from '@remotion/cli/config';
Config.setChromiumOpenGlRenderer('swangle');
Config.setBrowserExecutable('/opt/pw-browsers/chromium-1243/chrome-linux64/chrome');
Config.setConcurrency(4);
Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(92);
