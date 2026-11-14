import { Config } from '@remotion/cli/config';

// Explicit GL backend for deterministic headless WebGL rendering where supported.
Config.setChromiumOpenGlRenderer('angle');
