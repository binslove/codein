"use strict";

/* ===============================
   CodeIn Frontend (API Version)
   - JWT 기반 로그인
   - Boards / Events API 연동
   - localStorage 데모 제거
================================ */

const API = "/api/v1";
const AUTH_KEY = "codein_auth";

/* ===============================
   Auth / Token Helpers
================================ */
function getAuth() {
  try {
    return JSON.parse(localStorage.getItem(AUTH_KEY)) || null;
  } catch {
    return null;
  }
}

function getToken() {
  const auth = getAuth();
  return auth?.token || null;
}

function setAuth(payload) {
  localStorage.setItem(AUTH_KEY, JSON.stringify(payload));
}

function clearAuth() {
  localStorage.removeItem(AUTH_KEY);
}

/* ===============================
   API Wrapper
================================ */
async function apiFetch(path, options = {}) {
  const token = getToken();
  const headers = options.headers || {};

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API}${path}`, {
    ...options,
    headers,
  });

  let data = null;
  try {
    data = await res.json();
  } catch {}

  if (!res.ok) {
    const msg = data?.detail || `API Error ${res.status}`;
    throw new Error(msg);
  }

  return data;
}

/* ===============================
   Roles (server side 기준)
================================ */
const ROLES = { GUEST: 0, MEMBER: 1, ADMIN: 2, SUPERADMIN: 3 };

function getRole() {
  const auth = getAuth();
  return auth?.role ?? ROLES.GUEST;
}

function hasRole(min) {
  return getRole() >= min;
}

/* ===============================
   Login / Logout
================================ */
async function login(email, password) {
  try {
    const data = await apiFetch("/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email,
        password,
        name: "x",
        student_id: "x",
        major: "x",
        generation: "x",
      }),
    });

    const payload = {
      token: data.access_token || data.token,
      role: data.role || ROLES.MEMBER,
      email,
    };

    setAuth(payload);
    return { ok: true };
  } catch (e) {
    return { ok: false, message: e.message };
  }
}

function logout() {
  clearAuth();
  location.href = "./index.html";
}

/* ===============================
   UI Binding
================================ */
function bindLoginUI() {
  const form = document.getElementById("loginForm");
  if (!form) return;

  const userEl = document.getElementById("loginUser");
  const passEl = document.getElementById("loginPass");
  const msgEl = document.getElementById("loginMsg");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = (userEl?.value || "").trim();
    const password = (passEl?.value || "").trim();

    const res = await login(email, password);
    if (!res.ok) {
      if (msgEl) msgEl.textContent = res.message;
      return;
    }
    location.href = "./index.html";
  });
}

function bindLogoutUI() {
  document.querySelectorAll('[data-auth="logout"]').forEach((el) => {
    el.addEventListener("click", (e) => {
      e.preventDefault();
      logout();
    });
  });
}

function syncAuthUI() {
  const authed = !!getAuth();

  document.querySelectorAll('[data-auth="login"]').forEach((el) => {
    el.style.display = authed ? "none" : "";
  });

  document.querySelectorAll('[data-auth="logout"]').forEach((el) => {
    el.style.display = authed ? "" : "none";
  });
}

/* ===============================
   Boards (API)
================================ */
async function loadBoardPosts(boardId) {
  return await apiFetch(`/boards/${boardId}`);
}

async function renderBoardPosts(boardId) {
  const list = document.getElementById("boardPostList");
  if (!list) return;

  try {
    const posts = await loadBoardPosts(boardId);

    if (!posts.length) {
      list.innerHTML = `<div class="card card--padded"><p class="muted">아직 게시글이 없습니다.</p></div>`;
      return;
    }

    list.innerHTML = posts
      .map((p) => {
        const date = p.created_at
          ? new Date(p.created_at).toLocaleString()
          : "";
        return `
        <div class="card card--padded">
          <div style="display:flex;justify-content:space-between;gap:10px;">
            <div>
              <div style="font-weight:800">${escapeHtml(p.title)}</div>
              <div class="muted" style="font-size:12px">
                작성자 ${p.author_id} · ${date}
              </div>
            </div>
          </div>
          <div style="margin-top:10px">
            ${escapeHtml(p.content).replace(/\n/g, "<br>")}
          </div>
        </div>`;
      })
      .join("");
  } catch (e) {
    list.innerHTML = `<div class="card card--padded"><p class="muted">${e.message}</p></div>`;
  }
}

function initBoardsCrud() {
  const form = document.getElementById("boardWriteForm");
  const openBtn = document.getElementById("openWriteBtn");
  const gate = document.getElementById("boardWriteGate");

  const qs = new URLSearchParams(location.search);
  const board = qs.get("board") === "qa" ? 3 : 2; // free=2

  const canWrite = hasRole(ROLES.MEMBER);

  if (gate) gate.style.display = canWrite ? "none" : "";
  if (openBtn) openBtn.style.display = canWrite ? "" : "none";
  if (form) form.style.display = "none";

  if (openBtn) {
    openBtn.addEventListener("click", () => {
      if (form) form.style.display = "";
      openBtn.style.display = "none";
    });
  }

  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      if (!canWrite) return alert("회원만 작성 가능합니다.");

      const title = form.querySelector("[name=title]")?.value.trim();
      const content = form.querySelector("[name=content]")?.value.trim();
      if (!title || !content) return alert("제목/내용 입력");

      try {
        await apiFetch(`/boards/${board}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ title, content }),
        });

        form.reset();
        form.style.display = "none";
        if (openBtn) openBtn.style.display = "";
        await renderBoardPosts(board);
      } catch (e) {
        alert(e.message);
      }
    });
  }

  renderBoardPosts(board);
}

/* ===============================
   Events (API)
================================ */
async function renderEvents() {
  const list = document.getElementById("eventList");
  if (!list) return;

  try {
    const events = await apiFetch("/events/");
    list.innerHTML = events
      .map(
        (e) =>
          `<li><strong>${escapeHtml(e.title)}</strong> · ${escapeHtml(
            e.start_time
          )} ~ ${escapeHtml(e.end_time)}</li>`
      )
      .join("");
  } catch (e) {
    list.innerHTML = `<li class="muted">${e.message}</li>`;
  }
}

/* ===============================
   Utils
================================ */
function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (m) => {
    return {
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#039;",
    }[m];
  });
}

/* ===============================
   Boot
================================ */
document.addEventListener("DOMContentLoaded", () => {
  syncAuthUI();
  bindLoginUI();
  bindLogoutUI();

  const page = document.body.getAttribute("data-page");

  if (page === "boards") {
    initBoardsCrud();
  }

  if (page === "calendar") {
    renderEvents();
  }
});

/* Expose for devtools */
window.getRole = getRole;
window.hasRole = hasRole;
