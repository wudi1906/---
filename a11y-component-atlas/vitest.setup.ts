import { expect } from 'vitest';
import '@testing-library/jest-dom/vitest';

// jsdom does not implement canvas; provide a minimal stub to silence getContext errors
if (typeof HTMLCanvasElement !== 'undefined') {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  (HTMLCanvasElement.prototype as any).getContext = (type: string) => {
    return {} as unknown as CanvasRenderingContext2D;
  };
}
