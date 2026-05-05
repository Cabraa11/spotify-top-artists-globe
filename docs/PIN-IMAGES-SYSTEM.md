# Pin images: from generation to display (first principles)

## 1. Generation (pin-generator.html)

**What happens:**
- A `<div class="custom-pin">` is created with the label (e.g. "#1 Taylor Swift").
- **html2canvas** draws that div onto a **canvas** using a **scale** factor (e.g. 2 or 6).  
  So: `canvas pixel size = (div CSS size) × scale`.
- The canvas is exported as PNG: `canvas.toDataURL('image/png')`.
- All PNGs are zipped and downloaded as **pin-images.zip**. You unzip so **pin-images/1.png … 100.png** sit next to the map.

**What we control:**
- **Quality:** Higher `scale` in html2canvas → more pixels → sharper PNG. Lower scale → smaller file, blurrier if the map then zooms in.
- **Intrinsic size:** The PNG’s width/height in pixels = (pill size in CSS pixels) × scale. So a big scale and a big pill → a **large image in pixels**.

**Output:** Files like `pin-images/21.png` with a fixed **intrinsic size** (e.g. 400×80 px or 80×24 px). There is no “display at 56px” stored in the file; only pixel dimensions.

---

## 2. Storage and path

- **pin-images/** lives next to **spotify_top100_map.html** (e.g. inside **spotify-map/**).
- The map is opened via **HTTP** (e.g. `http://localhost:8765/spotify_top100_map.html`) so the browser can load `pin-images/1.png` etc. (file:// would block that).
- No processing of the files; they’re just static PNGs.

---

## 3. Display (spotify_top100_map.html)

**What happens:**
- For each artist, the code:
  1. Creates an **`<img>`** with `src = 'pin-images/' + rank + '.png'`.
  2. Optionally sets **width/height** (attributes or CSS).
  3. Puts that `img` inside a **`<template>`**.
  4. Appends the template to a **`Marker3DInteractiveElement`** (Google Maps 3D API).
  5. Appends the marker to the **Map3DElement** (the 3D globe).

**The crucial part:**  
How does the **3D map** decide how big the marker appears on the globe?

- It is **not** documented in a way that says “we use the img’s CSS width/height.”
- In practice, the marker size appears to follow the **image’s intrinsic (natural) size** in pixels. So:
  - **Large PNG (e.g. 400×80 px)** → marker is drawn **large** on the globe.
  - **Small PNG (e.g. 80×24 px)** → marker is drawn **small**.
- Our **width/height** on the `<img>` (56×28) do **not** seem to change the 3D marker size; the map likely uses **naturalWidth / naturalHeight** (the real pixel dimensions of the PNG) when placing the marker in the 3D scene.

So:
- **High-quality (high-res) PNGs** → large intrinsic size → **markers appear too big**.
- **Small PNGs** → small intrinsic size → **markers small**, but **quality is lost** if we generate them small.

---

## 4. Why “small in CSS” doesn’t fix it

- We tried: `img.style.width = '36px'`, `maxWidth`, and `img.setAttribute('width', '56')` etc.
- The 3D marker is rendered in a different context (WebGL/3D). The library probably measures the **content’s natural size** (the PNG’s pixel dimensions) to scale the quad/sprite on the globe, and **does not** use our layout/CSS size. So changing CSS/attributes on the `<img>` doesn’t change how big the marker is drawn.

---

## 5. What we want

- **Keep high-quality PNGs:** Generate at high resolution (e.g. scale 6, full-size pill) so the **source files** are sharp.
- **Show small on the map:** The marker on the globe should be small (e.g. ~56×28 logical pixels).

So we need: **high-res source, small input to the marker**.

---

## 6. Solution: downscale at display time (keep quality, small marker)

**Idea:**  
Don’t give the 3D marker the big PNG directly. Instead:

1. Load the high-res PNG into an `<img>`.
2. When loaded, **draw it into a small canvas** (e.g. 56×28 or 112×56 for 2× sharpness).
3. Use **that canvas** (or a new img with `src = canvas.toDataURL()`) as the **marker’s image**.

Then:
- The **file** on disk stays **high-res** (good quality).
- The **image the marker sees** has **small intrinsic size** (56×28 or 112×56), so the marker is drawn **small** on the globe.
- The browser’s drawImage(scaled) does the downscale; we keep quality in the asset and only shrink at display time.

So:
- **Generation:** We can use high scale and full-size pill again (best quality).
- **Display:** In the map, for each pin we create the small canvas from the loaded high-res img and pass the small image to the marker.

No need to reduce quality when generating; we only reduce **display size** in code when creating the marker.
