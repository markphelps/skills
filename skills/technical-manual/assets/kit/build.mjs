#!/usr/bin/env node
// Build a technical manual: manual.json + HTML fragments -> numbered, paginated PDF.
// usage: node build.mjs <manual-dir> [--png] [--dpi 80] [--out file.pdf]
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { execFileSync } from 'node:child_process';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const kit = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const dir = path.resolve(args.find(a => !a.startsWith('--')) || '.');
const wantPng = args.includes('--png');
const outArg = args.includes('--out') ? args[args.indexOf('--out') + 1] : null;
const problems = [];
const book = JSON.parse(fs.readFileSync(path.join(dir, 'manual.json'), 'utf8'));
const dpi = args.includes('--dpi') ? args[args.indexOf('--dpi') + 1] : '80';
// fragments may pull in generated pieces: <!--#include research/figs/hex-tiny.html-->
const read = f => bind(fs.readFileSync(path.join(dir, f), 'utf8').replace(/<!--\s*#include\s+(\S+?)\s*-->/g, (m, inc) => {
  const p = path.join(dir, inc); if (!fs.existsSync(p)) { problems.push(`${f}: include not found: ${inc}`); return ''; } return fs.readFileSync(p, 'utf8').trimEnd(); }), f);
const esc = s => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

// ---- data binding: prose and listings read from captures, so they cannot drift from the data
//   <span data-value="research/captures/x.json#tensors.0.offset" data-format="int">…</span>
//   <pre class="listing" data-include="research/captures/x.txt" data-lines="5-12" …></pre>
const bound = { values: 0, includes: 0 };
const jsonCache = {};
const lookup = (ref, where) => {
  const [file, ptr = ''] = ref.split('#');
  const p = path.join(dir, file);
  if (!fs.existsSync(p)) { problems.push(`${where}: data-value file not found: ${file}`); return undefined; }
  jsonCache[p] ??= JSON.parse(fs.readFileSync(p, 'utf8'));
  let v = jsonCache[p];
  for (const k of ptr.replace(/^\//, '').split(/[./]/).filter(Boolean)) {
    if (v == null || !(k in Object(v))) { problems.push(`${where}: data-value path not found: ${ref}`); return undefined; }
    v = v[k];
  }
  return v;
};
const fmt = (v, f) => {
  if (f === 'int' && typeof v === 'number') return v.toLocaleString('en-US');
  if (f === 'hex' && typeof v === 'number') return '0x' + v.toString(16);
  if (f === 'bytes' && typeof v === 'number') return v < 1024 ? `${v} B` : v < 1048576 ? `${(v / 1024).toFixed(1)} KiB` : v < 1073741824 ? `${(v / 1048576).toFixed(2)} MiB` : `${(v / 1073741824).toFixed(2)} GiB`;
  if (f && f.startsWith('fixed') && typeof v === 'number') return v.toFixed(+f.slice(5) || 0);
  if (f === 'pct' && typeof v === 'number') return `${(v * 100).toFixed(2)}%`;
  return typeof v === 'object' ? JSON.stringify(v) : String(v);
};
const bind = (html, where) => html
  .replace(/<(\w+)([^>]*?)\sdata-value="([^"]+)"([^>]*)>([\s\S]*?)<\/\1>/g, (m, tag, a1, ref, a2) => {
    const v = lookup(ref, where); if (v === undefined) return m;
    bound.values++;
    const f = (a1 + a2).match(/data-format="([^"]+)"/)?.[1];
    return `<${tag}${a1} data-value="${ref}"${a2}>${esc(fmt(v, f))}</${tag}>`;
  })
  .replace(/<pre([^>]*?)\sdata-include="([^"]+)"([^>]*)>([\s\S]*?)<\/pre>/g, (m, a1, inc, a2) => {
    const p = path.join(dir, inc);
    if (!fs.existsSync(p)) { problems.push(`${where}: data-include file not found: ${inc}`); return m; }
    let lines = fs.readFileSync(p, 'utf8').replace(/\n$/, '').split('\n');
    const range = (a1 + a2).match(/data-lines="(\d*)-?(\d*)"/);
    let loc = '';
    if (range) { const a = +range[1] || 1, b = range[2] ? +range[2] : (/-/.test(range[0]) ? lines.length : a); lines = lines.slice(a - 1, b); loc = `:${a}–${b}`; }
    bound.includes++;
    const attrs = a1 + a2;
    const src = /data-src=/.test(attrs) || !/class="listing"/.test(attrs) ? '' : ` data-src="${inc}${loc}"`;
    return `<pre${a1} data-include="${inc}"${a2}${src}>${esc(lines.join('\n'))}</pre>`;
  });

