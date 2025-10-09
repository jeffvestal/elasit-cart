# Elasti-Cart Scripts Reference

Complete reference for all deployment and management scripts in the repository.

## 🚀 Deployment Scripts

### `deploy-canonical.sh` ✅ **PRIMARY DEPLOYMENT SCRIPT**

Deploy all Agent Builder tools and agents to any cluster using canonical definitions.

```bash
# Fresh deployment
export KIBANA_URL=https://your-cluster.kb.cloud.es.io
export KIBANA_API_KEY=your_api_key
./deploy-canonical.sh

# Force redeploy (deletes existing first)
./deploy-canonical.sh --delete-existing
```

**What it does:**
- Activates Python virtual environment
- Calls `deploy_canonical_agents.py`
- Deploys 8 tools and 5 agents from `canonical-definitions/`

**Exit codes:**
- `0` = Success, all deployed
- `1` = Failure, some definitions failed

---

### `deploy_canonical_agents.py` 

Python script that performs the actual deployment. Called by `deploy-canonical.sh`.

```bash
source venv/bin/activate
python deploy_canonical_agents.py --delete-existing
```

**Arguments:**
- `--delete-existing` - Delete existing tools/agents before deploying

**What it does:**
- Reads `canonical-definitions/tools.json` and `agents.json`
- Filters out read-only fields (readonly, created_at, updated_at, type for agents)
- Creates tools and agents via Agent Builder API
- Reports success/failure for each item

---

### `verify-deployment.sh` ✅ **VERIFICATION SCRIPT**

Verify that deployment is correct and complete.

```bash
export KIBANA_URL=https://your-cluster.kb.cloud.es.io
export KIBANA_API_KEY=your_api_key
./verify-deployment.sh
```

**What it checks:**
- ✅ 8 tools deployed
- ✅ 5 agents deployed
- ✅ `check_store_inventory` tool has correct query

**Exit codes:**
- `0` = Deployment verified
- `1` = Deployment incorrect or incomplete

---

## 📚 Documentation

### `DEPLOYMENT.md` ✅ **MAIN DEPLOYMENT GUIDE**

Complete deployment guide with:
- Quick start instructions
- Prerequisites and setup
- Deployment commands
- Verification steps
- Troubleshooting
- Schema reference

**Read this first** when deploying to a new cluster.

---

### `canonical-definitions/README.md`

Documentation for the canonical tool and agent definitions:
- Schema format for tools and agents
- List of all tools and agents
- Key fixes and changes
- How to update canonical definitions

---

### `SCRIPTS.md` (this file)

Complete reference for all scripts in the repository.

---

## 🗂️ Directory Structure

```
/Users/jeffvestal/repos/elasti-cart/
├── canonical-definitions/          # ✅ SOURCE OF TRUTH
│   ├── tools.json                  # 8 tool definitions
│   ├── agents.json                 # 5 agent definitions
│   └── README.md                   # Schema documentation
│
├── agent-builder-service/
│   └── agent_builder_client.py     # Agent Builder API client
│
├── deploy-canonical.sh             # ✅ Main deployment script
├── deploy_canonical_agents.py      # Python deployment logic
├── verify-deployment.sh            # ✅ Verification script
│
├── DEPLOYMENT.md                   # ✅ Main deployment guide
└── SCRIPTS.md                      # This file
```

---

## 🎯 Common Workflows

### Deploy to New Cluster

```bash
# 1. Set credentials
export KIBANA_URL=https://new-cluster.kb.cloud.es.io
export KIBANA_API_KEY=new_api_key

# 2. Deploy
./deploy-canonical.sh

# 3. Verify
./verify-deployment.sh
```

---

### Redeploy After Changes

