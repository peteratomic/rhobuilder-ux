// Role paths — from the "Choose your path" table in rhobuilder's README.
// `page` is the generated page under docs/ (same name as the source .md).
window.RHO_ROLES = [
  {
    id: "author",
    name: "A non-technical author",
    short: "Non-technical author",
    desc: "You have an idea for a dApp and want to shape it, without writing contract code.",
    intro: "Go from idea to a validated design. You won't need to write Rholang or learn the registry schema.",
    steps: [
      {
        title: "Quickstart", page: "start",
        summary: "The shortest route from a fresh checkout to a validated design and a scaffold plan.",
        points: [
          "Run a read-only check that shows what your machine is missing",
          "Launch the studio in your browser",
          "Start a design with the composer, or let the assistant interview you"
        ]
      },
      {
        title: "Studio tour", page: "ui",
        summary: "A walk through the rhobuilder studio and what each part of the dashboard shows.",
        points: [
          "Readiness, networks and the primitive graph",
          "The design composer and ready-made examples",
          "Project status in plain labels: Draft, Scaffold, Tested, Owed and more"
        ],
        note: "The studio never signs, funds or holds keys. Those steps stay in the terminal."
      },
      {
        title: "Core concepts", page: "concepts",
        summary: "The idea behind rhobuilder: write only the part that's genuinely new, and reuse what's already on-chain.",
        points: [
          "Commodity vs unique: payments, escrow and booking already exist",
          "Reuse, extend or new, and why duplicates are refused",
          "What each status really means, and which networks allow what"
        ]
      }
    ]
  },
  {
    id: "developer",
    name: "A developer",
    short: "Developer",
    desc: "You'll design, implement and test the contracts and adapters.",
    intro: "Learn the build loop, the design document and the CLI that every front end calls.",
    steps: [
      {
        title: "Workflow", page: "workflow",
        summary: "The end-to-end loop, from probing the network to closing out a release.",
        points: ["Probe, design, reuse, scaffold", "Implement, prove, test", "Plan the deploy, execute from the CLI, close"]
      },
      {
        title: "Design and reuse", page: "design",
        summary: "The design.json document, and the gate that refuses duplicate primitives before any code is written.",
        points: ["The rhobuilder.design/v1 schema, field by field", "Tagging components reuse, extend or new", "Running the gate, with passing and refused examples"]
      },
      {
        title: "Command reference", page: "command-reference",
        summary: "Every rhobuilder command, flag and exit code, with structured JSON output.",
        points: ["Global flags and the JSON envelope", "chain, registry, design, baseline, deploy and more", "Which commands are read-only and which are gated"]
      }
    ]
  },
  {
    id: "operator",
    name: "An operator",
    short: "Operator",
    desc: "You install and run rhobuilder, and manage deploys to devnet and testnet.",
    intro: "Get rhobuilder installed, run a local chain safely, then prepare for the public testnet.",
    steps: [
      {
        title: "Install", page: "install",
        summary: "Prerequisites, the readiness check, and installing from source or from a release package.",
        points: ["What you need: Node, Rust, Python, plus optional Docker and Lean", "Source build or a checksummed release tarball", "Environment variables, upgrades and uninstalling"]
      },
      {
        title: "Local devnet", page: "devnet",
        summary: "Running and onboarding a local, disposable chain, and the results measured on it.",
        points: ["The safe lifecycle: status, start, wait, onboard", "Dry run first; --execute only on devnet", "Why a not-run suite is never counted as a pass"]
      },
      {
        title: "Public testnet", page: "baseline",
        summary: "The gated testnet campaign: preflight, plan, dry run and verification.",
        points: ["Read-only preflight that lists every blocker", "The gates live execution must clear", "Pins and the current account-factory blocker"],
        note: "No live testnet deploy has been run yet. It needs separate approval and a funded key."
      }
    ]
  },
  {
    id: "evaluator",
    name: "An evaluator or maintainer",
    short: "Evaluator or maintainer",
    desc: "You need to understand how rhobuilder works, and whether to trust it.",
    intro: "See how it's put together, where the safety boundaries are, and how every claim is tested.",
    steps: [
      {
        title: "Architecture", page: "architecture",
        summary: "A Rust decision core with thin front ends: the studio, the plugin and the MCP server.",
        points: ["What each crate and folder is responsible for", "The data flow from idea to deploy evidence", "Trust boundaries: only the CLI decides and signs"]
      },
      {
        title: "Security model", page: "security",
        summary: "How keys, funding and live deploys are protected, and what each surface may and may not do.",
        points: ["The threat model and its main risks", "How keys are handled, and the network gates", "Integrity of pinned, vendored terms"]
      },
      {
        title: "Testing and gates", page: "testing",
        summary: "The test layers, the project check profiles, and how status claims are earned.",
        points: ["From Rust unit tests to package self-tests", "Static, formal and full project profiles", "CI, and why evidence isn't authority"]
      }
    ]
  }
];
