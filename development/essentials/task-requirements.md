# Project Task Requirements - AnkiBrain

## Success Criteria for All Feature Tasks

This document defines the **MANDATORY** success criteria that ALL feature tasks must satisfy before being marked complete in the AnkiBrain project.

### 🚨 CRITICAL REQUIREMENTS

#### Python Code Quality Requirements
- [ ] **Python Linting**: `ruff check .` passes with zero violations
- [ ] **Python Type Checking**: `mypy .` passes with zero type errors (if configured)
- [ ] **Code Formatting**: All Python files follow PEP 8 standards
- [ ] **Import Organization**: Imports are properly organized and unused imports removed

#### Application Startup Requirements  
- [ ] **Plugin Loads**: AnkiBrain plugin loads in Anki without errors
- [ ] **Startup Performance**: Application startup completes without hanging or excessive delays
- [ ] **Logging Functional**: Performance logging system generates logs without errors
- [ ] **No Startup Crashes**: No exceptions or crashes during plugin initialization

#### Anki Integration Requirements
- [ ] **Menu Integration**: AnkiBrain menu appears correctly in Anki's menu bar
- [ ] **Side Panel**: AnkiBrain side panel loads and displays properly
- [ ] **Card Hooks**: Card injection functionality works without breaking Anki's card display
- [ ] **Profile Compatibility**: Plugin works across different Anki user profiles

#### Performance Logging Requirements
- [ ] **Logging Active**: Performance logging captures timing data for all major operations
- [ ] **Log Files Created**: Log files are generated in the `logs/` directory
- [ ] **Bottleneck Detection**: Performance thresholds identify slow operations automatically
- [ ] **Structured Output**: Log entries contain actionable diagnostic information

#### External Dependencies Requirements
- [ ] **Python Environment**: Virtual environment setup works correctly
- [ ] **ChatAI Module**: External Python subprocess starts successfully (LOCAL mode)
- [ ] **API Integration**: OpenAI API key validation and usage functions properly
- [ ] **Settings Management**: User settings load, save, and persist correctly

#### Error Handling Requirements
- [ ] **Graceful Failures**: All error conditions are handled gracefully without crashing Anki
- [ ] **Error Logging**: Errors are logged with sufficient context for debugging
- [ ] **User Feedback**: Users receive appropriate feedback for error conditions
- [ ] **Recovery Paths**: Application can recover from transient errors

### 🔧 VALIDATION COMMANDS

#### Manual Testing Sequence
```bash
# 1. Code quality checks
ruff check .
ruff format --check .

# 2. Start Anki and verify:
# - AnkiBrain menu appears
# - Side panel loads without errors
# - Performance logs are generated in logs/ directory
# - No error messages in Anki's debug console

# 3. Test core functionality:
# - Switch between LOCAL and SERVER modes
# - Verify ChatAI subprocess starts (LOCAL mode)
# - Test settings save/load
# - Verify card injection doesn't break card display
```

#### Log File Verification
```bash
# Check that performance logs are being generated
ls -la logs/
tail -f logs/ankibrain_performance.log

# Verify structured logging output contains timing data
grep "duration_ms" logs/ankibrain_performance.log
grep "bottleneck" logs/ankibrain_performance.log
```

### 📋 SPECIAL CONSIDERATIONS FOR ANKIBRAIN

#### Plugin Architecture Considerations
- **Anki Compatibility**: Must work with Anki 2.1+ without breaking core functionality
- **Qt Integration**: UI components must integrate properly with Anki's Qt-based interface
- **Thread Safety**: Async operations must not block Anki's main UI thread
- **Memory Management**: Plugin must not cause memory leaks or excessive memory usage

#### ChatAI Subprocess Management
- **Process Lifecycle**: External Python processes must start, run, and terminate cleanly
- **Communication**: Inter-process communication must be reliable and performant
- **Error Recovery**: Subprocess failures must not crash the main Anki application
- **Resource Cleanup**: All subprocesses and resources must be properly cleaned up on exit

#### Performance Considerations
- **Startup Time**: Plugin initialization should not significantly delay Anki startup
- **Runtime Performance**: Plugin operations should not noticeably impact Anki's responsiveness
- **Log Overhead**: Performance logging should have minimal impact on actual performance
- **Resource Usage**: Plugin should use system resources efficiently

### 🚨 TASK COMPLETION PROTOCOL

#### Before Marking Any Feature Task Complete:
1. **Run all validation commands listed above**
2. **Test in actual Anki environment** (not just code review)
3. **Verify performance logging is working and capturing data**
4. **Check that no new errors appear in Anki's debug output**
5. **Ensure all existing functionality still works**

#### Evidence Documentation Required:
- **Linting Results**: Output from `ruff check .` showing zero violations
- **Anki Startup Test**: Screenshot or description of successful Anki startup with plugin loaded
- **Log File Evidence**: Sample of performance log output showing timing data
- **Functionality Test**: Verification that core AnkiBrain features still work

#### If Requirements Cannot Be Met:
- **Create Error Task**: If any requirement fails, create a separate error-category task to fix the issue
- **Document Blockers**: Clearly document what prevents the requirement from being met
- **Seek User Guidance**: Ask for user input if requirements seem impossible to satisfy

### 🎯 PROJECT-SPECIFIC SUCCESS METRICS

#### Startup Performance Targets
- **Total Startup Time**: < 30 seconds for LOCAL mode (including ChatAI subprocess)
- **Webview Load Time**: < 10 seconds for side panel webview initialization
- **Subprocess Start**: < 20 seconds for ChatAI external process startup
- **Settings Load**: < 2 seconds for user settings loading

#### Logging Coverage Targets
- **Timing Coverage**: All operations > 100ms should be timed and logged
- **Bottleneck Detection**: Performance thresholds should catch operations > 5 seconds
- **Error Logging**: All exceptions should be logged with full context
- **Diagnostic Data**: Logs should contain enough information to identify performance issues

---

**Document Purpose:** This file defines the quality gate for all AnkiBrain feature implementations and ensures consistent, reliable plugin behavior.

### 🎯 RECENT UPDATES

#### Comprehensive Logging Implementation (2025-09-13)
- **✅ COMPLETED**: Full performance logging system implemented to diagnose startup performance issues
- **Features Added**:
  - Project-specific performance thresholds (500ms to 30s based on operation type)
  - Structured JSON logging to `logs/ankibrain_performance.log`
  - Comprehensive startup timing throughout __init__.py, boot.py, and ExternalScriptManager
  - Automatic bottleneck detection with contextual warnings
  - Memory usage tracking (when psutil available)
  - Thread-safe logger instances with proper cleanup
- **Testing Completed**: All logging functionality verified working via comprehensive test suite
- **Performance Targets**: Thresholds configured to meet AnkiBrain-specific requirements (20s for subprocess, 10s for webview, 2s for settings, etc.)

---

**Last Updated:** 2025-09-13
**Status:** Active Standards - Comprehensive requirements for AnkiBrain plugin development with logging diagnostics