# Session Analysis Extension for claude-devtools

**Status:** Proof of Concept (PoC) - Architecture and Implementation

## Overview

This analysis engine extends claude-devtools with intelligent session analysis and actionable insights. It leverages existing session data structures and follows the project's architecture patterns.

## Files Created

### 1. Type Definitions

**File:** `src/shared/types/analysis.ts`

Defines all analysis-related types:

- `AnalysisInsight` - Insight with category, severity, description, why it matters, what to do
- `FileAccessPattern` - File access frequency and methods
- `ToolUsagePattern` - Tool usage statistics and patterns
- `ContextUsageMetrics` - Token usage, compactions, efficiency score
- `SessionEfficiencyMetrics` - Overall efficiency metrics
- `SessionAnalysis` - Complete analysis result
- `AnalysisOptions` - Configurable thresholds
- `AnalysisInput` - Input data interface

### 2. Analyzer Engine

**File:** `src/shared/utils/sessionAnalyzer.ts`

Main analysis class with methods:

- `analyze(input: AnalysisInput)` - Main entry point
- `calculateContextMetrics()` - Token usage, compactions
- `analyzeFileAccessPatterns()` - Detect duplicate reads
- `analyzeToolUsagePatterns()` - Tool usage statistics
- `calculateEfficiencyMetrics()` - Overall efficiency scores
- `generateInsights()` - Create actionable insights

## Architecture

### Data Flow

```
Session Data (existing)
    ↓
SessionAnalyzer.analyze()
    ↓
Analysis Components:
  - Context Metrics
  - File Access Patterns
  - Tool Usage Patterns
  - Efficiency Metrics
  - Insights Generation
    ↓
SessionAnalysis Output
    ↓
UI Display (extension point)
```

### Integration Points

1. **Data Source:** Uses existing `Session` and `ParsedMessage` types from `@main/types`
2. **Location:** Placed in `src/shared/` for cross-process usage
3. **Type Safety:** Follows existing type patterns
4. **Export:** Ready for import by renderer components

## Analysis Features

### Anti-Pattern Detection

✅ **Duplicate File Reads**
- Detects files accessed multiple times
- Threshold: 3+ reads (configurable)
- Severity: medium (3-4), high (5+)

✅ **High Context Compaction**
- Tracks compaction events
- Calculates compaction rate
- Threshold: 5%+ of turns (configurable)

✅ **Tool Overuse**
- Identifies heavily used tools
- Threshold: 20+ uses (configurable)
- Detects usage patterns (sequential/parallel/mixed)

✅ **High Token Usage**
- Calculates avg tokens per turn
- Threshold: 5000+ tokens (configurable)
- Context efficiency score (0-100)

### Security Checks

✅ **Sensitive File Access**
- Detects .env, secrets.json, etc.
- Medium severity alert
- Actionable security guidance

### Efficiency Metrics

✅ **Session Efficiency**
- Token efficiency score
- File access efficiency score
- Tool usage efficiency score
- Overall efficiency (weighted average)

## Output Format

### SessionAnalysis Structure

```typescript
interface SessionAnalysis {
  sessionId: string;
  timestamp: number;
  contextMetrics: ContextUsageMetrics;
  fileAccessPatterns: FileAccessPattern[];
  toolUsagePatterns: ToolUsagePattern[];
  efficiencyMetrics: SessionEfficiencyMetrics;
  insights: AnalysisInsight[];
}
```

### Insight Structure

```typescript
interface AnalysisInsight {
  category: 'anti-pattern' | 'efficiency' | 'security' | 'performance';
  severity: 'low' | 'medium' | 'high' | 'critical';
  title: string;
  description: string;
  whyItMatters: string;      // Actionable: explains impact
  whatToDo: string;           // Actionable: specific steps
  data?: {
    file?: string;
    count?: number;
    tool?: string;
    tokens?: number;
  };
}
```

## Usage Example

### In Renderer Component

```typescript
import { SessionAnalyzer } from '@shared/utils/sessionAnalyzer';
import type { SessionAnalysis, AnalysisInsight } from '@shared/types/analysis';

// Analyze session
const analyzer = new SessionAnalyzer({
  duplicateFileThreshold: 3,
  overusedToolThreshold: 20,
});

const analysis: SessionAnalysis = analyzer.analyze({
  session: currentSession,
  messages: parsedMessages,
  chunks: chunks,
});

// Display insights
<InsightPanel insights={analysis.insights} />
<MetricsView metrics={analysis.efficiencyMetrics} />
<FileAccessChart patterns={analysis.fileAccessPatterns} />
```

