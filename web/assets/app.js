const textEl = document.getElementById('inputText');
const btnEl = document.getElementById('synthesizeBtn');
const emotionEl = document.getElementById('emotion');
const sentimentEl = document.getElementById('sentiment');
const intensityEl = document.getElementById('intensity');
const voiceProfileEl = document.getElementById('voiceProfile');
const ssmlEl = document.getElementById('ssml');
const playerEl = document.getElementById('player');
const statusEl = document.getElementById('status');

async function synthesize() {
  const text = textEl.value.trim();
  if (!text) {
    statusEl.textContent = 'Please enter text first.';
    return;
  }

  btnEl.disabled = true;
  statusEl.textContent = 'Analyzing emotion and generating voice...';

  try {
    const payload = { text };

    const metaRes = await fetch('/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!metaRes.ok) {
      throw new Error('Failed to synthesize metadata.');
    }

    const meta = await metaRes.json();
    emotionEl.textContent = meta.emotion;
    sentimentEl.textContent = String(meta.sentiment_score);
    intensityEl.textContent = String(meta.intensity);
    voiceProfileEl.textContent = JSON.stringify(meta.voice_profile, null, 2);
    ssmlEl.textContent = meta.ssml;

    const audioRes = await fetch('/synthesize/audio', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!audioRes.ok) {
      throw new Error('Failed to synthesize audio.');
    }

    const blob = await audioRes.blob();
    const url = URL.createObjectURL(blob);
    playerEl.src = url;
    await playerEl.play().catch(() => undefined);

    statusEl.textContent = 'Done. Audio generated and ready to play.';
  } catch (err) {
    statusEl.textContent = `Error: ${err.message || err}`;
  } finally {
    btnEl.disabled = false;
  }
}

btnEl.addEventListener('click', synthesize);
