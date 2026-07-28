import { defineConfig } from "vitest/config"

export default defineConfig({
  test: {
    globals: true,
    environment: "node",
    include: ["src/**/*.{test,spec}.{ts,tsx}", "tests/**/*.{test,spec}.{ts,tsx}"],
    exclude: ["node_modules", "dist", "coverage", ".build", ".turbo"],
    clearMocks: true,
    restoreMocks: true,
    passWithNoTests: false,
    coverage: {
      provider: "v8",
      include: ["src/**/*.{ts,tsx}"],
      exclude: [
        "**/*.config.*",
        "**/*.d.ts",
        "**/*.gen.*",
        "**/generated/**",
        "**/tests/**",
        "**/*.{test,spec}.*",
        "**/test-setup.*",
      ],
      reporter: ["text", "json-summary", "lcov"],
      reportsDirectory: "coverage",
    },
  },
})
