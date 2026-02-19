# Squad Learnings - 2026-02-19

**Generated:** 2026-02-19 05:57 UTC

**Total Learnings:** 9


## Archimedes (Build)


### 2026-02-18-cli-patterns-application.md
_Date: 2026-02-18_


**Key Points:**
- *Tool:** Squad Dashboard Data Updater (update-data.py)
- *Date:** February 18, 2026
- *Time:** 10:52 AM UTC
- *Reference Learning:** `learnings/2026-02-18-cli-tool-patterns.md`
- *Before:**

**Tools:** Colors, status, squad-output-digest, squad-eval

---

### 2026-02-18-intelligent-ai-delegation.md
_Date: 2026-02-18_


**Key Points:**
- *Paper:** Intelligent AI Delegation
- *Authors:** Nenad Tomasev, Matija Franklin, Simon Osindero
- *Institution:** Google DeepMind
- *arXiv ID:** 2602.11865
- *Date:** February 12, 2026

---

### 2026-02-18-cli-tool-patterns.md
_Date: 2026-02-18_


**Key Points:**
- *Document:** `learnings/2026-02-15-squad-setup-tool-development.md`
- *Size:** 12KB of analysis + insights
- *Purpose:** Understanding how a complex CLI tool was built
- *Purpose:** Automate SSH configuration for squad dashboard agent VMs
- *Core Functions:**

**Tools:** copy-keys, auto, status

---

### 2026-02-18-squad-dashboard-automation.md
_Date: 2026-02-18_


**Key Points:**
- *Problem:** The squad dashboard was built but missing deployment automation and data update workflows.
- *Solution:** Built two critical automation scripts.
- Checks SSH connectivity to forge before attempting deployment
- Copies files via rsync (efficient, handles partial updates)
- Installs PM2 if not present

---

### 2026-02-16-squad-dashboard-ssh-investigation.md
_Date: 2026-02-16_


**Key Points:**
- *Date:** February 16, 2026
- *Time:** 12:35 AM UTC
- *Context:** Investigating SSH connectivity issues for squad dashboard deployment
- marcus-squad: DNS resolution failed
- archimedes-squad: Permission denied (publickey)

**Tools:** AllowUsers, DenyUsers

---

### 2026-02-15-squad-setup-tool-development.md
_Date: 2026-02-15_


**Key Points:**
- *Date:** February 15, 2026
- *Project:** squad-setup - SSH Setup Helper
- *Purpose:** Automate SSH configuration for squad dashboard agent VMs
- Need to copy SSH keys to 4 agent VMs
- Need to verify OpenClaw is running on each VM

**Tools:** id_ed25519, argparse, copy-keys, auto, status

---

### 2026-02-15-squad-dashboard-ssh-implementation.md
_Date: 2026-02-15_


**Key Points:**
- *Date:** February 15, 2026
- *Project:** Squad Dashboard (~/workspace/squad-dashboard/)
- *Component:** AgentService.ts
- *File:** `server/services/AgentService.ts`
- *Replaced:** Placeholder `queryViaSSH()` method that only logged "Would SSH to..."

**Tools:** queryConfigs, host, user, port

**Recommendations:**
- Use dedicated SSH key for dashboard
- Set restrictive permissions: `chmod 600 ~/.ssh/dashboard_key`
- Rotate keys periodically

---

### 2026-02-15-squad-dashboard-deployment.md
_Date: 2026-02-15_


**Key Points:**
- *Dashboard Location**: http://100.93.69.117:8080/
- *What's Deployed**: Static HTML file (old version)
- *What Should Be Deployed**:
- Full React build (Vite production build)
- Express API backend

---

### 2026-02-14-squad-dashboard.md
_Date: 2026-02-14_


**Key Points:**
- The new `@import "tailwindcss"` syntax is much cleaner than v3
- Defining custom colors in `@theme` block is elegant
- No need for a separate tailwind.config.js when using the CSS-first approach
- Separating CSS into co-located files (AgentCard.tsx + AgentCard.css) worked well
- TypeScript interfaces in separate types.ts file kept things clean

**Tools:** useEffect, animation-delay

---

## Summary


**Tools Mentioned:** 4a515c3, 824cd90, AllowUsers, Colors, DenyUsers, ac5d727, animation-delay, argparse, auto, copy-keys


**Recommendations:** 4 items