// ---- fonts -------------------------------------------------------------
const face = (pkg, fam, w, style = 'normal') => {
  const f = path.join(kit, 'node_modules/@fontsource', pkg, 'files');
  return ['latin', 'latin-ext'].map(sub => {
    const p = path.join(f, `${pkg}-${sub}-${w}-${style}.woff2`);
    if (!fs.existsSync(p)) return '';
    const range = sub === 'latin' ? 'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD'
      : 'U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF';
    return `@font-face{font-family:"${fam}";font-weight:${w};font-style:${style};src:url("${pathToFileURL(p)}") format("woff2");unicode-range:${range}}`;
  }).join('\n');
};
const fonts = [
  face('manrope', 'Manrope', 600), face('manrope', 'Manrope', 700),
  face('source-sans-3', 'Source Sans 3', 400), face('source-sans-3', 'Source Sans 3', 600), face('source-sans-3', 'Source Sans 3', 700),
  face('source-sans-3', 'Source Sans 3', 400, 'italic'), face('source-sans-3', 'Source Sans 3', 600, 'italic'),
  face('source-serif-4', 'Source Serif 4', 400, 'italic'),
  face('jetbrains-mono', 'JetBrains Mono', 400), face('jetbrains-mono', 'JetBrains Mono', 500), face('jetbrains-mono', 'JetBrains Mono', 700),
].join('\n');

// ---- highlight listings in node ---------------------------------------
const hljs = require('highlight.js');
const unesc = s => s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&amp;/g, '&');
const highlight = html => html.replace(/<pre class="listing"([^>]*)>([\s\S]*?)<\/pre>/g, (m, attrs, body) => {
  const lang = (attrs.match(/data-lang="([^"]+)"/) || [])[1];
  const code = unesc(body.replace(/^\n/, '').replace(/\s+$/, ''));
  let out = esc(code);
  if (lang && hljs.getLanguage(lang)) out = hljs.highlight(code, { language: lang }).value;
  return `<pre class="listing"${attrs}>${out}</pre>`;
});

// ---- assemble ----------------------------------------------------------
// measured from the reference manuals: warm = GGUF, cool = Parquet / Pi
const presets = { warm: { accent: '#c9793f', accentInk: '#7a3e12', dark: '#16120f', cover: 'dark' },
  cool: { accent: '#2a5f88', accentInk: '#24405e', dark: '#0f1826', cover: 'paper', ink: '#161d27', ink2: '#3b4452', ink3: '#5f6772', ink4: '#878e97' } };
const t = typeof book.theme === 'string' ? { ...presets[book.theme] } : { ...(presets[book.theme?.preset] || {}), ...(book.theme || {}) };
if (typeof book.theme === 'string' && !presets[book.theme]) problems.push(`manual.json: unknown theme "${book.theme}" (use "warm", "cool" or an object)`);
const partColours = ['#b5622a', '#2f5f88', '#1f7a7c', '#3c7a3c', '#6a52a8', '#b06a1c', '#a03a58', '#7a4a9a', '#56782a', '#4a6a8a'];
const parts = (book.parts || []).map((p, i) => ({ ...p, n: p.number ?? String(i + 1), colour: p.colour || partColours[i % partColours.length] }));
const themeCss = `:root{${t.accent ? `--accent:${t.accent};` : ''}${t.accentInk ? `--accent-ink:${t.accentInk};` : ''}${t.dark ? `--dark:${t.dark};` : ''}${['ink', 'ink2', 'ink3', 'ink4'].map((k, i) => t[k] ? `--ink${i ? '-' + (i + 1) : ''}:${t[k]};` : '').join('')}}`;
const coverKind = (book.cover?.style || t.cover) === 'paper' ? 'paper' : 'dark';
const darkHex = t.dark || '#16120f';
const pageBg = `@page part{background:${darkHex}}` + (coverKind === 'dark' ? `@page cover{background:${darkHex}}` : '');
const plate = book.cover?.plate ? read(book.cover.plate) : '';
const short = book.short || book.title;

