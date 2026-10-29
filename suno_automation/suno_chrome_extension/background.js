const API_BASE = "http://localhost:8088";
let isBusy = false;

async function reportLog(jobId, msg, step = null, status = null) {
  try {
    await fetch(`${API_BASE}/api/ext-report`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ job_id: jobId, msg, step, status })
    });
  } catch (e) {}
}

function injectIntoSunoTab(data) {
  return new Promise((resolve) => {
    function triggerClick(el) {
      if (!el) return;
      ["pointerdown", "mousedown", "mouseup", "click"].forEach((t) => {
        el.dispatchEvent(new MouseEvent(t, { bubbles: true, cancelable: true, view: window }));
      });
    }

    function setReactValue(el, value) {
      if (!el) return;
      const proto = el.tagName === "TEXTAREA"
        ? window.HTMLTextAreaElement.prototype
        : window.HTMLInputElement.prototype;
      const setter = Object.getOwnPropertyDescriptor(proto, "value")?.set;
      if (setter) setter.call(el, value);
      else el.value = value;
      el.dispatchEvent(new InputEvent("input", { bubbles: true, data: value, inputType: "insertText" }));
      el.dispatchEvent(new Event("change", { bubbles: true }));
    }

    // 1. Chuyển sang tab Advanced
    const advTab = Array.from(document.querySelectorAll('button[role="tab"], button'))
      .find((e) => e.textContent.trim() === "Advanced");
    if (advTab) {
      triggerClick(advTab);
      advTab.click();
    }

    setTimeout(() => {
      // 2. Điền Lyrics vào ô [contenteditable="true"]
      const ce = Array.from(document.querySelectorAll('[contenteditable="true"]'))
        .find((e) => e.getBoundingClientRect().width > 200);
      if (ce) {
        ce.scrollIntoView({ block: "center" });
        ce.focus();
        const sel = window.getSelection();
        const range = document.createRange();
        range.selectNodeContents(ce);
        sel.removeAllRanges();
        sel.addRange(range);
        if (!data.instrumental && data.lyrics) {
          document.execCommand("insertText", false, data.lyrics);
        } else {
          document.execCommand("delete", false, null);
        }
        ce.style.outline = "2px solid #38A169";
      }

      // 3. Điền Styles vào ô textarea (có dấu phẩy trong placeholder)
      const styleTa = Array.from(document.querySelectorAll("textarea"))
        .find((e) => (e.placeholder || "").includes(","))
        || Array.from(document.querySelectorAll("textarea")).find((e) => e.getBoundingClientRect().width > 200);
      if (styleTa) {
        styleTa.scrollIntoView({ block: "center" });
        styleTa.focus();
        setReactValue(styleTa, data.style);
        styleTa.style.outline = "2px solid #38A169";
      }

      // 4. Điền Song Title
      const inps = Array.from(document.querySelectorAll("input"))
        .filter((e) => (e.placeholder || "").toLowerCase().includes("song title"));
      const titleInp = inps[inps.length - 1];
      if (titleInp && data.title) {
        titleInp.scrollIntoView({ block: "center" });
        titleInp.focus();
        setReactValue(titleInp, data.title);
        titleInp.style.outline = "2px solid #38A169";
      }

      // 5. Bấm nút Create
      setTimeout(() => {
        const createBtns = Array.from(document.querySelectorAll("button"))
          .filter((e) => e.offsetParent !== null && e.textContent.trim().includes("Create") && e.getBoundingClientRect().width > 120);
        const btn = createBtns[createBtns.length - 1];
        if (btn && !btn.disabled) {
          btn.style.outline = "3px solid #F26835";
          triggerClick(btn);
          btn.click();
          resolve({ clicked: true });
        } else {
          resolve({ clicked: false });
        }
      }, 600);
    }, 800);
  });
}

async function pollServer() {
  if (isBusy) return;
  try {
    const res = await fetch(`${API_BASE}/api/ext-poll`);
    if (!res.ok) return;
    const data = await res.json();
    if (!data || !data.task) return;

    isBusy = true;
    const task = data.task;
    const jobId = task.job_id;
    const payload = task.payload || {};

    await reportLog(jobId, "⚡ [EXTENSION] Đã nhận lệnh trên trình duyệt Chrome chính! Đang chuyển sang tab Suno...", 2);

    let tabs = await chrome.tabs.query({ url: ["https://suno.com/*", "https://*.suno.com/*"] });
    let sunoTab = tabs[0];
    if (!sunoTab) {
      sunoTab = await chrome.tabs.create({ url: "https://suno.com/create", active: true });
      await new Promise((r) => setTimeout(r, 5000));
    } else {
      await chrome.tabs.update(sunoTab.id, { active: true });
      if (!sunoTab.url.includes("suno.com/create")) {
        await chrome.tabs.update(sunoTab.id, { url: "https://suno.com/create" });
        await new Promise((r) => setTimeout(r, 4000));
      }
    }

    await reportLog(jobId, `✍️ [EXTENSION] Đang điền bài '${payload.title}' và bấm nút Create...`, 2);

    const execRes = await chrome.scripting.executeScript({
      target: { tabId: sunoTab.id },
      world: "MAIN",
      func: injectIntoSunoTab,
      args: [payload]
    });

    const result = execRes?.[0]?.result;
    if (result && result.clicked) {
      await reportLog(jobId, "🎉 [EXTENSION] ĐÃ ĐIỀN LỜI, STYLE, TIÊU ĐỀ & BẤM NÚT CREATE TRỰC TIẾP TRÊN CHROME CHÍNH!", 3, "completed");
    } else {
      await reportLog(jobId, "✅ [EXTENSION] Đã điền dữ liệu lên tab Suno! Hãy kiểm tra nút Create.", 3, "completed");
    }
  } catch (e) {
  } finally {
    isBusy = false;
  }
}

setInterval(pollServer, 1000);
