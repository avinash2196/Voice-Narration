import type { Environment } from 'vitest';
import { builtinEnvironments } from 'vitest/environments';

// The built-in jsdom environment replaces the global AbortController and
// AbortSignal with jsdom's own, but keeps Node's fetch and Request. Node's
// Request accepts only Node's AbortSignal, so a fetch given a jsdom signal is
// rejected before the request mock sees it. This environment is the built-in
// jsdom environment with Node's AbortController and AbortSignal kept, so a
// request carrying an abort signal reaches the request mock.
const jsdomWithNodeAbort: Environment = {
  name: 'jsdom-node-abort',
  transformMode: 'web',
  async setup(global, options) {
    const NodeAbortController = global.AbortController;
    const NodeAbortSignal = global.AbortSignal;
    const jsdomEnvironment = await builtinEnvironments.jsdom.setup(global, options);
    global.AbortController = NodeAbortController;
    global.AbortSignal = NodeAbortSignal;
    return jsdomEnvironment;
  },
};

export default jsdomWithNodeAbort;