let body = `<section class="cover ${coverKind}">
  <div class="meta-strings"><span class="short">${esc(short)}</span><span class="footer">${esc(short)} / Technical Manual</span></div>
  <div class="cover-top"><div class="cover-name">${esc(book.title)}</div><div class="cover-ed">Technical Manual<br>${esc(book.edition || '')}</div></div>
  <div class="plate">${plate}</div>
  <div class="cover-title"><h1>${esc(book.title)}</h1><div class="sub">Technical Manual</div><p>${esc(book.description || '')}</p>
  <div class="cover-parts">${parts.filter(p => p.n !== 'R').map(p => `<span style="--pc:${p.colour}">${esc(p.short || p.title)}</span>`).join('')}</div></div>
</section>
<section class="front" id="contents"><h1 class="plain">Contents</h1><div class="toc" data-generate="toc"></div></section>
<section class="front fm">${book.front ? read(book.front) : ''}</section>
`;
for (const p of parts) {
  body += `<div class="part" data-n="${esc(p.n)}" data-title="${esc(p.title)}" data-deck="${esc(p.deck || '')}" data-colour="${p.colour}">\n${read(p.file)}\n</div>\n`;
}
const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><title>${esc(book.title)} Technical Manual</title>
<meta name="author" content="${esc(book.author || '')}"><meta name="description" content="${esc(book.description || '')}">
<style>${fonts}</style><style>${fs.readFileSync(path.join(kit, 'manual.css'), 'utf8')}</style><style>${themeCss}${pageBg}</style>
${fs.existsSync(path.join(dir, 'extra.css')) ? `<style>${read('extra.css')}</style>` : ''}
<script>window.PagedConfig = { auto: false };</script></head><body>${highlight(body)}</body></html>`;
const buildDir = path.join(dir, 'build');
fs.mkdirSync(buildDir, { recursive: true });
const htmlPath = path.join(buildDir, 'book.html');
fs.writeFileSync(htmlPath, html);

// ---- in-page: numbering, generated matter, lint ------------------------
function prepare(short) {
  const problems = [];
    const $ = (s, r = document) => [...r.querySelectorAll(s)];
  const el = (tag, cls, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; };
  const ids = new Set();
  const figs = [];
  const toc = document.querySelector('[data-generate="toc"]');
  // front matter: "00"
  const fm = document.querySelector('section.fm');
  if (fm && fm.querySelector('[data-title]')) {
    const s = fm.querySelector('[data-title]');
    const head = el('div', 'sec-head', `<div class="sec-num">00</div><h1 class="sec-title">${s.dataset.title}</h1>${s.dataset.deck ? `<p class="deck">${s.dataset.deck}</p>` : ''}`);
    s.prepend(head);
    for (const f of $('figure.fig', fm)) problems.push(`front matter: <figure class="fig"> "${f.dataset.title || ''}" is not numbered there. Use a plain table or .swatches, or move the figure into a section.`);
  }
  for (const part of $('div.part')) {
    const n = part.dataset.n, isRef = n === 'R';
    const secs = $(':scope > section.sec', part);
    if (!secs.length) problems.push(`part ${n}: no <section class="sec"> found`);
    const opener = el('section', 'part-opener');
    opener.id = `part-${n}`;
    opener.innerHTML = `<div class="kicker">${isRef ? 'APPENDIX' : 'PART ' + n}</div><h1>${part.dataset.title}</h1>
      ${part.dataset.deck ? `<p class="deck">${part.dataset.deck}</p>` : ''}<div class="list"></div>
      <div class="foot"><span>${short} Technical Manual</span><span>${isRef ? 'Reference' : 'Part ' + n}</span></div>`;
    opener.dataset.ghost = isRef ? 'R' : String(n).padStart(2, '0');
    part.prepend(opener);
    toc.append(el('div', 'toc-part', `<i style="--pc:${part.dataset.colour}">${n}</i>${part.dataset.title}`));
    let fi = 0;
    secs.forEach((s, i) => {
      const num = `${n}.${i + 1}`;
      s.dataset.part = n;
      if (!s.id) problems.push(`section ${num} "${s.dataset.title}": missing id`);
      if (ids.has(s.id)) problems.push(`duplicate id #${s.id}`); ids.add(s.id);
      if (!s.dataset.title) problems.push(`section ${num}: missing data-title`);
      if (!s.dataset.deck) problems.push(`section ${num} "${s.dataset.title}": missing data-deck (the one-sentence italic claim under the title)`);
      s.prepend(el('div', 'sec-head', `<div class="sec-num">${num}</div><h1 class="sec-title">${s.dataset.title}</h1>${s.dataset.deck ? `<p class="deck">${s.dataset.deck}</p>` : ''}`));
      const src = s.querySelector(':scope > .sources');
      if (!src || src.textContent.trim().length < 8) problems.push(`section ${num} "${s.dataset.title}": no <p class="sources"> line. Every section names what it was written from.`);
      else if (src !== s.lastElementChild) problems.push(`section ${num}: .sources must be the last element of the section`);
      const row = `<i>${num}</i><span>${s.dataset.title}</span>`;
      const a = el('a', '', row); a.href = '#' + s.id; toc.append(a);
      const b = el('a', '', row); b.href = '#' + s.id; opener.querySelector('.list').append(b);
      for (const f of $('figure.fig', s)) {
        fi++; const fnum = `${n}.${fi}`;
        if (!f.id) f.id = `fig-${fnum.replace('.', '-')}`;
        if (ids.has(f.id)) problems.push(`duplicate id #${f.id}`); ids.add(f.id);
        const cap = f.querySelector(':scope > figcaption');
        const lead = cap?.querySelector('b')?.textContent.trim().replace(/[.:]$/, '');
        if (!cap) problems.push(`Fig. ${fnum}: no <figcaption>`);
        else if (!lead) problems.push(`Fig. ${fnum}: caption must open with a bold finding, <b>What the figure shows.</b>`);
        if (!f.dataset.title) problems.push(`Fig. ${fnum}: missing data-title`);
        if (!f.dataset.tag) problems.push(`Fig. ${fnum}: missing data-tag (kind and provenance, e.g. "byte layout · real file", "measured", "spec §3.2")`);
        const frame = el('div', 'fig-frame'), fb = el('div', 'fig-body');
        for (const c of [...f.childNodes]) if (c !== cap) fb.append(c);
        frame.append(el('div', 'fig-head', `<span><span class="fig-no">Fig. ${fnum}</span><span class="fig-title">${f.dataset.title || ''}</span></span><span>${f.dataset.tag || ''}</span>`), fb);
        f.prepend(frame);
        f.dataset.num = fnum;
        figs.push({ part: n, partTitle: part.dataset.title, num: fnum, id: f.id, lead: lead || f.dataset.title || '' });
      }
    });
  }
  for (const part of $('div.part')) part.replaceWith(...part.childNodes);
  // listings
  for (const pre of $('pre.listing')) {
    const w = el('div', 'listing');
    const d = pre.dataset;
    w.innerHTML = `<div class="listing-head"><b>${d.name || ''}</b><span>${d.src || ''}</span><span class="lang">${d.lang || ''}</span></div>`;
    if (!d.src) problems.push(`listing "${d.name || pre.textContent.slice(0, 30)}": missing data-src (file path, line range or commit it was taken from; or "written for this manual")`);
    pre.replaceWith(w); pre.className = ''; w.append(pre);
  }
  // references
  for (const a of $('a.xref, a.figref')) {
    const id = (a.getAttribute('href') || '').slice(1);
    const target = id && document.getElementById(id);
    if (!target) { problems.push(`broken reference: <a href="#${id}">${a.textContent}</a>`); a.removeAttribute('class'); continue; }
    if (a.classList.contains('figref')) { a.textContent = `Fig. ${target.dataset.num || '?'}`; }
  }
  // index of figures
  const fx = document.querySelector('[data-generate="figure-index"]');
  if (fx) { fx.classList.add('fig-index'); let last = null;
    for (const f of figs) { if (f.part !== last) { fx.append(el('h4', '', f.part === 'R' ? 'Reference' : `Part ${f.part} · ${f.partTitle}`)); last = f.part; }
      const a = el('a', '', `<i>${f.num}</i><span>${f.lead}</span>`); a.href = '#' + f.id; fx.append(a); } }
  // svg arrowheads
  const defs = el('div'); defs.innerHTML = `<svg width="0" height="0" style="position:absolute"><defs>
    <marker id="tm-arrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse"><path d="M0 .6 7.4 4 0 7.4z" fill="#56504a"/></marker>
    <marker id="tm-arrow-err" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse"><path d="M0 .6 7.4 4 0 7.4z" fill="#a03a58"/></marker>
    <marker id="tm-arrow-data" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="4.2" markerHeight="4.2" orient="auto-start-reverse"><path d="M0 .6 7.4 4 0 7.4z" fill="#56504a"/></marker></defs></svg>`;
  document.body.append(defs.firstChild);
  // prose lint: things this style never does
  const text = $('section.sec, section.fm').map(s => s.textContent).join('\n');
  const banned = [/\bseamless(ly)?\b/i, /\bpowerful\b/i, /\brobust\b/i, /\bblazing(ly)?\b/i, /\bleverag(e|es|ing)\b/i, /\bdelve\b/i, /\bit'?s worth noting\b/i, /\bin today'?s\b/i, /\bgame.chang/i, /\bunder the hood\b/i, /\bsimply put\b/i];
  for (const re of banned) { const m = text.match(re); if (m) problems.push(`prose: "${m[0]}" reads as filler. State the mechanism or the number instead.`); }
  const notes = [];
  for (const s of $('section.sec')) {
    if (s.dataset.part === 'R') continue;
    if (!s.querySelector('figure.fig, table, .listing, pre.listing, pre.term')) problems.push(`section "${s.dataset.title}": no figure, table or listing. Every section shows something.`);
  }
  const ill = $('figure.fig').filter(f => /illustrative/i.test(f.dataset.tag || '')).length;
  if (ill) notes.push(`${ill} figure(s) tagged illustrative: each must be one a capture could not produce, and its caption must say so.`);
  return { problems, notes, figures: figs.length, sections: $('section.sec').length };
}

