// server/database/eslint.config.js
import { defineConfig } from 'eslint';

export default defineConfig({
  languageOptions: {
    ecmaVersion: 2020,  // Enables ES6/ES8 features (async/await, etc.)
    globals: {
      // Define any global variables here if needed
      process: 'readonly', // For example, Node's `process` object
    },
  },
  extends: ['eslint:recommended'],  // Use ESLint's recommended rules
  rules: {
    // You can add custom rules here
  },
});