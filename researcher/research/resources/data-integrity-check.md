# Data Integrity Check

## Problem

When saving large content (especially from web sources), there's a risk of truncating data during the save process. This happened when ingesting a 5.8万字 article where only the first 3000 characters were saved initially.

## Root Cause

The issue occurs when:
1. Tool results are saved to temporary files due to size (e.g., `tool-results/xxx.txt`)
2. The main agent manually constructs content for `Write` tool
3. Content is accidentally truncated during manual construction

## Solution: Always Use Raw Data

When dealing with large content from tool results:

### ❌ Wrong Approach
```
Read tool result → Manually construct markdown → Write to file
(Risk: Manual construction may truncate content)
```

### ✅ Correct Approach
```
Read tool result → Extract raw data directly → Write to file
(Use jq, cat, or direct file operations to preserve full content)
```

## Implementation

### For Web Content (CDP/WebFetch)

When tool result is saved to a file like `/path/to/tool-results/xxx.txt`:

```bash
# Extract textContent field directly
cat /path/to/tool-results/xxx.txt | jq -r '.value.textContent' > raw/article.md

# Verify file size
wc -c raw/article.md
```

### For File Uploads

When user provides a file:

```bash
# Copy directly, don't read and rewrite
cp /path/to/source.md raw/article.md
```

### Verification Steps

After saving, ALWAYS verify:

1. **Check file size**:
   ```bash
   wc -c raw/article.md
   ```

2. **Compare with source**:
   - Original tool result size: X bytes
   - Saved file size: Y bytes
   - If Y < X significantly, data was truncated

3. **Spot check content**:
   ```bash
   # Check if file ends properly (not mid-sentence)
   tail -20 raw/article.md
   ```

## Checklist for Web Content Ingestion

- [ ] Use `/web-access` or CDP to fetch content
- [ ] If tool result is large (>100KB), it will be saved to temp file
- [ ] Extract raw content using `jq` or `cat`, NOT manual construction
- [ ] Verify saved file size matches source size
- [ ] Proceed with multi-agent analysis only after verification

## Example: Correct Implementation

```bash
# Step 1: Fetch content (returns tool-results/abc.txt)
curl -s -X POST "http://localhost:3456/eval?target=XXX" -d 'script'

# Step 2: Extract and save raw content
cat /path/to/tool-results/abc.txt | jq -r '.value.textContent' > raw/article.md

# Step 3: Verify
echo "Original size: $(cat /path/to/tool-results/abc.txt | jq -r '.value.textContent' | wc -c)"
echo "Saved size: $(wc -c < raw/article.md)"

# Step 4: Only proceed if sizes match
if [ $(wc -c < raw/article.md) -gt 10000 ]; then
  echo "✅ Content saved successfully"
else
  echo "❌ Content truncated, retry"
fi
```

## Key Principle

**Never manually reconstruct large content. Always use direct data extraction.**