function inspect() {
  const out = [];
  const pages = [...document.querySelectorAll('.pagedjs_page')];
  pages.forEach((pg, i) => {
    const area = pg.querySelector('.pagedjs_page_content'); if (!area) return;
    const r = area.getBoundingClientRect();
    if (pg.querySelector('section.cover, section.part-opener') || !pg.querySelector('section.sec, section.fm')) return;
    for (const e of area.querySelectorAll('.fig-frame, table, .listing, pre, .callout, .strip, .hex, svg')) {
      const b = e.getBoundingClientRect();
      if (b.width && b.right > r.right + 1.5) out.push(`page ${i + 1}: <${e.tagName.toLowerCase()} class="${e.getAttribute('class') || ''}"> is ${Math.round(b.right - r.right)}px wider than the text block`);
      if (b.height && b.bottom > r.bottom + 2) out.push(`page ${i + 1}: <${e.tagName.toLowerCase()} class="${e.getAttribute('class') || ''}"> runs ${Math.round(b.bottom - r.bottom)}px past the bottom margin (too tall for one page: split it or shrink it)`);
    }
    for (const e of area.querySelectorAll('figure.fig[data-split-to], .listing[data-split-to], .callout[data-split-to]')) out.push(`page ${i + 1}: ${e.className.split(' ')[0]} is split across pages`);
    for (const e of area.querySelectorAll('.strip > *, .cells > *, .flow > div')) {
      if (e.scrollWidth > e.clientWidth + 1.5) out.push(`page ${i + 1}: text "${e.textContent.trim().slice(0, 28)}" does not fit its box in a .${e.parentElement.className.split(' ')[0]} (widen the box, shorten the label, or move the label beside it)`);
    }
    for (const svg of area.querySelectorAll('svg')) {
      const sb = svg.getBoundingClientRect();
      const ts = [...svg.querySelectorAll('text')].map(t => ({ s: t.textContent.trim(), b: t.getBoundingClientRect() })).filter(t => t.s && t.b.width);
      const fig = svg.closest('figure')?.dataset.num;
      for (const t of ts) if (t.b.right > sb.right + 2 || t.b.left < sb.left - 2) out.push(`page ${i + 1}${fig ? ` Fig. ${fig}` : ''}: SVG text "${t.s.slice(0, 30)}" runs outside the drawing`);
      let hits = 0;
      for (let a = 0; a < ts.length && hits < 3; a++) for (let b = a + 1; b < ts.length && hits < 3; b++) {
        const A = ts[a].b, B = ts[b].b;
        const w = Math.min(A.right, B.right) - Math.max(A.left, B.left), h = Math.min(A.bottom, B.bottom) - Math.max(A.top, B.top);
        if (w > 2 && h > 2 && w * h > 0.2 * Math.min(A.width * A.height, B.width * B.height)) { hits++; out.push(`page ${i + 1}${fig ? ` Fig. ${fig}` : ''}: SVG labels overlap: "${ts[a].s.slice(0, 24)}" and "${ts[b].s.slice(0, 24)}"`); }
      }
    }
    const kids = area.querySelectorAll('section.sec > *:not(.sec-head), section.fm > *');
    const used = [...kids].reduce((m, k) => Math.max(m, k.getBoundingClientRect().bottom), r.top) - r.top;
    const last = !pages[i + 1] || pages[i + 1].querySelector('.sec-head, section.part-opener');
    const pct = Math.round(used / r.height * 100);
    if (!last && pct < 70) out.push(`page ${i + 1}: only ${pct}% full mid-section (a tall unbreakable block was pushed to the next page; reorder blocks or split the big one)`);
    if (last && !area.querySelector('.sec-head') && pct < 14) out.push(`page ${i + 1}: only the last ${pct}% of a section spills onto this page. Tighten a figure or move a block so it fits on the previous page, or add the detail the section is missing; do not delete sourced facts to fix layout.`);
  });
  return { pages: pages.length, layout: out };
}

