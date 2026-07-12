// ============ State ============
let modules = [];
let moduleNames = ['excel', 'email', 'document', 'file_organizer', 'data_extraction',
  'meeting_notes', 'invoice', 'scheduler', 'text_processor', 'formula',
  'converter', 'pipeline', 'workflow', 'cli_extras'
];

const ModuleTitles = {
  excel: '📊 Excel报表生成器',
  email: '✉️ 邮件撰写发送',
  document: '📄 文档模板填充',
  file_organizer: '📁 智能文件整理',
  data_extraction: '🔍 数据提取器',
  meeting_notes: '📝 会议纪要处理器',
  invoice: '🧾 发票处理器',
  scheduler: '⏰ 定时任务管理器',
  text_processor: '📚 文本摘要翻译',
  formula: '🔢 Excel公式生成器',
  converter: '🔄 批量文档转换',
  pipeline: '🔗 自动化流水线',
  workflow: '⚙️ 工作流编排',
  cli_extras: 'ℹ️ 系统信息'
};

// ============ DOM ============
const $ = (s) => document.querySelector(s);
const $$ = (s) => document.querySelectorAll(s);

const elModuleList = $('#module-list');
const elPages = {
  welcome: $('#page-welcome'),
  module: $('#page-module'),
  result: $('#page-result'),
  history: $('#page-history'),
};
const elAiPrompt = $('#ai-prompt');
const elBtnAiRun = $('#btn-ai-run');
const elModeSelect = $('#mode-select');
const elResultLog = $('#result-log');
const elResultOutput = $('#result-output');
const elModuleDetail = $('#module-detail');
const elHistoryList = $('#history-list');

// ============ Navigation ============
function showPage(name) {
  Object.values(elPages).forEach(p => p.classList.remove('active'));
  if (elPages[name]) elPages[name].classList.add('active');
}

// ============ Load Modules ============
async function loadModules() {
  try {
    const resp = await fetch('/api/modules');
    const data = await resp.json();
    if (Array.isArray(data)) {
      modules = data;
    }
  } catch {}
  renderModuleList();
}

function renderModuleList() {
  let html = '';
  const names = moduleNames;
  names.forEach((name, i) => {
    const mod = modules.find(m => m.name === name);
    const title = mod ? mod.title : (ModuleTitles[name] || name);
    html += `<li data-module="${name}"><span class="module-num">${i + 1}</span> ${title}</li>`;
  });
  elModuleList.innerHTML = html;

  elModuleList.querySelectorAll('li').forEach(li => {
    li.addEventListener('click', () => {
      elModuleList.querySelectorAll('li').forEach(l => l.classList.remove('active'));
      li.classList.add('active');
      showModule(li.dataset.module);
    });
  });
}

// ============ Show Module ============
function showModule(name) {
  const mod = modules.find(m => m.name === name) || { name, title: ModuleTitles[name] || name, description: '' };
  showPage('module');

  elModuleDetail.innerHTML = `
    <div class="module-detail-header">
      <h2>${ModuleTitles[name] || name}</h2>
      <p class="desc">${mod.description || '办公自动化场景'}</p>
    </div>
    <div class="exec-form">
      <label>自然语言描述需求</label>
      <textarea id="module-prompt" rows="3" placeholder="描述你要做什么..."></textarea>
      <label>模式</label>
      <select id="module-mode">
        <option value="demo">Demo</option>
        <option value="real">Real</option>
      </select>
      <button class="btn-primary" onclick="executeModule('${name}')">🚀 执行</button>
    </div>
  `;
}

// ============ Execute ============
async function executeModule(name) {
  const prompt = $('#module-prompt')?.value || '执行自动化任务';
  const mode = $('#module-mode')?.value || 'demo';

  showPage('result');
  elResultLog.innerHTML = '';
  elResultOutput.innerHTML = '';

  logResult('step', `[${name}] 正在执行...`);

  try {
    const resp = await fetch(`/api/modules/${name}/execute`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ module: name, params: { description: prompt }, mode }),
    });
    const data = await resp.json();

    if (data.success) {
      logResult('success', `✅ ${data.message || '执行成功'}`);
      if (data.files && data.files.length) {
        logResult('info', '生成文件:');
        data.files.forEach(f => logResult('info', `  📄 ${f}`));
      }
      if (data.output) {
        elResultOutput.innerHTML = `<pre>${data.output}</pre>`;
      }
    } else {
      logResult('error', `❌ ${data.error || '执行失败'}`);
    }
  } catch (e) {
    logResult('error', `❌ ${e.message}`);
  }

  // Fallback demo
  logResult('info', '⚠️ 如果模块尚未实现，请先完成 Wave 3-4 的模块创建');
}

// ============ AI Automate ============
elBtnAiRun.addEventListener('click', async () => {
  const prompt = elAiPrompt.value.trim();
  if (!prompt) return;

  showPage('result');
  elResultLog.innerHTML = '';
  elResultOutput.innerHTML = '';
  elBtnAiRun.disabled = true;

  logResult('step', '🤔 AI 正在分析需求...');

  try {
    const mode = elModeSelect.value;
    const resp = await fetch('/api/ai-automate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description: prompt, mode }),
    });

    const reader = resp.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (!line.startsWith('data: ')) continue;
        try {
          const data = JSON.parse(line.slice(6));
          if (data.step === 'analyze') {
            logResult('step', `🔍 ${data.content}`);
          } else if (data.step === 'executing') {
            logResult('step', `⚙️ ${data.content}`);
          } else if (data.step === 'result') {
            logResult('success', `✅ ${data.content}`);
          } else if (data.step === 'error') {
            logResult('error', `❌ ${data.content}`);
          } else if (data.content) {
            logResult('info', data.content);
          }
        } catch {}
      }
    }
  } catch (e) {
    logResult('error', `❌ ${e.message}`);
  }

  elBtnAiRun.disabled = false;
});

// ============ Prompt Examples ============
document.querySelectorAll('.example-tag').forEach(el => {
  el.addEventListener('click', () => {
    elAiPrompt.value = el.dataset.prompt;
    elAiPrompt.focus();
  });
});

// ============ Log ============
function logResult(type, text) {
  const div = document.createElement('div');
  div.className = `log-${type}`;
  div.textContent = text;
  elResultLog.appendChild(div);
  elResultLog.scrollTop = elResultLog.scrollHeight;
}

// ============ Back ============
$('#btn-back').addEventListener('click', () => showPage('welcome'));
$('#btn-back-from-history').addEventListener('click', () => showPage('welcome'));

// ============ History ============
$('#btn-exec-history').addEventListener('click', () => {
  showPage('history');
  loadHistory();
});

async function loadHistory() {
  elHistoryList.innerHTML = '<div class="history-item">暂无执行记录</div>';
}

// ============ Init ============
loadModules();
