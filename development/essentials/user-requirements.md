# User Requirements for AnkiBrain

## Project Scope Definition

This document defines the **ONLY** changes requested by the user for the AnkiBrain project.

### 🎯 Primary Requirements

**1. Add support for ChatGPT 5 and 5 mini models**

**2. Add comprehensive logging to diagnose startup performance issues**

### Scope Boundaries

**✅ WHAT TO IMPLEMENT:**
- Add ChatGPT 5 model support to the application
- Add ChatGPT 5 mini model support to the application
- Ensure these models integrate with existing functionality
- **NEW:** Implement comprehensive logging throughout the codebase, especially for startup processes
- **NEW:** Add performance timing and bottleneck detection for startup diagnostics
- **NEW:** Create structured logging output for analyzing slow startup issues

**❌ WHAT NOT TO IMPLEMENT:**
- No other model additions unless explicitly requested
- No UI changes beyond what's required for the new models or logging
- No feature additions beyond model support and logging diagnostics
- No refactoring of existing code unless required for model integration or logging implementation
- No optimization or performance improvements unless required for model support or logging functionality

### Implementation Notes

- This scope includes both the original ChatGPT model requirements and the new logging requirements
- The logging implementation is specifically focused on diagnosing startup performance problems
- Any additional changes or features require explicit user authorization
- Focus implementation on adding the two ChatGPT model variants and comprehensive performance logging
- Maintain compatibility with existing functionality

### Success Criteria

**ChatGPT Model Support:**
- [x] ChatGPT 5 model is available and functional in the application (model identifier: `gpt-5`)
- [x] ChatGPT 5 mini model is available and functional in the application (model identifier: `gpt-5-mini`) 
- [x] Both models integrate seamlessly with existing features
- [x] Frontend UI already includes dropdown options for both ChatGPT 5 models in Settings screen
- [x] Backend ChatAI system supports dynamic model configuration via settings.json
- [x] Both LOCAL and SERVER modes support the new model identifiers

**Comprehensive Logging Implementation:**
- [x] Performance logging utility module created (performance_logger.py)
- [x] Startup timing added to __init__.py and boot.py
- [x] Performance logging integrated into AnkiBrainModule startup sequence
- [x] Logging added to ExternalScriptManager for subprocess timing diagnostics
- [x] Structured log output with timing data, bottleneck detection, and diagnostic context
- [x] Log files generated in logs/ directory for startup analysis
- [x] Performance thresholds configured to identify bottlenecks automatically
- [x] Project-specific performance thresholds configured based on AnkiBrain requirements
- [x] Comprehensive testing completed - all logging functionality verified working
- [x] Bottleneck detection active with appropriate thresholds (500ms-30s based on operation type)

**General Requirements:**
- [ ] Application builds successfully
- [ ] Application runs without errors
- [ ] All existing functionality remains intact
- [ ] Logging does not negatively impact application performance
- [ ] Log output provides actionable insights for startup performance diagnosis

---

**Document Purpose:** This file serves as the authoritative reference for implementation scope and prevents scope creep during development.

**Last Updated:** 2025-09-13
**Status:** Active Requirements - Updated to include comprehensive logging for startup diagnostics