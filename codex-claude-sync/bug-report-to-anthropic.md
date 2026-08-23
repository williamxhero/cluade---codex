# Bug Report to Anthropic

## Issue: Claude Code Settings UI Not Displaying All Skills

### Environment
- **Application**: Claude Code
- **Platform**: Windows 11 Pro 10.0.26200
- **Model**: claude-opus-5

### Problem Description
The Settings → Skills page only displays 1 skill, despite having 56 skills correctly installed and functional.

### Expected Behavior
Settings → Skills should display all 56 installed skills, similar to how Codex displays 55 skills in its Settings page.

### Actual Behavior
- Settings → Skills page: Shows only 1 skill
- `/` command in chat: Shows ~100+ skills (correct)
- All skills are functional via commands (e.g., `/grill-me`, `/code-review`)

### Steps to Reproduce
1. Install 56 skills in `C:\Users\will\.claude\skills\`
2. Create `config.toml` with all skills explicitly configured
3. Add `userSkills` array to `settings.json`
4. Restart Claude Code
5. Open Settings → Skills
6. Observe: Only 1 skill displayed

### Configuration Files

**Directory Structure**:
```
C:\Users\will\.claude\
├── skills/
│   ├── apex-strategy-report/
│   ├── code-review/
│   ├── grill-me/
│   └── ... (56 total)
├── config.toml (with all 56 skills configured)
├── settings.json (with userSkills array)
└── skills-lock.json (with all 56 skills)
```

**config.toml** (excerpt):
```toml
[[skills.config]]
path = 'C:\Users\will\.claude\skills\apex-strategy-report\SKILL.md'
enabled = true

[[skills.config]]
path = 'C:\Users\will\.claude\skills\code-review\SKILL.md'
enabled = true

... (56 total)
```

**settings.json** (excerpt):
```json
{
  "userSkills": [
    "apex-strategy-report",
    "ask-matt",
    "asr",
    ... (56 total)
  ]
}
```

### What Works
- All 56 skills are functionally loaded
- `/` command shows ~100+ skills
- Skill commands execute correctly (e.g., `/grill-me`, `/code-review`)
- Skills are properly formatted with valid YAML frontmatter

### What Doesn't Work
- Settings → Skills UI only displays 1 skill
- UI does not reflect the actual skills loaded

### Comparison with Codex
- **Codex Settings**: Correctly displays 55 skills
- **Codex config**: Similar structure with `[[skills.config]]` sections
- **Claude Code**: Identical configuration but UI shows only 1

### Troubleshooting Attempted
1. ✅ Multiple complete restarts of Claude Code
2. ✅ Created `skills-lock.json` with all skills
3. ✅ Added `userSkills` to `settings.json`
4. ✅ Created `config.toml` with explicit skill configuration
5. ✅ Cleared cache directory
6. ✅ Verified all SKILL.md files have correct format
7. ❌ Settings UI still shows only 1 skill

### Diagnostic Output

**Skills directory count**:
```bash
$ find C:/Users/will/.claude/skills/ -name "SKILL.md" | wc -l
56
```

**All skills have valid format**:
```bash
$ diagnose-skills.py
✅ 56 valid skills found
❌ 0 invalid skills
```

**Skills functional via commands**:
```
/grill-me → ✅ Works
/code-review → ✅ Works
/apex-strategy-report → ✅ Works
```

### Expected Fix
Settings → Skills UI should scan and display all skills from:
- `C:\Users\will\.claude\skills\` directory
- Or read from `config.toml` [[skills.config]] sections
- Or read from `settings.json` userSkills array

### Additional Context
This appears to be a UI rendering issue rather than a loading issue, as all skills are functionally available. The Settings page may not be correctly reading the skill configuration or may have a display limit bug.

### Migration Context
Skills were migrated from Codex using a custom migration tool:
- Source: Codex `.codex/skills/` and `.agents/skills/`
- Target: Claude Code `.claude/skills/`
- All files verified and functional

### Contact
User: will
GitHub: https://github.com/williamxhero/cluade---codex

---

**Priority**: Medium (functionality works, but UI is misleading)
**Category**: UI Bug
**Reproducible**: Yes, consistently
