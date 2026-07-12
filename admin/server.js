import express from 'express';
import { spawn, execFileSync } from 'child_process';
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import 'dotenv/config';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = join(__dirname, '..');

function findPython() {
  if (process.platform === 'win32') {
    const winPath = join(PROJECT_ROOT, '.venv', 'Scripts', 'python.exe');
    if (existsSync(winPath)) return winPath;
    return 'python';
  }
  const unixPath = join(PROJECT_ROOT, '.venv', 'bin', 'python3');
  if (existsSync(unixPath)) return unixPath;
  const altPath = join(PROJECT_ROOT, '.venv', 'bin', 'python');
  if (existsSync(altPath)) return altPath;
  return 'python3';
}
const PYTHON = findPython();

const app = express();
app.use(express.json());
app.use(express.static(join(__dirname, 'public')));

// ============ Helper: 运行 Python 代码 ============

function runPython(code) {
  try {
    // Use execFileSync to avoid shell escaping issues with Chinese paths
    const result = execFileSync(
      PYTHON, ['-c', code],
      { encoding: 'utf-8', timeout: 30000, cwd: PROJECT_ROOT }
    );
    return result.trim();
  } catch (e) {
    console.error('Python exec error:', e.message);
    return JSON.stringify({ success: false, error: e.stderr || e.message });
  }
}

function parseJsonOrFallback(text) {
  try {
    // Try parsing entire output as JSON
    return JSON.parse(text);
  } catch {
    // Try to extract JSON from output
    const match = text.match(/\{[\s\S]*\}|\[[\s\S]*\]/);
    if (match) {
      try { return JSON.parse(match[0]); } catch {}
    }
    return { success: true, output: text };
  }
}

// ============ API: 模块列表 ============

app.get('/api/modules', (req, res) => {
  const code = `
import json, sys
sys.path.insert(0, ${JSON.stringify(PROJECT_ROOT)})
try:
    from office_automation.modules.registry import list_modules, init
    init()
    modules = list_modules()
    print(json.dumps([{
        "name": m.name, "title": m.title,
        "description": m.description, "enabled": m.enabled
    } for m in modules], ensure_ascii=False))
except Exception as e:
    print(json.dumps({"error": str(e)}))
  `;
  const result = runPython(code);
  res.json(parseJsonOrFallback(result));
});

// ============ API: 模块详情 ============

app.get('/api/modules/:name', (req, res) => {
  const name = req.params.name;
  const code = `
import json, sys
sys.path.insert(0, ${JSON.stringify(PROJECT_ROOT)})
try:
    from office_automation.modules.registry import get_module, init
    init()
    m = get_module("${name}")
    print(json.dumps({
        "name": m.name, "title": m.title,
        "description": m.description, "enabled": m.enabled
    }, ensure_ascii=False))
except Exception as e:
    print(json.dumps({"error": str(e)}))
  `;
  const result = runPython(code);
  res.json(parseJsonOrFallback(result));
});

// ============ API: 执行模块 ============

app.post('/api/modules/:name/execute', (req, res) => {
  const name = req.params.name;
  const { action, params, mode } = req.body;
  const finalAction = action || 'generate_report';
  const finalParams = JSON.stringify(params || {});
  const finalMode = mode || 'demo';

  const code = `
import json, sys
sys.path.insert(0, ${JSON.stringify(PROJECT_ROOT)})
try:
    from office_automation.executor import execute_module
    from office_automation.modules.registry import init
    init()
    result = execute_module(
        "${name}", "${finalAction}", ${finalParams}
    )
    print(json.dumps(result, ensure_ascii=False))
except Exception as e:
    import traceback
    print(json.dumps({
        "success": False,
        "error": str(e),
        "traceback": traceback.format_exc()
    }))
  `;

  const result = runPython(code);
  res.json(parseJsonOrFallback(result));
});

// ============ API: AI 自动化 ============

app.post('/api/ai-automate', (req, res) => {
  const { description, mode } = req.body;
  const effectiveMode = mode || 'demo';

  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.flushHeaders();

  const send = (data) => res.write(`data: ${JSON.stringify(data)}\n\n`);

  // Step 1: AI classifies intent
  const classifyCode = `
import asyncio, json, sys
sys.path.insert(0, ${JSON.stringify(PROJECT_ROOT)})
try:
    from office_automation.ai import create_provider
    provider = create_provider(mode="${effectiveMode}")
    system_prompt = '你是一个办公自动化助手。分析用户的自然语言需求，输出JSON：{"module":"模块名","action":"动作名","params":{}}。可用模块: excel, email, document, file_organizer, data_extraction, meeting_notes, invoice, scheduler, text_processor, formula, converter, pipeline, workflow, cli_extras。只输出JSON。'
    result = asyncio.run(provider.chat([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": ${JSON.stringify(description || '')}}
    ]))
    print(result)
except Exception as e:
    print(json.dumps({"module": "excel", "action": "generate_report", "params": {"title": "${description || '报表'}"}}))
  `;

  const intentRaw = runPython(classifyCode);
  let intent;
  try { intent = JSON.parse(intentRaw.trim()); } catch {
    intent = { module: 'excel', action: 'generate_report', params: { title: description || '报表' } };
  }

  send({ step: 'analyze', content: `识别为: ${intent.module}.${intent.action}` });

  // Step 2: Execute
  const execCode = `
import asyncio, json, sys
sys.path.insert(0, ${JSON.stringify(PROJECT_ROOT)})
try:
    from office_automation.executor import execute_module
    from office_automation.modules.registry import init
    init()
    result = execute_module(
        "${intent.module}", "${intent.action}", ${JSON.stringify(intent.params || {})}
    )
    print(json.dumps(result, ensure_ascii=False))
except Exception as e:
    print(json.dumps({"success": False, "error": str(e)}))
  `;

  send({ step: 'executing', content: '正在执行...' });

  const execResult = runPython(execCode);
  send({ step: 'result', content: execResult });
  send({ done: true });
  res.end();
});

// ============ API: 执行历史 ============

const HISTORY_FILE = join(PROJECT_ROOT, 'data', 'executions.json');

app.get('/api/executions', (req, res) => {
  if (existsSync(HISTORY_FILE)) {
    const data = readFileSync(HISTORY_FILE, 'utf-8');
    try { res.json(JSON.parse(data)); return; } catch {}
  }
  res.json([]);
});

// ============ 静态文件（SPA 前端） ============

app.get('*', (req, res) => {
  res.sendFile(join(__dirname, 'public', 'index.html'));
});

// ============ 启动 ============

const PORT = process.env.PORT || 4323;
app.listen(PORT, () => {
  console.log(`📋 AutoOffice 管理面板: http://localhost:${PORT}`);
});