## UI Display Recommendations

### Insights Panel

Display each insight with:

1. **Category icon** (🔒 security, ⚠️ anti-pattern, ⚡ efficiency, 📊 performance)
2. **Severity badge** (low/medium/high/critical)
3. **Title and description**
4. **"Why this matters" section** - Explain impact
5. **"What to do" section** - Actionable steps
6. **Related data** - Links to files/tools

### Metrics Dashboard

- Session efficiency score (0-100 gauge)
- Token efficiency bar
- File access efficiency bar
- Tool usage efficiency bar

### Visualizations

- File access frequency chart
- Tool usage distribution
- Context timeline with compaction markers
- Token usage per turn graph

## Configuration

```typescript
const options = {
  duplicateFileThreshold: 3,      // Default: 3
  overusedToolThreshold: 20,       // Default: 20
  compactionRateThreshold: 0.05,   // Default: 5%
  highTokenThreshold: 5000,         // Default: 5000
  includeSecurityChecks: true,        // Default: true
};
```

## Next Steps for Integration

### 1. Update Type Exports

Add to `src/shared/types/index.ts`:

```typescript
export * from './analysis';
```

### 2. Create UI Components

Add components in `src/renderer/components/analysis/`:

- `InsightPanel.tsx` - Display insights
- `MetricsDashboard.tsx` - Show efficiency scores
- `FileAccessChart.tsx` - Visualize patterns
- `AnalysisSettings.tsx` - Configuration UI

### 3. Add to Store

Create slice in `src/renderer/store/slices/analysisSlice.ts`:

```typescript
interface AnalysisSlice {
  analyses: Map<string, SessionAnalysis>;
  selectedSessionAnalysis: SessionAnalysis | null;
  analyzeSession: (sessionId: string) => Promise<void>;
}
```

### 4. Add API Endpoint

Add to `src/main/http/` or `src/main/ipc/`:

```typescript
ipcMain.handle('analysis:analyze', async (event, sessionId) => {
  const analysis = analyzer.analyze(/* session data */);
  return analysis;
});
```

### 5. Integrate into Session View

Add analysis panel to session detail view:

```typescript
// In SessionContextPanel or similar
{selectedSession && (
  <AnalysisPanel sessionId={selectedSession.id} />
)}
```

## Benefits Over Standalone Tool

1. **Leverages Existing Infrastructure**
   - Uses parsed session data (no re-parsing needed)
   - Integrates with existing store/state
   - Reuses UI components and styling

2. **Real-time Updates**
   - Can analyze sessions as they're loaded
   - Updates with session changes
   - Integrated into session workflow

3. **Better UX**
   - Inline insights (no separate tool needed)
   - Visual feedback in familiar UI
   - Actionable recommendations in context

4. **Extensible**
   - Easy to add new analysis types
   - Configurable per user
   - Can track trends over time

## Testing

```typescript
// Test analyzer
import { SessionAnalyzer } from '@shared/utils/sessionAnalyzer';

const analyzer = new SessionAnalyzer();
const result = analyzer.analyze(mockData);

expect(result.insights.length).toBeGreaterThan(0);
expect(result.efficiencyMetrics.overallEfficiency).toBeGreaterThanOrEqual(0);
expect(result.efficiencyMetrics.overallEfficiency).toBeLessThanOrEqual(100);
```

## Future Enhancements

1. **Trend Analysis** - Compare sessions over time
2. **Custom Rules** - User-configurable patterns
3. **Export** - Download analysis reports
4. **Auto-suggestions** - Suggest improvements in real-time
5. **Integration with Actions** - One-click fixes
6. **ML-based Detection** - Learn from user patterns

---

**Status:** Architecture complete, ready for UI integration

**Files Created:**
- `src/shared/types/analysis.ts` (4417 bytes)
- `src/shared/utils/sessionAnalyzer.ts` (13688 bytes)

**Total Lines:** ~500 lines of TypeScript

**Integration Ready:** Yes, follows project patterns
