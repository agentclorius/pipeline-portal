// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@astrojs/tailwind';

// https://astro.build/config
export default defineConfig({
  site: 'https://returnaaps.github.io',
  base: '/partner-pipeline',
  integrations: [tailwindcss()],
});