```bash
# 1. Export current production definitions
export KIBANA_URL=https://prod-cluster.kb.cloud.es.io
export KIBANA_API_KEY=prod_api_key

curl -s "${KIBANA_URL}/api/agent_builder/tools" \
  -H "Authorization: ApiKey ${KIBANA_API_KEY}" \
  -H "kbn-xsrf: true" | \
  jq '[.results[] | select(.readonly == false)]' > canonical-definitions/tools.json

curl -s "${KIBANA_URL}/api/agent_builder/agents" \
  -H "Authorization: ApiKey ${KIBANA_API_KEY}" \
  -H "kbn-xsrf: true" | \
  jq '[.results[] | select(.readonly == false)]' > canonical-definitions/agents.json

# 2. Commit changes
git add canonical-definitions/
git commit -m "Update canonical definitions"

# 3. Deploy to target cluster
export KIBANA_URL=https://target-cluster.kb.cloud.es.io
export KIBANA_API_KEY=target_api_key

./deploy-canonical.sh --delete-existing

# 4. Verify
./verify-deployment.sh
```

---

### Quick Health Check

```bash
export KIBANA_URL=https://your-cluster.kb.cloud.es.io
export KIBANA_API_KEY=your_api_key

./verify-deployment.sh
```

---

## 🔧 Deprecated/Legacy Scripts

The following scripts are **NOT** used in the current deployment workflow:

### `agent-builder-service/deploy_updated_agents.py` ❌ DEPRECATED
Old deployment script that used Python class definitions instead of canonical JSON. **Do not use.**

### `agent-builder-service/deploy-agents.sh` ❌ DEPRECATED
Old shell wrapper for the deprecated deployment script. **Do not use.**

### `agent-builder-service/redeploy_agents.py` ❌ DEPRECATED
Old redeployment script. **Do not use.**

**Why deprecated?**
- Used Python code as source of truth instead of JSON
- More complex and harder to maintain
- Schema didn't match API requirements
- Led to deployment failures

**Current approach:**
- Use canonical JSON definitions (`canonical-definitions/*.json`)
- Simple, declarative, and version-controlled
- Matches API schema exactly
- Proven to work

---

## 📝 Script Maintenance

### When to Update Scripts

Update deployment scripts when:
1. Agent Builder API schema changes
2. New tools or agents are added
3. Tool/agent configuration format changes
4. New deployment requirements emerge

### How to Update

1. **Test changes on dev cluster first**
2. **Update canonical definitions** in `canonical-definitions/`
3. **Test deployment script**: `./deploy-canonical.sh --delete-existing`
4. **Verify**: `./verify-deployment.sh`
5. **Update documentation** if needed
6. **Commit and push changes**

---

## 🆘 Troubleshooting

### Script fails with "readonly" error
**Solution:** The script now filters out `readonly`, `created_at`, and `updated_at` fields.

### Script fails with "type" error for agents
**Solution:** The script filters out `type` from agent create requests (API inconsistency).

### Script can't find virtual environment
**Solution:** Create it: `python3 -m venv venv && source venv/bin/activate && pip install aiohttp python-dotenv`

### Wrong number of tools/agents deployed
**Solution:** Old duplicates may exist. Use `./deploy-canonical.sh --delete-existing` to clean up.

---

## 📊 Script Summary Table

| Script | Purpose | Required Env Vars | Exit Codes |
|--------|---------|-------------------|------------|
| `deploy-canonical.sh` | Deploy tools & agents | `KIBANA_URL`, `KIBANA_API_KEY` | 0=success, 1=failure |
| `deploy_canonical_agents.py` | Python deployment logic | Same | 0=success, 1=failure |
| `verify-deployment.sh` | Verify deployment | Same | 0=verified, 1=incorrect |

---

## 🎓 Learning Path

1. **Start here:** Read `DEPLOYMENT.md`
2. **Deploy to test cluster:** `./deploy-canonical.sh`
3. **Verify:** `./verify-deployment.sh`
4. **Understand the data:** Read `canonical-definitions/README.md`
5. **Make changes:** Edit canonical JSONs, redeploy
6. **Reference:** Use this file (`SCRIPTS.md`) for quick lookup

---

## 📞 Support

For script issues:
1. Check this reference guide
2. Review `DEPLOYMENT.md` 
3. Check script exit codes
4. Review logs from script output
5. Verify environment variables are set

---

**Last Updated:** 2025-10-08  
**Version:** 1.0 (Canonical Deployment System)

