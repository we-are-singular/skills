import fs from "node:fs"
import { parse } from "jsonc-parser"

const WORKSPACE_FILE = "./__PROJECT_NAME__.code-workspace"
const NON_SCOPED_TYPES = ["build", "ci", "docs", "tools", "style"]

const getWorkspaceScopes = () => {
  const contents = fs.readFileSync(WORKSPACE_FILE, "utf8")
  const errors = []
  const workspace = parse(contents, errors, { allowTrailingComma: true })

  if (errors.length > 0 || !Array.isArray(workspace?.folders)) {
    throw new Error(`Could not read commit scopes from ${WORKSPACE_FILE}`)
  }

  const scopes = workspace.folders.map(folder => {
    const displayName = String(folder.name ?? folder.path)
    const normalized = displayName.replace(/[^@/a-zA-Z0-9.-]/g, "").toLowerCase()
    const scope = normalized.includes("/") ? normalized.split("/").at(-1) : normalized
    return scope === "." ? "root" : scope
  })

  return [...new Set(scopes.filter(Boolean))]
}

export default {
  extends: ["@commitlint/config-conventional"],
  rules: {
    "type-enum": [
      2,
      "always",
      [
        "build",
        "ci",
        "tools",
        "docs",
        "feat",
        "feature",
        "fix",
        "perf",
        "refactor",
        "design",
        "style",
        "test",
        "release",
      ],
    ],
    "subject-case": [0],
    "workspace-scope": [2, "always"],
    "subject-after-ticket-case": [2, "always"],
  },
  plugins: [
    {
      rules: {
        "subject-after-ticket-case": (parsed, when) => {
          if (!parsed.subject) return [false, "Subject is required"]

          const subject = String(parsed.subject).trim()
          const subjectWithoutTicket = subject.replace(/^(?:(?:ISSUE|TICKET)-\d+|#\d+)(?::)?\s+/, "")
          const isLowercase = subjectWithoutTicket.length > 0 && subjectWithoutTicket === subjectWithoutTicket.toLowerCase()
          const isValid = when === "never" ? !isLowercase : isLowercase
          const expectation = when === "never" ? "must not be entirely lowercase" : "must be lowercase"

          return [isValid, `Subject ${expectation} after an optional ISSUE-123, TICKET-123, or #123 prefix`]
        },
        "workspace-scope": (parsed, when) => {
          const scopes = getWorkspaceScopes()
          const hasValidScope = parsed.scope ? scopes.includes(parsed.scope) : NON_SCOPED_TYPES.includes(parsed.type)
          const isValid = when === "never" ? !hasValidScope : hasValidScope

          return [
            isValid,
            `Scope must be one of [${scopes.join(", ")}]; only ${NON_SCOPED_TYPES.join(", ")} may omit it`,
          ]
        },
      },
    },
  ],
}
