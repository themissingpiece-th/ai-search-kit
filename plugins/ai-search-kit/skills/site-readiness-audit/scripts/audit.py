#!/usr/bin/env python3
"""Website readiness audit for SEO & AI Search (Access / Understand / Trust).

Standard library only. Usage:
    python3 audit.py https://www.example.com/ https://www.example.com/product [--psi-key KEY] [--out result.json]

Prints a JSON report. If the sandbox cannot reach the internet, the report has
"network_blocked": true so the skill can switch to its fallback mode.
"""
import argparse, json, os, re, ssl, time
import urllib.error, urllib.parse, urllib.request
from html.parser import HTMLParser

TIMEOUT = 20
BROWSER_UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/129.0 Safari/537.36')
# Bot tokens used in robots.txt, and representative user-agent strings for the firewall test.
BOTS = {
    'Googlebot': ('Googlebot', 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'),
    'Google-Extended': ('Google-Extended', None),   # robots.txt token only, never fetches
    'Bingbot': ('bingbot', 'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'),
    'OAI-SearchBot': ('OAI-SearchBot', 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot'),
    'GPTBot': ('GPTBot', 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; GPTBot/1.1; +https://openai.com/gptbot'),
    'ChatGPT-User': ('ChatGPT-User', 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; ChatGPT-User/1.0; +https://openai.com/bot'),
    'PerplexityBot': ('PerplexityBot', 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)'),
    'ClaudeBot': ('ClaudeBot', 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; ClaudeBot/1.0; +claudebot@anthropic.com)'),
}
UA_TEST_BOTS = ['Googlebot', 'OAI-SearchBot', 'GPTBot', 'PerplexityBot', 'ClaudeBot']


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


_ctx = ssl.create_default_context()
_opener = urllib.request.build_opener(NoRedirect, urllib.request.HTTPSHandler(context=_ctx))


def fetch(url, ua=BROWSER_UA, follow=True, max_hops=6, read=True):
    """Return dict(status, final_url, chain, headers, body, ms, error)."""
    chain, cur, t0 = [], url, time.time()
    for _ in range(max_hops):
        req = urllib.request.Request(cur, headers={'User-Agent': ua, 'Accept-Language': 'th,en;q=0.8',
                                                   'Accept': 'text/html,application/xhtml+xml,*/*;q=0.8'})
        try:
            resp = _opener.open(req, timeout=TIMEOUT)
            body = resp.read(3_000_000) if read else b''
            return {'status': resp.status, 'final_url': cur, 'chain': chain, 'headers': dict(resp.headers),
                    'body': body, 'ms': int((time.time() - t0) * 1000), 'error': None}
        except urllib.error.HTTPError as e:
            if e.code in (301, 302, 303, 307, 308) and follow and e.headers.get('Location'):
                nxt = urllib.parse.urljoin(cur, e.headers['Location'])
                chain.append({'from': cur, 'status': e.code, 'to': nxt})
                cur = nxt
                continue
            body = b''
            try:
                body = e.read(200_000)
            except Exception:
                pass
            return {'status': e.code, 'final_url': cur, 'chain': chain, 'headers': dict(e.headers or {}),
                    'body': body, 'ms': int((time.time() - t0) * 1000), 'error': None}
        except Exception as e:  # network / proxy / DNS / TLS
            return {'status': None, 'final_url': cur, 'chain': chain, 'headers': {}, 'body': b'',
                    'ms': int((time.time() - t0) * 1000), 'error': f'{type(e).__name__}: {e}'}
    return {'status': None, 'final_url': cur, 'chain': chain, 'headers': {}, 'body': b'', 'ms': 0,
            'error': 'too many redirects'}


def is_network_block(r):
    err = (r.get('error') or '').lower()
    return any(s in err for s in ('tunnel connection failed', 'proxy', 'name or service not known',
                                  'nodename nor servname', 'temporary failure in name resolution',
                                  'network is unreachable'))


class PageParser(HTMLParser):
    def __init__(self, base):
        super().__init__(convert_charrefs=True)
        self.base = base
        self.title, self.in_title = '', False
        self.meta, self.links, self.hreflang, self.canonical = {}, [], [], None
        self.h = {'h1': [], 'h2': [], 'h3': []}
        self._htag, self._hbuf = None, ''
        self.tables = self.lists = self.imgs = self.imgs_no_alt = self.scripts = 0
        self.jsonld, self._in_ld, self._ld = [], False, ''
        self.text, self._skip = [], 0
        self.lang = None
        self.a_texts = []

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or '') for k, v in attrs}
        if tag == 'html':
            self.lang = a.get('lang')
        elif tag == 'title':
            self.in_title = True
        elif tag == 'meta':
            key = (a.get('name') or a.get('property') or '').lower()
            if key:
                self.meta[key] = a.get('content', '')
        elif tag == 'link':
            rel = a.get('rel', '').lower()
            if 'canonical' in rel:
                self.canonical = urllib.parse.urljoin(self.base, a.get('href', ''))
            if 'alternate' in rel and a.get('hreflang'):
                self.hreflang.append(a.get('hreflang'))
        elif tag in self.h:
            self._htag, self._hbuf = tag, ''
        elif tag == 'table':
            self.tables += 1
        elif tag in ('ul', 'ol'):
            self.lists += 1
        elif tag == 'img':
            self.imgs += 1
            if not a.get('alt', '').strip():
                self.imgs_no_alt += 1
        elif tag == 'a' and a.get('href'):
            self.links.append(urllib.parse.urljoin(self.base, a['href']))
        elif tag == 'script':
            self.scripts += 1
            if 'ld+json' in a.get('type', '').lower():
                self._in_ld, self._ld = True, ''
            else:
                self._skip += 1
        elif tag in ('style', 'noscript', 'template', 'svg'):
            self._skip += 1

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        elif tag == self._htag:
            self.h[tag].append(re.sub(r'\s+', ' ', self._hbuf).strip()[:160]); self._htag = None
        elif tag == 'script':
            if self._in_ld:
                self.jsonld.append(self._ld); self._in_ld = False
            elif self._skip:
                self._skip -= 1
        elif tag in ('style', 'noscript', 'template', 'svg') and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self._in_ld:
            self._ld += data; return
        if self._htag:
            self._hbuf += data
        if not self._skip and data.strip():
            self.text.append(data.strip())


def ld_types(blobs):
    types, errors = [], 0
    def walk(o):
        if isinstance(o, dict):
            t = o.get('@type')
            if t:
                types.extend(t if isinstance(t, list) else [t])
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    for b in blobs:
        try:
            walk(json.loads(b))
        except Exception:
            errors += 1
    return sorted(set(map(str, types))), errors


def parse_robots(txt):
    """Group robots.txt rules by user-agent (RFC 9309 / Google style)."""
    groups, cur, last_was_ua = [], None, False
    for raw in txt.splitlines():
        line = raw.split('#', 1)[0].strip()
        if ':' not in line:
            continue
        k, v = (x.strip() for x in line.split(':', 1))
        k = k.lower()
        if k == 'user-agent':
            if not last_was_ua:
                cur = {'agents': [], 'rules': []}; groups.append(cur)
            cur['agents'].append(v.lower()); last_was_ua = True
        elif k in ('allow', 'disallow') and cur is not None:
            cur['rules'].append((k, v)); last_was_ua = False
        else:
            last_was_ua = False
    return groups


def _rule_re(path):
    pat = re.escape(path).replace(r'\*', '.*')
    if pat.endswith(r'\$'):
        pat = pat[:-2] + '$'
    return re.compile(pat)


def robots_allowed(groups, token, url):
    token = token.lower()
    named = [g for g in groups if any(a != '*' and a in token for a in g['agents'])]
    chosen = named or [g for g in groups if '*' in g['agents']]
    rules = [r for g in chosen for r in g['rules']]
    u = urllib.parse.urlparse(url)
    path = (u.path or '/') + ('?' + u.query if u.query else '')
    best = None                                   # (length, is_allow)
    for kind, val in rules:
        if not val:
            continue                              # empty Disallow = allow all
        if _rule_re(val).match(path):
            cand = (len(val), kind == 'allow')
            if best is None or cand[0] > best[0] or (cand[0] == best[0] and cand[1]):
                best = cand
    return True if best is None else best[1]


def robots_check(origin, urls):
    r = fetch(origin + '/robots.txt')
    out = {'url': origin + '/robots.txt', 'status': r['status'], 'error': r['error'], 'sitemaps': [],
           'per_bot': {}, 'raw_excerpt': ''}
    if r['status'] == 200:
        txt = r['body'].decode('utf-8', 'replace')
        out['raw_excerpt'] = txt[:1500]
        out['sitemaps'] = re.findall(r'(?im)^\s*sitemap:\s*(\S+)', txt)
        groups = parse_robots(txt)
        named = {a for g in groups for a in g['agents']}
        for name, (token, _) in BOTS.items():
            out['per_bot'][name] = {
                'mentioned_by_name': token.lower() in named,
                'allowed': {u: robots_allowed(groups, token, u) for u in urls},
            }
    return out


def sitemap_check(origin, declared):
    cands = declared or [origin + '/sitemap.xml', origin + '/sitemap_index.xml']
    res = []
    for sm in cands[:3]:
        r = fetch(sm)
        body = r['body'].decode('utf-8', 'replace') if r['body'] else ''
        res.append({'url': sm, 'status': r['status'], 'error': r['error'],
                    'locs': len(re.findall(r'<loc>', body)), 'is_index': '<sitemapindex' in body})
    return res


def psi(url, key):
    api = ('https://www.googleapis.com/pagespeedonline/v5/runPagespeed?strategy=mobile&category=performance&key='
           + key + '&url=' + urllib.parse.quote(url, safe=''))
    try:
        with urllib.request.urlopen(api, timeout=60) as resp:
            d = json.loads(resp.read())
        lr = d.get('lighthouseResult', {})
        audits = lr.get('audits', {})
        crux = d.get('loadingExperience', {}).get('metrics', {})
        return {
            'performance_score': round((lr.get('categories', {}).get('performance', {}).get('score') or 0) * 100),
            'lcp_lab': audits.get('largest-contentful-paint', {}).get('displayValue'),
            'cls_lab': audits.get('cumulative-layout-shift', {}).get('displayValue'),
            'field_overall': d.get('loadingExperience', {}).get('overall_category'),
            'field_lcp_ms': crux.get('LARGEST_CONTENTFUL_PAINT_MS', {}).get('percentile'),
            'field_inp_ms': crux.get('INTERACTION_TO_NEXT_PAINT', {}).get('percentile'),
            'field_cls': crux.get('CUMULATIVE_LAYOUT_SHIFT_SCORE', {}).get('percentile'),
        }
    except Exception as e:
        return {'error': f'{type(e).__name__}: {e}'}


def page_check(url, psi_key):
    r = fetch(url)
    page = {'url': url, 'status': r['status'], 'final_url': r['final_url'], 'redirect_chain': r['chain'],
            'ms': r['ms'], 'error': r['error'], 'https': url.startswith('https://')}
    hdr = {k.lower(): v for k, v in r['headers'].items()}
    page['x_robots_tag'] = hdr.get('x-robots-tag')
    page['server_hint'] = ' / '.join(v for v in (hdr.get('server'), hdr.get('cf-ray') and 'cloudflare') if v) or None
    if r['status'] == 200 and r['body']:
        enc = 'utf-8'
        m = re.search(r'charset=([\w-]+)', hdr.get('content-type', ''))
        if m:
            enc = m.group(1)
        html = r['body'].decode(enc, 'replace')
        p = PageParser(r['final_url']); p.feed(html)
        text = ' '.join(p.text)
        types, ld_err = ld_types(p.jsonld)
        host = urllib.parse.urlparse(r['final_url']).netloc
        internal = [l for l in p.links if urllib.parse.urlparse(l).netloc == host]
        lower_links = ' '.join(p.links).lower()
        page.update({
            'title': p.title.strip()[:200], 'title_len': len(p.title.strip()),
            'meta_description': p.meta.get('description', '')[:300],
            'meta_robots': p.meta.get('robots', '') or p.meta.get('googlebot', ''),
            'canonical': p.canonical, 'canonical_is_self': (p.canonical or '').rstrip('/') == r['final_url'].rstrip('/') if p.canonical else None,
            'html_lang': p.lang, 'hreflang': p.hreflang[:20],
            'h1': p.h['h1'][:5], 'h1_count': len(p.h['h1']), 'h2': p.h['h2'][:15], 'h2_count': len(p.h['h2']),
            'visible_text_chars': len(text), 'text_sample': text[:600],
            'tables': p.tables, 'lists': p.lists, 'images': p.imgs, 'images_missing_alt': p.imgs_no_alt,
            'scripts': p.scripts, 'jsonld_types': types, 'jsonld_parse_errors': ld_err,
            'og_title': p.meta.get('og:title'), 'date_modified_hint': p.meta.get('article:modified_time') or ('dateModified' in html),
            'internal_links': len(set(internal)), 'external_links': len(set(p.links) - set(internal)),
            'links_about': any(k in lower_links for k in ('/about', 'about-us', 'เกี่ยวกับ')),
            'links_contact': any(k in lower_links for k in ('/contact', 'contact-us', 'ติดต่อ')),
            'likely_js_dependent': len(text) < 600 and p.scripts > 10,
        })
    # firewall / user-agent test
    ua_test = {}
    for name in UA_TEST_BOTS:
        rr = fetch(url, ua=BOTS[name][1], read=False)
        ua_test[name] = rr['status'] if rr['status'] else rr['error']
    page['ua_test'] = ua_test
    page['ua_blocked'] = [n for n, s in ua_test.items() if isinstance(s, int) and s in (401, 403, 429, 503)
                          and r['status'] == 200]
    page['pagespeed'] = psi(r['final_url'], psi_key) if psi_key else {'skipped': 'no PageSpeed API key — check manually at pagespeed.web.dev'}
    return page


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('urls', nargs='+')
    ap.add_argument('--psi-key', default=os.environ.get('PSI_API_KEY'), help='Google PageSpeed Insights API key (optional)')
    ap.add_argument('--out')
    a = ap.parse_args()
    urls = [u if u.startswith('http') else 'https://' + u for u in a.urls][:6]
    origin = '{0.scheme}://{0.netloc}'.format(urllib.parse.urlparse(urls[0]))
    report = {'checked_at': time.strftime('%Y-%m-%d %H:%M'), 'origin': origin, 'urls': urls,
              'network_blocked': False}
    probe = fetch(origin + '/', read=False)
    if probe['status'] is None and is_network_block(probe):
        report['network_blocked'] = True
        report['network_error'] = probe['error']
    else:
        rb = robots_check(origin, urls)
        report['robots'] = rb
        report['sitemaps'] = sitemap_check(origin, rb.get('sitemaps'))
        llms = fetch(origin + '/llms.txt', read=False)
        report['llms_txt'] = {'status': llms['status']}
        report['pages'] = [page_check(u, a.psi_key if i < 2 else None) for i, u in enumerate(urls)]
    js = json.dumps(report, ensure_ascii=False, indent=1, default=str)
    if a.out:
        open(a.out, 'w', encoding='utf-8').write(js)
    print(js)


if __name__ == '__main__':
    main()
