import { defineConfig } from "vitest/config"

export default defineConfig({
  test: {
    globals: true,
    clearMocks: true,
    restoreMocks: true,
    passWithNoTests: false,
    coverage: {
      provider: "v8",
      include: [
        "src/**/*.{js,jsx,ts,tsx}",
        "client/src/**/*.{js,jsx,ts,tsx}",
        "server/**/*.{js,mjs,cjs,ts,mts,cts}",
      ],
      exclude: ["**/*.{test,spec}.{js,jsx,mjs,cjs,ts,tsx,mts,cts}", "**/tests/**", "**/fixtures/**"],
      reporter: ["text", "json-summary", "lcov"],
      reportsDirectory: "coverage",
    },
    projects: [
      {
        extends: true,
        test: {
          name: "client",
          environment: "jsdom",
          include: [
            "src/**/*.{test,spec}.{js,jsx,ts,tsx}",
            "client/src/**/*.{test,spec}.{js,jsx,ts,tsx}",
          ],
        },
      },
      {
        extends: true,
        test: {
          name: "server",
          environment: "node",
          include: ["server/**/*.{test,spec}.{js,mjs,cjs,ts,mts,cts}"],
        },
      },
    ],
  },
})
