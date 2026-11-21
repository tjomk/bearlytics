(function() {
    const script = document.currentScript;
    const site = script?.dataset?.site || '';
    const base = script.src.split('/script.js')[0];
    const currentDomain = window.location.hostname;
    const refParam = new URLSearchParams(window.location.search).get('ref');
    const getDomain = url => { try { return new URL(url).hostname; } catch { return null; } };
    const ref = [refParam, document.referrer].find(r => r && getDomain(r) !== currentDomain) || '';

    // keepalive: the request survives the navigation a link click triggers
    const send = (endpoint, qs) =>
        fetch(`${base}/${site}/${endpoint}?${qs}`, { keepalive: true });

    send('hit', `path=${encodeURIComponent(window.location.pathname)}&ref=${encodeURIComponent(ref)}`);

    // Event tracking: record one named event (clicks, downloads, submits, custom JS).
    // One recording path for every trigger — attribute, imperative call, submit.
    const track = name =>
        send('event', `name=${encodeURIComponent(name)}` +
                      `&path=${encodeURIComponent(window.location.pathname)}` +
                      `&ref=${encodeURIComponent(ref)}`);

    window.bearlytics = window.bearlytics || {};
    window.bearlytics.track = track;

    // One delegated capture-phase listener covers click and submit, including
    // elements added later. For submits, resolve from e.submitter so the
    // attribute can sit on the submit button OR the form (Enter-key submits
    // covered); never falls back to reading input values.
    const fire = e => {
        const origin = (e.type === 'submit' && e.submitter) ? e.submitter : e.target;
        const el = origin?.closest?.('[data-bearlytics-event]');
        if (el && el.dataset.bearlyticsEvent) track(el.dataset.bearlyticsEvent);
    };
    document.addEventListener('click', fire, true);
    document.addEventListener('submit', fire, true);
})();
