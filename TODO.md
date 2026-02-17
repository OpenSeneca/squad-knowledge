# Archimedes — TODO

## RIGHT NOW: Deploy Squad Dashboard to Forge

**Blocker:** SSH access to forge (100.93.69.117) blocked with "Permission denied (publickey)"

**Architecture (no SSH needed from dashboard side):**
- Dashboard reads from data.json file (Argus pushes updates)
- Auto-refreshes every 60 seconds via client-side fetch()
- Simple Node.js HTTP server serves static files

**Deployment Steps:**
1. Copy dashboard to forge: `scp -r squad-dashboard/ forge:~/dashboard/`
2. SSH to forge and verify files
3. Start server: `pm2 start server.js --name squad-dashboard`
4. Access at: http://forge:8000 or http://100.93.69.117:8000

**Workaround for SSH blocker:**
- Need Justin to set up SSH key for exedev@forge
- Or provide alternative deployment method
- Dashboard is already built and tested locally

## After Dashboard Deployment

- [ ] Argus data push script (updates data.json every 5 minutes)
- [ ] Output digest script
- [ ] Paper summarizer

## Questions for Justin

1. **SSH to Forge:** Can you set up SSH key for exedev@100.93.69.117?
2. **Deployment Method:** Should I copy via SCP, or is there another way?

## Rules

- NO MORE SSH INVESTIGATION. Dashboard reads data.json. Period.
- Don't spend forever debugging — if blocked after 2 attempts, log and move on.
- Build things with a clear user.

## What To Build (After Dashboard Deployed)

If SSH access resolved:

1. **Argus monitoring script** — Script to query all 4 agents and update data.json
2. **Output digest tool** — Aggregate outputs from all agents
3. **Tools for Justin** — CLI utilities he actually needs