// ---- render ------------------------------------------------------------
const { chromium } = require('playwright-core');
async function launch() {
  const root = process.env.PLAYWRIGHT_BROWSERS_PATH || '';
  const found = root && fs.existsSync(root) ? fs.readdirSync(root).filter(d => /^chromium-\d+$/.test(d)).map(d => path.join(root, d, 'chrome-linux/chrome')).filter(fs.existsSync) : [];
  const cands = [process.env.CHROME_PATH, ...found, '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser'].filter(Boolean);
  try { return await chromium.launch(); } catch {}
  for (const c of cands) { if (fs.existsSync(c)) { try { return await chromium.launch({ executablePath: c }); } catch {} } }
  throw new Error('No Chromium found. Run `npx playwright-core install chromium` in the kit folder, or set CHROME_PATH.');
}
const browser = await launch();
const page = await browser.newPage();
page.on('pageerror', e => problems.push('page error: ' + e.message));
await page.goto(pathToFileURL(htmlPath).href);
await page.evaluate(() => document.fonts.ready);
const prep = await page.evaluate(prepare, short);
problems.push(...prep.problems);
await page.addScriptTag({ path: path.join(kit, 'node_modules/pagedjs/dist/paged.polyfill.js') });
await page.evaluate(async () => { await window.PagedPolyfill.preview(); });
await page.evaluate(() => document.fonts.ready);
const info = await page.evaluate(inspect);
const pdfPath = path.resolve(outArg || path.join(dir, `${(book.slug || book.title).replace(/[^\w.-]+/g, '-')}-Technical-Manual.pdf`));
await page.pdf({ path: pdfPath, preferCSSPageSize: true, printBackground: true, outline: true, tagged: false });
await browser.close();

if (wantPng) {
  const pd = path.join(buildDir, 'pages'); fs.rmSync(pd, { recursive: true, force: true }); fs.mkdirSync(pd, { recursive: true });
  try { execFileSync('pdftoppm', ['-r', dpi, '-png', pdfPath, path.join(pd, 'p')]); console.log(`page images: ${pd}`); }
  catch { console.log('pdftoppm not available, so no page images were written. Install Poppler (macOS: brew install poppler; Debian/Ubuntu: apt install poppler-utils) and rebuild with --png.'); }
}
console.log(`${pdfPath}\n${info.pages} pages · ${prep.sections} sections · ${prep.figures} figures · ${bound.values} bound values · ${bound.includes} included listings`);
const perPage = prep.figures / Math.max(1, info.pages);
if (info.pages > 20 && perPage < 0.4) prep.notes.push(`${prep.figures} figures in ${info.pages} pages (${perPage.toFixed(2)} per page): the style wants about one every two pages.`);
for (const n of prep.notes) console.log('note: ' + n);
const all = [...problems, ...info.layout];
if (all.length) { console.log(`\n${all.length} problem(s) to fix:`); for (const p of all) console.log(' - ' + p); process.exitCode = 1; }
else console.log('checks passed: sources, captions, references, layout');
