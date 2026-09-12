#!/usr/bin/env python3
"""Exercise the rendered Commons site in Chromium and save review screenshots."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import json

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / '.tools' / 'review'

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT / 'site/_site')))
    Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}'
    pages = [
        'index.html', 'tas2/index.html', 'tej3-4/index.html', 'ttj3-4/index.html',
        'resources/index.html', 'tools/index.html', 'wellbeing/index.html',
        'glossary/index.html', 'about.html', 'lore/index.html',
        'lore/from-a-pen-and-paper-mark-to-a-crest.html',
        'lore/nice-as-an-iterative-design-cycle.html',
        'lore/remembering-the-port-credit-boys.html',
        'resources/nice-design-process.html', 'tools/nice-design-tool.html',
    ]
    errors = []
    failed_external = set()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={'width': 1440, 'height': 1000})
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.on('response', lambda response: errors.append(f'{response.status}: {response.url}') if response.url.startswith(base) and response.status >= 400 else None)
            page.on('requestfailed', lambda request: failed_external.add(request.url) if not request.url.startswith(base) else errors.append(f'Request failed: {request.url}'))
            for route in pages:
                assert page.goto(base + '/' + route).ok, route
                page.locator('img').evaluate_all('async (images) => { for (const image of images) image.loading = "eager"; await Promise.all(images.map(image => image.decode().catch(() => null))); }')
                page.wait_for_load_state('networkidle')
                assert page.locator('nav.navbar').count() == 1, f'Navbar: {route}'
                nav = page.locator('#navbarCollapse a.nav-link').all_text_contents()
                assert len(nav) == len(set(nav)), f'Duplicate navigation: {route}'
                assert page.locator('main').inner_text().strip(), f'Empty main: {route}'
                assert page.evaluate('getComputedStyle(document.body).fontFamily').find('Source') >= 0, f'CSS: {route}'
                broken = page.locator('img').evaluate_all('(images) => images.filter(i => i.src.startsWith(location.origin) && (!i.complete || !i.naturalWidth)).map(i => i.src)')
                assert not broken, broken
                if route.startswith('lore/') and route != 'lore/index.html':
                    themes = page.locator('.commons-lore-taxonomy')
                    assert themes.is_visible(), f'Lore themes: {route}'
                    tools = page.locator('.bs-site-tools')
                    assert tools.bounding_box()['y'] >= themes.bounding_box()['y'] + themes.bounding_box()['height'], f'Overlapping Lore tools: {route}'
                page.screenshot(path=str(OUTPUT / (route.replace('/', '-') + '.png')))

            page.goto(base + '/lore/index.html')
            page.locator('[data-bs-filter-category="Design"]').click()
            assert page.locator('[data-bs-research-item]:visible').count() == 2
            page.locator('[data-bs-clear-filters]').click()
            assert page.locator('[data-bs-research-item]:visible').count() == 3

            page.goto(base + '/glossary/index.html')
            page.locator('#bs-glossary-search').fill('25 Percent Rule')
            page.wait_for_timeout(250)
            assert page.locator('[data-bs-glossary-entry]:visible').count() == 1

            page.goto(base + '/tools/nice-design-tool.html')
            page.locator('#nice-project-title').fill('Consolidation verification')
            page.locator('#nice-situation').fill('A <test> & a design project')
            assert 'Consolidation verification' in page.locator('#nice-report').inner_text()
            assert 'A <test> & a design project' in page.locator('#nice-report').inner_text()
            assert page.locator('#nice-report test').count() == 0
            for selector, extension in [('#nice-download-md', '.md'), ('#nice-download-doc', '.doc')]:
                with page.expect_download() as downloaded:
                    page.locator(selector).click()
                download = downloaded.value
                assert download.suggested_filename.endswith(extension)
                destination = OUTPUT / download.suggested_filename
                download.save_as(destination)
                assert 'Consolidation verification' in destination.read_text(encoding='utf-8-sig')
            page.emulate_media(media='print')
            assert page.locator('#nice-report').is_visible()
            page.emulate_media(media='screen')

            page.goto(base + '/resources/nice-design-process-slides.html')
            page.wait_for_function('typeof Reveal !== "undefined" && Reveal.isReady()')
            before = page.evaluate('Reveal.getIndices().h')
            page.keyboard.press('ArrowRight')
            page.wait_for_timeout(800)
            assert page.evaluate('Reveal.getIndices().h') > before
            assert 'A modern phone' in page.evaluate('Reveal.getCurrentSlide().innerText')
            page.screenshot(path=str(OUTPUT / 'nice-slides.png'))

            page.set_viewport_size({'width': 390, 'height': 844})
            for route in ['index.html', 'lore/from-a-pen-and-paper-mark-to-a-crest.html', 'tools/nice-design-tool.html']:
                page.goto(base + '/' + route)
                page.wait_for_load_state('networkidle')
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), f'Horizontal overflow: {route}'
                page.screenshot(path=str(OUTPUT / ('mobile-' + route.replace('/', '-') + '.png')))
            page.goto(base + '/index.html')
            page.locator('.navbar-toggler').click()
            page.locator('#navbarCollapse').wait_for(state='visible')
            page.locator('#navbarCollapse a.nav-link').filter(has_text='TAS2').click()
            page.wait_for_url('**/tas2/**')
            assert not errors, errors
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    result = {'desktop_pages': len(pages), 'mobile_pages': 3, 'local_errors': errors, 'external_request_failures': sorted(failed_external)}
    (OUTPUT / 'browser-results.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
