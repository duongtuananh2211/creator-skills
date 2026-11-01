import { defineConfig, type Plugin } from 'vite';
import { createReadStream, existsSync, statSync } from 'node:fs';
import { resolve, join, sep } from 'node:path';

// Serve three's Draco decoder at /draco/ so Draco-compressed GLBs load without a CDN.
function dracoDecoder(): Plugin {
  const dir = resolve('node_modules/three/examples/jsm/libs/draco/gltf');
  return {
    name: 'draco-decoder',
    configureServer(server) {
      server.middlewares.use('/draco', (req, res, next) => {
        const rel = decodeURIComponent((req.url ?? '/').split('?')[0]);
        const file = join(dir, rel);
        if (!file.startsWith(dir + sep) || !existsSync(file) || !statSync(file).isFile()) return next();
        res.setHeader('Content-Type', file.endsWith('.wasm') ? 'application/wasm' : 'text/javascript');
        createReadStream(file).pipe(res);
      });
    },
  };
}

export default defineConfig({
  plugins: [dracoDecoder()],
  server: {
    port: 5173,
    watch: { ignored: ['**/renders/**'] },
  },
  build: { target: 'esnext' },
});
