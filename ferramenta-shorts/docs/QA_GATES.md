# Quality gates (all mandatory, in this order)
0. Declare the intent of every take (HEROES) and the reference colour of every hero asset.
1. `node qa_takes.mjs 3`   TAKE INSPECTOR: cropped / too small / hidden / empty / camera-inside-geometry. Fix every FAIL before rendering.
2. `node qa_camera.mjs web/story.js`   no accidental fly-throughs (every location change is a declared cut).
3. `node qa_color.mjs pig:#ffb6d2 10 26 520 ...` + `python3 qa_color_check.py`   hero colour measured on screen.
4. Render (3 shards, RESUME=1).  5. `python3 qa_frames.py frames web/story.js --sheet flagged.jpg`   black/white/flat/blurry/glitch/flicker.
6. Review flagged frames + one contact sheet per take. Reject: deformed or clipped object/character, cropped hero, wrong colour, floating/sunk object, mirrored/cut text, empty take, camera inside geometry.
7. Re-render ONLY the rejected frames (`--rerender` deletes them; `RESUME=1 node render.mjs frames "<list>"`). Repeat 5-7 until clean.
8. Encode, then freezedetect/blackdetect/ebur128 on the MP4.
